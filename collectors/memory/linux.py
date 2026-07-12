"""
Linux Memory Telemetry Collector

Collects Linux-specific memory metrics.
"""

from __future__ import annotations

from typing import Any

import psutil

from collectors.memory.shared import default_compressed_memory


def collect_memory_platform_metrics(
    virtual_memory: psutil.svmem, swap_memory: psutil.sswap
) -> dict[str, Any]:
    """
    Collect Linux-specific memory metrics.

    Args:
        virtual_memory: The active psutil.virtual_memory() object.
        swap_memory: The active psutil.swap_memory() object.

    Returns:
        dict[str, Any]: Linux-specific virtual and swap memory metrics.
    """
    # Linux supports cached, buffers, shared, active, and inactive memory.
    # Swap sin/sout are supported depending on kernel config (available via psutil).
    # TODO: In Version 2, parse /proc/meminfo directly to query more granular
    # metrics (e.g. Slab, Dirty, Writeback) and compression metrics (Zswap/Zram).

    return {
        "virtual_memory": {
            "cached_bytes": getattr(virtual_memory, "cached", None),
            "buffers_bytes": getattr(virtual_memory, "buffers", None),
            "shared_bytes": getattr(virtual_memory, "shared", None),
            "active_bytes": getattr(virtual_memory, "active", None),
            "inactive_bytes": getattr(virtual_memory, "inactive", None),
        },
        "swap_memory": {
            "swap_in_bytes": getattr(swap_memory, "sin", None),
            "swap_out_bytes": getattr(swap_memory, "sout", None),
        },
        "compressed": default_compressed_memory(),
    }
