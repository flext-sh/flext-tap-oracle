"""FLEXT Tap Oracle settings — connection reused from ``settings.DbOracle``.

Oracle connection scalars are the SSOT of ``flext-db-oracle`` and are inherited
via MRO as ``settings.DbOracle.*``. This module declares ONLY tap-specific knobs
under ``settings.TapOracle.*``.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from typing import TYPE_CHECKING, Annotated

from flext_db_oracle import FlextDbOracleSettings
from flext_meltano import FlextMeltanoSettings, m


class FlextTapOracleSettings(FlextDbOracleSettings, FlextMeltanoSettings):
    """Oracle tap settings; connection via ``DbOracle.*``, knobs via ``TapOracle.*``."""

    model_config = m.SettingsConfigDict(
        env_prefix="FLEXT_TAP_ORACLE_",
        env_nested_delimiter="__",
        extra="ignore",
    )

    class _TapOracle(m.BaseModel):
        """Tap-specific knobs only (Oracle connection lives in ``DbOracle``)."""

        batch_size: Annotated[
            int,
            m.Field(default=1000, ge=1, description="Extraction batch size"),
        ]
        stream_prefix: Annotated[
            str,
            m.Field(default="", description="Singer stream name prefix"),
        ]

    if TYPE_CHECKING:
        TapOracle: _TapOracle
    else:
        TapOracle: _TapOracle = m.Field(
            default_factory=_TapOracle,
            description="Namespaced Oracle tap settings.",
        )


settings: FlextTapOracleSettings = FlextTapOracleSettings.fetch_global()
"""Pre-instantiated settings singleton — ``from flext_tap_oracle import settings``."""

__all__: list[str] = ["FlextTapOracleSettings", "settings"]
