# AUTO-GENERATED FILE — Regenerate with: make gen
"""Tests package."""

from __future__ import annotations

import typing as _t

from flext_core.lazy import build_lazy_import_map, install_lazy_exports

if _t.TYPE_CHECKING:
    from flext_core.decorators import d
    from flext_core.exceptions import e
    from flext_core.handlers import h
    from flext_core.mixins import x
    from flext_core.result import r
    from flext_core.service import s
    from tests.constants import (
        TestsFlextTapOracleConstants,
        TestsFlextTapOracleConstants as c,
    )
    from tests.models import TestsFlextTapOracleModels, TestsFlextTapOracleModels as m
    from tests.protocols import (
        TestsFlextTapOracleProtocols,
        TestsFlextTapOracleProtocols as p,
    )
    from tests.typings import TestsFlextTapOracleTypes, TestsFlextTapOracleTypes as t
    from tests.utilities import (
        TestsFlextTapOracleUtilities,
        TestsFlextTapOracleUtilities as u,
    )
_LAZY_IMPORTS = build_lazy_import_map(
    {
        ".constants": ("TestsFlextTapOracleConstants",),
        ".models": ("TestsFlextTapOracleModels",),
        ".protocols": ("TestsFlextTapOracleProtocols",),
        ".typings": ("TestsFlextTapOracleTypes",),
        ".utilities": ("TestsFlextTapOracleUtilities",),
        "flext_core.decorators": ("d",),
        "flext_core.exceptions": ("e",),
        "flext_core.handlers": ("h",),
        "flext_core.mixins": ("x",),
        "flext_core.result": ("r",),
        "flext_core.service": ("s",),
    },
    alias_groups={
        ".constants": (("c", "TestsFlextTapOracleConstants"),),
        ".models": (("m", "TestsFlextTapOracleModels"),),
        ".protocols": (("p", "TestsFlextTapOracleProtocols"),),
        ".typings": (("t", "TestsFlextTapOracleTypes"),),
        ".utilities": (("u", "TestsFlextTapOracleUtilities"),),
    },
)

__all__ = [
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
    "u",
    "x",
]


install_lazy_exports(__name__, globals(), _LAZY_IMPORTS)
