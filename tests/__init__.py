# AUTO-GENERATED FILE — DO NOT EDIT MANUALLY.
# Regenerate with: make gen
#
"""Tests package."""

from __future__ import annotations

import typing as _t

from flext_core.lazy import install_lazy_exports

if _t.TYPE_CHECKING:
    import tests.conftest as _tests_conftest

    conftest = _tests_conftest
    import tests.constants as _tests_constants

    constants = _tests_constants
    import tests.models as _tests_models
    from tests.constants import (
        TestsFlextTapOracleConstants,
        TestsFlextTapOracleConstants as c,
    )

    models = _tests_models
    import tests.protocols as _tests_protocols
    from tests.models import TestsFlextTapOracleModels, TestsFlextTapOracleModels as m

    protocols = _tests_protocols
    import tests.test_enterprise_tap as _tests_test_enterprise_tap
    from tests.protocols import (
        TestsFlextTapOracleProtocols,
        TestsFlextTapOracleProtocols as p,
    )

    test_enterprise_tap = _tests_test_enterprise_tap
    import tests.typings as _tests_typings

    typings = _tests_typings
    import tests.utilities as _tests_utilities
    from tests.typings import TestsFlextTapOracleTypes, TestsFlextTapOracleTypes as t

    utilities = _tests_utilities
    from flext_core.decorators import FlextDecorators as d
    from flext_core.exceptions import FlextExceptions as e
    from flext_core.handlers import FlextHandlers as h
    from flext_core.mixins import FlextMixins as x
    from flext_core.result import FlextResult as r
    from flext_core.service import FlextService as s
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
