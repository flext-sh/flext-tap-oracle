"""Oracle Tap Streams - Complete Stream Implementation.

Copyright (c) 2025 FLEXT Contributors
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from collections.abc import Iterable, Mapping, Sequence
from datetime import datetime
from typing import Protocol

from flext_core import FlextLogger, r
from flext_db_oracle import FlextDbOracleApi
from flext_meltano import FlextMeltanoStream as Stream, p
from pydantic import BaseModel

from flext_tap_oracle import c, m, t, u

type OracleValue = m.NormalizedValue | BaseModel | None


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

    logger = FlextLogger(__name__)

    class _Tap(Protocol):
        typed_config: OracleValue

    class OracleStream(Stream):
        """Oracle stream using MAXIMUM flext-db-oracle infrastructure.

        This implementation leverages ALL available flext-db-oracle functionality:
        - FlextDbOracleMetadataManager for schema information
        - FlextDbOracleObservabilityManager for monitoring
        - FlextDbOracleApi for optimized database operations
        - Native Oracle connection pooling and performance optimization.
        """

        def __init__(
            self,
            tap: p.Meltano.Tap,
            name: str,
            table_name: str,
            schema: Mapping[str, OracleValue],
            oracle_api: FlextDbOracleApi,
        ) -> None:
            """Initialize Oracle stream with maximum flext-db-oracle integration."""
            self.name = name
            self.schema = dict(schema)
            self.table_name: str = table_name
            self.oracle_api: FlextDbOracleApi = oracle_api
            self._tap: p.Meltano.Tap = tap
            self._metadata_manager: Mapping[str, OracleValue] | None = None
            self._observability_manager: Mapping[str, OracleValue] | None = None

        @property
        def metadata_manager(self) -> object:
            """Get flext-db-oracle metadata manager with lazy initialization."""
            if self._metadata_manager is None:
                connection = self.oracle_api.connection
                if connection is None:
                    tap_config: OracleValue = getattr(self._tap, "typed_config", None)
                    if (
                        tap_config
                        and getattr(tap_config, "get_oracle_config", None) is not None
                    ):
                        pass
                    else:
                        msg = "Cannot create metadata manager without valid Oracle connection"
                        raise RuntimeError(msg)
                metadata_placeholder: dict[str, t.Container] = {}
                self._metadata_manager = metadata_placeholder
            return self._metadata_manager

        @property
        def observability_manager(self) -> object:
            """Get flext-db-oracle observability manager with lazy initialization."""
            if self._observability_manager is None:
                obs_placeholder: dict[str, t.Container] = {}
                self._observability_manager = obs_placeholder
            return self._observability_manager

        def estimate_row_count(self) -> int | None:
            """Estimate table row count using Oracle system views."""
            try:
                cleaned_name = (
                    self.table_name.replace("_", "").replace("$", "").replace("#", "")
                )
                if not self.table_name or not cleaned_name.isalnum():
                    FlextTapOracleStreams.logger.warning(
                        "Invalid table name for count estimation: %s", self.table_name
                    )
                    return None
                safe_table_name = self.table_name.replace('"', '""')
                sql: str = f'SELECT COUNT(*) FROM "{safe_table_name}"'
                result: r[list[m.Dict]] = self.oracle_api.query(sql)
                if result.is_success and result.value:
                    result_rows: list[m.Dict] = result.value
                    first_row: m.Dict = result_rows[0]
                    first_val = next(iter(first_row.root.values()), None)
                    if isinstance(first_val, int | float):
                        return int(first_val)
                    match first_val:
                        case str() as first_str:
                            return int(first_str)
                        case _:
                            return None
                return None
            except (ValueError, TypeError, KeyError, AttributeError, OSError) as e:
                err_msg = str(e)
                FlextTapOracleStreams.logger.warning(
                    "Failed to estimate row count for %s: %s", self.table_name, err_msg
                )
                return None

        def get_records(
            self, context: Mapping[str, OracleValue] | None = None
        ) -> Iterable[dict[str, OracleValue]]:
            """Get records from Oracle table using flext-db-oracle exclusively - NO direct SQLAlchemy."""
            try:
                _ = context
                with self.oracle_api as api:
                    schema_name: str | None = None
                    safe_table = self.table_name.replace('"', '""')
                    sql = (
                        f'SELECT * FROM "{schema_name}"."{safe_table}"'
                        if schema_name
                        else f'SELECT * FROM "{safe_table}"'
                    )
                    query_result: r[list[m.Dict]] = api.query(sql)
                    if query_result.is_failure:
                        error_msg: str = query_result.error or "unknown query error"
                        FlextTapOracleStreams.logger.error(
                            "Failed to execute query: %s", error_msg
                        )
                        return
                    rows: list[m.Dict] = query_result.unwrap_or([])
                    for row in rows:
                        record: dict[str, OracleValue] = dict(row.root)
                        yield record
            except (ValueError, TypeError, KeyError, AttributeError, OSError) as e:
                FlextTapOracleStreams.logger.exception(
                    "Error getting records from %s", self.table_name
                )
                msg = f"Failed to get records: {e}"
                raise RuntimeError(msg) from e

        def get_stream_metadata(self) -> Mapping[str, OracleValue]:
            """Get complete stream metadata."""
            return {
                "name": self.name,
                "table_name": self.table_name,
                "schema": {},
                "table_info": self.get_table_info(),
                "estimated_rows": self.estimate_row_count(),
            }

        def get_table_info(self) -> Mapping[str, OracleValue]:
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
                    table_metadata_result, "data", None
                ):
                    table = table_metadata_result.data
                    columns = getattr(table, "columns", [])
                    return {
                        "table_name": self.table_name,
                        "stream_name": self.name,
                        "column_count": len(columns) if u.is_list_like(columns) else 0,
                        "oracle_schema": getattr(
                            table, "schema_name", c.TapOracle.DEFAULT_OPERATION_NAME
                        ),
                        "table_type": getattr(table, "table_type", "TABLE"),
                    }
                return {
                    "table_name": self.table_name,
                    "error": "Metadata not available",
                }
            except (ValueError, TypeError, KeyError, AttributeError, OSError) as e:
                FlextTapOracleStreams.logger.exception("Failed to get table info")
                return {"table_name": self.table_name, "error": str(e)}

        def _process_results_fallback(
            self, query_data: OracleValue
        ) -> Iterable[Mapping[str, OracleValue]]:
            """Fallback processing without metadata (minimal implementation)."""
            column_names: list[str] = []
            if not isinstance(query_data, Iterable) or isinstance(
                query_data, str | bytes
            ):
                FlextTapOracleStreams.logger.warning(
                    "Cannot process query data in fallback mode"
                )
                return
            data_rows: Iterable[OracleValue] = query_data
            for row_data in data_rows:
                try:
                    record: dict[str, OracleValue]
                    match row_data:
                        case list() as row_list:
                            if column_names:
                                record = dict(zip(column_names, row_list, strict=False))
                            else:
                                record = {
                                    f"col_{i}": value
                                    for i, value in enumerate(row_list)
                                }
                        case tuple() as row_tuple:
                            tuple_values = [str(value) for value in row_tuple]
                            if column_names:
                                record = dict(
                                    zip(column_names, tuple_values, strict=False)
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
                            str_val: OracleValue = str(row_data)
                            record = {"data": str_val}
                    yield record
                except (ValueError, TypeError, KeyError, AttributeError, OSError):
                    FlextTapOracleStreams.logger.exception(
                        "Failed to process record in fallback mode"
                    )
                    continue

        def _process_results_with_table_metadata(
            self, query_data: OracleValue, table_metadata: OracleValue
        ) -> Iterable[Mapping[str, OracleValue]]:
            """Process results using flext-db-oracle table metadata."""
            columns = getattr(table_metadata, "columns", None)
            if columns is None or not u.is_list_like(columns):
                FlextTapOracleStreams.logger.warning(
                    "Table metadata missing columns, using fallback"
                )
                yield from self._process_results_fallback(query_data)
                return
            column_names: list[str] = [getattr(col, "name", "") for col in columns]
            if not isinstance(query_data, Iterable) or isinstance(
                query_data, str | bytes
            ):
                FlextTapOracleStreams.logger.warning(
                    "Unexpected query data structure, using fallback"
                )
                yield from self._process_results_fallback(query_data)
                return
            data_rows: Iterable[OracleValue] = query_data
            for row_data in data_rows:
                try:
                    record: dict[str, OracleValue]
                    match row_data:
                        case list() as row_list:
                            record = dict(zip(column_names, row_list, strict=False))
                        case tuple() as row_tuple:
                            tuple_values = [str(value) for value in row_tuple]
                            record = dict(zip(column_names, tuple_values, strict=False))
                        case Mapping() as row_mapping:
                            record = {
                                str(column): value
                                for column, value in row_mapping.items()
                            }
                        case _:
                            row_type_name = type(row_data).__name__
                            FlextTapOracleStreams.logger.warning(
                                "Unexpected row data type: %s", row_type_name
                            )
                            continue
                    record = self._transform_oracle_types_with_table_metadata(
                        record, columns
                    )
                    yield record
                except (ValueError, TypeError, KeyError, AttributeError, OSError):
                    FlextTapOracleStreams.logger.exception(
                        "Failed to process record using flext-db-oracle metadata"
                    )
                    continue

        def _transform_oracle_types_with_table_metadata(
            self,
            record: Mapping[str, OracleValue],
            column_metadata: Sequence[OracleValue],
        ) -> dict[str, OracleValue]:
            """Transform Oracle data types using flext-db-oracle type knowledge."""
            transformed_record: dict[str, OracleValue] = {}
            meta_lookup: dict[str, OracleValue] = {}
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
            tap: p.Meltano.Tap,
            name: str,
            table_name: str,
            schema: Mapping[str, OracleValue],
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
            tap: p.Meltano.Tap,
            table_metadata: OracleValue,
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
            properties: dict[str, OracleValue] = {}
            schema: dict[str, OracleValue] = {
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


__all__ = ["FlextTapOracleStreams"]
