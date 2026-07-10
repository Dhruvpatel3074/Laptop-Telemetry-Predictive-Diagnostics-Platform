"""
Memory Collector Package

Dynamically proxies to the existing collectors/memory.py file at the parent level
to resolve module shadowing and maintain backwards-compatibility.
"""

from __future__ import annotations

import importlib.util
import os
import sys

# Resolve the path to the parent memory.py file
_parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
_memory_py_path = os.path.join(_parent_dir, "memory.py")

if os.path.exists(_memory_py_path):
    _spec = importlib.util.spec_from_file_location(
        "collectors.memory_file", _memory_py_path
    )
    if _spec and _spec.loader:
        _module = importlib.util.module_from_spec(_spec)
        # Add to sys.modules under a temp name to allow relative imports inside it if any
        sys.modules["collectors.memory_file"] = _module
        _spec.loader.exec_module(_module)
        # Expose all public attributes of the module to this package
        globals().update(
            {k: v for k, v in _module.__dict__.items() if not k.startswith("__")}
        )
