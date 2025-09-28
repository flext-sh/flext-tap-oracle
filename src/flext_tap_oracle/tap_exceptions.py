"""Oracle Tap Exceptions - Comprehensive Error Handling.

Uses flext-core base exceptions with Oracle tap specific context.

Copyright (c) 2025 FLEXT Contributors
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from typing import override

from flext_core import FlextExceptions, FlextTypes

# =====================================================
# BASE ORACLE TAP EXCEPTIONS
# =====================================================


class FlextTapOracleError(FlextExceptions.Error):
    """Base error for Oracle tap operations."""


class FlextTapOracleValidationError(FlextExceptions.ValidationError):
    """Oracle tap validation errors."""


class FlextTapOracleConnectionError(FlextExceptions.ConnectionError):
    """Oracle tap connection errors."""


class FlextTapOracleConfigurationError(FlextExceptions.ConfigurationError):
    """Oracle tap configuration errors."""


class FlextTapOracleProcessingError(FlextExceptions.ProcessingError):
    """Oracle tap processing errors."""


# =====================================================
# ORACLE-SPECIFIC EXCEPTIONS WITH CONTEXT
# =====================================================


class FlextTapOracleQueryError(FlextTapOracleError):
    """Oracle tap SQL query errors with Oracle-specific context."""

    @override
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

    @override
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

    @override
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

    @override
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

    @override
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
# EXPORTS
# =====================================================

__all__: FlextTypes.Core.StringList = [
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
]
