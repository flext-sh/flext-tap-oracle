# AUTO-GENERATED FILE — DO NOT EDIT MANUALLY.
# Regenerate with: make gen
#
"""FLEXT Tap Oracle - Oracle Database Singer Tap for FLEXT ecosystem.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from collections.abc import Mapping, MutableMapping, Sequence
from typing import TYPE_CHECKING

from flext_core.lazy import cleanup_submodule_namespace, lazy_getattr

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

if TYPE_CHECKING:
    from flext_core import FlextTypes
    from flext_db_oracle import d, e, h, r, s, x

    from flext_tap_oracle import (
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
        logger,
        main,
        run_cli,
    )
    from flext_tap_oracle.typings import FlextTapOracleTypes, FlextTapOracleTypes as t
    from flext_tap_oracle.utilities import (
        FlextTapOracleUtilities,
        FlextTapOracleUtilities as u,
    )

_LAZY_IMPORTS: Mapping[str, Sequence[str]] = {
    "FlextOracleConnectionTestService": [
        "flext_tap_oracle._utilities._client",
        "FlextOracleConnectionTestService",
    ],
    "FlextOracleDiscoveryService": [
        "flext_tap_oracle._utilities._client",
        "FlextOracleDiscoveryService",
    ],
    "FlextOracleTableFilterService": [
        "flext_tap_oracle._utilities._client",
        "FlextOracleTableFilterService",
    ],
    "FlextOracleTapService": [
        "flext_tap_oracle._utilities._client",
        "FlextOracleTapService",
    ],
    "FlextTapOracleCli": ["flext_tap_oracle.tap", "FlextTapOracleCli"],
    "FlextTapOracleConstants": [
        "flext_tap_oracle.constants",
        "FlextTapOracleConstants",
    ],
    "FlextTapOracleDiscoverCommand": [
        "flext_tap_oracle.tap",
        "FlextTapOracleDiscoverCommand",
    ],
    "FlextTapOracleModels": ["flext_tap_oracle.models", "FlextTapOracleModels"],
    "FlextTapOracleProtocols": [
        "flext_tap_oracle.protocols",
        "FlextTapOracleProtocols",
    ],
    "FlextTapOracleSettings": ["flext_tap_oracle.settings", "FlextTapOracleSettings"],
    "FlextTapOracleStreams": ["flext_tap_oracle.streams", "FlextTapOracleStreams"],
    "FlextTapOracleSyncCommand": ["flext_tap_oracle.tap", "FlextTapOracleSyncCommand"],
    "FlextTapOracleTypes": ["flext_tap_oracle.typings", "FlextTapOracleTypes"],
    "FlextTapOracleUtilities": [
        "flext_tap_oracle.utilities",
        "FlextTapOracleUtilities",
    ],
    "FlextTapOracleUtilitiesClientMixin": [
        "flext_tap_oracle._utilities._client",
        "FlextTapOracleUtilitiesClientMixin",
    ],
    "c": ["flext_tap_oracle.constants", "FlextTapOracleConstants"],
    "cli_api": ["flext_tap_oracle.tap", "cli_api"],
    "constants": ["flext_tap_oracle.constants", ""],
    "d": ["flext_db_oracle", "d"],
    "e": ["flext_db_oracle", "e"],
    "h": ["flext_db_oracle", "h"],
    "logger": ["flext_tap_oracle.tap", "logger"],
    "m": ["flext_tap_oracle.models", "FlextTapOracleModels"],
    "main": ["flext_tap_oracle.tap", "main"],
    "models": ["flext_tap_oracle.models", ""],
    "p": ["flext_tap_oracle.protocols", "FlextTapOracleProtocols"],
    "protocols": ["flext_tap_oracle.protocols", ""],
    "r": ["flext_db_oracle", "r"],
    "run_cli": ["flext_tap_oracle.tap", "run_cli"],
    "s": ["flext_db_oracle", "s"],
    "settings": ["flext_tap_oracle.settings", ""],
    "streams": ["flext_tap_oracle.streams", ""],
    "t": ["flext_tap_oracle.typings", "FlextTapOracleTypes"],
    "tap": ["flext_tap_oracle.tap", ""],
    "typings": ["flext_tap_oracle.typings", ""],
    "u": ["flext_tap_oracle.utilities", "FlextTapOracleUtilities"],
    "utilities": ["flext_tap_oracle.utilities", ""],
    "x": ["flext_db_oracle", "x"],
}

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


_LAZY_CACHE: MutableMapping[str, FlextTypes.ModuleExport] = {}


def __getattr__(name: str) -> FlextTypes.ModuleExport:
    """Lazy-load module attributes on first access (PEP 562).

    A local cache ``_LAZY_CACHE`` persists resolved objects across repeated
    accesses during process lifetime.

    Args:
        name: Attribute name requested by dir()/import.

    Returns:
        Lazy-loaded module export type.

    Raises:
        AttributeError: If attribute not registered.

    """
    if name in _LAZY_CACHE:
        return _LAZY_CACHE[name]

    value = lazy_getattr(name, _LAZY_IMPORTS, globals(), __name__)
    _LAZY_CACHE[name] = value
    return value


def __dir__() -> Sequence[str]:
    """Return list of available attributes for dir() and autocomplete.

    Returns:
        List of public names from module exports.

    """
    return sorted(__all__)


cleanup_submodule_namespace(__name__, _LAZY_IMPORTS)
