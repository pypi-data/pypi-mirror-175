from openapi_client import ExperimentMetricEntry
from openapi_client import ResponseExperimentInfo
from tensorflow import keras
import numpy as np
import logging
from typing import Optional, Union
import sys
import time
import os
import shortuuid
import six
from trumpet_client.launch.CRUD_API import API as TrumpetApi
import re
import atexit
import signal

MODE_TEST = "TEST"
MODE_NOT_STARTED = "NOT_STARTED"
MODE_LOCAL = "LOCAL"
MODE_MANAGED = "MANAGED"

SEND_INTERVAL_IN_SEC = 10

METRIC_KEY_REGEX = re.compile("^[a-zA-Z0-9/_-]+$")

class TrumpetRun(object):
    class ExitHook(object):
        def __init__(self, orig_exit):
            self.orig_exit = orig_exit
            self.exit_code = 0

        def exit(self, code=0):
            self.exit_code = code
            self.orig_exit(code)

    __slots__ = [
        "api",
        "_mode",
        "_collectors",
        "_sender",
        "_progress_updater",
        # "hyperparameters",
        "_experiment",
        "_logger",
        "_user_metric_collector",
        "_exit_hook",
        "_tensorboard_collector",
    ]

    def __init__(self) -> None:
        self.api = TrumpetApi()
        self._experiment = self._get_experiment_from_environment()
        # self.hyperparameters = HyperparametersController(self.api, self._experiment)
        self._mode = MODE_NOT_STARTED if self._experiment is None else MODE_MANAGED

        # self._user_metric_collector = UserMetricCollector()
        self._exit_hook = self.ExitHook(sys.exit)

    def _get_experiment_from_environment(self) -> Optional[ResponseExperimentInfo]:
        """Detect experiment from environment variables

        In a Trumpet-managed experiment, these variables will be defined.
        """
        experiment_id = os.environ.get("VESSL_EXPERIMENT_ID", None)
        access_token = os.environ.get("VESSL_ACCESS_TOKEN", None)

        if experiment_id is None or access_token is None:
            return None

        self.api.configure_access_token(access_token)
        try:
            return self.api.experiment_read_by_idapi(experiment_id=experiment_id)
        except TrumpetException:
            return None

    def _get_experiment_from_args(
        self,
        experiment_number,
        message: str = None,
        # hyperparameters: Hyperparameters = None,
    ) -> ResponseExperimentInfo:
        """Get or create a local experiment

        If experiment is specified, use it. Otherwise, create a new experiment.
        """
        # Create a new experiment
        if experiment_number is None:
            from vessl.experiment import create_local_experiment

            experiment = create_local_experiment(
                # message=message, hyperparameters=hyperparameters
                message=message
            )
            logger.debug(f"Created experiment {experiment.id}")
            return experiment

        # Continue with previous experiment
        from vessl.experiment import read_experiment

        experiment = read_experiment(experiment_number)
        if not experiment.is_local or experiment.local_execution_spec is None:
            raise TrumpetException(
                f"{experiment.number}: cannot use Trumpet-managed experiment."
            )
        if experiment.status != "running":
            raise TrumpetException(
                f"{experiment.number}: experiment must be running."
            )

        return experiment

    def _signal_handler(self, signo, frames):
        sys.exit(130)  # job was terminated by the owner

    def _start(self):
        """Start sender and register hooks"""
        self._sender.start()

        sys.exit = self._exit_hook.exit
        atexit.register(self._stop)
        signal.signal(signal.SIGINT, self._signal_handler)
        signal.signal(signal.SIGTERM, self._signal_handler)

    def _stop(self):
        """Stop sender and restore hooks"""
        if self._mode != MODE_LOCAL:
            return

        self._sender.stop()

        sys.exit = self._exit_hook.orig_exit
        self.api.local_experiment_finish_api(
            self._experiment.id,
            # local_experiment_finish_api_input=LocalExperimentFinishAPIInput(
            #     exit_code=self._exit_hook.exit_code
            # ),
        )

    def _send_without_collector(self, payloads):
        """Send metrics without using the collector

        In a Trumpet-managed experiment, metrics are sent immediately instead of being queued.
        """
        assert self._mode == MODE_MANAGED
        res = self.api.experiment_metrics_update_api(
            self._experiment.id,
            # experiment_metrics_update_api_input=ExperimentMetricsUpdateAPIInput(
            #     metrics=payloads
            # ),
        )
        if res.rejected:
            logger.warning(f"{res.rejected} payloads(s) were rejected.")

    def init(
        self,
        experiment_number=None,
        message: str = None,
        tensorboard: bool = False,
        hp: dict = None,
        **kwargs,
    ):
        """Main function to setup Trumpet in a local setting

        If this is a Trumpet-managed experiment or vessl.init has already been called,
        this will do nothing.

        Args:
            experiment_number (str | int): experiment name or number
            message (str): experiment message
            tensorboard (bool): enable tensorboard integration. It is important to note
              that `vessl.init` must be called **before** initializing the writer
              (`tf.summary.create_file_writer` for TF2, SummaryWriter for PyTorch, etc).
            hp (dict): hyperparameters
        """
        if self._mode == MODE_NOT_STARTED:
            print(f"Initializing a new experiment...")
            self.api.set_configurations(
                organization_name=kwargs.get("organization_name"),
                project_name=kwargs.get("project_name"),
            )

            if hp:
                self.hyperparameters.update_items(hp)

            self._experiment = self._get_experiment_from_args(
                experiment_number,
                message,
                self.hyperparameters.as_list_of_dict(),
            )
            self._mode = MODE_LOCAL
            self.hyperparameters.configure(self.api, self._experiment)

            print(
                f"Connected to {self._experiment.number}.\n"
                f"For more info: {Endpoint.experiment.format(self._experiment.organization.name, self._experiment.project.name, self._experiment.number)}"
            )

            # For testing
            if "is_test" in kwargs and kwargs["is_test"]:
                return

            gpu_count = self._experiment.local_execution_spec.gpu_count or 0
            self._user_metric_collector = UserMetricCollector()
            collectors = [
                IOCollector(),
                SystemMetricCollector(gpu_count),
                self._user_metric_collector,
            ]
            self._sender = Sender(self.api, self._experiment.id, collectors)
            self._start()

        if self._mode == MODE_MANAGED:
            if hp is None:
                return
            self.hyperparameters.update(hp)

        if tensorboard:
            integrate_tensorboard()

    def upload(self, path: str):
        """Upload output files

        Args:
            path (str): path to upload
        """
        if self._mode == MODE_NOT_STARTED:
            logger.warning("Invalid. Use `vessl.init()` first.")
            return

        from vessl.experiment import upload_experiment_output_files

        upload_experiment_output_files(self._experiment.number, path)

    def finish(self):
        """Teardown Trumpet settings

        Use this function to stop tracking your experiment mid-script. If not called,
        tracking is stopped automatically upon exit.

        Args:
            path (str): path to upload
        """
        if self._mode == MODE_NOT_STARTED:
            logger.warning("Invalid. Use `vessl.init()` first.")
            return

        if self._mode == MODE_MANAGED:
            return

        self._stop()
        experiment_number = self._experiment.number
        self._mode = MODE_NOT_STARTED
        self._experiment = None
        print(f"Experiment {experiment_number} completed.")

    def log(
        self,
        payload: Dict[str, Any],
        step: Optional[int] = None,
        ts: Optional[float] = None,
    ):
        """Log metrics to Trumpet

        Args:
            payload (Dict[str, Any]): to log a scalar, value should be a number. To
                log an image, pass a single image or a list of images (type `vessl.util.image.Image`).
            step (int): step.
        """
        if self._mode == MODE_NOT_STARTED:
            logger.warning("Invalid. Use `vessl.init()` first.")
            return

        if ts is None:
            ts = time.time()

        scalar_dict = {}
        media_dict = {}

        for k, v in payload.items():
            if isinstance(v, list):
                if all(isinstance(i, Image) for i in v) or all(
                    isinstance(i, Audio) for i in v
                ):
                    media_dict[k] = v
            elif isinstance(v, Image) or isinstance(v, Audio):
                media_dict[k] = [v]
            else:
                scalar_dict[k] = v

        # Update step if step is specified. If a scalar is defined but step wasn't,
        # step will be autoincremented.
        if scalar_dict or step is not None:
            self._user_metric_collector.handle_step(step)

        if media_dict:
            self._update_media(media_dict, ts)

        if scalar_dict:
            self._update_metrics(scalar_dict, ts)

    # This should mirror app/influx/metric_schema.go > `isValidMetricKey`
    def _is_metric_key_valid(self, key: str):
        if not METRIC_KEY_REGEX.match(key):
            return False
        if key.startswith("/") or key.endswith("/"):
            return False
        for i in range(1, len(key)):
            if key[i] == "/" and key[i - 1] == "/":
                return False
        return True

    def _update_metrics(self, payload: Dict[str, Any], ts: float):
        invalid_keys = [k for k in payload.keys() if not self._is_metric_key_valid(k)]
        if invalid_keys:
            logger.warning(
                f"Invalid metric keys: {' '.join(invalid_keys)}. This payload will be rejected."
            )

        payloads = [self._user_metric_collector.build_metric_payload(payload, ts)]
        if self._mode == MODE_MANAGED:
            self._send_without_collector(payloads)
            return self._user_metric_collector.step
        return self._user_metric_collector.log_metrics(payloads)

    def _update_media(
        self,
        payload: Dict[str, Union[List[Image], List[Audio]]],
        ts: float,
    ):
        media_type, set_media_type = None, False
        path_to_caption = {}
        for media in payload.values():
            for medium in media:
                path = os.path.basename(medium.path)
                path_to_caption[path] = medium.caption
                if not set_media_type:
                    if not isinstance(medium, Image) and not isinstance(medium, Audio):
                        raise InvalidTypeError(
                            f"Invalid payload type error: {type(medium)}"
                        )
                    else:
                        media_type = type(medium).__name__
                        set_media_type = True

        from vessl.volume import copy_volume_file

        files = copy_volume_file(
            source_volume_id=None,
            source_path=os.path.join(VESSL_MEDIA_PATH, ""),
            dest_volume_id=self._experiment.experiment_plot_volume,
            dest_path="/",
        )

        for media in payload.values():
            for medium in media:
                medium.flush()

        plot_files = []
        if files:
            plot_files = [
                {
                    "step": None,
                    "path": file.path,
                    "caption": path_to_caption[file.path],
                    "timestamp": ts,
                }
                for file in files
                if file.path in path_to_caption
            ]

        payloads: List[ExperimentMetricEntry] = []
        for f in plot_files:
            payload = {}
            if media_type == Image.__name__:
                payload = {VESSL_PLOTS_FILETYPE_IMAGE: f}
            elif media_type == Audio.__name__:
                payload = {VESSL_PLOTS_FILETYPE_AUDIO: f}
            payloads.append(
                self._user_metric_collector.build_media_payload(payload, ts)
            )

        if self._mode == MODE_MANAGED:
            self._send_without_collector(payloads)
        else:
            self._user_metric_collector.log_media(payloads)

    def progress(self, value: float):
        """Update experiment progress

        Args:
            value (float): progress value as a decimal between 0 and 1
        """
        if self._experiment is None:
            logger.warning("Invalid. Use `vessl.init()` first.")
            return

        if not 0 < value <= 1:
            logger.warning(f"Invalid progress value {value}. (0 < value <= 1)")
            return

        if not hasattr(self, "_progress_updater"):
            # Do not initialize in init() since ProgressUpdater might not be used at all
            self._progress_updater = ProgressUpdater(self.api, self._experiment.id)
            self._progress_updater.start()

        self._progress_updater.update(value)
        logger.debug(f"Experiment progress: {value}")


