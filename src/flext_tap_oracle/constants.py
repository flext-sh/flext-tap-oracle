"""FLEXT Tap Oracle Constants - Oracle tap extraction constants.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT

"""

from __future__ import annotations

from enum import StrEnum
from typing import Final, Literal

from flext_core import FlextConstants
from flext_db_oracle import FlextDbOracleConstants


class FlextMeltanoTapOracleConstants(FlextConstants):
    """Oracle tap extraction-specific constants following FLEXT unified pattern.

    Inherits from FlextConstants for universal constants, defines only
    Oracle tap-specific constants using nested namespace classes.

    Composes with FlextDbOracleConstants to avoid duplication and ensure consistency.
    """

    class Oracle:
        """Oracle database connection constants."""

        # Use FlextDbOracleConstants for Oracle-specific configuration
        DEFAULT_PORT: Final[int] = (
            FlextDbOracleConstants.DbOracle.Connection.DEFAULT_PORT
        )
        DEFAULT_TIMEOUT: Final[int] = (
            FlextDbOracleConstants.DbOracle.Connection.DEFAULT_TIMEOUT
        )

        # Oracle-specific fetch configuration
        DEFAULT_FETCH_SIZE: Final[int] = (
            FlextDbOracleConstants.DbOracle.Query.DEFAULT_ARRAY_SIZE
        )
        MAX_QUERY_TIMEOUT: Final[int] = (
            FlextDbOracleConstants.DbOracle.Query.MAX_QUERY_TIMEOUT
        )

    class Singer:
        """Singer tap configuration constants."""

        # Use FlextConstants for performance settings
        DEFAULT_BATCH_SIZE: Final[int] = (
            FlextConstants.Performance.BatchProcessing.DEFAULT_SIZE
        )
        MAX_BATCH_SIZE: Final[int] = (
            FlextConstants.Performance.BatchProcessing.MAX_ITEMS
        )

    class Replication:
        """Oracle replication method constants."""

        class Method(StrEnum):
            """Oracle replication methods using StrEnum for type safety.

            DRY Pattern:
                StrEnum is the single source of truth. Use Method.FULL_TABLE.value
                or Method.FULL_TABLE directly - no base strings needed.
            """

            FULL_TABLE = "FULL_TABLE"
            INCREMENTAL = "INCREMENTAL"
            LOG_BASED = "LOG_BASED"

        DEFAULT_METHOD: Final[str] = Method.INCREMENTAL

    class TapValidation:
        """Oracle tap validation constants.

        Note: Does not override parent Validation class to avoid inheritance conflicts.
        """

        # Use FlextConstants for validation limits
        MIN_BATCH_SIZE: Final[int] = 1  # Minimum batch size is 1 record
        MAX_TIMEOUT: Final[int] = FlextConstants.Performance.MAX_TIMEOUT_SECONDS

        # Use FlextDbOracleConstants for Oracle-specific validation
        # Oracle identifiers are limited to 30 characters
        MAX_TABLE_NAME_LENGTH: Final[int] = (
            FlextDbOracleConstants.DbOracle.OracleValidation.MAX_TABLE_NAME_LENGTH
        )
        MAX_COLUMN_NAME_LENGTH: Final[int] = (
            FlextDbOracleConstants.DbOracle.OracleValidation.MAX_COLUMN_NAME_LENGTH
        )

    class Connection:
        """Oracle tap connection configuration."""

        DEFAULT_HOST: Final[str] = "localhost"
        DEFAULT_SERVICE_NAME: Final[str] = (
            FlextDbOracleConstants.DbOracle.Connection.DEFAULT_SERVICE_NAME
        )
        DEFAULT_USERNAME: Final[str] = (
            FlextDbOracleConstants.DbOracle.Connection.DEFAULT_USERNAME
        )

        # Pool configuration
        DEFAULT_POOL_MIN: Final[int] = (
            FlextDbOracleConstants.DbOracle.Connection.DEFAULT_POOL_MIN
        )
        DEFAULT_POOL_MAX: Final[int] = (
            FlextDbOracleConstants.DbOracle.Connection.DEFAULT_POOL_MAX
        )
        DEFAULT_POOL_TIMEOUT: Final[int] = (
            FlextDbOracleConstants.DbOracle.Connection.DEFAULT_POOL_TIMEOUT
        )

    class Extraction:
        """Tap-specific extraction configuration."""

        DEFAULT_QUERY_LIMIT: Final[int] = (
            FlextDbOracleConstants.DbOracle.Query.DEFAULT_QUERY_LIMIT
        )
        DEFAULT_COMMIT_SIZE: Final[int] = (
            FlextConstants.Performance.BatchProcessing.DEFAULT_SIZE
        )
        TEST_QUERY: Final[str] = (
            FlextDbOracleConstants.DbOracle.Query.TEST_QUERY
        )

    # Type-safe literals - PEP 695 syntax for type checking
    # All Literal types reference StrEnum members where available - NO string duplication!
    type ReplicationMethodLiteral = Literal[
        Replication.Method.FULL_TABLE,
        Replication.Method.INCREMENTAL,
        Replication.Method.LOG_BASED,
    ]
    """Oracle replication method literal - references Replication.Method StrEnum members."""


c = FlextMeltanoTapOracleConstants

__all__ = ["FlextMeltanoTapOracleConstants", "c"]
