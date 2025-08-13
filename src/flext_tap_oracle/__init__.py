"""FLEXT Tap Oracle - Oracle Database Singer Tap for FLEXT ecosystem.

This module implements a comprehensive Oracle Database Singer tap for data extraction
within the FLEXT ecosystem, following Singer specification and Clean Architecture
principles. The tap provides reliable, high-performance data extraction from Oracle
databases with comprehensive schema discovery and change data capture support.

The implementation leverages flext-meltano for Singer framework integration and
flext-db-oracle for Oracle-specific database operations, avoiding code duplication
and ensuring consistency across the FLEXT ecosystem.

Architecture (Clean Architecture + Singer Patterns):
    - Tap Layer: Singer tap implementation with stream discovery and extraction
    - Application Layer: Data extraction services and stream processing
    - Domain Layer: Oracle-specific data models and business rules
    - Infrastructure Layer: Database connectivity via flext-db-oracle

Module Organization (PEP8 Compliant):
    - tap_config.py: Configuration management and connection settings
    - tap_client.py: Main tap client implementation with stream processing
    - tap_streams.py: Oracle stream definitions, discovery, and data extraction
    - tap_models.py: Data models and schemas specific to Oracle tap operations
    - tap_exceptions.py: Comprehensive error handling for tap operations

Key Features:
    - Singer Specification Compliance: Full adherence to Singer tap standards
    - Schema Discovery: Automatic Oracle schema introspection and catalog generation
    - Incremental Extraction: Support for incremental data extraction with bookmarks
    - Change Data Capture: Oracle-specific CDC support with LogMiner integration
    - Performance Optimization: Bulk operations and Oracle-specific query optimization
    - Type Safety: Strong typing with proper Oracle data type mapping
    - Error Handling: Comprehensive error handling with FlextResult patterns
    - Connection Pooling: Efficient database connection management
    - Monitoring: Built-in metrics and observability for extraction operations

Oracle-Specific Features:
    - Advanced Data Types: Support for Oracle-specific types (CLOB, BLOB, XMLType, etc.)
    - Partition Awareness: Optimized extraction from partitioned tables
    - RAC Support: Oracle Real Application Clusters compatibility
    - Flashback Query: Point-in-time data extraction capabilities
    - PL/SQL Integration: Support for stored procedures and functions

Example:
    Basic Oracle tap configuration and execution:

    >>> from flext_tap_oracle import FlextTapOracleClient
    >>> from flext_core import FlextResult
    >>>
    >>> # Configure tap with Oracle connection
    >>> config = {
    ...     "host": "oracle.example.com",
    ...     "port": 1521,
    ...     "service_name": "ORCL",
    ...     "username": "tap_user",
    ...     "password": "secure_password",
    ...     "default_replication_method": "INCREMENTAL",
    ... }
    >>>
    >>> # Initialize and run tap
    >>> tap = FlextTapOracleClient(config)
    >>> catalog_result = tap.discover_catalog()
    >>> if catalog_result.is_success:
    ...     catalog = catalog_result.data
    ...     print(f"Discovered {len(catalog.streams)} streams")

    Stream-specific extraction:

    >>> # Extract data from specific table
    >>> extraction_result = tap.extract_stream(
    ...     "employees", bookmark={"updated_at": "2025-01-01"}
    ... )
    >>> if extraction_result.is_success:
    ...     records = extraction_result.data
    ...     print(f"Extracted {len(records)} records")

FLEXT Ecosystem Integration:
    This tap integrates seamlessly with flext-meltano for Singer orchestration,
    flext-db-oracle for database operations, and flext-core for consistent error
    handling and service management patterns.

Copyright (c) 2025 FLEXT Contributors
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
from flext_tap_oracle.models import (
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
__version_info__ = tuple(int(x) for x in __version__.split(".") if x.isdigit())

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
    "__version_info__",
]

# Note: FlextOracleTapBaseService is conditionally imported above but not exported in __all__
# to avoid type checking issues when not available
