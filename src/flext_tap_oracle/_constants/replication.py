"""Tap Oracle replication method constants.

Copyright (c) 2026 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from enum import StrEnum, unique


class FlextTapOracleConstantsReplication:
    """Oracle replication method constants composed into ``c.TapOracle``."""

    class Replication:
        """Oracle replication method constants."""

        @unique
        class Method(StrEnum):
            """Oracle replication methods using StrEnum for type safety.

            DRY Pattern:
                StrEnum is the single source of truth. Use Method.FULL_TABLE.value
                or Method.FULL_TABLE directly - no base strings needed.
            """

            FULL_TABLE = "FULL_TABLE"
            INCREMENTAL = "INCREMENTAL"
            LOG_BASED = "LOG_BASED"


__all__: list[str] = ["FlextTapOracleConstantsReplication"]
