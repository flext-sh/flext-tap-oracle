"""FLEXT Tap Oracle Types.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT

"""

from __future__ import annotations

from flext_db_oracle import FlextDbOracleTypes
from flext_meltano import FlextMeltanoTypes

from flext_tap_oracle._typings.base import FlextTapOracleTypingsBase


class FlextTapOracleTypes(FlextMeltanoTypes, FlextDbOracleTypes):
    """MRO facade composing Meltano + DbOracle type namespaces."""

    class TapOracle:
        """Tap Oracle domain namespace (flat members per AGENTS.md §149)."""

        OracleValue = FlextTapOracleTypingsBase.OracleValue


t = FlextTapOracleTypes

__all__: list[str] = ["FlextTapOracleTypes", "t"]
