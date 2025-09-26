"""FLEXT Tap Oracle Types - Domain-specific Oracle tap type definitions.

This module provides Oracle tap-specific type definitions extending FlextTypes.
Follows FLEXT standards:
- Domain-specific complex types only
- No simple aliases to primitive types
- Python 3.13+ syntax
- Extends FlextTypes properly

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from typing import Literal

from flext_core import FlextTypes

# =============================================================================
# TAP-ORACLE-SPECIFIC TYPE VARIABLES - Domain-specific TypeVars for Oracle tap operations
# =============================================================================


# Oracle tap domain TypeVars
class FlextTapOracleTypes(FlextTypes):
    """Oracle tap-specific type definitions extending FlextTypes.

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
            str, FlextTypes.Core.ConfigValue | dict[str, object]
        ]
        type ExtractionState = dict[str, FlextTypes.Core.JsonValue | object]
        type ExtractionMetrics = dict[str, int | float | bool | dict[str, object]]
        type BatchConfiguration = dict[
            str, int | bool | dict[str, FlextTypes.Core.ConfigValue]
        ]
        type StreamDefinition = dict[
            str, str | list[str] | dict[str, FlextTypes.Core.JsonValue]
        ]
        type TableMetadata = dict[
            str, FlextTypes.Core.JsonValue | list[dict[str, object]]
        ]

    # =========================================================================
    # ORACLE DATABASE TYPES - Complex database interaction types
    # =========================================================================

    class Database:
        """Oracle database complex types."""

        type DatabaseConfiguration = dict[
            str, str | int | bool | dict[str, FlextTypes.Core.ConfigValue]
        ]
        type ConnectionPool = dict[str, int | bool | dict[str, object]]
        type QueryConfiguration = dict[str, str | int | bool | list[str]]
        type TableSchema = dict[str, list[dict[str, FlextTypes.Core.JsonValue]]]
        type ColumnDefinition = dict[str, str | bool | int | dict[str, object]]
        type IndexInformation = dict[str, str | list[str] | dict[str, object]]

    # =========================================================================
    # SINGER PROTOCOL TYPES - Complex Singer protocol types
    # =========================================================================

    class Singer:
        """Singer protocol complex types."""

        type CatalogEntry = dict[str, str | dict[str, FlextTypes.Core.JsonValue]]
        type StreamSchema = dict[str, dict[str, FlextTypes.Core.JsonValue]]
        type TapConfiguration = dict[
            str, FlextTypes.Core.ConfigValue | dict[str, object]
        ]
        type StateBookmark = dict[str, FlextTypes.Core.JsonValue | object]
        type RecordMessage = dict[str, str | dict[str, FlextTypes.Core.JsonValue]]
        type SchemaMessage = dict[str, str | dict[str, FlextTypes.Core.JsonValue]]

    # =========================================================================
    # ORACLE TAP CONFIGURATION TYPES - Complex configuration types
    # =========================================================================

    class Configuration:
        """Oracle tap configuration complex types."""

        type TapOracleConfig = dict[
            str, FlextTypes.Core.ConfigValue | dict[str, object]
        ]
        type ConnectionSettings = dict[str, str | int | bool | dict[str, object]]
        type ExtractionSettings = dict[
            str, int | bool | dict[str, FlextTypes.Core.ConfigValue]
        ]
        type PerformanceSettings = dict[str, int | float | bool | dict[str, object]]
        type SecuritySettings = dict[
            str, str | bool | dict[str, FlextTypes.Core.ConfigValue]
        ]
        type StreamSettings = dict[str, bool | str | list[str] | dict[str, object]]

    # =========================================================================
    # SINGER TAP ORACLE PROJECT TYPES - Domain-specific project types extending FlextTypes
    # =========================================================================

    class Project(FlextTypes.Project):
        """Singer Tap Oracle-specific project types extending FlextTypes.Project.

        Adds Singer tap Oracle-specific project types while inheriting
        generic types from FlextTypes. Follows domain separation principle:
        Singer tap Oracle domain owns Oracle extraction and Singer protocol-specific types.
        """

        # Singer tap Oracle-specific project types extending the generic ones
        type ProjectType = Literal[
            # Generic types inherited from FlextTypes.Project
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
            str, FlextTypes.Core.ConfigValue | object
        ]
        type OracleExtractorConfig = dict[str, str | int | bool | list[str]]
        type SingerProtocolConfig = dict[str, bool | str | dict[str, object]]
        type TapOraclePipelineConfig = dict[str, FlextTypes.Core.ConfigValue | object]


# =============================================================================
# PUBLIC API EXPORTS - Oracle tap TypeVars and types
# =============================================================================

__all__: list[str] = [
    "FlextTapOracleTypes",
]
