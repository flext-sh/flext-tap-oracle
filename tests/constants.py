"""Module skeleton for TestsFlextTapOracleConstants.

Test constants for flext-tap-oracle.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from flext_tests import FlextTestsConstants

from flext_tap_oracle import FlextTapOracleConstants


class TestsFlextTapOracleConstants(FlextTestsConstants, FlextTapOracleConstants):
    """Test constants for flext-tap-oracle."""

    class TapOracle(FlextTapOracleConstants.TapOracle):
        """TapOracle domain namespace — inherits production constants."""

        class Tests:
            """Test-specific constants."""


c = TestsFlextTapOracleConstants
__all__: list[str] = ["TestsFlextTapOracleConstants", "c"]
