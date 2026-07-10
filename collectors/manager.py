"""
Collector Manager

Provides simple infrastructure for registering, unregistering, and executing
telemetry collectors.
"""

from __future__ import annotations

import logging
from typing import Any, Callable

# Configure logger
logger = logging.getLogger(__name__)


class CollectorManager:
    """Manages the lifecycle, registration, and execution of telemetry collectors."""

    def __init__(self) -> None:
        """Initialize the CollectorManager with an empty registry."""
        self._collectors: dict[str, Callable[[], dict[str, Any]]] = {}

    def register(
        self, name: str, collector_callable: Callable[[], dict[str, Any]]
    ) -> None:
        """
        Register a telemetry collector callable.

        Args:
            name: The unique name of the collector (e.g., 'cpu').
            collector_callable: A callable function that collects metrics and returns a dict.

        Raises:
            TypeError: If the collector_callable is not callable.
            ValueError: If a collector with the same name is already registered.
        """
        if not callable(collector_callable):
            raise TypeError("Collector must be a callable.")

        if name in self._collectors:
            raise ValueError(f"Collector '{name}' is already registered.")

        self._collectors[name] = collector_callable
        logger.info("Registered collector: %s", name)

    def unregister(self, name: str) -> None:
        """
        Unregister a telemetry collector.

        Args:
            name: The name of the collector to remove.

        Raises:
            KeyError: If the collector is not registered.
        """
        if name not in self._collectors:
            raise KeyError(f"Collector '{name}' is not registered.")

        del self._collectors[name]
        logger.info("Unregistered collector: %s", name)

    def run_collector(self, name: str) -> dict[str, Any]:
        """
        Run a single registered collector by name.

        Handles exceptions gracefully to prevent application crashes.

        Args:
            name: Name of the collector.

        Returns:
            dict[str, Any]: The collected metrics, or an error status dictionary.
        """
        if name not in self._collectors:
            logger.error(
                "Execution failed: Collector '%s' is not registered.", name
            )
            return {
                "available": False,
                "error": f"Collector '{name}' not registered",
            }

        collector_callable = self._collectors[name]
        try:
            return collector_callable()
        except Exception as err:
            logger.exception(
                "Unexpected error executing collector '%s': %s", name, err
            )
            return {"available": False, "error": f"Unexpected error: {str(err)}"}

    def run_all(self) -> dict[str, dict[str, Any]]:
        """
        Run all registered collectors.

        Returns:
            dict[str, dict[str, Any]]: Dictionary mapping collector name to metrics.
        """
        results: dict[str, dict[str, Any]] = {}
        for name in self._collectors:
            results[name] = self.run_collector(name)
        return results

    def list_collectors(self) -> list[str]:
        """
        List all registered collector names.

        Returns:
            list[str]: List of registered collector names.
        """
        return list(self._collectors.keys())
