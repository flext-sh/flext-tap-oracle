"""FLEXT Tap Oracle Types.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT

"""

from __future__ import annotations

from flext_db_oracle import FlextDbOracleTypes
from flext_meltano import t


class FlextTapOracleTypes(t, FlextDbOracleTypes):
    """MRO facade composing Meltano + DbOracle type namespaces."""

    class TapOracle:
        """Tap Oracle domain namespace (flat members per AGENTS.md §149)."""

        type SummaryData = t.JsonMapping
        type OracleValue = t.JsonValue | None


t = FlextTapOracleTypes

__all__: list[str] = ["FlextTapOracleTypes", "t"]
