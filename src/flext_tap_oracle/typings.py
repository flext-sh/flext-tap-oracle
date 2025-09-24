"""Typing definitions for flext-tap-oracle.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from flext_core import FlextTypes as CoreFlextTypes


class FlextTapOracleTypes(CoreFlextTypes):
    """Type definitions for flext-tap-oracle."""

    # Re-export core types for convenience
    Core = CoreFlextTypes

    # Oracle-specific type aliases
    OracleTableName = str
    OracleColumnName = str
    OracleRecord = dict[str, object]
    OracleRecords = list[OracleRecord]
