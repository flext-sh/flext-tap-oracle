"""Singer Oracle tap protocol contracts.

Of the 9 inner ``TapOracle.*`` Protocol classes that previously lived in the
facade, 7 had **zero workspace consumers** (per AGENTS.md §3.5 + STRICT YAGNI
they were deleted). Only ``TapOracle.Tap`` (consumed by ``streams.py``) and
``TapOracle.CommandRunner`` (consumed by ``tap.py``) remain.

Copyright (c) 2026 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from typing import TYPE_CHECKING, Protocol, runtime_checkable

from flext_meltano import FlextMeltanoProtocols

if TYPE_CHECKING:
    from flext_tap_oracle import t


class FlextTapOracleProtocolsBase:
    """Singer Tap Oracle structural protocol contracts for ``p.TapOracle``."""

    @runtime_checkable
    class CommandRunner(Protocol):
        """Structural protocol for Oracle tap command execution."""

        def execute(self) -> FlextMeltanoProtocols.Result[t.JsonMapping]:
            """Execute the Oracle tap command and return results."""
            ...

    @runtime_checkable
    class Tap(Protocol):
        """Structural protocol for Oracle tap value used in stream context."""

        typed_config: t.JsonValue


__all__: list[str] = [
    "CommandRunner",
    "FlextTapOracleProtocolsBase",
    "Tap",
]
