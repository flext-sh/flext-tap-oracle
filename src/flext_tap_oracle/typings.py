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

from flext_core.typings import FlextTypes as _tap_t
from flext_db_oracle.typings import FlextDbOracleTypes
from flext_meltano import FlextMeltanoTypes
from pydantic import BaseModel

from flext_tap_oracle.constants import FlextTapOracleConstants as c


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

        type MeltanoTapOracleProjectType = c.MeltanoTapOracleProjectType

        class Extraction:
            """Oracle extraction complex types."""

            type ExtractionConfiguration = dict[str, _tap_t.GeneralValueType]
            type ExtractionState = dict[str, _tap_t.Container]
            type ExtractionMetrics = dict[str, _tap_t.GeneralValueType]
            type BatchConfiguration = dict[str, _tap_t.GeneralValueType]
            type StreamDefinition = dict[
                str,
                str | list[str] | dict[str, _tap_t.Scalar],
            ]
            type TableMetadata = dict[str, list[_tap_t.Scalar]]

        class Singer:
            """Singer protocol complex types."""

            type CatalogEntry = dict[str, str | dict[str, _tap_t.Container]]
            type StreamSchema = dict[str, dict[str, _tap_t.Container]]
            type TapConfiguration = dict[str, _tap_t.GeneralValueType]
            type StateBookmark = dict[str, _tap_t.Container]
            type RecordMessage = dict[str, str | dict[str, _tap_t.Scalar]]
            type SchemaMessage = dict[str, str | dict[str, _tap_t.Container]]

        class Configuration:
            """Oracle tap configuration complex types."""

            type TapOracleConfig = dict[str, _tap_t.GeneralValueType]
            type ConnectionSettings = dict[str, _tap_t.GeneralValueType]
            type ExtractionSettings = dict[str, _tap_t.GeneralValueType]
            type PerformanceSettings = dict[str, _tap_t.GeneralValueType]
            type SecuritySettings = dict[str, _tap_t.GeneralValueType]
            type StreamSettings = dict[str, _tap_t.GeneralValueType]

        class Project:
            """Singer Tap Oracle-specific project types.

            Adds Singer tap Oracle-specific project types.
            Follows domain separation principle:
            Singer tap Oracle domain owns Oracle extraction and Singer protocol-specific types.
            """

            type ProjectType = c.ProjectType
            type SingerTapOracleProjectConfig = dict[str, _tap_t.GeneralValueType]
            type OracleExtractorConfig = dict[str, str | int | bool | list[str]]
            type SingerProtocolConfig = dict[str, _tap_t.GeneralValueType]
            type TapOraclePipelineConfig = dict[str, _tap_t.GeneralValueType]

        class Summary:
            """Summary and reporting complex types."""

            type SummaryData = dict[str, _tap_t.GeneralValueType | None]
            type OracleValue = _tap_t.NormalizedValue | BaseModel | None


t = FlextTapOracleTypes

# Re-export from class for module-level access
OracleValue = t.TapOracle.Summary.OracleValue

__all__ = ["FlextTapOracleTypes", "OracleValue", "t"]
