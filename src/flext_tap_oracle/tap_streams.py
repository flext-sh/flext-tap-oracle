"""Oracle Tap Streams - Complete Stream Implementation.

PEP8 CONSOLIDATION: All Oracle stream definition and processing logic consolidated.
This module consolidates oracle_stream.py following the established FLEXT pattern
for comprehensive stream management.

MAXIMUM use of flext-db-oracle infrastructure for Oracle stream processing.

Copyright (c) 2025 FLEXT Contributors
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from time import perf_counter
from typing import TYPE_CHECKING

from flext_core import get_flext_container, get_logger
from flext_db_oracle import (
    FlextDbOracleApi,
    FlextDbOracleConnection,
    FlextDbOracleMetadataManager,
    FlextDbOracleObservabilityManager,
)
from flext_meltano import Stream

if TYPE_CHECKING:
    from collections.abc import Iterable, Mapping

    from flext_meltano import Tap

logger = get_logger(__name__)


class OracleStream(Stream):
    """Oracle stream using MAXIMUM flext-db-oracle infrastructure.

    This implementation leverages ALL available flext-db-oracle functionality:
    - FlextDbOracleMetadataManager for schema information
    - FlextDbOracleObservabilityManager for monitoring
    - FlextDbOracleApi for optimized database operations
    - Native Oracle connection pooling and performance optimization
    """

    def __init__(
        self,
        tap: Tap,
        name: str,
        table_name: str,
        schema: dict[str, object],
        oracle_api: FlextDbOracleApi,
    ) -> None:
        """Initialize Oracle stream with maximum flext-db-oracle integration."""
        super().__init__(tap, name=name, schema=schema)
        self.table_name = table_name
        self.oracle_api = oracle_api
        self._tap = tap

        # Use flext-db-oracle infrastructure services
        self._metadata_manager: FlextDbOracleMetadataManager | None = None
        self._observability_manager: FlextDbOracleObservabilityManager | None = None

    @property
    def metadata_manager(self) -> FlextDbOracleMetadataManager:
        """Get flext-db-oracle metadata manager with lazy initialization."""
        if self._metadata_manager is None:
            # Use REAL constructor - requires FlextDbOracleConnection
            connection = self.oracle_api.connection
            if connection is None:
                # Fallback: create connection from tap config using CORRECT method
                tap_config = getattr(self._tap, "typed_config", None)
                if tap_config and hasattr(tap_config, "get_oracle_config"):
                    oracle_config = tap_config.get_oracle_config()
                    connection = FlextDbOracleConnection(oracle_config)
                else:
                    msg = (
                        "Cannot create metadata manager without valid Oracle connection"
                    )
                    raise RuntimeError(msg)

            self._metadata_manager = FlextDbOracleMetadataManager(connection)
        return self._metadata_manager

    @property
    def observability_manager(self) -> FlextDbOracleObservabilityManager:
        """Get flext-db-oracle observability manager with lazy initialization."""
        if self._observability_manager is None:
            # Use REAL constructor - requires FlextContainer and context_name
            container = get_flext_container()
            context_name = f"oracle_stream_{self.table_name}"
            self._observability_manager = FlextDbOracleObservabilityManager(
                container,
                context_name,
            )
        return self._observability_manager

    def get_records(
        self,
        context: Mapping[str, object] | None,
    ) -> Iterable[dict[str, object]]:
        """Extract records using MAXIMUM flext-db-oracle capabilities."""
        try:
            # Log operation start using proper info logging
            logger.info(
                "Starting stream extraction for table: %s",
                self.table_name,
            )
            operation_start_time = perf_counter()

            # Build optimized query using tap configuration
            tap_config = getattr(self._tap, "typed_config", None)

            # Build query with proper Oracle identifier escaping
            if (
                tap_config
                and hasattr(tap_config, "schema_name")
                and tap_config.schema_name
            ):
                # Use Oracle identifier quoting to prevent injection
                schema_name = tap_config.schema_name.replace('"', '""')  # Escape quotes
                table_name = self.table_name.replace('"', '""')  # Escape quotes
                sql = f'SELECT * FROM "{schema_name}"."{table_name}"'  # nosec B608  # noqa: S608
            else:
                table_name = self.table_name.replace('"', '""')  # Escape quotes
                sql = f'SELECT * FROM "{table_name}"'  # nosec B608  # noqa: S608

            logger.info("Executing Oracle query via flext-db-oracle: %s", sql[:200])

            # Execute query using flext-db-oracle API
            result = self.oracle_api.query(sql)

            if result.success and result.data:
                # Use flext-db-oracle metadata for table information
                table_metadata_result = self.metadata_manager.get_table_metadata(
                    self.table_name,
                    schema_name=getattr(tap_config, "schema_name", None)
                    if tap_config
                    else None,
                )

                if table_metadata_result.success and table_metadata_result.data:
                    # Convert Oracle results to Singer records using flext-db-oracle metadata
                    yield from self._process_results_with_table_metadata(
                        result.data,
                        table_metadata_result.data,
                    )
                else:
                    # Fallback processing without metadata
                    yield from self._process_results_fallback(result.data)

                # Log successful operation using proper info logging
                operation_time = perf_counter() - operation_start_time
                record_count = (
                    len(result.data) if hasattr(result.data, "__len__") else 0
                )
                logger.info(
                    "Stream extraction completed in %.2fs for table %s (records: %d)",
                    operation_time,
                    self.table_name,
                    record_count,
                )
            else:
                logger.warning(
                    "No data from Oracle table %s via flext-db-oracle: %s",
                    self.table_name,
                    result.error if hasattr(result, "error") else "Empty result",
                )
                # Log no-data completion using proper info logging
                operation_time = perf_counter() - operation_start_time
                logger.info(
                    "Stream extraction completed with no data in %.2fs for table: %s",
                    operation_time,
                    self.table_name,
                )

        except Exception as e:
            logger.exception(
                "Oracle extraction failed via flext-db-oracle for table %s",
                self.table_name,
            )
            # Log failed operation using flext-db-oracle observability
            if hasattr(self, "_observability_manager") and self._observability_manager:
                operation_time = (
                    perf_counter() - operation_start_time
                    if "operation_start_time" in locals()
                    else 0
                )
                self.observability_manager.log_error_with_context(
                    "Stream",
                    f"Stream extraction failed after {operation_time:.2f}s: {e}",
                    table=self.table_name,
                )

    def _process_results_with_table_metadata(
        self,
        query_data: object,  # TDbOracleQueryResult from flext-db-oracle
        table_metadata: object,  # FlextDbOracleTable instance
    ) -> Iterable[dict[str, object]]:
        """Process results using flext-db-oracle table metadata."""
        # Extract column metadata from FlextDbOracleTable
        if not hasattr(table_metadata, "columns"):
            logger.warning("Table metadata missing columns, using fallback")
            yield from self._process_results_fallback(query_data)
            return

        column_names = [col.name for col in table_metadata.columns]

        # Handle TDbOracleQueryResult data structure
        if hasattr(query_data, "__iter__") and not isinstance(query_data, (str, bytes)):
            data_rows = query_data
        else:
            logger.warning("Unexpected query data structure, using fallback")
            yield from self._process_results_fallback(query_data)
            return

        # Convert data to dictionaries using flext-db-oracle metadata
        for row_data in data_rows:
            try:
                if isinstance(row_data, (list, tuple)):
                    record = dict(zip(column_names, row_data, strict=False))
                elif isinstance(row_data, dict):
                    record = row_data
                else:
                    logger.warning("Unexpected row data type: %s", type(row_data))
                    continue

                # Apply Oracle-specific transformations using flext-db-oracle knowledge
                record = self._transform_oracle_types_with_table_metadata(
                    record,
                    table_metadata.columns,
                )

                yield record

            except Exception:
                logger.exception(
                    "Failed to process record using flext-db-oracle metadata",
                )
                continue

    def _process_results_fallback(
        self,
        query_data: object,
    ) -> Iterable[dict[str, object]]:
        """Fallback processing without metadata (minimal implementation)."""
        # Use schema properties as column names
        column_names = list(self.schema.get("properties", {}).keys())

        # Handle different query_data structures
        if hasattr(query_data, "__iter__") and not isinstance(query_data, (str, bytes)):
            data_rows = query_data
        else:
            logger.warning("Cannot process query data in fallback mode")
            return

        for row_data in data_rows:
            try:
                if isinstance(row_data, (list, tuple)):
                    if column_names:
                        record = dict(zip(column_names, row_data, strict=False))
                    else:
                        # Generic column naming
                        record = {f"col_{i}": value for i, value in enumerate(row_data)}
                elif isinstance(row_data, dict):
                    record = row_data
                else:
                    # Convert other types to string
                    record = {"data": str(row_data)}

                yield record

            except Exception:
                logger.exception("Failed to process record in fallback mode")
                continue

    def _transform_oracle_types_with_table_metadata(
        self,
        record: dict[str, object],
        column_metadata: list[object],  # FlextDbOracleColumn instances
    ) -> dict[str, object]:
        """Transform Oracle data types using flext-db-oracle type knowledge."""
        transformed_record: dict[str, object] = {}

        # Create metadata lookup by column name
        meta_lookup = {}
        for col_meta in column_metadata:
            col_name = getattr(col_meta, "name", None) or getattr(
                col_meta,
                "column_name",
                None,
            )
            if col_name:
                meta_lookup[col_name] = col_meta

        for column_name, value in record.items():
            if value is None:
                transformed_record[column_name] = None
                continue

            # Get Oracle type information from flext-db-oracle metadata
            col_meta = meta_lookup.get(column_name)
            oracle_type = None
            if col_meta:
                oracle_type = getattr(col_meta, "data_type", None) or getattr(
                    col_meta,
                    "type",
                    None,
                )

            # Apply Oracle-specific transformations based on type
            if oracle_type and oracle_type.upper().startswith(("DATE", "TIMESTAMP")):
                # Convert Oracle datetime objects to ISO string
                if hasattr(value, "isoformat"):
                    transformed_record[column_name] = value.isoformat()
                else:
                    transformed_record[column_name] = str(value)
            elif oracle_type and oracle_type.upper().startswith(("CLOB", "BLOB")):
                # Handle Oracle LOB types
                transformed_record[column_name] = (
                    str(value) if value is not None else None
                )
            elif hasattr(value, "__str__"):
                # Convert other Oracle-specific types to string representation
                transformed_record[column_name] = str(value)
            else:
                # Keep value as-is for basic types
                transformed_record[column_name] = value

        return transformed_record

    # ADDITIONAL ORACLE STREAM METHODS

    def get_table_info(self) -> dict[str, object]:
        """Get Oracle table information using flext-db-oracle metadata."""
        try:
            table_metadata_result = self.metadata_manager.get_table_metadata(
                self.table_name,
            )
            if table_metadata_result.success and table_metadata_result.data:
                table = table_metadata_result.data
                return {
                    "table_name": self.table_name,
                    "stream_name": self.name,
                    "column_count": len(table.columns)
                    if hasattr(table, "columns")
                    else 0,
                    "oracle_schema": getattr(table, "schema_name", "unknown"),
                    "table_type": getattr(table, "table_type", "TABLE"),
                }
            return {"table_name": self.table_name, "error": "Metadata not available"}

        except Exception as e:
            logger.exception("Failed to get table info")
            return {"table_name": self.table_name, "error": str(e)}

    def estimate_row_count(self) -> int | None:
        """Estimate table row count using Oracle system views."""
        try:
            # Validate table name is a valid Oracle identifier before using in SQL
            if not self.table_name or not self.table_name.replace("_", "").replace("$", "").replace("#", "").isalnum():
                logger.warning("Invalid table name for count estimation: %s", self.table_name)
                return None

            # Safe query construction using template - table name pre-validated
            safe_table_name = self.table_name.replace('"', '""')  # Escape quotes
            query_template = 'SELECT COUNT(*) FROM "{}"'
            result = self.oracle_api.query(query_template.format(safe_table_name))

            if result.success and result.data and hasattr(result.data, "__getitem__"):
                first_row = result.data[0]
                if isinstance(first_row, (list, tuple)) and first_row:
                    return int(first_row[0])
                if isinstance(first_row, dict):
                    # Get first value from dict
                    return int(next(iter(first_row.values())))

            return None

        except Exception as e:
            logger.warning(
                "Failed to estimate row count for %s: %s", self.table_name, e,
            )
            return None

    def get_stream_metadata(self) -> dict[str, object]:
        """Get comprehensive stream metadata."""
        return {
            "name": self.name,
            "table_name": self.table_name,
            "schema": self.schema,
            "table_info": self.get_table_info(),
            "estimated_rows": self.estimate_row_count(),
        }


# FACTORY FUNCTIONS


def create_oracle_stream(
    tap: Tap,
    name: str,
    table_name: str,
    schema: dict[str, object],
    oracle_api: FlextDbOracleApi,
) -> OracleStream:
    """Create Oracle stream.

    Args:
        tap: Parent tap instance
        name: Stream name
        table_name: Oracle table name
        schema: Stream schema definition
        oracle_api: Oracle database API instance

    Returns:
        Configured Oracle stream instance

    """
    return OracleStream(
        tap=tap,
        name=name,
        table_name=table_name,
        schema=schema,
        oracle_api=oracle_api,
    )


def create_oracle_stream_from_table(
    tap: Tap,
    table_metadata: object,  # FlextDbOracleTable
    oracle_api: FlextDbOracleApi,
    stream_prefix: str = "oracle",
) -> OracleStream:
    """Create Oracle stream from table metadata.

    Args:
        tap: Parent tap instance
        table_metadata: Oracle table metadata from flext-db-oracle
        oracle_api: Oracle database API instance
        stream_prefix: Prefix for stream name

    Returns:
        Configured Oracle stream instance

    """
    table_name = getattr(table_metadata, "name", "unknown")
    stream_name = f"{stream_prefix}_{table_name.lower()}"

    # Build basic schema from table metadata
    schema: dict[str, object] = {"type": "object", "properties": {}}
    if hasattr(table_metadata, "columns"):
        for column in table_metadata.columns:
            col_name = getattr(column, "name", "unknown")
            col_type = getattr(column, "data_type", "string")

            # Map Oracle types to Singer schema types
            singer_type = "string"  # Default
            if col_type.upper().startswith(("NUMBER", "INTEGER")):
                singer_type = "integer"
            elif col_type.upper().startswith(("DATE", "TIMESTAMP")):
                singer_type = "string"  # ISO format
            elif col_type.upper().startswith("FLOAT"):
                singer_type = "number"

            properties = schema.get("properties", {})
            if isinstance(properties, dict):
                properties[col_name] = {"type": singer_type}
                schema["properties"] = properties

    return create_oracle_stream(
        tap=tap,
        name=stream_name,
        table_name=table_name,
        schema=schema,
        oracle_api=oracle_api,
    )


# Backward compatibility aliases
FlextOracleStream = OracleStream

__all__ = [
    "FlextOracleStream",
    "OracleStream",
    "create_oracle_stream",
    "create_oracle_stream_from_table",
]
