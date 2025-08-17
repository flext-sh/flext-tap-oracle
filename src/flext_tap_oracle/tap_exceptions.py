"""Oracle Tap Exceptions - Comprehensive Error Handling.

PEP8 CONSOLIDATION: All Oracle tap exception handling consolidated using the
factory pattern from flext-core. This module provides Oracle tap specific
exceptions while leveraging the established FLEXT error handling patterns.

Uses flext-core base exceptions with Oracle tap specific context.

Copyright (c) 2025 FLEXT Contributors
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from flext_core import (
    FlextError,
    FlextOperationError,
    FlextValidationError,
)

# =====================================================
# BASE ORACLE TAP EXCEPTIONS
# =====================================================


class FlextTapOracleError(FlextError):
    """Base error for Oracle tap operations."""


class FlextTapOracleValidationError(FlextValidationError):
    """Oracle tap validation errors."""


class FlextTapOracleConnectionError(FlextOperationError):
    """Oracle tap connection errors."""


class FlextTapOracleConfigurationError(FlextValidationError):
    """Oracle tap configuration errors."""


class FlextTapOracleProcessingError(FlextOperationError):
    """Oracle tap processing errors."""


# =====================================================
# ORACLE-SPECIFIC EXCEPTIONS WITH CONTEXT
# =====================================================


class FlextTapOracleQueryError(FlextTapOracleError):
    """Oracle tap SQL query errors with Oracle-specific context."""

    def __init__(
        self,
        message: str = "Oracle tap query failed",
        query: str | None = None,
        oracle_error_code: str | None = None,
        table_name: str | None = None,
        **kwargs: object,
    ) -> None:
        """Initialize Oracle tap query error with Oracle-specific context."""
        context = kwargs.copy()
        if query is not None:
            context["query"] = query[:200]  # Truncate long queries
        if oracle_error_code is not None:
            context["oracle_error_code"] = oracle_error_code
        if table_name is not None:
            context["table_name"] = table_name

        super().__init__(f"Oracle tap query: {message}", context=context)


class FlextTapOracleStreamError(FlextTapOracleError):
    """Oracle tap stream processing errors with stream-specific context."""

    def __init__(
        self,
        message: str = "Oracle tap stream error",
        stream_name: str | None = None,
        table_name: str | None = None,
        record_count: int | None = None,
        **kwargs: object,
    ) -> None:
        """Initialize Oracle tap stream error with stream-specific context."""
        context = kwargs.copy()
        if stream_name is not None:
            context["stream_name"] = stream_name
        if table_name is not None:
            context["table_name"] = table_name
        if record_count is not None:
            context["record_count"] = record_count

        super().__init__(f"Oracle tap stream: {message}", context=context)


class FlextTapOracleDiscoveryError(FlextTapOracleError):
    """Oracle tap discovery errors with discovery-specific context."""

    def __init__(
        self,
        message: str = "Oracle tap discovery failed",
        schema_name: str | None = None,
        table_count: int | None = None,
        **kwargs: object,
    ) -> None:
        """Initialize Oracle tap discovery error with discovery-specific context."""
        context = kwargs.copy()
        if schema_name is not None:
            context["schema_name"] = schema_name
        if table_count is not None:
            context["table_count"] = table_count

        super().__init__(f"Oracle tap discovery: {message}", context=context)


class FlextTapOracleMetadataError(FlextTapOracleError):
    """Oracle tap metadata errors with metadata-specific context."""

    def __init__(
        self,
        message: str = "Oracle tap metadata error",
        table_name: str | None = None,
        schema_name: str | None = None,
        column_name: str | None = None,
        **kwargs: object,
    ) -> None:
        """Initialize Oracle tap metadata error with metadata-specific context."""
        context = kwargs.copy()
        if table_name is not None:
            context["table_name"] = table_name
        if schema_name is not None:
            context["schema_name"] = schema_name
        if column_name is not None:
            context["column_name"] = column_name

        super().__init__(f"Oracle tap metadata: {message}", context=context)


class FlextTapOracleExtractionError(FlextTapOracleProcessingError):
    """Oracle tap data extraction errors with extraction-specific context."""

    def __init__(
        self,
        message: str = "Oracle tap extraction failed",
        table_name: str | None = None,
        batch_size: int | None = None,
        records_processed: int | None = None,
        **kwargs: object,
    ) -> None:
        """Initialize Oracle tap extraction error with extraction-specific context."""
        context = kwargs.copy()
        if table_name is not None:
            context["table_name"] = table_name
        if batch_size is not None:
            context["batch_size"] = batch_size
        if records_processed is not None:
            context["records_processed"] = records_processed

        super().__init__(f"Oracle tap extraction: {message}", context=context)


# =====================================================
# EXCEPTION FACTORY USING FLEXT-CORE PATTERN
# =====================================================

# Note: Exception factory functionality can be added later if needed
# For now, using direct exception instantiation with context


# =====================================================
# FACTORY FUNCTIONS FOR COMMON ORACLE TAP ERRORS
# =====================================================


def create_connection_error(
    message: str = "Oracle connection failed",
    host: str | None = None,
    port: int | None = None,
    service_name: str | None = None,
    **kwargs: object,
) -> FlextTapOracleConnectionError:
    """Create Oracle connection errors with context.

    Args:
      message: Error message
      host: Oracle host
      port: Oracle port
      service_name: Oracle service name
      **kwargs: Additional context

    Returns:
      Configured Oracle connection error

    """
    context = kwargs.copy()
    if host is not None:
        context["host"] = host
    if port is not None:
        context["port"] = port
    if service_name is not None:
        context["service_name"] = service_name

    return FlextTapOracleConnectionError(message, context=context)


def create_query_error(
    message: str = "Oracle query failed",
    query: str | None = None,
    table_name: str | None = None,
    oracle_error_code: str | None = None,
    **kwargs: object,
) -> FlextTapOracleQueryError:
    """Create Oracle query errors with context.

    Args:
      message: Error message
      query: SQL query that failed
      table_name: Oracle table name
      oracle_error_code: Oracle-specific error code
      **kwargs: Additional context

    Returns:
      Configured Oracle query error

    """
    return FlextTapOracleQueryError(
        message=message,
        query=query,
        oracle_error_code=oracle_error_code,
        table_name=table_name,
        **kwargs,
    )


def create_stream_error(
    message: str = "Stream processing failed",
    stream_name: str | None = None,
    table_name: str | None = None,
    record_count: int | None = None,
    **kwargs: object,
) -> FlextTapOracleStreamError:
    """Create Oracle stream errors with context.

    Args:
      message: Error message
      stream_name: Singer stream name
      table_name: Oracle table name
      record_count: Number of records processed before failure
      **kwargs: Additional context

    Returns:
      Configured Oracle stream error

    """
    return FlextTapOracleStreamError(
        message=message,
        stream_name=stream_name,
        table_name=table_name,
        record_count=record_count,
        **kwargs,
    )


def create_discovery_error(
    message: str = "Discovery failed",
    schema_name: str | None = None,
    table_count: int | None = None,
    **kwargs: object,
) -> FlextTapOracleDiscoveryError:
    """Create Oracle discovery errors with context.

    Args:
      message: Error message
      schema_name: Oracle schema name
      table_count: Number of tables discovered before failure
      **kwargs: Additional context

    Returns:
      Configured Oracle discovery error

    """
    return FlextTapOracleDiscoveryError(
        message=message,
        schema_name=schema_name,
        table_count=table_count,
        **kwargs,
    )


def create_configuration_error(
    message: str = "Configuration invalid",
    config_field: str | None = None,
    config_value: object = None,
    **kwargs: object,
) -> FlextTapOracleConfigurationError:
    """Create Oracle configuration errors with context.

    Args:
      message: Error message
      config_field: Configuration field that caused the error
      config_value: Invalid configuration value
      **kwargs: Additional context

    Returns:
      Configured Oracle configuration error

    """
    context = kwargs.copy()
    if config_field is not None:
        context["config_field"] = config_field
    if config_value is not None:
        context["config_value"] = str(config_value)

    return FlextTapOracleConfigurationError(message, context=context)


def create_extraction_error(
    message: str = "Data extraction failed",
    table_name: str | None = None,
    batch_size: int | None = None,
    records_processed: int | None = None,
    **kwargs: object,
) -> FlextTapOracleExtractionError:
    """Create Oracle extraction errors with context.

    Args:
      message: Error message
      table_name: Oracle table name
      batch_size: Configured batch size
      records_processed: Number of records processed before failure
      **kwargs: Additional context

    Returns:
      Configured Oracle extraction error

    """
    return FlextTapOracleExtractionError(
        message=message,
        table_name=table_name,
        batch_size=batch_size,
        records_processed=records_processed,
        **kwargs,
    )


# =====================================================
# ERROR HANDLING UTILITIES
# =====================================================


def handle_oracle_exception(
    exc: Exception,
    operation: str = "unknown",
    **context: object,
) -> FlextTapOracleError:
    """Convert generic exceptions to Oracle tap specific errors.

    Args:
      exc: Original exception
      operation: Operation that failed
      **context: Additional context

    Returns:
      Oracle tap specific error

    """
    base_message = f"Oracle tap {operation} failed: {exc}"
    full_context = {
        "original_exception": str(exc),
        "exception_type": type(exc).__name__,
        "operation": operation,
        **context,
    }

    # Map common exception types to specific Oracle tap errors
    if "connection" in str(exc).lower() or "connect" in str(exc).lower():
        return FlextTapOracleError(base_message, context=full_context)
    if "query" in str(exc).lower() or "sql" in str(exc).lower():
        return FlextTapOracleError(base_message, context=full_context)
    if "stream" in str(exc).lower():
        return FlextTapOracleError(base_message, context=full_context)
    if "discovery" in str(exc).lower():
        return FlextTapOracleError(base_message, context=full_context)
    if "config" in str(exc).lower():
        return FlextTapOracleError(base_message, context=full_context)
    return FlextTapOracleError(base_message, context=full_context)


# =====================================================
# EXPORTS
# =====================================================

__all__: list[str] = [
    "FlextTapOracleConfigurationError",
    "FlextTapOracleConnectionError",
    "FlextTapOracleDiscoveryError",
    "FlextTapOracleError",
    "FlextTapOracleExtractionError",
    "FlextTapOracleMetadataError",
    "FlextTapOracleProcessingError",
    "FlextTapOracleQueryError",
    "FlextTapOracleStreamError",
    "FlextTapOracleValidationError",
    "create_configuration_error",
    "create_connection_error",
    "create_discovery_error",
    "create_extraction_error",
    "create_query_error",
    "create_stream_error",
    "handle_oracle_exception",
]
