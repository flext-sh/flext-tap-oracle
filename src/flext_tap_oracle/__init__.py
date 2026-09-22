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
<<<<<<< HEAD
    from flext_cli import cli
    from flext_db_oracle import db_oracle, e
    from flext_meltano import main, meltano, s
    from pydantic_core import from_json, to_json, to_jsonable_python

    from flext_core import core, d, h, lazy_attribute, r, x
=======
    from flext_db_oracle import e, s

    from flext_core import d, h, r, x
>>>>>>> origin/0.12.0-dev

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
    "from_json",
    "h",
    "lazy_attribute",
    "m",
    "main",
    "meltano",
    "p",
    "r",
    "s",
    "settings",
    "t",
    "tap_oracle",
    "to_json",
    "to_jsonable_python",
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
<<<<<<< HEAD
            "flext_cli": ("cli",),
            "flext_core": ("core", "d", "h", "lazy_attribute", "r", "x"),
            "flext_db_oracle": ("db_oracle", "e"),
            "flext_meltano": ("main", "meltano", "s"),
            "pydantic_core": ("from_json", "to_json", "to_jsonable_python"),
=======
            "flext_core": ("d", "h", "r", "x"),
            "flext_db_oracle": ("e", "s"),
>>>>>>> origin/0.12.0-dev
        }),
        alias_groups=MappingProxyType({}),
        sort_keys=False,
    )
)

install_lazy_exports(__name__, globals(), _LAZY_IMPORTS, public_exports=__all__)
