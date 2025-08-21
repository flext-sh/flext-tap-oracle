"""Oracle Tap Configuration - Comprehensive Configuration Management.

PEP8 CONSOLIDATION: All Oracle tap configuration logic consolidated into one module.
This module consolidates config.py + relevant parts of models.py following the
established FLEXT pattern for comprehensive configuration management.

COMPOSIÇÃO SEM DUPLICAÇÃO using flext-core, flext-db-oracle, and flext-meltano.

Copyright (c) 2025 FLEXT Contributors
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

import re
from typing import Literal, Self

from flext_core import (
    FlextBaseConfigModel,
    FlextConstants,
    FlextResult,
    FlextValueObject,
)
from flext_db_oracle import FlextDbOracleConfig
from pydantic import Field, field_validator, model_validator


class FlextOracleTapConfiguration(FlextValueObject):
    """Oracle tap configuration - ONLY tap-specific settings.

    Complementa FlextDbOracleConfig com configurações específicas do tap.
    """

    # Singer tap specific settings - USE FlextConstants defaults
    batch_size: int = Field(
        default=FlextConstants.Performance.DEFAULT_BATCH_SIZE,
        ge=1,
        le=FlextConstants.Performance.MAX_BATCH_SIZE,
        description="Batch size for data extraction",
    )

    max_parallel_streams: int = Field(
        default=1,  # Oracle-specific default (conservative for database connections)
        ge=1,
        le=FlextConstants.Limits.MAX_THREADS,
        description="Maximum parallel stream processing",
    )

    stream_prefix: str = Field(
        default="oracle",  # Oracle-specific prefix (not duplicating general constants)
        description="Prefix for Singer stream names",
    )

    tables_filter: list[str] | None = Field(
        default=None,
        description="Tables to include (None = all tables)",
    )

    exclude_tables: list[str] | None = Field(
        default=None,
        description="Tables to exclude",
    )

    @model_validator(mode="after")
    def validate_configuration_consistency(self) -> Self:
        """Validate tap configuration consistency - Python 3.13 enhanced validators."""
        # Check for conflicting table filters
        if (
            self.tables_filter
            and self.exclude_tables
            and set(self.tables_filter) & set(self.exclude_tables)
        ):
            conflicting = set(self.tables_filter) & set(self.exclude_tables)
            msg = f"Tables cannot be both included and excluded: {conflicting}"
            raise ValueError(msg)

        # Advanced batch size validation based on parallel streams
        max_load = FlextConstants.Performance.MAX_BATCH_SIZE * 50  # Conservative limit
        total_load = self.batch_size * self.max_parallel_streams
        if total_load > max_load:
            msg = (
                f"Total batch load too high: "
                f"{self.batch_size} x {self.max_parallel_streams} = "
                f"{total_load} > {max_load:,}"
            )
            raise ValueError(msg)

        # Validate table name patterns (Oracle specific)
        if self.tables_filter:
            for table_name in self.tables_filter:
                if not self._is_valid_oracle_table_name(table_name):
                    msg = f"Invalid Oracle table name pattern: {table_name}"
                    raise ValueError(msg)

        return self

    @staticmethod
    def _is_valid_oracle_table_name(name: str) -> bool:
        """Validate Oracle table name pattern - Python 3.13 enhanced."""
        max_length = FlextConstants.Limits.MAX_STRING_LENGTH
        if not name or len(name) > max_length:
            return False

        # Oracle table names: start with letter, contain letters/digits/underscore/dollar/hash
        if not name[0].isalpha():
            return False

        return all(c.isalnum() or c in "_$#" for c in name)

    def validate_business_rules(self) -> FlextResult[None]:
        """Validate tap configuration business rules - backward compatibility."""
        # Kept for backward compatibility, main validation moved to model_validator
        return FlextResult[None].ok(None)


class FlextOracleTapStreamMetadata(FlextValueObject):
    """Oracle tap stream metadata - ONLY tap-specific fields.

    Extends Oracle table metadata with tap-specific information.
    """

    # Tap-specific metadata (não duplica FlextDbOracleTable)
    stream_name: str = Field(..., description="Singer stream name")
    replication_method: Literal["FULL_TABLE", "INCREMENTAL"] = Field(
        default="FULL_TABLE",
        description="Replication method for this stream",
    )
    replication_key: str | None = Field(
        default=None,
        description="Column used for incremental replication",
    )
    is_selected: bool = Field(
        default=True,
        description="Whether stream is selected for extraction",
    )

    @field_validator("stream_name")
    @classmethod
    def validate_stream_name(cls, v: str) -> str:
        """Validate stream name follows Singer conventions - Python 3.13 enhanced."""
        if not v or not v.strip():
            msg = "Stream name cannot be empty"
            raise ValueError(msg)

        # Enhanced validation with Python 3.13 string methods
        max_length = FlextConstants.Limits.MAX_STRING_LENGTH
        if len(v) > max_length:
            msg = f"Stream name too long: {len(v)} > {max_length} characters"
            raise ValueError(msg)

        if v.startswith(("_", "-")) or v.endswith(("_", "-")):
            msg = "Stream name cannot start/end with underscore or dash"
            raise ValueError(msg)

        # Remove invalid characters for Singer streams using Python 3.13 enhanced string processing
        cleaned = "".join(c if c.isalnum() or c in "_-" else "_" for c in v)
        return cleaned.lower()

    @model_validator(mode="after")
    def validate_replication_consistency(self) -> Self:
        """Validate replication configuration consistency - Python 3.13 Self typing."""
        if self.replication_method == "INCREMENTAL":
            if not self.replication_key:
                msg = "Incremental replication requires a replication_key"
                raise ValueError(msg)

            # Advanced validation: check if replication key is reasonable
            max_key_length = FlextConstants.Limits.MAX_STRING_LENGTH
            if len(self.replication_key) > max_key_length:
                msg = f"Replication key too long: {len(self.replication_key)} > {max_key_length}"
                raise ValueError(msg)

        elif self.replication_method == "FULL_TABLE" and self.replication_key:
            msg = "Full table replication should not have replication_key"
            raise ValueError(msg)

        return self

    def validate_business_rules(self) -> FlextResult[None]:
        """Validate tap-specific business rules - Python 3.13 enhanced."""
        # This method is kept for backward compatibility but
        # most validation moved to model_validator for better Pydantic integration
        return FlextResult[None].ok(None)


class FlextOracleTapConfig(FlextBaseConfigModel):
    """Oracle Tap Configuration usando COMPOSIÇÃO das bases existentes.

    Esta classe COMPÕE funcionalidade das bases existentes:
    - FlextBaseConfigModel: Configuração base modernizada do flext-core
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

    def validate_business_rules(self) -> FlextResult[None]:
        """Validate Oracle tap configuration business rules using FlextBaseConfigModel pattern."""
        # Validate Oracle configuration
        oracle_validation = self._validate_oracle_config()
        if not oracle_validation.success:
            return oracle_validation

        # Validate tap-specific configuration
        tap_validation = self.tap_config.validate_business_rules()
        if not tap_validation.success:
            return tap_validation

        # Cross-validate configurations
        cross_validation = self._validate_cross_configuration()
        if not cross_validation.success:
            return cross_validation

        return FlextResult[None].ok(None)

    def _validate_oracle_config(self) -> FlextResult[None]:
        """Validate Oracle configuration."""
        if not self.oracle_config:
            return FlextResult[None].fail("Oracle database configuration is required")

        try:
            connection_string = self.oracle_config.get_connection_string()
            if not connection_string:
                return FlextResult[None].fail(
                    "Oracle connection string cannot be generated"
                )
        except Exception as e:
            return FlextResult[None].fail(
                f"Oracle configuration validation failed: {e}"
            )

        return FlextResult[None].ok(None)

    def _validate_cross_configuration(self) -> FlextResult[None]:
        """Validate cross-configuration compatibility."""
        # Cross-validate Oracle and tap configurations
        if hasattr(self.oracle_config, "pool_max"):
            max_connections = getattr(self.oracle_config, "pool_max", 10)
            if self.tap_config.max_parallel_streams > max_connections:
                return FlextResult[None].fail(
                    f"Parallel streams ({self.tap_config.max_parallel_streams}) exceeds "
                    f"Oracle connection pool limit ({max_connections})",
                )

        # Validate batch size against Oracle limits
        if self.tap_config.batch_size > FlextConstants.Performance.MAX_BATCH_SIZE:
            return FlextResult[None].fail(
                f"Batch size too large for Oracle: {self.tap_config.batch_size} > "
                f"{FlextConstants.Performance.MAX_BATCH_SIZE:,} (may cause memory issues)",
            )

        return FlextResult[None].ok(None)

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


