"""Oracle Tap type definitions using flext-db-oracle types.

This module provides Oracle Tap specific type definitions by importing
types from flext-db-oracle and flext-core to avoid duplication and ensure consistency.

PRINCIPLE: NO DUPLICATION - use existing types from flext-* ecosystem.
"""

from __future__ import annotations

# Only define types specific to the tap that don't exist in flext-db-oracle
# Import from flext-core and define aliases - NO DUPLICATION
from typing import Literal

from flext_core import FlextEnvironment

# Import Oracle types from flext-db-oracle
from flext_db_oracle import (
    TDbOracleColumn,
    TDbOracleQueryResult,
    TDbOracleSchema,
    TDbOracleTable,
)

# Use existing types from flext-core - ELIMINATED ALL DUPLICATIONS
TapEnvironment = FlextEnvironment
# Use same definition as flext-core semantic_types - NO DUPLICATION
TapReplicationMethod = Literal["FULL_TABLE", "INCREMENTAL", "LOG_BASED"]

__all__: list[str] = [
    # Re-export Oracle types
    "TDbOracleColumn",
    "TDbOracleQueryResult",
    "TDbOracleSchema",
    "TDbOracleTable",
    # Tap-specific types
    "TapEnvironment",
    "TapReplicationMethod",
]
