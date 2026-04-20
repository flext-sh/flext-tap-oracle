"""Types for flext-tap-oracle tests - uses composition with TestsFlextTypes.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT

"""

from __future__ import annotations

from collections.abc import (
    Mapping,
    Sequence,
)
from typing import Literal

from flext_core import FlextTypes
from flext_tests import FlextTestsTypes

from flext_tap_oracle import FlextTapOracleTypes


class TestsFlextTapOracleTypes(FlextTestsTypes, FlextTapOracleTypes):
    """Types for flext-tap-oracle tests - uses composition with TestsFlextTypes.

    Architecture: Uses composition (not inheritance) with TestsFlextTypes and FlextTapOracleTypes
    for flext-tap-oracle-specific type definitions.

    Access patterns:
    - TestsFlextTapOracleTypes.Tests.* = flext_tests test types (via composition)
    - TestsFlextTapOracleTypes.TapOracleTest.* = flext-tap-oracle-specific test types
    - TestsFlextTapOracleTypes.* = TestsFlextTypes types (via composition)

    Rules:
    - Use composition, not inheritance (TestsFlextTypes deprecates subclassing)
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

        type TestOraclePort = Literal[1521, 10521, 1522]
        type MockOracleRecord = Mapping[str, FlextTypes.Scalar]
        type MockOracleTable = Sequence[MockOracleRecord]
        type TestScenario = FlextTestsTypes.FlatContainerMapping
        type TestValidationResult = Mapping[
            str, bool | str | FlextTestsTypes.StrSequence
        ]
        type TestPerformanceResult = Mapping[str, float | int | str]


t = TestsFlextTapOracleTypes
__all__: list[str] = ["TestsFlextTapOracleTypes", "t"]
