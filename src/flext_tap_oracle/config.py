"""FLEXT Tap Oracle Configuration - Enhanced FlextConfig Implementation.

Single unified configuration class for Oracle Singer tap operations following
FLEXT 1.0.0 patterns with enhanced singleton, SecretStr, and Pydantic 2.11+ features.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT

"""

from __future__ import annotations

import re
from typing import Self

from flext_core import FlextConfig, FlextConstants, FlextResult
from flext_db_oracle import FlextDbOracleModels
from pydantic import Field, SecretStr, field_validator, model_validator
from pydantic_settings import SettingsConfigDict


class FlextMeltanoTapOracleConfig(FlextConfig):
    """Oracle Tap Configuration using enhanced FlextConfig patterns.

    This class extends FlextConfig and includes all the configuration fields
    needed for Oracle tap operations. Uses the enhanced singleton pattern
    with get_or_create_shared_instance for thread-safe configuration management.

    Follows standardized pattern:
    - Extends FlextConfig from flext-core
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
            "description": "Oracle Singer tap configuration extending FlextConfig",
        },
    )

    # Oracle Database Configuration using SecretStr for password
    oracle_host: str = Field(
        default="localhost",
        description="Oracle database host",
    )

    oracle_port: int = Field(
        default=FlextConstants.Platform.DATABASE_DEFAULT_PORT,
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
        default="oracle",
        description="Prefix for Singer stream names",
    )

    batch_size: int = Field(
        default=FlextConstants.Performance.DEFAULT_BATCH_SIZE,
        ge=1,
        le=FlextConstants.Performance.MAX_BATCH_SIZE_VALIDATION,
        description="Batch size for data extraction",
    )

    max_parallel_streams: int = Field(
        default=FlextConstants.Container.DEFAULT_WORKERS,
        ge=1,
        le=FlextConstants.Container.MAX_WORKERS,
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
        default=FlextConstants.Performance.BatchProcessing.MAX_ITEMS,
        ge=100,
        le=100000,
        description="Oracle fetch size for queries",
    )

    query_timeout: int = Field(
        default=FlextConstants.Network.DEFAULT_TIMEOUT,
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

        max_schemas = (
            FlextConstants.Limits.MAX_LIST_SIZE // 10
        )  # Reasonable schema limit
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
        if not self.oracle_service_name and not self.oracle_sid:
            msg = "Either oracle_service_name or oracle_sid must be provided"
            raise ValueError(msg)

        # Cannot have both service_name and sid
        if self.oracle_service_name and self.oracle_sid:
            msg = "Cannot specify both oracle_service_name and oracle_sid"
            raise ValueError(msg)

        # Validate parallel streams vs batch size
        max_safe_parallel = FlextConstants.Container.MAX_WORKERS
        max_safe_batch = FlextConstants.Performance.BatchProcessing.MAX_ITEMS // 2
        if (
            self.max_parallel_streams > max_safe_parallel
            and self.batch_size > max_safe_batch
        ):
            msg = "High parallelism with large batch sizes may cause memory issues"
            raise ValueError(msg)

        return self

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
            max_safe_parallel = FlextConstants.Container.MAX_WORKERS
            max_safe_batch = FlextConstants.Performance.BatchProcessing.MAX_ITEMS // 2
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

    @classmethod
    def create_for_environment(
        cls, environment: str, **overrides: object
    ) -> FlextMeltanoTapOracleConfig:
        """Create configuration for specific environment using enhanced singleton pattern."""
        env_overrides: dict[str, object] = {}

        if environment == "production":
            env_overrides.update({
                "batch_size": FlextConstants.Performance.DEFAULT_BATCH_SIZE,
                "max_parallel_streams": FlextConstants.Container.DEFAULT_WORKERS,
                "query_timeout": FlextConstants.Network.DEFAULT_TIMEOUT
                * 10,  # 5 minutes for production
            })
        elif environment == "development":
            env_overrides.update({
                "batch_size": FlextConstants.Performance.BatchProcessing.DEFAULT_SIZE,  # Smaller batches for development
                "max_parallel_streams": 1,
                "query_timeout": FlextConstants.Network.DEFAULT_TIMEOUT * 2,
            })
        elif environment == "staging":
            env_overrides.update({
                "batch_size": FlextConstants.Performance.DEFAULT_BATCH_SIZE // 2,
                "max_parallel_streams": 2,
                "query_timeout": FlextConstants.Network.DEFAULT_TIMEOUT * 6,
            })

        all_overrides = {**env_overrides, **overrides}
        return cls.get_or_create_shared_instance(
            project_name="flext-tap-oracle", environment=environment, **all_overrides
        )

    @classmethod
    def get_global_instance(cls) -> Self:
        """Get the global singleton instance using enhanced FlextConfig pattern."""
        return cls.get_or_create_shared_instance(project_name="flext-tap-oracle")

    @classmethod
    def create_for_development(cls, **overrides: object) -> Self:
        """Create configuration for development environment."""
        dev_overrides: dict[str, object] = {
            "oracle_host": "localhost",
            "oracle_port": FlextConstants.Platform.DATABASE_DEFAULT_PORT,
            "oracle_service_name": "ORCL",
            "oracle_username": "tap_dev",
            "batch_size": FlextConstants.Performance.BatchProcessing.DEFAULT_SIZE,
            "max_parallel_streams": 1,
            "query_timeout": FlextConstants.Network.DEFAULT_TIMEOUT * 2,
            **overrides,
        }
        return cls.get_or_create_shared_instance(
            project_name="flext-tap-oracle", **dev_overrides
        )

    @classmethod
    def create_for_production(cls, **overrides: object) -> Self:
        """Create configuration for production environment."""
        prod_overrides: dict[str, object] = {
            "batch_size": FlextConstants.Performance.BatchProcessing.MAX_ITEMS,
            "max_parallel_streams": FlextConstants.Container.DEFAULT_WORKERS,
            "query_timeout": FlextConstants.Network.DEFAULT_TIMEOUT * 10,
            "fetch_size": FlextConstants.Performance.BatchProcessing.MAX_ITEMS * 5,
            "enable_incremental": True,
            **overrides,
        }
        return cls.get_or_create_shared_instance(
            project_name="flext-tap-oracle", **prod_overrides
        )

    @classmethod
    def create_for_testing(cls, **overrides: object) -> Self:
        """Create configuration for testing environment."""
        test_overrides: dict[str, object] = {
            "oracle_host": "test-oracle",
            "oracle_port": FlextConstants.Platform.DATABASE_DEFAULT_PORT,
            "oracle_service_name": "XE",
            "oracle_username": "test_user",
            "batch_size": FlextConstants.Performance.BatchProcessing.DEFAULT_SIZE // 10,
            "max_parallel_streams": 1,
            "query_timeout": FlextConstants.Network.DEFAULT_TIMEOUT,
            **overrides,
        }
        return cls.get_or_create_shared_instance(
            project_name="flext-tap-oracle", **test_overrides
        )

    @classmethod
    def reset_global_instance(cls) -> None:
        """Reset the global FlextMeltanoTapOracleConfig instance (mainly for testing)."""
        cls.reset_shared_instance()


# Factory function for backward compatibility (will be removed in future versions)
def create_oracle_tap_config(
    oracle_params: dict[str, object],
    tap_params: dict[str, object] | None = None,
    meltano_params: dict[str, object] | None = None,
) -> FlextResult[FlextMeltanoTapOracleConfig]:
    """Create Oracle tap configuration using grouped parameters.

    Args:
    oracle_params: Oracle database connection parameters
    tap_params: Optional tap-specific parameters
    meltano_params: Optional Meltano parameters

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

        # Merge Oracle parameters with other configurations
        config_data = {
            **oracle_params,
            **tap_config,
            **meltano_config,
        }

        config_instance = (
            FlextMeltanoTapOracleConfig.get_global_instance().model_validate(
                config_data
            )
        )
        return FlextResult[FlextMeltanoTapOracleConfig].ok(config_instance)

    except Exception as e:
        return FlextResult[FlextMeltanoTapOracleConfig].fail(
            f"Oracle tap configuration creation failed: {e}",
        )


