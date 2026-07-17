"""Singer Oracle tap protocols for FLEXT ecosystem.

Of the 9 inner ``TapOracle.*`` Protocol classes that previously lived here, 7
had **zero workspace consumers** (per AGENTS.md §3.5 + STRICT YAGNI they
were deleted). Only ``TapOracle.Tap`` (consumed by ``streams.py``) and
``TapOracle.CommandRunner`` (consumed by ``tap.py``) remain.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from typing import TYPE_CHECKING, Protocol, runtime_checkable

from flext_db_oracle import FlextDbOracleProtocols
from flext_meltano import FlextMeltanoProtocols, p as meltano_p
from flext_tap_oracle import p

if TYPE_CHECKING:
    from flext_tap_oracle import t


class FlextTapOracleProtocols(FlextMeltanoProtocols, FlextDbOracleProtocols):
    """Singer Oracle tap protocols facade — composes Meltano + Oracle protocols."""

    class TapOracle:
        """Singer Tap Oracle structural protocols (consumer surface)."""

        @runtime_checkable
        class CommandRunner(Protocol):
            """Structural protocol for Oracle tap command execution."""

            def execute(self) -> meltano_p.Result[t.JsonMapping]:
                """Execute the Oracle tap command and return results."""
                ...

        @runtime_checkable
        class Tap(Protocol):
            """Structural protocol for Oracle tap value used in stream context."""

            typed_config: t.JsonValue


p = FlextTapOracleProtocols
__all__: list[str] = ["FlextTapOracleProtocols", "p"]
