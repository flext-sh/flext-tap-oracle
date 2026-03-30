# AUTO-GENERATED FILE — DO NOT EDIT MANUALLY.
# Regenerate with: make gen
#
"""FLEXT Tap Oracle - Oracle Database Singer Tap for FLEXT ecosystem.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from collections.abc import Mapping, Sequence
from typing import TYPE_CHECKING

from flext_core.lazy import install_lazy_exports

from flext_tap_oracle.__version__ import (
    __author__ as __author__,
    __author_email__ as __author_email__,
    __description__ as __description__,
    __license__ as __license__,
    __title__ as __title__,
    __url__ as __url__,
    __version__ as __version__,
    __version_info__ as __version_info__,
)

if TYPE_CHECKING:
    from flext_db_oracle import d, e, h, r, s, x

    from flext_tap_oracle import (
        constants as constants,
        models as models,
        protocols as protocols,
        settings as settings,
        streams as streams,
        tap as tap,
        typings as typings,
        utilities as utilities,
    )
    from flext_tap_oracle._utilities._client import (
        FlextOracleConnectionTestService as FlextOracleConnectionTestService,
        FlextOracleDiscoveryService as FlextOracleDiscoveryService,
        FlextOracleTableFilterService as FlextOracleTableFilterService,
        FlextOracleTapService as FlextOracleTapService,
        FlextTapOracleUtilitiesClientMixin as FlextTapOracleUtilitiesClientMixin,
    )
    from flext_tap_oracle.constants import (
        FlextTapOracleConstants as FlextTapOracleConstants,
        FlextTapOracleConstants as c,
    )
    from flext_tap_oracle.models import (
        FlextTapOracleModels as FlextTapOracleModels,
        FlextTapOracleModels as m,
    )
    from flext_tap_oracle.protocols import (
        FlextTapOracleProtocols as FlextTapOracleProtocols,
        FlextTapOracleProtocols as p,
    )
    from flext_tap_oracle.settings import (
        FlextTapOracleSettings as FlextTapOracleSettings,
    )
    from flext_tap_oracle.streams import FlextTapOracleStreams as FlextTapOracleStreams
    from flext_tap_oracle.tap import (
        FlextTapOracleCli as FlextTapOracleCli,
        FlextTapOracleDiscoverCommand as FlextTapOracleDiscoverCommand,
        FlextTapOracleSyncCommand as FlextTapOracleSyncCommand,
        cli_api as cli_api,
        logger as logger,
        main as main,
        run_cli as run_cli,
    )
    from flext_tap_oracle.typings import (
        FlextTapOracleTypes as FlextTapOracleTypes,
        FlextTapOracleTypes as t,
    )
    from flext_tap_oracle.utilities import (
        FlextTapOracleUtilities as FlextTapOracleUtilities,
        FlextTapOracleUtilities as u,
    )

_LAZY_IMPORTS: Mapping[str, Sequence[str]] = {
    "FlextOracleConnectionTestService": ["flext_tap_oracle._utilities._client", "FlextOracleConnectionTestService"],
    "FlextOracleDiscoveryService": ["flext_tap_oracle._utilities._client", "FlextOracleDiscoveryService"],
    "FlextOracleTableFilterService": ["flext_tap_oracle._utilities._client", "FlextOracleTableFilterService"],
    "FlextOracleTapService": ["flext_tap_oracle._utilities._client", "FlextOracleTapService"],
    "FlextTapOracleCli": ["flext_tap_oracle.tap", "FlextTapOracleCli"],
    "FlextTapOracleConstants": ["flext_tap_oracle.constants", "FlextTapOracleConstants"],
    "FlextTapOracleDiscoverCommand": ["flext_tap_oracle.tap", "FlextTapOracleDiscoverCommand"],
    "FlextTapOracleModels": ["flext_tap_oracle.models", "FlextTapOracleModels"],
    "FlextTapOracleProtocols": ["flext_tap_oracle.protocols", "FlextTapOracleProtocols"],
    "FlextTapOracleSettings": ["flext_tap_oracle.settings", "FlextTapOracleSettings"],
    "FlextTapOracleStreams": ["flext_tap_oracle.streams", "FlextTapOracleStreams"],
    "FlextTapOracleSyncCommand": ["flext_tap_oracle.tap", "FlextTapOracleSyncCommand"],
    "FlextTapOracleTypes": ["flext_tap_oracle.typings", "FlextTapOracleTypes"],
    "FlextTapOracleUtilities": ["flext_tap_oracle.utilities", "FlextTapOracleUtilities"],
    "FlextTapOracleUtilitiesClientMixin": ["flext_tap_oracle._utilities._client", "FlextTapOracleUtilitiesClientMixin"],
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

_EXPORTS: Sequence[str] = [
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


install_lazy_exports(__name__, globals(), _LAZY_IMPORTS, _EXPORTS)
