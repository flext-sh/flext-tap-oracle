"""FLEXT Tap Oracle Configuration - Enhanced FlextSettings Implementation.

Single unified configuration class for Oracle Singer tap operations following
FLEXT 1.0.0 patterns with enhanced singleton, SecretStr, and Pydantic 2.11+ features.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT

"""

from __future__ import annotations

import re
from collections.abc import Mapping
from typing import Self, override

from flext_core import FlextResult, FlextSettings
from pydantic import Field, SecretStr, field_validator, model_validator
from pydantic_settings import SettingsConfigDict

from flext_tap_oracle.constants import c
from flext_tap_oracle.typings import t


class FlextMeltanoTapOracleSettings(FlextSettings):
    """Oracle Tap Configuration using enhanced FlextSettings patterns.

    This class extends FlextSettings and includes all the configuration fields
    needed for Oracle tap operations. Uses the enhanced singleton pattern
    with get_or_create_shared_instance for thread-safe configuration management.

    Follows standardized pattern:
    - Extends FlextSettings from flext-core
    - Uses SecretStr for sensitive data (oracle_password)
    - All defaults from FlextConstants where possible
    - Uses enhanced singleton pattern with inverse dependency injection
    - Uses Pydantic 2.11+ features (field_validator, model_validator)
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
        # Enhanced Pydantic 2.11+ features
        validate_return=True,
        json_schema_extra={
            "title": "FLEXT Tap Oracle Configuration",
            "description": "Oracle Singer tap configuration extending FlextSettings",
        },
    )

    # Oracle Database Configuration using SecretStr for password
    oracle_host: str = Field(
        default="localhost",
        description="Oracle database host",
    )

    oracle_port: int = Field(
        default=c.TapOracle.Oracle.DEFAULT_PORT,
        ge=1,
        le=65535,
        description="Oracle database port",
    )

    oracle_service_name: str = Field(
        default="",
        description="Oracle service name",
    )

    oracle_sid: str = Field(
        default="",
        description="Oracle SID",
    )

    oracle_username: str = Field(
        default="",
        description="Oracle username",
    )

    oracle_password: SecretStr = Field(
        default_factory=lambda: SecretStr(""),
        description="Oracle password (sensitive)",
    )

    # Tap-specific Configuration using FlextConstants where applicable
    stream_prefix: str = Field(
        default=c.TapOracle.DEFAULT_STREAM_PREFIX,
        min_length=1,
        description="Prefix for Singer stream names",
    )

    batch_size: int = Field(
        default=c.TapOracle.Singer.DEFAULT_BATCH_SIZE,
        ge=1,
        le=c.TapOracle.Singer.MAX_BATCH_SIZE,
        description="Batch size for data extraction",
    )

    max_parallel_streams: int = Field(
        default=4,
        ge=1,
        le=8,
        description="Maximum parallel streams for extraction",
    )

    tables_filter: list[str] | None = Field(
        default=None,
        description="List of table names to extract (None = all tables)",
    )

    schemas_filter: list[str] | None = Field(
        default=None,
        description="List of schema names to extract (None = all schemas)",
    )

    enable_incremental: bool = Field(
        default=True,
        description="Enable incremental extraction",
    )

    incremental_column: str = Field(
        default="LAST_MODIFIED",
        description="Column for incremental extraction",
    )

    # Performance Configuration using FlextConstants
    fetch_size: int = Field(
        default=c.TapOracle.Oracle.DEFAULT_FETCH_SIZE,
        ge=100,
        le=100000,
        description="Oracle fetch size for queries",
    )

    query_timeout: int = Field(
        default=30,
        ge=1,
        le=3600,
        description="Query timeout in seconds",
    )

    # Project identification
    project_name: str = Field(
        default="flext-tap-oracle",
        description="Project name",
    )

    project_version: str = Field(
        default="0.9.0",
        description="Project version",
    )

    # Pydantic 2.11+ field validators
    @field_validator("stream_prefix")
    @classmethod
    def validate_stream_prefix(cls, v: str) -> str:
        """Validate stream prefix follows Oracle naming conventions.

        Checks regex, length, and applies lowercase transformation.
        """
        # Oracle identifiers: start with letter, contain letters/digits/underscore
        if not re.match(r"^[a-zA-Z][a-zA-Z0-9_]*$", v):
            msg = f"Invalid stream prefix: {v}. Must start with letter and contain only letters, digits, and underscores"
            raise ValueError(msg)

        max_length = c.TapOracle.TapValidation.MAX_STREAM_PREFIX_LENGTH
        if len(v) > max_length:
            msg = f"Stream prefix too long: {len(v)} > {max_length}"
            raise ValueError(msg)

        return v.lower()

    @field_validator("tables_filter")
    @classmethod
    def validate_tables_filter(cls, v: list[str] | None) -> list[str] | None:
        """Validate tables filter list."""
        if v is None:
            return v

        max_count = c.TapOracle.TapValidation.MAX_TABLES_FILTER_COUNT
        if len(v) > max_count:
            msg = f"Too many tables specified: {len(v)} > {max_count}"
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

        max_schemas = c.TapOracle.TapValidation.MAX_SCHEMAS_FILTER_COUNT
        if len(v) > max_schemas:
            msg = f"Too many schemas specified: {len(v)} > {max_schemas}"
            raise ValueError(msg)

        for schema in v:
            if not re.match(r"^[a-zA-Z][a-zA-Z0-9_]*$", schema):
                msg = f"Invalid schema name: {schema}"
                raise ValueError(msg)

        return v

    @model_validator(mode="after")
    def validate_oracle_connection_config(self) -> Self:
        """Validate Oracle connection configuration."""
        # Either service_name or sid must be provided
        service_name = self.oracle_service_name.strip() if self.oracle_service_name else ""
        sid = self.oracle_sid.strip() if self.oracle_sid else ""

        if not service_name and not sid:
            msg = "Either oracle_service_name or oracle_sid must be provided"
            raise ValueError(msg)

        # Cannot have both service_name and sid
        if service_name and sid:
            msg = "Cannot specify both oracle_service_name and oracle_sid"
            raise ValueError(msg)

        # Validate parallel streams vs batch size
        max_safe_parallel = c.TapOracle.TapValidation.MAX_SAFE_PARALLEL_STREAMS
        max_safe_batch = c.TapOracle.Singer.MAX_BATCH_SIZE // 2
        if (
            self.max_parallel_streams > max_safe_parallel
            and self.batch_size > max_safe_batch
        ):
            msg = "High parallelism with large batch sizes may cause memory issues"
            raise ValueError(msg)

        return self

    def validate_business_rules(self) -> FlextResult[bool]:
        """Validate Oracle tap configuration business rules."""
        try:
            # Validate Oracle configuration
            if not self.oracle_host:
                return FlextResult[bool].fail("Oracle host is required")

            if not self.oracle_username:
                return FlextResult[bool].fail("Oracle username is required")

            if not self.oracle_password.get_secret_value():
                return FlextResult[bool].fail("Oracle password is required")

            # Validate connection string can be generated
            try:
                self.get_connection_string()
            except ValueError as e:
                return FlextResult[bool].fail(
                    f"Connection string validation failed: {e}",
                )

            # Validate performance settings
            max_safe_parallel = c.TapOracle.TapValidation.MAX_SAFE_PARALLEL_STREAMS
            max_safe_batch = c.TapOracle.Singer.MAX_BATCH_SIZE // 2
            if (
                self.max_parallel_streams > max_safe_parallel
                and self.batch_size > max_safe_batch
            ):
                return FlextResult[bool].fail(
                    "High parallelism with large batch sizes may cause memory issues",
                )

            # Validate filters
            if (
                self.tables_filter
                and len(self.tables_filter)
                > c.TapOracle.TapValidation.MAX_TABLES_FILTER_COUNT
            ):
                return FlextResult[bool].fail(
                    f"Too many tables specified: {len(self.tables_filter)}",
                )

            return FlextResult[bool].ok(value=True)

        except (ValueError, TypeError, KeyError, AttributeError, OSError) as e:
            return FlextResult[bool].fail(f"Business rules validation failed: {e}")

    # Configuration helper methods
    def get_oracle_config(self) -> Mapping[str, t.JsonValue]:
        """Get Oracle configuration for flext-db-oracle integration."""
        return {
            "host": self.oracle_host,
            "port": self.oracle_port,
            "service_name": self.oracle_service_name,
            "sid": self.oracle_sid,
            "username": self.oracle_username,
            "password": self.oracle_password.get_secret_value(),
            "pool_min": 1,
            "pool_max": self.max_parallel_streams + 2,  # Extra connections for metadata
            "timeout": self.query_timeout,
        }

    def get_tap_config(self) -> Mapping[str, t.JsonValue]:
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

    def get_performance_config(self) -> Mapping[str, t.JsonValue]:
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

    @classmethod
    def create_for_environment(
        cls,
        environment: str,
        **overrides: t.JsonValue,
    ) -> FlextMeltanoTapOracleSettings:
        """Create configuration for specific environment using enhanced singleton pattern."""
        env_overrides: dict[str, t.JsonValue] = {}

        if environment == "production":
            env_overrides.update({
                "batch_size": c.TapOracle.Singer.MAX_BATCH_SIZE,
                "max_parallel_streams": c.TapOracle.EnvironmentDefaults.Production.MAX_PARALLEL_STREAMS,
                "query_timeout": c.TapOracle.EnvironmentDefaults.Production.QUERY_TIMEOUT_SECONDS,
            })
        elif environment == "development":
            env_overrides.update({
                "batch_size": c.TapOracle.Singer.DEFAULT_BATCH_SIZE,
                "max_parallel_streams": c.TapOracle.EnvironmentDefaults.Development.MAX_PARALLEL_STREAMS,
                "query_timeout": c.TapOracle.EnvironmentDefaults.Development.QUERY_TIMEOUT_SECONDS,
            })
        elif environment == "staging":
            env_overrides.update({
                "batch_size": c.TapOracle.Singer.DEFAULT_BATCH_SIZE * 2,
                "max_parallel_streams": c.TapOracle.EnvironmentDefaults.Staging.MAX_PARALLEL_STREAMS,
                "query_timeout": c.TapOracle.EnvironmentDefaults.Staging.QUERY_TIMEOUT_SECONDS,
            })

        all_overrides = {**env_overrides, **overrides}
        return cls.model_validate(all_overrides)

    @classmethod
    @override
    def get_global_instance(cls) -> Self:
        """Get the global singleton instance using enhanced FlextSettings pattern."""
        return cls()

    @classmethod
    def create_for_development(cls, **overrides: t.JsonValue) -> Self:
        """Create configuration for development environment."""
        dev_overrides: dict[str, t.JsonValue] = {
            "oracle_host": "localhost",
            "oracle_port": c.TapOracle.Oracle.DEFAULT_PORT,
            "oracle_service_name": "ORCL",
            "oracle_username": "tap_dev",
            "batch_size": c.TapOracle.Singer.DEFAULT_BATCH_SIZE,
            "max_parallel_streams": 1,
            "query_timeout": 60,
            **overrides,
        }
        return cls.model_validate(dev_overrides)

    @classmethod
    def create_for_production(cls, **overrides: t.JsonValue) -> Self:
        """Create configuration for production environment."""
        prod_overrides: dict[str, t.JsonValue] = {
            "batch_size": c.TapOracle.Singer.MAX_BATCH_SIZE,
            "max_parallel_streams": 4,
            "query_timeout": 300,
            "fetch_size": c.TapOracle.Oracle.DEFAULT_FETCH_SIZE * 5,
            "enable_incremental": True,
            **overrides,
        }
        return cls.model_validate(prod_overrides)

    @classmethod
    def create_for_testing(cls, **overrides: t.JsonValue) -> Self:
        """Create configuration for testing environment."""
        test_overrides: dict[str, t.JsonValue] = {
            "oracle_host": "test-oracle",
            "oracle_port": c.TapOracle.Oracle.DEFAULT_PORT,
            "oracle_service_name": "XE",
            "oracle_username": "test_user",
            "batch_size": 100,
            "max_parallel_streams": 1,
            "query_timeout": 30,
            **overrides,
        }
        return cls.model_validate(test_overrides)

    @classmethod
    @override
    def reset_global_instance(cls) -> None:
        """Reset the global FlextMeltanoTapOracleSettings instance (mainly for testing)."""
        # No shared instance to reset


def create_oracle_tap_config(
    oracle_params: dict[str, t.JsonValue],
    tap_params: dict[str, t.JsonValue] | None = None,
    meltano_params: dict[str, t.JsonValue] | None = None,
) -> FlextResult[FlextMeltanoTapOracleSettings]:
    """Create Oracle tap configuration using grouped parameters.

    Args:
        oracle_params: Oracle database connection parameters
        tap_params: Optional tap-specific parameters
        meltano_params: Optional Meltano parameters

    Returns:
        FlextResult containing validated Oracle tap configuration

    """
    try:
        tap_config = tap_params or {}
        meltano_config = meltano_params or {}

        tap_config.setdefault("batch_size", 1000)
        tap_config.setdefault("stream_prefix", c.TapOracle.DEFAULT_STREAM_PREFIX)
        meltano_config.setdefault("project_root", ".")
        meltano_config.setdefault("environment", "production")

        config_data = {
            **oracle_params,
            **tap_config,
            **meltano_config,
        }

        config_instance = FlextMeltanoTapOracleSettings.model_validate(config_data)
        return FlextResult[FlextMeltanoTapOracleSettings].ok(config_instance)

    except (ValueError, TypeError, KeyError, AttributeError, OSError) as e:
        return FlextResult[FlextMeltanoTapOracleSettings].fail(
            f"Oracle tap configuration creation failed: {e}",
        )


def validate_oracle_tap_configuration(
    config: FlextMeltanoTapOracleSettings,
) -> FlextResult[bool]:
    """Validate Oracle tap configuration using FlextSettings patterns."""
    return config.validate_business_rules()


__all__: list[str] = [
    "FlextMeltanoTapOracleSettings",
    "create_oracle_tap_config",
    "validate_oracle_tap_configuration",
]
