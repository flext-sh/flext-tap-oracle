"""Module skeleton for TestsFlextTapOracleConstants.

Test constants for flext-tap-oracle.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from enum import StrEnum, unique

from flext_tests import FlextTestsConstants

from flext_tap_oracle import FlextTapOracleConstants


class TestsFlextTapOracleConstants(FlextTestsConstants, FlextTapOracleConstants):
    """Test constants for flext-tap-oracle."""

    class TapOracle(FlextTapOracleConstants.TapOracle):
        """TapOracle domain namespace — inherits production constants."""

        class Tests:
            """Test-specific constants."""

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


c = TestsFlextTapOracleConstants
__all__: list[str] = ["TestsFlextTapOracleConstants", "c"]
