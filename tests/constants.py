"""Module skeleton for TestsFlextTapOracleConstants.

Test constants for flext-tap-oracle.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from typing import Final

from flext_tap_oracle import FlextTapOracleConstants
from flext_tests import FlextTestsConstants


class TestsFlextTapOracleConstants(FlextTestsConstants, FlextTapOracleConstants):
    """Test constants for flext-tap-oracle."""

    class TapOracle(FlextTapOracleConstants.TapOracle):
        """TapOracle domain namespace — inherits production constants."""

        class Tests:
            """Test-specific constants."""

            SHARED_CONTAINER_NAME: Final[str] = "flext-oracle-db-test"
            SHARED_CONTAINER_PORT_PREFIX: Final[str] = "1521"
            SHARED_CONTAINER_HOST: Final[str] = "localhost"
            SHARED_CONTAINER_DEFAULT_PORT: Final[int] = 1522
            SHARED_CONTAINER_USER: Final[str] = "flext_test"
            SHARED_CONTAINER_PASSWORD: Final[str] = "flext_test_password"
            SHARED_CONTAINER_SERVICE_NAME: Final[str] = "FLEXTDB"
            SHARED_CONTAINER_SCHEMA_NAME: Final[str] = "FLEXT_TEST"
            SHARED_ORACLE_HOST_ENV: Final[str] = "FLEXT_TAP_ORACLE_ORACLE_HOST"
            SHARED_ORACLE_PORT_ENV: Final[str] = "FLEXT_TAP_ORACLE_ORACLE_PORT"
            SHARED_ORACLE_USER_ENV: Final[str] = "FLEXT_TAP_ORACLE_ORACLE_USER"
            SHARED_ORACLE_PASSWORD_ENV: Final[str] = "FLEXT_TAP_ORACLE_ORACLE_PASSWORD"
            SHARED_ORACLE_SERVICE_ENV: Final[str] = (
                "FLEXT_TAP_ORACLE_ORACLE_SERVICE_NAME"
            )
            SHARED_ORACLE_SCHEMA_ENV: Final[str] = "FLEXT_TAP_ORACLE_SCHEMA_NAME"
            ORACLE_HOST_ENV: Final[str] = "ORACLE_HOST"
            ORACLE_PORT_ENV: Final[str] = "ORACLE_PORT"
            ORACLE_USERNAME_ENV: Final[str] = "ORACLE_USERNAME"
            ORACLE_PASSWORD_ENV: Final[str] = "ORACLE_PASSWORD"
            ORACLE_SERVICE_NAME_ENV: Final[str] = "ORACLE_SERVICE_NAME"
            FLEXT_ENV_NAME: Final[str] = "FLEXT_ENV"
            FLEXT_LOG_LEVEL_ENV: Final[str] = "FLEXT_LOG_LEVEL"
            SINGER_LOG_LEVEL_ENV: Final[str] = "SINGER_SDK_LOG_LEVEL"
            TEST_MODE_ENV: Final[str] = "ORACLE_TAP_TEST_MODE"
            TEST_ENV_VALUE: Final[str] = "test"
            DEBUG_LOG_LEVEL: Final[str] = "DEBUG"
            TRUE_VALUE: Final[str] = "true"
            SOCKET_TIMEOUT_SECONDS: Final[float] = 0.5
            UNIT_ORACLE_HOST: Final[str] = "test-oracle"
            UNIT_ORACLE_PORT: Final[int] = 1521
            UNIT_ORACLE_SERVICE_NAME: Final[str] = "TESTDB"
            UNIT_ORACLE_USER: Final[str] = "testuser"
            UNIT_ORACLE_PASSWORD: Final[str] = "testpass"
            UNIT_BATCH_SIZE: Final[int] = 1000
            CREATE_CONFIG_HOST: Final[str] = "localhost"
            CREATE_CONFIG_PORT: Final[int] = 1521
            CREATE_CONFIG_SERVICE_NAME: Final[str] = "XE"
            CREATE_CONFIG_USER: Final[str] = "tap_user"
            CREATE_CONFIG_PASSWORD: Final[str] = "secret"


c = TestsFlextTapOracleConstants
__all__: list[str] = ["TestsFlextTapOracleConstants", "c"]
