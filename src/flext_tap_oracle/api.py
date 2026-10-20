"""FLEXT service orchestrator for tap-oracle.

Thin facade — all infrastructure from ``FlextMeltanoTapServiceBase`` via MRO.
The tap uses FlextMeltanoAbstractions (CLI dispatch), not singer_sdk.Tap.
``create_tap_instance`` is unsupported and raises ``TypeError`` — use CLI
dispatch instead.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT

"""

from __future__ import annotations

from typing import Annotated, Never, override

from flext_meltano.services.consumer_bases.tap_service_base import (
    FlextMeltanoTapServiceBase,
)

from flext_tap_oracle import FlextTapOracleSettings, m, p, t


class FlextTapOracleService(FlextMeltanoTapServiceBase):
    """Orchestrator for tap-oracle. CLI dispatch, not Singer SDK."""

    tap_name: Annotated[
        t.NonEmptyStr,
        m.Field(description="Canonical Singer tap identifier."),
    ] = "tap-oracle"

    def __init__(self, settings: FlextTapOracleSettings | None = None) -> None:
        """Expose the canonical settings bootstrap on the concrete tap facade.

        Args:
            settings: Optional concrete settings passed through to the service
                base bootstrap.

        """
        super().__init__(settings=settings)

    @override
    def create_tap_instance(
        self,
        _settings: p.Settings | t.JsonMapping | None = None,
    ) -> Never:
        """Not supported — use CLI dispatch via FlextTapOracleCli.

        Raises:
            TypeError: If tap-oracle uses CLI dispatch, not singer_sdk.Tap.

        """
        msg = "tap-oracle uses CLI dispatch, not singer_sdk.Tap"
        raise TypeError(msg)


tap_oracle: FlextTapOracleService = FlextTapOracleService.fetch_global()
"""Process-wide tap-oracle facade singleton resolved from the global container."""

__all__: list[str] = ["FlextTapOracleService", "tap_oracle"]
