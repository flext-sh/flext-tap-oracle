"""Oracle Tap Models - Specific Data Models for Oracle Tap.

PEP8 CONSOLIDATION: Oracle tap specific data models, re-exporting from flext-db-oracle
to avoid duplication. This module provides a centralized location for all models
used by the Oracle tap while maximizing reuse of existing infrastructure.

ZERO DUPLICAÇÃO using flext-core + flext-db-oracle base models.

Copyright (c) 2025 FLEXT Contributors
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from typing import Literal

# Import and re-export base models from flext-core - NEVER duplicate
from flext_core import FlextResult, FlextValueObject

# Import and re-export Oracle models from flext-db-oracle - NEVER duplicate
from flext_db_oracle import (
    FlextDbOracleColumn,
    FlextDbOracleSchema,
    FlextDbOracleTable,
    TDbOracleColumn,
    TDbOracleConnectionStatus,
    TDbOracleQueryResult,
    TDbOracleSchema,
    TDbOracleTable,
)

# Import Singer/Meltano types from flext-meltano
from flext_meltano import PropertiesList, Property, Stream

# Import from tap configuration module (avoiding circular imports)
from pydantic import Field

# =====================================================
# TAP-SPECIFIC MODELS (only what doesn't exist elsewhere)
# =====================================================


class OracleTapStreamInfo(FlextValueObject):
    """Oracle tap stream information - aggregates tap and Oracle metadata.

    This model combines Oracle table metadata with tap-specific stream configuration
    to provide a complete view of stream information for the tap.
    """

    def validate_business_rules(self) -> FlextResult[None]:
        """Validate stream info business rules."""
        return FlextResult.ok(None)

    # Stream identity
    stream_name: str = Field(..., description="Singer stream name")
    table_name: str = Field(..., description="Oracle table name")
    schema_name: str | None = Field(None, description="Oracle schema name")

    # Stream configuration
    is_selected: bool = Field(
        default=True,
        description="Whether stream is selected for extraction",
    )
    replication_method: Literal["FULL_TABLE", "INCREMENTAL"] = Field(
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
    last_extracted: str | None = Field(None, description="Last extraction timestamp")

    def to_singer_stream_info(self) -> dict[str, object]:
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


class OracleTapDiscoveryResult(FlextValueObject):
    """Result of Oracle table discovery operation.

    Aggregates discovery results with both raw Oracle metadata and
    processed tap stream information.
    """

    def validate_business_rules(self) -> FlextResult[None]:
        """Validate discovery result business rules."""
        return FlextResult.ok(None)

    # Discovery metadata
    schema_name: str = Field(..., description="Oracle schema that was discovered")
    discovery_timestamp: str = Field(..., description="When discovery was performed")
    total_tables: int = Field(..., description="Total number of tables discovered")

    # Raw Oracle metadata
    oracle_tables: list[FlextDbOracleTable] = Field(
        default_factory=list,
        description="Raw Oracle table metadata from flext-db-oracle",
    )

    # Processed stream information
    stream_info: list[OracleTapStreamInfo] = Field(
        default_factory=list,
        description="Processed stream information for tap use",
    )

    # Filtering results
    filtered_tables: list[str] = Field(
        default_factory=list,
        description="Table names after applying filters",
    )
    excluded_tables: list[str] = Field(
        default_factory=list,
        description="Table names that were excluded",
    )

    def get_selected_streams(self) -> list[OracleTapStreamInfo]:
        """Get only selected streams."""
        return [stream for stream in self.stream_info if stream.is_selected]

    def get_table_by_name(self, table_name: str) -> FlextDbOracleTable | None:
        """Get Oracle table metadata by name."""
        for table in self.oracle_tables:
            if table.name == table_name:
                return table
        return None

    def to_singer_catalog(self) -> dict[str, object]:
        """Convert to Singer catalog format."""
        return {
            "streams": [stream.to_singer_stream_info() for stream in self.stream_info],
            "metadata": {
                "schema": self.schema_name,
                "discovery_timestamp": self.discovery_timestamp,
                "total_tables": self.total_tables,
            },
        }


class OracleTapExecutionStats(FlextValueObject):
    """Oracle tap execution statistics and metrics.

    Tracks runtime statistics for tap execution, performance metrics,
    and operational information.
    """

    # Execution metadata
    execution_id: str = Field(..., description="Unique execution identifier")
    start_timestamp: str = Field(..., description="Execution start time")
    end_timestamp: str | None = Field(None, description="Execution end time")

    # Stream statistics
    streams_processed: int = Field(default=0, description="Number of streams processed")
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
    duration_seconds: float = Field(default=0.0, description="Total execution duration")

    # Error tracking
    errors_encountered: int = Field(
        default=0,
        description="Number of errors encountered",
    )
    failed_streams: list[str] = Field(
        default_factory=list,
        description="Names of failed streams",
    )

    # Oracle-specific metrics
    oracle_connection_time: float = Field(
        default=0.0,
        description="Oracle connection time",
    )
    oracle_query_time: float = Field(default=0.0, description="Total Oracle query time")
    oracle_result_processing_time: float = Field(
        default=0.0,
        description="Result processing time",
    )

    def update_performance_metrics(self) -> OracleTapExecutionStats:
        """Return new instance with updated calculated performance metrics."""
        if self.duration_seconds > 0:
            return self.model_copy(
                update={
                    "avg_records_per_second": self.total_records
                    / self.duration_seconds,
                    "avg_bytes_per_second": self.total_bytes / self.duration_seconds,
                },
            )
        return self

    def add_stream_stats(
        self,
        records: int,
        bytes_processed: int,
        processing_time: float,
    ) -> OracleTapExecutionStats:
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

    def mark_stream_error(self, stream_name: str) -> OracleTapExecutionStats:
        """Return new instance with marked stream error."""
        new_failed_streams = self.failed_streams.copy() if self.failed_streams else []
        if stream_name not in new_failed_streams:
            new_failed_streams.append(stream_name)
        return self.model_copy(
            update={
                "errors_encountered": self.errors_encountered + 1,
                "failed_streams": new_failed_streams,
            },
        )

    def to_summary(self) -> dict[str, object]:
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


# =====================================================
# TYPE ALIASES AND ADDITIONAL TYPES
# =====================================================

# Re-export types from flext-db-oracle with tap-specific aliases
TapOracleTable = TDbOracleTable
TapOracleColumn = TDbOracleColumn
TapOracleSchema = TDbOracleSchema
TapOracleQueryResult = TDbOracleQueryResult
TapOracleConnectionStatus = TDbOracleConnectionStatus

# Tap-specific type definitions
TapReplicationMethod = Literal["FULL_TABLE", "INCREMENTAL"]
TapStreamSelection = Literal["selected", "automatic", "excluded"]
TapExecutionMode = Literal["discovery", "extraction", "test", "validate"]


# =====================================================
# FACTORY FUNCTIONS
# =====================================================


def create_stream_info_from_oracle_table(
    oracle_table: FlextDbOracleTable,
    stream_prefix: str = "oracle",
    replication_method: TapReplicationMethod = "FULL_TABLE",
) -> FlextResult[OracleTapStreamInfo]:
    """Create stream info from Oracle table metadata.

    Args:
        oracle_table: Oracle table metadata from flext-db-oracle
        stream_prefix: Prefix for stream name
        replication_method: Default replication method

    Returns:
        FlextResult containing stream info

    """
    try:
        stream_name = f"{stream_prefix}_{oracle_table.name.lower()}"

        stream_info = OracleTapStreamInfo(
            stream_name=stream_name,
            table_name=oracle_table.name,
            schema_name=getattr(oracle_table, "schema_name", None),
            replication_method=replication_method,
            column_count=len(oracle_table.columns)
            if hasattr(oracle_table, "columns")
            else None,
        )

        return FlextResult.ok(stream_info)

    except Exception as e:
        return FlextResult.fail(f"Failed to create stream info from Oracle table: {e}")


def create_discovery_result(
    schema_name: str,
    oracle_tables: list[FlextDbOracleTable],
    stream_prefix: str = "oracle",
) -> FlextResult[OracleTapDiscoveryResult]:
    """Create discovery result from Oracle tables.

    Args:
        schema_name: Oracle schema name
        oracle_tables: List of Oracle table metadata
        stream_prefix: Prefix for stream names

    Returns:
        FlextResult containing discovery result

    """
    try:
        # Create stream info for each table
        stream_info = []
        for table in oracle_tables:
            stream_result = create_stream_info_from_oracle_table(table, stream_prefix)
            if stream_result.success and stream_result.data:
                stream_info.append(stream_result.data)

        discovery_result = OracleTapDiscoveryResult(
            schema_name=schema_name,
            discovery_timestamp="now",  # Would use actual timestamp
            total_tables=len(oracle_tables),
            oracle_tables=oracle_tables,
            stream_info=stream_info,
            filtered_tables=[table.name for table in oracle_tables],
        )

        return FlextResult.ok(discovery_result)

    except Exception as e:
        return FlextResult.fail(f"Failed to create discovery result: {e}")


# =====================================================
# EXPORTS
# =====================================================

__all__: list[str] = [
    "FlextDbOracleColumn",
    "FlextDbOracleSchema",
    "FlextDbOracleTable",
    "OracleTapDiscoveryResult",
    "OracleTapExecutionStats",
    "OracleTapStreamInfo",
    "PropertiesList",
    "Property",
    "Stream",
    "TDbOracleColumn",
    "TDbOracleConnectionStatus",
    "TDbOracleQueryResult",
    "TDbOracleSchema",
    "TDbOracleTable",
    "TapExecutionMode",
    "TapOracleColumn",
    "TapOracleConnectionStatus",
    "TapOracleQueryResult",
    "TapOracleSchema",
    "TapOracleTable",
    "TapReplicationMethod",
    "TapStreamSelection",
    "create_discovery_result",
    "create_stream_info_from_oracle_table",
]
