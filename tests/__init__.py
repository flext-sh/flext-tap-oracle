# AUTO-GENERATED FILE — Regenerate with: make gen
"""Tests package."""

from __future__ import annotations

import typing as _t

from flext_core.lazy import install_lazy_exports

if _t.TYPE_CHECKING:
    from flext_core.decorators import FlextDecorators as d
    from flext_core.exceptions import FlextExceptions as e
    from flext_core.handlers import FlextHandlers as h
    from flext_core.mixins import FlextMixins as x
    from flext_core.result import FlextResult as r
    from flext_core.service import FlextService as s
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
_LAZY_IMPORTS = {
    "TestsFlextTapOracleConstants": ".constants",
    "TestsFlextTapOracleModels": ".models",
    "TestsFlextTapOracleProtocols": ".protocols",
    "TestsFlextTapOracleTypes": ".typings",
    "TestsFlextTapOracleUtilities": ".utilities",
    "c": (".constants", "TestsFlextTapOracleConstants"),
    "d": ("flext_core.decorators", "FlextDecorators"),
    "e": ("flext_core.exceptions", "FlextExceptions"),
    "h": ("flext_core.handlers", "FlextHandlers"),
    "m": (".models", "TestsFlextTapOracleModels"),
    "p": (".protocols", "TestsFlextTapOracleProtocols"),
    "r": ("flext_core.result", "FlextResult"),
    "s": ("flext_core.service", "FlextService"),
    "t": (".typings", "TestsFlextTapOracleTypes"),
    "u": (".utilities", "TestsFlextTapOracleUtilities"),
    "x": ("flext_core.mixins", "FlextMixins"),
}

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
