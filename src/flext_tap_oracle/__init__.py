# AUTO-GENERATED FILE — DO NOT EDIT MANUALLY.
# Regenerate with: make codegen
#
"""FLEXT Tap Oracle - Oracle Database Singer Tap for FLEXT ecosystem.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from typing import TYPE_CHECKING

from flext_core.lazy import cleanup_submodule_namespace, lazy_getattr

if TYPE_CHECKING:
    from flext_core.typings import FlextTypes
    from flext_db_oracle import d, e, h, r, s, x

    from flext_tap_oracle.__version__ import (
        __all__,
        __author__,
        __author_email__,
        __description__,
        __license__,
        __title__,
        __url__,
        __version__,
        __version_info__,
    )
    from flext_tap_oracle.client import (
        FlextOracleConnectionTestService,
        FlextOracleDiscoveryService,
        FlextOracleTableFilterService,
        FlextOracleTapService,
        create_oracle_discovery_service,
        create_oracle_tap_service,
    )
    from flext_tap_oracle.constants import FlextTapOracleConstants, c
    from flext_tap_oracle.models import FlextTapOracleModels, m
    from flext_tap_oracle.protocols import FlextTapOracleProtocols, p
    from flext_tap_oracle.settings import (
        FlextTapOracleSettings,
        create_oracle_tap_config,
        validate_oracle_tap_configuration,
    )
    from flext_tap_oracle.streams import FlextTapOracleStreams
    from flext_tap_oracle.tap import (
        OracleTapDiscoverCommand,
        OracleTapDiscoverParams,
        OracleTapSyncCommand,
        OracleTapSyncParams,
        cli,
        cli_api,
        create_tap_oracle_cli,
        handle_discover_command,
        handle_sync_command,
        logger,
        main,
    )
    from flext_tap_oracle.typings import FlextTapOracleTypes, OracleValue, t
    from flext_tap_oracle.utilities import FlextTapOracleUtilities, u

_LAZY_IMPORTS: dict[str, tuple[str, str]] = {
    "FlextOracleConnectionTestService": (
        "flext_tap_oracle.client",
        "FlextOracleConnectionTestService",
    ),
    "FlextOracleDiscoveryService": (
        "flext_tap_oracle.client",
        "FlextOracleDiscoveryService",
    ),
    "FlextOracleTableFilterService": (
        "flext_tap_oracle.client",
        "FlextOracleTableFilterService",
    ),
    "FlextOracleTapService": ("flext_tap_oracle.client", "FlextOracleTapService"),
    "FlextTapOracleConstants": (
        "flext_tap_oracle.constants",
        "FlextTapOracleConstants",
    ),
    "FlextTapOracleModels": ("flext_tap_oracle.models", "FlextTapOracleModels"),
    "FlextTapOracleProtocols": (
        "flext_tap_oracle.protocols",
        "FlextTapOracleProtocols",
    ),
    "FlextTapOracleSettings": ("flext_tap_oracle.settings", "FlextTapOracleSettings"),
    "FlextTapOracleStreams": ("flext_tap_oracle.streams", "FlextTapOracleStreams"),
    "FlextTapOracleTypes": ("flext_tap_oracle.typings", "FlextTapOracleTypes"),
    "FlextTapOracleUtilities": (
        "flext_tap_oracle.utilities",
        "FlextTapOracleUtilities",
    ),
    "OracleTapDiscoverCommand": ("flext_tap_oracle.tap", "OracleTapDiscoverCommand"),
    "OracleTapDiscoverParams": ("flext_tap_oracle.tap", "OracleTapDiscoverParams"),
    "OracleTapSyncCommand": ("flext_tap_oracle.tap", "OracleTapSyncCommand"),
    "OracleTapSyncParams": ("flext_tap_oracle.tap", "OracleTapSyncParams"),
    "OracleValue": ("flext_tap_oracle.typings", "OracleValue"),
    "__all__": ("flext_tap_oracle.__version__", "__all__"),
    "__author__": ("flext_tap_oracle.__version__", "__author__"),
    "__author_email__": ("flext_tap_oracle.__version__", "__author_email__"),
    "__description__": ("flext_tap_oracle.__version__", "__description__"),
    "__license__": ("flext_tap_oracle.__version__", "__license__"),
    "__title__": ("flext_tap_oracle.__version__", "__title__"),
    "__url__": ("flext_tap_oracle.__version__", "__url__"),
    "__version__": ("flext_tap_oracle.__version__", "__version__"),
    "__version_info__": ("flext_tap_oracle.__version__", "__version_info__"),
    "c": ("flext_tap_oracle.constants", "c"),
    "cli": ("flext_tap_oracle.tap", "cli"),
    "cli_api": ("flext_tap_oracle.tap", "cli_api"),
    "create_oracle_discovery_service": (
        "flext_tap_oracle.client",
        "create_oracle_discovery_service",
    ),
    "create_oracle_tap_config": (
        "flext_tap_oracle.settings",
        "create_oracle_tap_config",
    ),
    "create_oracle_tap_service": (
        "flext_tap_oracle.client",
        "create_oracle_tap_service",
    ),
    "create_tap_oracle_cli": ("flext_tap_oracle.tap", "create_tap_oracle_cli"),
    "d": ("flext_db_oracle", "d"),
    "e": ("flext_db_oracle", "e"),
    "h": ("flext_db_oracle", "h"),
    "handle_discover_command": ("flext_tap_oracle.tap", "handle_discover_command"),
    "handle_sync_command": ("flext_tap_oracle.tap", "handle_sync_command"),
    "logger": ("flext_tap_oracle.tap", "logger"),
    "m": ("flext_tap_oracle.models", "m"),
    "main": ("flext_tap_oracle.tap", "main"),
    "p": ("flext_tap_oracle.protocols", "p"),
    "r": ("flext_db_oracle", "r"),
    "s": ("flext_db_oracle", "s"),
    "t": ("flext_tap_oracle.typings", "t"),
    "u": ("flext_tap_oracle.utilities", "u"),
    "validate_oracle_tap_configuration": (
        "flext_tap_oracle.settings",
        "validate_oracle_tap_configuration",
    ),
    "x": ("flext_db_oracle", "x"),
}

__all__ = [
    "FlextOracleConnectionTestService",
    "FlextOracleDiscoveryService",
    "FlextOracleTableFilterService",
    "FlextOracleTapService",
    "FlextTapOracleConstants",
    "FlextTapOracleModels",
    "FlextTapOracleProtocols",
    "FlextTapOracleSettings",
    "FlextTapOracleStreams",
    "FlextTapOracleTypes",
    "FlextTapOracleUtilities",
    "OracleTapDiscoverCommand",
    "OracleTapDiscoverParams",
    "OracleTapSyncCommand",
    "OracleTapSyncParams",
    "OracleValue",
    "__all__",
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
    "cli_api",
    "create_oracle_discovery_service",
    "create_oracle_tap_config",
    "create_oracle_tap_service",
    "create_tap_oracle_cli",
    "d",
    "e",
    "h",
    "handle_discover_command",
    "handle_sync_command",
    "logger",
    "m",
    "main",
    "p",
    "r",
    "s",
    "t",
    "u",
    "validate_oracle_tap_configuration",
    "x",
]


def __getattr__(name: str) -> FlextTypes.ModuleExport:
    """Lazy-load module attributes on first access (PEP 562)."""
    return lazy_getattr(name, _LAZY_IMPORTS, globals(), __name__)


def __dir__() -> list[str]:
    """Return list of available attributes for dir() and autocomplete."""
    return sorted(__all__)


cleanup_submodule_namespace(__name__, _LAZY_IMPORTS)
