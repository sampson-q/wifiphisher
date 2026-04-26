"""Unit tests for phase-1 modernization modules."""

import logging
import os
import unittest

import wifiphisher.common.constants as constants
import wifiphisher.configuration.config as config
import wifiphisher.core.exceptions as core_exceptions
import wifiphisher.core.runtime_context as runtime_context
import wifiphisher.telemetry.logging as telemetry_logging


class TestRuntimeContext(unittest.TestCase):
    """Test typed runtime context behavior."""

    def test_context_defaults_and_reset(self):
        context = runtime_context.RuntimeContext()
        self.assertTrue(context.session_id)
        self.assertEqual({}, context.discovered_aps)

        context.discovered_aps = {"ap-1": ("1", "ssid", "aa:bb:cc:dd:ee:ff")}
        context.reset_discovered_aps()
        self.assertEqual({}, context.discovered_aps)


class TestRuntimeConfig(unittest.TestCase):
    """Test layered runtime configuration behavior."""

    def test_default_logging_config(self):
        runtime_cfg = config.load_config()
        self.assertEqual(runtime_cfg.logging.file_path, constants.LOG_FILEPATH)
        self.assertEqual(runtime_cfg.logging.level, constants.LOG_LEVEL)
        self.assertFalse(runtime_cfg.logging.json)

    def test_environment_override(self):
        original_level = os.environ.get("WIFIPHISHER_LOG_LEVEL")
        original_json = os.environ.get("WIFIPHISHER_LOG_JSON")
        try:
            os.environ["WIFIPHISHER_LOG_LEVEL"] = "DEBUG"
            os.environ["WIFIPHISHER_LOG_JSON"] = "true"
            runtime_cfg = config.load_config()
            self.assertEqual(runtime_cfg.logging.level, "DEBUG")
            self.assertTrue(runtime_cfg.logging.json)
        finally:
            if original_level is None:
                os.environ.pop("WIFIPHISHER_LOG_LEVEL", None)
            else:
                os.environ["WIFIPHISHER_LOG_LEVEL"] = original_level
            if original_json is None:
                os.environ.pop("WIFIPHISHER_LOG_JSON", None)
            else:
                os.environ["WIFIPHISHER_LOG_JSON"] = original_json

    def test_invalid_level_raises(self):
        with self.assertRaises(core_exceptions.ConfigurationError):
            config.load_config(runtime_overrides={"logging_level": "INVALID"})

    def test_invalid_logging_directory_raises(self):
        with self.assertRaises(core_exceptions.ConfigurationError):
            config.load_config(
                runtime_overrides={
                    "logging_file_path": "/path/that/does/not/exist/wifiphisher.log"
                })


class TestTelemetryLogging(unittest.TestCase):
    """Test structured logging helpers."""

    def test_build_logging_config_json(self):
        logging_cfg = telemetry_logging.build_logging_config(
            file_path="/tmp/test.log",
            level="DEBUG",
            json_format=True)
        self.assertEqual(logging_cfg["handlers"]["file"]["filename"], "/tmp/test.log")
        self.assertEqual(logging_cfg["handlers"]["file"]["level"], "DEBUG")
        self.assertEqual(logging_cfg["handlers"]["file"]["formatter"], "json")

    def test_session_filter_adds_id(self):
        session_filter = telemetry_logging.SessionContextFilter("session-123")
        record = logging.LogRecord(
            name="test",
            level=logging.INFO,
            pathname=__file__,
            lineno=1,
            msg="hello",
            args=(),
            exc_info=None)
        session_filter.filter(record)
        self.assertEqual(record.session_id, "session-123")
