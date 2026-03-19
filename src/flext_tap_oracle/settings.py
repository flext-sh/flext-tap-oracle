"""FLEXT Tap Oracle Configuration - Enhanced FlextSettings Implementation.

Single unified configuration class for Oracle Singer tap operations following
FLEXT 1.0.0 patterns with enhanced singleton, SecretStr, and Pydantic 2.11+ features.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT

"""

from __future__ import annotations

from typing import Annotated

from flext_core import FlextLogger, FlextSettings, r
from pydantic import Field, SecretStr

from flext_tap_oracle import c, t

logger = FlextLogger(__name__)


class FlextTapOracleSettings(FlextSettings):
    """Runtime settings for Oracle Singer tap operations."""

    oracle_host: Annotated[
        str,
        Field(default="localhost", description="Oracle database host"),
    ]
    oracle_port: Annotated[int, Field(default=1521, description="Oracle database port")]
    oracle_service_name: Annotated[
        str,
        Field(default="ORCL", description="Oracle service name or SID"),
    ]
    oracle_user: Annotated[SecretStr, Field(description="Oracle database username")]
    oracle_password: Annotated[SecretStr, Field(description="Oracle database password")]
    batch_size: Annotated[
        int,
        Field(default=1000, ge=1, description="Batch size for data extraction"),
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

    def get_oracle_config(self) -> dict[str, t.Scalar]:
        """Get Oracle database connection configuration."""
        return {
            "host": self.oracle_host,
            "port": self.oracle_port,
            "service_name": self.oracle_service_name,
            "user": self.oracle_user.get_secret_value(),
            "password": self.oracle_password.get_secret_value(),
        }

    def get_tap_config(self) -> dict[str, t.Scalar]:
        """Get tap-specific configuration settings."""
        return {
            "batch_size": self.batch_size,
            "stream_prefix": self.stream_prefix,
            "project_root": self.project_root,
            "environment": self.environment,
        }


def create_oracle_tap_config(
    oracle_params: dict[str, t.Scalar],
    tap_params: dict[str, t.Scalar] | None = None,
    meltano_params: dict[str, t.Scalar] | None = None,
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
        tap_config = tap_params or {}
        meltano_config = meltano_params or {}
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
    except (ValueError, TypeError, KeyError, AttributeError, OSError) as e:
        return r[FlextTapOracleSettings].fail(
            f"Oracle tap configuration creation failed: {e}",
        )


def validate_oracle_tap_configuration(
    config: FlextTapOracleSettings,
) -> r[bool]:
    """Validate Oracle tap configuration using FlextSettings patterns."""
    return config.validate_business_rules()


__all__: list[str] = [
    "FlextTapOracleSettings",
    "create_oracle_tap_config",
    "validate_oracle_tap_configuration",
]
