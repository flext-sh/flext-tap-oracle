"""Models for flext-tap-oracle.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT

"""

from __future__ import annotations

from collections.abc import Sequence
from datetime import datetime
from typing import Annotated, ClassVar, Literal, Self

from flext_core import r
from flext_db_oracle import FlextDbOracleModels
from flext_meltano import FlextMeltanoModels
from pydantic import (
    ConfigDict,
    Field,
    computed_field,
    field_validator,
    model_validator,
)

from flext_tap_oracle import c, t


class FlextTapOracleModels(FlextMeltanoModels, FlextDbOracleModels):
    """Complete models for Oracle tap operations extending FlextMeltanoModels.

    Provides standardized models for all Oracle tap domain entities including:
    - Singer stream metadata and configuration
    - Oracle table extraction configuration
    - Replication and discovery operations
    - Performance monitoring and metrics
    - Singer protocol compliance models

    All nested classes inherit FlextMeltanoModels validation and patterns.
    """

    class TapOracle:
        """Tap Oracle  namespace for cross-project access."""

        # Pydantic 2.11 Configuration - Enterprise Singer Oracle Tap Features
        model_config: ClassVar[ConfigDict] = ConfigDict(
            validate_assignment=True,
            use_enum_values=True,
            arbitrary_types_allowed=True,
            extra="forbid",
            frozen=False,
            validate_return=True,
            ser_json_timedelta="iso8601",
            ser_json_bytes="base64",
            hide_input_in_errors=True,
            json_schema_extra={
                "title": "FLEXT Singer Oracle Tap Models",
                "description": "Enterprise Oracle database extraction models with Singer protocol compliance",
                "examples": [
                    {
                        "tap_name": "tap-oracle",
                        "extraction_mode": "incremental_replication",
                        "oracle_connection": "oracle://user@host:1521/service",
                    },
                ],
                "tags": ["singer", "oracle", "tap", "extraction", "database"],
                "version": "2.11.0",
            },
        )

        # Oracle Tap Domain - namespace metadata as static methods on plain class

        @staticmethod
        def get_active_model_names() -> Sequence[str]:
            """List of active Oracle tap model names."""
            return [
                "OracleTapStreamMetadata",
                "OracleTapDiscoveryConfig",
                "OracleTapExtractionConfig",
                "OracleTapPerformanceMetrics",
                "OracleTapStreamInfo",
                "OracleTapDiscoveryResult",
                "OracleTapExecutionStats",
                "OracleConnection",
                "OracleQuery",
                "OracleRecord",
            ]

        @staticmethod
        def get_system_summary() -> t.TapOracle.Summary.SummaryData:
            """Complete Singer Oracle tap system summary with database extraction capabilities."""
            return {
                "total_models": len(
                    FlextTapOracleModels.TapOracle.get_active_model_names(),
                ),
                "tap_type": "singer_oracle_database_extractor",
                "extraction_features": [
                    "oracle_table_discovery",
                    "incremental_replication",
                    "full_table_extraction",
                    "schema_introspection",
                    "performance_monitoring",
                    "connection_pooling",
                ],
                "singer_compliance": {
                    "protocol_version": "singer_v1",
                    "stream_discovery": True,
                    "catalog_generation": True,
                    "state_management": True,
                    "incremental_bookmarking": True,
                },
                "oracle_capabilities": {
                    "connection_pooling": True,
                    "query_optimization": True,
                    "batch_processing": True,
                    "type_mapping": True,
                    "schema_discovery": True,
                },
            }

        class OracleTapStreamMetadata(FlextMeltanoModels.Entity):
            """Oracle tap stream metadata with Singer protocol compliance.

            Extends Oracle table metadata with tap-specific information
            for Singer streaming operations and replication configuration.
            """

            # Pydantic 2.11 Configuration - Stream Metadata Features
            model_config: ClassVar[ConfigDict] = ConfigDict(
                validate_assignment=True,
                extra="forbid",
                frozen=False,
                json_schema_extra={
                    "description": "Oracle Singer stream metadata with replication support",
                    "examples": [
                        {
                            "stream_name": "users",
                            "table_name": "USERS",
                            "replication_method": "INCREMENTAL",
                        },
                    ],
                },
            )

            # Singer stream configuration
            stream_name: Annotated[str, Field(..., description="Singer stream name")]
            replication_method: Annotated[
                Literal["FULL_TABLE", "INCREMENTAL"],
                Field(
                    default="FULL_TABLE",
                    description="Replication method for this stream",
                ),
            ]
            replication_key: Annotated[
                str | None,
                Field(
                    default=None,
                    description="Column used for incremental replication",
                ),
            ]
            is_selected: Annotated[
                bool,
                Field(
                    default=True,
                    description="Whether stream is selected for extraction",
                ),
            ]

            # Oracle-specific metadata
            table_name: Annotated[str, Field(..., description="Oracle table name")]
            schema_name: Annotated[
                str | None,
                Field(
                    default=None,
                    description="Oracle schema name",
                ),
            ]
            estimated_rows: Annotated[
                int | None,
                Field(
                    default=None,
                    description="Estimated row count",
                ),
            ]
            column_count: Annotated[
                int | None,
                Field(
                    default=None,
                    description="Number of columns",
                ),
            ]

            @computed_field
            def stream_metadata_summary(self) -> t.TapOracle.Summary.SummaryData:
                """Oracle stream metadata summary."""
                estimated_volume: dict[str, t.NormalizedValue] = {}
                if self.estimated_rows is not None:
                    estimated_volume["rows"] = self.estimated_rows
                if self.column_count is not None:
                    estimated_volume["columns"] = self.column_count
                return {
                    "stream_name": self.stream_name,
                    "table_reference": f"{self.schema_name}.{self.table_name}"
                    if self.schema_name
                    else self.table_name,
                    "extraction_type": self.replication_method,
                    "is_incremental": self.replication_method == "INCREMENTAL",
                    "replication_column": self.replication_key,
                    "selected_for_extraction": self.is_selected,
                    "estimated_volume": estimated_volume,
                }

            @field_validator("stream_name")
            @classmethod
            def validate_stream_name(cls, v: str) -> str:
                """Validate stream name follows Singer conventions."""
                if not v or not v.strip():
                    msg = "Stream name cannot be empty"
                    raise ValueError(msg)

                # Enhanced validation with proper limits
                max_length = c.TapOracle.MAX_IDENTIFIER_LENGTH
                if len(v) > max_length:
                    msg = f"Stream name too long: {len(v)} > {max_length} characters"
                    raise ValueError(msg)

                if v.startswith(("_", "-")) or v.endswith(("_", "-")):
                    msg = "Stream name cannot start/end with underscore or dash"
                    raise ValueError(msg)

                # Clean invalid characters for Singer streams
                cleaned = "".join(c if c.isalnum() or c in "_-" else "_" for c in v)
                return cleaned.lower()

            def validate_business_rules(self) -> r[bool]:
                """Validate tap-specific business rules."""
                return r[bool].ok(value=True)

            @model_validator(mode="after")
            def validate_replication_consistency(self) -> Self:
                """Validate replication configuration consistency."""
                if self.replication_method == "INCREMENTAL":
                    if not self.replication_key:
                        msg = "Incremental replication requires a replication_key"
                        raise ValueError(msg)

                    # Validation for replication key length
                    max_key_length = c.TapOracle.MAX_IDENTIFIER_LENGTH
                    if len(self.replication_key) > max_key_length:
                        msg = f"Replication key too long: {len(self.replication_key)} > {max_key_length}"
                        raise ValueError(msg)

                elif self.replication_method == "FULL_TABLE" and self.replication_key:
                    msg = "Full table replication should not have replication_key"
                    raise ValueError(msg)

                return self

            @model_validator(mode="after")
            def validate_stream_metadata(self) -> Self:
                """Validate Oracle stream metadata."""
                if (
                    self.replication_method == "INCREMENTAL"
                    and not self.replication_key
                ):
                    msg = "Incremental replication requires a replication_key"
                    raise ValueError(msg)
                if self.replication_method == "FULL_TABLE" and self.replication_key:
                    msg = "Full table replication should not have replication_key"
                    raise ValueError(msg)
                return self

        class OracleTapDiscoveryConfig(FlextMeltanoModels.Entity):
            """Configuration for Oracle tap discovery operations."""

            # Pydantic 2.11 Configuration - Discovery Features
            model_config: ClassVar[ConfigDict] = ConfigDict(
                validate_assignment=True,
                extra="forbid",
                frozen=False,
                json_schema_extra={
                    "description": "Oracle database discovery configuration",
                    "examples": [
                        {
                            "schema_names": ["HR", "SALES"],
                            "include_views": True,
                            "max_tables": 100,
                        },
                    ],
                },
            )

            # Discovery scope
            schema_names: Annotated[
                Sequence[str],
                Field(
                    default_factory=list,
                    description="Oracle schemas to discover",
                ),
            ]
            table_patterns: Annotated[
                Sequence[str],
                Field(
                    default_factory=list,
                    description="Table name patterns to include",
                ),
            ]
            exclude_patterns: Annotated[
                Sequence[str],
                Field(
                    default_factory=list,
                    description="Table name patterns to exclude",
                ),
            ]

            # Discovery options
            include_views: Annotated[
                bool,
                Field(
                    default=False,
                    description="Include Oracle views in discovery",
                ),
            ]
            include_system_tables: Annotated[
                bool,
                Field(
                    default=False,
                    description="Include system tables in discovery",
                ),
            ]
            max_tables: Annotated[
                int,
                Field(
                    default=c.DEFAULT_SIZE,
                    description="Maximum number of tables to discover",
                ),
            ]

            # Performance settings
            discovery_timeout: Annotated[
                int,
                Field(
                    default=c.DEFAULT_TIMEOUT_SECONDS * 10,
                    description="Discovery timeout in seconds",
                ),
            ]
            parallel_discovery: Annotated[
                bool,
                Field(
                    default=True,
                    description="Enable parallel discovery",
                ),
            ]

            @computed_field
            def discovery_scope_summary(self) -> t.TapOracle.Summary.SummaryData:
                """Oracle discovery scope summary."""
                return {
                    "target_schemas": len(self.schema_names),
                    "include_patterns": len(self.table_patterns),
                    "exclude_patterns": len(self.exclude_patterns),
                    "discovery_options": {
                        "include_views": self.include_views,
                        "include_system_tables": self.include_system_tables,
                        "max_tables": self.max_tables,
                    },
                    "performance": {
                        "timeout_seconds": self.discovery_timeout,
                        "parallel_enabled": self.parallel_discovery,
                    },
                }

            @model_validator(mode="after")
            def validate_discovery_config(self) -> Self:
                """Validate Oracle discovery configuration."""
                if self.max_tables <= 0:
                    msg = "Max tables must be positive"
                    raise ValueError(msg)
                if self.discovery_timeout <= 0:
                    msg = "Discovery timeout must be positive"
                    raise ValueError(msg)
                return self

        class OracleTapExtractionConfig(FlextMeltanoModels.Entity):
            """Configuration for Oracle tap extraction operations."""

            # Pydantic 2.11 Configuration - Extraction Features
            model_config: ClassVar[ConfigDict] = ConfigDict(
                validate_assignment=True,
                extra="forbid",
                frozen=False,
                json_schema_extra={
                    "description": "Oracle database extraction configuration",
                    "examples": [
                        {
                            "batch_size": 10000,
                            "parallel_streams": 4,
                            "incremental_column": "UPDATED_AT",
                        },
                    ],
                },
            )

            # Extraction parameters
            batch_size: Annotated[
                int,
                Field(
                    default=c.DEFAULT_SIZE * 10,
                    description="Number of rows per batch",
                ),
            ]
            max_rows: Annotated[
                int | None,
                Field(
                    default=None,
                    description="Maximum rows to extract (None for unlimited)",
                ),
            ]

            # Performance optimization
            parallel_streams: Annotated[
                int,
                Field(
                    default=1,
                    description="Number of parallel extraction streams",
                ),
            ]
            enable_query_hints: Annotated[
                bool,
                Field(
                    default=True,
                    description="Enable Oracle query optimization hints",
                ),
            ]

            # Incremental extraction
            incremental_column: Annotated[
                str | None,
                Field(
                    default=None,
                    description="Column for incremental extraction",
                ),
            ]
            incremental_bookmark: Annotated[
                str | None,
                Field(
                    default=None,
                    description="Bookmark value for incremental extraction",
                ),
            ]

            @computed_field
            def extraction_config_summary(self) -> t.TapOracle.Summary.SummaryData:
                """Oracle extraction configuration summary."""
                return {
                    "batch_processing": {
                        "batch_size": self.batch_size,
                        "max_rows": self.max_rows,
                        "unlimited": self.max_rows is None,
                    },
                    "performance": {
                        "parallel_streams": self.parallel_streams,
                        "query_hints_enabled": self.enable_query_hints,
                    },
                    "incremental_settings": {
                        "column": self.incremental_column,
                        "bookmark": self.incremental_bookmark,
                        "incremental_enabled": bool(self.incremental_column),
                    },
                }

            @model_validator(mode="after")
            def validate_extraction_config(self) -> Self:
                """Validate Oracle extraction configuration."""
                if self.batch_size <= 0:
                    msg = "Batch size must be positive"
                    raise ValueError(msg)
                if self.parallel_streams <= 0:
                    msg = "Parallel streams must be positive"
                    raise ValueError(msg)
                if self.max_rows is not None and self.max_rows <= 0:
                    msg = "Max rows must be positive when specified"
                    raise ValueError(msg)
                return self

        class OracleTapPerformanceMetrics(FlextMeltanoModels.Entity):
            """Performance metrics for Oracle tap operations."""

            # Pydantic 2.11 Configuration - Performance Features
            model_config: ClassVar[ConfigDict] = ConfigDict(
                validate_assignment=True,
                extra="forbid",
                frozen=False,
                json_schema_extra={
                    "description": "Oracle tap performance metrics with complete monitoring",
                    "examples": [
                        {
                            "extraction_id": "ext_123",
                            "total_records": 50000,
                            "avg_records_per_second": 1000.0,
                        },
                    ],
                },
            )

            # Extraction metrics
            extraction_id: Annotated[
                str,
                Field(description="Unique extraction identifier"),
            ]
            start_time: Annotated[str, Field(description="Extraction start timestamp")]
            end_time: Annotated[
                str | None,
                Field(
                    default=None,
                    description="Extraction end timestamp",
                ),
            ]

            # Volume metrics
            total_records: Annotated[
                int,
                Field(default=0, description="Total records extracted"),
            ]
            total_bytes: Annotated[
                int,
                Field(default=0, description="Total bytes processed"),
            ]
            streams_processed: Annotated[
                int,
                Field(
                    default=0,
                    description="Number of streams processed",
                ),
            ]

            # Performance metrics
            avg_records_per_second: Annotated[
                float,
                Field(
                    default=0.0,
                    description="Average records per second",
                ),
            ]
            avg_bytes_per_second: Annotated[
                float,
                Field(
                    default=0.0,
                    description="Average bytes per second",
                ),
            ]

            # Oracle-specific metrics
            oracle_connection_time: Annotated[
                float,
                Field(
                    default=0.0,
                    description="Oracle connection establishment time",
                ),
            ]
            oracle_query_time: Annotated[
                float,
                Field(
                    default=0.0,
                    description="Total Oracle query execution time",
                ),
            ]

            @computed_field
            def performance_analysis_summary(
                self,
            ) -> t.TapOracle.Summary.SummaryData:
                """Oracle tap performance analysis summary."""
                duration = 0.0
                if self.start_time and self.end_time:
                    start = datetime.fromisoformat(self.start_time)
                    end = datetime.fromisoformat(self.end_time)
                    duration = (end - start).total_seconds()

                return {
                    "extraction_performance": {
                        "extraction_id": self.extraction_id,
                        "duration_seconds": duration,
                        "records_extracted": self.total_records,
                        "bytes_processed": self.total_bytes,
                        "streams_processed": self.streams_processed,
                    },
                    "throughput": {
                        "records_per_second": self.avg_records_per_second,
                        "bytes_per_second": self.avg_bytes_per_second,
                        "mbps": self.avg_bytes_per_second / (1024 * 1024),
                    },
                    "oracle_metrics": {
                        "connection_time": self.oracle_connection_time,
                        "query_time": self.oracle_query_time,
                        "query_efficiency": self.oracle_query_time / duration
                        if duration > 0
                        else 0,
                    },
                }

            @model_validator(mode="after")
            def validate_performance_metrics(self) -> Self:
                """Validate Oracle performance metrics."""
                if self.total_records < 0:
                    msg = "Total records cannot be negative"
                    raise ValueError(msg)
                if self.total_bytes < 0:
                    msg = "Total bytes cannot be negative"
                    raise ValueError(msg)
                return self

        class OracleTapStreamInfo(FlextMeltanoModels.Entity):
            """Oracle tap stream information - aggregates tap and Oracle metadata.

            This model combines Oracle table metadata with tap-specific stream configuration
            to provide a complete view of stream information for the tap.
            """

            # Pydantic 2.11 Configuration - Stream Info Features
            model_config: ClassVar[ConfigDict] = ConfigDict(
                validate_assignment=True,
                extra="forbid",
                frozen=False,
                json_schema_extra={
                    "description": "Oracle tap stream with complete metadata",
                    "examples": [
                        {
                            "stream_name": "users",
                            "table_name": "USERS",
                            "replication_method": "INCREMENTAL",
                        },
                    ],
                },
            )

            # Stream identity
            stream_name: Annotated[str, Field(..., description="Singer stream name")]
            table_name: Annotated[str, Field(..., description="Oracle table name")]
            schema_name: Annotated[
                str | None,
                Field(None, description="Oracle schema name"),
            ]

            # Stream configuration
            is_selected: Annotated[
                bool,
                Field(
                    default=True,
                    description="Whether stream is selected for extraction",
                ),
            ]
            replication_method: Annotated[
                Literal["FULL_TABLE", "INCREMENTAL"],
                Field(
                    default="FULL_TABLE",
                    description="Replication method for this stream",
                ),
            ]
            replication_key: Annotated[
                str | None,
                Field(
                    None,
                    description="Column used for incremental replication",
                ),
            ]

            # Runtime information (populated at runtime)
            estimated_rows: Annotated[
                int | None,
                Field(None, description="Estimated row count"),
            ]
            column_count: Annotated[
                int | None,
                Field(None, description="Number of columns"),
            ]
            last_extracted: Annotated[
                str | None,
                Field(
                    None,
                    description="Last extraction timestamp",
                ),
            ]

            @computed_field
            def stream_info_summary(self) -> t.TapOracle.Summary.SummaryData:
                """Oracle stream information summary."""
                return {
                    "stream_identity": {
                        "name": self.stream_name,
                        "table": self.table_name,
                        "schema": self.schema_name,
                        "full_reference": f"{self.schema_name}.{self.table_name}"
                        if self.schema_name
                        else self.table_name,
                    },
                    "extraction_config": {
                        "selected": self.is_selected,
                        "replication_method": self.replication_method,
                        "replication_key": self.replication_key,
                        "is_incremental": self.replication_method == "INCREMENTAL",
                    },
                    "table_metadata": {
                        "estimated_rows": self.estimated_rows,
                        "column_count": self.column_count,
                        "last_extracted": self.last_extracted,
                    },
                }

            def to_singer_stream_info(self) -> t.TapOracle.Summary.SummaryData:
                """Convert to Singer stream information format."""
                return {
                    "tap_stream_id": self.stream_name,
                    "table_name": self.table_name,
                    "schema": self.schema_name,
                    "metadata": {
                        "replication-method": self.replication_method,
                        "replication-key": self.replication_key,
                        "selected": self.is_selected,
                    },
                    "stats": {
                        "estimated_rows": self.estimated_rows,
                        "column_count": self.column_count,
                        "last_extracted": self.last_extracted,
                    },
                }

            def validate_business_rules(self) -> r[bool]:
                """Validate stream info business rules."""
                return r[bool].ok(value=True)

            @model_validator(mode="after")
            def validate_stream_info(self) -> Self:
                """Validate Oracle stream information."""
                if not self.stream_name:
                    msg = "Stream name is required"
                    raise ValueError(msg)
                if not self.table_name:
                    msg = "Table name is required"
                    raise ValueError(msg)
                return self

        class OracleTapDiscoveryResult(FlextMeltanoModels.Entity):
            """Result of Oracle table discovery operation.

            Aggregates discovery results with both raw Oracle metadata and
            processed tap stream information.
            """

            # Pydantic 2.11 Configuration - Discovery Result Features
            model_config: ClassVar[ConfigDict] = ConfigDict(
                validate_assignment=True,
                extra="forbid",
                frozen=False,
                json_schema_extra={
                    "description": "Oracle discovery result with complete metadata",
                    "examples": [
                        {
                            "schema_name": "HR",
                            "total_tables": 15,
                            "discovery_timestamp": "2023-01-01T00:00:00Z",
                        },
                    ],
                },
            )

            # Discovery metadata
            schema_name: Annotated[
                str,
                Field(
                    ...,
                    description="Oracle schema that was discovered",
                ),
            ]
            discovery_timestamp: Annotated[
                str,
                Field(
                    ...,
                    description="When discovery was performed",
                ),
            ]
            total_tables: Annotated[
                int,
                Field(
                    ...,
                    description="Total number of tables discovered",
                ),
            ]

            # Raw Oracle metadata
            oracle_tables: Annotated[
                Sequence[FlextDbOracleModels.DbOracle.Table],
                Field(
                    default_factory=list,
                    description="Raw Oracle table metadata from flext-db-oracle",
                ),
            ]

            # Processed stream information
            stream_info: Annotated[
                Sequence[FlextTapOracleModels.TapOracle.OracleTapStreamInfo],
                Field(
                    default_factory=list,
                    description="Processed stream information for tap use",
                ),
            ]

            # Filtering results
            filtered_tables: Annotated[
                Sequence[str],
                Field(
                    default_factory=list,
                    description="Table names after applying filters",
                ),
            ]
            excluded_tables: Annotated[
                Sequence[str],
                Field(
                    default_factory=list,
                    description="Table names that were excluded",
                ),
            ]

            @computed_field
            def discovery_result_summary(self) -> t.TapOracle.Summary.SummaryData:
                """Oracle discovery result summary."""
                selected_streams = len([s for s in self.stream_info if s.is_selected])

                return {
                    "discovery_metadata": {
                        "schema": self.schema_name,
                        "timestamp": self.discovery_timestamp,
                        "total_tables_found": self.total_tables,
                    },
                    "processing_results": {
                        "raw_tables": len(self.oracle_tables),
                        "stream_configurations": len(self.stream_info),
                        "selected_streams": selected_streams,
                        "excluded_tables": len(self.excluded_tables),
                    },
                    "filtering_efficiency": {
                        "inclusion_rate": len(self.filtered_tables) / self.total_tables
                        if self.total_tables > 0
                        else 0,
                        "exclusion_rate": len(self.excluded_tables) / self.total_tables
                        if self.total_tables > 0
                        else 0,
                        "selection_rate": selected_streams / len(self.stream_info)
                        if self.stream_info
                        else 0,
                    },
                }

            def get_selected_streams(
                self,
            ) -> Sequence[m.TapOracle.OracleTapStreamInfo]:
                """Get only selected streams."""
                return [stream for stream in self.stream_info if stream.is_selected]

            def get_table_by_name(
                self,
                table_name: str,
            ) -> FlextDbOracleModels.DbOracle.Table | None:
                """Get Oracle table metadata by name."""
                for table in self.oracle_tables:
                    if table.name == table_name:
                        return table
                return None

            def to_singer_catalog(self) -> t.TapOracle.Summary.SummaryData:
                """Convert to Singer catalog format."""
                return {
                    "streams": [
                        stream.to_singer_stream_info() for stream in self.stream_info
                    ],
                    "metadata": {
                        "schema": self.schema_name,
                        "discovery_timestamp": self.discovery_timestamp,
                        "total_tables": self.total_tables,
                    },
                }

            def validate_business_rules(self) -> r[bool]:
                """Validate discovery result business rules."""
                return r[bool].ok(value=True)

            @model_validator(mode="after")
            def validate_discovery_result(self) -> Self:
                """Validate Oracle discovery result."""
                if not self.schema_name:
                    msg = "Schema name is required"
                    raise ValueError(msg)
                if self.total_tables < 0:
                    msg = "Total tables cannot be negative"
                    raise ValueError(msg)
                return self

        class OracleTapExecutionStats(FlextMeltanoModels.Entity):
            """Oracle tap execution statistics and metrics.

            Tracks runtime statistics for tap execution, performance metrics,
            and operational information.
            """

            # Pydantic 2.11 Configuration - Execution Stats Features
            model_config: ClassVar[ConfigDict] = ConfigDict(
                validate_assignment=True,
                extra="forbid",
                frozen=False,
                json_schema_extra={
                    "description": "Oracle tap execution statistics with performance tracking",
                    "examples": [
                        {
                            "execution_id": "exec_123",
                            "streams_processed": 5,
                            "total_records": 100000,
                        },
                    ],
                },
            )

            # Execution metadata
            execution_id: Annotated[
                str,
                Field(..., description="Unique execution identifier"),
            ]
            start_timestamp: Annotated[
                str,
                Field(..., description="Execution start time"),
            ]
            end_timestamp: Annotated[
                str | None,
                Field(None, description="Execution end time"),
            ]

            # Stream statistics
            streams_processed: Annotated[
                int,
                Field(
                    default=0,
                    description="Number of streams processed",
                ),
            ]
            total_records: Annotated[
                int,
                Field(default=0, description="Total records extracted"),
            ]
            total_bytes: Annotated[
                int,
                Field(default=0, description="Total bytes processed"),
            ]

            # Performance metrics
            avg_records_per_second: Annotated[
                float,
                Field(
                    default=0.0,
                    description="Average records per second",
                ),
            ]
            avg_bytes_per_second: Annotated[
                float,
                Field(
                    default=0.0,
                    description="Average bytes per second",
                ),
            ]
            duration_seconds: Annotated[
                float,
                Field(
                    default=0.0,
                    description="Total execution duration",
                ),
            ]

            # Error tracking
            errors_encountered: Annotated[
                int,
                Field(
                    default=0,
                    description="Number of errors encountered",
                ),
            ]
            failed_streams: Annotated[
                Sequence[str],
                Field(
                    default_factory=list,
                    description="Names of failed streams",
                ),
            ]

            # Oracle-specific metrics
            oracle_connection_time: Annotated[
                float,
                Field(
                    default=0.0,
                    description="Oracle connection time",
                ),
            ]
            oracle_query_time: Annotated[
                float,
                Field(
                    default=0.0,
                    description="Total Oracle query time",
                ),
            ]
            oracle_result_processing_time: Annotated[
                float,
                Field(
                    default=0.0,
                    description="Result processing time",
                ),
            ]

            @computed_field
            def execution_stats_summary(self) -> t.TapOracle.Summary.SummaryData:
                """Oracle tap execution statistics summary."""
                success_rate = 0.0
                if self.streams_processed > 0:
                    successful_streams = self.streams_processed - len(
                        self.failed_streams,
                    )
                    success_rate = successful_streams / self.streams_processed

                return {
                    "execution_overview": {
                        "execution_id": self.execution_id,
                        "duration_seconds": self.duration_seconds,
                        "status": "completed" if self.end_timestamp else "running",
                    },
                    "volume_metrics": {
                        "streams_processed": self.streams_processed,
                        "total_records": self.total_records,
                        "total_bytes": self.total_bytes,
                        "avg_records_per_stream": self.total_records
                        / self.streams_processed
                        if self.streams_processed > 0
                        else 0,
                    },
                    "performance_metrics": {
                        "records_per_second": self.avg_records_per_second,
                        "bytes_per_second": self.avg_bytes_per_second,
                        "mbps": self.avg_bytes_per_second / (1024 * 1024),
                    },
                    "quality_metrics": {
                        "success_rate": success_rate,
                        "errors_encountered": self.errors_encountered,
                        "failed_streams": len(self.failed_streams),
                        "error_rate": self.errors_encountered / self.total_records
                        if self.total_records > 0
                        else 0,
                    },
                    "oracle_metrics": {
                        "connection_time": self.oracle_connection_time,
                        "query_time": self.oracle_query_time,
                        "processing_time": self.oracle_result_processing_time,
                        "query_efficiency": self.oracle_query_time
                        / self.duration_seconds
                        if self.duration_seconds > 0
                        else 0,
                    },
                }

            def add_stream_stats(
                self,
                records: int,
                bytes_processed: int,
                processing_time: float,
            ) -> m.TapOracle.OracleTapExecutionStats:
                """Return new instance with added statistics for a processed stream."""
                updated = self.model_copy(
                    update={
                        "streams_processed": self.streams_processed + 1,
                        "total_records": self.total_records + records,
                        "total_bytes": self.total_bytes + bytes_processed,
                        "oracle_result_processing_time": self.oracle_result_processing_time
                        + processing_time,
                    },
                )
                return updated.update_performance_metrics()

            def mark_stream_error(
                self,
                stream_name: str,
            ) -> m.TapOracle.OracleTapExecutionStats:
                """Return new instance with marked stream error."""
                new_failed_streams: list[str] = (
                    list(self.failed_streams)
                    if self.failed_streams
                    else []
                )
                if stream_name not in new_failed_streams:
                    new_failed_streams.append(stream_name)
                return self.model_copy(
                    update={
                        "errors_encountered": self.errors_encountered + 1,
                        "failed_streams": new_failed_streams,
                    },
                )

            def to_summary(self) -> t.TapOracle.Summary.SummaryData:
                """Create execution summary."""
                return {
                    "execution_id": self.execution_id,
                    "duration_seconds": self.duration_seconds,
                    "streams_processed": self.streams_processed,
                    "total_records": self.total_records,
                    "avg_records_per_second": self.avg_records_per_second,
                    "errors": self.errors_encountered,
                    "success_rate": (
                        (self.streams_processed - len(self.failed_streams))
                        / max(self.streams_processed, 1)
                    )
                    * 100,
                }

            def update_performance_metrics(
                self,
            ) -> m.TapOracle.OracleTapExecutionStats:
                """Return new instance with updated calculated performance metrics."""
                if self.duration_seconds > 0:
                    return self.model_copy(
                        update={
                            "avg_records_per_second": self.total_records
                            / self.duration_seconds,
                            "avg_bytes_per_second": self.total_bytes
                            / self.duration_seconds,
                        },
                    )
                return self

            def validate_business_rules(self) -> r[bool]:
                """Validate execution stats business rules."""
                return r[bool].ok(value=True)

            @model_validator(mode="after")
            def validate_execution_stats(self) -> Self:
                """Validate Oracle execution statistics."""
                if not self.execution_id:
                    msg = "Execution ID is required"
                    raise ValueError(msg)
                if self.streams_processed < 0:
                    msg = "Streams processed cannot be negative"
                    raise ValueError(msg)
                return self

        class OracleTapDiscoverParams(FlextMeltanoModels.Entity):
            """Parameters for Oracle tap discover command."""

            config_file: Annotated[str | None, Field(default=None)]
            output_file: Annotated[str | None, Field(default=None)]

            @classmethod
            def from_click_args(cls, **kwargs: t.Scalar) -> Self:
                """Create discover params from Click command arguments."""
                config_file_value: t.Scalar | None = kwargs.get("config_file")
                output_file_value: t.Scalar | None = kwargs.get("output_file")
                return cls(
                    config_file=str(config_file_value) if config_file_value else None,
                    output_file=str(output_file_value) if output_file_value else None,
                )

            def validate_business_rules(self) -> r[bool]:
                """Validate discover params business rules."""
                return r[bool].ok(value=True)

        class OracleTapSyncParams(FlextMeltanoModels.Entity):
            """Parameters for Oracle tap sync command."""

            config_file: Annotated[str | None, Field(default=None)]
            catalog_file: Annotated[str | None, Field(default=None)]
            state_file: Annotated[str | None, Field(default=None)]

            @classmethod
            def from_click_args(cls, **kwargs: t.Scalar) -> Self:
                """Create sync params from Click command arguments."""
                config_file_value: t.Scalar | None = kwargs.get("config_file")
                catalog_file_value: t.Scalar | None = kwargs.get("catalog_file")
                state_file_value: t.Scalar | None = kwargs.get("state_file")
                return cls(
                    config_file=str(config_file_value) if config_file_value else None,
                    catalog_file=str(catalog_file_value)
                    if catalog_file_value
                    else None,
                    state_file=str(state_file_value) if state_file_value else None,
                )

            def validate_business_rules(self) -> r[bool]:
                """Validate sync params business rules."""
                return r[bool].ok(value=True)

        # =====================================================
        #
        # The following functions have been moved to FlextTapOracleUtilities:
        # - create_stream_info_from_oracle_table -> FlextTapOracleUtilities.StreamManagement.create_stream_info_from_oracle_table
        # - create_discovery_result -> FlextTapOracleUtilities.StreamManagement.create_discovery_result
        #
        # Use the utilities pattern instead of standalone functions.


# =====================================================
# MAIN EXPORTS
# =====================================================

# Short aliases
m = FlextTapOracleModels

__all__: Sequence[str] = [
    "FlextTapOracleModels",
    "m",
]
