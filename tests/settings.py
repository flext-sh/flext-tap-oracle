"""Runtime settings for flext-tap-oracle tests."""

from __future__ import annotations

from flext_tap_oracle import FlextTapOracleSettings
from flext_tests import FlextTestsSettings


class TestsFlextTapOracleSettings(FlextTapOracleSettings, FlextTestsSettings):
    """Tap Oracle settings extended with the shared test namespace.

    Oracle credentials live under ``settings.TapOracle.*`` (ADR-005) with
    non-secret defaults, so no flat legacy overrides are declared here.
    """


__all__: list[str] = ["TestsFlextTapOracleSettings"]
