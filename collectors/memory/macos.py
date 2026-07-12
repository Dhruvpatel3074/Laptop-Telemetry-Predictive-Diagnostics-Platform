"""
macOS Memory Telemetry Collector

Collects macOS-specific memory metrics.
"""

from __future__ import annotations

from typing import Any

import psutil

from collectors.memory.shared import (
    default_compressed_memory,
    default_memory_pressure,
)


def collect_memory_platform_metrics(
    virtual_memory: psutil.svmem, swap_memory: psutil.sswap
) -> dict[str, Any]:
    """
    Collect macOS-specific memory metrics.

    Args:
        virtual_memory: The active psutil.virtual_memory() object.
        swap_memory: The active psutil.swap_memory() object.

    Returns:
        dict[str, Any]: macOS-specific virtual and swap memory metrics.
    """
    # macOS active/inactive are supported by psutil.
    # Wired memory is also supported on macOS (returned under virtual_memory).
    # TODO: Implement native Mach APIs (vm_stat, host_statistics) or PyObjC
    # in Version 2 to fetch actual memory pressure and compressed memory values.

    return {
        "virtual_memory": {
            "cached_bytes": getattr(virtual_memory, "cached", None),
            "buffers_bytes": getattr(virtual_memory, "buffers", None),
            "shared_bytes": getattr(virtual_memory, "shared", None),
            "active_bytes": getattr(virtual_memory, "active", None),
            "inactive_bytes": getattr(virtual_memory, "inactive", None),
            "wired_bytes": getattr(virtual_memory, "wired", None),
        },
        "swap_memory": {
            "swap_in_bytes": getattr(swap_memory, "sin", None),
            "swap_out_bytes": getattr(swap_memory, "sout", None),
        },
        "memory_pressure": default_memory_pressure(),
        "compressed": default_compressed_memory(),
    }
