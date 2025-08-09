"""FLEXT Tap Oracle - Oracle Database Singer Tap Implementation.

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

# Import Oracle tap implementations using COMPOSITION + domain services
from flext_tap_oracle.base_service import FlextOracleTapService, create_oracle_tap_service
from flext_tap_oracle.domain_services import (
    FlextOracleConnectionTestService,
    FlextOracleDiscoveryService,
    FlextOracleTableFilterService,
)
# TEMPORARY FACADE for compatibility during refactoring
from flext_tap_oracle.legacy_facade import FlextOracleTapBaseService
from flext_tap_oracle.config import FlextOracleTapConfig, TapOracleConfig, create_oracle_tap_config
from flext_tap_oracle.oracle_stream import OracleStream

# REFATORAÇÃO COMPLETA: Usando COMPOSIÇÃO + Domain Services
# - FlextOracleTapService (composição, não herança)
# - Domain Services (FlextDomainService[T] from flext-core)

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
    # Oracle Tap implementations - COMPOSITION + DOMAIN SERVICES
    "FlextOracleConnectionTestService",
    "FlextOracleDiscoveryService",
    "FlextOracleTapService",
    "FlextOracleTapBaseService",  # TEMPORARY FACADE - TO BE REMOVED
    "FlextOracleTapConfig",
    "FlextOracleTableFilterService",
    "OracleStream",
    "TapOracleConfig",  # Backward compatibility alias
    # Factory functions
    "create_data_validation_plugin",
    "create_meltano_tap_service",
    "create_oracle_tap_config",
    "create_oracle_tap_service",
    "create_performance_monitor_plugin",
    "create_security_audit_plugin",
    "get_tap_test_class",
    "register_all_oracle_plugins",
    # Utilities
    "singer_typing",
    "th",
    "__version__",
]
