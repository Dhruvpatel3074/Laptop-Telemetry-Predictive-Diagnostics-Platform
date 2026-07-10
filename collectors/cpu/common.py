"""
CPU Telemetry Collector

Orchestrates cross-platform and platform-specific CPU metric collection.
"""

from __future__ import annotations

from typing import Any

import psutil

from collectors import platform
from collectors.cpu.shared import (
    get_default_load_average,
    get_default_temperature,
)


def collect_cpu_metrics() -> dict[str, Any]:
    """
    Collect CPU telemetry from the host machine.

    Returns:
        dict[str, Any]: Dictionary containing CPU telemetry metrics.
    """
    cpu_metrics: dict[str, Any] = {}

    # ==========================================================
    # Cross-Platform CPU Usage & Info
    # ==========================================================
    # TODO: This will later be replaced by a non-blocking stateful sampler
    # once the Telemetry Scheduler is implemented.
    cpu_metrics["usage_percent"] = psutil.cpu_percent(interval=1)

    # TODO: This will later be replaced by a non-blocking stateful sampler
    # once the Telemetry Scheduler is implemented.
    cpu_metrics["per_core_usage"] = psutil.cpu_percent(interval=1, percpu=True)

    cpu_metrics["physical_cores"] = psutil.cpu_count(logical=False)
    cpu_metrics["logical_cores"] = psutil.cpu_count(logical=True)

    # Frequency
    frequency = psutil.cpu_freq()
    if frequency is not None:
        cpu_metrics["frequency"] = {
            "current_mhz": frequency.current,
            "minimum_mhz": frequency.min,
            "maximum_mhz": frequency.max,
        }
    else:
        cpu_metrics["frequency"] = {
            "current_mhz": None,
            "minimum_mhz": None,
            "maximum_mhz": None,
        }

    # Times
    cpu_times = psutil.cpu_times()
    cpu_metrics["times"] = {
        "user_seconds": cpu_times.user,
        "system_seconds": cpu_times.system,
        "idle_seconds": cpu_times.idle,
    }

    # Stats
    cpu_stats = psutil.cpu_stats()
    cpu_metrics["stats"] = {
        "context_switches": getattr(cpu_stats, "ctx_switches", None),
        "interrupts": getattr(cpu_stats, "interrupts", None),
        "soft_interrupts": getattr(cpu_stats, "soft_interrupts", None),
        "syscalls": getattr(cpu_stats, "syscalls", None),
        "dpc": getattr(cpu_stats, "dpc", None),
    }

    # Process Info
    # Optimization: Use len(psutil.pids()) instead of listing psutil process objects.
    cpu_metrics["process_count"] = len(psutil.pids())

    # TODO: running_process_count should later be collected using the
    # scheduler at a lower frequency.
    processes = list(psutil.process_iter(["status"]))
    cpu_metrics["running_process_count"] = sum(
        1
        for process in processes
        if process.info["status"] == psutil.STATUS_RUNNING
    )

    # ==========================================================
    # Platform-Specific CPU Metrics
    # ==========================================================
    platform_name = platform.get_platform_name()
    platform_metrics: dict[str, Any] = {}

    if platform_name == "windows":
        from collectors.cpu.windows import collect_cpu_platform_metrics
        platform_metrics = collect_cpu_platform_metrics()
    elif platform_name == "macos":
        from collectors.cpu.macos import collect_cpu_platform_metrics
        platform_metrics = collect_cpu_platform_metrics()
    elif platform_name == "linux":
        from collectors.cpu.linux import collect_cpu_platform_metrics
        platform_metrics = collect_cpu_platform_metrics()
    else:
        # Fallback default values
        platform_metrics = {
            "temperature": get_default_temperature(),
            "load_average": get_default_load_average(),
        }

    cpu_metrics.update(platform_metrics)

    return cpu_metrics
