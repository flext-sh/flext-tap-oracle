"""Oracle tap exception hierarchy using flext-core patterns.

Copyright (c) 2025 FLEXT Contributors
SPDX-License-Identifier: MIT

Domain-specific exceptions for Oracle tap operations inheriting from flext-core.
"""

from __future__ import annotations

from flext_core.exceptions import (
    FlextAuthenticationError,
    FlextConfigurationError,
    FlextConnectionError,
    FlextError,
    FlextProcessingError,
    FlextTimeoutError,
    FlextValidationError,
)


class FlextTapOracleError(FlextError):
    """Base exception for Oracle tap operations."""

    def __init__(
        self,
        message: str = "Oracle tap error",
        database_name: str | None = None,
        **kwargs: object,
    ) -> None:
        """Initialize Oracle tap error with context."""
        context = kwargs.copy()
        if database_name is not None:
            context["database_name"] = database_name

        super().__init__(message, error_code="ORACLE_TAP_ERROR", context=context)


class FlextTapOracleConnectionError(FlextConnectionError):
    """Oracle tap connection errors."""

    def __init__(
        self,
        message: str = "Oracle tap connection failed",
        host: str | None = None,
        port: int | None = None,
        service_name: str | None = None,
        **kwargs: object,
    ) -> None:
        """Initialize Oracle tap connection error with context."""
        context = kwargs.copy()
        if host is not None:
            context["host"] = host
        if port is not None:
            context["port"] = port
        if service_name is not None:
            context["service_name"] = service_name

        super().__init__(f"Oracle tap connection: {message}", **context)


class FlextTapOracleAuthenticationError(FlextAuthenticationError):
    """Oracle tap authentication errors."""

    def __init__(
        self,
        message: str = "Oracle tap authentication failed",
        username: str | None = None,
        **kwargs: object,
    ) -> None:
        """Initialize Oracle tap authentication error with context."""
        context = kwargs.copy()
        if username is not None:
            context["username"] = username

        super().__init__(f"Oracle tap auth: {message}", **context)


class FlextTapOracleValidationError(FlextValidationError):
    """Oracle tap validation errors."""

    def __init__(
        self,
        message: str = "Oracle tap validation failed",
        field: str | None = None,
        value: object = None,
        table_name: str | None = None,
        **kwargs: object,
    ) -> None:
        """Initialize Oracle tap validation error with context."""
        validation_details: dict[str, object] = {}
        if field is not None:
            validation_details["field"] = field
        if value is not None:
            validation_details["value"] = str(value)[:100]  # Truncate long values

        context = kwargs.copy()
        if table_name is not None:
            context["table_name"] = table_name

        super().__init__(
            f"Oracle tap validation: {message}",
            validation_details=validation_details,
            context=context,
        )


class FlextTapOracleConfigurationError(FlextConfigurationError):
    """Oracle tap configuration errors."""

    def __init__(
        self,
        message: str = "Oracle tap configuration error",
        config_key: str | None = None,
        **kwargs: object,
    ) -> None:
        """Initialize Oracle tap configuration error with context."""
        context = kwargs.copy()
        if config_key is not None:
            context["config_key"] = config_key

        super().__init__(f"Oracle tap config: {message}", **context)


class FlextTapOracleProcessingError(FlextProcessingError):
    """Oracle tap processing errors."""

    def __init__(
        self,
        message: str = "Oracle tap processing failed",
        table_name: str | None = None,
        record_number: int | None = None,
        **kwargs: object,
    ) -> None:
        """Initialize Oracle tap processing error with context."""
        context = kwargs.copy()
        if table_name is not None:
            context["table_name"] = table_name
        if record_number is not None:
            context["record_number"] = record_number

        super().__init__(f"Oracle tap processing: {message}", **context)


class FlextTapOracleQueryError(FlextTapOracleError):
    """Oracle tap SQL query errors."""

    def __init__(
        self,
        message: str = "Oracle tap query failed",
        query: str | None = None,
        oracle_error_code: str | None = None,
        **kwargs: object,
    ) -> None:
        """Initialize Oracle tap query error with context."""
        context = kwargs.copy()
        if query is not None:
            context["query"] = query[:200]  # Truncate long queries
        if oracle_error_code is not None:
            context["oracle_error_code"] = oracle_error_code

        super().__init__(f"Oracle tap query: {message}", context=context)


class FlextTapOracleTimeoutError(FlextTimeoutError):
    """Oracle tap timeout errors."""

    def __init__(
        self,
        message: str = "Oracle tap operation timed out",
        operation: str | None = None,
        timeout_seconds: float | None = None,
        **kwargs: object,
    ) -> None:
        """Initialize Oracle tap timeout error with context."""
        context = kwargs.copy()
        if operation is not None:
            context["operation"] = operation
        if timeout_seconds is not None:
            context["timeout_seconds"] = timeout_seconds

        super().__init__(f"Oracle tap timeout: {message}", **context)


class FlextTapOracleStreamError(FlextTapOracleError):
    """Oracle tap stream processing errors."""

    def __init__(
        self,
        message: str = "Oracle tap stream error",
        stream_name: str | None = None,
        table_name: str | None = None,
        **kwargs: object,
    ) -> None:
        """Initialize Oracle tap stream error with context."""
        context = kwargs.copy()
        if stream_name is not None:
            context["stream_name"] = stream_name
        if table_name is not None:
            context["table_name"] = table_name

        super().__init__(f"Oracle tap stream: {message}", context=context)


__all__ = [
    "FlextTapOracleAuthenticationError",
    "FlextTapOracleConfigurationError",
    "FlextTapOracleConnectionError",
    "FlextTapOracleError",
    "FlextTapOracleProcessingError",
    "FlextTapOracleQueryError",
    "FlextTapOracleStreamError",
    "FlextTapOracleTimeoutError",
    "FlextTapOracleValidationError",
]
