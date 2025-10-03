"""Oracle Tap Client - Complete Tap Implementation with Domain Services.

Copyright (c) 2025 FLEXT Contributors
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from typing import override

from flext_db_oracle import (
    FlextDbOracleApi,
    FlextDbOracleTable,
)
from flext_meltano import (
    FlextMeltanoTypeAdapters,
    FlextTap,
)

from flext_core import FlextLogger, FlextResult, FlextTypes
from flext_tap_oracle.config import FlextTapOracleConfig
from flext_tap_oracle.typings import FlextTapOracleTypes

logger = FlextLogger(__name__)
# =====================================================
# DOMAIN SERVICES - Using FlextService[T] pattern
# =====================================================


class FlextOracleDiscoveryService:
    """Oracle table discovery service - simplified without Pydantic validation."""

    @override
    def __init__(
        self,
        oracle_api: FlextDbOracleApi,
        schema_name: str | None = None,
    ) -> None:
        """Initialize Oracle table discovery service.

        Args:
            oracle_api: FLEXT Oracle database API instance
            schema_name: Oracle schema name (defaults to 'USER')

        """
        # ZERO TOLERANCE FIX: Initialize utilities for ALL business logic
        from flext_tap_oracle.utilities import FlextTapOracleUtilities

        self._utilities = FlextTapOracleUtilities()
        self.oracle_api: FlextDbOracleApi = oracle_api
        self.schema_name: str | None = schema_name

    @override
    def execute(self: object) -> FlextResult[list[FlextDbOracleTable]]:
        """Execute Oracle table discovery using flext-db-oracle infrastructure."""
        try:
            schema_name = self.schema_name or "USER"  # Default Oracle schema
            logger.info("Discovering Oracle tables in schema: %s", schema_name)

            # ZERO TOLERANCE FIX: Use utilities for connection validation
            connection_validation_result = (
                self._utilities.ConfigurationValidation.validate_oracle_connection(
                    connection=self.oracle_api.connection, schema_name=schema_name
                )
            )
            if connection_validation_result.is_failure:
                return FlextResult[list[FlextDbOracleTable]].fail(
                    f"Connection validation failed: {connection_validation_result.error}"
                )

            # Get metadata manager from oracle_api
            connection = self.oracle_api.connection
            if connection is None:
                return FlextResult[list[FlextDbOracleTable]].fail(
                    "No Oracle connection available",
                )

            # ZERO TOLERANCE FIX: Use utilities for table discovery
            discovery_result = self._utilities.StreamManagement.discover_oracle_tables(
                connection=connection, schema_name=schema_name
            )

            if discovery_result.is_success:
                tables = discovery_result.unwrap()
                logger.info("Discovered %d Oracle tables", len(tables))
                return FlextResult[list[FlextDbOracleTable]].ok(tables)

            error_msg = discovery_result.error or "No tables found"
            logger.warning("Oracle table discovery failed: %s", error_msg)
            return FlextResult[list[FlextDbOracleTable]].fail(
                f"Table discovery failed: {error_msg}",
            )

        except Exception as e:
            # ZERO TOLERANCE FIX: Use utilities for error handling
            handled_error_result = (
                self._utilities.ErrorHandling.handle_oracle_discovery_error(
                    error=e, schema_name=schema_name, context="table_discovery"
                )
            )
            logger.exception("Oracle table discovery error")
            return FlextResult[list[FlextDbOracleTable]].fail(
                handled_error_result.unwrap_or(f"Table discovery error: {e}")
            )


class FlextOracleConnectionTestService:
    """Oracle connection test service - simplified without Pydantic validation."""

    @override
    def __init__(self, oracle_api: FlextDbOracleApi) -> None:
        """Initialize the instance."""
        # ZERO TOLERANCE FIX: Initialize utilities for ALL business logic
        from flext_tap_oracle.utilities import FlextTapOracleUtilities

        self._utilities = FlextTapOracleUtilities()
        self.oracle_api = oracle_api

    @override
    def execute(self: object) -> FlextResult[bool]:
        """Execute Oracle connection test using flext-db-oracle infrastructure."""
        try:
            logger.info("Testing Oracle connection")

            # ZERO TOLERANCE FIX: Use utilities for connection testing
            connection_test_result = (
                self._utilities.ConfigurationValidation.test_oracle_connection(
                    oracle_api=self.oracle_api
                )
            )

            if connection_test_result.is_success:
                logger.info("Oracle connection test successful")
                return FlextResult[bool].ok(True)

            error_msg = connection_test_result.error or "Connection failed"
            logger.error("Oracle connection test failed: %s", error_msg)
            return FlextResult[bool].fail(str(error_msg))

        except Exception as e:
            # ZERO TOLERANCE FIX: Use utilities for error handling
            handled_error_result = (
                self._utilities.ErrorHandling.handle_oracle_connection_error(
                    error=e, context="connection_test"
                )
            )
            logger.exception("Oracle connection test error")
            return FlextResult[bool].fail(
                handled_error_result.unwrap_or(f"Connection test error: {e}")
            )


class FlextOracleTableFilterService:
    """Oracle table filtering service - simplified without Pydantic validation."""

    @override
    def __init__(
        self,
        tap_config: FlextTapOracleConfig,
        discovery_service: FlextOracleDiscoveryService,
    ) -> None:
        """Initialize Oracle table filtering service.

        Args:
            tap_config: FLEXT Oracle tap configuration
            discovery_service: Oracle table discovery service

        """
        # ZERO TOLERANCE FIX: Initialize utilities for ALL business logic
        from flext_tap_oracle.utilities import FlextTapOracleUtilities

        self._utilities = FlextTapOracleUtilities()
        self.tap_config = tap_config
        self.discovery_service = discovery_service

    @override
    def execute(self: object) -> FlextResult[FlextTypes.StringList]:
        """Execute table filtering based on tap configuration."""
        try:
            tap_configuration: FlextTapOracleTypes.Configuration.TapOracleConfig = (
                self.tap_config.get_tap_config()
            )

            # ZERO TOLERANCE FIX: Use utilities for configuration validation
            config_validation_result = (
                self._utilities.ConfigurationValidation.validate_table_filter_config(
                    tables_filter=tap_configuration.tables_filter,
                    exclude_tables=tap_configuration.exclude_tables,
                )
            )
            if config_validation_result.is_failure:
                return FlextResult[FlextTypes.StringList].fail(
                    f"Configuration validation failed: {config_validation_result.error}"
                )

            # If specific tables are configured, use them
            if tap_configuration.tables_filter:
                logger.info(
                    "Using configured table filter: %s",
                    tap_configuration.tables_filter,
                )
                return FlextResult[FlextTypes.StringList].ok(
                    list(tap_configuration.tables_filter),
                )

            # Otherwise discover all tables and apply exclusions
            tables_result: FlextResult[object] = self.discovery_service.execute()
            if tables_result.is_failure:
                error_msg = tables_result.error or "Unknown discovery error"
                return FlextResult[FlextTypes.StringList].fail(error_msg)

            if tables_result.data is None:
                return FlextResult[None].fail("No table data returned")

            table_names = [table.name for table in tables_result.data]

            # ZERO TOLERANCE FIX: Use utilities for table filtering
            filtering_result = self._utilities.StreamManagement.filter_oracle_tables(
                discovered_tables=table_names,
                exclude_tables=tap_configuration.exclude_tables or [],
                performance_optimization=True,
            )

            if filtering_result.is_success:
                filtered_tables = filtering_result.unwrap()
                logger.info(
                    "Applied filtering, %d tables remaining", len(filtered_tables)
                )
                return FlextResult[FlextTypes.StringList].ok(filtered_tables)
            return FlextResult[FlextTypes.StringList].fail(
                f"Table filtering failed: {filtering_result.error}"
            )

        except Exception as e:
            # ZERO TOLERANCE FIX: Use utilities for error handling
            handled_error_result = (
                self._utilities.ErrorHandling.handle_oracle_filtering_error(
                    error=e, context="table_filtering"
                )
            )
            logger.exception("Table filtering error")
            return FlextResult[FlextTypes.StringList].fail(
                handled_error_result.unwrap_or(f"Table filtering error: {e}")
            )


# =====================================================
# MAIN TAP SERVICE - Using COMPOSITION pattern
# =====================================================


class FlextOracleTapService:
    """Oracle Tap Service using COMPOSITION with FlextMeltanoTapService + Domain Services.

    Esta classe usa COMPOSIÇÃO ao invés de herança:
    - FlextMeltanoTapService para funcionalidade base Singer/Meltano
    - Domain Services (FlextService[T]) para lógica Oracle

    SOLID Principles:
    - Single Responsibility: Cada domain service tem uma responsabilidade
    - Open/Closed: Extensível via novos domain services
    - Liskov Substitution: Domain services são intercambiáveis
    - Interface Segregation: Interfaces específicas por domain service
    - Dependency Inversion: Depends on abstractions (FlextService[T])
    """

    @override
    def __init__(self, config: FlextTapOracleConfig) -> None:
        """Initialize Oracle tap service using COMPOSITION pattern."""
        # ZERO TOLERANCE FIX: Initialize utilities for ALL business logic
        from flext_tap_oracle.utilities import FlextTapOracleUtilities

        self._utilities = FlextTapOracleUtilities()
        self._config: FlextTapOracleTypes.Configuration.TapOracleConfig = config

        # ZERO TOLERANCE FIX: Use utilities for configuration validation
        config_validation_result = (
            self._utilities.ConfigurationValidation.validate_tap_oracle_config(
                config=config
            )
        )
        if config_validation_result.is_failure:
            msg = f"Configuration validation failed: {config_validation_result.error}"
            raise ValueError(msg)

        # COMPOSITION: Use FlextTap for base functionality

        # Create tap configuration using FlextMeltano abstractions
        tap_config_dict = {
            "host": getattr(config, "host", "localhost"),
            "port": getattr(config, "port", 1521),
            "service_name": getattr(config, "service_name", "ORCL"),
            "username": getattr(config, "username", ""),
            "password": getattr(config, "password", ""),
        }

        # ZERO TOLERANCE FIX: Use utilities for tap config creation
        tap_config_creation_result = (
            self._utilities.ConfigurationValidation.create_flext_tap_config(
                tap_type="tap-oracle", connection_config=tap_config_dict
            )
        )

        if tap_config_creation_result.is_failure:
            msg = f"Failed to create tap config: {tap_config_creation_result.error}"
            raise ValueError(msg)

        adapter = FlextMeltanoTypeAdapters()
        self._meltano_service = FlextTap(tap_config_creation_result.unwrap(), adapter)

        # COMPOSITION: Create Oracle API
        oracle_config: FlextTapOracleTypes.Database.DatabaseConfiguration = (
            self._config.get_oracle_config()
        )
        self._oracle_api = FlextDbOracleApi(oracle_config)

        # COMPOSITION: Create domain services (FlextService[T])
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
    def config(self: object) -> FlextTapOracleConfig:
        """Get Oracle tap configuration."""
        return self._config

    @property
    def oracle_api(self: object) -> FlextDbOracleApi:
        """Get Oracle API."""
        return self._oracle_api

    @property
    def discovery_service(self: object) -> FlextOracleDiscoveryService:
        """Get Oracle discovery domain service."""
        return self._discovery_service

    @property
    def connection_test_service(self: object) -> FlextOracleConnectionTestService:
        """Get Oracle connection test domain service."""
        return self._connection_test_service

    @property
    def table_filter_service(self: object) -> FlextOracleTableFilterService:
        """Get Oracle table filter domain service."""
        return self._table_filter_service

    # DELEGATION: Delegate base functionality to FlextMeltanoTapService
    def validate_service(self: object) -> FlextResult[bool]:
        """Validate service using base FlextMeltanoTapService."""
        return self._meltano_service.validate_service()

    def get_health_status(
        self: object,
    ) -> FlextResult[FlextTapOracleTypes.Configuration.TapOracleConfig]:
        """Get health status using base FlextMeltanoTapService."""
        return self._meltano_service.get_health_status()

    def discover_catalog(
        self: object,
    ) -> FlextResult[FlextTapOracleTypes.Singer.CatalogEntry]:
        """Discover catalog using base FlextMeltanoTapService."""
        return self._meltano_service.discover_catalog()

    # ORACLE-SPECIFIC: Use domain services for Oracle functionality
    def discover_oracle_tables(
        self,
        schema_name: str | None = None,
    ) -> FlextResult[list[FlextDbOracleTable]]:
        """Discover Oracle tables using domain service."""
        if schema_name:
            # Create new service with specific schema_name (FlextService[T] is immutable)
            discovery_service = FlextOracleDiscoveryService(
                oracle_api=self._oracle_api,
                schema_name=schema_name,
            )
            return discovery_service.execute()
        return self._discovery_service.execute()

    def test_oracle_connection(self: object) -> FlextResult[bool]:
        """Test Oracle connection using domain service."""
        return self._connection_test_service.execute()

    def get_filtered_tables(self: object) -> FlextResult[FlextTypes.StringList]:
        """Get filtered table list using domain service."""
        return self._table_filter_service.execute()

    # HIGH-LEVEL ORCHESTRATION METHODS
    def initialize_tap(
        self: object,
    ) -> FlextResult[FlextTapOracleTypes.Configuration.TapOracleConfig]:
        """Initialize Oracle tap with connection test and table discovery."""
        try:
            logger.info("Initializing Oracle tap service")

            # ZERO TOLERANCE FIX: Use utilities for initialization process
            initialization_result = (
                self._utilities.StreamManagement.initialize_oracle_tap(
                    oracle_api=self._oracle_api,
                    config=self._config,
                    connection_test_service=self._connection_test_service,
                    table_filter_service=self._table_filter_service,
                )
            )

            if initialization_result.is_success:
                initialization_status = initialization_result.unwrap()
                logger.info("Oracle tap initialization completed successfully")
                return FlextResult[
                    FlextTapOracleTypes.Configuration.TapOracleConfig
                ].ok(initialization_status)
            return FlextResult[FlextTapOracleTypes.Configuration.TapOracleConfig].fail(
                f"Initialization failed: {initialization_result.error}"
            )

        except Exception as e:
            # ZERO TOLERANCE FIX: Use utilities for error handling
            handled_error_result = (
                self._utilities.ErrorHandling.handle_oracle_initialization_error(
                    error=e, context="tap_initialization"
                )
            )
            logger.exception("Oracle tap initialization failed")
            return FlextResult[FlextTapOracleTypes.Configuration.TapOracleConfig].fail(
                handled_error_result.unwrap_or(f"Initialization failed: {e}")
            )

    def get_tap_status(
        self: object,
    ) -> FlextResult[FlextTapOracleTypes.Configuration.TapOracleConfig]:
        """Get comprehensive Oracle tap status."""
        try:
            # ZERO TOLERANCE FIX: Use utilities for status generation
            status_generation_result = (
                self._utilities.PerformanceOptimization.generate_comprehensive_status(
                    meltano_service=self._meltano_service,
                    connection_test_service=self._connection_test_service,
                    discovery_service=self._discovery_service,
                    table_filter_service=self._table_filter_service,
                )
            )

            if status_generation_result.is_success:
                combined_status = status_generation_result.unwrap()
                return FlextResult[
                    FlextTapOracleTypes.Configuration.TapOracleConfig
                ].ok(combined_status)
            return FlextResult[FlextTapOracleTypes.Configuration.TapOracleConfig].fail(
                f"Status generation failed: {status_generation_result.error}"
            )

        except Exception as e:
            # ZERO TOLERANCE FIX: Use utilities for error handling
            handled_error_result = (
                self._utilities.ErrorHandling.handle_oracle_status_error(
                    error=e, context="status_check"
                )
            )
            logger.exception("Failed to get tap status")
            return FlextResult[FlextTapOracleTypes.Configuration.TapOracleConfig].fail(
                handled_error_result.unwrap_or(f"Status check failed: {e}")
            )


# =====================================================
# FACTORY FUNCTIONS
# =====================================================


def create_oracle_tap_service(
    config: FlextTapOracleConfig,
) -> FlextResult[FlextOracleTapService]:
    """Create Oracle tap service using COMPOSITION.

    Args:
      config: Oracle tap configuration

    Returns:
      FlextResult containing Oracle tap service

    """
    try:
        service = FlextOracleTapService(config=config)
        return FlextResult[FlextOracleTapService].ok(service)

    except Exception as e:
        return FlextResult[FlextOracleTapService].fail(
            f"Oracle tap service creation failed: {e}",
        )


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
        return FlextResult[FlextOracleDiscoveryService].ok(service)

    except Exception as e:
        return FlextResult[FlextOracleDiscoveryService].fail(
            f"Oracle discovery service creation failed: {e}",
        )


__all__: FlextTypes.StringList = [
    "FlextOracleConnectionTestService",
    "FlextOracleDiscoveryService",
    "FlextOracleTableFilterService",
    "FlextOracleTapService",
    "create_oracle_discovery_service",
    "create_oracle_tap_service",
]
