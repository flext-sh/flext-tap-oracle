"""Typed fixtures backed by the public tap-oracle owners.

Copyright (c) 2026 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from flext_tap_oracle import (
    FlextTapOracleConfig,
    FlextTapOracleService,
    FlextTapOracleSettings,
    config,
    settings,
)
from tests import u


@u.Tests.fixture
def tap_oracle_settings() -> FlextTapOracleSettings:
    """Return the settings singleton consumed by the runtime facade."""
    return settings


@u.Tests.fixture
def tap_oracle_config() -> FlextTapOracleConfig:
    """Return the validated public configuration singleton."""
    return config


@u.Tests.fixture
def tap_oracle_service(
    tap_oracle_settings: FlextTapOracleSettings,
) -> FlextTapOracleService:
    """Return the real public service with its settings dependency injected."""
    return FlextTapOracleService(settings=tap_oracle_settings)
