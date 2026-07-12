"""
Windows Memory Telemetry Collector

Collects Windows-specific memory metrics.
"""

from __future__ import annotations

from typing import Any

import psutil

from collectors.memory.shared import (
    default_compressed_memory,
    default_pagefile,
    get_default_platform_swap_memory,
    get_default_platform_virtual_memory,
)


def collect_memory_platform_metrics(
    virtual_memory: psutil.svmem, swap_memory: psutil.sswap
) -> dict[str, Any]:
    """
    Collect Windows-specific memory metrics.

    Args:
        virtual_memory: The active psutil.virtual_memory() object.
        swap_memory: The active psutil.swap_memory() object.

    Returns:
        dict[str, Any]: Windows-specific virtual and swap memory metrics.
    """
    # Windows-specific placeholders for commit info, page file, and compressed memory.
    # TODO: Implement native Win32 Memory APIs (e.g. GlobalMemoryStatusEx)
    # in Version 2 to retrieve actual pagefile usage, commit limits, and compression stats.

    # Windows doesn't support cached/buffers/shared/active/inactive or swap in/out via psutil.
    return {
        "virtual_memory": get_default_platform_virtual_memory(),
        "swap_memory": get_default_platform_swap_memory(),
        "pagefile": default_pagefile(),
        "commit": {
            "available": False,
            "total_bytes": None,
            "used_bytes": None,
        },
        "compressed": default_compressed_memory(),
    }
