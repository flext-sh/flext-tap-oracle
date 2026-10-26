# AUTO-GENERATED FILE — Regenerate with: make gen
"""Tests package.

Copyright (c) 2026 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from types import MappingProxyType
from typing import TYPE_CHECKING

from flext_core.lazy import install_lazy_exports

if TYPE_CHECKING:
    from flext_db_oracle import e
    from flext_tests import (
        api,
        config,
        d,
        h,
        install_local_packages,
        r,
        settings,
        td,
        tf,
        tk,
        tm,
        x,
    )

    from flext_tap_oracle import (
        build_lazy_import_map,
        cleanup_submodule_namespace,
        cli,
        core,
        db_oracle,
        install_lazy_exports,
        lazy,
        lazy_getattr,
        lazy_member,
        main,
        meltano,
        merge_lazy_imports,
        normalize_lazy_imports,
        resolve_lazy_members,
        tap_oracle,
    )
    from tests.base import TestsFlextTapOracleServiceBase, s
    from tests.constants import TestsFlextTapOracleConstants, c
    from tests.models import TestsFlextTapOracleModels, m
    from tests.protocols import TestsFlextTapOracleProtocols, p
    from tests.settings import TestsFlextTapOracleSettings
    from tests.typings import TestsFlextTapOracleTypes, t
    from tests.utilities import TestsFlextTapOracleUtilities, u


__all__: tuple[str, ...] = (
    "TestsFlextTapOracleConstants",
    "TestsFlextTapOracleModels",
    "TestsFlextTapOracleProtocols",
    "TestsFlextTapOracleServiceBase",
    "TestsFlextTapOracleSettings",
    "TestsFlextTapOracleTypes",
    "TestsFlextTapOracleUtilities",
    "api",
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
    "install_local_packages",
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
    "td",
    "tf",
    "tk",
    "tm",
    "u",
    "x",
)

install_lazy_exports(
    __name__,
    globals(),
    MappingProxyType({
        "TestsFlextTapOracleConstants": ".constants",
        "TestsFlextTapOracleModels": ".models",
        "TestsFlextTapOracleProtocols": ".protocols",
        "TestsFlextTapOracleServiceBase": ".base",
        "TestsFlextTapOracleSettings": ".settings",
        "TestsFlextTapOracleTypes": ".typings",
        "TestsFlextTapOracleUtilities": ".utilities",
        "api": "flext_tests",
        "build_lazy_import_map": "flext_tap_oracle",
        "c": ".constants",
        "cleanup_submodule_namespace": "flext_tap_oracle",
        "cli": "flext_tap_oracle",
        "config": "flext_tests",
        "core": "flext_tap_oracle",
        "d": "flext_tests",
        "db_oracle": "flext_tap_oracle",
        "e": "flext_db_oracle",
        "h": "flext_tests",
        "install_lazy_exports": "flext_tap_oracle",
        "install_local_packages": "flext_tests",
        "lazy": "flext_tap_oracle",
        "lazy_getattr": "flext_tap_oracle",
        "lazy_member": "flext_tap_oracle",
        "m": ".models",
        "main": "flext_tap_oracle",
        "meltano": "flext_tap_oracle",
        "merge_lazy_imports": "flext_tap_oracle",
        "normalize_lazy_imports": "flext_tap_oracle",
        "p": ".protocols",
        "r": "flext_tests",
        "resolve_lazy_members": "flext_tap_oracle",
        "s": ".base",
        "settings": "flext_tests",
        "t": ".typings",
        "tap_oracle": "flext_tap_oracle",
        "td": "flext_tests",
        "tf": "flext_tests",
        "tk": "flext_tests",
        "tm": "flext_tests",
        "u": ".utilities",
        "x": "flext_tests",
    }),
    public_exports=__all__,
)
