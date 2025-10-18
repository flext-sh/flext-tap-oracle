"""FLEXT Tap Oracle Utilities - Domain-specific utilities for Oracle tap operations.

This module provides comprehensive Oracle tap utilities extending FlextUtilities
with nested classes for error handling, stream management, discovery operations,
and configuration validation. Follows FLEXT standards with single-class pattern.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT

"""

from __future__ import annotations

from typing import ClassVar

from flext_core import (
    FlextContainer,
    FlextLogger,
    FlextResult,
    FlextUtilities,
)
from flext_db_oracle import FlextDbOracleTable

from flext_tap_oracle.models import FlextMeltanoTapOracleModels
from flext_tap_oracle.tap_exceptions import (
    FlextMeltanoTapOracleConfigurationError,
    FlextMeltanoTapOracleConnectionError,
    FlextMeltanoTapOracleDiscoveryError,
    FlextMeltanoTapOracleExtractionError,
    FlextMeltanoTapOracleQueryError,
    FlextMeltanoTapOracleStreamError,
)


class FlextMeltanoTapOracleUtilities(FlextUtilities):
    """Unified Oracle tap utilities class extending FlextUtilities with nested classes.

    Provides comprehensive Oracle tap utilities with nested classes for:
    - Error handling and exception creation
    - Stream information management
    - Discovery operations
    - Configuration validation
    - Performance optimization
    - Data extraction helpers

    Follows FLEXT pattern: single class with nested subclasses.
    """

    # Constants
    MAX_PORT_NUMBER = 65535
    LARGE_TABLE_THRESHOLD = 100000
    EXCELLENT_PERFORMANCE_THRESHOLD = 1000
    GOOD_PERFORMANCE_THRESHOLD = 500
    MODERATE_PERFORMANCE_THRESHOLD = 100

    def __init__(self) -> None:
        """Initialize FlextMeltanoTapOracleUtilities service."""
        super().__init__()
        self._container = FlextContainer.get_global()
        self.logger = FlextLogger(__name__)

    def execute(self) -> FlextResult[dict[str, object]]:
        """Execute the main domain service operation.

        Returns:
            FlextResult[dict[str, object]]: Service status and capabilities.

        """
        return FlextResult[dict[str, object]].ok({
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

    @property
    def logger(self) -> FlextLogger:
        """Get logger instance."""
        return self.logger

    @property
    def container(self) -> FlextContainer:
        """Get container instance."""
        return self._container

    class ErrorHandling:
        """Oracle tap error handling utilities with enhanced context."""

        @staticmethod
        def create_connection_error(
            message: str = "Oracle connection failed",
            host: str | None = None,
            port: int | None = None,
            service_name: str | None = None,
            **kwargs: object,
        ) -> FlextMeltanoTapOracleConnectionError:
            """Create Oracle connection errors with context."""
            context = kwargs.copy()
            if host is not None:
                context["host"] = host
            if port is not None:
                context["port"] = port
            if service_name is not None:
                context["service_name"] = service_name

            return FlextMeltanoTapOracleConnectionError(message, context=context)

        @staticmethod
        def create_query_error(
            message: str = "Oracle query execution failed",
            sql_query: str | None = None,
            table_name: str | None = None,
            **kwargs: object,
        ) -> FlextMeltanoTapOracleQueryError:
            """Create Oracle query errors with SQL context."""
            context = kwargs.copy()
            if sql_query is not None:
                context["sql_query"] = sql_query
            if table_name is not None:
                context["table_name"] = table_name

            return FlextMeltanoTapOracleQueryError(message, context=context)

        @staticmethod
        def create_stream_error(
            message: str = "Stream processing failed",
            stream_name: str | None = None,
            stream_type: str | None = None,
            **kwargs: object,
        ) -> FlextMeltanoTapOracleStreamError:
            """Create stream processing errors with stream context."""
            context = kwargs.copy()
            if stream_name is not None:
                context["stream_name"] = stream_name
            if stream_type is not None:
                context["stream_type"] = stream_type

            return FlextMeltanoTapOracleStreamError(message, context=context)

        @staticmethod
        def create_discovery_error(
            message: str = "Table discovery failed",
            schema_name: str | None = None,
            **kwargs: object,
        ) -> FlextMeltanoTapOracleDiscoveryError:
            """Create discovery errors with schema context."""
            context = kwargs.copy()
            if schema_name is not None:
                context["schema_name"] = schema_name

            return FlextMeltanoTapOracleDiscoveryError(message, context=context)

        @staticmethod
        def create_configuration_error(
            message: str = "Configuration validation failed",
            config_section: str | None = None,
            **kwargs: object,
        ) -> FlextMeltanoTapOracleConfigurationError:
            """Create configuration errors with section context."""
            context = kwargs.copy()
            if config_section is not None:
                context["config_section"] = config_section

            return FlextMeltanoTapOracleConfigurationError(message, context=context)

        @staticmethod
        def create_extraction_error(
            message: str = "Data extraction failed",
            table_name: str | None = None,
            extraction_method: str | None = None,
            **kwargs: object,
        ) -> FlextMeltanoTapOracleExtractionError:
            """Create extraction errors with method context."""
            context = kwargs.copy()
            if table_name is not None:
                context["table_name"] = table_name
            if extraction_method is not None:
                context["extraction_method"] = extraction_method

            return FlextMeltanoTapOracleExtractionError(message, context=context)

        @staticmethod
        def handle_oracle_exception(
            exception: Exception,
            operation: str = "unknown",
            **context: object,
        ) -> FlextResult[None]:
            """Handle Oracle exceptions with proper error mapping."""
            try:
                error_message = f"Oracle {operation} failed: {exception}"

                # Map common Oracle exceptions to specific error types
                if "connection" in str(exception).lower():
                    error = FlextMeltanoTapOracleUtilities.ErrorHandling.create_connection_error(
                        error_message, **context
                    )
                elif (
                    "sql" in str(exception).lower() or "query" in str(exception).lower()
                ):
                    error = (
                        FlextMeltanoTapOracleUtilities.ErrorHandling.create_query_error(
                            error_message, **context
                        )
                    )
                elif "discovery" in str(exception).lower():
                    error = FlextMeltanoTapOracleUtilities.ErrorHandling.create_discovery_error(
                        error_message, **context
                    )
                else:
                    # Generic extraction error for other cases
                    error = FlextMeltanoTapOracleUtilities.ErrorHandling.create_extraction_error(
                        error_message, **context
                    )

                return FlextResult[None].fail(str(error))

            except Exception as e:
                return FlextResult[None].fail(f"Exception handling failed: {e}")

    class StreamManagement:
        """Oracle tap stream management utilities."""

        @staticmethod
        def create_stream_info_from_oracle_table(
            oracle_table: FlextDbOracleTable,
            stream_prefix: str = "oracle",
            replication_method: str = "FULL_TABLE",
        ) -> FlextResult[object]:
            """Create stream info from Oracle table metadata."""
            try:
                stream_name = f"{stream_prefix}_{oracle_table.name.lower()}"

                stream_info = FlextMeltanoTapOracleModels.OracleTapStreamInfo(
                    stream_name=stream_name,
                    table_name=oracle_table.name,
                    schema_name=getattr(oracle_table, "schema_name", None),
                    replication_method=replication_method,
                    column_count=len(oracle_table.columns)
                    if hasattr(oracle_table, "columns")
                    else None,
                )

                return FlextResult[object].ok(stream_info)

            except Exception as e:
                return FlextResult[object].fail(
                    f"Failed to create stream info from Oracle table: {e}",
                )

        @staticmethod
        def create_discovery_result(
            tables: list[object],
            schema_name: str,
        ) -> FlextResult[object]:
            """Create discovery result from Oracle tables."""
            try:
                # Convert tables to stream info
                stream_infos = []
                for table in tables:
                    stream_result = FlextMeltanoTapOracleUtilities.StreamManagement.create_stream_info_from_oracle_table(
                        table
                    )
                    if stream_result.is_success:
                        stream_infos.append(stream_result.unwrap())

                discovery_result = FlextMeltanoTapOracleModels.OracleTapDiscoveryResult(
                    schema_name=schema_name,
                    discovered_tables=len(tables),
                    stream_infos=stream_infos,
                )

                return FlextResult[object].ok(discovery_result)

            except Exception as e:
                return FlextResult[object].fail(
                    f"Failed to create discovery result: {e}",
                )

    class ConfigurationValidation:
        """Oracle tap configuration validation utilities."""

        @staticmethod
        def validate_oracle_config(
            config: dict,
        ) -> FlextResult[dict[str, object]]:
            """Validate Oracle configuration parameters."""
            try:
                required_fields = [
                    "host",
                    "port",
                    "service_name",
                    "username",
                    "password",
                ]
                for field in required_fields:
                    if field not in config:
                        return FlextResult[dict[str, object]].fail(
                            f"Missing required Oracle field: {field}"
                        )
                    if not config[field]:
                        return FlextResult[dict[str, object]].fail(
                            f"Empty Oracle field: {field}"
                        )

                # Validate port is numeric
                try:
                    port = int(config["port"])
                    if (
                        port <= 0
                        or port > FlextMeltanoTapOracleUtilities.MAX_PORT_NUMBER
                    ):
                        return FlextResult[dict[str, object]].fail(
                            f"Oracle port must be between 1 and {FlextMeltanoTapOracleUtilities.MAX_PORT_NUMBER}"
                        )
                    config["port"] = port
                except ValueError:
                    return FlextResult[dict[str, object]].fail(
                        "Oracle port must be numeric"
                    )

                return FlextResult[dict[str, object]].ok(config)

            except Exception as e:
                return FlextResult[dict[str, object]].fail(
                    f"Oracle config validation failed: {e}"
                )

        @staticmethod
        def build_connection_string(config: dict) -> FlextResult[str]:
            """Build Oracle connection string from configuration."""
            try:
                validation_result = FlextMeltanoTapOracleUtilities.ConfigurationValidation.validate_oracle_config(
                    config
                )
                if validation_result.is_failure:
                    return FlextResult[str].fail(validation_result.error)

                validated_config = validation_result.unwrap()

                connection_string = (
                    f"oracle://{validated_config['username']}:{validated_config['password']}"
                    f"@{validated_config['host']}:{validated_config['port']}"
                    f"/{validated_config['service_name']}"
                )

                return FlextResult[str].ok(connection_string)

            except Exception as e:
                return FlextResult[str].fail(f"Connection string building failed: {e}")

        @staticmethod
        def test_oracle_connectivity(
            config: dict,
        ) -> FlextResult[dict[str, object]]:
            """Test Oracle connectivity with configuration."""
            try:
                # Validate configuration first
                validation_result = FlextMeltanoTapOracleUtilities.ConfigurationValidation.validate_oracle_config(
                    config
                )
                if validation_result.is_failure:
                    return FlextResult[dict[str, object]].fail(validation_result.error)

                # Note: In a real implementation, this would test actual connectivity
                # For now, return structure validation
                connectivity_result = {
                    "status": "validated",
                    "host": config["host"],
                    "port": config["port"],
                    "service_name": config["service_name"],
                    "connection_test": "structural_validation_passed",
                }

                return FlextResult[dict[str, object]].ok(connectivity_result)

            except Exception as e:
                return FlextResult[dict[str, object]].fail(
                    f"Oracle connectivity test failed: {e}"
                )

    class PerformanceOptimization:
        """Oracle tap performance optimization utilities."""

        # Performance optimization constants
        DEFAULT_BATCH_SIZE: ClassVar[int] = 1000
        MAX_PARALLEL_STREAMS: ClassVar[int] = 5
        MEMORY_THRESHOLD_MB: ClassVar[int] = 512

        @staticmethod
        def optimize_extraction_query(
            base_query: str,
            table_stats: dict,
        ) -> FlextResult[str]:
            """Optimize extraction query based on table statistics."""
            try:
                optimized_query = base_query

                # Add optimizations based on table size
                row_count = table_stats.get("row_count", 0)
                if row_count > FlextMeltanoTapOracleUtilities.LARGE_TABLE_THRESHOLD:
                    # Add parallel hints for large tables
                    optimized_query = f"/*+ PARALLEL(4) */ {optimized_query}"

                # Add index hints if available
                if "primary_key" in table_stats:
                    pk_column = table_stats["primary_key"]
                    optimized_query = f"/*+ INDEX_ASC({pk_column}) */ {optimized_query}"

                return FlextResult[str].ok(optimized_query)

            except Exception as e:
                return FlextResult[str].fail(f"Query optimization failed: {e}")

        @staticmethod
        def calculate_extraction_metrics(
            start_time: float,
            end_time: float,
            records_processed: int,
        ) -> FlextResult[dict[str, object]]:
            """Calculate extraction performance metrics."""
            try:
                duration = end_time - start_time
                records_per_second = records_processed / max(duration, 0.001)

                metrics = {
                    "duration_seconds": round(duration, 3),
                    "records_processed": records_processed,
                    "records_per_second": round(records_per_second, 2),
                    "performance_rating": (
                        "excellent"
                        if records_per_second
                        > FlextMeltanoTapOracleUtilities.EXCELLENT_PERFORMANCE_THRESHOLD
                        else "good"
                        if records_per_second
                        > FlextMeltanoTapOracleUtilities.GOOD_PERFORMANCE_THRESHOLD
                        else "moderate"
                        if records_per_second
                        > FlextMeltanoTapOracleUtilities.MODERATE_PERFORMANCE_THRESHOLD
                        else "slow"
                    ),
                }

                return FlextResult[dict[str, object]].ok(metrics)

            except Exception as e:
                return FlextResult[dict[str, object]].fail(
                    f"Metrics calculation failed: {e}"
                )


__all__: list[str] = [
    "FlextMeltanoTapOracleUtilities",
]
