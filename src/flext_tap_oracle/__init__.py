# AUTO-GENERATED FILE — DO NOT EDIT MANUALLY.
# Regenerate with: make gen
#
"""Flext tap oracle package."""

from __future__ import annotations

import typing as _t

from flext_core.lazy import install_lazy_exports, merge_lazy_imports
from flext_tap_oracle.__version__ import *

if _t.TYPE_CHECKING:
    from flext_core.decorators import FlextDecorators as d
    from flext_core.exceptions import FlextExceptions as e
    from flext_core.handlers import FlextHandlers as h
    from flext_core.mixins import FlextMixins as x
    from flext_core.result import FlextResult as r
    from flext_tap_oracle._utilities.client import FlextTapOracleUtilitiesClientMixin
    from flext_tap_oracle.api import FlextTapOracleService, FlextTapOracleService as s
    from flext_tap_oracle.constants import (
        FlextTapOracleConstants,
        FlextTapOracleConstants as c,
    )
    from flext_tap_oracle.models import FlextTapOracleModels, FlextTapOracleModels as m
    from flext_tap_oracle.protocols import (
        FlextTapOracleProtocols,
        FlextTapOracleProtocols as p,
    )
    from flext_tap_oracle.settings import FlextTapOracleSettings
    from flext_tap_oracle.streams import FlextTapOracleStreams
    from flext_tap_oracle.tap import (
        FlextTapOracleCli,
        FlextTapOracleDiscoverCommand,
        FlextTapOracleSyncCommand,
        cli_api,
        run_cli,
    )
    from flext_tap_oracle.typings import FlextTapOracleTypes, FlextTapOracleTypes as t
    from flext_tap_oracle.utilities import (
        FlextTapOracleUtilities,
        FlextTapOracleUtilities as u,
    )
_LAZY_IMPORTS = merge_lazy_imports(
    ("flext_tap_oracle._utilities",),
    {
        "FlextTapOracleCli": ("flext_tap_oracle.tap", "FlextTapOracleCli"),
        "FlextTapOracleConstants": (
            "flext_tap_oracle.constants",
            "FlextTapOracleConstants",
        ),
        "FlextTapOracleDiscoverCommand": (
            "flext_tap_oracle.tap",
            "FlextTapOracleDiscoverCommand",
        ),
        "FlextTapOracleModels": ("flext_tap_oracle.models", "FlextTapOracleModels"),
        "FlextTapOracleProtocols": (
            "flext_tap_oracle.protocols",
            "FlextTapOracleProtocols",
        ),
        "FlextTapOracleService": ("flext_tap_oracle.api", "FlextTapOracleService"),
        "FlextTapOracleSettings": (
            "flext_tap_oracle.settings",
            "FlextTapOracleSettings",
        ),
        "FlextTapOracleStreams": ("flext_tap_oracle.streams", "FlextTapOracleStreams"),
        "FlextTapOracleSyncCommand": (
            "flext_tap_oracle.tap",
            "FlextTapOracleSyncCommand",
        ),
        "FlextTapOracleTypes": ("flext_tap_oracle.typings", "FlextTapOracleTypes"),
        "FlextTapOracleUtilities": (
            "flext_tap_oracle.utilities",
            "FlextTapOracleUtilities",
        ),
        "__author__": ("flext_tap_oracle.__version__", "__author__"),
        "__author_email__": ("flext_tap_oracle.__version__", "__author_email__"),
        "__description__": ("flext_tap_oracle.__version__", "__description__"),
        "__license__": ("flext_tap_oracle.__version__", "__license__"),
        "__title__": ("flext_tap_oracle.__version__", "__title__"),
        "__url__": ("flext_tap_oracle.__version__", "__url__"),
        "__version__": ("flext_tap_oracle.__version__", "__version__"),
        "__version_info__": ("flext_tap_oracle.__version__", "__version_info__"),
        "c": ("flext_tap_oracle.constants", "FlextTapOracleConstants"),
        "cli_api": ("flext_tap_oracle.tap", "cli_api"),
        "d": ("flext_core.decorators", "FlextDecorators"),
        "e": ("flext_core.exceptions", "FlextExceptions"),
        "h": ("flext_core.handlers", "FlextHandlers"),
        "m": ("flext_tap_oracle.models", "FlextTapOracleModels"),
        "p": ("flext_tap_oracle.protocols", "FlextTapOracleProtocols"),
        "r": ("flext_core.result", "FlextResult"),
        "run_cli": ("flext_tap_oracle.tap", "run_cli"),
        "s": ("flext_tap_oracle.api", "FlextTapOracleService"),
        "t": ("flext_tap_oracle.typings", "FlextTapOracleTypes"),
        "u": ("flext_tap_oracle.utilities", "FlextTapOracleUtilities"),
        "x": ("flext_core.mixins", "FlextMixins"),
    },
)
_ = _LAZY_IMPORTS.pop("cleanup_submodule_namespace", None)
_ = _LAZY_IMPORTS.pop("install_lazy_exports", None)
_ = _LAZY_IMPORTS.pop("lazy_getattr", None)
_ = _LAZY_IMPORTS.pop("logger", None)
_ = _LAZY_IMPORTS.pop("merge_lazy_imports", None)
_ = _LAZY_IMPORTS.pop("output", None)
_ = _LAZY_IMPORTS.pop("output_reporting", None)

__all__ = [
    "FlextTapOracleCli",
    "FlextTapOracleConstants",
    "FlextTapOracleDiscoverCommand",
    "FlextTapOracleModels",
    "FlextTapOracleProtocols",
    "FlextTapOracleService",
    "FlextTapOracleSettings",
    "FlextTapOracleStreams",
    "FlextTapOracleSyncCommand",
    "FlextTapOracleTypes",
    "FlextTapOracleUtilities",
    "FlextTapOracleUtilitiesClientMixin",
    "__author__",
    "__author_email__",
    "__description__",
    "__license__",
    "__title__",
    "__url__",
    "__version__",
    "__version_info__",
    "c",
    "cli_api",
    "d",
    "e",
    "h",
    "m",
    "p",
    "r",
    "run_cli",
    "s",
    "t",
    "u",
    "x",
]


install_lazy_exports(__name__, globals(), _LAZY_IMPORTS)
