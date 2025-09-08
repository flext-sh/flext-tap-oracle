"""Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT.
"""

from __future__ import annotations
from flext_core import FlextTypes


"""FLEXT Tap Oracle - Oracle Database Singer Tap for FLEXT ecosystem."""
"""
Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""


# Re-export flext-db-oracle infrastructure that this tap uses extensively
from flext_db_oracle import (
    # Core Oracle database functionality
    FlextDbOracleApi,
    FlextDbOracleClient,
    FlextDbOracleConfig,
    FlextDbOracleConstants,
    FlextDbOracleExceptions,
    FlextDbOracleModels,
    FlextDbOracleServices,
    FlextDbOracleUtilities,
    # Note: Column, QueryResult, Schema, Table are accessible via FlextDbOracleModels
)

# === FLEXT-MELTANO INTEGRATION ===
# Import only what exists and is actually used
from flext_meltano import (
    FlextMeltanoBridge,
    FlextMeltanoConfig,
)

# =====================================================
# NEW PEP8 CONSOLIDATED STRUCTURE - PRIMARY IMPORTS
# =====================================================

# Configuration - Comprehensive configuration management
from flext_tap_oracle.tap_config import (
    FlextOracleTapConfig,
    FlextOracleTapConfiguration,
    FlextOracleTapStreamMetadata,
    create_oracle_tap_config,
    # Backward compatibility aliases
    TapOracleConfig,
    Config,
)

# Client - Main tap implementation with domain services
from flext_tap_oracle.tap_client import (
    FlextOracleTapService,
    FlextOracleConnectionTestService,
    FlextOracleDiscoveryService,
    FlextOracleTableFilterService,
    create_oracle_tap_service,
    create_oracle_discovery_service,
    # Backward compatibility aliases
    FlextOracleTapClient,
    OracleTapService,
)

# Main alias for external usage
FlextTapOracle = FlextOracleTapService

# Streams - Oracle stream definitions and processing
from flext_tap_oracle.tap_streams import (
    OracleStream,
    create_oracle_stream,
    create_oracle_stream_from_table,
    # Backward compatibility
    FlextOracleStream,
)

# Models - Data models and types
from flext_tap_oracle.models import (
    OracleTapDiscoveryResult,
    OracleTapExecutionStats,
    OracleTapStreamInfo,
)

# Factory functions and type aliases from tap_models
from flext_tap_oracle.tap_models import (
    create_discovery_result,
    create_stream_info_from_oracle_table,
    # Type aliases for backward compatibility
    TapOracleTable,
    TapOracleColumn,
    TapOracleSchema,
    TapReplicationMethod,
)

# Exceptions - Comprehensive error handling
from flext_tap_oracle.tap_exceptions import (
    FlextTapOracleError,
    FlextTapOracleValidationError,
    FlextTapOracleConnectionError,
    FlextTapOracleConfigurationError,
    FlextTapOracleProcessingError,
    FlextTapOracleQueryError,
    FlextTapOracleStreamError,
    FlextTapOracleDiscoveryError,
    FlextTapOracleMetadataError,
    FlextTapOracleExtractionError,
    # Factory functions
    create_connection_error,
    create_query_error,
    create_stream_error,
    create_discovery_error,
    create_configuration_error,
    create_extraction_error,
    handle_oracle_exception,
)

# =====================================================
# BACKWARD COMPATIBILITY - OLD IMPORTS STILL WORK
# =====================================================

# Legacy imports moved to _legacy/ directory for backward compatibility
_LEGACY_IMPORTS_AVAILABLE = False  # Simplified for type checking

# TEMPORARY FACADE for compatibility during refactoring (will be removed)
_LEGACY_FACADE_AVAILABLE = False  # Simplified for type checking


__version__ = "0.9.0"
__version_info__ = tuple(int(x) for x in __version__.split(".") if x.isdigit())

__all__: FlextTypes.Core.StringList = [
    # Infrastructure from flext-db-oracle
    "FlextDbOracleApi",
    "FlextDbOracleColumn",
    "FlextDbOracleConfig",
    "FlextDbOracleConnection",
    "FlextDbOracleMetadataManager",
    "FlextDbOracleObservabilityManager",
    "FlextDbOracleOperationTracker",
    "FlextDbOracleSchema",
    "FlextDbOracleTable",
    "FlextDbOracleQueryResult",
    # Meltano infrastructure
    "FlextMeltanoBridge",
    "FlextMeltanoConfig",
    # ===== NEW PEP8 CONSOLIDATED STRUCTURE =====
    # Main Tap Classes
    "FlextTapOracle",  # Alias for FlextOracleTapService
    "FlextOracleTapService",  # Main service class
    # Configuration
    "FlextOracleTapConfig",
    "FlextOracleTapConfiguration",
    "FlextOracleTapStreamMetadata",
    "create_oracle_tap_config",
    # Client & Services
    "FlextOracleConnectionTestService",
    "FlextOracleDiscoveryService",
    "FlextOracleTableFilterService",
    "create_oracle_tap_service",
    "create_oracle_discovery_service",
    # Streams
    "OracleStream",
    "create_oracle_stream",
    "create_oracle_stream_from_table",
    # Models
    "OracleTapDiscoveryResult",
    "OracleTapExecutionStats",
    "OracleTapStreamInfo",
    "create_discovery_result",
    "create_stream_info_from_oracle_table",
    # Exceptions
    "FlextTapOracleError",
    "FlextTapOracleValidationError",
    "FlextTapOracleConnectionError",
    "FlextTapOracleConfigurationError",
    "FlextTapOracleProcessingError",
    "FlextTapOracleQueryError",
    "FlextTapOracleStreamError",
    "FlextTapOracleDiscoveryError",
    "FlextTapOracleMetadataError",
    "FlextTapOracleExtractionError",
    "create_connection_error",
    "create_query_error",
    "create_stream_error",
    "create_discovery_error",
    "create_configuration_error",
    "create_extraction_error",
    "handle_oracle_exception",
    # ===== BACKWARD COMPATIBILITY =====
    "TapOracleConfig",  # Alias to FlextOracleTapConfig
    "Config",  # Short alias to FlextOracleTapConfig
    "FlextOracleTapClient",  # Alias to FlextOracleTapService
    "OracleTapService",  # Short alias to FlextOracleTapService
    "FlextOracleStream",  # Alias to OracleStream
    "TapOracleTable",  # Type alias
    "TapOracleColumn",  # Type alias
    "TapOracleSchema",  # Type alias
    "TapReplicationMethod",  # Type alias
    "__version__",
    "__version_info__",
]

# Note: FlextOracleTapBaseService is conditionally imported above but not exported in __all__
# to avoid type checking issues when not available
