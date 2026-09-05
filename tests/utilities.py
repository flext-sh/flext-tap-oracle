"""Public test utilities facade for flext-tap-oracle.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT

"""

from __future__ import annotations

from flext_tap_oracle import FlextTapOracleUtilities
from flext_tests import FlextTestsUtilities


class TestsFlextTapOracleUtilities(FlextTestsUtilities, FlextTapOracleUtilities):
    """Compose the canonical test and tap-oracle utility facades."""


u = TestsFlextTapOracleUtilities
__all__: list[str] = ["TestsFlextTapOracleUtilities", "u"]
