"""FLEXT Tap Oracle Constants - Oracle tap extraction constants.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from typing import ClassVar, Final

from flext_core import FlextConstants


class FlextTapOracleConstants(FlextConstants):
    """Oracle tap extraction-specific constants following FLEXT unified pattern.

    Inherits from FlextConstants for universal constants, defines only
    Oracle tap-specific constants using nested namespace classes.
    """

    # Project metadata (Final attributes inherited from FlextConstants)
    # CONSTANTS_VERSION, PROJECT_PREFIX, PROJECT_NAME inherited from FlextConstants

    class Oracle:
        """Oracle database connection constants."""

        # Use FlextConstants for common database defaults where available
        DEFAULT_PORT: Final[int] = 1521  # Oracle-specific port
        DEFAULT_TIMEOUT: Final[int] = FlextConstants.Network.DEFAULT_TIMEOUT

        # Oracle-specific fetch configuration
        DEFAULT_FETCH_SIZE: Final[int] = FlextConstants.Performance.DEFAULT_BATCH_SIZE

    class Singer:
        """Singer tap configuration constants."""

        # Use FlextConstants for performance settings
        DEFAULT_BATCH_SIZE: Final[int] = FlextConstants.Performance.DEFAULT_BATCH_SIZE
        MAX_BATCH_SIZE: Final[int] = FlextConstants.Performance.MAX_BATCH_ITEMS

    class Replication:
        """Oracle replication method constants."""

        REPLICATION_METHODS: ClassVar[Final[list[str]]] = [
            "FULL_TABLE",
            "INCREMENTAL",
            "LOG_BASED",
        ]

        DEFAULT_METHOD: Final[str] = "INCREMENTAL"

    class Validation:
        """Oracle tap validation constants."""

        # Use FlextConstants for validation limits
        MIN_BATCH_SIZE: Final[int] = FlextConstants.Performance.MIN_TAKE
        MAX_TIMEOUT: Final[int] = FlextConstants.Performance.MAX_TIMEOUT_SECONDS


__all__ = ["FlextTapOracleConstants"]
