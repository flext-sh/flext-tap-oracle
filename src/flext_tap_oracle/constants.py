# AUTO-GENERATED FILE — Regenerate with: make gen
"""FLEXT Tap Oracle Constants - Oracle tap extraction constants.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT

"""

from __future__ import annotations

from flext_db_oracle import FlextDbOracleConstants
from flext_meltano import FlextMeltanoConstants

from flext_tap_oracle._constants import (
    FlextTapOracleConstantsBase,
    FlextTapOracleConstantsReplication,
    FlextTapOracleConstantsValues,
)


class FlextTapOracleConstants(FlextMeltanoConstants, FlextDbOracleConstants):
    """Oracle tap extraction-specific constants following FLEXT unified pattern.

    Inherits from FlextMeltanoConstants for universal constants, defines only
    Oracle tap-specific constants using nested namespace classes.

    Composes with FlextDbOracleConstants to avoid duplication and ensure consistency.
    """

    class TapOracle(
        FlextTapOracleConstantsBase,
        FlextTapOracleConstantsReplication,
        FlextTapOracleConstantsValues.TapOracle,
    ):
        """Tap Oracle namespace for cross-project access."""


c = FlextTapOracleConstants

__all__: list[str] = ["FlextTapOracleConstants", "c"]
