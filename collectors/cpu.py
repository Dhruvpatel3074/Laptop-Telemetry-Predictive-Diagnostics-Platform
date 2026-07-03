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

    Returns:
        dict[str, Any]:
            Dictionary containing CPU metrics.
    """

    metrics: dict[str, Any] = {}

    # -----------------------------
    # Timestamp
    # -----------------------------
    metrics["timestamp"] = datetime.now(UTC).isoformat()

    # -----------------------------
    # CPU Usage
    # -----------------------------
    metrics["usage_percent"] = psutil.cpu_percent(interval=1)

    # -----------------------------
    # CPU Core Information
    # -----------------------------
    metrics["physical_cores"] = psutil.cpu_count(logical=False)
    metrics["logical_cores"] = psutil.cpu_count(logical=True)

    return metrics