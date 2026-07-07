"""
CPU Telemetry Collector

Collects CPU-related metrics from the host machine using psutil.
This module is designed to be reused by the Telemetry Engine,
analytics layer, and API backend.
"""

from __future__ import annotations

from datetime import datetime, UTC
from typing import Any

import psutil


def collect_cpu_metrics() -> dict[str, Any]:
    """
    Collect CPU telemetry from the host machine.

    Return
        dict[str, Any]:
            Dictionary containing CPU metrics.
    """
    metrics: dict[str, Any]={}
    cpu_metrics: dict[str, Any] = {}

    # -----------------------------
    # Timestamp
    # -----------------------------
    timestamp = datetime.now(UTC).isoformat()
    
    metrics["timestamp"] =  timestamp

    # -----------------------------
    # CPU Usage
    # -----------------------------
    cpu_metrics["usage_percent"] = psutil.cpu_percent(interval=1)

    # -----------------------------
    # CPU Core Information
    # -----------------------------
    cpu_metrics["physical_cores"] = psutil.cpu_count(logical=False)
    cpu_metrics["logical_cores"] = psutil.cpu_count(logical=True)
    
    
    frequency = psutil.cpu_freq()
    
    if frequency is not None:
        cpu_metrics["frequency"] = {
            "current_mhz": frequency.current,
            "minimum_mhz": frequency.min,
            "maximum_mhz": frequency.max
        }
    else:
        cpu_metrics["frequency"] = {
            "current_mhz": None,
            "minimum_mhz": None,
            "maximum_mhz": None
        }
    
    metrics["cpu"] = cpu_metrics
    
    

    return metrics