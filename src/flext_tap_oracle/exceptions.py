"""Oracle tap exception hierarchy using flext-core base exceptions.

Copyright (c) 2025 FLEXT Contributors
SPDX-License-Identifier: MIT

Domain-specific exceptions for Oracle tap operations.
"""

from __future__ import annotations

# Import base exceptions that actually exist in flext-core
from flext_core import (
    FlextError,
    FlextOperationError,
    FlextValidationError,
)


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


class FlextTapOracleQueryError(FlextTapOracleError):
    """Oracle tap SQL query errors with Oracle-specific context."""

    def __init__(
        self,
        message: str = "Oracle tap query failed",
        query: str | None = None,
        oracle_error_code: str | None = None,
        **kwargs: object,
    ) -> None:
        """Initialize Oracle tap query error with Oracle-specific context."""
        context = kwargs.copy()
        if query is not None:
            context["query"] = query[:200]  # Truncate long queries
        if oracle_error_code is not None:
            context["oracle_error_code"] = oracle_error_code

        super().__init__(f"Oracle tap query: {message}", context=context)


class FlextTapOracleStreamError(FlextTapOracleError):
    """Oracle tap stream processing errors with Oracle-specific context."""

    def __init__(
        self,
        message: str = "Oracle tap stream error",
        stream_name: str | None = None,
        table_name: str | None = None,
        **kwargs: object,
    ) -> None:
        """Initialize Oracle tap stream error with Oracle-specific context."""
        context = kwargs.copy()
        if stream_name is not None:
            context["stream_name"] = stream_name
        if table_name is not None:
            context["table_name"] = table_name

        super().__init__(f"Oracle tap stream: {message}", context=context)


__all__: list[str] = [
    "FlextTapOracleConfigurationError",
    "FlextTapOracleConnectionError",
    "FlextTapOracleError",
    "FlextTapOracleProcessingError",
    "FlextTapOracleQueryError",
    "FlextTapOracleStreamError",
    "FlextTapOracleValidationError",
]
