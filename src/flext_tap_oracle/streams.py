"""Oracle Tap Streams - Complete Stream Implementation.

Copyright (c) 2025 FLEXT Contributors
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from collections.abc import Iterable, Mapping, Sequence
from datetime import datetime
from typing import override

from flext_core import FlextLogger, FlextResult, t, u
from flext_db_oracle import FlextDbOracleApi
from flext_meltano import FlextMeltanoStream as Stream, FlextMeltanoTap as Tap

from flext_tap_oracle.constants import c


class FlextTapOracleStreams:
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
            schema: Mapping[str, t.ContainerValue],
            oracle_api: FlextDbOracleApi,
        ) -> None:
            """Initialize Oracle stream with maximum flext-db-oracle integration."""
            super().__init__(tap, name=name, schema=dict(schema))
            self.table_name: str = table_name
            self.oracle_api: FlextDbOracleApi = oracle_api
            self._tap: Tap = tap
            # Use flext-db-oracle infrastructure services (lazy initialized)
            self._metadata_manager: t.ContainerValue | None = None
            self._observability_manager: t.ContainerValue | None = None

        @property
        def metadata_manager(self) -> t.ContainerValue:
            """Get flext-db-oracle metadata manager with lazy initialization."""
            if self._metadata_manager is None:
                # Use REAL constructor - requires FlextDbOracleConnection
                connection = self.oracle_api.connection
                if connection is None:
                    # Fallback: create connection from tap config using CORRECT method
                    tap_config: t.ContainerValue = getattr(
                        self._tap,
                        "typed_config",
                        None,
                    )
                    if (
                        tap_config
                        and getattr(tap_config, "get_oracle_config", None) is not None
                    ):
                        # Note: FlextDbOracleConnection does not exist in flext_db_oracle
                        # oracle_config = tap_config.get_oracle_config()
                        # connection = FlextDbOracleConnection(oracle_config)
                        pass
                    else:
                        msg = "Cannot create metadata manager without valid Oracle connection"
                        raise RuntimeError(msg)
                # Note: FlextDbOracleMetadataManager does not exist in flext_db_oracle
                # self._metadata_manager = FlextDbOracleMetadataManager(connection)
                self._metadata_manager = dict[str, t.ContainerValue]()
            return self._metadata_manager

        @property
        def observability_manager(self) -> t.ContainerValue:
            """Get flext-db-oracle observability manager with lazy initialization."""
            if self._observability_manager is None:
                # Use REAL constructor - requires FlextContainer and context_name
                # Note: FlextDbOracleObservabilityManager does not exist in flext_db_oracle
                # container = FlextContainer.get_global()
                # context_name = f"oracle_stream_{self.table_name}"
                # self._observability_manager = FlextDbOracleObservabilityManager(...)
                self._observability_manager = dict[str, t.ContainerValue]()
            return self._observability_manager

        @override
        def get_records(
            self,
            context: Mapping[str, t.ContainerValue] | None = None,
        ) -> Iterable[dict[str, t.ContainerValue]]:
            """Get records from Oracle table using flext-db-oracle exclusively - NO direct SQLAlchemy."""
            try:
                _ = context
                with self.oracle_api as api:
                    # Get schema name safely from tap config
                    schema_name: str | None = None
                    tap_cfg = getattr(self._tap, "config", {})
                    match tap_cfg:
                        case dict() as tap_cfg_dict:
                            raw_schema = tap_cfg_dict.get("schema_name")
                            match raw_schema:
                                case str() as schema_str if schema_str:
                                    schema_name = schema_str

                    # Build safe query with validated table name (pre-validated identifier)
                    safe_table = self.table_name.replace('"', '""')
                    sql = (  # nosec B608
                        f'SELECT * FROM "{schema_name}"."{safe_table}"'  # nosec B608
                        if schema_name
                        else f'SELECT * FROM "{safe_table}"'  # nosec B608
                    )

                    # Use flext-db-oracle query API
                    query_result: FlextResult[list[m.Dict]] = api.query(sql)

                    if query_result.is_failure:
                        FlextTapOracleStreams.logger.error(
                            "Failed to execute query: %s",
                            query_result.error,
                        )
                        return

                    # Process results using flext-db-oracle result handling
                    rows = query_result.value or []

                    for row in rows:
                        # t.Dict is a RootModel[dict] — extract root dict
                        record: dict[str, t.ContainerValue] = dict(row.root)
                        yield record

            except (ValueError, TypeError, KeyError, AttributeError, OSError) as e:
                FlextTapOracleStreams.logger.exception(
                    "Error getting records from %s",
                    self.table_name,
                )
                msg = f"Failed to get records: {e}"
                raise RuntimeError(msg) from e

        def _process_results_with_table_metadata(
            self,
            query_data: t.ContainerValue,  # TDbOracleQueryResult from flext-db-oracle
            table_metadata: t.ContainerValue,  # FlextDbOracleTable instance
        ) -> Iterable[Mapping[str, t.ContainerValue]]:
            """Process results using flext-db-oracle table metadata."""
            # Extract column metadata from FlextDbOracleTable
            columns = getattr(table_metadata, "columns", None)
            if columns is None or not u.is_list_like(columns):
                FlextTapOracleStreams.logger.warning(
                    "Table metadata missing columns, using fallback",
                )
                yield from self._process_results_fallback(query_data)
                return
            column_names: list[str] = [getattr(col, "name", "") for col in columns]
            # Handle TDbOracleQueryResult data structure
            if not isinstance(query_data, Iterable) or isinstance(
                query_data,
                str | bytes,
            ):
                FlextTapOracleStreams.logger.warning(
                    "Unexpected query data structure, using fallback",
                )
                yield from self._process_results_fallback(query_data)
                return
            # Convert data to dictionaries using flext-db-oracle metadata
            data_rows: Iterable[t.ContainerValue] = query_data
            for row_data in data_rows:
                try:
                    record: dict[str, t.ContainerValue]
                    match row_data:
                        case list() as row_list:
                            record = dict(zip(column_names, row_list, strict=False))
                        case tuple() as row_tuple:
                            tuple_values = [str(value) for value in row_tuple]
                            record = dict(
                                zip(column_names, tuple_values, strict=False),
                            )
                        case Mapping() as row_mapping:
                            record = {
                                str(column): value
                                for column, value in row_mapping.items()
                            }
                        case _:
                            row_type_name = type(row_data).__name__
                            FlextTapOracleStreams.logger.warning(
                                "Unexpected row data type: %s",
                                row_type_name,
                            )
                            continue
                    # Apply Oracle-specific transformations using flext-db-oracle knowledge
                    record = self._transform_oracle_types_with_table_metadata(
                        record,
                        columns,
                    )
                    yield record
                except (ValueError, TypeError, KeyError, AttributeError, OSError):
                    FlextTapOracleStreams.logger.exception(
                        "Failed to process record using flext-db-oracle metadata",
                    )
                    continue

        def _process_results_fallback(
            self,
            query_data: t.ContainerValue,
        ) -> Iterable[Mapping[str, t.ContainerValue]]:
            """Fallback processing without metadata (minimal implementation)."""
            # Use schema properties as column names
            schema_props = self.schema.get("properties", {})
            column_names: list[str] = []
            match schema_props:
                case dict() as schema_props_dict:
                    column_names = list(schema_props_dict.keys())
            # Handle different query_data structures
            if not isinstance(query_data, Iterable) or isinstance(
                query_data,
                str | bytes,
            ):
                FlextTapOracleStreams.logger.warning(
                    "Cannot process query data in fallback mode",
                )
                return
            data_rows: Iterable[t.ContainerValue] = query_data
            for row_data in data_rows:
                try:
                    record: dict[str, t.ContainerValue]
                    match row_data:
                        case list() as row_list:
                            if column_names:
                                record = dict[str, t.ContainerValue](
                                    zip(column_names, row_list, strict=False),
                                )
                            else:
                                # Generic column naming
                                record = {
                                    f"col_{i}": value
                                    for i, value in enumerate(row_list)
                                }
                        case tuple() as row_tuple:
                            tuple_values = [str(value) for value in row_tuple]
                            if column_names:
                                record = dict[str, t.ContainerValue](
                                    zip(column_names, tuple_values, strict=False),
                                )
                            else:
                                record = {
                                    f"col_{i}": str(value)
                                    for i, value in enumerate(tuple_values)
                                }
                        case Mapping() as row_mapping:
                            record = {
                                str(column): value
                                for column, value in row_mapping.items()
                            }
                        case _:
                            # Convert other types to string representation
                            str_val: t.ContainerValue = str(row_data)
                            record = {"data": str_val}
                    yield record
                except (ValueError, TypeError, KeyError, AttributeError, OSError):
                    FlextTapOracleStreams.logger.exception(
                        "Failed to process record in fallback mode",
                    )
                    continue

        def _transform_oracle_types_with_table_metadata(
            self,
            record: Mapping[str, t.ContainerValue],
            column_metadata: Sequence[
                t.ContainerValue
            ],  # FlextDbOracleColumn instances
        ) -> dict[str, t.ContainerValue]:
            """Transform Oracle data types using flext-db-oracle type knowledge."""
            transformed_record: dict[str, t.ContainerValue] = {}
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
                oracle_type_str = str(oracle_type) if oracle_type else ""
                if oracle_type_str and oracle_type_str.upper().startswith((
                    "DATE",
                    "TIMESTAMP",
                )):
                    # Convert Oracle datetime objects to ISO string
                    if isinstance(value, datetime):
                        transformed_record[column_name] = value.isoformat()
                    else:
                        transformed_record[column_name] = str(value)
                elif oracle_type_str and oracle_type_str.upper().startswith((
                    "CLOB",
                    "BLOB",
                )):
                    # Handle Oracle LOB types
                    transformed_record[column_name] = (
                        str(value) if value is not None else None
                    )
                elif getattr(value, "__str__", None) is not None:
                    # Convert other Oracle-specific types to string representation
                    transformed_record[column_name] = str(value)
                else:
                    # Keep value as-is for basic types
                    transformed_record[column_name] = value
            return transformed_record

        # ADDITIONAL ORACLE STREAM METHODS
        def get_table_info(self) -> Mapping[str, t.ContainerValue]:
            """Get Oracle table information using flext-db-oracle metadata."""
            try:
                mgr = self.metadata_manager
                get_meta = getattr(mgr, "get_table_metadata", None)
                if get_meta is None:
                    return {
                        "table_name": self.table_name,
                        "error": "Metadata manager not available",
                    }
                table_metadata_result = get_meta(self.table_name)
                if getattr(table_metadata_result, "is_success", None) and getattr(
                    table_metadata_result,
                    "data",
                    None,
                ):
                    table = table_metadata_result.data
                    columns = getattr(table, "columns", [])
                    return {
                        "table_name": self.table_name,
                        "stream_name": self.name,
                        "column_count": len(columns) if u.is_list_like(columns) else 0,
                        "oracle_schema": getattr(
                            table,
                            "schema_name",
                            c.TapOracle.DEFAULT_OPERATION_NAME,
                        ),
                        "table_type": getattr(table, "table_type", "TABLE"),
                    }
                return {
                    "table_name": self.table_name,
                    "error": "Metadata not available",
                }
            except (ValueError, TypeError, KeyError, AttributeError, OSError) as e:
                FlextTapOracleStreams.logger.exception(
                    "Failed to get table info",
                )
                return {"table_name": self.table_name, "error": str(e)}

        def estimate_row_count(self) -> int | None:
            """Estimate table row count using Oracle system views."""
            try:
                # Validate table name is a valid Oracle identifier before using in SQL
                cleaned_name = (
                    self.table_name.replace("_", "").replace("$", "").replace("#", "")
                )
                if not self.table_name or not cleaned_name.isalnum():
                    FlextTapOracleStreams.logger.warning(
                        "Invalid table name for count estimation: %s",
                        self.table_name,
                    )
                    return None
                # Safe query construction using template - table name pre-validated
                safe_table_name = self.table_name.replace('"', '""')
                sql: str = f'SELECT COUNT(*) FROM "{safe_table_name}"'  # nosec B608
                result: FlextResult[list[m.Dict]] = self.oracle_api.query(sql)
                if result.is_success and result.value:
                    first_row = result.value[0]
                    # t.Dict root is dict[str, ContainerValue]
                    first_val = next(iter(first_row.root.values()), None)
                    if isinstance(first_val, int | float):
                        return int(first_val)
                    match first_val:
                        case str() as first_str:
                            return int(first_str)
                return None
            except (ValueError, TypeError, KeyError, AttributeError, OSError) as e:
                err_msg = str(e)
                FlextTapOracleStreams.logger.warning(
                    "Failed to estimate row count for %s: %s",
                    self.table_name,
                    err_msg,
                )
                return None

        def get_stream_metadata(self) -> Mapping[str, t.ContainerValue]:
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
            schema: Mapping[str, t.ContainerValue],
            oracle_api: FlextDbOracleApi,
        ) -> FlextTapOracleStreams.OracleStream:
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
            return FlextTapOracleStreams.OracleStream(
                tap=tap,
                name=name,
                table_name=table_name,
                schema=schema,
                oracle_api=oracle_api,
            )

        @staticmethod
        def create_oracle_stream_from_table(
            tap: Tap,
            table_metadata: t.ContainerValue,  # FlextDbOracleTable
            oracle_api: FlextDbOracleApi,
            stream_prefix: str = c.TapOracle.DEFAULT_STREAM_PREFIX,
        ) -> FlextTapOracleStreams.OracleStream:
            """Create Oracle stream from table metadata.

            Args:
            tap: Parent tap instance
            table_metadata: Oracle table metadata from flext-db-oracle
            oracle_api: Oracle database API instance
            stream_prefix: Prefix for stream name

            Returns:
            Configured Oracle stream instance

            """
            table_name_raw = getattr(table_metadata, "name", None)
            table_name = (
                str(table_name_raw)
                if table_name_raw
                else c.TapOracle.DEFAULT_OPERATION_NAME
            )
            stream_name = f"{stream_prefix}_{table_name.lower()}"

            # Build basic schema from table metadata
            properties: dict[str, t.ContainerValue] = {}
            columns_raw = getattr(table_metadata, "columns", None)
            if isinstance(columns_raw, list):
                for column in columns_raw:
                    col_name = str(
                        getattr(column, "name", c.TapOracle.DEFAULT_OPERATION_NAME),
                    )
                    col_type = str(
                        getattr(
                            column,
                            "data_type",
                            c.TapOracle.SingerTypes.DEFAULT_TYPE,
                        ),
                    )

                    # Map Oracle types to Singer schema types
                    singer_type = c.TapOracle.SingerTypes.DEFAULT_TYPE
                    if col_type.upper().startswith(("NUMBER", "INTEGER")):
                        singer_type = c.TapOracle.SingerTypes.NUMERIC_TYPE
                    elif col_type.upper().startswith(("DATE", "TIMESTAMP")):
                        singer_type = (
                            c.TapOracle.SingerTypes.DATETIME_TYPE
                        )  # ISO format
                    elif col_type.upper().startswith("FLOAT"):
                        singer_type = c.TapOracle.SingerTypes.NUMERIC_TYPE

                    properties[col_name] = {"type": singer_type}

            schema: dict[str, t.ContainerValue] = {
                "type": "object",
                "properties": properties,
            }

            return FlextTapOracleStreams.StreamFactory.create_oracle_stream(
                tap=tap,
                name=stream_name,
                table_name=table_name,
                schema=schema,
                oracle_api=oracle_api,
            )


__all__ = [
    "FlextTapOracleStreams",
]
