"""FlextTapOracleConfig — frozen config singleton for flext-tap-oracle (ADR-005 §7).

Model-less: business rules live in ``config/*.yaml`` under the ``TapOracle:`` key and
are exposed through the open ``config.TapOracle`` namespace (``extra="allow"``), with
no per-domain model. Access is ``config.TapOracle.<domain>[<key>...]``.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from pydantic import BaseModel, ConfigDict

from flext_meltano import FlextMeltanoConfig


class _TapOracleNamespace(BaseModel):
    """Open, frozen namespace exposing every ``config/*.yaml`` domain model-less."""

    model_config = ConfigDict(extra="allow", frozen=True)


class FlextTapOracleConfig(FlextMeltanoConfig):
    """TapOracle config auto-loaded model-less from ``config/*.yaml``."""

    TapOracle: _TapOracleNamespace = _TapOracleNamespace()


config: FlextTapOracleConfig = FlextTapOracleConfig.fetch_global()
"""Pre-instantiated frozen config singleton — ``from flext_tap_oracle import config``."""

__all__: list[str] = ["FlextTapOracleConfig", "config"]
