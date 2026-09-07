"""Public test constants facade for flext-tap-oracle.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT

"""

from __future__ import annotations

from flext_tap_oracle import FlextTapOracleConstants
from flext_tests import FlextTestsConstants


class TestsFlextTapOracleConstants(FlextTestsConstants, FlextTapOracleConstants):
    """Compose the canonical test and tap-oracle constants facades."""


c = TestsFlextTapOracleConstants
__all__: list[str] = ["TestsFlextTapOracleConstants", "c"]
