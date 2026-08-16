# AUTO-GENERATED FILE — Regenerate with: make gen
"""Flext Tap Oracle package."""

from __future__ import annotations

from typing import TYPE_CHECKING

from types import MappingProxyType

from flext_core.lazy import build_lazy_import_map, install_lazy_exports

from .__version__ import __author__ as __author__
from .__version__ import __author_email__ as __author_email__
from .__version__ import __description__ as __description__
from .__version__ import __license__ as __license__
from .__version__ import __title__ as __title__
from .__version__ import __url__ as __url__
from .__version__ import __version__ as __version__
from .__version__ import __version_info__ as __version_info__

if TYPE_CHECKING:
    from flext_db_oracle import d, e, h, r, s, x

    from ._config import FlextTapOracleConfig, config
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
__all__: tuple[str, ...] = (
    "FlextTapOracleCli",
    "FlextTapOracleConfig",
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
    "config",
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
    MappingProxyType(
        build_lazy_import_map(
            MappingProxyType({
                "._config": ("FlextTapOracleConfig", "config"),
                "._settings": ("FlextTapOracleSettings", "settings"),
                ".api": ("FlextTapOracleService", "tap_oracle"),
                ".constants": ("FlextTapOracleConstants", "c"),
                ".models": ("FlextTapOracleModels", "m"),
                ".protocols": ("FlextTapOracleProtocols", "p"),
                ".tap": (
                    "FlextTapOracleCli",
                    "FlextTapOracleDiscoverCommand",
                    "FlextTapOracleSyncCommand",
                ),
                ".typings": ("FlextTapOracleTypes", "t"),
                ".utilities": ("FlextTapOracleUtilities", "u"),
                "flext_db_oracle": ("d", "e", "h", "r", "s", "x"),
            }),
            alias_groups=MappingProxyType({}),
            sort_keys=False,
        )
    ),
    public_exports=__all__,
)
