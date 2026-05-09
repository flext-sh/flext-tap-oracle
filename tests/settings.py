"""Runtime settings for flext-tap-oracle tests."""

from __future__ import annotations

from flext_tests.settings import FlextTestsSettings

from flext_tap_oracle import FlextTapOracleSettings


class TestsFlextTapOracleSettings(FlextTapOracleSettings, FlextTestsSettings):
    """Tap Oracle settings extended with the shared test namespace."""


__all__: list[str] = ["TestsFlextTapOracleSettings"]
