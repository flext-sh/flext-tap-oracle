"""Oracle Tap Exceptions - Comprehensive Error Handling.

Exception hierarchy for flext-tap-oracle extending FlextExceptions with
Oracle tap-specific context fields for database operations, schema discovery,
and Singer protocol data extraction.

Copyright (c) 2025 FLEXT Contributors
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from typing import override

from flext_core import FlextConstants, FlextExceptions, FlextTypes


class FlextMeltanoTapOracleExceptions:
    """Oracle tap exception hierarchy extending FlextExceptions.

    Provides structured error handling with Oracle-specific context:
    - Query errors with SQL and Oracle error codes
    - Stream processing errors with table and record context
    - Schema discovery errors with metadata context
    - Connection errors with Oracle database context
    """

    class TapError(FlextExceptions.BaseError):
        """Base error for Oracle tap operations with Singer context."""

        @override
        def __init__(
            self,
            message: str,
            *,
            tap_stream_id: str | None = None,
            catalog_entry: str | None = None,
            **kwargs: object,
        ) -> None:
            """Initialize Oracle tap error with Singer tap context."""
            self.tap_stream_id = tap_stream_id
            self.catalog_entry = catalog_entry

            # Extract common parameters
            base_context, correlation_id, error_code = self._extract_common_kwargs(
                kwargs
            )

            # Build context with Singer tap-specific fields
            context = self._build_context(
                base_context,
                tap_stream_id=tap_stream_id,
                catalog_entry=catalog_entry,
            )

            super().__init__(
                message,
                code=error_code or FlextConstants.Errors.GENERIC_ERROR,
                context=context,
                correlation_id=correlation_id,
            )

    class ValidationError(FlextExceptions.ValidationError):
        """Oracle tap validation error - extends FlextExceptions."""

        @override
        def __init__(
            self,
            message: str,
            stream_name: str | None = None,
            **kwargs: object,
        ) -> None:
            """Initialize Oracle tap validation error."""
            self.stream_name = stream_name

            # Extract common parameters
            base_context, correlation_id, error_code = self._extract_common_kwargs(
                kwargs
            )

            # Build context with stream info
            context = self._build_context(
                base_context,
                stream_name=stream_name,
            )

            super().__init__(
                message,
                context=context,
                correlation_id=correlation_id,
                error_code=error_code or "TAP_VALIDATION_ERROR",
                **{
                    k: v
                    for k, v in kwargs.items()
                    if k not in {"context", "correlation_id", "error_code"}
                },
            )

    class OracleConnectionError(FlextExceptions.ConnectionError):
        """Oracle tap connection error - extends FlextExceptions."""

        @override
        def __init__(
            self,
            message: str,
            host: str | None = None,
            port: int | None = None,
            service_name: str | None = None,
            **kwargs: object,
        ) -> None:
            """Initialize Oracle connection error."""
            self.host = host
            self.port = port
            self.service_name = service_name

            # Extract common parameters
            base_context, correlation_id, error_code = self._extract_common_kwargs(
                kwargs
            )

            # Build context with Oracle connection details
            context = self._build_context(
                base_context,
                host=host,
                port=port,
                service_name=service_name,
            )

            super().__init__(
                message,
                context=context,
                correlation_id=correlation_id,
                error_code=error_code or "TAP_ORACLE_CONNECTION_ERROR",
                **{
                    k: v
                    for k, v in kwargs.items()
                    if k not in {"context", "correlation_id", "error_code"}
                },
            )

    class ConfigurationError(FlextExceptions.ConfigurationError):
        """Oracle tap configuration error - extends FlextExceptions."""

        @override
        def __init__(
            self,
            message: str,
            config_key: str | None = None,
            **kwargs: object,
        ) -> None:
            """Initialize Oracle tap configuration error."""
            # Extract common parameters
            base_context, correlation_id, _ = self._extract_common_kwargs(kwargs)

            # Build context with config key
            context = self._build_context(
                base_context,
                config_key=config_key,
            )

            super().__init__(
                message,
                config_key=config_key,
                context=context,
                correlation_id=correlation_id,
                **{
                    k: v
                    for k, v in kwargs.items()
                    if k
                    not in {"context", "correlation_id", "error_code", "config_key"}
                },
            )

    class ProcessingError(FlextExceptions.ProcessingError):
        """Oracle tap processing error - extends FlextExceptions."""

        @override
        def __init__(
            self,
            message: str,
            operation: str | None = None,
            **kwargs: object,
        ) -> None:
            """Initialize Oracle tap processing error."""
            self.operation = operation

            # Extract common parameters
            base_context, correlation_id, error_code = self._extract_common_kwargs(
                kwargs
            )

            # Build context with operation info
            context = self._build_context(
                base_context,
                operation=operation,
            )

            super().__init__(
                message,
                operation=operation,
                context=context,
                correlation_id=correlation_id,
                error_code=error_code or "TAP_PROCESSING_ERROR",
                **{
                    k: v
                    for k, v in kwargs.items()
                    if k not in {"context", "correlation_id", "error_code", "operation"}
                },
            )

    class QueryError(TapError):
        """Oracle tap SQL query error with Oracle-specific context."""

        @override
        def __init__(
            self,
            message: str = "Oracle tap query failed",
            query: str | None = None,
            oracle_error_code: str | None = None,
            table_name: str | None = None,
            **kwargs: object,
        ) -> None:
            """Initialize Oracle query error with SQL and error code context."""
            self.query = query[:200] if query else None  # Truncate long queries
            self.oracle_error_code = oracle_error_code
            self.table_name = table_name

            # Extract common parameters
            base_context, correlation_id, error_code = self._extract_common_kwargs(
                kwargs
            )

            # Build context with Oracle query details
            context = self._build_context(
                base_context,
                query=self.query,
                oracle_error_code=oracle_error_code,
                table_name=table_name,
            )

            super().__init__(
                f"Oracle query error: {message}",
                context=context,
                correlation_id=correlation_id,
                error_code=error_code or f"ORACLE_{oracle_error_code}"
                if oracle_error_code
                else "TAP_QUERY_ERROR",
                **{
                    k: v
                    for k, v in kwargs.items()
                    if k not in {"context", "correlation_id", "error_code"}
                },
            )

    class StreamError(TapError):
        """Oracle tap stream processing error with stream context."""

        @override
        def __init__(
            self,
            message: str = "Oracle tap stream error",
            stream_name: str | None = None,
            table_name: str | None = None,
            record_count: int | None = None,
            **kwargs: object,
        ) -> None:
            """Initialize stream error with processing context."""
            self.stream_name = stream_name
            self.table_name = table_name
            self.record_count = record_count

            # Extract common parameters
            base_context, correlation_id, error_code = self._extract_common_kwargs(
                kwargs
            )

            # Build context with stream details
            context = self._build_context(
                base_context,
                stream_name=stream_name,
                table_name=table_name,
                record_count=record_count,
            )

            super().__init__(
                f"Stream processing error: {message}",
                tap_stream_id=stream_name,
                context=context,
                correlation_id=correlation_id,
                error_code=error_code or "TAP_STREAM_ERROR",
                **{
                    k: v
                    for k, v in kwargs.items()
                    if k not in {"context", "correlation_id", "error_code"}
                },
            )

    class DiscoveryError(TapError):
        """Oracle tap schema discovery error with metadata context."""

        @override
        def __init__(
            self,
            message: str = "Oracle tap discovery failed",
            schema_name: str | None = None,
            table_count: int | None = None,
            **kwargs: object,
        ) -> None:
            """Initialize discovery error with schema context."""
            self.schema_name = schema_name
            self.table_count = table_count

            # Extract common parameters
            base_context, correlation_id, error_code = self._extract_common_kwargs(
                kwargs
            )

            # Build context with discovery details
            context = self._build_context(
                base_context,
                schema_name=schema_name,
                table_count=table_count,
            )

            super().__init__(
                f"Schema discovery error: {message}",
                context=context,
                correlation_id=correlation_id,
                error_code=error_code or "TAP_DISCOVERY_ERROR",
                **{
                    k: v
                    for k, v in kwargs.items()
                    if k not in {"context", "correlation_id", "error_code"}
                },
            )

    class MetadataError(TapError):
        """Oracle tap metadata error with table/column context."""

        @override
        def __init__(
            self,
            message: str = "Oracle tap metadata error",
            table_name: str | None = None,
            schema_name: str | None = None,
            column_name: str | None = None,
            **kwargs: object,
        ) -> None:
            """Initialize metadata error with database object context."""
            self.table_name = table_name
            self.schema_name = schema_name
            self.column_name = column_name

            # Extract common parameters
            base_context, correlation_id, error_code = self._extract_common_kwargs(
                kwargs
            )

            # Build context with metadata details
            context = self._build_context(
                base_context,
                table_name=table_name,
                schema_name=schema_name,
                column_name=column_name,
            )

            super().__init__(
                f"Metadata error: {message}",
                context=context,
                correlation_id=correlation_id,
                error_code=error_code or "TAP_METADATA_ERROR",
                **{
                    k: v
                    for k, v in kwargs.items()
                    if k not in {"context", "correlation_id", "error_code"}
                },
            )

    class ExtractionError(ProcessingError):
        """Oracle tap data extraction error with batch context."""

        @override
        def __init__(
            self,
            message: str = "Oracle tap extraction failed",
            table_name: str | None = None,
            batch_size: int | None = None,
            records_processed: int | None = None,
            **kwargs: object,
        ) -> None:
            """Initialize extraction error with batch processing context."""
            self.table_name = table_name
            self.batch_size = batch_size
            self.records_processed = records_processed

            # Extract common parameters
            base_context, correlation_id, error_code = self._extract_common_kwargs(
                kwargs
            )

            # Build context with extraction details
            context = self._build_context(
                base_context,
                table_name=table_name,
                batch_size=batch_size,
                records_processed=records_processed,
            )

            super().__init__(
                f"Data extraction error: {message}",
                operation="data_extraction",
                context=context,
                correlation_id=correlation_id,
                error_code=error_code or "TAP_EXTRACTION_ERROR",
                **{
                    k: v
                    for k, v in kwargs.items()
                    if k not in {"context", "correlation_id", "error_code", "operation"}
                },
            )


# Backward compatibility aliases - property-based exports
FlextMeltanoTapOracleError = FlextMeltanoTapOracleExceptions.TapError
FlextMeltanoTapOracleValidationError = FlextMeltanoTapOracleExceptions.ValidationError
FlextMeltanoTapOracleConnectionError = (
    FlextMeltanoTapOracleExceptions.OracleConnectionError
)
FlextMeltanoTapOracleConfigurationError = (
    FlextMeltanoTapOracleExceptions.ConfigurationError
)
FlextMeltanoTapOracleProcessingError = FlextMeltanoTapOracleExceptions.ProcessingError
FlextMeltanoTapOracleQueryError = FlextMeltanoTapOracleExceptions.QueryError
FlextMeltanoTapOracleStreamError = FlextMeltanoTapOracleExceptions.StreamError
FlextMeltanoTapOracleDiscoveryError = FlextMeltanoTapOracleExceptions.DiscoveryError
FlextMeltanoTapOracleMetadataError = FlextMeltanoTapOracleExceptions.MetadataError
FlextMeltanoTapOracleExtractionError = FlextMeltanoTapOracleExceptions.ExtractionError


__all__: FlextTypes.StringList = [
    "FlextMeltanoTapOracleConfigurationError",
    "FlextMeltanoTapOracleConnectionError",
    "FlextMeltanoTapOracleDiscoveryError",
    "FlextMeltanoTapOracleError",
    "FlextMeltanoTapOracleExceptions",
    "FlextMeltanoTapOracleExtractionError",
    "FlextMeltanoTapOracleMetadataError",
    "FlextMeltanoTapOracleProcessingError",
    "FlextMeltanoTapOracleQueryError",
    "FlextMeltanoTapOracleStreamError",
    "FlextMeltanoTapOracleValidationError",
]
