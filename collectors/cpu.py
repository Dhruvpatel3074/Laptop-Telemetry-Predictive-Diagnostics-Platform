"""
CPU Telemetry Collector

Collects CPU-related metrics from the host machine using psutil.
This module is designed to be reused by the Telemetry Engine,
Analytics Layer, and API Backend.
"""

from __future__ import annotations

from typing import Any

import psutil


def collect_cpu_metrics() -> dict[str, Any]:
    """
    Collect CPU telemetry from the host machine.

    Returns:
        dict[str, Any]:
            Dictionary containing CPU telemetry metrics.
    """

    cpu_metrics: dict[str, Any] = {}

    # ==========================================================
    # CPU Usage
    # ==========================================================

    cpu_metrics["usage_percent"] = psutil.cpu_percent(interval=1)

    cpu_metrics["per_core_usage"] = psutil.cpu_percent(
        interval=1,
        percpu=True,
    )

    # ==========================================================
    # CPU Core Information
    # ==========================================================

    cpu_metrics["physical_cores"] = psutil.cpu_count(logical=False)
    cpu_metrics["logical_cores"] = psutil.cpu_count(logical=True)

    # ==========================================================
    # CPU Frequency
    # ==========================================================

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

    # ==========================================================
    # CPU Times
    # ==========================================================

    cpu_times = psutil.cpu_times()

    cpu_metrics["times"] = {
        "user_seconds": cpu_times.user,
        "system_seconds": cpu_times.system,
        "idle_seconds": cpu_times.idle,
    }

    # ==========================================================
    # CPU Statistics
    # ==========================================================

    cpu_stats = psutil.cpu_stats()

    cpu_metrics["stats"] = {
        "context_switches": getattr(cpu_stats, "ctx_switches", None),
        "interrupts": getattr(cpu_stats, "interrupts", None),
        "soft_interrupts": getattr(cpu_stats, "soft_interrupts", None),
        "syscalls": getattr(cpu_stats, "syscalls", None),
        "dpc": getattr(cpu_stats, "dpc", None),
    }

    # ==========================================================
    # CPU Temperature
    # ==========================================================

    cpu_metrics["temperature"] = {
        "available": False,
        "current_celsius": None,
        "high_celsius": None,
        "critical_celsius": None,
    }

    if hasattr(psutil, "sensors_temperatures"):

        temperatures = psutil.sensors_temperatures()

        if temperatures:

            sensor_name = next(iter(temperatures))
            sensor = temperatures[sensor_name][0]

            cpu_metrics["temperature"] = {
                "available": True,
                "current_celsius": sensor.current,
                "high_celsius": sensor.high,
                "critical_celsius": sensor.critical,
            }

    # ==========================================================
    # Process Information
    # ==========================================================

    processes = list(psutil.process_iter(["status"]))

    cpu_metrics["process_count"] = len(processes)

    cpu_metrics["running_process_count"] = sum(
        1
        for process in processes
        if process.info["status"] == psutil.STATUS_RUNNING
    )

    # ==========================================================
    # Load Average
    # ==========================================================

    cpu_metrics["load_average"] = {
        "available": False,
        "1_minute": None,
        "5_minutes": None,
        "15_minutes": None,
    }

    if hasattr(psutil, "getloadavg"):

        load_1, load_5, load_15 = psutil.getloadavg()

        cpu_metrics["load_average"] = {
            "available": True,
            "1_minute": load_1,
            "5_minutes": load_5,
            "15_minutes": load_15,
        }

    return cpu_metrics