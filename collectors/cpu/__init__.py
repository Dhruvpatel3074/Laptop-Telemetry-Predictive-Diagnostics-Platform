"""
CPU Collector Package

Exposes the CPU metric collection interface.
"""

from __future__ import annotations

from collectors.cpu.common import collect_cpu_metrics

__all__ = ["collect_cpu_metrics"]
