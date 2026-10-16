"""Singer Oracle tap protocols for FLEXT ecosystem.

Only ``TapOracle.Tap`` (consumed by ``streams.py``) and
``TapOracle.CommandRunner`` (consumed by ``tap.py``) are published here; the
contracts themselves live in the ``_protocols`` family parts.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT

"""

from __future__ import annotations

from flext_db_oracle import FlextDbOracleProtocols
from flext_meltano import FlextMeltanoProtocols

from flext_tap_oracle._protocols.base import FlextTapOracleProtocolsBase


class FlextTapOracleProtocols(FlextMeltanoProtocols, FlextDbOracleProtocols):
    """Singer Oracle tap protocols facade — composes Meltano + Oracle protocols."""

    class TapOracle:
        """Singer Tap Oracle structural protocols (consumer surface)."""

        CommandRunner = FlextTapOracleProtocolsBase.CommandRunner
        Tap = FlextTapOracleProtocolsBase.Tap


p = FlextTapOracleProtocols
__all__: list[str] = ["FlextTapOracleProtocols", "p"]
