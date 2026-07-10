"""Service base for flext-tap-oracle tests."""

from __future__ import annotations

from typing import override

from flext_tests import s as tests_s

from flext_tap_oracle import m
from tests.settings import TestsFlextTapOracleSettings


class TestsFlextTapOracleServiceBase(tests_s):
    """Tap Oracle test service base with source and test settings namespaces."""

    @classmethod
    @override
    def fetch_settings(cls) -> TestsFlextTapOracleSettings:
        """Return the typed Tap Oracle+Tests settings singleton."""

    @classmethod
    @override
    def _runtime_bootstrap_options(cls) -> m.RuntimeBootstrapOptions:
        return m.RuntimeBootstrapOptions(settings_type=TestsFlextTapOracleSettings)


s = TestsFlextTapOracleServiceBase

__all__: list[str] = ["TestsFlextTapOracleServiceBase", "s"]
