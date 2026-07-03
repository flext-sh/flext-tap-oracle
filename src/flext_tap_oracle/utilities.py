"""FLEXT Tap Oracle Utilities - Domain-specific utilities for Oracle tap operations.

This module provides complete Oracle tap utilities extending u
with nested classes for error handling, stream management, discovery operations,
and configuration validation. Follows FLEXT standards with single-class pattern.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT

"""

from __future__ import annotations

from flext_core import FlextUtilitiesGuardsTypeCore
from flext_db_oracle import FlextDbOracleUtilities
from flext_meltano import u
from flext_tap_oracle._utilities.client import FlextTapOracleUtilitiesClientMixin


class FlextTapOracleUtilities(u, FlextDbOracleUtilities, FlextUtilitiesGuardsTypeCore):
    """Unified Oracle tap utilities class extending u classes."""

    class TapOracle(FlextTapOracleUtilitiesClientMixin):
        """Tap Oracle namespace for cross-project access."""

        pass


u = FlextTapOracleUtilities

__all__: list[str] = ["FlextTapOracleUtilities", "u"]
