"""Oracle Tap Client - Complete Tap Implementation with Domain Services.

PEP8 CONSOLIDATION: All Oracle tap client logic consolidated into one module.
This module consolidates base_service.py + domain_services.py following the
established FLEXT pattern for comprehensive tap implementation.

COMPOSITION using FlextMeltanoTapService + Domain Services pattern from flext-core.

Copyright (c) 2025 FLEXT Contributors
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from typing import TYPE_CHECKING

# Import CORRECT base service from flext-meltano + logger + FlextResult from flext-core
from flext_core import FlextDomainService, FlextResult, get_logger

# Import Oracle infrastructure - NEVER duplicate
from flext_db_oracle import (
    FlextDbOracleApi,
    FlextDbOracleMetadataManager,
    FlextDbOracleTable,
)
from flext_meltano import FlextMeltanoTapService

logger = get_logger(__name__)

if TYPE_CHECKING:
    from flext_tap_oracle.tap_config import FlextOracleTapConfig


# =====================================================
# DOMAIN SERVICES - Using FlextDomainService[T] pattern
# =====================================================


class FlextOracleDiscoveryService(FlextDomainService[list[FlextDbOracleTable]]):
    """Oracle table discovery domain service using FlextDomainService[T]."""

    oracle_api: FlextDbOracleApi
    schema_name: str | None = None

    def execute(self) -> FlextResult[list[FlextDbOracleTable]]:
        """Execute Oracle table discovery using flext-db-oracle infrastructure."""
        try:
            schema_name = self.schema_name or "USER"  # Default Oracle schema
            logger.info("Discovering Oracle tables in schema: %s", schema_name)

            # Get metadata manager from oracle_api
            connection = self.oracle_api.connection
            if connection is None:
                return FlextResult.fail("No Oracle connection available")

            metadata_manager = FlextDbOracleMetadataManager(connection)
            schema_result = metadata_manager.get_schema_metadata(schema_name)

            if schema_result.success and schema_result.data:
                tables = schema_result.data.tables
                logger.info("Discovered %d Oracle tables", len(tables))
                return FlextResult.ok(tables)

            error_msg = schema_result.error or "No tables found"
            logger.warning("Oracle table discovery failed: %s", error_msg)
            return FlextResult.fail(f"Table discovery failed: {error_msg}")

        except Exception as e:
            logger.exception("Oracle table discovery error")
            return FlextResult.fail(f"Table discovery error: {e}")


class FlextOracleConnectionTestService(FlextDomainService[bool]):
    """Oracle connection test domain service using FlextDomainService[T]."""

    oracle_api: FlextDbOracleApi

    def execute(self) -> FlextResult[bool]:
        """Execute Oracle connection test using flext-db-oracle infrastructure."""
        try:
            logger.info("Testing Oracle connection")

            # Use existing flext-db-oracle API
            connection_result = self.oracle_api.test_connection()

            if hasattr(connection_result, "success") and connection_result.success:
                logger.info("Oracle connection test successful")
                success = True
                return FlextResult.ok(success)

            error_msg = getattr(connection_result, "error", "Connection failed")
            logger.error("Oracle connection test failed: %s", error_msg)
            return FlextResult.fail(str(error_msg))

        except Exception as e:
            logger.exception("Oracle connection test error")
            return FlextResult.fail(f"Connection test error: {e}")


class FlextOracleTableFilterService(FlextDomainService[list[str]]):
    """Oracle table filtering domain service using FlextDomainService[T]."""

    tap_config: FlextOracleTapConfig
    discovery_service: FlextOracleDiscoveryService

    def execute(self) -> FlextResult[list[str]]:
        """Execute table filtering based on tap configuration."""
        try:
            tap_configuration = self.tap_config.get_tap_config()

            # If specific tables are configured, use them
            if tap_configuration.tables_filter:
                logger.info(
                    "Using configured table filter: %s",
                    tap_configuration.tables_filter,
                )
                return FlextResult.ok(list(tap_configuration.tables_filter))

            # Otherwise discover all tables and apply exclusions
            tables_result = self.discovery_service.execute()
            if tables_result.is_failure:
                error_msg = tables_result.error or "Unknown discovery error"
                return FlextResult.fail(error_msg)

            if tables_result.data is None:
                return FlextResult.fail("No table data returned")

            table_names = [table.name for table in tables_result.data]

            # Apply exclusions
            if tap_configuration.exclude_tables:
                excluded = set(tap_configuration.exclude_tables)
                table_names = [name for name in table_names if name not in excluded]
                logger.info("Applied exclusions, %d tables remaining", len(table_names))

            return FlextResult.ok(table_names)

        except Exception as e:
            logger.exception("Table filtering error")
            return FlextResult.fail(f"Table filtering error: {e}")


# =====================================================
# MAIN TAP SERVICE - Using COMPOSITION pattern
# =====================================================


class FlextOracleTapService:
    """Oracle Tap Service using COMPOSITION with FlextMeltanoTapService + Domain Services.

    Esta classe usa COMPOSIÇÃO ao invés de herança:
    - FlextMeltanoTapService para funcionalidade base Singer/Meltano
    - Domain Services (FlextDomainService[T]) para lógica Oracle

    SOLID Principles:
    - Single Responsibility: Cada domain service tem uma responsabilidade
    - Open/Closed: Extensível via novos domain services
    - Liskov Substitution: Domain services são intercambiáveis
    - Interface Segregation: Interfaces específicas por domain service
    - Dependency Inversion: Depends on abstractions (FlextDomainService[T])
    """

    def __init__(self, config: FlextOracleTapConfig) -> None:
        """Initialize Oracle tap service using COMPOSITION pattern."""
        self._config = config

        # COMPOSITION: Use FlextMeltanoTapService for base functionality
        self._meltano_service = FlextMeltanoTapService(config)

        # COMPOSITION: Create Oracle API
        oracle_config = self._config.get_oracle_config()
        self._oracle_api = FlextDbOracleApi(oracle_config)

        # COMPOSITION: Create domain services (FlextDomainService[T])
        # Get schema name from service name or use default
        schema_name = (
            getattr(oracle_config, "schema_name", None) or oracle_config.service_name
        )
        self._discovery_service = FlextOracleDiscoveryService(
            oracle_api=self._oracle_api,
            schema_name=schema_name,
        )
        self._connection_test_service = FlextOracleConnectionTestService(
            oracle_api=self._oracle_api,
        )
        self._table_filter_service = FlextOracleTableFilterService(
            tap_config=self._config,
            discovery_service=self._discovery_service,
        )

    @property
    def config(self) -> FlextOracleTapConfig:
        """Get Oracle tap configuration."""
        return self._config

    @property
    def oracle_api(self) -> FlextDbOracleApi:
        """Get Oracle API."""
        return self._oracle_api

    @property
    def discovery_service(self) -> FlextOracleDiscoveryService:
        """Get Oracle discovery domain service."""
        return self._discovery_service

    @property
    def connection_test_service(self) -> FlextOracleConnectionTestService:
        """Get Oracle connection test domain service."""
        return self._connection_test_service

    @property
    def table_filter_service(self) -> FlextOracleTableFilterService:
        """Get Oracle table filter domain service."""
        return self._table_filter_service

    # DELEGATION: Delegate base functionality to FlextMeltanoTapService
    def validate_service(self) -> FlextResult[bool]:
        """Validate service using base FlextMeltanoTapService."""
        return self._meltano_service.validate_service()

    def get_health_status(self) -> FlextResult[dict[str, object]]:
        """Get health status using base FlextMeltanoTapService."""
        return self._meltano_service.get_health_status()

    def discover_catalog(self) -> FlextResult[dict[str, object]]:
        """Discover catalog using base FlextMeltanoTapService."""
        return self._meltano_service.discover_catalog()

    # ORACLE-SPECIFIC: Use domain services for Oracle functionality
    def discover_oracle_tables(
        self,
        schema_name: str | None = None,
    ) -> FlextResult[list[FlextDbOracleTable]]:
        """Discover Oracle tables using domain service."""
        if schema_name:
            # Create new service with specific schema_name (FlextDomainService[T] is immutable)
            discovery_service = FlextOracleDiscoveryService(
                oracle_api=self._oracle_api,
                schema_name=schema_name,
            )
            return discovery_service.execute()
        return self._discovery_service.execute()

    def test_oracle_connection(self) -> FlextResult[bool]:
        """Test Oracle connection using domain service."""
        return self._connection_test_service.execute()

    def get_filtered_tables(self) -> FlextResult[list[str]]:
        """Get filtered table list using domain service."""
        return self._table_filter_service.execute()

    # HIGH-LEVEL ORCHESTRATION METHODS
    def initialize_tap(self) -> FlextResult[dict[str, object]]:
        """Initialize Oracle tap with connection test and table discovery."""
        try:
            logger.info("Initializing Oracle tap service")

            # Test connection first
            connection_result = self.test_oracle_connection()
            if connection_result.is_failure:
                return FlextResult.fail(
                    f"Connection test failed: {connection_result.error}",
                )

            # Discover tables
            tables_result = self.get_filtered_tables()
            if tables_result.is_failure:
                return FlextResult.fail(
                    f"Table discovery failed: {tables_result.error}",
                )

            # Prepare initialization status
            status = {
                "connection_status": "connected",
                "tables_discovered": len(tables_result.data or []),
                "oracle_config": {
                    "host": self._config.oracle_config.host,
                    "port": self._config.oracle_config.port,
                    "service_name": self._config.oracle_config.service_name,
                },
                "tap_config": {
                    "batch_size": self._config.tap_config.batch_size,
                    "stream_prefix": self._config.tap_config.stream_prefix,
                    "max_parallel_streams": self._config.tap_config.max_parallel_streams,
                },
            }

            logger.info("Oracle tap initialization completed successfully")
            return FlextResult.ok(status)

        except Exception as e:
            logger.exception("Oracle tap initialization failed")
            return FlextResult.fail(f"Initialization failed: {e}")

    def get_tap_status(self) -> FlextResult[dict[str, object]]:
        """Get comprehensive Oracle tap status."""
        try:
            # Get base health status
            health_result = self.get_health_status()
            base_status = health_result.data if health_result.success else {}

            # Add Oracle-specific status
            oracle_status = {
                "oracle_connection": "unknown",
                "discovered_tables": 0,
                "filtered_tables": 0,
            }

            # Test Oracle connection
            connection_result = self.test_oracle_connection()
            oracle_status["oracle_connection"] = (
                "connected" if connection_result.success else "failed"
            )

            # Get table counts
            discovery_result = self.discover_oracle_tables()
            if discovery_result.success:
                oracle_status["discovered_tables"] = len(discovery_result.data or [])

            filter_result = self.get_filtered_tables()
            if filter_result.success:
                oracle_status["filtered_tables"] = len(filter_result.data or [])

            # Combine status
            combined_status: dict[str, object] = {
                "oracle_tap": oracle_status,
                "timestamp": "now",  # Would use actual timestamp in real implementation
            }
            if base_status:
                combined_status.update(base_status)

            return FlextResult.ok(combined_status)

        except Exception as e:
            logger.exception("Failed to get tap status")
            return FlextResult.fail(f"Status check failed: {e}")


# =====================================================
# FACTORY FUNCTIONS
# =====================================================


def create_oracle_tap_service(
    config: FlextOracleTapConfig,
) -> FlextResult[FlextOracleTapService]:
    """Create Oracle tap service using COMPOSITION.

    Args:
        config: Oracle tap configuration

    Returns:
        FlextResult containing Oracle tap service

    """
    try:
        service = FlextOracleTapService(config=config)
        return FlextResult.ok(service)

    except Exception as e:
        return FlextResult.fail(f"Oracle tap service creation failed: {e}")


def create_oracle_discovery_service(
    oracle_api: FlextDbOracleApi,
    schema_name: str | None = None,
) -> FlextResult[FlextOracleDiscoveryService]:
    """Create Oracle discovery service.

    Args:
        oracle_api: Oracle database API instance
        schema_name: Optional schema name for discovery

    Returns:
        FlextResult containing Oracle discovery service

    """
    try:
        service = FlextOracleDiscoveryService(
            oracle_api=oracle_api,
            schema_name=schema_name,
        )
        return FlextResult.ok(service)

    except Exception as e:
        return FlextResult.fail(f"Oracle discovery service creation failed: {e}")


# Backward compatibility aliases
FlextOracleTapClient = FlextOracleTapService  # Common naming pattern
OracleTapService = FlextOracleTapService  # Short alias

__all__: list[str] = [
    "FlextOracleConnectionTestService",
    "FlextOracleDiscoveryService",
    "FlextOracleTableFilterService",
    "FlextOracleTapClient",
    "FlextOracleTapService",
    "OracleTapService",
    "create_oracle_discovery_service",
    "create_oracle_tap_service",
]
