"""FLEXT Tap Oracle Constants - Oracle tap extraction constants.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT

"""

from __future__ import annotations

from enum import StrEnum, unique
from typing import TYPE_CHECKING, Final

from flext_db_oracle import c as _db_oracle_c
from flext_meltano import c

from ._constants.values import FlextTapOracleConstantsValues

if TYPE_CHECKING:
    from flext_meltano import t


class FlextTapOracleConstants(c, _db_oracle_c):
    """Oracle tap extraction-specific constants following FLEXT unified pattern.

    Inherits from FlextMeltanoConstants for universal constants, defines only
    Oracle tap-specific constants using nested namespace classes.

    Composes with FlextDbOracleConstants to avoid duplication and ensure consistency.
    """

    class TapOracle(FlextTapOracleConstantsValues.TapOracle):
        """Tap Oracle  namespace for cross-project access."""

        MAX_IDENTIFIER_LENGTH: Final[int] = 255
        DEFAULT_STREAM_PREFIX: Final[str] = "oracle"
        DEFAULT_OPERATION_NAME: Final[str] = "unknown"

        INITIAL_RECORD_COUNT: Final[int] = 0

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

        class Extraction(FlextTapOracleConstantsValues.TapOracle.Extraction):
            """Tap-specific extraction configuration."""


c = FlextTapOracleConstants
__all__: t.StrSequence = ("FlextTapOracleConstants", "c")
