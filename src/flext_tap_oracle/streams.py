"""Oracle Tap Streams - Complete Stream Implementation.

Copyright (c) 2025 FLEXT Contributors
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from collections.abc import Iterable, Mapping, MutableMapping, Sequence
from datetime import datetime

from flext_db_oracle import FlextDbOracleApi
from flext_tap_oracle import c, p, t, u


class FlextTapOracleStreams:
    """Unified streams class for Oracle tap operations with complete stream management.

    Consolidates ALL Oracle tap stream-related functionality:
    - OracleStream implementation for data extraction
    - Stream factory methods and utilities
    - Oracle metadata processing and type conversion
    - Performance optimization for large tables
    - Complete integration with flext-db-oracle infrastructure

    All nested classes and methods follow SOLID principles and r patterns.
    """

    logger = u.fetch_logger(__name__)

    class OracleStream:
        """Oracle stream using MAXIMUM flext-db-oracle infrastructure.

        This implementation leverages ALL available flext-db-oracle functionality:
        - FlextDbOracleMetadataManager for schema information
        - FlextDbOracleObservabilityManager for monitoring
        - FlextDbOracleApi for optimized database operations
        - Native Oracle connection pooling and performance optimization.
        """

        def __init__(
            self,
            tap: p.TapOraclePrivate.Tap,
            name: str,
            table_name: str,
            schema: Mapping[str, t.GeneralValueType],
            oracle_api: FlextDbOracleApi,
        ) -> None:
            """Initialize Oracle stream with maximum flext-db-oracle integration."""
            self.name = name
            self.schema = dict(schema)
            self.table_name: str = table_name
            self.oracle_api: FlextDbOracleApi = oracle_api
            _ = tap

        def estimate_row_count(self) -> int | None:
            """Estimate table row count using Oracle system views."""
            try:
                cleaned_name = (
                    self.table_name.replace("_", "").replace("$", "").replace("#", "")
                )
                if not self.table_name or not cleaned_name.isalnum():
                    FlextTapOracleStreams.logger.warning(
                        "Invalid table name for count estimation: %s",
                        self.table_name,
                    )
                    return None
                safe_table_name = self.table_name.replace('"', '""')
                sql: str = f'SELECT COUNT(*) FROM "{safe_table_name}"'  # nosec B608 — table name validated via isalnum()
                result: p.Result[Sequence[t.Dict]] = self.oracle_api.query(sql)
                if result.success and result.value:
                    result_rows: Sequence[t.Dict] = result.value
                    first_row: t.Dict = result_rows[0]
                    first_val = next(iter(first_row.root.values()), None)
                    if isinstance(first_val, t.NUMERIC_TYPES) and not isinstance(
                        first_val,
                        bool,
                    ):
                        return int(first_val)
                    match first_val:
                        case str() as first_str:
                            return int(first_str)
                        case _:
                            return None
                return None
            except c.Meltano.SINGER_SAFE_EXCEPTIONS as e:
                err_msg = str(e)
                FlextTapOracleStreams.logger.warning(
                    "Failed to estimate row count for %s: %s",
                    self.table_name,
                    err_msg,
                )
                return None

        def get_records(
            self,
            context: Mapping[str, t.TapOracle.Summary.OracleValue] | None = None,
        ) -> Iterable[Mapping[str, t.TapOracle.Summary.OracleValue]]:
            """Get records from Oracle table using flext-db-oracle exclusively - NO direct SQLAlchemy."""
            try:
                _ = context
                with self.oracle_api as api:
                    table_metadata_result = api.get_table_metadata(self.table_name)
                    if table_metadata_result.failure:
                        msg = (
                            table_metadata_result.error
                            or "Table metadata is not available"
                        )
                        raise RuntimeError(msg)
                    schema_name: str | None = None
                    safe_table = self.table_name.replace('"', '""')
                    sql: str
                    if schema_name:
                        sql = f'SELECT * FROM "{schema_name}"."{safe_table}"'  # nosec B608
                    else:
                        sql = f'SELECT * FROM "{safe_table}"'  # nosec B608
                    query_result: p.Result[Sequence[t.Dict]] = api.query(sql)
                    if query_result.failure:
                        error_msg: str = query_result.error or "unknown query error"
                        raise RuntimeError(error_msg)
                    rows: Sequence[t.Dict] = query_result.value
                    yield from self._process_results_with_table_metadata(
                        rows,
                        table_metadata_result.value,
                    )
            except c.Meltano.SINGER_SAFE_EXCEPTIONS as e:
                FlextTapOracleStreams.logger.exception(
                    "Error getting records from %s",
                    self.table_name,
                )
                msg = f"Failed to get records: {e}"
                raise RuntimeError(msg) from e

        def get_stream_metadata(self) -> Mapping[str, t.GeneralValueType | None]:
            """Get complete stream metadata."""
            return {
                "name": self.name,
                "table_name": self.table_name,
                "schema": dict(self.schema),
                "table_info": str(self.get_table_info()),
                "estimated_rows": self.estimate_row_count(),
            }

        def get_table_info(self) -> Mapping[str, t.GeneralValueType | None]:
            """Get Oracle table information using flext-db-oracle metadata."""
            try:
                table_metadata_result = self.oracle_api.get_table_metadata(
                    self.table_name,
                )
                if table_metadata_result.success:
                    table = table_metadata_result.value
                    columns = getattr(table, "columns", [])
                    return {
                        "table_name": self.table_name,
                        "stream_name": self.name,
                        "column_count": len(columns) if u.list_like(columns) else 0,
                        "oracle_schema": getattr(
                            table,
                            "schema_name",
                            c.TapOracle.DEFAULT_OPERATION_NAME,
                        ),
                        "table_type": getattr(table, "table_type", "TABLE"),
                    }
                return {
                    "table_name": self.table_name,
                    "error": table_metadata_result.error or "Metadata not available",
                }
            except c.Meltano.SINGER_SAFE_EXCEPTIONS as e:
                FlextTapOracleStreams.logger.exception("Failed to get table info")
                return {"table_name": self.table_name, "error": str(e)}

        def _process_results_with_table_metadata(
            self,
            query_data: Sequence[t.Dict],
            table_metadata: t.TapOracle.Summary.OracleValue,
        ) -> Iterable[Mapping[str, t.TapOracle.Summary.OracleValue]]:
            """Process results using flext-db-oracle table metadata."""
            columns = getattr(table_metadata, "columns", None)
            if columns is None or not u.list_like(columns):
                msg = "Table metadata is missing column definitions"
                raise RuntimeError(msg)
            column_names: t.StrSequence = [
                getattr(col, "name", "") for col in columns if getattr(col, "name", "")
            ]
            if not column_names:
                msg = "Table metadata did not include usable column names"
                raise RuntimeError(msg)
            for row_data in query_data:
                try:
                    record: Mapping[str, t.TapOracle.Summary.OracleValue] = dict(
                        row_data.root,
                    )
                    missing_columns = [
                        column_name
                        for column_name in column_names
                        if column_name not in record
                    ]
                    if missing_columns:
                        msg = (
                            f"Oracle row is missing expected columns: {missing_columns}"
                        )
                        raise RuntimeError(msg)
                    record = self._transform_oracle_types(
                        record,
                        columns,
                    )
                    yield record
                except c.Meltano.SINGER_SAFE_EXCEPTIONS as e:
                    msg = f"Failed to process Oracle record: {e}"
                    raise RuntimeError(msg) from e

        def _transform_oracle_types(
            self,
            record: Mapping[str, t.TapOracle.Summary.OracleValue],
            column_metadata: Sequence[t.TapOracle.Summary.OracleValue],
        ) -> Mapping[str, t.TapOracle.Summary.OracleValue]:
            """Transform Oracle data types using flext-db-oracle type knowledge."""
            transformed_record: MutableMapping[
                str, t.TapOracle.Summary.OracleValue
            ] = {}
            meta_lookup: MutableMapping[str, t.TapOracle.Summary.OracleValue] = {}
            for col_meta_value in column_metadata:
                col_name = getattr(col_meta_value, "name", None) or getattr(
                    col_meta_value,
                    "column_name",
                    None,
                )
                if isinstance(col_name, str) and col_name:
                    meta_lookup[col_name] = col_meta_value
            for column_name, value in record.items():
                if value is None:
                    transformed_record[column_name] = None
                    continue
                col_meta = meta_lookup.get(column_name)
                oracle_type = None
                if col_meta is not None:
                    oracle_type = getattr(col_meta, "data_type", None) or getattr(
                        col_meta,
                        "type",
                        None,
                    )
                oracle_type_str = str(oracle_type) if oracle_type else ""
                if oracle_type_str and oracle_type_str.upper().startswith((
                    "DATE",
                    "TIMESTAMP",
                )):
                    if isinstance(value, datetime):
                        transformed_record[column_name] = value.isoformat()
                    else:
                        transformed_record[column_name] = str(value)
                elif (
                    oracle_type_str
                    and oracle_type_str.upper().startswith(("CLOB", "BLOB"))
                ) or getattr(value, "__str__", None) is not None:
                    transformed_record[column_name] = str(value)
                else:
                    transformed_record[column_name] = value
            return transformed_record

    class StreamFactory:
        """Factory class for creating Oracle streams with complete configuration."""

        @staticmethod
        def create_oracle_stream(
            tap: p.TapOraclePrivate.Tap,
            name: str,
            table_name: str,
            schema: Mapping[str, t.GeneralValueType],
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
            tap: p.TapOraclePrivate.Tap,
            table_metadata: t.TapOracle.Summary.OracleValue,
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
            properties: Mapping[str, t.GeneralValueType] = {}
            schema: Mapping[str, t.GeneralValueType] = {
                "type": "t.RecursiveContainer",
                "properties": properties,
            }
            return FlextTapOracleStreams.StreamFactory.create_oracle_stream(
                tap=tap,
                name=stream_name,
                table_name=table_name,
                schema=schema,
                oracle_api=oracle_api,
            )


__all__: list[str] = ["FlextTapOracleStreams"]
