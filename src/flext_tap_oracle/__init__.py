# AUTO-GENERATED FILE — Regenerate with: make gen
"""Flext Tap Oracle package."""

from __future__ import annotations

from typing import TYPE_CHECKING

from flext_core.lazy import build_lazy_import_map, install_lazy_exports
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
    from flext_db_oracle import d, e, h, r, s, x

    from ._settings import FlextTapOracleSettings, settings
    from .api import FlextTapOracleService, tap_oracle
    from .constants import FlextTapOracleConstants, FlextTapOracleConstants as c
    from .models import FlextTapOracleModels, FlextTapOracleModels as m
    from .protocols import FlextTapOracleProtocols, FlextTapOracleProtocols as p
    from .tap import (
        FlextTapOracleCli,
        FlextTapOracleDiscoverCommand,
        FlextTapOracleSyncCommand,
    )
    from .typings import FlextTapOracleTypes, FlextTapOracleTypes as t
    from .utilities import FlextTapOracleUtilities, FlextTapOracleUtilities as u

    _ = (
        c,
        FlextTapOracleConstants,
        t,
        FlextTapOracleTypes,
        p,
        FlextTapOracleProtocols,
        m,
        FlextTapOracleModels,
        u,
        FlextTapOracleUtilities,
        d,
        e,
        h,
        r,
        s,
        x,
        FlextTapOracleSettings,
        settings,
        FlextTapOracleService,
        tap_oracle,
        FlextTapOracleCli,
        FlextTapOracleDiscoverCommand,
        FlextTapOracleSyncCommand,
    )


_LAZY_MODULES: dict[str, tuple[str, ...]] = {
    "._settings": (
        "FlextTapOracleSettings",
        "settings",
    ),
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
    "flext_db_oracle": (
        "d",
        "e",
        "h",
        "r",
        "s",
        "x",
    ),
}


_LAZY_ALIAS_GROUPS: dict[str, tuple[tuple[str, str], ...]] = {}


_LAZY_IMPORTS = build_lazy_import_map(
    _LAZY_MODULES,
    alias_groups=_LAZY_ALIAS_GROUPS,
    sort_keys=False,
)

_DIRECT_IMPORTS: tuple[str, ...] = (
    "FlextTapOracleCli",
    "FlextTapOracleConstants",
    "FlextTapOracleDiscoverCommand",
    "FlextTapOracleModels",
    "FlextTapOracleProtocols",
    "FlextTapOracleService",
    "FlextTapOracleSettings",
    "FlextTapOracleSyncCommand",
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
    "build_lazy_import_map",
    "c",
    "d",
    "e",
    "h",
    "install_lazy_exports",
    "m",
    "p",
    "r",
    "s",
    "settings",
    "t",
    "tap_oracle",
    "u",
    "x",
)

__all__: tuple[str, ...] = (
    "FlextTapOracleCli",
    "FlextTapOracleConstants",
    "FlextTapOracleDiscoverCommand",
    "FlextTapOracleModels",
    "FlextTapOracleProtocols",
    "FlextTapOracleService",
    "FlextTapOracleSettings",
    "FlextTapOracleSyncCommand",
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
    "d",
    "e",
    "h",
    "m",
    "p",
    "r",
    "s",
    "settings",
    "t",
    "tap_oracle",
    "u",
    "x",
)


install_lazy_exports(
    __name__,
    globals(),
    _LAZY_IMPORTS,
    public_exports=__all__,
)
