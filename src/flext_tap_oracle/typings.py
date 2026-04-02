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

from pydantic import TypeAdapter

from flext_db_oracle import FlextDbOracleTypes
from flext_meltano import FlextMeltanoTypes


class FlextTapOracleTypes(FlextMeltanoTypes, FlextDbOracleTypes):
    """MRO facade composing Meltano + DbOracle type namespaces.

    Access: ``t.Meltano.*`` (Singer protocol), ``t.DbOracle.*`` (Oracle domain),
    and all core ``t.*`` types via MRO inheritance.
    """

    GENERAL_VALUE_MAP_ADAPTER: TypeAdapter[FlextMeltanoTypes.GeneralValueMapping] = (
        TypeAdapter(FlextMeltanoTypes.GeneralValueMapping)
    )
    INTEGER_ADAPTER: TypeAdapter[FlextMeltanoTypes.IntegerValue] = TypeAdapter(
        FlextMeltanoTypes.IntegerValue
    )

    class TapOracle:
        """Tap Oracle namespace for type definitions.

        Contains all Oracle tap-specific complex type definitions
        organized by functional domains.
        """

        class Summary:
            """Summary and reporting complex types."""

            type SummaryData = FlextDbOracleTypes.ContainerMapping
            type OracleValue = FlextDbOracleTypes.ValueOrModel | None


t = FlextTapOracleTypes

__all__ = ["FlextTapOracleTypes", "t"]
