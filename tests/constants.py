"""Module skeleton for TestsFlextTapOracleConstants.

Test constants for flexttaporacle.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from enum import StrEnum, unique


class TestsFlextTapOracleConstants:
    """Test constants for flexttaporacle."""

    @unique
    class TestOracleHost(StrEnum):
        LOCALHOST = "localhost"
        TEST_HOST = "test-host"

    @unique
    class TestServiceName(StrEnum):
        XE = "XE"
        ORCL = "ORCL"
        TESTDB = "TESTDB"

    @unique
    class TestReplicationMethod(StrEnum):
        FULL_TABLE = "FULL_TABLE"
        INCREMENTAL = "INCREMENTAL"


c = TestsFlextTapOracleConstants
__all__ = ["TestsFlextTapOracleConstants", "c"]
