import logging
import time
from typing import Optional
from typing import Union
import os
import sys
from trumpet_client.envs import *

TRUMPET_MEDIA_PATH = "trumpet-media"
TRUMPET_IMAGE_PATH = "images"
TRUMPET_AUDIO_PATH = "audio"
TRUMPET_PLOTS_FILETYPE_IMAGE = "image"
TRUMPET_PLOTS_FILETYPE_IMAGES = "images"
TRUMPET_PLOTS_FILETYPE_AUDIO = "audio"
logging.INFO
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

FORMAT_LEVEL_MAP = {
    logging.FATAL: "F",  # FATAL is alias of CRITICAL
    logging.ERROR: "E",
    logging.WARN: "W",
    logging.INFO: "I",
    logging.DEBUG: "D",
}

class Formatter(logging.Formatter):
    def format(self, record: logging.LogRecord):
        level = FORMAT_LEVEL_MAP.get(record.levelno, "?")

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
        self._logger = logging.getLogger(__name__)
        self._handler: Optional[logging.Handler] = None

        self.set_level(TRUMPET_LOG_LEVEL)
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

