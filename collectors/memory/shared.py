"""
Shared Memory Collector Utilities

Provides shared data structures and default dictionaries for memory telemetry.
"""

from __future__ import annotations

from typing import Any


def default_pagefile() -> dict[str, Any]:
    """
    Get the default page file metrics dictionary (Windows specific).

    Returns:
        dict[str, Any]: Default page file metrics structure.
    """
    return {
        "available": False,
        "total_bytes": None,
        "used_bytes": None,
        "free_bytes": None,
    }


def default_memory_pressure() -> dict[str, Any]:
    """
    Get the default memory pressure metrics dictionary (macOS specific).

    Returns:
        dict[str, Any]: Default memory pressure metrics structure.
    """
    return {
        "available": False,
        "pressure_percent": None,
        "status": None,
    }


def default_compressed_memory() -> dict[str, Any]:
    """
    Get the default compressed memory metrics dictionary.

    Returns:
        dict[str, Any]: Default compressed memory metrics structure.
    """
    return {
        "available": False,
        "compressed_bytes": None,
    }


def get_default_platform_virtual_memory() -> dict[str, Any]:
    """
    Get default values for platform-dependent virtual memory metrics.

    Returns:
        dict[str, Any]: Dictionary with None/default values.
    """
    return {
        "cached_bytes": None,
        "buffers_bytes": None,
        "shared_bytes": None,
        "active_bytes": None,
        "inactive_bytes": None,
    }


def get_default_platform_swap_memory() -> dict[str, Any]:
    """
    Get default values for platform-dependent swap memory metrics.

    Returns:
        dict[str, Any]: Dictionary with None/default values.
    """
    return {
        "swap_in_bytes": None,
        "swap_out_bytes": None,
    }
