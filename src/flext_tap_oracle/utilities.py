"""FLEXT Tap Oracle Utilities - Domain-specific utilities for Oracle tap operations.

This module provides complete Oracle tap utilities extending u
with nested classes for error handling, stream management, discovery operations,
and configuration validation. Follows FLEXT standards with single-class pattern.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT

"""

from __future__ import annotations

from collections.abc import Mapping
from datetime import UTC, datetime
from typing import Literal

from flext_core import (
    FlextContainer,
    FlextExceptions,
    FlextLogger,
    FlextResult,
    t,
)
from flext_db_oracle import FlextDbOracleModels, FlextDbOracleUtilities
from flext_meltano import FlextMeltanoUtilities

from flext_tap_oracle.constants import c
from flext_tap_oracle.models import m


class FlextTapOracleUtilities(FlextMeltanoUtilities, FlextDbOracleUtilities):
    """Unified Oracle tap utilities class extending u classes.

    Provides complete Oracle tap utilities with nested classes for:
    - Error handling and exception creation
    - Stream information management
    - Discovery operations
    - Configuration validation
    - Performance optimization
    - Data extraction helpers

    Follows FLEXT pattern: single class with nested subclasses.
    """

    class TapOracle:
        """Tap Oracle  namespace for cross-project access."""

        def __init__(self) -> None:
            """Initialize FlextTapOracleUtilities service."""
            super().__init__()
            self._container = FlextContainer.get_global()
            self._logger = FlextLogger(__name__)

        @property
        def container(self) -> FlextContainer:
            """Get container instance."""
            return self._container

        @property
        def logger(self) -> FlextLogger:
            """Get logger instance."""
            return self._logger

        def execute(self) -> FlextResult[Mapping[str, t.ContainerValue]]:
            """Execute the main domain service operation.

            Returns:
            FlextResult[Mapping[str, t.ContainerValue]]: Service status and capabilities.

            """
            return FlextResult[Mapping[str, t.ContainerValue]].ok({
                "status": "operational",
                "service": "flext-tap-oracle-utilities",
                "capabilities": [
                    "error_handling",
                    "stream_management",
                    "discovery_operations",
                    "configuration_validation",
                    "performance_optimization",
                    "data_extraction",
                ],
            })

        class ErrorHandling:
            """Oracle tap error handling utilities with enhanced context."""

            @staticmethod
            def create_configuration_error(
                message: str = "Configuration validation failed",
                config_section: str | None = None,
            ) -> FlextExceptions.ConfigurationError:
                """Create configuration errors with section context."""
                context: dict[str, str] = {}
                if config_section is not None:
                    context["config_section"] = config_section

                return FlextExceptions.ConfigurationError(message, context=context)

            @staticmethod
            def create_connection_error(
                message: str = "Oracle connection failed",
                host: str | None = None,
                port: int | None = None,
                service_name: str | None = None,
            ) -> FlextExceptions.ConnectionError:
                """Create Oracle connection errors with context."""
                context: dict[str, str | int] = {}
                if host is not None:
                    context["host"] = host
                if port is not None:
                    context["port"] = port
                if service_name is not None:
                    context["service_name"] = service_name

                return FlextExceptions.ConnectionError(message, context=context)

            @staticmethod
            def create_discovery_error(
                message: str = "Table discovery failed",
                schema_name: str | None = None,
            ) -> FlextExceptions.OperationError:
                """Create discovery errors with schema context."""
                context: dict[str, str] = {}
                if schema_name is not None:
                    context["schema_name"] = schema_name

                return FlextExceptions.OperationError(message, context=context)

            @staticmethod
            def create_extraction_error(
                message: str = "Data extraction failed",
                table_name: str | None = None,
                extraction_method: str | None = None,
            ) -> FlextExceptions.OperationError:
                """Create extraction errors with method context."""
                context: dict[str, str] = {}
                if table_name is not None:
                    context["table_name"] = table_name
                if extraction_method is not None:
                    context["extraction_method"] = extraction_method

                return FlextExceptions.OperationError(message, context=context)

            @staticmethod
            def create_query_error(
                message: str = "Oracle query execution failed",
                sql_query: str | None = None,
                table_name: str | None = None,
            ) -> FlextExceptions.OperationError:
                """Create Oracle query errors with SQL context."""
                context: dict[str, str] = {}
                if sql_query is not None:
                    context["sql_query"] = sql_query
                if table_name is not None:
                    context["table_name"] = table_name

                return FlextExceptions.OperationError(message, context=context)

            @staticmethod
            def create_stream_error(
                message: str = "Stream processing failed",
                stream_name: str | None = None,
                stream_type: str | None = None,
            ) -> FlextExceptions.OperationError:
                """Create stream processing errors with stream context."""
                context: dict[str, str] = {}
                if stream_name is not None:
                    context["stream_name"] = stream_name
                if stream_type is not None:
                    context["stream_type"] = stream_type

                return FlextExceptions.OperationError(message, context=context)

            @staticmethod
            def handle_oracle_exception(
                exception: Exception,
                operation: str = c.TapOracle.DEFAULT_OPERATION_NAME,
            ) -> FlextResult[bool]:
                """Handle Oracle exceptions with proper error mapping."""
                try:
                    error_message = f"Oracle {operation} failed: {exception}"
                    exc_str = str(exception).lower()

                    # Map common Oracle exceptions to specific error types
                    err_handling = FlextTapOracleUtilities.TapOracle.ErrorHandling
                    err: (
                        FlextExceptions.ConnectionError
                        | FlextExceptions.OperationError
                        | FlextExceptions.ConfigurationError
                    )
                    if "connection" in exc_str:
                        err = err_handling.create_connection_error(
                            error_message,
                        )
                    elif "sql" in exc_str or "query" in exc_str:
                        err = err_handling.create_query_error(
                            error_message,
                        )
                    elif "discovery" in exc_str:
                        err = err_handling.create_discovery_error(
                            error_message,
                        )
                    else:
                        err = err_handling.create_extraction_error(
                            error_message,
                        )

                    return FlextResult[bool].fail(str(err))

                except (ValueError, TypeError, KeyError, AttributeError, OSError) as e:
                    return FlextResult[bool].fail(f"Exception handling failed: {e}")

        class StreamManagement:
            """Oracle tap stream management utilities."""

            @staticmethod
            def create_discovery_result(
                tables: list[t.ContainerValue],
                schema_name: str,
            ) -> FlextResult[m.TapOracle.OracleTapDiscoveryResult]:
                """Create discovery result from Oracle tables."""
                try:
                    # Convert tables to stream info
                    stream_infos: list[m.TapOracle.OracleTapStreamInfo] = []
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
                    )

                    return FlextResult[m.TapOracle.OracleTapDiscoveryResult].ok(
                        discovery_result,
                    )

                except (ValueError, TypeError, KeyError, AttributeError, OSError) as e:
                    return FlextResult[m.TapOracle.OracleTapDiscoveryResult].fail(
                        f"Failed to create discovery result: {e}",
                    )

            @staticmethod
            def create_stream_info_from_oracle_table(
                oracle_table: FlextDbOracleModels.DbOracle.Table,
                stream_prefix: str = c.TapOracle.DEFAULT_STREAM_PREFIX,
                replication_method: Literal["FULL_TABLE", "INCREMENTAL"] = "FULL_TABLE",
            ) -> FlextResult[m.TapOracle.OracleTapStreamInfo]:
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
                    )

                    return FlextResult[m.TapOracle.OracleTapStreamInfo].ok(stream_info)

                except (ValueError, TypeError, KeyError, AttributeError, OSError) as e:
                    return FlextResult[m.TapOracle.OracleTapStreamInfo].fail(
                        f"Failed to create stream info from Oracle table: {e}",
                    )

        class ConfigurationValidation:
            """Oracle tap configuration validation utilities."""

            @staticmethod
            def build_connection_string(
                config: Mapping[str, t.ContainerValue],
            ) -> FlextResult[str]:
                """Build Oracle connection string from configuration."""
                try:
                    cfg_validator = (
                        FlextTapOracleUtilities.TapOracle.ConfigurationValidation
                    )
                    validation_result = cfg_validator.validate_oracle_config(config)
                    if validation_result.is_failure:
                        return FlextResult[str].fail(validation_result.error)

                    validated_config = validation_result.value

                    connection_string = (
                        f"oracle://{validated_config['username']}:{validated_config['password']}"
                        f"@{validated_config['host']}:{validated_config['port']}"
                        f"/{validated_config['service_name']}"
                    )

                    return FlextResult[str].ok(connection_string)

                except (ValueError, TypeError, KeyError, AttributeError, OSError) as e:
                    return FlextResult[str].fail(
                        f"Connection string building failed: {e}",
                    )

            @staticmethod
            def test_oracle_connectivity(
                config: Mapping[str, t.ContainerValue],
            ) -> FlextResult[Mapping[str, t.ContainerValue]]:
                """Test Oracle connectivity with configuration."""
                try:
                    # Validate configuration first
                    cfg_validator = (
                        FlextTapOracleUtilities.TapOracle.ConfigurationValidation
                    )
                    validation_result = cfg_validator.validate_oracle_config(config)
                    if validation_result.is_failure:
                        return FlextResult[Mapping[str, t.ContainerValue]].fail(
                            validation_result.error,
                        )

                    # Note: In a real implementation, this would test actual connectivity
                    # For now, return structure validation
                    connectivity_result = {
                        "status": "validated",
                        "host": config["host"],
                        "port": config["port"],
                        "service_name": config["service_name"],
                        "connection_test": "structural_validation_passed",
                    }

                    return FlextResult[Mapping[str, t.ContainerValue]].ok(
                        connectivity_result,
                    )

                except (ValueError, TypeError, KeyError, AttributeError, OSError) as e:
                    return FlextResult[Mapping[str, t.ContainerValue]].fail(
                        f"Oracle connectivity test failed: {e}",
                    )

            @staticmethod
            def validate_oracle_config(
                config: Mapping[str, t.ContainerValue],
            ) -> FlextResult[Mapping[str, t.ContainerValue]]:
                """Validate Oracle configuration parameters."""
                try:
                    validated_config: dict[str, t.ContainerValue] = dict(config)
                    required_fields = [
                        "host",
                        "port",
                        "service_name",
                        "username",
                        "password",
                    ]
                    for field in required_fields:
                        if field not in validated_config:
                            return FlextResult[Mapping[str, t.ContainerValue]].fail(
                                f"Missing required Oracle field: {field}",
                            )
                        if not validated_config[field]:
                            return FlextResult[Mapping[str, t.ContainerValue]].fail(
                                f"Empty Oracle field: {field}",
                            )

                    # Validate port is numeric
                    max_port = c.TapOracle.MAX_PORT_NUMBER
                    try:
                        port = int(str(validated_config["port"]))
                        if port <= 0 or port > max_port:
                            return FlextResult[Mapping[str, t.ContainerValue]].fail(
                                f"Oracle port must be between 1 and {max_port}",
                            )
                        validated_config["port"] = port
                    except ValueError:
                        return FlextResult[Mapping[str, t.ContainerValue]].fail(
                            "Oracle port must be numeric",
                        )

                    return FlextResult[Mapping[str, t.ContainerValue]].ok(
                        validated_config,
                    )

                except (ValueError, TypeError, KeyError, AttributeError, OSError) as e:
                    return FlextResult[Mapping[str, t.ContainerValue]].fail(
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
            ) -> FlextResult[Mapping[str, t.ContainerValue]]:
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

                    metrics: dict[str, t.ContainerValue] = {
                        "duration_seconds": round(duration, 3),
                        "records_processed": records_processed,
                        "records_per_second": round(records_per_second, 2),
                        "performance_rating": performance_rating,
                    }

                    return FlextResult[Mapping[str, t.ContainerValue]].ok(metrics)

                except (ValueError, TypeError, KeyError, AttributeError, OSError) as e:
                    return FlextResult[Mapping[str, t.ContainerValue]].fail(
                        f"Metrics calculation failed: {e}",
                    )

            @staticmethod
            def optimize_extraction_query(
                base_query: str,
                table_stats: Mapping[str, t.ContainerValue],
            ) -> FlextResult[str]:
                """Optimize extraction query based on table statistics."""
                try:
                    optimized_query = base_query

                    # Add optimizations based on table size
                    row_count = table_stats.get("row_count", 0)
                    if isinstance(row_count, int | float):
                        numeric_row_count = float(row_count)
                        if numeric_row_count > c.TapOracle.LARGE_TABLE_THRESHOLD:
                            # Add parallel hints for large tables
                            optimized_query = f"/*+ PARALLEL(4) */ {optimized_query}"

                    # Add index hints if available
                    if "primary_key" in table_stats:
                        pk_column = table_stats["primary_key"]
                        optimized_query = (
                            f"/*+ INDEX_ASC({pk_column}) */ {optimized_query}"
                        )

                    return FlextResult[str].ok(optimized_query)

                except (ValueError, TypeError, KeyError, AttributeError, OSError) as e:
                    return FlextResult[str].fail(f"Query optimization failed: {e}")


# Runtime alias for simplified usage
u = FlextTapOracleUtilities

__all__: list[str] = [
    "FlextTapOracleUtilities",
    "u",
]
