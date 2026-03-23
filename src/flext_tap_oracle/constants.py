"""FLEXT Tap Oracle Constants - Oracle tap extraction constants.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT

"""

from __future__ import annotations

from enum import StrEnum, unique
from typing import Final

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

            class Development:
                """Development environment defaults."""

            class Staging:
                """Staging environment defaults."""

        class SingerTypes:
            """Singer protocol type mappings for Oracle data types."""

            DEFAULT_TYPE: Final[str] = "string"

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

        class Performance:
            """Oracle tap performance optimization constants."""

            DEFAULT_BATCH_SIZE: Final[int] = FlextDbOracleConstants.DEFAULT_BATCH_SIZE

        class TapValidation:
            """Oracle tap validation constants.

            Note: Does not override parent Validation class to avoid inheritance conflicts.
            """

            MAX_IDENTIFIER_LENGTH: Final[int] = 255

        class Connection:
            """Oracle tap connection configuration."""

            DEFAULT_HOST: Final[str] = FlextDbOracleConstants.LOCALHOST
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

        class Extraction:
            """Tap-specific extraction configuration."""

            TEST_QUERY: Final[str] = "SELECT 1 FROM DUAL"

    @unique
    class MeltanoTapOracleProjectType(StrEnum):
        """Project type literals for Meltano tap metadata."""

        LIBRARY = "library"
        APPLICATION = "application"
        SERVICE = "service"
        MELTANO_PROJECT = "meltano-project"
        ELT_PIPELINE = "elt-pipeline"
        DATA_PIPELINE = "data-pipeline"
        ETL_SERVICE = "etl-service"
        SINGER_TAP = "singer-tap"
        SINGER_TARGET = "singer-target"
        DBT_PROJECT = "dbt-project"
        DATA_INTEGRATION = "data-integration"
        MELTANO_PLUGIN = "meltano-plugin"
        DATA_CONNECTOR = "data-connector"
        ORACLE_SERVICE = "oracle-service"
        DATABASE_SERVICE = "database-service"
        DATA_WAREHOUSE = "data-warehouse"
        ORACLE_CLIENT = "oracle-client"
        DB_MIGRATION = "db-migration"
        SCHEMA_MANAGER = "schema-manager"
        SQL_SERVICE = "sql-service"
        ORACLE_API = "oracle-api"
        DATABASE_API = "database-api"
        ORACLE_TAP = "oracle-tap"
        ORACLE_TARGET = "oracle-target"

    @unique
    class TapOracleProjectType(StrEnum):
        """Project type literals for tap package metadata."""

        SINGER_TAP = "singer-tap"
        ORACLE_EXTRACTOR = "oracle-extractor"
        DATABASE_EXTRACTOR = "database-extractor"
        SINGER_TAP_ORACLE = "singer-tap-oracle"
        TAP_ORACLE = "tap-oracle"
        ORACLE_CONNECTOR = "oracle-connector"
        DATABASE_CONNECTOR = "database-connector"
        SINGER_PROTOCOL = "singer-protocol"
        ORACLE_ETL = "oracle-etl"
        DATABASE_ETL = "database-etl"
        ORACLE_INTEGRATION = "oracle-integration"
        SINGER_STREAM = "singer-stream"
        ETL_TAP = "etl-tap"
        DATA_PIPELINE = "data-pipeline"
        ORACLE_TAP = "oracle-tap"
        SINGER_INTEGRATION = "singer-integration"

    @unique
    class TestOracleHost(StrEnum):
        """Test Oracle host literals."""

        LOCALHOST = "localhost"
        TEST_HOST = "test-host"

    @unique
    class TestServiceName(StrEnum):
        """Test Oracle service name literals."""

        XE = "XE"
        ORCL = "ORCL"
        TESTDB = "TESTDB"

    @unique
    class TestReplicationMethod(StrEnum):
        """Test replication method literals."""

        FULL_TABLE = "FULL_TABLE"
        INCREMENTAL = "INCREMENTAL"


c = FlextTapOracleConstants
__all__ = ["FlextTapOracleConstants", "c"]
