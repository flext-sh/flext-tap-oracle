"""FLEXT Tap Oracle - Oracle Database Singer Tap for FLEXT ecosystem.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from typing import TYPE_CHECKING, Any

from flext_core.lazy import cleanup_submodule_namespace, lazy_getattr

if TYPE_CHECKING:
    from flext_tap_oracle.__version__ import __version__, __version_info__
    from flext_tap_oracle.client import (
        FlextOracleConnectionTestService,
        FlextOracleDiscoveryService,
        FlextOracleTableFilterService,
        FlextOracleTapService,
    )
    from flext_tap_oracle.constants import (
        FlextTapOracleConstants,
        FlextTapOracleConstants as c,
    )
    from flext_tap_oracle.models import FlextTapOracleModels, FlextTapOracleModels as m
    from flext_tap_oracle.protocols import (
        FlextTapOracleProtocols,
        FlextTapOracleProtocols as p,
    )
    from flext_tap_oracle.settings import FlextTapOracleSettings
    from flext_tap_oracle.streams import FlextTapOracleStreams
    from flext_tap_oracle.typings import FlextTapOracleTypes, FlextTapOracleTypes as t
    from flext_tap_oracle.utilities import (
        FlextTapOracleUtilities,
        FlextTapOracleUtilities as u,
    )

# Lazy import mapping: export_name -> (module_path, attr_name)
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
    "__version__": ("flext_tap_oracle.__version__", "__version__"),
    "__version_info__": ("flext_tap_oracle.__version__", "__version_info__"),
    "c": ("flext_tap_oracle.constants", "FlextTapOracleConstants"),
    "m": ("flext_tap_oracle.models", "FlextTapOracleModels"),
    "p": ("flext_tap_oracle.protocols", "FlextTapOracleProtocols"),
    "t": ("flext_tap_oracle.typings", "FlextTapOracleTypes"),
    "u": ("flext_tap_oracle.utilities", "FlextTapOracleUtilities"),
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
    "__version__",
    "__version_info__",
    "c",
    "m",
    "p",
    "t",
    "u",
]


def __getattr__(
    name: str,
) -> Any:  # JUSTIFIED: Ruff (any-type) with PEP 562 dynamic module exports — https://docs.astral.sh/ruff/rules/any-type/
    """Lazy-load module attributes on first access (PEP 562)."""
    return lazy_getattr(name, _LAZY_IMPORTS, globals(), __name__)


def __dir__() -> list[str]:
    """Return list of available attributes for dir() and autocomplete."""
    return sorted(__all__)


cleanup_submodule_namespace(__name__, _LAZY_IMPORTS)
