# AUTO-GENERATED FILE — Regenerate with: make gen
"""Tests package.

Copyright (c) 2026 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from types import MappingProxyType
from typing import TYPE_CHECKING

from flext_core import build_lazy_import_map, install_lazy_exports

if TYPE_CHECKING:
    from flext_db_oracle import e
    from flext_tests import api, d, h, r, td, tf, tk, tm, x

    from tests import unit
    from tests.base import TestsFlextTapOracleServiceBase, s
    from tests.constants import TestsFlextTapOracleConstants, c
    from tests.models import TestsFlextTapOracleModels, m
    from tests.protocols import TestsFlextTapOracleProtocols, p
    from tests.settings import TestsFlextTapOracleSettings
    from tests.typings import TestsFlextTapOracleTypes, t
    from tests.utilities import TestsFlextTapOracleUtilities, u


__all__: tuple[str, ...] = (
    "TestsFlextTapOracleConstants",
    "TestsFlextTapOracleModels",
    "TestsFlextTapOracleProtocols",
    "TestsFlextTapOracleServiceBase",
    "TestsFlextTapOracleSettings",
    "TestsFlextTapOracleTypes",
    "TestsFlextTapOracleUtilities",
    "api",
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
            "flext_db_oracle": ("e",),
            "flext_tests": ("api", "d", "h", "r", "td", "tf", "tk", "tm", "x"),
        }),
        alias_groups=MappingProxyType({}),
        sort_keys=False,
    ),
)

install_lazy_exports(__name__, globals(), _LAZY_IMPORTS, public_exports=__all__)
