"""FLEXT Tap Oracle Types - Domain-specific Oracle tap type definitions.

This module provides Oracle tap-specific type definitions extending FlextCore.Types.
Follows FLEXT standards:
- Domain-specific complex types only
- No simple aliases to primitive types
- Python 3.13+ syntax
- Extends FlextCore.Types properly

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from typing import Literal

from flext_core import FlextCore

# =============================================================================
# TAP-ORACLE-SPECIFIC TYPE VARIABLES - Domain-specific TypeVars for Oracle tap operations
# =============================================================================


# Oracle tap domain TypeVars
class FlextMeltanoTapOracleTypes(FlextCore.Types):
    """Oracle tap-specific type definitions extending FlextCore.Types.

    Domain-specific type system for Oracle database extraction operations.
    Contains ONLY complex Oracle tap-specific types, no simple aliases.
    Uses Python 3.13+ type syntax and patterns.
    """

    # =========================================================================
    # ORACLE TAP EXTRACTION TYPES - Complex extraction operation types
    # =========================================================================

    class Extraction:
        """Oracle extraction complex types."""

        type ExtractionConfiguration = dict[
            str, FlextCore.Types.ConfigValue | FlextCore.Types.Dict
        ]
        type ExtractionState = dict[str, FlextCore.Types.JsonValue | object]
        type ExtractionMetrics = dict[str, int | float | bool | FlextCore.Types.Dict]
        type BatchConfiguration = dict[
            str, int | bool | dict[str, FlextCore.Types.ConfigValue]
        ]
        type StreamDefinition = dict[
            str, str | FlextCore.Types.StringList | dict[str, FlextCore.Types.JsonValue]
        ]
        type TableMetadata = dict[
            str, FlextCore.Types.JsonValue | list[FlextCore.Types.Dict]
        ]

    # =========================================================================
    # ORACLE DATABASE TYPES - Complex database interaction types
    # =========================================================================

    class Database:
        """Oracle database complex types."""

        type DatabaseConfiguration = dict[
            str, str | int | bool | dict[str, FlextCore.Types.ConfigValue]
        ]
        type ConnectionPool = dict[str, int | bool | FlextCore.Types.Dict]
        type QueryConfiguration = dict[
            str, str | int | bool | FlextCore.Types.StringList
        ]
        type TableSchema = dict[str, list[dict[str, FlextCore.Types.JsonValue]]]
        type ColumnDefinition = dict[str, str | bool | int | FlextCore.Types.Dict]
        type IndexInformation = dict[
            str, str | FlextCore.Types.StringList | FlextCore.Types.Dict
        ]

    # =========================================================================
    # SINGER PROTOCOL TYPES - Complex Singer protocol types
    # =========================================================================

    class Singer:
        """Singer protocol complex types."""

        type CatalogEntry = dict[str, str | dict[str, FlextCore.Types.JsonValue]]
        type StreamSchema = dict[str, dict[str, FlextCore.Types.JsonValue]]
        type TapConfiguration = dict[
            str, FlextCore.Types.ConfigValue | FlextCore.Types.Dict
        ]
        type StateBookmark = dict[str, FlextCore.Types.JsonValue | object]
        type RecordMessage = dict[str, str | dict[str, FlextCore.Types.JsonValue]]
        type SchemaMessage = dict[str, str | dict[str, FlextCore.Types.JsonValue]]

    # =========================================================================
    # ORACLE TAP CONFIGURATION TYPES - Complex configuration types
    # =========================================================================

    class Configuration:
        """Oracle tap configuration complex types."""

        type TapOracleConfig = dict[
            str, FlextCore.Types.ConfigValue | FlextCore.Types.Dict
        ]
        type ConnectionSettings = dict[str, str | int | bool | FlextCore.Types.Dict]
        type ExtractionSettings = dict[
            str, int | bool | dict[str, FlextCore.Types.ConfigValue]
        ]
        type PerformanceSettings = dict[str, int | float | bool | FlextCore.Types.Dict]
        type SecuritySettings = dict[
            str, str | bool | dict[str, FlextCore.Types.ConfigValue]
        ]
        type StreamSettings = dict[
            str, bool | str | FlextCore.Types.StringList | FlextCore.Types.Dict
        ]

    # =========================================================================
    # SINGER TAP ORACLE PROJECT TYPES - Domain-specific project types extending FlextCore.Types
    # =========================================================================

    class Project(FlextCore.Types.Project):
        """Singer Tap Oracle-specific project types extending FlextCore.Types.Project.

        Adds Singer tap Oracle-specific project types while inheriting
        generic types from FlextCore.Types. Follows domain separation principle:
        Singer tap Oracle domain owns Oracle extraction and Singer protocol-specific types.
        """

        # Singer tap Oracle-specific project types extending the generic ones
        type ProjectType = Literal[
            # Generic types inherited from FlextCore.Types.Project
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
        type SingerTapOracleProjectConfig = dict[
            str, FlextCore.Types.ConfigValue | object
        ]
        type OracleExtractorConfig = dict[
            str, str | int | bool | FlextCore.Types.StringList
        ]
        type SingerProtocolConfig = dict[str, bool | str | FlextCore.Types.Dict]
        type TapOraclePipelineConfig = dict[str, FlextCore.Types.ConfigValue | object]


# =============================================================================
# PUBLIC API EXPORTS - Oracle tap TypeVars and types
# =============================================================================

__all__: FlextCore.Types.StringList = [
    "FlextMeltanoTapOracleTypes",
]
