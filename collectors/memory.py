"""
Memory Telemetry Collector

Collects memory-related metrics from the host machine using psutil.
This module is designed to be reused by the Telemetry Engine,
Analytics Layer, and API Backend.
"""

from __future__ import annotations

from typing import Any

import psutil


def collect_memory_metrics() -> dict[str, Any]:
    """
    Collect memory telemetry from the host machine.

    Returns:
        dict[str, Any]:
            Dictionary containing memory telemetry metrics.
    """

    memory_metrics: dict[str, Any] = {}

    # ==========================================================
    # Virtual Memory
    # ==========================================================

    virtual_memory = psutil.virtual_memory()

    memory_metrics["virtual_memory"] = {
        "total_bytes": virtual_memory.total,
        "available_bytes": virtual_memory.available,
        "used_bytes": virtual_memory.used,
        "free_bytes": virtual_memory.free,
        "usage_percent": virtual_memory.percent,
        "cached_bytes": getattr(virtual_memory, "cached", None),
        "buffers_bytes": getattr(virtual_memory, "buffers", None),
        "shared_bytes": getattr(virtual_memory, "shared", None),
        "active_bytes": getattr(virtual_memory, "active", None),
        "inactive_bytes": getattr(virtual_memory, "inactive", None),
    }

    # ==========================================================
    # Swap Memory
    # ==========================================================

    swap_memory = psutil.swap_memory()

    memory_metrics["swap_memory"] = {
        "total_bytes": swap_memory.total,
        "used_bytes": swap_memory.used,
        "free_bytes": swap_memory.free,
        "usage_percent": swap_memory.percent,
        "swap_in_bytes": getattr(swap_memory, "sin", None),
        "swap_out_bytes": getattr(swap_memory, "sout", None),
    }

    return memory_metrics