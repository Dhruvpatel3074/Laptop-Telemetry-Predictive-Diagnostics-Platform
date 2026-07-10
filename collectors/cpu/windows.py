"""
Windows CPU Telemetry Collector

Collects Windows-specific CPU metrics (temperature, load average, etc.).
"""

from __future__ import annotations

from typing import Any

from collectors.cpu.shared import (
    get_default_load_average,
    get_default_temperature,
)


def collect_cpu_platform_metrics() -> dict[str, Any]:
    """
    Collect Windows-specific CPU metrics.

    Returns:
        dict[str, Any]: Windows-specific CPU metrics.
    """
    return {
        "temperature": get_default_temperature(),
        "load_average": get_default_load_average(),
    }
