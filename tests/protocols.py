"""Test protocol definitions for flext-tap-oracle.

Provides TestsFlextTapOracleProtocols, combining FlextTestsProtocols with
FlextMeltanoTapOracleProtocols for test-specific protocol definitions.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from flext_tests.protocols import FlextTestsProtocols

from flext_tap_oracle.protocols import FlextMeltanoTapOracleProtocols


class TestsFlextTapOracleProtocols(FlextTestsProtocols, FlextMeltanoTapOracleProtocols):
    """Test protocols combining FlextTestsProtocols and FlextMeltanoTapOracleProtocols.

    Provides access to:
    - tp.Tests.Docker.* (from FlextTestsProtocols)
    - tp.Tests.Factory.* (from FlextTestsProtocols)
    - tp.TapOracle.* (from FlextMeltanoTapOracleProtocols)
    """

    class Tests:
        """Project-specific test protocols.

        Extends FlextTestsProtocols.Tests with TapOracle-specific protocols.
        """

        class TapOracle:
            """TapOracle-specific test protocols."""


# Runtime aliases
p = TestsFlextTapOracleProtocols
tp = TestsFlextTapOracleProtocols

__all__ = ["TestsFlextTapOracleProtocols", "p", "tp"]
