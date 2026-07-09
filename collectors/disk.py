"""
Disk Telemetry Collector

Collects disk-related metrics from the host machine using psutil.
This module is designed to be reused by the Telemetry Engine,
Analytics Layer, and API Backend.
"""

from __future__ import annotations

from typing import Any

import psutil


def collect_disk_metrics() -> dict[str, Any]:
    """
    Collect disk telemetry from the host machine.

    Returns:
        dict[str, Any]:
            Dictionary containing disk telemetry metrics.
    """

    disk_metrics: dict[str, Any] = {}

    # ==========================================================
    # Disk Usage
    # ==========================================================

    disk_usage = psutil.disk_usage("/")

    disk_metrics["usage"] = {
        "total_bytes": disk_usage.total,
        "used_bytes": disk_usage.used,
        "free_bytes": disk_usage.free,
        "usage_percent": disk_usage.percent,
    }

    # ==========================================================
    # Disk I/O Counters
    # ==========================================================

    disk_io = psutil.disk_io_counters()

    if disk_io is not None:

        disk_metrics["io"] = {
            "read_count": disk_io.read_count,
            "write_count": disk_io.write_count,
            "read_bytes": disk_io.read_bytes,
            "write_bytes": disk_io.write_bytes,
            "read_time_ms": getattr(disk_io, "read_time", None),
            "write_time_ms": getattr(disk_io, "write_time", None),
            "busy_time_ms": getattr(disk_io, "busy_time", None),
        }

    else:

        disk_metrics["io"] = {
            "read_count": None,
            "write_count": None,
            "read_bytes": None,
            "write_bytes": None,
            "read_time_ms": None,
            "write_time_ms": None,
            "busy_time_ms": None,
        }

    # ==========================================================
    # Disk Partitions
    # ==========================================================

    partitions = []

    for partition in psutil.disk_partitions():

        partitions.append({
            "device": partition.device,
            "mountpoint": partition.mountpoint,
            "filesystem": partition.fstype,
            "options": partition.opts,
        })

    disk_metrics["partitions"] = partitions

    disk_metrics["partition_count"] = len(partitions)

    return disk_metrics