def validate_oracle_tap_configuration(
    config: FlextMeltanoTapOracleConfig,
) -> FlextResult[None]:
    """Validate Oracle tap configuration using FlextConfig patterns - ZERO DUPLICATION."""
    # Required string fields validation
    required_fields = [
        (config.oracle_host, "Oracle host is required"),
        (config.oracle_username, "Oracle username is required"),
        (config.oracle_password.get_secret_value(), "Oracle password is required"),
    ]

    # Validate required string fields
    for field_value, error_message in required_fields:
        if not (field_value and str(field_value).strip()):
            return FlextResult[None].fail(error_message)

    # Validate Oracle port range
    if not (
        FlextConstants.Network.MIN_PORT
        <= config.oracle_port
        <= FlextConstants.Network.MAX_PORT
    ):
        return FlextResult[None].fail(
            f"Oracle port must be between {FlextConstants.Network.MIN_PORT} and {FlextConstants.Network.MAX_PORT}"
        )

    # Validate either service_name or sid
    if not config.oracle_service_name and not config.oracle_sid:
        return FlextResult[None].fail(
            "Either oracle_service_name or oracle_sid must be provided"
        )

    # Validate batch size constraints
    if config.batch_size < 1:
        return FlextResult[None].fail("Batch size must be at least 1")

    # Validate query timeout
    if config.query_timeout < 1:
        return FlextResult[None].fail("Query timeout must be at least 1 second")

    return FlextResult[None].ok(None)


__all__: list[str] = [
    "FlextMeltanoTapOracleConfig",
    "create_oracle_tap_config",
    "validate_oracle_tap_configuration",
]
