"""Models for flext-tap-oracle.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT

"""

from __future__ import annotations

from flext_db_oracle import FlextDbOracleModels
from flext_meltano import FlextMeltanoModels

from flext_tap_oracle._models.base import FlextTapOracleModelsBase
from flext_tap_oracle._models.params import FlextTapOracleModelsParams


class FlextTapOracleModels(FlextMeltanoModels, FlextDbOracleModels):
    """Models facade for the Oracle tap (flext-meltano + flext-db-oracle)."""

    class TapOracle(FlextTapOracleModelsBase):
        """Tap Oracle namespace for cross-project access."""

        OracleTapDiscoverParams = FlextTapOracleModelsParams.OracleTapDiscoverParams
        OracleTapSyncParams = FlextTapOracleModelsParams.OracleTapSyncParams


m = FlextTapOracleModels

__all__: list[str] = ["FlextTapOracleModels", "m"]
