"""Protocols for flext-tap-oracle tests - uses composition with TestsFlextProtocols.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT

"""

from __future__ import annotations

from flext_tap_oracle import FlextTapOracleProtocols
from flext_tests import FlextTestsProtocols


class TestsFlextTapOracleProtocols(FlextTestsProtocols, FlextTapOracleProtocols):
    """Protocols for flext-tap-oracle tests - uses composition with TestsFlextProtocols.

    Architecture: Uses composition (not inheritance) with TestsFlextProtocols and FlextTapOracleProtocols
    for flext-tap-oracle-specific protocol definitions.

    Access patterns:
    - TestsFlextTapOracleProtocols.Tests.* = flext_tests test protocols (via composition)
    - TestsFlextTapOracleProtocols.TapOracle.* = flext-tap-oracle-specific protocols
      (``CommandRunner``, ``Tap``, inherited from ``FlextTapOracleProtocols``)
    - TestsFlextTapOracleProtocols.* = TestsFlextProtocols protocols (via composition)

    Rules:
    - Use composition, not inheritance (TestsFlextProtocols deprecates subclassing)
    - Generic protocols accessed via Tests namespace
    """

    # Why (bad-override fix, flext-tap-oracle PR #80): this class previously
    # redeclared a local ``TapOracle`` nested namespace to host three
    # test-only Protocol classes (MockOracleConnection, TestDataProvider,
    # TestAssertion). All three had zero workspace consumers (STRICT YAGNI)
    # and the redeclaration incompatibly shadowed the real, consumed
    # ``FlextTapOracleProtocols.TapOracle`` (CommandRunner/Tap, used by
    # src/flext_tap_oracle/tap.py and streams.py) inherited via multiple
    # inheritance — a pyrefly [bad-override] error. Deleted the dead
    # namespace instead of renaming it; ``TapOracle`` now resolves solely to
    # the inherited, real protocol.


p = TestsFlextTapOracleProtocols
__all__: list[str] = ["TestsFlextTapOracleProtocols", "p"]
