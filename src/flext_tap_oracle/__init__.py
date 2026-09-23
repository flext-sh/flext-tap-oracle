# AUTO-GENERATED FILE — Regenerate with: make gen
"""Flext Tap Oracle package."""

from __future__ import annotations

from types import MappingProxyType
from typing import TYPE_CHECKING

from flext_core.lazy import build_lazy_import_map, install_lazy_exports

from .__version__ import (
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
    from flext_db_oracle import db_oracle, e
    from flext_meltano import (
        cli,
        core,
        d,
        h,
        lazy_attribute,
        main,
        meltano,
        r,
        s,
        services,
        x,
    )

    from ._config import FlextTapOracleConfig, config
    from ._settings import FlextTapOracleSettings, settings
    from .api import FlextTapOracleService, tap_oracle
    from .constants import FlextTapOracleConstants, c
    from .models import FlextTapOracleModels, m
    from .protocols import FlextTapOracleProtocols, FlextTapOracleProtocols as p
    from .streams import FlextTapOracleStreams
    from .typings import FlextTapOracleTypes, t
    from .utilities import FlextTapOracleUtilities, u


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
    "cli",
    "config",
    "core",
    "d",
    "db_oracle",
    "e",
    "h",
    "lazy_attribute",
    "m",
    "main",
    "meltano",
    "p",
    "r",
    "s",
    "services",
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
            ".constants": ("FlextTapOracleConstants", "c"),
            ".models": ("FlextTapOracleModels", "m"),
            ".protocols": ("FlextTapOracleProtocols", "p"),
            ".streams": ("FlextTapOracleStreams",),
            ".typings": ("FlextTapOracleTypes", "t"),
            ".utilities": ("FlextTapOracleUtilities", "u"),
            "flext_db_oracle": ("db_oracle", "e"),
            "flext_meltano": (
                "cli",
                "core",
                "d",
                "h",
                "lazy_attribute",
                "main",
                "meltano",
                "r",
                "s",
                "services",
                "x",
            ),
        }),
        alias_groups=MappingProxyType({}),
        sort_keys=False,
    )
)

install_lazy_exports(__name__, globals(), _LAZY_IMPORTS, public_exports=__all__)
