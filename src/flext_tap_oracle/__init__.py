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
    from flext_db_oracle import d as d, e as e, h as h, r as r, s as s, x as x
    from flext_tap_oracle.api import (
        FlextTapOracleService as FlextTapOracleService,
        tap_oracle as tap_oracle,
    )
    from flext_tap_oracle.constants import (
        FlextTapOracleConstants as FlextTapOracleConstants,
        c as c,
    )
    from flext_tap_oracle.models import (
        FlextTapOracleModels as FlextTapOracleModels,
        m as m,
    )
    from flext_tap_oracle.protocols import (
        FlextTapOracleProtocols as FlextTapOracleProtocols,
        p as p,
    )
    from flext_tap_oracle.tap import (
        FlextTapOracleCli as FlextTapOracleCli,
        FlextTapOracleDiscoverCommand as FlextTapOracleDiscoverCommand,
        FlextTapOracleSyncCommand as FlextTapOracleSyncCommand,
    )
    from flext_tap_oracle.typings import (
        FlextTapOracleTypes as FlextTapOracleTypes,
        t as t,
    )
    from flext_tap_oracle.utilities import (
        FlextTapOracleUtilities as FlextTapOracleUtilities,
        u as u,
    )
_LAZY_IMPORTS = build_lazy_import_map(
    {
        "._settings": ("FlextTapOracleSettings", "settings"),
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
    },
)


__all__: tuple[str, ...] = (
    "FlextTapOracleSettings",
    "settings",
    "FlextTapOracleCli",
    "FlextTapOracleConstants",
    "FlextTapOracleDiscoverCommand",
    "FlextTapOracleModels",
    "FlextTapOracleProtocols",
    "FlextTapOracleService",
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
