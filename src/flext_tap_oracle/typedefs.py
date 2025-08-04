"""Oracle Tap type definitions using flext-db-oracle types.

This module provides Oracle Tap specific type definitions by importing
types from flext-db-oracle to avoid duplication and ensure consistency.
"""

from __future__ import annotations

# Only define types specific to the tap that don't exist in flext-db-oracle
from typing import Literal

# Import Oracle types from flext-db-oracle
from flext_db_oracle.types import (
    TDbOracleColumn,
    TDbOracleQueryResult,
    TDbOracleSchema,
    TDbOracleTable,
)

# Tap-specific types that extend Oracle functionality
TapReplicationMethod = Literal["FULL_TABLE", "INCREMENTAL"]
TapEnvironment = Literal["development", "staging", "production"]

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
