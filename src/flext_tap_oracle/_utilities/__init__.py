# AUTO-GENERATED FILE — DO NOT EDIT MANUALLY.
# Regenerate with: make gen
#
"""FLEXT Tap Oracle Utilities - Internal subpackage.

Copyright (c) 2025 FLEXT Contributors
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from collections.abc import Mapping, Sequence
from typing import TYPE_CHECKING as _TYPE_CHECKING

from flext_core.lazy import install_lazy_exports

if _TYPE_CHECKING:
    from flext_core import FlextTypes

    from flext_tap_oracle._utilities._client import *

_LAZY_IMPORTS: Mapping[str, str | Sequence[str]] = {
    "FlextOracleConnectionTestService": "flext_tap_oracle._utilities._client",
    "FlextOracleDiscoveryService": "flext_tap_oracle._utilities._client",
    "FlextOracleTableFilterService": "flext_tap_oracle._utilities._client",
    "FlextOracleTapService": "flext_tap_oracle._utilities._client",
    "FlextTapOracleUtilitiesClientMixin": "flext_tap_oracle._utilities._client",
    "_client": "flext_tap_oracle._utilities._client",
}


install_lazy_exports(__name__, globals(), _LAZY_IMPORTS)
