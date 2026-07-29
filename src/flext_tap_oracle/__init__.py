# @generated AUTO-GENERATED FILE — Regenerate with: make gen
"""Flext Tap Oracle package."""

from __future__ import annotations

from typing import TYPE_CHECKING

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
    from flext_db_oracle import d as d
    from flext_db_oracle import e as e
    from flext_db_oracle import h as h
    from flext_db_oracle import r as r
    from flext_db_oracle import s as s
    from flext_db_oracle import x as x

    from ._config import FlextTapOracleConfig as FlextTapOracleConfig
    from ._config import config as config
    from ._settings import FlextTapOracleSettings as FlextTapOracleSettings
    from ._settings import settings as settings
    from .api import FlextTapOracleService as FlextTapOracleService
    from .api import tap_oracle as tap_oracle
    from .constants import FlextTapOracleConstants as FlextTapOracleConstants

    c: type[FlextTapOracleConstants]
    from .models import FlextTapOracleModels as FlextTapOracleModels

    m: type[FlextTapOracleModels]
    from .protocols import FlextTapOracleProtocols as FlextTapOracleProtocols

    p: type[FlextTapOracleProtocols]
    from .tap import FlextTapOracleCli as FlextTapOracleCli
    from .tap import FlextTapOracleDiscoverCommand as FlextTapOracleDiscoverCommand
    from .tap import FlextTapOracleSyncCommand as FlextTapOracleSyncCommand
    from .typings import FlextTapOracleTypes as FlextTapOracleTypes

    t: type[FlextTapOracleTypes]
    from .utilities import FlextTapOracleUtilities as FlextTapOracleUtilities

    u: type[FlextTapOracleUtilities]

_LAZY_MODULES: dict[str, tuple[str, ...]] = {
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
}


_LAZY_ALIAS_GROUPS: dict[str, tuple[tuple[str, str], ...]] = {}


_LAZY_IMPORTS = build_lazy_import_map(
    _LAZY_MODULES, alias_groups=_LAZY_ALIAS_GROUPS, sort_keys=False
)

_PUBLIC_EXPORTS: tuple[str, ...] = (
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

__all__: tuple[str, ...] = tuple(_PUBLIC_EXPORTS)

install_lazy_exports(__name__, globals(), _LAZY_IMPORTS, public_exports=__all__)
