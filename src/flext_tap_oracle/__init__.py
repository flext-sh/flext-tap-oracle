# AUTO-GENERATED FILE — DO NOT EDIT MANUALLY.
# Regenerate with: make gen
#
"""FLEXT Tap Oracle - Oracle Database Singer Tap for FLEXT ecosystem.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from collections.abc import Mapping, Sequence
from typing import TYPE_CHECKING as _TYPE_CHECKING

from flext_core.lazy import install_lazy_exports, merge_lazy_imports

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

if _TYPE_CHECKING:
    from flext_core import FlextTypes
    from flext_db_oracle import d, e, h, r, s, x

    from flext_tap_oracle import (
        _utilities,
        constants,
        models,
        protocols,
        settings,
        streams,
        tap,
        typings,
        utilities,
    )
    from flext_tap_oracle._utilities import (
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

_LAZY_IMPORTS: Mapping[str, str | Sequence[str]] = merge_lazy_imports(
    ("flext_tap_oracle._utilities",),
    {
        "FlextTapOracleCli": "flext_tap_oracle.tap",
        "FlextTapOracleConstants": "flext_tap_oracle.constants",
        "FlextTapOracleDiscoverCommand": "flext_tap_oracle.tap",
        "FlextTapOracleModels": "flext_tap_oracle.models",
        "FlextTapOracleProtocols": "flext_tap_oracle.protocols",
        "FlextTapOracleSettings": "flext_tap_oracle.settings",
        "FlextTapOracleStreams": "flext_tap_oracle.streams",
        "FlextTapOracleSyncCommand": "flext_tap_oracle.tap",
        "FlextTapOracleTypes": "flext_tap_oracle.typings",
        "FlextTapOracleUtilities": "flext_tap_oracle.utilities",
        "_utilities": "flext_tap_oracle._utilities",
        "c": ("flext_tap_oracle.constants", "FlextTapOracleConstants"),
        "cli_api": "flext_tap_oracle.tap",
        "constants": "flext_tap_oracle.constants",
        "d": "flext_db_oracle",
        "e": "flext_db_oracle",
        "h": "flext_db_oracle",
        "logger": "flext_tap_oracle.tap",
        "m": ("flext_tap_oracle.models", "FlextTapOracleModels"),
        "main": "flext_tap_oracle.tap",
        "models": "flext_tap_oracle.models",
        "p": ("flext_tap_oracle.protocols", "FlextTapOracleProtocols"),
        "protocols": "flext_tap_oracle.protocols",
        "r": "flext_db_oracle",
        "run_cli": "flext_tap_oracle.tap",
        "s": "flext_db_oracle",
        "settings": "flext_tap_oracle.settings",
        "streams": "flext_tap_oracle.streams",
        "t": ("flext_tap_oracle.typings", "FlextTapOracleTypes"),
        "tap": "flext_tap_oracle.tap",
        "typings": "flext_tap_oracle.typings",
        "u": ("flext_tap_oracle.utilities", "FlextTapOracleUtilities"),
        "utilities": "flext_tap_oracle.utilities",
        "x": "flext_db_oracle",
    },
)


install_lazy_exports(
    __name__,
    globals(),
    _LAZY_IMPORTS,
    [
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
