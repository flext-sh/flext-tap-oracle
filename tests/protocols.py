"""Protocols for flext-tap-oracle tests - uses composition with TestsFlextProtocols.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT

"""

from __future__ import annotations

from flext_tap_oracle import FlextTapOracleProtocols
from flext_tests import FlextTestsProtocols


class TestsFlextTapOracleProtocols(FlextTestsProtocols, FlextTapOracleProtocols):
    """Compose the canonical test and tap-oracle protocol facades."""


p = TestsFlextTapOracleProtocols
__all__: list[str] = ["TestsFlextTapOracleProtocols", "p"]
