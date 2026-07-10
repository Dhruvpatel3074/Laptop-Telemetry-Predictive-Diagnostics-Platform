"""
Configuration Settings

Defines global configuration constants for the telemetry platform.
"""

from __future__ import annotations

import os

# Base directory of the project
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Telemetry settings
TELEMETRY_INTERVAL_SECONDS = 5.0
DEFAULT_LOG_LEVEL = "INFO"

# Enabled collectors (future toggle support)
ENABLED_COLLECTORS = {
    "cpu": True,
    "memory": True,
    "disk": True,
    "battery": True,
    "gpu": True,
    "network": True,
    "system": True,
}
