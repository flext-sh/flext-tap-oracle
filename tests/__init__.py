# AUTO-GENERATED FILE — Regenerate with: make gen
"""Tests package."""

from __future__ import annotations

import typing as _t

from flext_core.lazy import build_lazy_import_map, install_lazy_exports

if _t.TYPE_CHECKING:
    from flext_tests import td, tf, tk, tm, tv

    from flext_tap_oracle import d, e, h, r, s, x
    from tests.constants import TestsFlextTapOracleConstants, c
    from tests.models import TestsFlextTapOracleModels, m
    from tests.protocols import TestsFlextTapOracleProtocols, p
    from tests.typings import TestsFlextTapOracleTypes, t
    from tests.utilities import TestsFlextTapOracleUtilities, u
_LAZY_IMPORTS = build_lazy_import_map(
    {
        ".constants": (
            "TestsFlextTapOracleConstants",
            "c",
        ),
        ".models": (
            "TestsFlextTapOracleModels",
            "m",
        ),
        ".protocols": (
            "TestsFlextTapOracleProtocols",
            "p",
        ),
        ".typings": (
            "TestsFlextTapOracleTypes",
            "t",
        ),
        ".utilities": (
            "TestsFlextTapOracleUtilities",
            "u",
        ),
        "flext_tap_oracle": (
            "d",
            "e",
            "h",
            "r",
            "s",
            "x",
        ),
        "flext_tests": (
            "td",
            "tf",
            "tk",
            "tm",
            "tv",
        ),
    },
)


install_lazy_exports(__name__, globals(), _LAZY_IMPORTS)

__all__: list[str] = [
    "TestsFlextTapOracleConstants",
    "TestsFlextTapOracleModels",
    "TestsFlextTapOracleProtocols",
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
    "x",
]
