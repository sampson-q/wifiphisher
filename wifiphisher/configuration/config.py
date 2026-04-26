"""Typed layered configuration with defaults, env overrides and runtime overrides."""

import os
from dataclasses import dataclass

import wifiphisher.common.constants as constants
from wifiphisher.core.exceptions import ConfigurationError


@dataclass
class LoggingConfig:
    """Logging settings for a runtime session."""

    is_enabled: bool = False
    level: str = constants.LOG_LEVEL
    file_path: str = constants.LOG_FILEPATH
    json: bool = False


@dataclass
class RuntimeConfig:
    """Root runtime configuration."""

    logging: LoggingConfig


def _to_bool(value):
    if isinstance(value, bool):
        return value
    return str(value).strip().lower() in ("1", "true", "yes", "on")


def _read_environment_layer():
    return {
        "logging_level": os.getenv("WIFIPHISHER_LOG_LEVEL"),
        "logging_file_path": os.getenv("WIFIPHISHER_LOG_PATH"),
        "logging_json": os.getenv("WIFIPHISHER_LOG_JSON"),
    }


def _apply_overrides(config, env_layer, runtime_overrides):
    if env_layer.get("logging_level"):
        config.logging.level = env_layer["logging_level"]
    if env_layer.get("logging_file_path"):
        config.logging.file_path = env_layer["logging_file_path"]
    if env_layer.get("logging_json") is not None:
        config.logging.json = _to_bool(env_layer["logging_json"])

    if runtime_overrides:
        if runtime_overrides.get("logging_level"):
            config.logging.level = runtime_overrides["logging_level"]
        if runtime_overrides.get("logging_file_path"):
            config.logging.file_path = runtime_overrides["logging_file_path"]
        if runtime_overrides.get("logging_json") is not None:
            config.logging.json = _to_bool(runtime_overrides["logging_json"])
        if runtime_overrides.get("logging_enabled") is not None:
            config.logging.is_enabled = _to_bool(runtime_overrides["logging_enabled"])


def _validate(config):
    valid_levels = {"CRITICAL", "ERROR", "WARNING", "INFO", "DEBUG", "NOTSET"}
    if config.logging.level not in valid_levels:
        raise ConfigurationError(
            "Invalid logging level: {}. Expected one of {}.".format(
                config.logging.level, sorted(valid_levels)
            )
        )
    if not config.logging.file_path:
        raise ConfigurationError("Logging file path must not be empty.")
    log_dir = os.path.dirname(config.logging.file_path) or os.getcwd()
    if not os.path.isdir(log_dir):
        raise ConfigurationError(
            "Logging directory does not exist: {}".format(log_dir))


def load_config(runtime_overrides=None):
    """Load layered runtime configuration."""
    config = RuntimeConfig(logging=LoggingConfig())
    env_layer = _read_environment_layer()
    _apply_overrides(config, env_layer, runtime_overrides or {})
    _validate(config)
    return config
