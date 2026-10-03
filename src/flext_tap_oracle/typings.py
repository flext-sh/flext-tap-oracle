"""FLEXT Tap Oracle Types.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT

"""

from __future__ import annotations

from flext_db_oracle import FlextDbOracleTypes
from flext_meltano import FlextMeltanoTypes


class FlextTapOracleTypes(FlextMeltanoTypes, FlextDbOracleTypes):
    """MRO facade composing Meltano + DbOracle type namespaces."""

    class TapOracle:
        """Tap Oracle domain namespace (flat members per AGENTS.md §149)."""

        type SummaryData = FlextMeltanoTypes.JsonMapping
        type OracleValue = FlextMeltanoTypes.JsonValue | None


t = FlextTapOracleTypes

__all__: list[str] = ["FlextTapOracleTypes", "t"]
