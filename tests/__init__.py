# AUTO-GENERATED FILE — Regenerate with: make gen
"""Tests package."""

from __future__ import annotations

from types import MappingProxyType
from typing import TYPE_CHECKING

from flext_core.lazy import build_lazy_import_map, install_lazy_exports

if TYPE_CHECKING:
    from flext_cli import cli
    from flext_db_oracle import db_oracle, e
    from flext_infra import docs_main, infra, main
    from flext_meltano import meltano
    from flext_tests import (
        active_rules,
        api,
        config,
        discover_repository_root,
        install_local_packages,
        load_infra_report,
        settings,
        split_csv,
        td,
        tf,
        tk,
        tm,
        tv,
    )
    from pydantic_core import from_json, to_json, to_jsonable_python

    from flext_core import core, d, h, lazy_attribute, r, x
    from flext_tap_oracle import tap_oracle

    from . import unit
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
    from .utilities import (
        TestsFlextTapOracleUtilities,
        TestsFlextTapOracleUtilities as u,
    )
__all__: tuple[str, ...] = (
    "TestsFlextTapOracleConstants",
    "TestsFlextTapOracleModels",
    "TestsFlextTapOracleProtocols",
    "TestsFlextTapOracleServiceBase",
    "TestsFlextTapOracleSettings",
    "TestsFlextTapOracleTypes",
    "TestsFlextTapOracleUtilities",
    "active_rules",
    "api",
    "c",
    "cli",
    "config",
    "core",
    "d",
    "db_oracle",
    "discover_repository_root",
    "docs_main",
    "e",
    "from_json",
    "h",
    "infra",
    "install_local_packages",
    "lazy_attribute",
    "load_infra_report",
    "m",
    "main",
    "meltano",
    "p",
    "r",
    "s",
    "settings",
    "split_csv",
    "t",
    "tap_oracle",
    "td",
    "tf",
    "tk",
    "tm",
    "to_json",
    "to_jsonable_python",
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
            ".utilities": ("TestsFlextTapOracleUtilities", "u"),
            "flext_cli": ("cli",),
            "flext_core": ("core", "d", "h", "lazy_attribute", "r", "x"),
            "flext_db_oracle": ("db_oracle", "e"),
            "flext_infra": ("docs_main", "infra", "main"),
            "flext_meltano": ("meltano",),
            "flext_tap_oracle": ("tap_oracle",),
            "flext_tests": (
                "active_rules",
                "api",
                "config",
                "discover_repository_root",
                "install_local_packages",
                "load_infra_report",
                "settings",
                "split_csv",
                "td",
                "tf",
                "tk",
                "tm",
                "tv",
            ),
            "pydantic_core": ("from_json", "to_json", "to_jsonable_python"),
        }),
        alias_groups=MappingProxyType({}),
        sort_keys=False,
    )
)

install_lazy_exports(__name__, globals(), _LAZY_IMPORTS, public_exports=__all__)
