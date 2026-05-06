"""FLEXT Tap Oracle Constants - Oracle tap extraction constants.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT

"""

from __future__ import annotations

from enum import StrEnum, unique
from typing import Final

from flext_db_oracle import FlextDbOracleConstants
from flext_meltano import c, t


class FlextTapOracleConstants(c, FlextDbOracleConstants):
    """Oracle tap extraction-specific constants following FLEXT unified pattern.

    Inherits from FlextMeltanoConstants for universal constants, defines only
    Oracle tap-specific constants using nested namespace classes.

    Composes with FlextDbOracleConstants to avoid duplication and ensure consistency.
    """

    class TapOracle:
        """Tap Oracle  namespace for cross-project access."""

        MAX_PORT_NUMBER = 65535
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

        class Extraction:
            """Tap-specific extraction configuration."""

            TEST_QUERY: Final[str] = "SELECT 1 FROM DUAL"


c = FlextTapOracleConstants
__all__: t.StrSequence = ("FlextTapOracleConstants", "c")
