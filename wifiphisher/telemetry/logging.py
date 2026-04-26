"""Structured logging helpers."""

import copy
import json
import logging

import wifiphisher.common.constants as constants

LOGGER_NAME_WIDTH = 32


class SessionContextFilter(logging.Filter):
    """Inject runtime session ID into every log record."""

    def __init__(self, session_id):
        super(SessionContextFilter, self).__init__()
        self._session_id = session_id

    def filter(self, record):
        record.session_id = self._session_id
        return True


class JsonFormatter(logging.Formatter):
    """Serialize log records as JSON objects."""

    def format(self, record):
        payload = {
            "timestamp": self.formatTime(record, self.datefmt),
            "level": record.levelname,
            "logger": record.name,
            "session_id": getattr(record, "session_id", ""),
            "message": record.getMessage(),
        }
        return json.dumps(payload, sort_keys=True)


def build_logging_config(file_path=None, level=None, json_format=False):
    """Build logging configuration using existing defaults as baseline."""
    logging_config = copy.deepcopy(constants.LOGGING_CONFIG)
    if file_path:
        logging_config["handlers"]["file"]["filename"] = file_path
    if level:
        logging_config["handlers"]["file"]["level"] = level
    if json_format:
        logging_config["formatters"]["json"] = {
            "()": "wifiphisher.telemetry.logging.JsonFormatter"
        }
        logging_config["handlers"]["file"]["formatter"] = "json"
    else:
        logging_config["formatters"]["detailed"]["format"] = (
            "%(asctime)s - %(name)" + str(LOGGER_NAME_WIDTH) +
            "s - %(levelname)s - [session_id=%(session_id)s] %(message)s")
    return logging_config
