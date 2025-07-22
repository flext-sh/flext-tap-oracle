"""FLEXT TAP ORACLE - Singer Oracle Database Extraction with simplified imports.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT

Version 0.7.0 - Singer Oracle Tap with simplified public API:
- All common imports available from root: from flext_tap_oracle import TapOracle
- Built on flext-core foundation for robust Oracle integration
- Deprecation warnings for internal imports
"""

from __future__ import annotations

import contextlib
import importlib.metadata
import warnings
from typing import Any, Never

# Foundation patterns - ALWAYS from flext-core
from flext_core import (
    BaseConfig as OracleBaseConfig,  # Configuration base
)
from flext_core import (
    DomainBaseModel as BaseModel,  # Base for Oracle models
)
from flext_core import (
    DomainError as OracleError,  # Oracle-specific errors
)
from flext_core import (
    ValidationError,  # Validation errors
)
from flext_core.domain.shared_types import ServiceResult

try:
    __version__ = importlib.metadata.version("flext-tap-oracle")
except importlib.metadata.PackageNotFoundError:
    __version__ = "0.7.0"

__version_info__ = tuple(int(x) for x in __version__.split(".") if x.isdigit())


class FlextTapOracleDeprecationWarning(DeprecationWarning):
    """Custom deprecation warning for FLEXT TAP ORACLE import changes."""


def _show_deprecation_warning(old_import: str, new_import: str) -> None:
    """Show deprecation warning for import paths."""
    message_parts = [
        f"⚠️  DEPRECATED IMPORT: {old_import}",
        f"✅ USE INSTEAD: {new_import}",
        "🔗 This will be removed in version 1.0.0",
        "📖 See FLEXT TAP ORACLE docs for migration guide",
    ]
    warnings.warn(
        "\n".join(message_parts),
        FlextTapOracleDeprecationWarning,
        stacklevel=3,
    )


# ================================
# SIMPLIFIED PUBLIC API EXPORTS
# ================================

# Foundation patterns - imported at top of file

# Singer Tap exports - conditional import with proper error handling
try:
    from flext_tap_oracle.tap import TapOracle
except ImportError as e:
    # Store error for fallback class
    import_error_msg = str(e)

    # Tap module exists but may have dependency issues - re-raise with context
    import warnings
    warnings.warn(
        f"Failed to import TapOracle: {import_error_msg}. Check Oracle dependencies in pyproject.toml",
        ImportWarning,
        stacklevel=2
    )
    # Define placeholder that fails gracefully when used
    class TapOracle:  # type: ignore[no-redef]
        def __init__(self, *_args: Any, **_kwargs: Any) -> None:
            raise ImportError(f"TapOracle is not available due to import error: {import_error_msg}")

        @classmethod
        def cli(cls) -> Never:
            raise ImportError(f"TapOracle CLI is not available due to import error: {import_error_msg}")

# Oracle Client exports - simplified imports
with contextlib.suppress(ImportError):
    from flext_tap_oracle.client import OracleClient

# Oracle Streams exports - simplified imports
with contextlib.suppress(ImportError):
    from flext_tap_oracle.streams import (
        OracleTableStream,
    )

# ================================
# PUBLIC API EXPORTS
# ================================

__all__ = [
    "BaseConfig",
    "BaseModel",  # from flext_tap_oracle import BaseModel
    "DomainBaseModel",
    # Deprecation utilities
    "FlextTapOracleDeprecationWarning",
    # Core Patterns (from flext-core)
    "OracleBaseConfig",  # from flext_tap_oracle import OracleBaseConfig
    "OracleClient",  # from flext_tap_oracle import OracleClient
    "OracleError",  # from flext_tap_oracle import OracleError
    # Oracle Streams (simplified access)
    "OracleTableStream",  # from flext_tap_oracle import OracleTableStream
    "ServiceResult",  # from flext_tap_oracle import ServiceResult
    # Main Singer Tap (simplified access)
    "TapOracle",  # from flext_tap_oracle import TapOracle
    "ValidationError",  # from flext_tap_oracle import ValidationError
    # Version
    "__version__",
    "__version_info__",
]
