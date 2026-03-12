"""Types for flext-tap-oracle tests - uses composition with FlextTestsTypes.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT

"""

from __future__ import annotations

from typing import Literal

from flext_tests import FlextTestsTypes

from flext_tap_oracle import t


class TestsFlextTapOracleTypes(FlextTestsTypes):
    """Types for flext-tap-oracle tests - uses composition with FlextTestsTypes.

    Architecture: Uses composition (not inheritance) with FlextTestsTypes and FlextTapOracleTypes
    for flext-tap-oracle-specific type definitions.

    Access patterns:
    - TestsFlextTapOracleTypes.Tests.* = flext_tests test types (via composition)
    - TestsFlextTapOracleTypes.TapOracle.* = flext-tap-oracle-specific test types
    - TestsFlextTapOracleTypes.* = FlextTestsTypes types (via composition)

    Rules:
    - Use composition, not inheritance (FlextTestsTypes deprecates subclassing)
    - flext-tap-oracle-specific types go in TapOracle namespace
    - Generic types accessed via Tests namespace
    """

    class TapOracle:
        """Tap Oracle test types - domain-specific for Oracle tap testing.

        Contains test types specific to Oracle tap functionality including:
        - Test configuration types
        - Mock data types
        - Test scenario types
        """

        type TestOracleHost = Literal["localhost", "test-host"]
        type TestOraclePort = Literal[1521, 10521, 1522]
        type TestServiceName = Literal["XE", "ORCL", "TESTDB"]
        type TestReplicationMethod = Literal["FULL_TABLE", "INCREMENTAL"]
        type MockOracleRecord = dict[str, t.Scalar]
        type MockOracleTable = list[MockOracleRecord]
        type TestScenario = dict[str, object]
        type TestValidationResult = dict[str, bool | str | list[str]]
        type TestPerformanceResult = dict[str, float | int | str]


tt = TestsFlextTapOracleTypes
__all__ = ["TestsFlextTapOracleTypes", "tt"]
