# AUTO-GENERATED FILE — Regenerate with: make gen
"""Static instance-to-protocol evidence required by candidate admission.

Copyright (c) 2026 FLEXT Team. All rights reserved.
src/flext_tap_oracle/_protocols/model_conformance
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from flext_tap_oracle import FlextTapOracleModels, FlextTapOracleProtocols

    def model_protocol_1(
        value: (FlextTapOracleModels.TapOracle.ConfigNamespace),
    ) -> FlextTapOracleProtocols.TapOracle.ConfigNamespace:
        return value

    def model_protocol_2(
        value: (FlextTapOracleModels.TapOracle.OracleTapDiscoverParams),
    ) -> FlextTapOracleProtocols.TapOracle.OracleTapDiscoverParams:
        return value

    def model_protocol_3(
        value: (FlextTapOracleModels.TapOracle.OracleTapSyncParams),
    ) -> FlextTapOracleProtocols.TapOracle.OracleTapSyncParams:
        return value
