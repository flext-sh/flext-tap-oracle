# AUTO-GENERATED FILE — Regenerate with: make gen
"""Source-derived structural model contracts.

Copyright (c) 2026 FLEXT Team. All rights reserved.
src/flext_tap_oracle/_protocols/params
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from collections.abc import Sequence
from typing import TYPE_CHECKING, Protocol, runtime_checkable

from flext_meltano import FlextMeltanoProtocols

if TYPE_CHECKING:
    from flext_core import p


class FlextTapOracleProtocolsParams:
    """Own the structural contracts declared by its model source."""

    @runtime_checkable
    class OracleTapDiscoverParams(FlextMeltanoProtocols.Model, Protocol):
        """Structural data contract projected from the owning model."""

        @property
        def domain_events(self) -> Sequence[p.DomainEvent]:
            """List of uncommitted domain events for event sourcing."""
            ...

        @property
        def config_file(self) -> str | None:
            """Path to configuration file."""
            ...

        @property
        def output_file(self) -> str | None:
            """Path to output file."""
            ...

    @runtime_checkable
    class OracleTapSyncParams(FlextMeltanoProtocols.Model, Protocol):
        """Structural data contract projected from the owning model."""

        @property
        def domain_events(self) -> Sequence[p.DomainEvent]:
            """List of uncommitted domain events for event sourcing."""
            ...

        @property
        def config_file(self) -> str | None:
            """Path to configuration file."""
            ...

        @property
        def catalog_file(self) -> str | None:
            """Path to catalog file."""
            ...

        @property
        def state_file(self) -> str | None:
            """Path to state file."""
            ...


__all__: list[str] = [
    "FlextTapOracleProtocolsParams",
]
