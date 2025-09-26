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
from flext_tap_oracle.models import (
    OracleTapDiscoveryResult,
    OracleTapExecutionStats,
    OracleTapStreamInfo,
    TapOracleModels,
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
    FlextOracleTapConfig,
    FlextOracleTapConfiguration,
    # Backward compatibility aliases
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
    create_configuration_error,
    # Factory functions
    create_connection_error,
    create_discovery_error,
    create_extraction_error,
    create_query_error,
    create_stream_error,
    handle_oracle_exception,
)

# Factory functions and type aliases from tap_models
from flext_tap_oracle.tap_models import (
    TapOracleColumn,
    TapOracleSchema,
    TapOracleTable,
    TapReplicationMethod,
    create_discovery_result,
    create_stream_info_from_oracle_table,
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


__version__ = "0.9.0"
__version_info__ = tuple(int(x) for x in __version__.split(".") if x.isdigit())

__all__: FlextTapOracleTypes.Core.StringList = [
    "Config",  # Short alias to FlextOracleTapConfig
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
    # Configuration
    "FlextOracleTapConfig",
    "FlextOracleTapConfiguration",
    "FlextOracleTapService",  # Main service class
    # ===== NEW PEP8 CONSOLIDATED STRUCTURE =====
    # Main Tap Classes
    "FlextTapOracle",
    "FlextTapOracleConfigurationError",
    "FlextTapOracleConnectionError",
    "FlextTapOracleDiscoveryError",
    # Exceptions
    "FlextTapOracleError",
    "FlextTapOracleExtractionError",
    "FlextTapOracleMetadataError",
    "FlextTapOracleProcessingError",
    "FlextTapOracleQueryError",
    "FlextTapOracleStreamError",
    "FlextTapOracleValidationError",
    # Streams
    "OracleStream",
    # Models
    "OracleTapDiscoveryResult",
    "OracleTapExecutionStats",
    "OracleTapService",  # Short alias to FlextOracleTapService
    "OracleTapStreamInfo",
    "TapOracleColumn",
    # ===== BACKWARD COMPATIBILITY =====
    "TapOracleConfig",
    "TapOracleModels",  # Unified models collection
    "TapOracleSchema",
    "TapOracleTable",
    "TapReplicationMethod",
    "__version__",
    "__version_info__",
    "create_configuration_error",
    "create_connection_error",
    "create_discovery_error",
    "create_discovery_result",
    "create_extraction_error",
    "create_oracle_discovery_service",
    "create_oracle_stream",
    "create_oracle_stream_from_table",
    "create_oracle_tap_config",
    "create_oracle_tap_service",
    "create_query_error",
    "create_stream_error",
    "create_stream_info_from_oracle_table",
    "handle_oracle_exception",
]

# Note: FlextOracleTapBaseService is conditionally imported above but not exported in __all__
# to avoid type checking issues when not available
