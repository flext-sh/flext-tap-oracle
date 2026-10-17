"""FlextTapOracleConfig — frozen config singleton for flext-tap-oracle (ADR-005 §7).

Model-less: business rules live in ``config/*.yaml`` under the ``TapOracle:`` key and
are exposed through the open ``config.TapOracle`` namespace (``extra="allow"``), with
no per-domain model. Access is ``config.TapOracle.<domain>[<key>...]``.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT

"""

from __future__ import annotations

from typing import Annotated

from flext_meltano import FlextMeltanoConfig, m
from flext_meltano.models import FlextMeltanoModelsConfig


class FlextTapOracleConfig(FlextMeltanoConfig):
    """TapOracle config auto-loaded model-less from ``config/*.yaml``.

    MRO carries ``FlextSettings`` FIRST (ENFORCE-042); the class stays a frozen,
    YAML-validated config singleton.
    """

    TapOracle: Annotated[
        FlextMeltanoModelsConfig.MeltanoNamespace,
        m.Field(
            description=(
                "Open namespace exposing ``config/*.yaml`` under ``TapOracle``."
            ),
        ),
    ] = FlextMeltanoModelsConfig.MeltanoNamespace()


config: FlextTapOracleConfig = FlextTapOracleConfig.fetch_global()
"""Pre-instantiated frozen config — ``from flext_tap_oracle import config``."""

__all__: list[str] = ["FlextTapOracleConfig", "config"]
