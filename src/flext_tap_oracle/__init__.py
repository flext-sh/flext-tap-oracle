# AUTO-GENERATED FILE — DO NOT EDIT MANUALLY.
# Regenerate with: make gen
#
"""Flext tap oracle package."""

from __future__ import annotations

import typing as _t

from flext_core.decorators import FlextDecorators as d
from flext_core.exceptions import FlextExceptions as e
from flext_core.handlers import FlextHandlers as h
from flext_core.lazy import install_lazy_exports, merge_lazy_imports
from flext_core.mixins import FlextMixins as x
from flext_core.result import FlextResult as r
from flext_tap_oracle.__version__ import *
from flext_tap_oracle.__version__ import (
    __author__,
    __author_email__,
    __description__,
    __license__,
    __title__,
    __url__,
    __version__,
    __version_info__,
)

if _t.TYPE_CHECKING:
    import flext_tap_oracle._utilities as _flext_tap_oracle__utilities

    _utilities = _flext_tap_oracle__utilities
    import flext_tap_oracle.api as _flext_tap_oracle_api

    api = _flext_tap_oracle_api
    import flext_tap_oracle.constants as _flext_tap_oracle_constants

    constants = _flext_tap_oracle_constants
    import flext_tap_oracle.models as _flext_tap_oracle_models

    models = _flext_tap_oracle_models
    import flext_tap_oracle.protocols as _flext_tap_oracle_protocols

    protocols = _flext_tap_oracle_protocols
    import flext_tap_oracle.settings as _flext_tap_oracle_settings

    settings = _flext_tap_oracle_settings
    import flext_tap_oracle.streams as _flext_tap_oracle_streams

    streams = _flext_tap_oracle_streams
    import flext_tap_oracle.tap as _flext_tap_oracle_tap

    tap = _flext_tap_oracle_tap
    import flext_tap_oracle.typings as _flext_tap_oracle_typings

    typings = _flext_tap_oracle_typings
    import flext_tap_oracle.utilities as _flext_tap_oracle_utilities

    utilities = _flext_tap_oracle_utilities

    _ = (
        FlextOracleConnectionTestService,
        FlextOracleDiscoveryService,
        FlextOracleTableFilterService,
        FlextOracleTapService,
        FlextTapOracleCli,
        FlextTapOracleConstants,
        FlextTapOracleDiscoverCommand,
        FlextTapOracleModels,
        FlextTapOracleProtocols,
        FlextTapOracleService,
        FlextTapOracleSettings,
        FlextTapOracleStreams,
        FlextTapOracleSyncCommand,
        FlextTapOracleTypes,
        FlextTapOracleUtilities,
        FlextTapOracleUtilitiesClientMixin,
        __author__,
        __author_email__,
        __description__,
        __license__,
        __title__,
        __url__,
        __version__,
        __version_info__,
        _utilities,
        api,
        c,
        cli_api,
        constants,
        d,
        e,
        h,
        logger,
        m,
        main,
        models,
        p,
        protocols,
        r,
        run_cli,
        s,
        settings,
        streams,
        t,
        tap,
        typings,
        u,
        utilities,
        x,
    )
_LAZY_IMPORTS = merge_lazy_imports(
    ("flext_tap_oracle._utilities",),
    {
        "FlextTapOracleCli": "flext_tap_oracle.tap",
        "FlextTapOracleConstants": "flext_tap_oracle.constants",
        "FlextTapOracleDiscoverCommand": "flext_tap_oracle.tap",
        "FlextTapOracleModels": "flext_tap_oracle.models",
        "FlextTapOracleProtocols": "flext_tap_oracle.protocols",
        "FlextTapOracleService": "flext_tap_oracle.api",
        "FlextTapOracleSettings": "flext_tap_oracle.settings",
        "FlextTapOracleStreams": "flext_tap_oracle.streams",
        "FlextTapOracleSyncCommand": "flext_tap_oracle.tap",
        "FlextTapOracleTypes": "flext_tap_oracle.typings",
        "FlextTapOracleUtilities": "flext_tap_oracle.utilities",
        "__author__": "flext_tap_oracle.__version__",
        "__author_email__": "flext_tap_oracle.__version__",
        "__description__": "flext_tap_oracle.__version__",
        "__license__": "flext_tap_oracle.__version__",
        "__title__": "flext_tap_oracle.__version__",
        "__url__": "flext_tap_oracle.__version__",
        "__version__": "flext_tap_oracle.__version__",
        "__version_info__": "flext_tap_oracle.__version__",
        "_utilities": "flext_tap_oracle._utilities",
        "api": "flext_tap_oracle.api",
        "c": ("flext_tap_oracle.constants", "FlextTapOracleConstants"),
        "cli_api": "flext_tap_oracle.tap",
        "constants": "flext_tap_oracle.constants",
        "d": ("flext_core.decorators", "FlextDecorators"),
        "e": ("flext_core.exceptions", "FlextExceptions"),
        "h": ("flext_core.handlers", "FlextHandlers"),
        "logger": "flext_tap_oracle.tap",
        "m": ("flext_tap_oracle.models", "FlextTapOracleModels"),
        "main": "flext_tap_oracle.tap",
        "models": "flext_tap_oracle.models",
        "p": ("flext_tap_oracle.protocols", "FlextTapOracleProtocols"),
        "protocols": "flext_tap_oracle.protocols",
        "r": ("flext_core.result", "FlextResult"),
        "run_cli": "flext_tap_oracle.tap",
        "s": ("flext_tap_oracle.api", "FlextTapOracleService"),
        "settings": "flext_tap_oracle.settings",
        "streams": "flext_tap_oracle.streams",
        "t": ("flext_tap_oracle.typings", "FlextTapOracleTypes"),
        "tap": "flext_tap_oracle.tap",
        "typings": "flext_tap_oracle.typings",
        "u": ("flext_tap_oracle.utilities", "FlextTapOracleUtilities"),
        "utilities": "flext_tap_oracle.utilities",
        "x": ("flext_core.mixins", "FlextMixins"),
    },
)

__all__ = [
    "FlextOracleConnectionTestService",
    "FlextOracleDiscoveryService",
    "FlextOracleTableFilterService",
    "FlextOracleTapService",
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
    "_utilities",
    "api",
    "c",
    "cli_api",
    "constants",
    "d",
    "e",
    "h",
    "logger",
    "m",
    "main",
    "models",
    "p",
    "protocols",
    "r",
    "run_cli",
    "s",
    "settings",
    "streams",
    "t",
    "tap",
    "typings",
    "u",
    "utilities",
    "x",
]


install_lazy_exports(__name__, globals(), _LAZY_IMPORTS)
