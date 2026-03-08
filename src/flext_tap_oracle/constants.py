"""FLEXT Tap Oracle Constants - Oracle tap extraction constants.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT

"""

from __future__ import annotations

from enum import StrEnum
from typing import Final, Literal

from flext_db_oracle import FlextDbOracleConstants
from flext_meltano import FlextMeltanoConstants


class FlextTapOracleConstants(FlextMeltanoConstants, FlextDbOracleConstants):
    """Oracle tap extraction-specific constants following FLEXT unified pattern.

    Inherits from FlextMeltanoConstants for universal constants, defines only
    Oracle tap-specific constants using nested namespace classes.

    Composes with FlextDbOracleConstants to avoid duplication and ensure consistency.
    """

    class TapOracle:
        """Tap Oracle  namespace for cross-project access."""

        MAX_PORT_NUMBER = 65535
        LARGE_TABLE_THRESHOLD = 100000
        EXCELLENT_PERFORMANCE_THRESHOLD = 1000
        GOOD_PERFORMANCE_THRESHOLD = 500
        MODERATE_PERFORMANCE_THRESHOLD = 100
        MAX_IDENTIFIER_LENGTH: Final[int] = 255
        DEFAULT_STREAM_PREFIX: Final[str] = "oracle"
        DEFAULT_OPERATION_NAME: Final[str] = "unknown"

        class EnvironmentDefaults:
            """Environment-specific performance defaults."""

            class Production:
                """Production environment defaults."""

                MAX_PARALLEL_STREAMS: Final[int] = 4
                QUERY_TIMEOUT_SECONDS: Final[int] = 300

            class Development:
                """Development environment defaults."""

                MAX_PARALLEL_STREAMS: Final[int] = 1
                QUERY_TIMEOUT_SECONDS: Final[int] = 60

            class Staging:
                """Staging environment defaults."""

                MAX_PARALLEL_STREAMS: Final[int] = 2
                QUERY_TIMEOUT_SECONDS: Final[int] = 180

        class SingerTypes:
            """Singer protocol type mappings for Oracle data types."""

            DEFAULT_TYPE: Final[str] = "string"
            NUMERIC_TYPE: Final[str] = "number"
            DATETIME_TYPE: Final[str] = "string"

        INITIAL_RECORD_COUNT: Final[int] = 0
        INITIAL_DURATION_SECONDS: Final[float] = 0.0

        class Oracle:
            """Oracle database connection constants."""

            DEFAULT_PORT: Final[int] = (
                FlextDbOracleConstants.DbOracle.Connection.DEFAULT_PORT
            )
            DEFAULT_TIMEOUT: Final[int] = (
                FlextDbOracleConstants.DbOracle.Connection.DEFAULT_TIMEOUT
            )
            DEFAULT_FETCH_SIZE: Final[int] = (
                FlextDbOracleConstants.DbOracle.Query.DEFAULT_ARRAY_SIZE
            )
            MAX_QUERY_TIMEOUT: Final[int] = (
                FlextDbOracleConstants.DbOracle.Query.MAX_QUERY_TIMEOUT
            )

        class Singer:
            """Singer tap configuration constants."""

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

        class Performance:
            """Oracle tap performance optimization constants."""

            DEFAULT_BATCH_SIZE: Final[int] = 1000
            MAX_PARALLEL_STREAMS: Final[int] = 5
            MEMORY_THRESHOLD_MB: Final[int] = 512

        class TapValidation:
            """Oracle tap validation constants.

            Note: Does not override parent Validation class to avoid inheritance conflicts.
            """

            MIN_BATCH_SIZE: Final[int] = 1
            MAX_TIMEOUT: Final[int] = (
                FlextMeltanoConstants.Performance.MAX_TIMEOUT_SECONDS
            )
            MAX_TABLE_NAME_LENGTH: Final[int] = (
                FlextDbOracleConstants.DbOracle.OracleValidation.MAX_TABLE_NAME_LENGTH
            )
            MAX_COLUMN_NAME_LENGTH: Final[int] = (
                FlextDbOracleConstants.DbOracle.OracleValidation.MAX_COLUMN_NAME_LENGTH
            )
            MAX_IDENTIFIER_LENGTH: Final[int] = 255
            MAX_STREAM_PREFIX_LENGTH: Final[int] = MAX_IDENTIFIER_LENGTH
            MAX_TABLES_FILTER_COUNT: Final[int] = 1000
            MAX_SCHEMAS_FILTER_COUNT: Final[int] = 100
            MAX_SAFE_PARALLEL_STREAMS: Final[int] = 8

        class Connection:
            """Oracle tap connection configuration."""

            DEFAULT_HOST: Final[str] = "localhost"
            DEFAULT_SERVICE_NAME: Final[str] = (
                FlextDbOracleConstants.DbOracle.Connection.DEFAULT_SERVICE_NAME
            )
            DEFAULT_USERNAME: Final[str] = (
                FlextDbOracleConstants.DbOracle.Connection.DEFAULT_USERNAME
            )
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

        type ReplicationMethodLiteral = Literal[
            Replication.Method.FULL_TABLE,
            Replication.Method.INCREMENTAL,
            Replication.Method.LOG_BASED,
        ]
        "Oracle replication method literal - references Replication.Method StrEnum members."
        TapReplicationMethod = Literal["FULL_TABLE", "INCREMENTAL"]
        TapStreamSelection = Literal["selected", "automatic", "excluded"]
        TapExecutionMode = Literal["discovery", "extraction", "test", "validate"]


c = FlextTapOracleConstants
__all__ = ["FlextTapOracleConstants", "c"]
