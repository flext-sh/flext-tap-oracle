"""Types for flext-tap-oracle tests - uses composition with t.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT

"""

from __future__ import annotations

from typing import Literal

from flext_core.typings import FlextTypes

from flext_tap_oracle import c
from flext_tap_oracle.typings import FlextTapOracleTypes


class TestsFlextTapOracleTypes(FlextTapOracleTypes):
    """Types for flext-tap-oracle tests - uses composition with t.

    Architecture: Uses composition (not inheritance) with t and FlextTapOracleTypes
    for flext-tap-oracle-specific type definitions.

    Access patterns:
    - TestsFlextTapOracleTypes.Tests.* = flext_tests test types (via composition)
    - TestsFlextTapOracleTypes.TapOracleTest.* = flext-tap-oracle-specific test types
    - TestsFlextTapOracleTypes.* = t types (via composition)

    Rules:
    - Use composition, not inheritance (t deprecates subclassing)
    - flext-tap-oracle-specific types go in TapOracleTest namespace
    - Generic types accessed via Tests namespace
    """

    class TapOracleTest:
        """Tap Oracle test types - domain-specific for Oracle tap testing.

        Contains test types specific to Oracle tap functionality including:
        - Test configuration types
        - Mock data types
        - Test scenario types
        """

        type TestOracleHost = c.TestOracleHost
        type TestOraclePort = Literal[1521, 10521, 1522]
        type TestServiceName = c.TestServiceName
        type TestReplicationMethod = c.TestReplicationMethod
        type MockOracleRecord = dict[str, FlextTypes.Scalar]
        type MockOracleTable = list[MockOracleRecord]
        type TestScenario = dict[str, object]
        type TestValidationResult = dict[str, bool | str | list[str]]
        type TestPerformanceResult = dict[str, float | int | str]


tt = TestsFlextTapOracleTypes
__all__ = ["TestsFlextTapOracleTypes", "tt"]

t = TestsFlextTapOracleTypes
