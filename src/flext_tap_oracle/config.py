"""Oracle Tap Configuration - COMPOSIÇÃO SEM DUPLICAÇÃO.

Este módulo implementa configuração do Oracle Tap usando COMPOSIÇÃO das
configurações existentes do flext-core, flext-meltano e flext-db-oracle.

PRINCÍPIO: COMPOR, não duplicar. Usar o que já existe.

Copyright (c) 2025 FLEXT Contributors
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

import re
from typing import Self

# Import base configs - NEVER duplicate functionality
# Import from flext-core SINGLE SOURCE - NO duplications
from flext_core import FlextConstants, FlextResult
from flext_db_oracle import FlextDbOracleConfig
from flext_meltano import FlextMeltanoConfig
from pydantic import Field, field_validator, model_validator

from flext_tap_oracle.models import FlextOracleTapConfiguration


class FlextOracleTapConfig(FlextMeltanoConfig):
    """Oracle Tap Configuration usando COMPOSIÇÃO das bases existentes.

    Esta classe COMPÕE funcionalidade das bases existentes:
    - FlextMeltanoConfig: Configuração base para taps Singer
    - FlextDbOracleConfig: Configuração Oracle database (via composition)
    - FlextOracleTapConfiguration: Configurações específicas do tap

    NUNCA duplica funcionalidade existente.
    """

    # Composition: Oracle database configuration
    oracle_config: FlextDbOracleConfig = Field(
        ...,
        description="Oracle database configuration from flext-db-oracle",
    )

    # Composition: Tap-specific configuration
    tap_config: FlextOracleTapConfiguration = Field(
        default_factory=FlextOracleTapConfiguration,
        description="Tap-specific configuration",
    )

    @field_validator("oracle_config", mode="before")
    @classmethod
    def validate_oracle_config(cls, v: object) -> FlextDbOracleConfig:
        """Validate Oracle configuration using existing validation."""
        if isinstance(v, dict):
            return FlextDbOracleConfig.model_validate(v)
        if isinstance(v, FlextDbOracleConfig):
            return v
        msg = "oracle_config must be dict or FlextDbOracleConfig"
        raise ValueError(msg)

    @model_validator(mode="after")
    def validate_tap_oracle_integration(self) -> Self:
        """Validate integration between Oracle and tap configurations - Python 3.13 enhanced."""
        # Enhanced validation for Oracle-tap compatibility
        max_tables = FlextConstants.Limits.MAX_LIST_SIZE
        if (
            self.tap_config.tables_filter
            and len(self.tap_config.tables_filter) > max_tables
        ):
            msg = (
                f"Too many tables specified: {len(self.tap_config.tables_filter)} > {max_tables:,} "
                f"(Oracle performance limit)"
            )
            raise ValueError(msg)

        # Validate Oracle connection limits vs tap parallelism
        if hasattr(self.oracle_config, "pool_max"):
            max_connections = getattr(self.oracle_config, "pool_max", 10)
            if self.tap_config.max_parallel_streams > max_connections:
                msg = (
                    f"Parallel streams ({self.tap_config.max_parallel_streams}) exceeds "
                    f"Oracle connection pool limit ({max_connections})"
                )
                raise ValueError(msg)

        # Advanced validation: batch size vs Oracle characteristics
        max_batch = FlextConstants.Performance.MAX_BATCH_SIZE
        if self.tap_config.batch_size > max_batch:
            msg = (
                f"Batch size too large for Oracle: {self.tap_config.batch_size} > {max_batch:,} "
                f"(may cause memory issues)"
            )
            raise ValueError(msg)

        # Cross-validate stream prefix with Oracle naming conventions
        if not self._is_valid_oracle_prefix(self.tap_config.stream_prefix):
            msg = f"Invalid Oracle-compatible stream prefix: {self.tap_config.stream_prefix}"
            raise ValueError(msg)

        return self

    @staticmethod
    def _is_valid_oracle_prefix(prefix: str) -> bool:
        """Validate stream prefix follows Oracle naming conventions - Python 3.13."""
        max_length = FlextConstants.Limits.MAX_STRING_LENGTH
        if not prefix or len(prefix) > max_length:
            return False

        # Oracle identifiers: start with letter, contain letters/digits/underscore - use flext-core pattern
        return bool(re.match(FlextConstants.Patterns.IDENTIFIER_PATTERN, prefix))

    @property
    def connection_string(self) -> str:
        """Get Oracle connection string from composed config."""
        return self.oracle_config.get_connection_string()

    @property
    def stream_prefix(self) -> str:
        """Get stream prefix for Singer streams."""
        return self.tap_config.stream_prefix

    @property
    def batch_size(self) -> int:
        """Get batch size for data extraction."""
        return self.tap_config.batch_size

    def get_oracle_config(self) -> FlextDbOracleConfig:
        """Get Oracle database configuration.

        Returns:
            FlextDbOracleConfig for use with flext-db-oracle components

        """
        return self.oracle_config

    def get_tap_config(self) -> FlextOracleTapConfiguration:
        """Get tap-specific configuration.

        Returns:
            FlextOracleTapConfiguration for tap operations

        """
        return self.tap_config


# Base FlextModel.from_dict method handles validation correctly


# Factory function for easy creation using configuration objects pattern
def create_oracle_tap_config(
    oracle_params: dict[str, object],
    tap_params: dict[str, object] | None = None,
    meltano_params: dict[str, object] | None = None,
) -> FlextResult[FlextOracleTapConfig]:
    """Factory function to create Oracle tap configuration using grouped parameters.

    Args:
        oracle_params: Oracle database connection parameters (host, port, username, password, etc.)
        tap_params: Optional tap-specific parameters (batch_size, stream_prefix, etc.)
        meltano_params: Optional Meltano parameters (project_root, environment, etc.)

    Returns:
        FlextResult containing validated Oracle tap configuration

    """
    try:
        # Apply defaults
        tap_config = tap_params or {}
        meltano_config = meltano_params or {}

        # Set default values using semantic constants
        tap_config.setdefault(
            "batch_size", FlextConstants.Performance.DEFAULT_BATCH_SIZE
        )
        tap_config.setdefault("stream_prefix", "oracle")
        meltano_config.setdefault("project_root", ".")
        meltano_config.setdefault(
            "environment", FlextConstants.Configuration.DEFAULT_ENVIRONMENT
        )

        config_data = {
            "oracle_config": oracle_params,
            "tap_config": tap_config,
            **meltano_config,
        }

        config_instance = FlextOracleTapConfig.model_validate(config_data)
        return FlextResult.ok(config_instance)

    except Exception as e:
        return FlextResult.fail(f"Oracle tap configuration creation failed: {e}")


# Backward compatibility aliases
TapOracleConfig = FlextOracleTapConfig
Config = FlextOracleTapConfig

__all__: list[str] = [
    "Config",  # Legacy alias
    "FlextOracleTapConfig",
    "TapOracleConfig",  # Legacy alias
    "create_oracle_tap_config",
]
