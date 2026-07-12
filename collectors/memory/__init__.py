"""
Memory Collector Package

Exposes the Memory metric collection interface.
"""

from __future__ import annotations

from collectors.memory.common import collect_memory_metrics

__all__ = ["collect_memory_metrics"]
