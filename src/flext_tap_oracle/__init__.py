# AUTO-GENERATED FILE — Regenerate with: make gen
"""Flext Tap Oracle package."""

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
    ("._utilities",),
    {
        "FlextTapOracleCli": ".tap",
        "FlextTapOracleConstants": ".constants",
        "FlextTapOracleDiscoverCommand": ".tap",
        "FlextTapOracleModels": ".models",
        "FlextTapOracleProtocols": ".protocols",
        "FlextTapOracleService": ".api",
        "FlextTapOracleSettings": ".settings",
        "FlextTapOracleStreams": ".streams",
        "FlextTapOracleSyncCommand": ".tap",
        "FlextTapOracleTypes": ".typings",
        "FlextTapOracleUtilities": ".utilities",
        "__author__": ".__version__",
        "__author_email__": ".__version__",
        "__description__": ".__version__",
        "__license__": ".__version__",
        "__title__": ".__version__",
        "__url__": ".__version__",
        "__version__": ".__version__",
        "__version_info__": ".__version__",
        "c": (".constants", "FlextTapOracleConstants"),
        "cli_api": ".tap",
        "d": ("flext_core.decorators", "FlextDecorators"),
        "e": ("flext_core.exceptions", "FlextExceptions"),
        "h": ("flext_core.handlers", "FlextHandlers"),
        "m": (".models", "FlextTapOracleModels"),
        "p": (".protocols", "FlextTapOracleProtocols"),
        "r": ("flext_core.result", "FlextResult"),
        "run_cli": ".tap",
        "s": (".api", "FlextTapOracleService"),
        "t": (".typings", "FlextTapOracleTypes"),
        "u": (".utilities", "FlextTapOracleUtilities"),
        "x": ("flext_core.mixins", "FlextMixins"),
    },
    exclude_names=(
        "cleanup_submodule_namespace",
        "install_lazy_exports",
        "lazy_getattr",
        "logger",
        "merge_lazy_imports",
        "output",
        "output_reporting",
    ),
    module_name=__name__,
)

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
