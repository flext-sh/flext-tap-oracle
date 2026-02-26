"""Types for flext-tap-oracle tests - uses composition with FlextTestsTypes.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT

"""

from __future__ import annotations

from typing import Literal

from flext_tap_oracle import t
from flext_tests import FlextTestsTypes


class TestsFlextMeltanoTapOracleTypes(FlextTestsTypes):
    """Types for flext-tap-oracle tests - uses composition with FlextTestsTypes.

    Architecture: Uses composition (not inheritance) with FlextTestsTypes and FlextMeltanoTapOracleTypes
    for flext-tap-oracle-specific type definitions.

    Access patterns:
    - TestsFlextMeltanoTapOracleTypes.Tests.* = flext_tests test types (via composition)
    - TestsFlextMeltanoTapOracleTypes.TapOracle.* = flext-tap-oracle-specific test types
    - TestsFlextMeltanoTapOracleTypes.* = FlextTestsTypes types (via composition)

    Rules:
    - Use composition, not inheritance (FlextTestsTypes deprecates subclassing)
    - flext-tap-oracle-specific types go in TapOracle namespace
    - Generic types accessed via Tests namespace
    """

    # TapOracle-specific test types namespace
    class TapOracle:
        """Tap Oracle test types - domain-specific for Oracle tap testing.

        Contains test types specific to Oracle tap functionality including:
        - Test configuration types
        - Mock data types
        - Test scenario types
        """

        # Test configuration literals
        type TestOracleHost = Literal["localhost", "test-host"]
        type TestOraclePort = Literal[1521, 10521, 1522]
        type TestServiceName = Literal["XE", "ORCL", "TESTDB"]
        type TestReplicationMethod = Literal["FULL_TABLE", "INCREMENTAL"]

        # Test data types
        type MockOracleRecord = dict[str, str | int | float | bool]
        type MockOracleTable = list[MockOracleRecord]
        type TestScenario = dict[str, t.GeneralValueType]

        # Test result types
        type TestValidationResult = dict[str, bool | str | list[str]]
        type TestPerformanceResult = dict[str, float | int | str]


# Alias for simplified usage
tt = TestsFlextMeltanoTapOracleTypes

__all__ = [
    "TestsFlextMeltanoTapOracleTypes",
    "tt",
]