TRUMPET_MEDIA_PATH = "trumpet-media"
TRUMPET_IMAGE_PATH = "images"
TRUMPET_AUDIO_PATH = "audio"
TRUMPET_PLOTS_FILETYPE_IMAGE = "image"
TRUMPET_PLOTS_FILETYPE_IMAGES = "images"
TRUMPET_PLOTS_FILETYPE_AUDIO = "audio"

TRUMPET_LOG_LEVEL_DEBUG = "DEBUG"
TRUMPET_LOG_LEVEL_INFO = "INFO"
TRUMPET_LOG_LEVEL_WARNING = "WARNING"
TRUMPET_LOG_LEVEL_ERROR = "ERROR"
TRUMPET_LOG_LEVEL_LEVELS = [
    TRUMPET_LOG_LEVEL_DEBUG,
    TRUMPET_LOG_LEVEL_INFO,
    TRUMPET_LOG_LEVEL_WARNING,
    TRUMPET_LOG_LEVEL_ERROR,
]

TRUMPET_LOG_LEVEL = (
    os.environ.get("TRUMPET_LOG")
    if os.environ.get("TRUMPET_LOG") in TRUMPET_LOG_LEVEL_LEVELS
    else TRUMPET_LOG_LEVEL_WARNING
)

LEVEL_MAP = {
    logging.FATAL: "F",  # FATAL is alias of CRITICAL
    logging.ERROR: "E",
    logging.WARN: "W",
    logging.INFO: "I",
    logging.DEBUG: "D",
}

