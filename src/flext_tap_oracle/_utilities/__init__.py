# AUTO-GENERATED FILE — DO NOT EDIT MANUALLY.
# Regenerate with: make gen
#
"""Utilities package."""

from __future__ import annotations

import typing as _t

from flext_core.lazy import install_lazy_exports

if _t.TYPE_CHECKING:
    import flext_tap_oracle._utilities._client as _flext_tap_oracle__utilities__client

    _client = _flext_tap_oracle__utilities__client

    _ = (
        FlextOracleConnectionTestService,
        FlextOracleDiscoveryService,
        FlextOracleTableFilterService,
        FlextOracleTapService,
        FlextTapOracleUtilitiesClientMixin,
        _client,
    )
_LAZY_IMPORTS = {
    "FlextOracleConnectionTestService": "flext_tap_oracle._utilities._client",
    "FlextOracleDiscoveryService": "flext_tap_oracle._utilities._client",
    "FlextOracleTableFilterService": "flext_tap_oracle._utilities._client",
    "FlextOracleTapService": "flext_tap_oracle._utilities._client",
    "FlextTapOracleUtilitiesClientMixin": "flext_tap_oracle._utilities._client",
    "_client": "flext_tap_oracle._utilities._client",
}

__all__ = [
    "FlextOracleConnectionTestService",
    "FlextOracleDiscoveryService",
    "FlextOracleTableFilterService",
    "FlextOracleTapService",
    "FlextTapOracleUtilitiesClientMixin",
    "_client",
]


install_lazy_exports(__name__, globals(), _LAZY_IMPORTS)
