# AUTO-GENERATED FILE — DO NOT EDIT MANUALLY.
# Regenerate with: make gen
#
"""Flext tap oracle package."""

from __future__ import annotations

from collections.abc import Mapping, Sequence
from typing import TYPE_CHECKING as _TYPE_CHECKING

from flext_core.lazy import install_lazy_exports
from flext_tap_oracle.__version__ import (
    __all__,
    __author__,
    __author_email__,
    __description__,
    __license__,
    __title__,
    __url__,
    __version__,
    __version_info__,
)

if _TYPE_CHECKING:
    from flext_core import FlextTypes
    from flext_core.decorators import FlextDecorators as d
    from flext_core.handlers import FlextHandlers as h
    from flext_core.mixins import FlextMixins as x
    from flext_core.result import FlextResult as r
    from flext_core.service import FlextService as s
    from flext_db_oracle.exceptions import FlextDbOracleExceptions as e
    from flext_tap_oracle import (
        api,
        constants,
        models,
        protocols,
        settings,
        streams,
        tap,
        typings,
        utilities,
    )
    from flext_tap_oracle._utilities._client import (
        FlextOracleConnectionTestService,
        FlextOracleDiscoveryService,
        FlextOracleTableFilterService,
        FlextOracleTapService,
        FlextTapOracleUtilitiesClientMixin,
    )
    from flext_tap_oracle.api import FlextTapOracleService
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
    from flext_tap_oracle.tap import FlextTapOracleDiscoverCommand, cli_api, logger
    from flext_tap_oracle.typings import FlextTapOracleTypes, FlextTapOracleTypes as t
    from flext_tap_oracle.utilities import (
        FlextTapOracleUtilities,
        FlextTapOracleUtilities as u,
    )

_LAZY_IMPORTS: FlextTypes.LazyImportIndex = {
    "FlextOracleConnectionTestService": "flext_tap_oracle._utilities._client",
    "FlextOracleDiscoveryService": "flext_tap_oracle._utilities._client",
    "FlextOracleTableFilterService": "flext_tap_oracle._utilities._client",
    "FlextOracleTapService": "flext_tap_oracle._utilities._client",
    "FlextTapOracleConstants": "flext_tap_oracle.constants",
    "FlextTapOracleDiscoverCommand": "flext_tap_oracle.tap",
    "FlextTapOracleModels": "flext_tap_oracle.models",
    "FlextTapOracleProtocols": "flext_tap_oracle.protocols",
    "FlextTapOracleService": "flext_tap_oracle.api",
    "FlextTapOracleSettings": "flext_tap_oracle.settings",
    "FlextTapOracleStreams": "flext_tap_oracle.streams",
    "FlextTapOracleTypes": "flext_tap_oracle.typings",
    "FlextTapOracleUtilities": "flext_tap_oracle.utilities",
    "FlextTapOracleUtilitiesClientMixin": "flext_tap_oracle._utilities._client",
    "api": "flext_tap_oracle.api",
    "c": ("flext_tap_oracle.constants", "FlextTapOracleConstants"),
    "cli_api": "flext_tap_oracle.tap",
    "constants": "flext_tap_oracle.constants",
    "d": ("flext_core.decorators", "FlextDecorators"),
    "e": ("flext_db_oracle.exceptions", "FlextDbOracleExceptions"),
    "h": ("flext_core.handlers", "FlextHandlers"),
    "logger": "flext_tap_oracle.tap",
    "m": ("flext_tap_oracle.models", "FlextTapOracleModels"),
    "models": "flext_tap_oracle.models",
    "p": ("flext_tap_oracle.protocols", "FlextTapOracleProtocols"),
    "protocols": "flext_tap_oracle.protocols",
    "r": ("flext_core.result", "FlextResult"),
    "s": ("flext_core.service", "FlextService"),
    "settings": "flext_tap_oracle.settings",
    "streams": "flext_tap_oracle.streams",
    "t": ("flext_tap_oracle.typings", "FlextTapOracleTypes"),
    "tap": "flext_tap_oracle.tap",
    "typings": "flext_tap_oracle.typings",
    "u": ("flext_tap_oracle.utilities", "FlextTapOracleUtilities"),
    "utilities": "flext_tap_oracle.utilities",
    "x": ("flext_core.mixins", "FlextMixins"),
}


install_lazy_exports(
    __name__,
    globals(),
    _LAZY_IMPORTS,
    [
        "__all__",
        "__author__",
        "__author_email__",
        "__description__",
        "__license__",
        "__title__",
        "__url__",
        "__version__",
        "__version_info__",
    ],
)
