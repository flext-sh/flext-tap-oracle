# AUTO-GENERATED FILE — DO NOT EDIT MANUALLY.
# Regenerate with: make gen
#
"""Utilities package."""

from __future__ import annotations

import typing as _t

from flext_core.lazy import install_lazy_exports

if _t.TYPE_CHECKING:
    import flext_tap_oracle._utilities.client as _flext_tap_oracle__utilities_client

    client = _flext_tap_oracle__utilities_client
    from flext_tap_oracle._utilities.client import FlextTapOracleUtilitiesClientMixin
_LAZY_IMPORTS = {
    "FlextTapOracleUtilitiesClientMixin": (
        "flext_tap_oracle._utilities.client",
        "FlextTapOracleUtilitiesClientMixin",
    ),
    "client": "flext_tap_oracle._utilities.client",
}

__all__ = [
    "FlextTapOracleUtilitiesClientMixin",
    "client",
]


install_lazy_exports(__name__, globals(), _LAZY_IMPORTS)
