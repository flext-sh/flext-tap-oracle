"""FLEXT Tap Oracle Constants - Oracle tap extraction constants.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from typing import ClassVar

from flext_core import FlextConstants


class FlextTapOracleConstants(FlextConstants):
    """Oracle tap extraction-specific constants following flext-core patterns."""

    # Oracle Connection Configuration
    DEFAULT_ORACLE_PORT = 1521
    DEFAULT_ORACLE_TIMEOUT = 30
    DEFAULT_FETCH_SIZE = 1000

    # Singer Tap Configuration
    DEFAULT_BATCH_SIZE = 1000
    MAX_BATCH_SIZE = 10000

    # Oracle Replication Methods
    REPLICATION_METHODS: ClassVar[list[str]] = [
        "FULL_TABLE",
        "INCREMENTAL",
        "LOG_BASED",
    ]


__all__ = ["FlextTapOracleConstants"]
