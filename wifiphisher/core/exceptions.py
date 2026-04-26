"""Structured exception hierarchy for modernized runtime components."""


class WifiphisherError(Exception):
    """Base class for modernized Wifiphisher runtime exceptions."""


class ConfigurationError(WifiphisherError):
    """Raised when configuration loading or validation fails."""

