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

from typing import Literal

from flext_db_oracle import FlextDbOracleTypes
from flext_meltano import FlextMeltanoTypes


class FlextTapOracleTypes(FlextMeltanoTypes, FlextDbOracleTypes):
    """Oracle tap-specific type definitions extending t.

    Domain-specific type system for Oracle database extraction operations.
    Contains ONLY complex Oracle tap-specific types, no simple aliases.
    Uses Python 3.13+ type syntax and patterns.
    """

    class Project(FlextMeltanoTypes.Meltano.Project, FlextDbOracleTypes.Project):
        """Unified project types resolving MRO between Meltano and DbOracle."""

    class TapOracle:
        """Tap Oracle namespace for type definitions.

        Contains all Oracle tap-specific complex type definitions
        organized by functional domains.
        """

        # Combined project types from both domains
        type MeltanoTapOracleProjectType = Literal[
            # Generic types inherited from t
            "library",
            "application",
            "service",
            # Meltano-specific types
            "meltano-project",
            "elt-pipeline",
            "data-pipeline",
            "etl-service",
            "singer-tap",
            "singer-target",
            "dbt-project",
            "data-integration",
            "meltano-plugin",
            "data-connector",
            # Oracle-specific types
            "oracle-service",
            "database-service",
            "data-warehouse",
            "oracle-client",
            "db-migration",
            "schema-manager",
            "sql-service",
            "oracle-api",
            "database-api",
            "oracle-tap",
            "oracle-target",
        ]

        # =========================================================================
        # ORACLE TAP EXTRACTION TYPES - Complex extraction operation types
        # =========================================================================

        class Extraction:
            """Oracle extraction complex types."""

            type ExtractionConfiguration = dict[
                str,
                t.GeneralValueType | dict[str, t.GeneralValueType],
            ]
            type ExtractionState = dict[str, t.JsonValue | t.GeneralValueType]
            type ExtractionMetrics = dict[
                str,
                int | float | bool | dict[str, t.GeneralValueType],
            ]
            type BatchConfiguration = dict[
                str,
                int | bool | dict[str, t.GeneralValueType],
            ]
            type StreamDefinition = dict[
                str,
                str | list[str] | dict[str, t.JsonValue],
            ]
            type TableMetadata = dict[
                str,
                t.JsonValue | list[dict[str, t.GeneralValueType]],
            ]

        # =========================================================================
        # SINGER PROTOCOL TYPES - Complex Singer protocol types
        # =========================================================================

        class Singer:
            """Singer protocol complex types."""

            type CatalogEntry = dict[str, str | dict[str, t.JsonValue]]
            type StreamSchema = dict[str, dict[str, t.JsonValue]]
            type TapConfiguration = dict[
                str,
                t.GeneralValueType | dict[str, t.GeneralValueType],
            ]
            type StateBookmark = dict[str, t.JsonValue | t.GeneralValueType]
            type RecordMessage = dict[str, str | dict[str, t.JsonValue]]
            type SchemaMessage = dict[str, str | dict[str, t.JsonValue]]

        # =========================================================================
        # ORACLE TAP CONFIGURATION TYPES - Complex configuration types
        # =========================================================================

        class Configuration:
            """Oracle tap configuration complex types."""

            type TapOracleConfig = dict[
                str,
                t.GeneralValueType | dict[str, t.GeneralValueType],
            ]
            type ConnectionSettings = dict[
                str,
                str | int | bool | dict[str, t.GeneralValueType],
            ]
            type ExtractionSettings = dict[
                str,
                int | bool | dict[str, t.GeneralValueType],
            ]
            type PerformanceSettings = dict[
                str,
                int | float | bool | dict[str, t.GeneralValueType],
            ]
            type SecuritySettings = dict[
                str,
                str | bool | dict[str, t.GeneralValueType],
            ]
            type StreamSettings = dict[
                str,
                bool | str | list[str] | dict[str, t.GeneralValueType],
            ]

        # =========================================================================
        # SINGER TAP ORACLE PROJECT TYPES - Domain-specific project types extending t
        # =========================================================================

        class Project:
            """Singer Tap Oracle-specific project types.

            Adds Singer tap Oracle-specific project types.
            Follows domain separation principle:
            Singer tap Oracle domain owns Oracle extraction and Singer protocol-specific types.
            """

            # Singer tap Oracle-specific project types extending the generic ones
            type ProjectType = Literal[
                # Generic types inherited from t
                "library",
                "application",
                "service",
                # Singer tap Oracle-specific types
                "singer-tap",
                "oracle-extractor",
                "database-extractor",
                "singer-tap-oracle",
                "tap-oracle",
                "oracle-connector",
                "database-connector",
                "singer-protocol",
                "oracle-etl",
                "database-etl",
                "oracle-integration",
                "singer-stream",
                "etl-tap",
                "data-pipeline",
                "oracle-tap",
                "singer-integration",
            ]

            # Singer tap Oracle-specific project configurations
            type SingerTapOracleProjectConfig = dict[str, t.GeneralValueType]
            type OracleExtractorConfig = dict[str, str | int | bool | list[str]]
            type SingerProtocolConfig = dict[
                str,
                bool | str | dict[str, t.GeneralValueType],
            ]
            type TapOraclePipelineConfig = dict[str, t.GeneralValueType]


# Runtime alias for simplified usage
t = FlextTapOracleTypes

__all__ = [
    "FlextTapOracleTypes",
    "t",
]