class Formatter(logging.Formatter):
    def format(self, record: logging.LogRecord):
        level = LEVEL_MAP.get(record.levelno, "?")

        try:
            formatted_msg = "%s" % (record.msg % record.args)
        except TypeError:
            formatted_msg = record.msg

        record_time = time.localtime(record.created)
        record_message = [
            (
                "%c%02d%02d %02d:%02d:%02d.%06d %s %s:%d] %s"
                % (
                    level,
                    record_time.tm_mon,
                    record_time.tm_mday,
                    record_time.tm_hour,
                    record_time.tm_min,
                    record_time.tm_sec,
                    (record.created - int(record.created)) * 1e6,
                    record.process if record.process is not None else "?????",
                    record.filename,
                    record.lineno,
                    line,
                )
            )
            for line in formatted_msg.split("\n")
        ]
        record_message = "\n".join(record_message)
        record.getMessage = lambda: record_message
        return super().format(record)


class TrumpetLogger(object):
    def __init__(self):
        self._logger = logging.getLogxger(__name__)
        self._handler: Optional[logging.Handler] = None

        self.set_level(TRUMPET_LOG_LEVEL)  # TODO: autodiscover from config
        self.set_io(sys.stderr)

    def set_io(self, io):
        if self._handler:
            self._logger.removeHandler(self._handler)

        self._handler = logging.StreamHandler(stream=io)
        self._handler.setFormatter(Formatter())
        self._logger.addHandler(self._handler)

    def set_level(self, level):
        self._logger.setLevel(level)


