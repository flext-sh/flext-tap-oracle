"""FLEXT Tap Oracle Configuration - Enhanced FlextSettings Implementation.

Single unified configuration class for Oracle Singer tap operations following
FLEXT 1.0.0 patterns with enhanced singleton, SecretStr, and Pydantic 2.11+ features.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT

"""

from __future__ import annotations

from typing import Annotated, ClassVar, Self

from pydantic import Field, SecretStr
from pydantic_settings import SettingsConfigDict

from flext_core import FlextSettings, r
from flext_tap_oracle import c, t


@FlextSettings.auto_register("tap-oracle")
class FlextTapOracleSettings(FlextSettings):
    """Runtime settings for Oracle Singer tap operations."""

    model_config: ClassVar[SettingsConfigDict] = SettingsConfigDict(
        env_prefix="FLEXT_TAP_ORACLE_", extra="ignore"
    )

    oracle_host: Annotated[
        t.NonEmptyStr,
        Field(
            default=c.DbOracle.OracleDefaults.DEFAULT_HOST,
            description="Oracle database host",
        ),
    ]
    oracle_port: Annotated[
        t.PortNumber,
        Field(
            default=c.DbOracle.Connection.DEFAULT_PORT,
            description="Oracle database port",
        ),
    ]
    oracle_service_name: Annotated[
        str,
        Field(
            default=c.DbOracle.Connection.DEFAULT_SERVICE_NAME,
            description="Oracle service name or SID",
        ),
    ]
    oracle_user: Annotated[SecretStr, Field(description="Oracle database username")]
    oracle_password: Annotated[SecretStr, Field(description="Oracle database password")]
    batch_size: Annotated[
        t.BatchSize,
        Field(default=1000, description="Batch size for data extraction"),
    ]
    stream_prefix: Annotated[
        str,
        Field(default="", description="Prefix for Singer stream names"),
    ]
    project_root: Annotated[str, Field(default=".", description="Meltano project root")]
    environment: Annotated[
        str,
        Field(default="production", description="Environment name"),
    ]

    def validate_business_rules(self) -> r[bool]:
        """Validate Oracle tap configuration business rules."""
        if not self.oracle_host:
            return r[bool].fail("Oracle host is required")
        if not self.oracle_service_name:
            return r[bool].fail("Oracle service name is required")
        return r[bool].ok(True)

    @staticmethod
    def _resolve_secret(value: SecretStr | str) -> str:
        """Resolve a SecretStr to its plain value."""
        if isinstance(value, SecretStr):
            return value.get_secret_value()
        return value

    def get_oracle_config(self) -> t.ConfigurationMapping:
        """Get Oracle database connection configuration."""
        return {
            "host": self.oracle_host,
            "port": self.oracle_port,
            "service_name": self.oracle_service_name,
            "user": self._resolve_secret(self.oracle_user),
            "password": self._resolve_secret(self.oracle_password),
        }

    def get_tap_config(self) -> t.ConfigurationMapping:
        """Get tap-specific configuration settings."""
        return {
            "batch_size": self.batch_size,
            "stream_prefix": self.stream_prefix,
            "project_root": self.project_root,
            "environment": self.environment,
        }

    @staticmethod
    def create_oracle_tap_config(
        oracle_params: t.ConfigurationMapping,
        tap_params: t.ConfigurationMapping | None = None,
        meltano_params: t.ConfigurationMapping | None = None,
    ) -> r[FlextTapOracleSettings]:
        """Create Oracle tap configuration using grouped parameters.

        Args:
            oracle_params: Oracle database connection parameters
            tap_params: Optional tap-specific parameters
            meltano_params: Optional Meltano parameters

        Returns:
            r containing validated Oracle tap configuration

        """
        try:
            tap_config: t.MutableScalarMapping = dict(tap_params) if tap_params else {}
            meltano_config: t.MutableScalarMapping = (
                dict(meltano_params) if meltano_params else {}
            )
            tap_config.setdefault("batch_size", 1000)
            tap_config.setdefault(
                "stream_prefix",
                c.TapOracle.DEFAULT_STREAM_PREFIX,
            )
            meltano_config.setdefault("project_root", ".")
            meltano_config.setdefault("environment", "production")
            config_data = {**oracle_params, **tap_config, **meltano_config}
            config_instance = FlextTapOracleSettings.model_validate(config_data)
            return r[FlextTapOracleSettings].ok(config_instance)
        except c.Meltano.SINGER_SAFE_EXCEPTIONS as e:
            return r[FlextTapOracleSettings].fail(
                f"Oracle tap configuration creation failed: {e}",
            )

    @classmethod
    def validate_oracle_tap_configuration(
        cls,
        settings: Self,
    ) -> r[bool]:
        """Validate Oracle tap configuration using FlextSettings patterns."""
        return settings.validate_business_rules()
