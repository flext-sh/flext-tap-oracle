"""Models for flext-tap-oracle.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from flext_core import FlextModels


class TapOracleModels:
    """Models for Oracle tap operations."""

    # Re-export core models
    Core = FlextModels

    # Oracle-specific model types
    OracleRecord = dict[str, object]
    OracleRecords = list[OracleRecord]
