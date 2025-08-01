"""Oracle tap exception hierarchy using flext-core DRY patterns.

Copyright (c) 2025 FLEXT Contributors
SPDX-License-Identifier: MIT

Domain-specific exceptions for Oracle tap operations using factory pattern to eliminate duplication.
"""

from __future__ import annotations

from typing import TYPE_CHECKING

from flext_core.exceptions import create_module_exception_classes

if TYPE_CHECKING:
    # For type checking, import the actual base types
    from flext_core.exceptions import (
        FlextAuthenticationError as FlextTapOracleAuthenticationError,
        FlextConfigurationError as FlextTapOracleConfigurationError,
        FlextConnectionError as FlextTapOracleConnectionError,
        FlextError as FlextTapOracleError,
        FlextProcessingError as FlextTapOracleProcessingError,
        FlextTimeoutError as FlextTapOracleTimeoutError,
        FlextValidationError as FlextTapOracleValidationError,
    )
else:
    # Create all standard exception classes using factory pattern - eliminates 150+ lines of duplication
    oracle_exceptions = create_module_exception_classes("flext_tap_oracle")

    # Import generated classes for clean usage
    FlextTapOracleError = oracle_exceptions["FlextTapOracleError"]
    FlextTapOracleValidationError = oracle_exceptions["FlextTapOracleValidationError"]
    FlextTapOracleConfigurationError = oracle_exceptions["FlextTapOracleConfigurationError"]
    FlextTapOracleConnectionError = oracle_exceptions["FlextTapOracleConnectionError"]
    FlextTapOracleProcessingError = oracle_exceptions["FlextTapOracleProcessingError"]
    FlextTapOracleAuthenticationError = oracle_exceptions["FlextTapOracleAuthenticationError"]
    FlextTapOracleTimeoutError = oracle_exceptions["FlextTapOracleTimeoutError"]


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
