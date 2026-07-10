"""
Verification Script for Telemetry Foundation (Phase 1)

This script registers and tests the new architecture components:
1. Platform detection functions
2. Exceptions hierarchy
3. CollectorManager registration, listing, running, and unregistering.
It integrates existing collectors to verify backwards-compatibility.
"""

from __future__ import annotations

import logging
from typing import Any

from collectors import exceptions, platform
from collectors.cpu import collect_cpu_metrics
from collectors.disk import collect_disk_metrics
from collectors.manager import CollectorManager
from collectors.memory import collect_memory_metrics

# Configure logging to stdout
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
)
logger = logging.getLogger("run_foundation")


def test_platform_detection() -> None:
    """Verify platform detection functions."""
    logger.info("=== Testing Platform Detection ===")
    logger.info("is_windows: %s", platform.is_windows())
    logger.info("is_macos: %s", platform.is_macos())
    logger.info("is_linux: %s", platform.is_linux())
    logger.info("get_platform_name: %s", platform.get_platform_name())


def test_exceptions() -> None:
    """Verify exceptions module and hierarchy."""
    logger.info("=== Testing Exceptions ===")
    try:
        raise exceptions.UnsupportedPlatformError(
            "Test platform error message"
        )
    except exceptions.TelemetryError as err:
        logger.info("Caught expected exception: %s (Type: %s)", err, type(err))


def test_collector_manager() -> None:
    """Verify CollectorManager functionality and compatibility with existing collectors."""
    logger.info("=== Testing CollectorManager ===")

    manager = CollectorManager()

    # Define a simple dummy collector
    def dummy_collector() -> dict[str, Any]:
        return {"dummy_metric": 42}

    # 1. Registration
    logger.info("Registering dummy_collector...")
    manager.register("dummy", dummy_collector)

    # Register existing collectors
    logger.info("Registering existing CPU, Memory, and Disk collectors...")
    manager.register("cpu", collect_cpu_metrics)
    manager.register("memory", collect_memory_metrics)
    manager.register("disk", collect_disk_metrics)

    # 2. Listing
    collectors_list = manager.list_collectors()
    logger.info("Registered collectors: %s", collectors_list)
    assert len(collectors_list) == 4

    # 3. Running a single collector
    logger.info("Running single collector (dummy)...")
    dummy_result = manager.run_collector("dummy")
    logger.info("Dummy Result: %s", dummy_result)
    assert dummy_result == {"dummy_metric": 42}

    # Running CPU collector to ensure compatibility
    logger.info("Running CPU collector via manager...")
    cpu_result = manager.run_collector("cpu")
    logger.info("CPU usage percent: %s%%", cpu_result.get("usage_percent"))
    assert "usage_percent" in cpu_result

    # 4. Running all collectors
    logger.info("Running all registered collectors...")
    all_results = manager.run_all()
    logger.info(
        "Successfully ran all collectors. Keys collected: %s",
        list(all_results.keys()),
    )
    assert "cpu" in all_results
    assert "memory" in all_results
    assert "disk" in all_results
    assert "dummy" in all_results

    # 5. Unregistration
    logger.info("Unregistering dummy_collector...")
    manager.unregister("dummy")
    logger.info("Collectors after unregistration: %s", manager.list_collectors())
    assert "dummy" not in manager.list_collectors()

    logger.info("✅ All CollectorManager tests passed successfully!")


if __name__ == "__main__":
    logger.info("Starting Telemetry Platform foundation tests...")
    test_platform_detection()
    test_exceptions()
    test_collector_manager()
    logger.info("🎉 Foundation verification completed successfully!")
