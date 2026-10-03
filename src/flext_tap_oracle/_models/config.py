"""flext-tap-oracle config models — typed business-rule shapes.

Frozen Pydantic shapes for the ``config/tap_oracle.yaml`` business-rule SSOT.
The ``_config.py`` facade validates the model-less YAML slice into these
classes and exposes the ready objects under ``config.TapOracle``.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from pydantic import BaseModel, ConfigDict, Field


class FlextTapOracleConfigModels:
    """Namespace of typed flext-tap-oracle config models."""

    class Connection(BaseModel):
        """Default Oracle connection scalars."""

        model_config = ConfigDict(frozen=True, extra="forbid")

        oracle_host: str = Field(description="Default Oracle host.")
        oracle_port: int = Field(
            ge=1, le=65535, description="Default Oracle listener port."
        )
        oracle_service_name: str = Field(description="Default Oracle service/SID.")
        oracle_user: str = Field(description="Default Oracle username.")
        oracle_password: str = Field(description="Default Oracle password.")

    class Extraction(BaseModel):
        """Tap extraction defaults."""

        model_config = ConfigDict(frozen=True, extra="forbid")

        batch_size: int = Field(ge=1, description="Default rows per extraction batch.")
        stream_prefix: str = Field(description="Default Singer stream name prefix.")
        test_query: str = Field(
            description="Lightweight query used to verify connectivity."
        )
        initial_record_count: int = Field(
            description="Initial record count before extraction starts."
        )

    class Replication(BaseModel):
        """Supported replication methods."""

        model_config = ConfigDict(frozen=True, extra="forbid")

        full_table: str = Field(description="Full-table replication method name.")
        incremental: str = Field(description="Incremental replication method name.")
        log_based: str = Field(description="Log-based replication method name.")

    class Defaults(BaseModel):
        """Miscellaneous tap defaults."""

        model_config = ConfigDict(frozen=True, extra="forbid")

        operation_name: str = Field(
            description="Default operation name for unclassified records."
        )
        max_identifier_length: int = Field(
            ge=1, description="Maximum Oracle identifier length."
        )

    class TapOracle(BaseModel):
        """Root tap-oracle business-rule namespace."""

        model_config = ConfigDict(frozen=True, extra="forbid")

        connection: FlextTapOracleConfigModels.Connection = Field(
            description="Default Oracle connection scalars."
        )
        extraction: FlextTapOracleConfigModels.Extraction = Field(
            description="Tap extraction defaults."
        )
        replication: FlextTapOracleConfigModels.Replication = Field(
            description="Supported replication methods."
        )
        defaults: FlextTapOracleConfigModels.Defaults = Field(
            description="Miscellaneous tap defaults."
        )

    class Root(BaseModel):
        """Root flext-tap-oracle config validated from ``config/*.yaml``."""

        model_config = ConfigDict(frozen=True, extra="ignore")

        TapOracle: FlextTapOracleConfigModels.TapOracle = Field(
            description="Tap-oracle business-rule config namespace."
        )


__all__: list[str] = ["FlextTapOracleConfigModels"]
