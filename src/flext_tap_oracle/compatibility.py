"""FLEXT Tap Oracle - Compatibility aliases and legacy support.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from flext_tap_oracle.tap_client import FlextOracleTapService
from flext_tap_oracle.typings import FlextTapOracleTypes

# Main alias for external usage
FlextTapOracle = FlextOracleTapService

# Ultra-simple aliases for test compatibility
FlextOracleTapBaseService = FlextOracleTapService

# Legacy support flags
_LEGACY_IMPORTS_AVAILABLE = False  # Simplified for type checking
_LEGACY_FACADE_AVAILABLE = False  # Simplified for type checking


__all__: FlextTapOracleTypes.Core.StringList = [
    "FlextOracleTapBaseService",
    "FlextTapOracle",
]
