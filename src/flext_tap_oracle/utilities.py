# AUTO-GENERATED FILE — Regenerate with: make gen
"""FLEXT Tap Oracle Utilities - Domain-specific utilities for Oracle tap operations.

This module provides complete Oracle tap utilities extending u
with nested classes for error handling, stream management, discovery operations,
and configuration validation. Follows FLEXT standards with single-class pattern.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT

"""

from __future__ import annotations

from flext_db_oracle import u as flext_db_oracle_u
from flext_meltano import u as flext_meltano_u

from flext_tap_oracle._utilities import FlextTapOracleUtilitiesClient


class FlextTapOracleUtilities(flext_meltano_u, flext_db_oracle_u):
    """Unified Oracle tap utilities over the Meltano and DbOracle facades.

    Composes the tap's client mixin with the flext-meltano and flext-db-oracle
    utility facades; consumers reach every helper via ``u.TapOracle.*``.

    """

    class TapOracle(FlextTapOracleUtilitiesClient):
        """Tap Oracle namespace for cross-project access."""


u = FlextTapOracleUtilities
__all__: list[str] = ["FlextTapOracleUtilities", "u"]
