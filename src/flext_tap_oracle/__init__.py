"""FLEXT Tap Oracle - Oracle Database Singer Tap for FLEXT ecosystem.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from typing import TYPE_CHECKING, Any

from flext_core import cleanup_submodule_namespace, lazy_getattr

if TYPE_CHECKING:
    from flext_tap_oracle.__version__ import __version__, __version_info__
    from flext_tap_oracle.client import (
        FlextOracleConnectionTestService,
        FlextOracleDiscoveryService,
        FlextOracleTableFilterService,
        FlextOracleTapService,
    )
    from flext_tap_oracle.constants import (
        FlextMeltanoTapOracleConstants,
        FlextMeltanoTapOracleConstants as c,
    )
    from flext_tap_oracle.models import (
        FlextMeltanoTapOracleModels,
        FlextMeltanoTapOracleModels as m,
    )
    from flext_tap_oracle.protocols import (
        FlextMeltanoTapOracleProtocols,
        FlextMeltanoTapOracleProtocols as p,
    )
    from flext_tap_oracle.settings import FlextMeltanoTapOracleSettings
    from flext_tap_oracle.streams import FlextMeltanoTapOracleStreams
    from flext_tap_oracle.typings import (
        FlextMeltanoTapOracleTypes,
        FlextMeltanoTapOracleTypes as t,
    )
    from flext_tap_oracle.utilities import (
        FlextTapOracleUtilities,
        FlextTapOracleUtilities as FlextMeltanoTapOracleUtilities,
        FlextTapOracleUtilities as u,
    )

# Lazy import mapping: export_name -> (module_path, attr_name)
_LAZY_IMPORTS: dict[str, tuple[str, str]] = {
    "FlextMeltanoTapOracleConstants": (
        "flext_tap_oracle.constants",
        "FlextMeltanoTapOracleConstants",
    ),
    "FlextMeltanoTapOracleModels": (
        "flext_tap_oracle.models",
        "FlextMeltanoTapOracleModels",
    ),
    "FlextMeltanoTapOracleProtocols": (
        "flext_tap_oracle.protocols",
        "FlextMeltanoTapOracleProtocols",
    ),
    "FlextMeltanoTapOracleSettings": (
        "flext_tap_oracle.settings",
        "FlextMeltanoTapOracleSettings",
    ),
    "FlextMeltanoTapOracleStreams": (
        "flext_tap_oracle.streams",
        "FlextMeltanoTapOracleStreams",
    ),
    "FlextMeltanoTapOracleTypes": (
        "flext_tap_oracle.typings",
        "FlextMeltanoTapOracleTypes",
    ),
    "FlextMeltanoTapOracleUtilities": (
        "flext_tap_oracle.utilities",
        "FlextTapOracleUtilities",
    ),
    "FlextTapOracleUtilities": (
        "flext_tap_oracle.utilities",
        "FlextTapOracleUtilities",
    ),
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
    "__version__": ("flext_tap_oracle.__version__", "__version__"),
    "__version_info__": ("flext_tap_oracle.__version__", "__version_info__"),
    "c": ("flext_tap_oracle.constants", "FlextMeltanoTapOracleConstants"),
    "m": ("flext_tap_oracle.models", "FlextMeltanoTapOracleModels"),
    "p": ("flext_tap_oracle.protocols", "FlextMeltanoTapOracleProtocols"),
    "t": ("flext_tap_oracle.typings", "FlextMeltanoTapOracleTypes"),
    "u": ("flext_tap_oracle.utilities", "FlextTapOracleUtilities"),
}

__all__ = [
    "FlextMeltanoTapOracleConstants",
    "FlextMeltanoTapOracleModels",
    "FlextMeltanoTapOracleProtocols",
    "FlextMeltanoTapOracleSettings",
    "FlextMeltanoTapOracleStreams",
    "FlextMeltanoTapOracleTypes",
    "FlextMeltanoTapOracleUtilities",
    "FlextOracleConnectionTestService",
    "FlextOracleDiscoveryService",
    "FlextOracleTableFilterService",
    "FlextOracleTapService",
    "FlextTapOracleUtilities",
    "__version__",
    "__version_info__",
    "c",
    "m",
    "p",
    "t",
    "u",
]


def __getattr__(name: str) -> Any:  # noqa: ANN401
    """Lazy-load module attributes on first access (PEP 562)."""
    return lazy_getattr(name, _LAZY_IMPORTS, globals(), __name__)


def __dir__() -> list[str]:
    """Return list of available attributes for dir() and autocomplete."""
    return sorted(__all__)


cleanup_submodule_namespace(__name__, _LAZY_IMPORTS)