_trumpet_logger = TrumpetLogger()

logger = _trumpet_logger._logger
set_log_io = _trumpet_logger.set_io
set_log_level = _trumpet_logger.set_level

from importlib import import_module

__VERSION__ = "0.1.49"

DEFAULT_ERROR_MESSAGE = (
    "An unexpected exception occurred. Use VESSL_LOG=DEBUG to view stack trace. "
    "(CLI version: %s)\n"
    "(`pip install --upgrade trumpet` might resolve this issue.)" % __VERSION__
)

class TrumpetException(Exception):
    def __init__(self, message=DEFAULT_ERROR_MESSAGE, exit_code=1):
        self.message = message
        self.exit_code = exit_code
        super().__init__(message)

class ImportPackageError(TrumpetException):
    pass

def get_module(name, required=None):
    try:
        return import_module(name)
    except ImportError:
        msg = f"Error importing optional module {name}"
        if required:
            logger.warn(msg)
            raise ImportPackageError(f"{required}")


def generate_uuid():
    generated_uuid = shortuuid.ShortUUID(
        alphabet=list("0123456789abcdefghijklmnopqrstuvwxyz")
    )
    return generated_uuid.random(8)

class Image:
    def __init__(
        self,
        data: Union[str, "Image", "PIL.Image", "numpy.ndarray"],
        caption: Optional[str] = "",
        mode: Optional[str] = None,
    ):
        self._image = None
        self._caption = None
        self._mode = None
        self._path = None

        self._init_meta(caption, mode)
        self._init_image(data)
        self._save_image()

    def _init_meta(self, caption, mode):
        self._caption = caption
        self._mode = mode

        os.makedirs(TRUMPET_MEDIA_PATH, exist_ok=True)
        self._path = os.path.join(TRUMPET_MEDIA_PATH, generate_uuid() + ".png")

    def _init_image_from_path(self, data):
        pil_image = get_module(
            "PIL.Image",
            required='Pillow package is required. Run "pip install Pillow".',
        )
        self._image = pil_image.open(data)

    def _init_image_from_data(self, data):
        pil_image = get_module(
            "PIL.Image",
            required='Pillow package is required. Run "pip install Pillow".',
        )
        if Image.get_type_name(data).startswith("torch."):
            self._image = pil_image.fromarray(
                data.mul(255)
                .clamp(0, 255)
                .byte()
                .permute(1, 2, 0)
                .squeeze()
                .cpu()
                .numpy()
            )
        elif isinstance(data, pil_image.Image):
            self._image = data
        else:
            if hasattr(data, "numpy"):
                data = data.numpy()
            if data.ndim > 2:
                data = data.squeeze()
            self._image = pil_image.fromarray(
                Image.to_uint8(data),
                mode=self._mode,
            )

    def _init_image(self, data):
        if isinstance(data, Image):
            self._image = data._image
        elif isinstance(data, six.string_types):
            self._init_image_from_path(data)
        else:
            self._init_image_from_data(data)

    def _save_image(self):
        self._image.save(self._path)

    def flush(self):
        if os.path.isfile(self._path):
            os.remove(self._path)
        else:
            logger.error(f"Error: {self._path} file not found")

    @property
    def path(self):
        return self._path

    @property
    def caption(self):
        return self._caption

    @classmethod
    def get_type_name(cls, obj):
        type_name = obj.__class__.__module__ + "." + obj.__class__.__name__
        if type_name in ["builtins.module", "__builtin__.module"]:
            return obj.__name__
        else:
            return type_name

    @classmethod
    def to_uint8(cls, data):
        np = get_module(
            "numpy",
            required='numpy package is required. Run "pip install numpy"',
        )
        dmin = np.min(data)
        if dmin < 0:
            data = (data - np.min(data)) / np.ptp(data)
        if np.max(data) <= 1.0:
            data = (data * 255).astype(np.int32)

        return data.clip(0, 255).astype(np.uint8)


