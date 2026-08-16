"""Oracle Tap Streams - Complete Stream Implementation.

Copyright (c) 2025 FLEXT Contributors
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from typing import TYPE_CHECKING

from flext_tap_oracle import c, m, p, t, u

if TYPE_CHECKING:
    from collections.abc import Iterable, Mapping, MutableMapping, Sequence

    from flext_db_oracle import FlextDbOracleApi


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
            tap: p.TapOracle.Tap,
            name: str,
            table_name: str,
            schema: t.JsonMapping,
            oracle_api: FlextDbOracleApi,
        ) -> None:
            """Initialize Oracle stream with maximum flext-db-oracle integration."""
            self.name = name
            self.schema = t.json_dict_adapter().validate_python(schema)
            self.table_name: str = table_name
            self.oracle_api: FlextDbOracleApi = oracle_api
            _ = tap

        def estimate_row_count(self) -> int | None:
            """Estimate table row count using Oracle system views."""

            def _run_estimate_row_count() -> int | None:
                cleaned_name = (
                    self.table_name.replace("_", "").replace("$", "").replace("#", "")
                )
                if not self.table_name or not cleaned_name.isalnum():
                    FlextTapOracleStreams.logger.warning(
                        "Invalid table name for count estimation: %s", self.table_name
                    )
                    return None
                safe_table_name = self.table_name.replace('"', '""')
                sql: str = " ".join(("SELECT COUNT(*) FROM", f'"{safe_table_name}"'))
                result: p.Result[Sequence[m.Dict]] = self.oracle_api.query(sql)
                if result.success and result.value:
                    result_rows: t.SequenceOf[m.Dict] = result.value
                    first_row: m.Dict = result_rows[0]
                    first_val = next(iter(first_row.root.values()), None)
                    if isinstance(first_val, t.NUMERIC_TYPES) and not isinstance(
                        first_val, bool
                    ):
                        return int(first_val)
                    match first_val:
                        case str() as first_str:
                            return int(first_str)
                        case _:
                            return None
                return None

            try:
                return _run_estimate_row_count()
            except c.Meltano.SINGER_SAFE_EXCEPTIONS as e:
                err_msg = str(e)
                FlextTapOracleStreams.logger.warning(
                    "Failed to estimate row count for %s: %s", self.table_name, err_msg
                )
                return None

        def get_records(
            self, context: t.MappingKV[str, t.TapOracle.OracleValue] | None = None
        ) -> Iterable[Mapping[str, t.TapOracle.OracleValue]]:
            """Get records from Oracle table using flext-db-oracle exclusively - NO direct SQLAlchemy."""
            try:
                rows, table_metadata = self._fetch_rows_with_table_metadata(context)
            except c.Meltano.SINGER_SAFE_EXCEPTIONS as e:
                FlextTapOracleStreams.logger.exception(
                    "Error getting records from %s", self.table_name
                )
                msg = f"Failed to get records: {e}"
                raise RuntimeError(msg) from e
            yield from self._process_results_with_table_metadata(rows, table_metadata)

        def _fetch_rows_with_table_metadata(
            self, context: t.MappingKV[str, t.TapOracle.OracleValue] | None
        ) -> tuple[t.SequenceOf[m.Dict], m.DbOracle.TableMetadata]:
            """Fetch Oracle rows and table metadata for this stream."""
            _ = context
            with self.oracle_api as api:
                table_metadata_result = api.fetch_table_metadata(self.table_name)
                if table_metadata_result.failure:
                    msg = (
                        table_metadata_result.error or "Table metadata is not available"
                    )
                    raise RuntimeError(msg)
                safe_table = self.table_name.replace('"', '""')
                sql = " ".join(("SELECT * FROM", f'"{safe_table}"'))
                query_result: p.Result[Sequence[m.Dict]] = api.query(sql)
                if query_result.failure:
                    error_msg: str = query_result.error or "unknown query error"
                    raise RuntimeError(error_msg)
                return query_result.value, table_metadata_result.value

        def get_stream_metadata(self) -> t.MappingKV[str, t.JsonValue | None]:
            """Get complete stream metadata."""
            return {
                "name": self.name,
                "table_name": self.table_name,
                "schema": dict(self.schema),
                "table_info": str(self.get_table_info()),
                "estimated_rows": self.estimate_row_count(),
            }

        def get_table_info(self) -> t.MappingKV[str, t.JsonValue | None]:
            """Get Oracle table information using flext-db-oracle metadata."""
            try:
                table_metadata_result = self.oracle_api.fetch_table_metadata(
                    self.table_name
                )
                if table_metadata_result.success:
                    table = table_metadata_result.value
                    columns = getattr(table, "columns", [])
                    return {
                        "table_name": self.table_name,
                        "stream_name": self.name,
                        "column_count": len(columns) if u.list_like(columns) else 0,
                        "oracle_schema": getattr(
                            table, "schema_name", c.TapOracle.DEFAULT_OPERATION_NAME
                        ),
                        "table_type": getattr(table, "table_type", "TABLE"),
                    }
            except c.Meltano.SINGER_SAFE_EXCEPTIONS as e:
                FlextTapOracleStreams.logger.exception("Failed to get table info")
                return {"table_name": self.table_name, "error": str(e)}
            else:
                return {
                    "table_name": self.table_name,
                    "error": table_metadata_result.error or "Metadata not available",
                }

        def _process_results_with_table_metadata(
            self,
            query_data: t.SequenceOf[m.Dict],
            table_metadata: m.DbOracle.TableMetadata,
        ) -> Iterable[t.JsonMapping]:
            """Process results using flext-db-oracle table metadata."""
            columns = table_metadata.columns
            if not columns:
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
                    yield self._process_result_row(row_data, column_names, columns)
                except c.Meltano.SINGER_SAFE_EXCEPTIONS as e:
                    msg = f"Failed to process Oracle record: {e}"
                    raise RuntimeError(msg) from e

        def _process_result_row(
            self,
            row_data: m.Dict,
            column_names: t.StrSequence,
            columns: t.SequenceOf[m.DbOracle.ColumnMetadata],
        ) -> t.JsonMapping:
            """Validate and transform one Oracle row."""
            record = t.Cli.JSON_MAPPING_ADAPTER.validate_python(row_data.root)
            missing_columns = [
                column_name for column_name in column_names if column_name not in record
            ]
            if missing_columns:
                msg = f"Oracle row is missing expected columns: {missing_columns}"
                raise RuntimeError(msg)
            return self.transform_oracle_types(record, columns)

        @staticmethod
        def transform_oracle_types(
            record: t.JsonMapping,
            column_metadata: t.SequenceOf[m.DbOracle.ColumnMetadata],
        ) -> t.JsonMapping:
            """Transform Oracle data types using flext-db-oracle type knowledge."""
            transformed_record: t.MutableJsonMapping = {}
            meta_lookup: MutableMapping[str, m.DbOracle.ColumnMetadata] = {}
            for col_meta_value in column_metadata:
                col_name = getattr(col_meta_value, "name", None) or getattr(
                    col_meta_value, "column_name", None
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
                        col_meta, "type", None
                    )
                oracle_type_str = str(oracle_type) if oracle_type else ""
                if oracle_type_str and oracle_type_str.upper().startswith((
                    "DATE",
                    "TIMESTAMP",
                    "CLOB",
                    "NCLOB",
                    "BLOB",
                )):
                    transformed_record[column_name] = str(value)
                else:
                    transformed_record[column_name] = value
            return t.Cli.JSON_MAPPING_ADAPTER.validate_python(transformed_record)

    class StreamFactory:
        """Factory class for creating Oracle streams with complete configuration."""

        @staticmethod
        def create_oracle_stream(
            tap: p.TapOracle.Tap,
            name: str,
            table_name: str,
            schema: t.JsonMapping,
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
            tap: p.TapOracle.Tap,
            table_metadata: t.TapOracle.OracleValue,
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
            properties: t.JsonMapping = {}
            schema = t.Cli.JSON_MAPPING_ADAPTER.validate_python({
                "type": "object",
                "properties": properties,
            })
            return FlextTapOracleStreams.StreamFactory.create_oracle_stream(
                tap=tap,
                name=stream_name,
                table_name=table_name,
                schema=schema,
                oracle_api=oracle_api,
            )


__all__: list[str] = ["FlextTapOracleStreams"]
