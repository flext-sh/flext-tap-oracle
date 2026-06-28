# AUTO-GENERATED FILE — Regenerate with: make gen
"""Flext Tap Oracle package."""

from __future__ import annotations

import typing as _t

from flext_core.lazy import (
    build_lazy_import_map,
    install_lazy_exports,
    merge_lazy_imports,
)
from flext_tap_oracle.__version__ import (
    __author__,
    __author_email__,
    __description__,
    __license__,
    __title__,
    __url__,
    __version__,
    __version_info__,
)

if _t.TYPE_CHECKING:
    from flext_meltano import d as d, e as e, h as h, r as r, s as s, x as x
    from flext_tap_oracle._utilities.client import (
        FlextTapOracleUtilitiesClientMixin as FlextTapOracleUtilitiesClientMixin,
    )
    from flext_tap_oracle.api import (
        FlextTapOracleService as FlextTapOracleService,
        tap_oracle as tap_oracle,
    )
    from flext_tap_oracle.constants import (
        FlextTapOracleConstants as FlextTapOracleConstants,
        c as c,
    )
    from flext_tap_oracle.models import (
        FlextTapOracleModels as FlextTapOracleModels,
        m as m,
    )
    from flext_tap_oracle.protocols import (
        FlextTapOracleProtocols as FlextTapOracleProtocols,
        p as p,
    )
    from flext_tap_oracle.settings import (
        FlextTapOracleSettings as FlextTapOracleSettings,
    )
    from flext_tap_oracle.streams import FlextTapOracleStreams as FlextTapOracleStreams
    from flext_tap_oracle.tap import (
        FlextTapOracleCli as FlextTapOracleCli,
        FlextTapOracleDiscoverCommand as FlextTapOracleDiscoverCommand,
        FlextTapOracleSyncCommand as FlextTapOracleSyncCommand,
    )
    from flext_tap_oracle.typings import (
        FlextTapOracleTypes as FlextTapOracleTypes,
        t as t,
    )
    from flext_tap_oracle.utilities import (
        FlextTapOracleUtilities as FlextTapOracleUtilities,
        u as u,
    )
_LAZY_IMPORTS = merge_lazy_imports(
    ("._utilities",),
    build_lazy_import_map(
        {
            "._utilities.client": ("FlextTapOracleUtilitiesClientMixin",),
            ".api": (
                "FlextTapOracleService",
                "tap_oracle",
            ),
            ".constants": (
                "FlextTapOracleConstants",
                "c",
            ),
            ".models": (
                "FlextTapOracleModels",
                "m",
            ),
            ".protocols": (
                "FlextTapOracleProtocols",
                "p",
            ),
            ".settings": ("FlextTapOracleSettings",),
            ".streams": ("FlextTapOracleStreams",),
            ".tap": (
                "FlextTapOracleCli",
                "FlextTapOracleDiscoverCommand",
                "FlextTapOracleSyncCommand",
            ),
            ".typings": (
                "FlextTapOracleTypes",
                "t",
            ),
            ".utilities": (
                "FlextTapOracleUtilities",
                "u",
            ),
            "flext_meltano": (
                "d",
                "e",
                "h",
                "r",
                "s",
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
    [
        "__author__",
        "__author_email__",
        "__description__",
        "__license__",
        "__title__",
        "__url__",
        "__version__",
        "__version_info__",
    ],
)

__all__: list[str] = [
    "FlextTapOracleCli",
    "FlextTapOracleConstants",
    "FlextTapOracleDiscoverCommand",
    "FlextTapOracleModels",
    "FlextTapOracleProtocols",
    "FlextTapOracleService",
    "FlextTapOracleSettings",
    "FlextTapOracleStreams",
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
    "d",
    "e",
    "h",
    "m",
    "p",
    "r",
    "s",
    "t",
    "tap_oracle",
    "u",
    "x",
]
