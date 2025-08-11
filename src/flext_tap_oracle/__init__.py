"""FLEXT Tap Oracle - Oracle Database Singer Tap Implementation.

PEP8 CONSOLIDATED STRUCTURE: This module provides backward compatibility while
exposing the new PEP8 consolidated structure. All functionality is now organized
in descriptive modules following FLEXT ecosystem patterns.

NEW STRUCTURE:
- tap_config.py: Complete configuration management
- tap_client.py: Tap client implementation with domain services
- tap_streams.py: Oracle stream definitions and processing
- tap_models.py: Data models specific to Oracle tap
- tap_exceptions.py: Comprehensive error handling

This project implements Oracle Database specific logic using generic flext-meltano interfaces
and flext-db-oracle for database connectivity. No implementation should be duplicated from
other FLEXT projects.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

# Re-export flext-db-oracle infrastructure that this tap uses extensively
from flext_db_oracle import (
    # Oracle plugins for extensibility
    ORACLE_PLUGINS,
    # Core Oracle database functionality
    FlextDbOracleApi,
    # Comprehensive metadata management (USED INSTEAD OF CUSTOM IMPLEMENTATIONS)
    FlextDbOracleColumn,
    FlextDbOracleConfig,
    FlextDbOracleConnection,
    # Advanced observability and monitoring (USED INSTEAD OF CUSTOM MONITORING)
    FlextDbOracleErrorHandler,
    FlextDbOracleMetadataManager,
    FlextDbOracleObservabilityManager,
    FlextDbOracleOperationTracker,
    FlextDbOracleSchema,
    FlextDbOracleTable,
    # Oracle-specific types and constants
    TDbOracleColumn,
    TDbOracleConnectionStatus,
    TDbOracleQueryResult,
    TDbOracleSchema,
    TDbOracleTable,
    create_data_validation_plugin,
    create_performance_monitor_plugin,
    create_security_audit_plugin,
    register_all_oracle_plugins,
)

# === FLEXT-MELTANO COMPLETE INTEGRATION ===
# Re-export ALL flext-meltano facilities for full ecosystem integration
# Import singer_typing as th for backward compatibility
from flext_meltano import (
    BatchSink,
    FlextMeltanoBaseService,
    # Bridge integration
    FlextMeltanoBridge,
    # Configuration and validation
    FlextMeltanoConfig,
    # Enterprise services from flext-meltano.base
    FlextMeltanoTapService,
    # Authentication patterns
    OAuthAuthenticator,
    # Typing definitions
    PropertiesList,
    Property,
    Sink,
    SQLSink,
    # Core Singer SDK classes (centralized from flext-meltano)
    Stream,
    Tap,
    Target,
    create_meltano_tap_service,
    # Testing utilities
    get_tap_test_class,
    # Singer typing utilities (centralized)
    singer_typing,
    singer_typing as th,
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

# Streams - Oracle stream definitions and processing
from flext_tap_oracle.tap_streams import (
    OracleStream,
    create_oracle_stream,
    create_oracle_stream_from_table,
    # Backward compatibility
    FlextOracleStream,
)

# Models - Data models and types
from flext_tap_oracle.tap_models import (
    OracleTapDiscoveryResult,
    OracleTapExecutionStats,
    OracleTapStreamInfo,
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

__all__: list[str] = [
    # Infrastructure from flext-db-oracle
    "ORACLE_PLUGINS",
    "FlextDbOracleApi",
    "FlextDbOracleColumn",
    "FlextDbOracleConfig",
    "FlextDbOracleConnection",
    "FlextDbOracleErrorHandler",
    "FlextDbOracleMetadataManager",
    "FlextDbOracleObservabilityManager",
    "FlextDbOracleOperationTracker",
    "FlextDbOracleSchema",
    "FlextDbOracleTable",
    # Types from flext-db-oracle
    "TDbOracleColumn",
    "TDbOracleConnectionStatus",
    "TDbOracleQueryResult",
    "TDbOracleSchema",
    "TDbOracleTable",
    # Meltano infrastructure
    "BatchSink",
    "FlextMeltanoBaseService",
    "FlextMeltanoBridge",
    "FlextMeltanoConfig",
    "FlextMeltanoTapService",
    "OAuthAuthenticator",
    "PropertiesList",
    "Property",
    "Sink",
    "SQLSink",
    "Stream",
    "Tap",
    "Target",
    # ===== NEW PEP8 CONSOLIDATED STRUCTURE =====
    # Configuration
    "FlextOracleTapConfig",
    "FlextOracleTapConfiguration",
    "FlextOracleTapStreamMetadata",
    "create_oracle_tap_config",
    # Client & Services
    "FlextOracleTapService",
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
    # Factory functions from flext-db-oracle
    "create_data_validation_plugin",
    "create_performance_monitor_plugin",
    "create_security_audit_plugin",
    "register_all_oracle_plugins",
    # Factory functions from flext-meltano
    "create_meltano_tap_service",
    "get_tap_test_class",
    # Utilities
    "singer_typing",
    "th",
    "__version__",
]

# Note: FlextOracleTapBaseService is conditionally imported above but not exported in __all__
# to avoid type checking issues when not available
