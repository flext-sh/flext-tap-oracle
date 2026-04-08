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
    from tests.conftest import pytest_configure, pytest_plugins

    constants = _tests_constants
    import tests.models as _tests_models
    from tests.constants import (
        FlextTapOracleTestConstants,
        FlextTapOracleTestConstants as c,
    )

    models = _tests_models
    import tests.protocols as _tests_protocols
    from tests.models import FlextTapOracleTestModels, FlextTapOracleTestModels as m

    protocols = _tests_protocols
    import tests.test_enterprise_tap as _tests_test_enterprise_tap
    from tests.protocols import (
        FlextTapOracleTestProtocols,
        FlextTapOracleTestProtocols as p,
    )

    test_enterprise_tap = _tests_test_enterprise_tap
    import tests.typings as _tests_typings

    typings = _tests_typings
    import tests.utilities as _tests_utilities
    from tests.typings import FlextTapOracleTestTypes, FlextTapOracleTestTypes as t

    utilities = _tests_utilities
    from flext_core.decorators import FlextDecorators as d
    from flext_core.exceptions import FlextExceptions as e
    from flext_core.handlers import FlextHandlers as h
    from flext_core.mixins import FlextMixins as x
    from flext_core.result import FlextResult as r
    from flext_core.service import FlextService as s
    from tests.utilities import (
        FlextTapOracleTestUtilities,
        FlextTapOracleTestUtilities as u,
    )
_LAZY_IMPORTS = {
    "FlextTapOracleTestConstants": ("tests.constants", "FlextTapOracleTestConstants"),
    "FlextTapOracleTestModels": ("tests.models", "FlextTapOracleTestModels"),
    "FlextTapOracleTestProtocols": ("tests.protocols", "FlextTapOracleTestProtocols"),
    "FlextTapOracleTestTypes": ("tests.typings", "FlextTapOracleTestTypes"),
    "FlextTapOracleTestUtilities": ("tests.utilities", "FlextTapOracleTestUtilities"),
    "c": ("tests.constants", "FlextTapOracleTestConstants"),
    "conftest": "tests.conftest",
    "constants": "tests.constants",
    "d": ("flext_core.decorators", "FlextDecorators"),
    "e": ("flext_core.exceptions", "FlextExceptions"),
    "h": ("flext_core.handlers", "FlextHandlers"),
    "m": ("tests.models", "FlextTapOracleTestModels"),
    "models": "tests.models",
    "p": ("tests.protocols", "FlextTapOracleTestProtocols"),
    "protocols": "tests.protocols",
    "pytest_configure": ("tests.conftest", "pytest_configure"),
    "pytest_plugins": ("tests.conftest", "pytest_plugins"),
    "r": ("flext_core.result", "FlextResult"),
    "s": ("flext_core.service", "FlextService"),
    "t": ("tests.typings", "FlextTapOracleTestTypes"),
    "test_enterprise_tap": "tests.test_enterprise_tap",
    "typings": "tests.typings",
    "u": ("tests.utilities", "FlextTapOracleTestUtilities"),
    "utilities": "tests.utilities",
    "x": ("flext_core.mixins", "FlextMixins"),
}

__all__ = [
    "FlextTapOracleTestConstants",
    "FlextTapOracleTestModels",
    "FlextTapOracleTestProtocols",
    "FlextTapOracleTestTypes",
    "FlextTapOracleTestUtilities",
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
    "pytest_configure",
    "pytest_plugins",
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
