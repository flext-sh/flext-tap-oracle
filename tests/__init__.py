# AUTO-GENERATED FILE — Regenerate with: make gen
"""Tests package."""

from __future__ import annotations

from typing import TYPE_CHECKING

from types import MappingProxyType

from flext_core.lazy import build_lazy_import_map, install_lazy_exports

if TYPE_CHECKING:
    from . import unit as unit
    from flext_tap_oracle import FlextTapOracleConstants
    from flext_tests import FlextTestsConstants, d, e, h, r, td, tf, tk, tm, tv, x
    from typing import Final

    from .base import (
        TestsFlextTapOracleServiceBase,
        TestsFlextTapOracleServiceBase as s,
    )
    from .constants import (
        TestsFlextTapOracleConstants,
        TestsFlextTapOracleConstants as c,
    )
    from .models import TestsFlextTapOracleModels, TestsFlextTapOracleModels as m
    from .protocols import (
        TestsFlextTapOracleProtocols,
        TestsFlextTapOracleProtocols as p,
    )
    from .settings import TestsFlextTapOracleSettings
    from .typings import TestsFlextTapOracleTypes, TestsFlextTapOracleTypes as t
    from .unit.fixtures import (
        docker_control,
        oracle_shared_container_environment,
        reset_tap_oracle_settings,
        set_test_environment,
        shared_oracle_container,
        skip_e2e_if_no_oracle,
        tap_oracle_create_params,
        tap_oracle_settings_overrides,
    )
    from .utilities import (
        TestsFlextTapOracleUtilities,
        TestsFlextTapOracleUtilities as u,
    )
__all__: tuple[str, ...] = (
    "Final",
    "FlextTapOracleConstants",
    "FlextTestsConstants",
    "TestsFlextTapOracleConstants",
    "TestsFlextTapOracleModels",
    "TestsFlextTapOracleProtocols",
    "TestsFlextTapOracleServiceBase",
    "TestsFlextTapOracleSettings",
    "TestsFlextTapOracleTypes",
    "TestsFlextTapOracleUtilities",
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
    "unit",
    "x",
)

_LAZY_IMPORTS = MappingProxyType(
    build_lazy_import_map(
        MappingProxyType({
            ".base": ("TestsFlextTapOracleServiceBase", "s"),
            ".constants": ("TestsFlextTapOracleConstants", "c"),
            ".models": ("TestsFlextTapOracleModels", "m"),
            ".protocols": ("TestsFlextTapOracleProtocols", "p"),
            ".settings": ("TestsFlextTapOracleSettings",),
            ".typings": ("TestsFlextTapOracleTypes", "t"),
            ".unit": ("unit",),
            ".unit.fixtures": (
                "docker_control",
                "oracle_shared_container_environment",
                "reset_tap_oracle_settings",
                "set_test_environment",
                "shared_oracle_container",
                "skip_e2e_if_no_oracle",
                "tap_oracle_create_params",
                "tap_oracle_settings_overrides",
            ),
            ".utilities": ("TestsFlextTapOracleUtilities", "u"),
            "flext_tap_oracle": ("FlextTapOracleConstants",),
            "flext_tests": (
                "FlextTestsConstants",
                "d",
                "e",
                "h",
                "r",
                "td",
                "tf",
                "tk",
                "tm",
                "tv",
                "x",
            ),
            "typing": ("Final",),
        }),
        alias_groups=MappingProxyType({}),
        sort_keys=False,
    )
)

install_lazy_exports(__name__, globals(), _LAZY_IMPORTS, public_exports=__all__)
