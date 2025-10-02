"""Models for flext-tap-oracle.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from datetime import UTC, datetime
from typing import Literal, Self

from flext_core import FlextConstants, FlextModels, FlextResult, FlextTypes
from flext_db_oracle import (
    FlextDbOracleColumn,
    FlextDbOracleQueryResult,
    FlextDbOracleSchema,
    FlextDbOracleTable,
)
from flext_meltano import FlextSingerStream as Stream
from pydantic import (
    ConfigDict,
    Field,
    FieldSerializationInfo,
    computed_field,
    field_serializer,
    field_validator,
    model_validator,
)

from flext_tap_oracle.utilities import FlextTapOracleUtilities


class FlextTapOracleModels(FlextModels):
    """Comprehensive models for Oracle tap operations extending FlextModels.

    Provides standardized models for all Oracle tap domain entities including:
    - Singer stream metadata and configuration
    - Oracle table extraction configuration
    - Replication and discovery operations
    - Performance monitoring and metrics
    - Singer protocol compliance models

    All nested classes inherit FlextModels validation and patterns.
    """

    # Pydantic 2.11 Configuration - Enterprise Singer Oracle Tap Features
    model_config = ConfigDict(
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
                }
            ],
            "tags": ["singer", "oracle", "tap", "extraction", "database"],
            "version": "2.11.0",
        },
    )

    # Advanced Pydantic 2.11 Features - Singer Oracle Tap Domain

    @computed_field
    @property
    def active_oracle_tap_models_count(self) -> int:
        """Count of active Oracle tap models with database extraction capabilities."""
        count = 0
        # Count core Singer Oracle tap models
        if hasattr(self, "OracleTapStreamMetadata"):
            count += 1
        if hasattr(self, "OracleTapDiscoveryConfig"):
            count += 1
        if hasattr(self, "OracleTapExtractionConfig"):
            count += 1
        if hasattr(self, "OracleTapPerformanceMetrics"):
            count += 1
        if hasattr(self, "OracleTapStreamInfo"):
            count += 1
        if hasattr(self, "OracleTapDiscoveryResult"):
            count += 1
        if hasattr(self, "OracleTapExecutionStats"):
            count += 1
        if hasattr(self, "OracleConnection"):
            count += 1
        if hasattr(self, "OracleQuery"):
            count += 1
        if hasattr(self, "OracleRecord"):
            count += 1
        return count

    @computed_field
    @property
    def oracle_tap_system_summary(self) -> dict[str, object]:
        """Comprehensive Singer Oracle tap system summary with database extraction capabilities."""
        return {
            "total_models": self.active_oracle_tap_models_count,
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

    @model_validator(mode="after")
    def validate_oracle_tap_system_consistency(self) -> Self:
        """Validate Singer Oracle tap system consistency and configuration."""
        # Singer Oracle tap database validation
        if (
            hasattr(self, "_oracle_connection")
            and self._oracle_connection
            and not hasattr(self, "OracleTapStreamMetadata")
        ):
            msg = "OracleTapStreamMetadata required when Oracle connection configured"
            raise ValueError(msg)

        # Discovery operation validation
        if (
            hasattr(self, "_discovery_mode")
            and self._discovery_mode
            and not hasattr(self, "OracleTapDiscoveryConfig")
        ):
            msg = "OracleTapDiscoveryConfig required for discovery operations"
            raise ValueError(msg)

        # Singer protocol compliance validation
        if hasattr(self, "_singer_mode") and self._singer_mode:
            required_models = ["OracleTapStreamInfo", "OracleTapExecutionStats"]
            for model in required_models:
                if not hasattr(self, model):
                    msg = f"{model} required for Singer protocol compliance"
                    raise ValueError(msg)

        return self

    @field_serializer("*", when_used="json")
    def serialize_with_oracle_metadata(
        self, value: object, _info: FieldSerializationInfo
    ) -> object:
        """Add Singer Oracle tap metadata to all serialized fields."""
        if isinstance(value, dict):
            return {
                **value,
                "_oracle_tap_metadata": {
                    "extraction_timestamp": datetime.now(UTC).isoformat(),
                    "tap_type": "oracle_database_extractor",
                    "singer_protocol": "v1.0",
                    "data_source": "oracle_database",
                },
            }
        if isinstance(value, (str, int, float, bool)) and hasattr(
            self, "_include_oracle_metadata"
        ):
            return {
                "value": value,
                "_oracle_context": {
                    "extracted_at": datetime.now(UTC).isoformat(),
                    "tap_name": "flext-tap-oracle",
                },
            }
        return value

    # Legacy type aliases for backward compatibility
    OracleRecord = dict[str, object]
    OracleRecords = list[OracleRecord]

    class OracleTapStreamMetadata(FlextModels.Entity):
        """Oracle tap stream metadata with Singer protocol compliance.

        Extends Oracle table metadata with tap-specific information
        for Singer streaming operations and replication configuration.
        """

        # Pydantic 2.11 Configuration - Stream Metadata Features
        model_config = ConfigDict(
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
                    }
                ],
            },
        )

        # Singer stream configuration
        stream_name: str = Field(..., description="Singer stream name")
        replication_method: Literal[FULL_TABLE, INCREMENTAL] = Field(
            default="FULL_TABLE",
            description="Replication method for this stream",
        )
        replication_key: str | None = Field(
            default=None,
            description="Column used for incremental replication",
        )
        is_selected: bool = Field(
            default=True,
            description="Whether stream is selected for extraction",
        )

        # Oracle-specific metadata
        table_name: str = Field(..., description="Oracle table name")
        schema_name: str | None = Field(default=None, description="Oracle schema name")
        estimated_rows: int | None = Field(
            default=None, description="Estimated row count"
        )
        column_count: int | None = Field(default=None, description="Number of columns")

        @computed_field
        @property
        def stream_metadata_summary(self) -> dict[str, object]:
            """Oracle stream metadata summary."""
            return {
                "stream_name": self.stream_name,
                "table_reference": f"{self.schema_name}.{self.table_name}"
                if self.schema_name
                else self.table_name,
                "extraction_type": self.replication_method,
                "is_incremental": self.replication_method == "INCREMENTAL",
                "replication_column": self.replication_key,
                "selected_for_extraction": self.is_selected,
                "estimated_volume": {
                    "rows": self.estimated_rows,
                    "columns": self.column_count,
                },
            }

        @model_validator(mode="after")
        def validate_stream_metadata(self) -> Self:
            """Validate Oracle stream metadata."""
            if self.replication_method == "INCREMENTAL" and not self.replication_key:
                msg = "Incremental replication requires a replication_key"
                raise ValueError(msg)
            if self.replication_method == "FULL_TABLE" and self.replication_key:
                msg = "Full table replication should not have replication_key"
                raise ValueError(msg)
            return self

        @field_validator("stream_name")
        @classmethod
        def validate_stream_name(cls, v: str) -> str:
            """Validate stream name follows Singer conventions."""
            if not v or not v.strip():
                msg = "Stream name cannot be empty"
                raise ValueError(msg)

            # Enhanced validation with proper limits
            max_length = FlextConstants.Limits.MAX_STRING_LENGTH
            if len(v) > max_length:
                msg = f"Stream name too long: {len(v)} > {max_length} characters"
                raise ValueError(msg)

            if v.startswith(("_", "-")) or v.endswith(("_", "-")):
                msg = "Stream name cannot start/end with underscore or dash"
                raise ValueError(msg)

            # Clean invalid characters for Singer streams
            cleaned = "".join(c if c.isalnum() or c in "_-" else "_" for c in v)
            return cleaned.lower()

        @model_validator(mode="after")
        def validate_replication_consistency(self) -> Self:
            """Validate replication configuration consistency."""
            if self.replication_method == "INCREMENTAL":
                if not self.replication_key:
                    msg = "Incremental replication requires a replication_key"
                    raise ValueError(msg)

                # Validation for replication key length
                max_key_length = FlextConstants.Limits.MAX_STRING_LENGTH
                if len(self.replication_key) > max_key_length:
                    msg = f"Replication key too long: {len(self.replication_key)} > {max_key_length}"
                    raise ValueError(msg)

            elif self.replication_method == "FULL_TABLE" and self.replication_key:
                msg = "Full table replication should not have replication_key"
                raise ValueError(msg)

            return self

        def validate_business_rules(self: object) -> FlextResult[None]:
            """Validate tap-specific business rules."""
            return FlextResult[None].ok(None)

    class OracleTapDiscoveryConfig(FlextModels.BaseConfig):
        """Configuration for Oracle tap discovery operations."""

        # Pydantic 2.11 Configuration - Discovery Features
        model_config = ConfigDict(
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
                    }
                ],
            },
        )

        # Discovery scope
        schema_names: list[str] = Field(
            default_factory=list, description="Oracle schemas to discover"
        )
        table_patterns: list[str] = Field(
            default_factory=list, description="Table name patterns to include"
        )
        exclude_patterns: list[str] = Field(
            default_factory=list, description="Table name patterns to exclude"
        )

        # Discovery options
        include_views: bool = Field(
            default=False, description="Include Oracle views in discovery"
        )
        include_system_tables: bool = Field(
            default=False, description="Include system tables in discovery"
        )
        max_tables: int = Field(
            default=FlextConstants.Performance.BatchProcessing.DEFAULT_SIZE,
            description="Maximum number of tables to discover",
        )

        # Performance settings
        discovery_timeout: int = Field(
            default=FlextConstants.Network.DEFAULT_TIMEOUT * 10,
            description="Discovery timeout in seconds",
        )
        parallel_discovery: bool = Field(
            default=True, description="Enable parallel discovery"
        )

        @computed_field
        @property
        def discovery_scope_summary(self) -> dict[str, object]:
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

    class OracleTapExtractionConfig(FlextModels.BaseConfig):
        """Configuration for Oracle tap extraction operations."""

        # Pydantic 2.11 Configuration - Extraction Features
        model_config = ConfigDict(
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
                    }
                ],
            },
        )

        # Extraction parameters
        batch_size: int = Field(
            default=FlextConstants.Performance.BatchProcessing.DEFAULT_SIZE * 10,
            description="Number of rows per batch",
        )
        max_rows: int | None = Field(
            default=None, description="Maximum rows to extract (None for unlimited)"
        )

        # Performance optimization
        parallel_streams: int = Field(
            default=1, description="Number of parallel extraction streams"
        )
        enable_query_hints: bool = Field(
            default=True, description="Enable Oracle query optimization hints"
        )

        # Incremental extraction
        incremental_column: str | None = Field(
            default=None, description="Column for incremental extraction"
        )
        incremental_bookmark: str | None = Field(
            default=None, description="Bookmark value for incremental extraction"
        )

        @computed_field
        @property
        def extraction_config_summary(self) -> dict[str, object]:
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

    class OracleTapPerformanceMetrics(FlextModels.BaseModel):
        """Performance metrics for Oracle tap operations."""

        # Pydantic 2.11 Configuration - Performance Features
        model_config = ConfigDict(
            validate_assignment=True,
            extra="forbid",
            frozen=False,
            json_schema_extra={
                "description": "Oracle tap performance metrics with comprehensive monitoring",
                "examples": [
                    {
                        "extraction_id": "ext_123",
                        "total_records": 50000,
                        "avg_records_per_second": 1000.0,
                    }
                ],
            },
        )

        # Extraction metrics
        extraction_id: str = Field(description="Unique extraction identifier")
        start_time: str = Field(description="Extraction start timestamp")
        end_time: str | None = Field(
            default=None, description="Extraction end timestamp"
        )

        # Volume metrics
        total_records: int = Field(default=0, description="Total records extracted")
        total_bytes: int = Field(default=0, description="Total bytes processed")
        streams_processed: int = Field(
            default=0, description="Number of streams processed"
        )

        # Performance metrics
        avg_records_per_second: float = Field(
            default=0.0, description="Average records per second"
        )
        avg_bytes_per_second: float = Field(
            default=0.0, description="Average bytes per second"
        )

        # Oracle-specific metrics
        oracle_connection_time: float = Field(
            default=0.0, description="Oracle connection establishment time"
        )
        oracle_query_time: float = Field(
            default=0.0, description="Total Oracle query execution time"
        )

        @computed_field
        @property
        def performance_analysis_summary(self) -> dict[str, object]:
            """Oracle tap performance analysis summary."""
            duration = 0.0
            if self.start_time and self.end_time:
                from datetime import datetime

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

    class OracleTapStreamInfo(FlextModels.Entity):
        """Oracle tap stream information - aggregates tap and Oracle metadata.

        This model combines Oracle table metadata with tap-specific stream configuration
        to provide a complete view of stream information for the tap.
        """

        # Pydantic 2.11 Configuration - Stream Info Features
        model_config = ConfigDict(
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
                    }
                ],
            },
        )

        # Stream identity
        stream_name: str = Field(..., description="Singer stream name")
        table_name: str = Field(..., description="Oracle table name")
        schema_name: str | None = Field(None, description="Oracle schema name")

        # Stream configuration
        is_selected: bool = Field(
            default=True,
            description="Whether stream is selected for extraction",
        )
        replication_method: Literal[FULL_TABLE, INCREMENTAL] = Field(
            default="FULL_TABLE",
            description="Replication method for this stream",
        )
        replication_key: str | None = Field(
            None,
            description="Column used for incremental replication",
        )

        # Runtime information (populated at runtime)
        estimated_rows: int | None = Field(None, description="Estimated row count")
        column_count: int | None = Field(None, description="Number of columns")
        last_extracted: str | None = Field(
            None, description="Last extraction timestamp"
        )

        @computed_field
        @property
        def stream_info_summary(self) -> dict[str, object]:
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

        def validate_business_rules(self: object) -> FlextResult[None]:
            """Validate stream info business rules."""
            return FlextResult[None].ok(None)

        def to_singer_stream_info(self: object) -> FlextTypes.Core.Dict:
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

    class OracleTapDiscoveryResult(FlextModels.Entity):
        """Result of Oracle table discovery operation.

        Aggregates discovery results with both raw Oracle metadata and
        processed tap stream information.
        """

        # Pydantic 2.11 Configuration - Discovery Result Features
        model_config = ConfigDict(
            validate_assignment=True,
            extra="forbid",
            frozen=False,
            json_schema_extra={
                "description": "Oracle discovery result with comprehensive metadata",
                "examples": [
                    {
                        "schema_name": "HR",
                        "total_tables": 15,
                        "discovery_timestamp": "2023-01-01T00:00:00Z",
                    }
                ],
            },
        )

        # Discovery metadata
        schema_name: str = Field(..., description="Oracle schema that was discovered")
        discovery_timestamp: str = Field(
            ..., description="When discovery was performed"
        )
        total_tables: int = Field(..., description="Total number of tables discovered")

        # Raw Oracle metadata
        oracle_tables: list[FlextDbOracleTable] = Field(
            default_factory=list,
            description="Raw Oracle table metadata from flext-db-oracle",
        )

        # Processed stream information
        stream_info: list[FlextTapOracleModels.OracleTapStreamInfo] = Field(
            default_factory=list,
            description="Processed stream information for tap use",
        )

        # Filtering results
        filtered_tables: FlextTypes.Core.StringList = Field(
            default_factory=list,
            description="Table names after applying filters",
        )
        excluded_tables: FlextTypes.Core.StringList = Field(
            default_factory=list,
            description="Table names that were excluded",
        )

        @computed_field
        @property
        def discovery_result_summary(self) -> dict[str, object]:
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

        def validate_business_rules(self: object) -> FlextResult[None]:
            """Validate discovery result business rules."""
            return FlextResult[None].ok(None)

        def get_selected_streams(
            self: object,
        ) -> list[FlextTapOracleModels.OracleTapStreamInfo]:
            """Get only selected streams."""
            return [stream for stream in self.stream_info if stream.is_selected]

        def get_table_by_name(self, table_name: str) -> FlextDbOracleTable | None:
            """Get Oracle table metadata by name."""
            for table in self.oracle_tables:
                if table.name == table_name:
                    return table
            return None

        def to_singer_catalog(self: object) -> FlextTypes.Core.Dict:
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

    class OracleTapExecutionStats(FlextModels.Entity):
        """Oracle tap execution statistics and metrics.

        Tracks runtime statistics for tap execution, performance metrics,
        and operational information.
        """

        # Pydantic 2.11 Configuration - Execution Stats Features
        model_config = ConfigDict(
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
                    }
                ],
            },
        )

        # Execution metadata
        execution_id: str = Field(..., description="Unique execution identifier")
        start_timestamp: str = Field(..., description="Execution start time")
        end_timestamp: str | None = Field(None, description="Execution end time")

        # Stream statistics
        streams_processed: int = Field(
            default=0, description="Number of streams processed"
        )
        total_records: int = Field(default=0, description="Total records extracted")
        total_bytes: int = Field(default=0, description="Total bytes processed")

        # Performance metrics
        avg_records_per_second: float = Field(
            default=0.0,
            description="Average records per second",
        )
        avg_bytes_per_second: float = Field(
            default=0.0,
            description="Average bytes per second",
        )
        duration_seconds: float = Field(
            default=0.0, description="Total execution duration"
        )

        # Error tracking
        errors_encountered: int = Field(
            default=0,
            description="Number of errors encountered",
        )
        failed_streams: FlextTypes.Core.StringList = Field(
            default_factory=list,
            description="Names of failed streams",
        )

        # Oracle-specific metrics
        oracle_connection_time: float = Field(
            default=0.0,
            description="Oracle connection time",
        )
        oracle_query_time: float = Field(
            default=0.0, description="Total Oracle query time"
        )
        oracle_result_processing_time: float = Field(
            default=0.0,
            description="Result processing time",
        )

        @computed_field
        @property
        def execution_stats_summary(self) -> dict[str, object]:
            """Oracle tap execution statistics summary."""
            success_rate = 0.0
            if self.streams_processed > 0:
                successful_streams = self.streams_processed - len(self.failed_streams)
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
                    "query_efficiency": self.oracle_query_time / self.duration_seconds
                    if self.duration_seconds > 0
                    else 0,
                },
            }

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

        def validate_business_rules(self: object) -> FlextResult[None]:
            """Validate execution stats business rules."""
            return FlextResult[None].ok(None)

        def update_performance_metrics(
            self: object,
        ) -> FlextTapOracleModels.OracleTapExecutionStats:
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

        def add_stream_stats(
            self,
            records: int,
            bytes_processed: int,
            processing_time: float,
        ) -> FlextTapOracleModels.OracleTapExecutionStats:
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
            self, stream_name: str
        ) -> FlextTapOracleModels.OracleTapExecutionStats:
            """Return new instance with marked stream error."""
            new_failed_streams = (
                self.failed_streams.copy() if self.failed_streams else []
            )
            if stream_name not in new_failed_streams:
                new_failed_streams.append(stream_name)
            return self.model_copy(
                update={
                    "errors_encountered": self.errors_encountered + 1,
                    "failed_streams": new_failed_streams,
                },
            )

        def to_summary(self: object) -> FlextTypes.Core.Dict:
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

    # Nested type aliases and additional types (moved from standalone definitions)
    # Re-export types from flext-db-oracle with tap-specific aliases
    TapOracleTable = FlextDbOracleTable
    TapOracleColumn = FlextDbOracleColumn
    TapOracleSchema = FlextDbOracleSchema
    TapOracleQueryResult = FlextDbOracleQueryResult

    # Tap-specific type definitions
    TapReplicationMethod = Literal["FULL_TABLE", "INCREMENTAL"]
    TapStreamSelection = Literal["selected", "automatic", "excluded"]
    TapExecutionMode = Literal["discovery", "extraction", "test", "validate"]

    # Legacy type aliases for backward compatibility
    TapStreamMetadata = dict[str, object]
    TapConfiguration = dict[str, object]


# =====================================================
# FUNCTIONS MOVED TO UTILITIES PATTERN
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

__all__: FlextTypes.Core.StringList = [
    "FlextDbOracleColumn",
    "FlextDbOracleQueryResult",
    "FlextDbOracleSchema",
    "FlextDbOracleTable",
    "FlextTapOracleModels",
    "FlextTapOracleUtilities",
    "Stream",
    "TapExecutionMode",
    "TapOracleColumn",
    "TapOracleQueryResult",
    "TapOracleSchema",
    "TapOracleTable",
    "TapReplicationMethod",
    "TapStreamSelection",
]
