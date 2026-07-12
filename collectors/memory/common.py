"""
Memory Telemetry Collector

Orchestrates cross-platform and platform-specific memory metric collection.
"""

from __future__ import annotations

from typing import Any

import psutil

from collectors import platform
from collectors.memory.shared import (
    get_default_platform_swap_memory,
    get_default_platform_virtual_memory,
)


def collect_memory_metrics() -> dict[str, Any]:
    """
    Collect memory telemetry from the host machine.

    Returns:
        dict[str, Any]: Dictionary containing memory telemetry metrics.
    """
    # Genuinely shared cross-platform base collections
    virtual_memory = psutil.virtual_memory()
    swap_memory = psutil.swap_memory()

    # Base virtual memory data structure
    virtual_memory_data: dict[str, Any] = {
        "total_bytes": virtual_memory.total,
        "available_bytes": virtual_memory.available,
        "used_bytes": virtual_memory.used,
        "free_bytes": virtual_memory.free,
        "usage_percent": virtual_memory.percent,
    }

    # Base swap memory data structure
    swap_memory_data: dict[str, Any] = {
        "total_bytes": swap_memory.total,
        "used_bytes": swap_memory.used,
        "free_bytes": swap_memory.free,
        "usage_percent": swap_memory.percent,
    }

    # Delegate platform-specific virtual/swap metrics
    platform_name = platform.get_platform_name()
    platform_metrics: dict[str, Any] = {}

    if platform_name == "windows":
        from collectors.memory.windows import collect_memory_platform_metrics
        platform_metrics = collect_memory_platform_metrics(
            virtual_memory, swap_memory
        )
    elif platform_name == "macos":
        from collectors.memory.macos import collect_memory_platform_metrics
        platform_metrics = collect_memory_platform_metrics(
            virtual_memory, swap_memory
        )
    elif platform_name == "linux":
        from collectors.memory.linux import collect_memory_platform_metrics
        platform_metrics = collect_memory_platform_metrics(
            virtual_memory, swap_memory
        )
    else:
        platform_metrics = {
            "virtual_memory": get_default_platform_virtual_memory(),
            "swap_memory": get_default_platform_swap_memory(),
        }

    # Update common structures with platform-specific fields
    virtual_memory_data.update(platform_metrics.get("virtual_memory", {}))
    swap_memory_data.update(platform_metrics.get("swap_memory", {}))

    # Return final consolidated result
    result = {
        "virtual_memory": virtual_memory_data,
        "swap_memory": swap_memory_data,
    }

    # Merge additional platform-specific top-level placeholders (e.g. pagefile, commit, memory_pressure, compressed)
    # only if they exist in platform_metrics to keep common.py clean and compliant.
    for key, value in platform_metrics.items():
        if key not in ("virtual_memory", "swap_memory"):
            result[key] = value

    return result
