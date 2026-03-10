"""FLEXT Tap Oracle Configuration - Enhanced FlextSettings Implementation.

Single unified configuration class for Oracle Singer tap operations following
FLEXT 1.0.0 patterns with enhanced singleton, SecretStr, and Pydantic 2.11+ features.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT

"""

from __future__ import annotations

from flext_core import FlextLogger, FlextResult, FlextSettings, c, t
from pydantic import Field, SecretStr

logger = FlextLogger(__name__)


class FlextTapOracleSettings(FlextSettings):
    """Runtime settings for Oracle Singer tap operations."""

    oracle_host: str = Field(default="localhost", description="Oracle database host")
    oracle_port: int = Field(default=1521, description="Oracle database port")
    oracle_service_name: str = Field(
        default="ORCL", description="Oracle service name or SID"
    )
    oracle_user: SecretStr = Field(description="Oracle database username")
    oracle_password: SecretStr = Field(description="Oracle database password")
    batch_size: int = Field(
        default=1000, ge=1, description="Batch size for data extraction"
    )
    stream_prefix: str = Field(default="", description="Prefix for Singer stream names")
    project_root: str = Field(default=".", description="Meltano project root")
    environment: str = Field(default="production", description="Environment name")

    def validate_business_rules(self) -> FlextResult[bool]:
        """Validate Oracle tap configuration business rules."""
        if not self.oracle_host:
            return FlextResult[bool].fail("Oracle host is required")
        if not self.oracle_service_name:
            return FlextResult[bool].fail("Oracle service name is required")
        return FlextResult[bool].ok(True)


def create_oracle_tap_config(
    oracle_params: dict[str, t.JsonValue],
    tap_params: dict[str, t.JsonValue] | None = None,
    meltano_params: dict[str, t.JsonValue] | None = None,
) -> FlextResult[FlextTapOracleSettings]:
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
        config_data = {**oracle_params, **tap_config, **meltano_config}
        config_instance = FlextTapOracleSettings.model_validate(config_data)
        return FlextResult[FlextTapOracleSettings].ok(config_instance)
    except (ValueError, TypeError, KeyError, AttributeError, OSError) as e:
        return FlextResult[FlextTapOracleSettings].fail(
            f"Oracle tap configuration creation failed: {e}"
        )


def validate_oracle_tap_configuration(
    config: FlextTapOracleSettings,
) -> FlextResult[bool]:
    """Validate Oracle tap configuration using FlextSettings patterns."""
    return config.validate_business_rules()


__all__: list[str] = [
    "FlextTapOracleSettings",
    "create_oracle_tap_config",
    "validate_oracle_tap_configuration",
]
