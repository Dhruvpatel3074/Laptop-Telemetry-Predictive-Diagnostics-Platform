"""
Telemetry Exceptions

Defines custom exceptions for the telemetry collection framework.
"""

from __future__ import annotations


class TelemetryError(Exception):
    """Base exception for all telemetry-related errors."""
    pass


class CollectorError(TelemetryError):
    """Exception raised during telemetry collection execution."""
    pass


class UnsupportedPlatformError(CollectorError):
    """Exception raised when a collector is run on an unsupported platform."""
    pass


class SensorUnavailableError(CollectorError):
    """Exception raised when a hardware sensor or metric source is unavailable."""
    pass
