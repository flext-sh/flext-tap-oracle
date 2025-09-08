"""Compatibility models module mapping to tap_models.

Re-exports domain models for tests that import flext_tap_oracle.models directly.


Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

"""
Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""


from flext_tap_oracle.tap_models import (
    FlextDbOracleColumn,
    FlextDbOracleQueryResult,
    FlextDbOracleSchema,
    FlextDbOracleTable,
    OracleTapDiscoveryResult,
    OracleTapExecutionStats,
    OracleTapStreamInfo,
    Stream,
)

__all__ = [
    "FlextDbOracleColumn",
    "FlextDbOracleQueryResult",
    "FlextDbOracleSchema",
    "FlextDbOracleTable",
    "OracleTapDiscoveryResult",
    "OracleTapExecutionStats",
    "OracleTapStreamInfo",
    "Stream",
]
