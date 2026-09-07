"""Typed fixtures backed by the public tap-oracle owners."""

from __future__ import annotations

import pytest

from flext_tap_oracle import (
    FlextTapOracleConfig,
    FlextTapOracleService,
    FlextTapOracleSettings,
    config,
    settings,
)


@pytest.fixture
def tap_oracle_settings() -> FlextTapOracleSettings:
    """Return the settings singleton consumed by the runtime facade."""
    return settings


@pytest.fixture
def tap_oracle_config() -> FlextTapOracleConfig:
    """Return the validated public configuration singleton."""
    return config


@pytest.fixture
def tap_oracle_service(
    tap_oracle_settings: FlextTapOracleSettings,
) -> FlextTapOracleService:
    """Return the real public service with its settings dependency injected."""
    return FlextTapOracleService(settings=tap_oracle_settings)
