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

    cpu_metrics: dict[str, Any] = {}

    # -----------------------------
    # Timestamp
    # -----------------------------
    cpu_metrics["timestamp"] = datetime.now(UTC).isoformat()

    # -----------------------------
    # CPU Usage
    # -----------------------------
    cpu_metrics["usage_percent"] = psutil.cpu_percent(interval=1)

    # -----------------------------
    # CPU Core Information
    # -----------------------------
    cpu_metrics["physical_cores"] = psutil.cpu_count(logical=False)
    cpu_metrics["logical_cores"] = psutil.cpu_count(logical=True)
    
    cpu_metrics={
        usage_percent :
        physical_cores:
        logical_cores:
    }
    
    frequency=psutil.cpu_freq()
    
    

    return metrics