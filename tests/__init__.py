# AUTO-GENERATED FILE — Regenerate with: make gen
"""Tests package."""

from __future__ import annotations

from types import MappingProxyType
from typing import TYPE_CHECKING

from flext_core.lazy import build_lazy_import_map, install_lazy_exports

if TYPE_CHECKING:
    from flext_tap_oracle import FlextTapOracleConstants
    from flext_tests import FlextTestsConstants, d, e, h, r, td, tf, tk, tm, tv, x

    from . import unit as unit
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
        }),
        alias_groups=MappingProxyType({}),
        sort_keys=False,
    )
)

install_lazy_exports(__name__, globals(), _LAZY_IMPORTS, public_exports=__all__)
