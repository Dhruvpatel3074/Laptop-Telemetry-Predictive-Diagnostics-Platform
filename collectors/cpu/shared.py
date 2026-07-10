"""
Shared CPU Collector Utilities

Provides shared data structures and default dictionaries for CPU telemetry.
"""

from __future__ import annotations

from typing import Any


def get_default_temperature() -> dict[str, Any]:
    """
    Get the default CPU temperature metrics dictionary when unavailable.

    Returns:
        dict[str, Any]: Default temperature metrics structure.
    """
    return {
        "available": False,
        "current_celsius": None,
        "high_celsius": None,
        "critical_celsius": None,
    }


def get_default_load_average() -> dict[str, Any]:
    """
    Get the default CPU load average metrics dictionary when unavailable.

    Returns:
        dict[str, Any]: Default load average metrics structure.
    """
    return {
        "available": False,
        "1_minute": None,
        "5_minutes": None,
        "15_minutes": None,
    }
