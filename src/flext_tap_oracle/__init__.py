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
    from enum import StrEnum, unique
    from flext_db_oracle import FlextDbOracleConstants, d, e, h, r, s, x
    from typing import Final, TYPE_CHECKING

    from ._config import FlextTapOracleConfig, config
    from ._settings import FlextTapOracleSettings, settings
    from .api import FlextTapOracleService, tap_oracle
    from .constants import FlextTapOracleConstants, FlextTapOracleConstants as c
    from .models import FlextTapOracleModels, FlextTapOracleModels as m
    from .protocols import FlextTapOracleProtocols, FlextTapOracleProtocols as p
    from .streams import FlextTapOracleStreams
    from .typings import FlextTapOracleTypes, FlextTapOracleTypes as t
    from .utilities import FlextTapOracleUtilities, FlextTapOracleUtilities as u
__all__: tuple[str, ...] = (
    "TYPE_CHECKING",
    "Final",
    "FlextDbOracleConstants",
    "FlextTapOracleConfig",
    "FlextTapOracleConstants",
    "FlextTapOracleModels",
    "FlextTapOracleProtocols",
    "FlextTapOracleService",
    "FlextTapOracleSettings",
    "FlextTapOracleStreams",
    "FlextTapOracleTypes",
    "FlextTapOracleUtilities",
    "StrEnum",
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
    "unique",
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
            "enum": ("StrEnum", "unique"),
            "flext_db_oracle": ("FlextDbOracleConstants", "d", "e", "h", "r", "s", "x"),
            "typing": ("Final", "TYPE_CHECKING"),
        }),
        alias_groups=MappingProxyType({}),
        sort_keys=False,
    )
)

install_lazy_exports(__name__, globals(), _LAZY_IMPORTS, public_exports=__all__)
