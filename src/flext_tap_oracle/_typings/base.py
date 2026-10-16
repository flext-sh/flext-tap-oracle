"""Tap Oracle type alias declarations.

Copyright (c) 2026 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from flext_meltano import FlextMeltanoTypes


class FlextTapOracleTypingsBase:
    """Tap Oracle value type aliases composed into ``t.TapOracle``."""

    type OracleValue = FlextMeltanoTypes.JsonValue | None


__all__: list[str] = [
    "FlextTapOracleTypingsBase",
    "OracleValue",
]
