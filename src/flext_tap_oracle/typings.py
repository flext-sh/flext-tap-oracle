"""FLEXT Tap Oracle Types - Domain-specific Oracle tap type definitions.

This module provides Oracle tap-specific type definitions extending t.
Follows FLEXT standards:
- Domain-specific complex types only
- No simple aliases to primitive types
- Python 3.13+ syntax
- Extends t properly

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT

"""

from __future__ import annotations

from collections.abc import Mapping

from flext_core import FlextTypes as _tap_t
from flext_db_oracle.typings import FlextDbOracleTypes
from flext_meltano import FlextMeltanoTypes
from pydantic import BaseModel


class FlextTapOracleTypes(FlextMeltanoTypes, FlextDbOracleTypes):
    """Oracle tap-specific type definitions extending t.

    Domain-specific type system for Oracle database extraction operations.
    Contains ONLY complex Oracle tap-specific types, no simple aliases.
    Uses Python 3.13+ type syntax and patterns.
    """

    class Project(FlextMeltanoTypes.Meltano.Project):
        """Unified project types resolving MRO between Meltano and DbOracle."""

    class TapOracle:
        """Tap Oracle namespace for type definitions.

        Contains all Oracle tap-specific complex type definitions
        organized by functional domains.
        """

        class Summary:
            """Summary and reporting complex types."""

            type SummaryData = Mapping[str, _tap_t.NormalizedValue]
            type OracleValue = _tap_t.NormalizedValue | BaseModel | None


t = FlextTapOracleTypes

# Re-export from class for module-level access
OracleValue = t.TapOracle.Summary.OracleValue

__all__ = ["FlextTapOracleTypes", "OracleValue", "t"]
