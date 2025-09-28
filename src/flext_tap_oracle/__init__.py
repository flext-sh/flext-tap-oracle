"""FLEXT Tap Oracle - Oracle Database Singer Tap for FLEXT ecosystem.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

# Re-export flext-db-oracle infrastructure that this tap uses extensively
from flext_db_oracle import (
    # Core Oracle database functionality
    FlextDbOracleApi,
    FlextDbOracleConfig,
    # Note: "Column", QueryResult, Schema, Table are accessible via FlextDbOracleModels
)

# === FLEXT-MELTANO INTEGRATION ===
# Import only what exists and is actually used
from flext_meltano import (
    FlextMeltanoBridge,
    FlextMeltanoConfig,
)

# Models - Data models and types
# Models - Unified models collection
# Additional model imports from models for backward compatibility
# Factory functions and type aliases from consolidated models
from flext_tap_oracle.models import (
    FlextTapOracleModels,
    FlextTapOracleModels as TapModels,  # alias for compatibility
    FlextTapOracleUtilities,
    TapOracleColumn,
    TapOracleSchema,
    TapOracleTable,
    TapReplicationMethod,
)

# Client - Main tap implementation with domain services
from flext_tap_oracle.tap_client import (
    FlextOracleConnectionTestService,
    FlextOracleDiscoveryService,
    FlextOracleTableFilterService,
    # Backward compatibility aliases
    FlextOracleTapClient,
    FlextOracleTapService,
    OracleTapService,
    create_oracle_discovery_service,
    create_oracle_tap_service,
)

# =====================================================
# NEW PEP8 CONSOLIDATED STRUCTURE - PRIMARY IMPORTS
# =====================================================
# Configuration - Comprehensive configuration management
from flext_tap_oracle.tap_config import (
    Config,
    # Backward compatibility aliases
    FlextOracleTapConfig,
    FlextOracleTapConfiguration,
    FlextTapOracleConfig,
    TapOracleConfig,
    create_oracle_tap_config,
)

# Exceptions - Comprehensive error handling
from flext_tap_oracle.tap_exceptions import (
    FlextTapOracleConfigurationError,
    FlextTapOracleConnectionError,
    FlextTapOracleDiscoveryError,
    FlextTapOracleError,
    FlextTapOracleExtractionError,
    FlextTapOracleMetadataError,
    FlextTapOracleProcessingError,
    FlextTapOracleQueryError,
    FlextTapOracleStreamError,
    FlextTapOracleValidationError,
)

# Streams - Oracle stream definitions and processing
from flext_tap_oracle.tap_streams import (
    # Backward compatibility
    FlextOracleStream,
    OracleStream,
    create_oracle_stream,
    create_oracle_stream_from_table,
)

# Core FLEXT imports
from flext_tap_oracle.typings import FlextTapOracleTypes

# Main alias for external usage
FlextTapOracle = FlextOracleTapService

# Ultra-simple aliases for test compatibility
FlextOracleTapBaseService = FlextOracleTapService

# Streams - Oracle stream definitions and processing
# Models - Data models and types

# Exceptions - Comprehensive error handling

# Factory functions and type aliases from tap_models

# =====================================================
# BACKWARD COMPATIBILITY - OLD IMPORTS STILL WORK
# =====================================================

# Legacy imports moved to _legacy/ directory for backward compatibility
_LEGACY_IMPORTS_AVAILABLE = False  # Simplified for type checking

# TEMPORARY FACADE for compatibility during refactoring (will be removed)
_LEGACY_FACADE_AVAILABLE = False  # Simplified for type checking

__all__ = [
    "Config",  # Short alias to FlextTapOracleConfig
    # Infrastructure from flext-db-oracle
    "FlextDbOracleApi",
    "FlextDbOracleConfig",
    # Meltano infrastructure
    "FlextMeltanoBridge",
    "FlextMeltanoConfig",
    # Client & Services
    "FlextOracleConnectionTestService",
    "FlextOracleDiscoveryService",
    "FlextOracleStream",
    "FlextOracleTableFilterService",
    "FlextOracleTapBaseService",  # Ultra-simple alias for test compatibility
    "FlextOracleTapClient",
    "FlextOracleTapConfig",  # Legacy alias
    "FlextOracleTapConfiguration",
    "FlextOracleTapService",  # Main service class
    # ===== NEW PEP8 CONSOLIDATED STRUCTURE =====
    # Main Tap Classes
    "FlextTapOracle",
    # Configuration
    "FlextTapOracleConfig",
    "FlextTapOracleConfigurationError",
    "FlextTapOracleConnectionError",
    "FlextTapOracleDiscoveryError",
    # Exceptions
    "FlextTapOracleError",
    "FlextTapOracleExtractionError",
    "FlextTapOracleMetadataError",
    "FlextTapOracleModels",  # Standardized [Project]Models pattern
    "FlextTapOracleProcessingError",
    "FlextTapOracleQueryError",
    "FlextTapOracleStreamError",
    "FlextTapOracleTypes",
    "FlextTapOracleUtilities",  # Standardized [Project]Utilities pattern
    "FlextTapOracleValidationError",
    # Streams
    "OracleStream",
    # Models - Access via FlextTapOracleModels.ClassName
    "OracleTapService",  # Short alias to FlextOracleTapService
    "TapModels",  # Backward compatibility alias
    "TapOracleColumn",
    # ===== BACKWARD COMPATIBILITY =====
    "TapOracleConfig",
    "TapOracleSchema",
    "TapOracleTable",
    "TapReplicationMethod",
    "create_oracle_discovery_service",
    "create_oracle_stream",
    "create_oracle_stream_from_table",
    "create_oracle_tap_config",
    "create_oracle_tap_service",
]

# Note: FlextOracleTapBaseService is conditionally imported above but not exported in __all__
# to avoid type checking issues when not available
