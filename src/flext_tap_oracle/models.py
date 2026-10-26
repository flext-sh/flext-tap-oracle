# AUTO-GENERATED FILE — Regenerate with: make gen
"""Models for flext-tap-oracle.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT

"""

from __future__ import annotations

from flext_db_oracle import m
from flext_meltano import m as flext_meltano_m

from flext_tap_oracle._models import (
    FlextTapOracleModelsBase,
    FlextTapOracleModelsParams,
)


class FlextTapOracleModels(flext_meltano_m, m):
    """Models facade for the Oracle tap (flext-meltano + flext-db-oracle)."""

    class TapOracle(FlextTapOracleModelsBase, FlextTapOracleModelsParams):
        """Tap Oracle namespace for cross-project access."""


m = FlextTapOracleModels
__all__: list[str] = ["FlextTapOracleModels", "m"]
