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
from importlib import import_module
from trumpet_client.exceptions import TrumpetException
from trumpet_client.loggers.logger import logger
from trumpet_client.loggers.logger import TRUMPET_LOG_LEVEL
from trumpet_client.loggers.logger import TRUMPET_PLOTS_FILETYPE_IMAGE
from trumpet_client.loggers.logger import TRUMPET_PLOTS_FILETYPE_IMAGES
from trumpet_client.loggers.logger import TRUMPET_MEDIA_PATH

class ImportPackageError(TrumpetException):
    pass

def generate_uuid():
    generated_uuid = shortuuid.ShortUUID(
        alphabet=list("0123456789abcdefghijklmnopqrstuvwxyz")
    )
    return generated_uuid.random(8)

def get_module(name, required=None):
    try:
        return import_module(name)
    except ImportError:
        msg = f"Error importing optional module {name}"
        if required:
            logger.warn(msg)
            raise ImportPackageError(f"{required}")

# TODO TEMP
def log(*args, **kwargs):
    print("log start")
    print(kwargs)
    print("log end")
    return kwargs

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
            num=1,
            labels=None,
            start_epoch=0,
            save=False,
    ):
        super().__init__()
        self._data_type = data_type
        self._num = num
        self._labels = labels
        self._start_epoch = start_epoch
        self._save = save
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

        if self._num > len(x_val):
            self._num = len(x_val)

        random_indices = np.random.choice(len(x_val), self._num, replace=False)
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

        # if self._save and self._data_type in (
        #         TRUMPET_PLOTS_FILETYPE_IMAGE,
        #         TRUMPET_PLOTS_FILETYPE_IMAGES,
        # ):
        #     if self.validation_data is None:
        #         logger.warn("Cannot find validation_data")
        #
        #     log({"validation_image": self._inference()})

    def on_epoch_end(self, epoch, logs=None):
        try:
            self._on_epoch_end(epoch, logs)
        except Exception as e:
            exc_info = e if TRUMPET_LOG_LEVEL == "DEBUG" else False
            logger.exception(f"{e.__class__.__name__}: {str(e)}", exc_info=exc_info)

if __name__ == "__main__":
    # TensorFlow and tf.keras
    import tensorflow as tf

    # Helper libraries
    import numpy as np
    import matplotlib.pyplot as plt

    print(tf.__version__)

    fashion_mnist = tf.keras.datasets.fashion_mnist

    (train_images, train_labels), (test_images, test_labels) = fashion_mnist.load_data()

    class_names = ['T-shirt/top', 'Trouser', 'Pullover', 'Dress', 'Coat',
                   'Sandal', 'Shirt', 'Sneaker', 'Bag', 'Ankle boot']

    train_images = train_images / 255.0

    test_images = test_images / 255.0

    model = tf.keras.Sequential([
        tf.keras.layers.Flatten(input_shape=(28, 28)),
        tf.keras.layers.Dense(128, activation='relu'),
        tf.keras.layers.Dense(10)
    ])

    model.compile(optimizer='adam',
                  loss=tf.keras.losses.SparseCategoricalCrossentropy(from_logits=True),
                  metrics=['accuracy'])

    model.fit(train_images, train_labels, epochs=10, callbacks=[ExperimentCallback(data_type="image",save=True,validation_data=(test_images,test_labels), labels=class_names)])
