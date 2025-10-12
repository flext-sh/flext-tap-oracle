"""FLEXT Tap Oracle Constants - Oracle tap extraction constants.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from typing import ClassVar, Final

from flext_core import FlextCore
from flext_db_oracle import FlextDbOracleConstants


class FlextMeltanoTapOracleConstants(FlextCore.Constants):
    """Oracle tap extraction-specific constants following FLEXT unified pattern.

    Inherits from FlextCore.Constants for universal constants, defines only
    Oracle tap-specific constants using nested namespace classes.

    Composes with FlextDbOracleConstants to avoid duplication and ensure consistency.
    """

    class Oracle:
        """Oracle database connection constants."""

        # Use FlextDbOracleConstants for Oracle-specific configuration
        DEFAULT_PORT: Final[int] = FlextDbOracleConstants.Connection.DEFAULT_PORT
        DEFAULT_TIMEOUT: Final[int] = FlextDbOracleConstants.Connection.DEFAULT_TIMEOUT

        # Oracle-specific fetch configuration
        DEFAULT_FETCH_SIZE: Final[int] = FlextDbOracleConstants.Query.DEFAULT_ARRAY_SIZE
        MAX_QUERY_TIMEOUT: Final[int] = FlextDbOracleConstants.Query.MAX_QUERY_TIMEOUT

    class Singer:
        """Singer tap configuration constants."""

        # Use FlextCore.Constants for performance settings
        DEFAULT_BATCH_SIZE: Final[int] = (
            FlextCore.Constants.Performance.DEFAULT_BATCH_SIZE
        )
        MAX_BATCH_SIZE: Final[int] = FlextCore.Constants.Performance.MAX_BATCH_ITEMS

    class Replication:
        """Oracle replication method constants."""

        REPLICATION_METHODS: ClassVar[Final[FlextCore.Types.StringList]] = [
            "FULL_TABLE",
            "INCREMENTAL",
            "LOG_BASED",
        ]

        DEFAULT_METHOD: Final[str] = "INCREMENTAL"

    class Validation:
        """Oracle tap validation constants."""

        # Use FlextCore.Constants for validation limits
        MIN_BATCH_SIZE: Final[int] = FlextCore.Constants.Performance.MIN_TAKE
        MAX_TIMEOUT: Final[int] = FlextCore.Constants.Performance.MAX_TIMEOUT_SECONDS

        # Use FlextDbOracleConstants for Oracle-specific validation
        MAX_TABLE_NAME_LENGTH: Final[int] = (
            FlextDbOracleConstants.Validation.MAX_TABLE_NAME_LENGTH
        )
        MAX_COLUMN_NAME_LENGTH: Final[int] = (
            FlextDbOracleConstants.Validation.MAX_COLUMN_NAME_LENGTH
        )

    class Connection:
        """Oracle tap connection configuration."""

        DEFAULT_HOST: Final[str] = FlextDbOracleConstants.Defaults.DEFAULT_HOST
        DEFAULT_SERVICE_NAME: Final[str] = (
            FlextDbOracleConstants.Defaults.DEFAULT_SERVICE_NAME
        )
        DEFAULT_USERNAME: Final[str] = FlextDbOracleConstants.Defaults.DEFAULT_USERNAME

        # Pool configuration
        DEFAULT_POOL_MIN: Final[int] = (
            FlextDbOracleConstants.Connection.DEFAULT_POOL_MIN
        )
        DEFAULT_POOL_MAX: Final[int] = (
            FlextDbOracleConstants.Connection.DEFAULT_POOL_MAX
        )
        DEFAULT_POOL_TIMEOUT: Final[int] = (
            FlextDbOracleConstants.Connection.DEFAULT_POOL_TIMEOUT
        )

    class Extraction:
        """Tap-specific extraction configuration."""

        DEFAULT_QUERY_LIMIT: Final[int] = (
            FlextDbOracleConstants.Query.DEFAULT_QUERY_LIMIT
        )
        DEFAULT_COMMIT_SIZE: Final[int] = (
            FlextDbOracleConstants.Performance.DEFAULT_COMMIT_SIZE
        )
        TEST_QUERY: Final[str] = FlextDbOracleConstants.Query.TEST_QUERY


__all__ = ["FlextMeltanoTapOracleConstants"]
