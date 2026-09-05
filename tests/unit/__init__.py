# AUTO-GENERATED FILE — Regenerate with: make gen
"""Tests.unit package."""

from __future__ import annotations

from typing import TYPE_CHECKING

from types import MappingProxyType

from flext_core.lazy import build_lazy_import_map, install_lazy_exports

if TYPE_CHECKING:
    from flext_tests import c, d, e, h, m, p, r, s, t, td, tf, tk, tm, tv, u, x

    from .fixtures import (
        docker_control,
        oracle_shared_container_environment,
        reset_tap_oracle_settings,
        set_test_environment,
        shared_oracle_container,
        skip_e2e_if_no_oracle,
        tap_oracle_create_params,
        tap_oracle_settings_overrides,
    )
    from .test_enterprise_tap import (
        TestsFlextTapOracleEnterpriseTap,
        TestsFlextTapOracleStreams,
    )
__all__: tuple[str, ...] = (
    "TestsFlextTapOracleEnterpriseTap",
    "TestsFlextTapOracleStreams",
    "c",
    "d",
    "docker_control",
    "e",
    "h",
    "m",
    "oracle_shared_container_environment",
    "p",
    "r",
    "reset_tap_oracle_settings",
    "s",
    "set_test_environment",
    "shared_oracle_container",
    "skip_e2e_if_no_oracle",
    "t",
    "tap_oracle_create_params",
    "tap_oracle_settings_overrides",
    "td",
    "tf",
    "tk",
    "tm",
    "tv",
    "u",
    "x",
)

_LAZY_IMPORTS = MappingProxyType(
    build_lazy_import_map(
        MappingProxyType({
            ".fixtures": (
                "docker_control",
                "oracle_shared_container_environment",
                "reset_tap_oracle_settings",
                "set_test_environment",
                "shared_oracle_container",
                "skip_e2e_if_no_oracle",
                "tap_oracle_create_params",
                "tap_oracle_settings_overrides",
            ),
            ".test_enterprise_tap": (
                "TestsFlextTapOracleEnterpriseTap",
                "TestsFlextTapOracleStreams",
            ),
            "flext_tests": (
                "c",
                "d",
                "e",
                "h",
                "m",
                "p",
                "r",
                "s",
                "t",
                "td",
                "tf",
                "tk",
                "tm",
                "tv",
                "u",
                "x",
            ),
        }),
        alias_groups=MappingProxyType({}),
        sort_keys=False,
    )
)

install_lazy_exports(__name__, globals(), _LAZY_IMPORTS, public_exports=__all__)
