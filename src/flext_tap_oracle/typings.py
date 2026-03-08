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

from flext_db_oracle.typings import FlextDbOracleTypes
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

        type MeltanoTapOracleProjectType = Literal[
            "library",
            "application",
            "service",
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

        class Extraction:
            """Oracle extraction complex types."""

            type ExtractionConfiguration = dict[
                str, t.ContainerValue | t.ConfigurationMapping
            ]
            type ExtractionState = dict[str, t.JsonValue | t.ContainerValue]
            type ExtractionMetrics = dict[
                str, int | float | bool | t.ConfigurationMapping
            ]
            type BatchConfiguration = dict[str, int | bool | t.ConfigurationMapping]
            type StreamDefinition = dict[str, str | list[str] | dict[str, t.JsonValue]]
            type TableMetadata = dict[str, t.JsonValue | list[t.ConfigurationMapping]]

        class Singer:
            """Singer protocol complex types."""

            type CatalogEntry = dict[str, str | dict[str, t.JsonValue]]
            type StreamSchema = dict[str, dict[str, t.JsonValue]]
            type TapConfiguration = dict[str, t.ContainerValue | t.ConfigurationMapping]
            type StateBookmark = dict[str, t.JsonValue | t.ContainerValue]
            type RecordMessage = dict[str, str | dict[str, t.JsonValue]]
            type SchemaMessage = dict[str, str | dict[str, t.JsonValue]]

        class Configuration:
            """Oracle tap configuration complex types."""

            type TapOracleConfig = dict[str, t.ContainerValue | t.ConfigurationMapping]
            type ConnectionSettings = dict[
                str, str | int | bool | t.ConfigurationMapping
            ]
            type ExtractionSettings = dict[str, int | bool | t.ConfigurationMapping]
            type PerformanceSettings = dict[
                str, int | float | bool | t.ConfigurationMapping
            ]
            type SecuritySettings = dict[str, str | bool | t.ConfigurationMapping]
            type StreamSettings = dict[
                str, bool | str | list[str] | t.ConfigurationMapping
            ]

        class Project:
            """Singer Tap Oracle-specific project types.

            Adds Singer tap Oracle-specific project types.
            Follows domain separation principle:
            Singer tap Oracle domain owns Oracle extraction and Singer protocol-specific types.
            """

            type ProjectType = Literal[
                "library",
                "application",
                "service",
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
            type SingerTapOracleProjectConfig = dict[str, t.ContainerValue]
            type OracleExtractorConfig = dict[str, str | int | bool | list[str]]
            type SingerProtocolConfig = dict[str, bool | str | t.ConfigurationMapping]
            type TapOraclePipelineConfig = dict[str, t.ContainerValue]


t = FlextTapOracleTypes
__all__ = ["FlextTapOracleTypes", "t"]
