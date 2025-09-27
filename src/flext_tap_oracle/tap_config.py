"""Oracle Tap Configuration - Comprehensive Configuration Management.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT.
"""

from __future__ import annotations

import re
from typing import Self

from pydantic import Field, SecretStr, field_validator, model_validator
from pydantic_settings import SettingsConfigDict

from flext_core import (
    FlextConfig,
    FlextConstants,
    FlextResult,
)
from flext_db_oracle import FlextDbOracleModels
from flext_tap_oracle.typings import FlextTapOracleTypes


class FlextOracleTapConfiguration(FlextConfig):
    """Oracle tap configuration - ONLY tap-specific settings.

    Complementa FlextDbOracleModels.OracleConfig com configurações específicas do tap.
    """

    # Singer tap specific settings - USE FlextConstants defaults
    batch_size: int = Field(
        default=FlextConstants.Performance.DEFAULT_BATCH_SIZE,
        ge=1,
        le=FlextConstants.Performance.MAX_BATCH_SIZE_VALIDATION,
        description="Batch size for data extraction",
    )

    max_parallel_streams: int = Field(
        default=1,  # Oracle-specific default (conservative for database connections)
        ge=1,
        le=10,  # Reasonable max for Oracle connections
        description="Maximum parallel stream processing",
    )

    stream_prefix: str = Field(
        default="oracle",  # Oracle-specific prefix (not duplicating general constants)
        description="Prefix for Singer stream names",
    )

    tables_filter: FlextTapOracleTypes.Core.StringList | None = Field(
        default=None,
        description="Tables to include (None = all tables)",
    )

    exclude_tables: FlextTapOracleTypes.Core.StringList | None = Field(
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
        max_load = (
            FlextConstants.Performance.MAX_BATCH_SIZE_VALIDATION * 50
        )  # Conservative limit
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

    def validate_business_rules(self: object) -> FlextResult[None]:
        """Validate tap configuration business rules - backward compatibility."""
        # Kept for backward compatibility, main validation moved to model_validator
        return FlextResult[None].ok(None)


class FlextTapOracleConfig(FlextConfig):
    """Oracle Tap Configuration extending FlextConfig.

    Follows standardized [Project]Config pattern:
    - Extends FlextConfig from flext-core
    - Uses SecretStr for sensitive data
    - All defaults from FlextConstants
    - Proper Pydantic 2 validation
    - Singleton pattern with proper typing

    Combines Oracle database configuration with tap-specific settings using composition.
    """

    model_config = SettingsConfigDict(
        env_prefix="FLEXT_TAP_ORACLE_",
        case_sensitive=False,
        extra="ignore",
        env_file=".env",
        env_file_encoding="utf-8",
        env_nested_delimiter="__",
        use_enum_values=True,
        validate_assignment=True,
        validate_default=True,
        frozen=False,
        str_strip_whitespace=True,
    )

    # Oracle Database Configuration (using composition)

    oracle_host: str = Field(default="localhost", description="Oracle database host")

    oracle_port: int = Field(
        default=1521, ge=1, le=65535, description="Oracle database port"
    )

    oracle_service_name: str = Field(default="", description="Oracle service name")

    oracle_sid: str = Field(default="", description="Oracle SID")

    oracle_username: str = Field(default="", description="Oracle username")

    oracle_password: SecretStr = Field(
        default_factory=lambda: SecretStr(""), description="Oracle password (sensitive)"
    )

    # Tap-specific Configuration
    stream_prefix: str = Field(
        default="oracle", description="Prefix for Singer stream names"
    )

    batch_size: int = Field(
        default=FlextConstants.Performance.DEFAULT_BATCH_SIZE,
        ge=1,
        le=FlextConstants.Performance.MAX_BATCH_SIZE_VALIDATION,
        description="Batch size for data extraction",
    )

    max_parallel_streams: int = Field(
        default=4,
        ge=1,
        le=FlextConstants.Container.MAX_WORKERS,
        description="Maximum parallel streams for extraction",
    )

    tables_filter: list[str] | None = Field(
        default=None, description="List of table names to extract (None = all tables)"
    )

    schemas_filter: list[str] | None = Field(
        default=None, description="List of schema names to extract (None = all schemas)"
    )

    enable_incremental: bool = Field(
        default=True, description="Enable incremental extraction"
    )

    incremental_column: str = Field(
        default="LAST_MODIFIED", description="Column for incremental extraction"
    )

    # Performance Configuration
    fetch_size: int = Field(
        default=10000, ge=100, le=100000, description="Oracle fetch size for queries"
    )

    query_timeout: int = Field(
        default=FlextConstants.Network.DEFAULT_TIMEOUT,
        ge=1,
        le=3600,
        description="Query timeout in seconds",
    )

    # Pydantic 2 field validators
    @field_validator("stream_prefix")
    @classmethod
    def validate_stream_prefix(cls, v: str) -> str:
        """Validate stream prefix follows Oracle naming conventions."""
        if not v or not v.strip():
            msg = "Stream prefix cannot be empty"
            raise ValueError(msg)

        # Oracle identifiers: start with letter, contain letters/digits/underscore
        if not re.match(r"^[a-zA-Z][a-zA-Z0-9_]*$", v):
            msg = f"Invalid stream prefix: {v}. Must start with letter and contain only letters, digits, and underscores"
            raise ValueError(msg)

        if len(v) > FlextConstants.Limits.MAX_STRING_LENGTH:
            msg = f"Stream prefix too long: {len(v)} > {FlextConstants.Limits.MAX_STRING_LENGTH}"
            raise ValueError(msg)

        return v.lower()

    @field_validator("tables_filter")
    @classmethod
    def validate_tables_filter(cls, v: list[str] | None) -> list[str] | None:
        """Validate tables filter list."""
        if v is None:
            return v

        if len(v) > FlextConstants.Limits.MAX_LIST_SIZE:
            msg = f"Too many tables specified: {len(v)} > {FlextConstants.Limits.MAX_LIST_SIZE}"
            raise ValueError(msg)

        for table in v:
            if not re.match(r"^[a-zA-Z][a-zA-Z0-9_]*$", table):
                msg = f"Invalid table name: {table}"
                raise ValueError(msg)

        return v

    @field_validator("schemas_filter")
    @classmethod
    def validate_schemas_filter(cls, v: list[str] | None) -> list[str] | None:
        """Validate schemas filter list."""
        if v is None:
            return v

        max_schemas = 100  # Reasonable schema limit
        if len(v) > max_schemas:
            msg = f"Too many schemas specified: {len(v)} > {max_schemas}"
            raise ValueError(msg)

        for schema in v:
            if not re.match(r"^[a-zA-Z][a-zA-Z0-9_]*$", schema):
                msg = f"Invalid schema name: {schema}"
                raise ValueError(msg)

        return v

    @model_validator(mode="after")
    def validate_oracle_connection_config(self) -> FlextOracleTapConfig:
        """Validate Oracle connection configuration."""
        # Either service_name or sid must be provided
        if not self.oracle_service_name and not self.oracle_sid:
            msg = "Either oracle_service_name or oracle_sid must be provided"
            raise ValueError(msg)

        # Cannot have both service_name and sid
        if self.oracle_service_name and self.oracle_sid:
            msg = "Cannot specify both oracle_service_name and oracle_sid"
            raise ValueError(msg)

        # Validate parallel streams vs batch size
        max_safe_parallel = 8
        max_safe_batch = 50000
        if (
            self.max_parallel_streams > max_safe_parallel
            and self.batch_size > max_safe_batch
        ):
            msg = "High parallelism with large batch sizes may cause memory issues"
            raise ValueError(msg)

        return self

    # Configuration helper methods
    def get_oracle_config(self) -> FlextDbOracleModels.OracleConfig:
        """Get Oracle configuration for flext-db-oracle integration."""
        return FlextDbOracleModels.OracleConfig(
            host=self.oracle_host,
            port=self.oracle_port,
            service_name=self.oracle_service_name,
            sid=self.oracle_sid,
            username=self.oracle_username,
            password=self.oracle_password.get_secret_value(),
            pool_min=1,
            pool_max=self.max_parallel_streams + 2,  # Extra connections for metadata
            timeout=self.query_timeout,
            domain_events=[],  # Initialize empty domain events list
        )

    def get_tap_config(self) -> dict[str, object]:
        """Get tap-specific configuration dictionary."""
        return {
            "stream_prefix": self.stream_prefix,
            "batch_size": self.batch_size,
            "max_parallel_streams": self.max_parallel_streams,
            "tables_filter": self.tables_filter,
            "schemas_filter": self.schemas_filter,
            "enable_incremental": self.enable_incremental,
            "incremental_column": self.incremental_column,
            "fetch_size": self.fetch_size,
        }

    def get_performance_config(self) -> dict[str, object]:
        """Get performance configuration dictionary."""
        return {
            "batch_size": self.batch_size,
            "max_parallel_streams": self.max_parallel_streams,
            "fetch_size": self.fetch_size,
            "query_timeout": self.query_timeout,
        }

    def get_connection_string(self) -> str:
        """Get Oracle connection string."""
        if self.oracle_service_name:
            return f"{self.oracle_host}:{self.oracle_port}/{self.oracle_service_name}"
        if self.oracle_sid:
            return f"{self.oracle_host}:{self.oracle_port}:{self.oracle_sid}"
        msg = "Cannot generate connection string: neither service_name nor sid provided"
        raise ValueError(msg)

    def validate_business_rules(self) -> FlextResult[None]:
        """Validate Oracle tap configuration business rules."""
        try:
            # Validate Oracle configuration
            if not self.oracle_host:
                return FlextResult[None].fail("Oracle host is required")

            if not self.oracle_username:
                return FlextResult[None].fail("Oracle username is required")

            if not self.oracle_password.get_secret_value():
                return FlextResult[None].fail("Oracle password is required")

            # Validate connection string can be generated
            try:
                self.get_connection_string()
            except ValueError as e:
                return FlextResult[None].fail(
                    f"Connection string validation failed: {e}"
                )

            # Validate performance settings
            max_safe_parallel = 8
            max_safe_batch = 50000
            if (
                self.max_parallel_streams > max_safe_parallel
                and self.batch_size > max_safe_batch
            ):
                return FlextResult[None].fail(
                    "High parallelism with large batch sizes may cause memory issues"
                )

            # Validate filters
            if (
                self.tables_filter
                and len(self.tables_filter) > FlextConstants.Limits.MAX_LIST_SIZE
            ):
                return FlextResult[None].fail(
                    f"Too many tables specified: {len(self.tables_filter)}"
                )

            return FlextResult[None].ok(None)

        except Exception as e:
            return FlextResult[None].fail(f"Business rules validation failed: {e}")

    @classmethod
    def create_for_environment(
        cls, environment: str, **overrides: object
    ) -> FlextOracleTapConfig:
        """Create configuration for specific environment."""
        env_overrides: dict[str, object] = {}

        if environment == "production":
            env_overrides.update({
                "batch_size": FlextConstants.Performance.DEFAULT_BATCH_SIZE,
                "max_parallel_streams": 4,
                "query_timeout": 300,  # 5 minutes for production
            })
        elif environment == "development":
            env_overrides.update({
                "batch_size": 1000,  # Smaller batches for development
                "max_parallel_streams": 1,
                "query_timeout": 60,
            })
        elif environment == "staging":
            env_overrides.update({
                "batch_size": FlextConstants.Performance.DEFAULT_BATCH_SIZE // 2,
                "max_parallel_streams": 2,
                "query_timeout": 180,
            })

        all_overrides = {**env_overrides, **overrides}
        # Pydantic BaseSettings handles kwargs validation and type conversion automatically
        return cls(**all_overrides)

    # Enhanced singleton pattern methods
    @classmethod
    def get_global_instance(cls) -> Self:
        """Get the global singleton instance using enhanced FlextConfig pattern."""
        return cls.get_or_create_shared_instance(project_name="flext-tap-oracle")

    @classmethod
    def create_for_development(cls, **overrides) -> Self:
        """Create development configuration instance."""
        dev_defaults = {
            "oracle_host": "localhost",
            "oracle_port": 1521,
            "oracle_service_name": "ORCL",
            "oracle_username": "tap_dev",
            "batch_size": 1000,
            "max_parallel_streams": 1,
            "query_timeout": 60,
        }
        dev_defaults.update(overrides)
        return cls(**dev_defaults)

    @classmethod
    def create_for_production(cls, **overrides) -> Self:
        """Create production configuration instance."""
        prod_defaults = {
            "batch_size": 10000,
            "max_parallel_streams": 4,
            "query_timeout": 300,
            "fetch_size": 50000,
            "enable_incremental": True,
        }
        prod_defaults.update(overrides)
        return cls(**prod_defaults)

    @classmethod
    def create_for_testing(cls, **overrides) -> Self:
        """Create testing configuration instance."""
        test_defaults = {
            "oracle_host": "test-oracle",
            "oracle_port": 1521,
            "oracle_service_name": "XE",
            "oracle_username": "test_user",
            "batch_size": 100,
            "max_parallel_streams": 1,
            "query_timeout": 30,
        }
        test_defaults.update(overrides)
        return cls(**test_defaults)


# Factory function for easy creation using configuration objects pattern
def create_oracle_tap_config(
    oracle_params: FlextTapOracleTypes.Database.DatabaseConfiguration,
    tap_params: FlextTapOracleTypes.Configuration.TapOracleConfig | None = None,
    meltano_params: FlextTapOracleTypes.Configuration.TapOracleConfig | None = None,
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
            FlextConstants.Config.DEFAULT_ENVIRONMENT,
        )

        # Merge Oracle parameters with other configurations
        config_data = {
            **oracle_params,  # Use oracle_params properly
            **tap_config,
            **meltano_config,
        }

        config_instance = FlextOracleTapConfig.model_validate(config_data)
        return FlextResult[FlextOracleTapConfig].ok(config_instance)

    except Exception as e:
        return FlextResult[FlextOracleTapConfig].fail(
            f"Oracle tap configuration creation failed: {e}",
        )


# Backward compatibility aliases
FlextOracleTapConfig = FlextTapOracleConfig
TapOracleConfig = FlextTapOracleConfig
Config = FlextTapOracleConfig

__all__: FlextTapOracleTypes.Core.StringList = [
    "Config",  # Legacy alias
    "FlextOracleTapConfig",  # Legacy alias
    "FlextOracleTapConfiguration",
    "FlextTapOracleConfig",
    "TapOracleConfig",  # Legacy alias
    "create_oracle_tap_config",
]
