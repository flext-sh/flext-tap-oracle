# AUTO-GENERATED FILE — Regenerate with: make gen
"""Static instance-to-protocol evidence required by candidate admission.

Copyright (c) 2026 FLEXT Team. All rights reserved.
src/flext_tap_oracle/_protocols/_model_conformance
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from flext_tap_oracle import m, p

    def model_protocol_1(
        value: m.TapOracle.ConfigNamespace,
    ) -> p.TapOracle.ConfigNamespace:
        return value

    def model_protocol_2(
        value: m.TapOracle.OracleTapDiscoverParams,
    ) -> p.TapOracle.OracleTapDiscoverParams:
        return value

    def model_protocol_3(
        value: m.TapOracle.OracleTapSyncParams,
    ) -> p.TapOracle.OracleTapSyncParams:
        return value
