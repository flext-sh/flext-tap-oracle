"""Service base for flext-tap-oracle tests."""

from __future__ import annotations

from typing import override

from flext_tests import s as tests_s

from flext_tap_oracle import m
from tests.settings import TestsFlextTapOracleSettings


class TestsFlextTapOracleServiceBase(tests_s):
    """Tap Oracle test service base with source and test settings namespaces."""

    # NOTE (multi-agent): flext-tests owns fetch_settings; this project
    # declares only its more-specific bootstrap settings type.
    @classmethod
    @override
    def _runtime_bootstrap_options(cls) -> p.RuntimeBootstrapOptions:
        return m.RuntimeBootstrapOptions(settings_type=TestsFlextTapOracleSettings)


s = TestsFlextTapOracleServiceBase

__all__: list[str] = ["TestsFlextTapOracleServiceBase", "s"]
