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
# 🚨 ARCHITECTURAL COMPLIANCE: Using DI container
from flext_tap_oracle.infrastructure.di_container import get_service_result, get_domain_entity, get_field, get_domain_value_object, get_base_config
ServiceResult = get_service_result()
DomainEntity = get_domain_entity()
Field = get_field()
DomainValueObject = get_domain_value_object()
BaseConfig = get_base_config()
    BaseConfig as OracleBaseConfig,  # Configuration base
)
# 🚨 ARCHITECTURAL COMPLIANCE: Using DI container
from flext_tap_oracle.infrastructure.di_container import get_service_result, get_domain_entity, get_field, get_domain_value_object, get_base_config
ServiceResult = get_service_result()
DomainEntity = get_domain_entity()
Field = get_field()
DomainValueObject = get_domain_value_object()
BaseConfig = get_base_config()
    DomainBaseModel as BaseModel,  # Base for Oracle models
)
# 🚨 ARCHITECTURAL COMPLIANCE: Using DI container
from flext_tap_oracle.infrastructure.di_container import get_service_result, get_domain_entity, get_field, get_domain_value_object, get_base_config
ServiceResult = get_service_result()
DomainEntity = get_domain_entity()
Field = get_field()
DomainValueObject = get_domain_value_object()
BaseConfig = get_base_config()
    DomainError as OracleError,  # Oracle-specific errors
)
# 🚨 ARCHITECTURAL COMPLIANCE: Using DI container
from flext_tap_oracle.infrastructure.di_container import get_service_result, get_domain_entity, get_field, get_domain_value_object, get_base_config
ServiceResult = get_service_result()
DomainEntity = get_domain_entity()
Field = get_field()
DomainValueObject = get_domain_value_object()
BaseConfig = get_base_config()
    ServiceResult,
    ValidationError,  # Validation errors
)

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

# Singer Tap exports - direct import (ZERO TOLERANCE for fallbacks)
from flext_tap_oracle.tap import TapOracle

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
