# AUTO-GENERATED FILE — Regenerate with: make gen
"""Tests package.

Copyright (c) 2026 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from typing import TYPE_CHECKING

from flext_core.lazy import install_lazy_exports

if TYPE_CHECKING:
    from flext_db_oracle import e
    from flext_tests import api, d, h, r, td, tf, tk, tm, x

    from flext_tap_oracle import (
        FlextTapOracleConfig,
        FlextTapOracleConstants,
        FlextTapOracleModels,
        FlextTapOracleProtocols,
        FlextTapOracleService,
        FlextTapOracleSettings,
        FlextTapOracleStreams,
        FlextTapOracleTypes,
        FlextTapOracleUtilities,
        FlextTapOracleVersion,
        __author__,
        __author_email__,
        __description__,
        __license__,
        __title__,
        __url__,
        __version__,
        __version_info__,
        config,
        main,
        settings,
        tap_oracle,
    )
    from tests.base import TestsFlextTapOracleServiceBase, s
    from tests.constants import TestsFlextTapOracleConstants, c
    from tests.models import TestsFlextTapOracleModels, m
    from tests.protocols import TestsFlextTapOracleProtocols, p
    from tests.settings import TestsFlextTapOracleSettings
    from tests.typings import TestsFlextTapOracleTypes, t
    from tests.unit import TestsFlextTapOracleEnterpriseTap
    from tests.utilities import TestsFlextTapOracleUtilities, u


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
    "TestsFlextTapOracleConstants",
    "TestsFlextTapOracleEnterpriseTap",
    "TestsFlextTapOracleModels",
    "TestsFlextTapOracleProtocols",
    "TestsFlextTapOracleServiceBase",
    "TestsFlextTapOracleSettings",
    "TestsFlextTapOracleTypes",
    "TestsFlextTapOracleUtilities",
    "__author__",
    "__author_email__",
    "__description__",
    "__license__",
    "__title__",
    "__url__",
    "__version__",
    "__version_info__",
    "api",
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
    {
        "FlextTapOracleConfig": "flext_tap_oracle",
        "FlextTapOracleConstants": "flext_tap_oracle",
        "FlextTapOracleModels": "flext_tap_oracle",
        "FlextTapOracleProtocols": "flext_tap_oracle",
        "FlextTapOracleService": "flext_tap_oracle",
        "FlextTapOracleSettings": "flext_tap_oracle",
        "FlextTapOracleStreams": "flext_tap_oracle",
        "FlextTapOracleTypes": "flext_tap_oracle",
        "FlextTapOracleUtilities": "flext_tap_oracle",
        "FlextTapOracleVersion": "flext_tap_oracle",
        "TestsFlextTapOracleConstants": ".constants",
        "TestsFlextTapOracleEnterpriseTap": ".unit",
        "TestsFlextTapOracleModels": ".models",
        "TestsFlextTapOracleProtocols": ".protocols",
        "TestsFlextTapOracleServiceBase": ".base",
        "TestsFlextTapOracleSettings": ".settings",
        "TestsFlextTapOracleTypes": ".typings",
        "TestsFlextTapOracleUtilities": ".utilities",
        "__author__": "flext_tap_oracle",
        "__author_email__": "flext_tap_oracle",
        "__description__": "flext_tap_oracle",
        "__license__": "flext_tap_oracle",
        "__title__": "flext_tap_oracle",
        "__url__": "flext_tap_oracle",
        "__version__": "flext_tap_oracle",
        "__version_info__": "flext_tap_oracle",
        "api": "flext_tests",
        "c": ".constants",
        "config": "flext_tap_oracle",
        "d": "flext_tests",
        "e": "flext_db_oracle",
        "h": "flext_tests",
        "m": ".models",
        "main": "flext_tap_oracle",
        "p": ".protocols",
        "r": "flext_tests",
        "s": ".base",
        "settings": "flext_tap_oracle",
        "t": ".typings",
        "tap_oracle": "flext_tap_oracle",
        "td": "flext_tests",
        "tf": "flext_tests",
        "tk": "flext_tests",
        "tm": "flext_tests",
        "u": ".utilities",
        "x": "flext_tests",
    },
    public_exports=__all__,
)
