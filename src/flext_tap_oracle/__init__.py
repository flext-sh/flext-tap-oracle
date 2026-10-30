# AUTO-GENERATED FILE — Regenerate with: make gen
"""Flext Tap Oracle package.

Copyright (c) 2026 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from types import MappingProxyType
from typing import TYPE_CHECKING

from flext_core.lazy import install_lazy_exports

if TYPE_CHECKING:
    from flext_db_oracle import db_oracle, e
    from flext_meltano import (
        build_lazy_import_map,
        cleanup_submodule_namespace,
        cli,
        core,
        d,
        h,
        install_lazy_exports,
        lazy,
        lazy_getattr,
        lazy_member,
        meltano,
        merge_lazy_imports,
        normalize_lazy_imports,
        r,
        resolve_lazy_members,
        s,
        x,
    )

    from flext_tap_oracle.__version__ import (
        FlextTapOracleVersion,
        __author__,
        __author_email__,
        __description__,
        __license__,
        __title__,
        __url__,
        __version__,
        __version_info__,
    )
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
    "FlextTapOracleVersion",
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
    "cleanup_submodule_namespace",
    "cli",
    "config",
    "core",
    "d",
    "db_oracle",
    "e",
    "h",
    "install_lazy_exports",
    "lazy",
    "lazy_getattr",
    "lazy_member",
    "m",
    "main",
    "meltano",
    "merge_lazy_imports",
    "normalize_lazy_imports",
    "p",
    "r",
    "resolve_lazy_members",
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
    MappingProxyType({
        "FlextTapOracleConfig": "._config",
        "FlextTapOracleConstants": ".constants",
        "FlextTapOracleModels": ".models",
        "FlextTapOracleProtocols": ".protocols",
        "FlextTapOracleService": ".api",
        "FlextTapOracleSettings": "._settings",
        "FlextTapOracleStreams": ".streams",
        "FlextTapOracleTypes": ".typings",
        "FlextTapOracleUtilities": ".utilities",
        "FlextTapOracleVersion": ".__version__",
        "__author__": ".__version__",
        "__author_email__": ".__version__",
        "__description__": ".__version__",
        "__license__": ".__version__",
        "__title__": ".__version__",
        "__url__": ".__version__",
        "__version_info__": ".__version__",
        "build_lazy_import_map": "flext_meltano",
        "c": ".constants",
        "cleanup_submodule_namespace": "flext_meltano",
        "cli": "flext_meltano",
        "config": "._config",
        "core": "flext_meltano",
        "d": "flext_meltano",
        "db_oracle": "flext_db_oracle",
        "e": "flext_db_oracle",
        "h": "flext_meltano",
        "install_lazy_exports": "flext_meltano",
        "lazy": "flext_meltano",
        "lazy_getattr": "flext_meltano",
        "lazy_member": "flext_meltano",
        "m": ".models",
        "main": ".cli",
        "meltano": "flext_meltano",
        "merge_lazy_imports": "flext_meltano",
        "normalize_lazy_imports": "flext_meltano",
        "p": ".protocols",
        "r": "flext_meltano",
        "resolve_lazy_members": "flext_meltano",
        "s": "flext_meltano",
        "settings": "._settings",
        "t": ".typings",
        "tap_oracle": ".api",
        "u": ".utilities",
        "x": "flext_meltano",
    }),
    public_exports=__all__,
)

if not TYPE_CHECKING:
    from flext_tap_oracle.__version__ import __version__