class ExperimentCallback(keras.callbacks.Callback):
    def __init__(
        self,
        data_type=None,
        validation_data=None,
        num_images=None,
        labels=None,
        start_epoch=0,
        save_image=False,
    ):
        super().__init__()
        self._data_type = data_type
        self._num_images = num_images or 1
        self._labels = labels
        self._start_epoch = start_epoch
        self._save_image = save_image

        self.validation_data = None
        if validation_data is not None:
            self.validation_data = validation_data

    def _results_to_predicts(self, results):
        predicts = []
        if results[0].shape[-1] == 1:
            if len(self._labels) == 2:
                predicts = [
                    self._lables[1] if result[0] > 0.5 else self._labels[0]
                    for result in results
                ]
            else:
                if not self._labels:
                    logger.warn("Cannot find labels for prediction")
                predicts = [result[0] for result in results]
        else:
            argmax_results = np.argmax(np.stack(results), axis=1)
            if not self._labels:
                logger.warn("Cannot find labels for prediction")
                predicts = argmax_results
            else:
                for argmax_result in argmax_results:
                    try:
                        predicts.append(self._labels[argmax_result])
                    except IndexError:
                        predicts.append(argmax_result)
        return predicts

    def _inference(self):
        x_val, y_val = self.validation_data

        if self._num_images > len(x_val):
            self._num_images = len(x_val)

        random_indices = np.random.choice(len(x_val), self._num_images, replace=False)
        x_val_random = [x_val[i] for i in random_indices]
        y_val_random = [y_val[i] for i in random_indices]

        results = self.model.predict(np.stack(x_val_random), batch_size=1)
        predicts = self._results_to_predicts(results)

        captions = []
        for predict, truth in zip(predicts, y_val_random):
            captions.append(f"Pred: {predict} Truth: {truth}")

        return [Image(x, caption=caption) for x, caption in zip(x_val_random, captions)]

    def _on_epoch_end(self, epoch, logs=None):
        log(step=epoch + self._start_epoch + 1, payload=logs)

        if self._save_image and self._data_type in (
            TRUMPET_PLOTS_FILETYPE_IMAGE,
            TRUMPET_PLOTS_FILETYPE_IMAGES,
        ):
            if self.validation_data is None:
                logger.warn("Cannot find validation_data")

            log({"validation_image": self._inference()})

    def on_epoch_end(self, epoch, logs=None):
        try:
            self._on_epoch_end(epoch, logs)
        except Exception as e:
            exc_info = e if TRUMPET_LOG_LEVEL == "DEBUG" else False
            logger.exception(f"{e.__class__.__name__}: {str(e)}", exc_info=exc_info)
