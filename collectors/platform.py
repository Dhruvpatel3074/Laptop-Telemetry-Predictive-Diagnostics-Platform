"""
Platform Detection Utility

Provides helper functions for identifying the host operating system.
This module is used by collectors to execute platform-specific code.
"""

from __future__ import annotations

import sys


def is_windows() -> bool:
    """
    Check if the host platform is Windows.

    Returns:
        bool: True if the platform is Windows, False otherwise.
    """
    return sys.platform.startswith("win32")


def is_macos() -> bool:
    """
    Check if the host platform is macOS.

    Returns:
        bool: True if the platform is macOS, False otherwise.
    """
    return sys.platform.startswith("darwin")


def is_linux() -> bool:
    """
    Check if the host platform is Linux.

    Returns:
        bool: True if the platform is Linux, False otherwise.
    """
    return sys.platform.startswith("linux")


def get_platform_name() -> str:
    """
    Get the name of the host platform.

    Returns:
        str: 'windows', 'macos', 'linux', or 'unknown'.
    """
    if is_windows():
        return "windows"
    if is_macos():
        return "macos"
    if is_linux():
        return "linux"
    return "unknown"
