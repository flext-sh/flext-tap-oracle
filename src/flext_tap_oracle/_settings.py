"""FLEXT Tap Oracle settings — namespaced under ``settings.TapOracle``.

Universal fields via MRO; project fields in the ``TapOracle`` group with simple
scalar types (env-settable). Oracle connection objects are built by consumers
from these scalars, not stored as complex settings fields.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from typing import TYPE_CHECKING, Annotated

from pydantic_settings import SettingsConfigDict

from flext_meltano import FlextMeltanoSettings, m


class FlextTapOracleSettings(FlextMeltanoSettings):
    """Oracle Singer tap settings; fields under ``settings.TapOracle.*``."""

    model_config = SettingsConfigDict(
        env_prefix="FLEXT_TAP_ORACLE_", env_nested_delimiter="__", extra="ignore"
    )

    class _TapOracle(m.BaseModel):
        """Namespaced Oracle tap settings."""

        oracle_host: Annotated[
            str, m.Field(default="localhost", description="Oracle host")
        ]
        oracle_port: Annotated[
            int, m.Field(default=1521, ge=1, le=65535, description="Oracle port")
        ]
        oracle_service_name: Annotated[
            str, m.Field(default="XEPDB1", description="Oracle service/SID")
        ]
        oracle_user: Annotated[str, m.Field(default="", description="Oracle username")]
        oracle_password: Annotated[
            str, m.Field(default="", description="Oracle password")
        ]
        batch_size: Annotated[
            int, m.Field(default=1000, ge=1, description="Extraction batch size")
        ]
        stream_prefix: Annotated[
            str, m.Field(default="", description="Singer stream name prefix")
        ]

    if TYPE_CHECKING:
        TapOracle: _TapOracle
    else:
        TapOracle: _TapOracle = m.Field(
            default_factory=_TapOracle, description="Namespaced Oracle tap settings."
        )


settings: FlextTapOracleSettings = FlextTapOracleSettings.fetch_global()
"""Pre-instantiated project settings singleton — ``from flext_tap_oracle import settings``."""

__all__: list[str] = ["FlextTapOracleSettings", "settings"]
