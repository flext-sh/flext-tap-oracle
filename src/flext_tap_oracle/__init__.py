# AUTO-GENERATED FILE — Regenerate with: make gen
"""Flext Tap Oracle package."""

from __future__ import annotations

import typing as _t

from flext_core.lazy import (
    build_lazy_import_map,
    install_lazy_exports,
    merge_lazy_imports,
)
from flext_tap_oracle.__version__ import *

if _t.TYPE_CHECKING:
    from flext_core.decorators import d
    from flext_core.exceptions import e
    from flext_core.handlers import h
    from flext_core.mixins import x
    from flext_core.result import r
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
    build_lazy_import_map(
        {
            ".__version__": (
                "__author__",
                "__author_email__",
                "__description__",
                "__license__",
                "__title__",
                "__url__",
                "__version__",
                "__version_info__",
            ),
            ".api": ("FlextTapOracleService",),
            ".constants": ("FlextTapOracleConstants",),
            ".models": ("FlextTapOracleModels",),
            ".protocols": ("FlextTapOracleProtocols",),
            ".settings": ("FlextTapOracleSettings",),
            ".streams": ("FlextTapOracleStreams",),
            ".tap": (
                "FlextTapOracleCli",
                "FlextTapOracleDiscoverCommand",
                "FlextTapOracleSyncCommand",
                "cli_api",
                "run_cli",
            ),
            ".typings": ("FlextTapOracleTypes",),
            ".utilities": ("FlextTapOracleUtilities",),
            "flext_core.decorators": ("d",),
            "flext_core.exceptions": ("e",),
            "flext_core.handlers": ("h",),
            "flext_core.mixins": ("x",),
            "flext_core.result": ("r",),
        },
        alias_groups={
            ".api": (("s", "FlextTapOracleService"),),
            ".constants": (("c", "FlextTapOracleConstants"),),
            ".models": (("m", "FlextTapOracleModels"),),
            ".protocols": (("p", "FlextTapOracleProtocols"),),
            ".typings": (("t", "FlextTapOracleTypes"),),
            ".utilities": (("u", "FlextTapOracleUtilities"),),
        },
    ),
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
