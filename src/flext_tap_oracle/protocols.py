# AUTO-GENERATED FILE — Regenerate with: make gen
"""Singer Oracle tap protocols for FLEXT ecosystem.

Only ``TapOracle.Tap`` (consumed by ``streams.py``) and
``TapOracle.CommandRunner`` (consumed by ``tap.py``) are published here; the
contracts themselves live in the ``_protocols`` family parts.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT

"""

from __future__ import annotations

from flext_db_oracle import p as flext_db_oracle_p
from flext_meltano import p as flext_meltano_p

from flext_tap_oracle._protocols import FlextTapOracleProtocolsBase


class FlextTapOracleProtocols(flext_meltano_p, flext_db_oracle_p):
    """Singer Oracle tap protocols facade — composes Meltano + Oracle protocols."""

    class TapOracle(FlextTapOracleProtocolsBase):
        """Singer Tap Oracle structural protocols (consumer surface)."""


p = FlextTapOracleProtocols
__all__: list[str] = ["FlextTapOracleProtocols", "p"]
