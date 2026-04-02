"""FLEXT service orchestrator for tap-oracle.

Thin facade — all infrastructure from ``FlextMeltanoTapServiceBase`` via MRO.
The tap uses FlextMeltanoAbstractions (CLI dispatch), not singer_sdk.Tap.
``create_tap_instance`` returns ``r[T].fail()`` — use CLI dispatch instead.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from typing import Never, override

from flext_meltano import FlextMeltanoTapServiceBase

from flext_tap_oracle import t


class FlextTapOracleService(FlextMeltanoTapServiceBase):
    """Orchestrator for tap-oracle. CLI dispatch, not Singer SDK."""

    tap_name: t.NonEmptyStr = "tap-oracle"

    @override
    def create_tap_instance(
        self,
        config: t.ContainerMapping | None = None,
    ) -> Never:
        """Not supported — use CLI dispatch via FlextTapOracleCli."""
        msg = "tap-oracle uses CLI dispatch, not singer_sdk.Tap"
        raise TypeError(msg)


__all__ = ["FlextTapOracleService"]
