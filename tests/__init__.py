# AUTO-GENERATED FILE — Regenerate with: make gen
"""Tests package."""

from __future__ import annotations

import typing as _t

from flext_core.lazy import (
    build_lazy_import_map,
    install_lazy_exports,
    merge_lazy_imports,
)

if _t.TYPE_CHECKING:
    from flext_tests import td as td, tf as tf, tk as tk, tv as tv

    from flext_tap_oracle import d as d, e as e, h as h, r as r, x as x
    from tests.base import (
        TestsFlextTapOracleServiceBase as TestsFlextTapOracleServiceBase,
        s as s,
    )
    from tests.constants import (
        TestsFlextTapOracleConstants as TestsFlextTapOracleConstants,
        c as c,
    )
    from tests.models import (
        TestsFlextTapOracleModels as TestsFlextTapOracleModels,
        m as m,
    )
    from tests.protocols import (
        TestsFlextTapOracleProtocols as TestsFlextTapOracleProtocols,
        p as p,
    )
    from tests.settings import (
        TestsFlextTapOracleSettings as TestsFlextTapOracleSettings,
    )
    from tests.typings import (
        TestsFlextTapOracleTypes as TestsFlextTapOracleTypes,
        t as t,
    )
    from tests.utilities import (
        TestsFlextTapOracleUtilities as TestsFlextTapOracleUtilities,
        u as u,
    )
_LAZY_IMPORTS = merge_lazy_imports(
    (".unit",),
    build_lazy_import_map(
        {
            ".base": (
                "TestsFlextTapOracleServiceBase",
                "s",
            ),
            ".constants": (
                "TestsFlextTapOracleConstants",
                "c",
            ),
            ".models": (
                "TestsFlextTapOracleModels",
                "m",
            ),
            ".protocols": (
                "TestsFlextTapOracleProtocols",
                "p",
            ),
            ".settings": ("TestsFlextTapOracleSettings",),
            ".typings": (
                "TestsFlextTapOracleTypes",
                "t",
            ),
            ".utilities": (
                "TestsFlextTapOracleUtilities",
                "u",
            ),
            "flext_tap_oracle": (
                "d",
                "e",
                "h",
                "r",
                "x",
            ),
            "flext_tests": (
                "td",
                "tf",
                "tk",
                "tv",
            ),
        },
    ),
    exclude_names=(
        "cleanup_submodule_namespace",
        "install_lazy_exports",
        "lazy_getattr",
        "logger",
        "merge_lazy_imports",
        "output",
        "output_reporting",
        "pytest_addoption",
        "pytest_collect_file",
        "pytest_collection_modifyitems",
        "pytest_configure",
        "pytest_runtest_setup",
        "pytest_runtest_teardown",
        "pytest_sessionfinish",
        "pytest_sessionstart",
        "pytest_terminal_summary",
        "pytest_warning_recorded",
    ),
    module_name=__name__,
)


install_lazy_exports(__name__, globals(), _LAZY_IMPORTS)

__all__: list[str] = [
    "TestsFlextTapOracleConstants",
    "TestsFlextTapOracleModels",
    "TestsFlextTapOracleProtocols",
    "TestsFlextTapOracleServiceBase",
    "TestsFlextTapOracleSettings",
    "TestsFlextTapOracleTypes",
    "TestsFlextTapOracleUtilities",
    "c",
    "d",
    "e",
    "h",
    "m",
    "p",
    "r",
    "s",
    "t",
    "td",
    "tf",
    "tk",
    "tv",
    "u",
    "x",
]
