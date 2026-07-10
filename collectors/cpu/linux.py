"""
Linux CPU Telemetry Collector

Collects Linux-specific CPU metrics (temperature, load average, etc.).
"""

from __future__ import annotations

from typing import Any

import psutil

from collectors.cpu.shared import (
    get_default_load_average,
    get_default_temperature,
)


def collect_cpu_platform_metrics() -> dict[str, Any]:
    """
    Collect Linux-specific CPU metrics.

    Returns:
        dict[str, Any]: Linux-specific CPU metrics.
    """
    metrics: dict[str, Any] = {}

    # Load Average (supported on Linux)
    metrics["load_average"] = get_default_load_average()
    if hasattr(psutil, "getloadavg"):
        try:
            load_1, load_5, load_15 = psutil.getloadavg()
            metrics["load_average"] = {
                "available": True,
                "1_minute": load_1,
                "5_minutes": load_5,
                "15_minutes": load_15,
            }
        except Exception:
            pass

    # Temperature (supported on Linux)
    metrics["temperature"] = get_default_temperature()
    if hasattr(psutil, "sensors_temperatures"):
        try:
            temperatures = psutil.sensors_temperatures()
            if temperatures:
                sensor_name = next(iter(temperatures))
                sensor = temperatures[sensor_name][0]
                metrics["temperature"] = {
                    "available": True,
                    "current_celsius": sensor.current,
                    "high_celsius": sensor.high,
                    "critical_celsius": sensor.critical,
                }
        except Exception:
            pass

    return metrics
