"""Types for flext-tap-oracle tests - uses composition with FlextTestsTypes.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT

"""

from __future__ import annotations

from collections.abc import Mapping, Sequence
from typing import Literal

from flext_core import FlextTypes
from flext_tests import FlextTestsTypes

from flext_tap_oracle import FlextTapOracleConstants as _c, FlextTapOracleTypes


class FlextTapOracleTestTypes(FlextTestsTypes, FlextTapOracleTypes):
    """Types for flext-tap-oracle tests - uses composition with FlextTestsTypes.

    Architecture: Uses composition (not inheritance) with FlextTestsTypes and FlextTapOracleTypes
    for flext-tap-oracle-specific type definitions.

    Access patterns:
    - FlextTapOracleTestTypes.Tests.* = flext_tests test types (via composition)
    - FlextTapOracleTestTypes.TapOracleTest.* = flext-tap-oracle-specific test types
    - FlextTapOracleTestTypes.* = FlextTestsTypes types (via composition)

    Rules:
    - Use composition, not inheritance (FlextTestsTypes deprecates subclassing)
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

        type TestOracleHost = _c.TestOracleHost
        type TestOraclePort = Literal[1521, 10521, 1522]
        type TestServiceName = _c.TestServiceName
        type TestReplicationMethod = _c.TestReplicationMethod
        type MockOracleRecord = Mapping[str, FlextTypes.Scalar]
        type MockOracleTable = Sequence[MockOracleRecord]
        type TestScenario = t.ContainerMapping
        type TestValidationResult = Mapping[str, bool | str | t.StrSequence]
        type TestPerformanceResult = Mapping[str, float | int | str]


t = FlextTapOracleTestTypes
__all__ = ["FlextTapOracleTestTypes", "t"]
