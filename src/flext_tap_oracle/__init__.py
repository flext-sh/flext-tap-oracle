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
    from flext_meltano import d, e, h, r, s, x

    from flext_tap_oracle._utilities.client import FlextTapOracleUtilitiesClientMixin
    from flext_tap_oracle.api import FlextTapOracleService, tap_oracle
    from flext_tap_oracle.constants import FlextTapOracleConstants, c
    from flext_tap_oracle.models import FlextTapOracleModels, m
    from flext_tap_oracle.protocols import FlextTapOracleProtocols, p
    from flext_tap_oracle.settings import FlextTapOracleSettings
    from flext_tap_oracle.streams import FlextTapOracleStreams
    from flext_tap_oracle.tap import (
        FlextTapOracleCli,
        FlextTapOracleDiscoverCommand,
        FlextTapOracleSyncCommand,
    )
    from flext_tap_oracle.typings import FlextTapOracleTypes, t
    from flext_tap_oracle.utilities import FlextTapOracleUtilities, u
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
            "._utilities.client": ("FlextTapOracleUtilitiesClientMixin",),
            ".api": (
                "FlextTapOracleService",
                "tap_oracle",
            ),
            ".constants": (
                "FlextTapOracleConstants",
                "c",
            ),
            ".models": (
                "FlextTapOracleModels",
                "m",
            ),
            ".protocols": (
                "FlextTapOracleProtocols",
                "p",
            ),
            ".settings": ("FlextTapOracleSettings",),
            ".streams": ("FlextTapOracleStreams",),
            ".tap": (
                "FlextTapOracleCli",
                "FlextTapOracleDiscoverCommand",
                "FlextTapOracleSyncCommand",
            ),
            ".typings": (
                "FlextTapOracleTypes",
                "t",
            ),
            ".utilities": (
                "FlextTapOracleUtilities",
                "u",
            ),
            "flext_meltano": (
                "d",
                "e",
                "h",
                "r",
                "s",
                "x",
            ),
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


install_lazy_exports(__name__, globals(), _LAZY_IMPORTS)

__all__: list[str] = [
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
    "d",
    "e",
    "h",
    "m",
    "p",
    "r",
    "s",
    "t",
    "tap_oracle",
    "u",
    "x",
]
