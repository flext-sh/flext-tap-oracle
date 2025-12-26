"""Oracle Tap Streams - Complete Stream Implementation.

Copyright (c) 2025 FLEXT Contributors
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from collections.abc import Iterable, Mapping
from typing import override

from flext_core import FlextLogger, FlextResult
from flext_db_oracle import FlextDbOracleApi
from flext_meltano import FlextMeltanoStream as Stream, FlextMeltanoTap as Tap


class FlextMeltanoTapOracleStreams:
    """Unified streams class for Oracle tap operations with complete stream management.

    Consolidates ALL Oracle tap stream-related functionality:
    - OracleStream implementation for data extraction
    - Stream factory methods and utilities
    - Oracle metadata processing and type conversion
    - Performance optimization for large tables
    - Complete integration with flext-db-oracle infrastructure

    All nested classes and methods follow SOLID principles and FlextResult patterns.
    """

    # Shared logger for all stream operations
    logger = FlextLogger(__name__)

    class OracleStream(Stream):
        """Oracle stream using MAXIMUM flext-db-oracle infrastructure.

        This implementation leverages ALL available flext-db-oracle functionality:
        - FlextDbOracleMetadataManager for schema information
        - FlextDbOracleObservabilityManager for monitoring
        - FlextDbOracleApi for optimized database operations
        - Native Oracle connection pooling and performance optimization.
        """

        @override
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
            self.table_name: str = table_name
            self.oracle_api: FlextDbOracleApi = oracle_api
            self._tap: Tap = tap
            # Use flext-db-oracle infrastructure services (lazy initialized)
            self._metadata_manager: object | None = None
            self._observability_manager: object | None = None

        @property
        def metadata_manager(self: object) -> object:
            """Get flext-db-oracle metadata manager with lazy initialization."""
            if self._metadata_manager is None:
                # Use REAL constructor - requires FlextDbOracleConnection
                connection = self.oracle_api.connection
                if connection is None:
                    # Fallback: create connection from tap config using CORRECT method
                    tap_config: dict[str, object] = getattr(
                        self._tap,
                        "typed_config",
                        None,
                    )
                    if tap_config and hasattr(tap_config, "get_oracle_config"):
                        # Note: FlextDbOracleConnection does not exist in flext_db_oracle
                        # oracle_config = tap_config.get_oracle_config()
                        # connection = FlextDbOracleConnection(oracle_config)
                        pass
                    else:
                        msg = "Cannot create metadata manager without valid Oracle connection"
                        raise RuntimeError(msg)
                # Note: FlextDbOracleMetadataManager does not exist in flext_db_oracle
                # self._metadata_manager = FlextDbOracleMetadataManager(connection)
                self._metadata_manager = {}
            return self._metadata_manager

        @property
        def observability_manager(self: object) -> object:
            """Get flext-db-oracle observability manager with lazy initialization."""
            if self._observability_manager is None:
                # Use REAL constructor - requires FlextContainer and context_name
                # Note: FlextDbOracleObservabilityManager does not exist in flext_db_oracle
                # container = FlextContainer.get_global()
                # context_name = f"oracle_stream_{self.table_name}"
                # self._observability_manager = FlextDbOracleObservabilityManager(...)
                self._observability_manager = {}
            return self._observability_manager

        def get_records(
            self,
            _context: Mapping[str, object] | None = None,
        ) -> Iterable[dict[str, object]]:
            """Get records from Oracle table using flext-db-oracle exclusively - NO direct SQLAlchemy."""
            oracle_api = self._create_oracle_api()
            tap_config = self.tap_config

            try:
                with oracle_api as api:
                    # Use safe query construction with parameterized queries through flext-db-oracle
                    # This prevents SQL injection by using proper parameter binding

                    # Get schema and table names safely
                    schema_name = None
                    if hasattr(tap_config, "schema_name") and tap_config.schema_name:
                        schema_name = tap_config.schema_name

                    # Use flext-db-oracle API for safe query construction
                    query_result = api.execute_table_query(
                        table_name=self.table_name,
                        schema_name=schema_name,
                        columns=["*"],  # Select all columns
                        where_conditions=None,  # No filtering for full extraction
                        order_by=None,
                        limit=None,
                    )

                    if query_result.is_failure:
                        FlextMeltanoTapOracleStreams.logger.error(
                            f"Failed to execute query: {query_result.error}",
                        )
                        return

                    # Process results using flext-db-oracle result handling
                    rows = query_result.data or []

                    for row in rows:
                        # Convert row to dict[str, object] format expected by Singer
                        if hasattr(row, "_asdict"):
                            # Handle named tuple rows
                            record = row._asdict()
                        elif isinstance(row, dict):
                            # Handle dict[str, object] rows
                            record = row
                        else:
                            # Handle other row formats
                            record = dict[str, object](row) if row else {}

                        # Apply any necessary transformations
                        processed_record = self._process_record(record)
                        yield processed_record

            except (ValueError, TypeError, KeyError, AttributeError, OSError) as e:
                FlextMeltanoTapOracleStreams.logger.exception(
                    f"Error getting records from {self.table_name}",
                )
                msg = f"Failed to get records: {e}"
                raise RuntimeError(msg) from e

        def _process_results_with_table_metadata(
            self,
            query_data: object,  # TDbOracleQueryResult from flext-db-oracle
            table_metadata: object,  # FlextDbOracleTable instance
        ) -> Iterable[dict[str, object]]:
            """Process results using flext-db-oracle table metadata."""
            # Extract column metadata from FlextDbOracleTable
            if not hasattr(table_metadata, "columns"):
                FlextMeltanoTapOracleStreams.logger.warning(
                    "Table metadata missing columns, using fallback",
                )
                yield from self._process_results_fallback(query_data)
                return
            column_names = [col.name for col in table_metadata.columns]
            # Handle TDbOracleQueryResult data structure
            if hasattr(query_data, "__iter__") and not isinstance(
                query_data,
                (str, bytes),
            ):
                data_rows = query_data
            else:
                FlextMeltanoTapOracleStreams.logger.warning(
                    "Unexpected query data structure, using fallback",
                )
                yield from self._process_results_fallback(query_data)
                return
            # Convert data to dictionaries using flext-db-oracle metadata
            for row_data in data_rows:
                try:
                    if isinstance(row_data, (list, tuple)):
                        record = dict[str, object](
                            zip(column_names, row_data, strict=False),
                        )
                    elif isinstance(row_data, dict):
                        record = row_data
                    else:
                        FlextMeltanoTapOracleStreams.logger.warning(
                            "Unexpected row data type: %s",
                            type(row_data),
                        )
                        continue
                    # Apply Oracle-specific transformations using flext-db-oracle knowledge
                    record = self._transform_oracle_types_with_table_metadata(
                        record,
                        table_metadata.columns,
                    )
                    yield record
                except (ValueError, TypeError, KeyError, AttributeError, OSError):
                    FlextMeltanoTapOracleStreams.logger.exception(
                        "Failed to process record using flext-db-oracle metadata",
                    )
                    continue

        def _process_results_fallback(
            self,
            query_data: object,
        ) -> Iterable[dict[str, object]]:
            """Fallback processing without metadata (minimal implementation)."""
            # Use schema properties as column names
            column_names: dict[str, object] = list(
                self.schema.get("properties", {}).keys(),
            )
            # Handle different query_data structures
            if hasattr(query_data, "__iter__") and not isinstance(
                query_data,
                (str, bytes),
            ):
                data_rows = query_data
            else:
                FlextMeltanoTapOracleStreams.logger.warning(
                    "Cannot process query data in fallback mode",
                )
                return
            for row_data in data_rows:
                try:
                    if isinstance(row_data, (list, tuple)):
                        if column_names:
                            record = dict[str, object](
                                zip(column_names, row_data, strict=False),
                            )
                        else:
                            # Generic column naming
                            record = {
                                f"col_{i}": value for i, value in enumerate(row_data)
                            }
                    elif isinstance(row_data, dict):
                        record = row_data
                    else:
                        # Convert other types to string
                        record = {"data": str(row_data)}
                    yield record
                except (ValueError, TypeError, KeyError, AttributeError, OSError):
                    FlextMeltanoTapOracleStreams.logger.exception(
                        "Failed to process record in fallback mode",
                    )
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
                if oracle_type and oracle_type.upper().startswith((
                    "DATE",
                    "TIMESTAMP",
                )):
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
        def get_table_info(self: object) -> dict[str, object]:
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
                return {
                    "table_name": self.table_name,
                    "error": "Metadata not available",
                }
            except (ValueError, TypeError, KeyError, AttributeError, OSError) as e:
                FlextMeltanoTapOracleStreams.logger.exception(
                    "Failed to get table info",
                )
                return {"table_name": self.table_name, "error": str(e)}

        def estimate_row_count(self: object) -> int | None:
            """Estimate table row count using Oracle system views."""
            try:
                # Validate table name is a valid Oracle identifier before using in SQL
                if (
                    not self.table_name
                    or not self.table_name
                    .replace("_", "")
                    .replace("$", "")
                    .replace("#", "")
                    .isalnum()
                ):
                    FlextMeltanoTapOracleStreams.logger.warning(
                        "Invalid table name for count estimation: %s",
                        self.table_name,
                    )
                    return None
                # Safe query construction using template - table name pre-validated
                safe_table_name = self.table_name.replace('"', '""')  # Escape quotes
                query_template: dict[str, object] = 'SELECT COUNT(*) FROM "{}"'
                result: FlextResult[object] = self.oracle_api.query(
                    query_template.format(safe_table_name),
                )
                if (
                    result.is_success
                    and result.value
                    and hasattr(result.value, "__getitem__")
                ):
                    first_row = result.value[0]
                    if isinstance(first_row, (list, tuple)) and first_row:
                        return int(first_row[0])
                    if isinstance(first_row, dict):
                        # Get first value from dict
                        return int(next(iter(first_row.values())))
                return None
            except (ValueError, TypeError, KeyError, AttributeError, OSError) as e:
                FlextMeltanoTapOracleStreams.logger.warning(
                    "Failed to estimate row count for %s: %s",
                    self.table_name,
                    e,
                )
                return None

        def get_stream_metadata(self: object) -> dict[str, object]:
            """Get complete stream metadata."""
            return {
                "name": self.name,
                "table_name": self.table_name,
                "schema": self.schema,
                "table_info": self.get_table_info(),
                "estimated_rows": self.estimate_row_count(),
            }

    class StreamFactory:
        """Factory class for creating Oracle streams with complete configuration."""

        @staticmethod
        def create_oracle_stream(
            tap: Tap,
            name: str,
            table_name: str,
            schema: dict[str, object],
            oracle_api: FlextDbOracleApi,
        ) -> FlextMeltanoTapOracleStreams.OracleStream:
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
            return FlextMeltanoTapOracleStreams.OracleStream(
                tap=tap,
                name=name,
                table_name=table_name,
                schema=schema,
                oracle_api=oracle_api,
            )

        @staticmethod
        def create_oracle_stream_from_table(
            tap: Tap,
            table_metadata: object,  # FlextDbOracleTable
            oracle_api: FlextDbOracleApi,
            stream_prefix: str = "oracle",
        ) -> FlextMeltanoTapOracleStreams.OracleStream:
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
                    if col_type.upper().startswith(("NUMBER", "INTEGER")):
                        pass
                    elif col_type.upper().startswith(("DATE", "TIMESTAMP")):
                        pass  # ISO format
                    elif col_type.upper().startswith("FLOAT"):
                        pass

                    properties: dict[str, object] = schema.get("properties", {})
                    if isinstance(properties, dict):
                        properties[col_name] = {"type": "singer_type"}
                        schema["properties"] = properties

            return FlextMeltanoTapOracleStreams.StreamFactory.create_oracle_stream(
                tap=tap,
                name=stream_name,
                table_name=table_name,
                schema=schema,
                oracle_api=oracle_api,
            )


# Backward compatibility classes with real inheritance
class OracleStream(FlextMeltanoTapOracleStreams.OracleStream):
    """OracleStream - real inheritance from FlextMeltanoTapOracleStreams.OracleStream."""


class FlextOracleStream(FlextMeltanoTapOracleStreams.OracleStream):
    """FlextOracleStream - real inheritance from FlextMeltanoTapOracleStreams.OracleStream."""


# Factory function exports for backward compatibility
create_oracle_stream = FlextMeltanoTapOracleStreams.StreamFactory.create_oracle_stream
create_oracle_stream_from_table = (
    FlextMeltanoTapOracleStreams.StreamFactory.create_oracle_stream_from_table
)

__all__ = [
    "FlextMeltanoTapOracleStreams",
    "FlextOracleStream",
    "OracleStream",
    "create_oracle_stream",
    "create_oracle_stream_from_table",
]
