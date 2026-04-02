"""FLEXT Tap Oracle Utilities - Domain-specific utilities for Oracle tap operations.

This module provides complete Oracle tap utilities extending u
with nested classes for error handling, stream management, discovery operations,
and configuration validation. Follows FLEXT standards with single-class pattern.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT

"""

from __future__ import annotations

from collections.abc import Mapping, MutableMapping, MutableSequence, Sequence
from datetime import UTC, datetime
from typing import Literal

from pydantic import ValidationError

from flext_core import FlextExceptions, r
from flext_db_oracle import FlextDbOracleModels, FlextDbOracleUtilities
from flext_meltano import FlextMeltanoUtilities
from flext_tap_oracle import FlextTapOracleUtilitiesClientMixin, c, m, t


class FlextTapOracleUtilities(FlextMeltanoUtilities, FlextDbOracleUtilities):
    """Unified Oracle tap utilities class extending u classes.

    Provides complete Oracle tap utilities with nested classes for:
    - Error handling and exception creation
    - Stream information management
    - Discovery operations
    - Configuration validation
    - Performance optimization
    - Client services (discovery, connection test, table filter, tap service)
    - Data extraction helpers

    Follows FLEXT pattern: single class with nested subclasses.
    """

    class TapOracle:
        """Tap Oracle namespace for cross-project access."""

        Client = FlextTapOracleUtilitiesClientMixin.TapOracle.Client

        class ErrorHandling:
            """Oracle tap error handling utilities."""

            @staticmethod
            def handle_oracle_exception(
                exception: Exception,
                operation: str = c.TapOracle.DEFAULT_OPERATION_NAME,
            ) -> r[bool]:
                """Handle Oracle exceptions with proper error mapping."""
                try:
                    error_message = f"Oracle {operation} failed: {exception}"
                    exc_str = str(exception).lower()
                    err: (
                        FlextExceptions.ConnectionError | FlextExceptions.OperationError
                    )
                    if "connection" in exc_str:
                        err = FlextExceptions.ConnectionError(error_message)
                    elif (
                        "sql" in exc_str or "query" in exc_str or "discovery" in exc_str
                    ):
                        err = FlextExceptions.OperationError(error_message)
                    else:
                        err = FlextExceptions.OperationError(error_message)
                    return r[bool].fail(str(err))
                except c.Meltano.Singer.SAFE_EXCEPTIONS as e:
                    return r[bool].fail(f"Exception handling failed: {e}")

        class StreamManagement:
            """Oracle tap stream management utilities."""

            @staticmethod
            def create_discovery_result(
                tables: Sequence[FlextDbOracleModels.DbOracle.Table],
                schema_name: str,
            ) -> r[m.TapOracle.OracleTapDiscoveryResult]:
                """Create discovery result from Oracle tables."""
                try:
                    stream_infos: MutableSequence[m.TapOracle.OracleTapStreamInfo] = []
                    for table in tables:
                        match table:
                            case FlextDbOracleModels.DbOracle.Table() as oracle_table:
                                pass
                            case _:
                                continue
                        stream_result = FlextTapOracleUtilities.TapOracle.StreamManagement.create_stream_info_from_oracle_table(
                            oracle_table,
                        )
                        if stream_result.is_success:
                            stream_infos.append(stream_result.value)
                    discovery_result = m.TapOracle.OracleTapDiscoveryResult(
                        schema_name=schema_name,
                        total_tables=len(tables),
                        discovery_timestamp=datetime.now(tz=UTC).isoformat(),
                        stream_info=stream_infos,
                        domain_events=[],
                        oracle_tables=[],
                        filtered_tables=[],
                        excluded_tables=[],
                    )
                    return r[m.TapOracle.OracleTapDiscoveryResult].ok(discovery_result)
                except c.Meltano.Singer.SAFE_EXCEPTIONS as e:
                    return r[m.TapOracle.OracleTapDiscoveryResult].fail(
                        f"Failed to create discovery result: {e}",
                    )

            @staticmethod
            def create_stream_info_from_oracle_table(
                oracle_table: FlextDbOracleModels.DbOracle.Table,
                stream_prefix: str = c.TapOracle.DEFAULT_STREAM_PREFIX,
                replication_method: Literal["FULL_TABLE", "INCREMENTAL"] = "FULL_TABLE",
            ) -> r[m.TapOracle.OracleTapStreamInfo]:
                """Create stream info from Oracle table metadata."""
                try:
                    stream_name = f"{stream_prefix}_{oracle_table.name.lower()}"
                    stream_info = m.TapOracle.OracleTapStreamInfo(
                        stream_name=stream_name,
                        table_name=oracle_table.name,
                        schema_name=getattr(oracle_table, "schema_name", None),
                        replication_method=replication_method,
                        replication_key=None,
                        estimated_rows=None,
                        last_extracted=None,
                        column_count=len(oracle_table.columns)
                        if getattr(oracle_table, "columns", None) is not None
                        else None,
                        domain_events=[],
                        is_selected=False,
                    )
                    return r[m.TapOracle.OracleTapStreamInfo].ok(stream_info)
                except c.Meltano.Singer.SAFE_EXCEPTIONS as e:
                    return r[m.TapOracle.OracleTapStreamInfo].fail(
                        f"Failed to create stream info from Oracle table: {e}",
                    )

        class ConfigurationValidation:
            """Oracle tap configuration validation utilities."""

            @staticmethod
            def build_connection_string(
                config: Mapping[str, t.GeneralValueType],
            ) -> r[str]:
                """Build Oracle connection string from configuration."""
                try:
                    cfg_validator = (
                        FlextTapOracleUtilities.TapOracle.ConfigurationValidation
                    )
                    validation_result = cfg_validator.validate_oracle_config(config)
                    if validation_result.is_failure:
                        return r[str].fail(validation_result.error)
                    validated_config = validation_result.value
                    connection_string = f"oracle://{validated_config['username']}:{validated_config['password']}@{validated_config['host']}:{validated_config['port']}/{validated_config['service_name']}"
                    return r[str].ok(connection_string)
                except c.Meltano.Singer.SAFE_EXCEPTIONS as e:
                    return r[str].fail(f"Connection string building failed: {e}")

            @staticmethod
            def test_oracle_connectivity(
                config: Mapping[str, t.GeneralValueType],
            ) -> r[Mapping[str, t.GeneralValueType]]:
                """Test Oracle connectivity with configuration."""
                try:
                    cfg_validator = (
                        FlextTapOracleUtilities.TapOracle.ConfigurationValidation
                    )
                    validation_result = cfg_validator.validate_oracle_config(config)
                    if validation_result.is_failure:
                        return r[t.GeneralValueMapping].fail(
                            validation_result.error,
                        )
                    connectivity_result = {
                        "status": "validated",
                        "host": config["host"],
                        "port": config["port"],
                        "service_name": config["service_name"],
                        "connection_test": "structural_validation_passed",
                    }
                    return r[t.GeneralValueMapping].ok(connectivity_result)
                except c.Meltano.Singer.SAFE_EXCEPTIONS as e:
                    return r[t.GeneralValueMapping].fail(
                        f"Oracle connectivity test failed: {e}",
                    )

            @staticmethod
            def validate_oracle_config(
                config: Mapping[str, t.GeneralValueType],
            ) -> r[Mapping[str, t.GeneralValueType]]:
                """Validate Oracle configuration parameters."""
                try:
                    validated_config: MutableMapping[str, t.GeneralValueType] = dict(
                        config
                    )
                    required_fields = [
                        "host",
                        "port",
                        "service_name",
                        "username",
                        "password",
                    ]
                    for field in required_fields:
                        if field not in validated_config:
                            return r[t.GeneralValueMapping].fail(
                                f"Missing required Oracle field: {field}",
                            )
                        if not validated_config[field]:
                            return r[t.GeneralValueMapping].fail(
                                f"Empty Oracle field: {field}",
                            )
                    max_port = c.TapOracle.MAX_PORT_NUMBER
                    try:
                        port = t.INTEGER_ADAPTER.validate_python(
                            validated_config["port"]
                        )
                        if port <= 0 or port > max_port:
                            return r[t.GeneralValueMapping].fail(
                                f"Oracle port must be between 1 and {max_port}",
                            )
                        validated_config["port"] = port
                    except ValidationError:
                        return r[t.GeneralValueMapping].fail(
                            "Oracle port must be numeric",
                        )
                    return r[t.GeneralValueMapping].ok(validated_config)
                except c.Meltano.Singer.SAFE_EXCEPTIONS as e:
                    return r[t.GeneralValueMapping].fail(
                        f"Oracle config validation failed: {e}",
                    )

        class PerformanceOptimization:
            """Oracle tap performance optimization utilities.

            Constants are accessed via constants module:
                c.TapOracle.Performance.DEFAULT_BATCH_SIZE
                c.TapOracle.Performance.MAX_PARALLEL_STREAMS
                c.TapOracle.Performance.MEMORY_THRESHOLD_MB
            """

            @staticmethod
            def calculate_extraction_metrics(
                start_time: float,
                end_time: float,
                records_processed: int,
            ) -> r[Mapping[str, t.GeneralValueType]]:
                """Calculate extraction performance metrics."""
                try:
                    duration = end_time - start_time
                    records_per_second = records_processed / max(duration, 0.001)
                    performance_rating: str = (
                        "excellent"
                        if records_per_second
                        > c.TapOracle.EXCELLENT_PERFORMANCE_THRESHOLD
                        else "good"
                        if records_per_second > c.TapOracle.GOOD_PERFORMANCE_THRESHOLD
                        else "moderate"
                        if records_per_second
                        > c.TapOracle.MODERATE_PERFORMANCE_THRESHOLD
                        else "slow"
                    )
                    metrics: Mapping[str, t.GeneralValueType] = {
                        "duration_seconds": round(duration, 3),
                        "records_processed": records_processed,
                        "records_per_second": round(records_per_second, 2),
                        "performance_rating": performance_rating,
                    }
                    return r[t.GeneralValueMapping].ok(metrics)
                except c.Meltano.Singer.SAFE_EXCEPTIONS as e:
                    return r[t.GeneralValueMapping].fail(
                        f"Metrics calculation failed: {e}",
                    )

            @staticmethod
            def optimize_extraction_query(
                base_query: str,
                table_stats: Mapping[str, t.GeneralValueType],
            ) -> r[str]:
                """Optimize extraction query based on table statistics."""
                try:
                    optimized_query = base_query
                    row_count = table_stats.get("row_count", 0)
                    if isinstance(row_count, t.Numeric):
                        numeric_row_count = float(row_count)
                        if numeric_row_count > c.TapOracle.LARGE_TABLE_THRESHOLD:
                            optimized_query = f"/*+ PARALLEL(4) */ {optimized_query}"
                    if "primary_key" in table_stats:
                        pk_column = table_stats["primary_key"]
                        optimized_query = (
                            f"/*+ INDEX_ASC({pk_column}) */ {optimized_query}"
                        )
                    return r[str].ok(optimized_query)
                except c.Meltano.Singer.SAFE_EXCEPTIONS as e:
                    return r[str].fail(f"Query optimization failed: {e}")


u = FlextTapOracleUtilities
__all__: t.StrSequence = ["FlextTapOracleUtilities", "u"]
