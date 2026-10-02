# AUTO-GENERATED FILE — Regenerate with: make gen
"""Flext Tap Oracle package.

Copyright (c) 2026 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from types import MappingProxyType
from typing import TYPE_CHECKING

from flext_core import build_lazy_import_map, install_lazy_exports
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
    from flext_db_oracle import e
    from flext_meltano import d, h, r, s, x

    from flext_tap_oracle._config import FlextTapOracleConfig, config
    from flext_tap_oracle._settings import FlextTapOracleSettings, settings
    from flext_tap_oracle.api import FlextTapOracleService, tap_oracle
    from flext_tap_oracle.cli import main
    from flext_tap_oracle.constants import FlextTapOracleConstants, c
    from flext_tap_oracle.models import FlextTapOracleModels, m
    from flext_tap_oracle.protocols import FlextTapOracleProtocols, p
    from flext_tap_oracle.streams import FlextTapOracleStreams
    from flext_tap_oracle.typings import FlextTapOracleTypes, t
    from flext_tap_oracle.utilities import FlextTapOracleUtilities, u


__all__: tuple[str, ...] = (
    "FlextTapOracleConfig",
    "FlextTapOracleConstants",
    "FlextTapOracleModels",
    "FlextTapOracleProtocols",
    "FlextTapOracleService",
    "FlextTapOracleSettings",
    "FlextTapOracleStreams",
    "FlextTapOracleTypes",
    "FlextTapOracleUtilities",
    "__author__",
    "__author_email__",
    "__description__",
    "__license__",
    "__title__",
    "__url__",
    "__version__",
    "__version_info__",
    "c",
    "config",
    "d",
    "e",
    "h",
    "m",
    "main",
    "p",
    "r",
    "s",
    "settings",
    "t",
    "tap_oracle",
    "u",
    "x",
)

_LAZY_IMPORTS = MappingProxyType(
    build_lazy_import_map(
        MappingProxyType({
            "._config": ("FlextTapOracleConfig", "config"),
            "._settings": ("FlextTapOracleSettings", "settings"),
            ".api": ("FlextTapOracleService", "tap_oracle"),
            ".cli": ("main",),
            ".constants": ("FlextTapOracleConstants", "c"),
            ".models": ("FlextTapOracleModels", "m"),
            ".protocols": ("FlextTapOracleProtocols", "p"),
            ".streams": ("FlextTapOracleStreams",),
            ".typings": ("FlextTapOracleTypes", "t"),
            ".utilities": ("FlextTapOracleUtilities", "u"),
            "flext_db_oracle": ("e",),
            "flext_meltano": ("d", "h", "r", "s", "x"),
        }),
        alias_groups=MappingProxyType({}),
        sort_keys=False,
    ),
)

install_lazy_exports(__name__, globals(), _LAZY_IMPORTS, public_exports=__all__)
