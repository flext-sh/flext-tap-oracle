"""Public test typing facade for flext-tap-oracle.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT

"""

from __future__ import annotations

from flext_tap_oracle import FlextTapOracleTypes
from flext_tests import FlextTestsTypes


class TestsFlextTapOracleTypes(FlextTestsTypes, FlextTapOracleTypes):
    """Compose the canonical test and tap-oracle typing facades."""


t = TestsFlextTapOracleTypes
__all__: list[str] = ["TestsFlextTapOracleTypes", "t"]
