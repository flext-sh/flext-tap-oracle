# AUTO-GENERATED FILE — DO NOT EDIT MANUALLY.
# Regenerate with: make gen
#
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
    from tests import (
        conftest,
        constants,
        models,
        protocols,
        test_enterprise_tap,
        typings,
        utilities,
    )
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
    "TestsFlextTapOracleConstants": ("tests.constants", "TestsFlextTapOracleConstants"),
    "TestsFlextTapOracleModels": ("tests.models", "TestsFlextTapOracleModels"),
    "TestsFlextTapOracleProtocols": ("tests.protocols", "TestsFlextTapOracleProtocols"),
    "TestsFlextTapOracleTypes": ("tests.typings", "TestsFlextTapOracleTypes"),
    "TestsFlextTapOracleUtilities": ("tests.utilities", "TestsFlextTapOracleUtilities"),
    "c": ("tests.constants", "TestsFlextTapOracleConstants"),
    "conftest": "tests.conftest",
    "constants": "tests.constants",
    "d": ("flext_core.decorators", "FlextDecorators"),
    "e": ("flext_core.exceptions", "FlextExceptions"),
    "h": ("flext_core.handlers", "FlextHandlers"),
    "m": ("tests.models", "TestsFlextTapOracleModels"),
    "models": "tests.models",
    "p": ("tests.protocols", "TestsFlextTapOracleProtocols"),
    "protocols": "tests.protocols",
    "r": ("flext_core.result", "FlextResult"),
    "s": ("flext_core.service", "FlextService"),
    "t": ("tests.typings", "TestsFlextTapOracleTypes"),
    "test_enterprise_tap": "tests.test_enterprise_tap",
    "typings": "tests.typings",
    "u": ("tests.utilities", "TestsFlextTapOracleUtilities"),
    "utilities": "tests.utilities",
    "x": ("flext_core.mixins", "FlextMixins"),
}

__all__ = [
    "TestsFlextTapOracleConstants",
    "TestsFlextTapOracleModels",
    "TestsFlextTapOracleProtocols",
    "TestsFlextTapOracleTypes",
    "TestsFlextTapOracleUtilities",
    "c",
    "conftest",
    "constants",
    "d",
    "e",
    "h",
    "m",
    "models",
    "p",
    "protocols",
    "r",
    "s",
    "t",
    "test_enterprise_tap",
    "typings",
    "u",
    "utilities",
    "x",
]


install_lazy_exports(__name__, globals(), _LAZY_IMPORTS)