# Factory function for easy creation using configuration objects pattern
def create_oracle_tap_config(
    oracle_params: dict[str, object],
    tap_params: dict[str, object] | None = None,
    meltano_params: dict[str, object] | None = None,
) -> FlextResult[FlextOracleTapConfig]:
    """Create Oracle tap configuration using grouped parameters.

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
            "batch_size",
            FlextConstants.Performance.DEFAULT_BATCH_SIZE,
        )
        tap_config.setdefault("stream_prefix", "oracle")
        meltano_config.setdefault("project_root", ".")
        meltano_config.setdefault(
            "environment",
            FlextConstants.Configuration.DEFAULT_ENVIRONMENT,
        )

        config_data = {
            "oracle_config": oracle_params,
            "tap_config": tap_config,
            **meltano_config,
        }

        config_instance = FlextOracleTapConfig.model_validate(config_data)
        return FlextResult[None].ok(config_instance)

    except Exception as e:
        return FlextResult[None].fail(f"Oracle tap configuration creation failed: {e}")


# Backward compatibility aliases
TapOracleConfig = FlextOracleTapConfig
Config = FlextOracleTapConfig

__all__: list[str] = [
    "Config",  # Legacy alias
    "FlextOracleTapConfig",
    "FlextOracleTapConfiguration",
    "FlextOracleTapStreamMetadata",
    "TapOracleConfig",  # Legacy alias
    "create_oracle_tap_config",
]
