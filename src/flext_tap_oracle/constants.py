"""FLEXT Tap Oracle Constants - Oracle tap extraction constants.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT

"""

from __future__ import annotations

from enum import StrEnum
from typing import Final, Literal

from flext_db_oracle import FlextDbOracleConstants
from flext_meltano import FlextMeltanoConstants


class FlextMeltanoTapOracleConstants(FlextMeltanoConstants, FlextDbOracleConstants):
    """Oracle tap extraction-specific constants following FLEXT unified pattern.

    Inherits from FlextMeltanoConstants for universal constants, defines only
    Oracle tap-specific constants using nested namespace classes.

    Composes with FlextDbOracleConstants to avoid duplication and ensure consistency.
    """

    class TapOracle:
        """Tap Oracle  namespace for cross-project access."""

        # Constants
        MAX_PORT_NUMBER = 65535
        LARGE_TABLE_THRESHOLD = 100000
        EXCELLENT_PERFORMANCE_THRESHOLD = 1000
        GOOD_PERFORMANCE_THRESHOLD = 500
        MODERATE_PERFORMANCE_THRESHOLD = 100

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

            # Use FlextMeltanoConstants for performance settings
            DEFAULT_BATCH_SIZE: Final[int] = (
                FlextMeltanoConstants.Performance.BatchProcessing.DEFAULT_SIZE
            )
            MAX_BATCH_SIZE: Final[int] = (
                FlextMeltanoConstants.Performance.BatchProcessing.MAX_ITEMS
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

            # Use FlextMeltanoConstants for validation limits
            MIN_BATCH_SIZE: Final[int] = 1  # Minimum batch size is 1 record
            MAX_TIMEOUT: Final[int] = (
                FlextMeltanoConstants.Performance.MAX_TIMEOUT_SECONDS
            )

            # Use FlextDbOracleConstants for Oracle-specific validation
            # Oracle identifiers are limited to 30 characters
            MAX_TABLE_NAME_LENGTH: Final[int] = (
                FlextDbOracleConstants.DbOracle.OracleValidation.MAX_TABLE_NAME_LENGTH
            )
            MAX_COLUMN_NAME_LENGTH: Final[int] = (
                FlextDbOracleConstants.DbOracle.OracleValidation.MAX_COLUMN_NAME_LENGTH
            )

            # Stream and filter validation limits
            # Oracle identifier limits (255 is max identifier length in Oracle)
            MAX_IDENTIFIER_LENGTH: Final[int] = 255
            MAX_STREAM_PREFIX_LENGTH: Final[int] = MAX_IDENTIFIER_LENGTH

            # Collection size limits
            MAX_TABLES_FILTER_COUNT: Final[int] = 1000  # Max number of tables to filter
            MAX_SCHEMAS_FILTER_COUNT: Final[int] = (
                100  # Max number of schemas to filter
            )

            # Performance validation limits
            MAX_SAFE_PARALLEL_STREAMS: Final[int] = (
                8  # Max parallel streams without memory issues
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
                FlextMeltanoConstants.Performance.BatchProcessing.DEFAULT_SIZE
            )
            TEST_QUERY: Final[str] = FlextDbOracleConstants.DbOracle.Query.TEST_QUERY

        # Type-safe literals - PEP 695 syntax for type checking
        # All Literal types reference StrEnum members where available - NO string duplication!
        type ReplicationMethodLiteral = Literal[
            Replication.Method.FULL_TABLE,
            Replication.Method.INCREMENTAL,
            Replication.Method.LOG_BASED,
        ]
        """Oracle replication method literal - references Replication.Method StrEnum members."""

        # Tap-specific type definitions
        TapReplicationMethod = Literal["FULL_TABLE", "INCREMENTAL"]
        TapStreamSelection = Literal["selected", "automatic", "excluded"]
        TapExecutionMode = Literal["discovery", "extraction", "test", "validate"]


c = FlextMeltanoTapOracleConstants

__all__ = ["FlextMeltanoTapOracleConstants", "c"]
