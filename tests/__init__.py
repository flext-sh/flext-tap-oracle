# AUTO-GENERATED FILE — Regenerate with: make gen
"""Tests package."""

from __future__ import annotations

from typing import TYPE_CHECKING

from flext_core.lazy import (
    build_lazy_import_map,
    install_lazy_exports,
    merge_lazy_imports,
)

if TYPE_CHECKING:
    from flext_tests import d, e, h, r, td, tf, tk, tm, tv, x

    from tests.base import TestsFlextTapOracleServiceBase, s
    from tests.constants import TestsFlextTapOracleConstants, c
    from tests.models import TestsFlextTapOracleModels, m
    from tests.protocols import TestsFlextTapOracleProtocols, p
    from tests.settings import TestsFlextTapOracleSettings
    from tests.typings import TestsFlextTapOracleTypes, t
    from tests.unit.test_enterprise_tap import TestsFlextTapOracleEnterpriseTap
    from tests.utilities import TestsFlextTapOracleUtilities, u
_LAZY_IMPORTS = merge_lazy_imports(
    (".unit",),
    build_lazy_import_map(
        {
            ".base": (
                "TestsFlextTapOracleServiceBase",
                "s",
            ),
            ".conftest": ("conftest",),
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
            ".unit": ("unit",),
            ".unit.test_enterprise_tap": ("TestsFlextTapOracleEnterpriseTap",),
            ".utilities": (
                "TestsFlextTapOracleUtilities",
                "u",
            ),
            "flext_tests": (
                "d",
                "e",
                "h",
                "r",
                "td",
                "tf",
                "tk",
                "tm",
                "tv",
                "x",
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


install_lazy_exports(
    __name__,
    globals(),
    _LAZY_IMPORTS,
    publish_all=False,
)
