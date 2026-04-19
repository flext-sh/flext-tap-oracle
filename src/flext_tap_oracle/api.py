"""FLEXT service orchestrator for tap-oracle.

Thin facade — all infrastructure from ``FlextMeltanoTapServiceBase`` via MRO.
The tap uses FlextMeltanoAbstractions (CLI dispatch), not singer_sdk.Tap.
``create_tap_instance`` returns ``r[T].fail()`` — use CLI dispatch instead.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from typing import Annotated, Never, override

from flext_core import u
from flext_meltano import FlextMeltanoTapServiceBase
from flext_tap_oracle import FlextTapOracleSettings, t


class FlextTapOracleService(FlextMeltanoTapServiceBase):
    """Orchestrator for tap-oracle. CLI dispatch, not Singer SDK."""

    tap_name: Annotated[
        t.NonEmptyStr,
        u.Field(description="Canonical Singer tap identifier."),
    ] = "tap-oracle"

    def __init__(
        self,
        settings: FlextTapOracleSettings | t.RecursiveContainerMapping | None = None,
    ) -> None:
        """Expose the canonical settings bootstrap on the concrete tap facade."""
        super().__init__(settings=settings)

    @override
    def create_tap_instance(
        self,
        settings: t.RecursiveContainerMapping | None = None,
    ) -> Never:
        """Not supported — use CLI dispatch via FlextTapOracleCli."""
        msg = "tap-oracle uses CLI dispatch, not singer_sdk.Tap"
        raise TypeError(msg)


tap_oracle = FlextTapOracleService

__all__: list[str] = ["FlextTapOracleService", "tap_oracle"]
