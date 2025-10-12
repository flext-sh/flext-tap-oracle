"""Oracle Tap Client - Complete Tap Implementation with Domain Services.

Copyright (c) 2025 FLEXT Contributors
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from typing import override

# Meltano imports not needed - using direct domain services
from flext_core import FlextCore
from flext_db_oracle import (
    FlextDbOracleApi,
    FlextDbOracleTable,
)

from flext_tap_oracle.config import FlextMeltanoTapOracleConfig
from flext_tap_oracle.typings import FlextMeltanoTapOracleTypes

logger = FlextCore.Logger(__name__)
# =====================================================
# DOMAIN SERVICES - Using FlextCore.Service[T] pattern
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
        from flext_tap_oracle.utilities import FlextMeltanoTapOracleUtilities

        self._utilities = FlextMeltanoTapOracleUtilities()
        self.oracle_api: FlextDbOracleApi = oracle_api
        self.schema_name: str | None = schema_name

    @override
    def execute(self: object) -> FlextCore.Result[list[FlextDbOracleTable]]:
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
                return FlextCore.Result[list[FlextDbOracleTable]].fail(
                    f"Connection validation failed: {connection_validation_result.error}"
                )

            # Get metadata manager from oracle_api
            connection = self.oracle_api.connection
            if connection is None:
                return FlextCore.Result[list[FlextDbOracleTable]].fail(
                    "No Oracle connection available",
                )

            # ZERO TOLERANCE FIX: Use utilities for table discovery
            discovery_result = self._utilities.StreamManagement.discover_oracle_tables(
                connection=connection, schema_name=schema_name
            )

            if discovery_result.is_success:
                tables = discovery_result.unwrap()
                logger.info("Discovered %d Oracle tables", len(tables))
                return FlextCore.Result[list[FlextDbOracleTable]].ok(tables)

            error_msg = discovery_result.error or "No tables found"
            logger.warning("Oracle table discovery failed: %s", error_msg)
            return FlextCore.Result[list[FlextDbOracleTable]].fail(
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
            return FlextCore.Result[list[FlextDbOracleTable]].fail(
                handled_error_result.unwrap_or(f"Table discovery error: {e}")
            )


class FlextOracleConnectionTestService:
    """Oracle connection test service - simplified without Pydantic validation."""

    @override
    def __init__(self, oracle_api: FlextDbOracleApi) -> None:
        """Initialize the instance."""
        # ZERO TOLERANCE FIX: Initialize utilities for ALL business logic
        from flext_tap_oracle.utilities import FlextMeltanoTapOracleUtilities

        self._utilities = FlextMeltanoTapOracleUtilities()
        self.oracle_api = oracle_api

    @override
    def execute(self: object) -> FlextCore.Result[bool]:
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
                return FlextCore.Result[bool].ok(True)

            error_msg = connection_test_result.error or "Connection failed"
            logger.error("Oracle connection test failed: %s", error_msg)
            return FlextCore.Result[bool].fail(str(error_msg))

        except Exception as e:
            # ZERO TOLERANCE FIX: Use utilities for error handling
            handled_error_result = (
                self._utilities.ErrorHandling.handle_oracle_connection_error(
                    error=e, context="connection_test"
                )
            )
            logger.exception("Oracle connection test error")
            return FlextCore.Result[bool].fail(
                handled_error_result.unwrap_or(f"Connection test error: {e}")
            )


class FlextOracleTableFilterService:
    """Oracle table filtering service - simplified without Pydantic validation."""

    @override
    def __init__(
        self,
        tap_config: FlextMeltanoTapOracleConfig,
        discovery_service: FlextOracleDiscoveryService,
    ) -> None:
        """Initialize Oracle table filtering service.

        Args:
            tap_config: FLEXT Oracle tap configuration
            discovery_service: Oracle table discovery service

        """
        # ZERO TOLERANCE FIX: Initialize utilities for ALL business logic
        from flext_tap_oracle.utilities import FlextMeltanoTapOracleUtilities

        self._utilities = FlextMeltanoTapOracleUtilities()
        self.tap_config = tap_config
        self.discovery_service = discovery_service

    @override
    def execute(self: object) -> FlextCore.Result[FlextCore.Types.StringList]:
        """Execute table filtering based on tap configuration."""
        try:
            tap_configuration: FlextMeltanoTapOracleTypes.Configuration.TapOracleConfig = self.tap_config.get_tap_config()

            # ZERO TOLERANCE FIX: Use utilities for configuration validation
            config_validation_result = (
                self._utilities.ConfigurationValidation.validate_table_filter_config(
                    tables_filter=tap_configuration.tables_filter,
                    exclude_tables=tap_configuration.exclude_tables,
                )
            )
            if config_validation_result.is_failure:
                return FlextCore.Result[FlextCore.Types.StringList].fail(
                    f"Configuration validation failed: {config_validation_result.error}"
                )

            # If specific tables are configured, use them
            if tap_configuration.tables_filter:
                logger.info(
                    "Using configured table filter: %s",
                    tap_configuration.tables_filter,
                )
                return FlextCore.Result[FlextCore.Types.StringList].ok(
                    list(tap_configuration.tables_filter),
                )

            # Otherwise discover all tables and apply exclusions
            tables_result: FlextCore.Result[object] = self.discovery_service.execute()
            if tables_result.is_failure:
                error_msg = tables_result.error or "Unknown discovery error"
                return FlextCore.Result[FlextCore.Types.StringList].fail(error_msg)

            if tables_result.data is None:
                return FlextCore.Result[None].fail("No table data returned")

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
                return FlextCore.Result[FlextCore.Types.StringList].ok(filtered_tables)
            return FlextCore.Result[FlextCore.Types.StringList].fail(
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
            return FlextCore.Result[FlextCore.Types.StringList].fail(
                handled_error_result.unwrap_or(f"Table filtering error: {e}")
            )


# =====================================================
# MAIN TAP SERVICE - Using COMPOSITION pattern
# =====================================================


class FlextOracleTapService:
    """Oracle Tap Service using COMPOSITION with FlextMeltanoTapService + Domain Services.

    Esta classe usa COMPOSIÇÃO ao invés de herança:
    - FlextMeltanoTapService para funcionalidade base Singer/Meltano
    - Domain Services (FlextCore.Service[T]) para lógica Oracle

    SOLID Principles:
    - Single Responsibility: Cada domain service tem uma responsabilidade
    - Open/Closed: Extensível via novos domain services
    - Liskov Substitution: Domain services são intercambiáveis
    - Interface Segregation: Interfaces específicas por domain service
    - Dependency Inversion: Depends on abstractions (FlextCore.Service[T])
    """

    @override
    def __init__(self, config: FlextMeltanoTapOracleConfig) -> None:
        """Initialize Oracle tap service using COMPOSITION pattern."""
        # ZERO TOLERANCE FIX: Initialize utilities for ALL business logic
        from flext_tap_oracle.utilities import FlextMeltanoTapOracleUtilities

        self._utilities = FlextMeltanoTapOracleUtilities()
        self._config: FlextMeltanoTapOracleTypes.Configuration.TapOracleConfig = config

        # ZERO TOLERANCE FIX: Use utilities for configuration validation
        config_validation_result = (
            self._utilities.ConfigurationValidation.validate_tap_oracle_config(
                config=config
            )
        )
        if config_validation_result.is_failure:
            msg = f"Configuration validation failed: {config_validation_result.error}"
            raise ValueError(msg)

        # COMPOSITION: Using direct domain services (no meltano_service needed)

        # COMPOSITION: Create Oracle API
        oracle_config: FlextMeltanoTapOracleTypes.Database.DatabaseConfiguration = (
            self._config.get_oracle_config()
        )
        self._oracle_api = FlextDbOracleApi(oracle_config)

        # COMPOSITION: Create domain services (FlextCore.Service[T])
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
    def config(self: object) -> FlextMeltanoTapOracleConfig:
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

    # Service methods - using direct domain services
    def validate_service(self: object) -> FlextCore.Result[bool]:
        """Validate service using connection test."""
        return self._connection_test_service.execute()

    def get_health_status(
        self: object,
    ) -> FlextCore.Result[FlextMeltanoTapOracleTypes.Configuration.TapOracleConfig]:
        """Get health status."""
        return FlextCore.Result[
            FlextMeltanoTapOracleTypes.Configuration.TapOracleConfig
        ].ok(self._config)

    def discover_catalog(
        self: object,
    ) -> FlextCore.Result[FlextMeltanoTapOracleTypes.Singer.CatalogEntry]:
        """Discover catalog - not implemented."""
        return FlextCore.Result[FlextMeltanoTapOracleTypes.Singer.CatalogEntry].fail(
            "Catalog discovery not implemented"
        )

    # ORACLE-SPECIFIC: Use domain services for Oracle functionality
    def discover_oracle_tables(
        self,
        schema_name: str | None = None,
    ) -> FlextCore.Result[list[FlextDbOracleTable]]:
        """Discover Oracle tables using domain service."""
        if schema_name:
            # Create new service with specific schema_name (FlextCore.Service[T] is immutable)
            discovery_service = FlextOracleDiscoveryService(
                oracle_api=self._oracle_api,
                schema_name=schema_name,
            )
            return discovery_service.execute()
        return self._discovery_service.execute()

    def test_oracle_connection(self: object) -> FlextCore.Result[bool]:
        """Test Oracle connection using domain service."""
        return self._connection_test_service.execute()

    def get_filtered_tables(
        self: object,
    ) -> FlextCore.Result[FlextCore.Types.StringList]:
        """Get filtered table list using domain service."""
        return self._table_filter_service.execute()

    # HIGH-LEVEL ORCHESTRATION METHODS
    def initialize_tap(
        self: object,
    ) -> FlextCore.Result[FlextMeltanoTapOracleTypes.Configuration.TapOracleConfig]:
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
                return FlextCore.Result[
                    FlextMeltanoTapOracleTypes.Configuration.TapOracleConfig
                ].ok(initialization_status)
            return FlextCore.Result[
                FlextMeltanoTapOracleTypes.Configuration.TapOracleConfig
            ].fail(f"Initialization failed: {initialization_result.error}")

        except Exception as e:
            # ZERO TOLERANCE FIX: Use utilities for error handling
            handled_error_result = (
                self._utilities.ErrorHandling.handle_oracle_initialization_error(
                    error=e, context="tap_initialization"
                )
            )
            logger.exception("Oracle tap initialization failed")
            return FlextCore.Result[
                FlextMeltanoTapOracleTypes.Configuration.TapOracleConfig
            ].fail(handled_error_result.unwrap_or(f"Initialization failed: {e}"))

    def get_tap_status(
        self: object,
    ) -> FlextCore.Result[FlextMeltanoTapOracleTypes.Configuration.TapOracleConfig]:
        """Get comprehensive Oracle tap status."""
        try:
            # Simple status - connection test result
            connection_test_result = self._connection_test_service.execute()

            if connection_test_result.is_success:
                return FlextCore.Result[
                    FlextMeltanoTapOracleTypes.Configuration.TapOracleConfig
                ].ok(self._config)
            return FlextCore.Result[
                FlextMeltanoTapOracleTypes.Configuration.TapOracleConfig
            ].fail(f"Connection test failed: {connection_test_result.error}")

        except Exception as e:
            logger.exception("Failed to get tap status")
            return FlextCore.Result[
                FlextMeltanoTapOracleTypes.Configuration.TapOracleConfig
            ].fail(f"Status check failed: {e}")


# =====================================================
# FACTORY FUNCTIONS
# =====================================================


def create_oracle_tap_service(
    config: FlextMeltanoTapOracleConfig,
) -> FlextCore.Result[FlextOracleTapService]:
    """Create Oracle tap service using COMPOSITION.

    Args:
      config: Oracle tap configuration

    Returns:
      FlextCore.Result containing Oracle tap service

    """
    try:
        service = FlextOracleTapService(config=config)
        return FlextCore.Result[FlextOracleTapService].ok(service)

    except Exception as e:
        return FlextCore.Result[FlextOracleTapService].fail(
            f"Oracle tap service creation failed: {e}",
        )


def create_oracle_discovery_service(
    oracle_api: FlextDbOracleApi,
    schema_name: str | None = None,
) -> FlextCore.Result[FlextOracleDiscoveryService]:
    """Create Oracle discovery service.

    Args:
      oracle_api: Oracle database API instance
      schema_name: Optional schema name for discovery

    Returns:
      FlextCore.Result containing Oracle discovery service

    """
    try:
        service = FlextOracleDiscoveryService(
            oracle_api=oracle_api,
            schema_name=schema_name,
        )
        return FlextCore.Result[FlextOracleDiscoveryService].ok(service)

    except Exception as e:
        return FlextCore.Result[FlextOracleDiscoveryService].fail(
            f"Oracle discovery service creation failed: {e}",
        )


__all__: FlextCore.Types.StringList = [
    "FlextOracleConnectionTestService",
    "FlextOracleDiscoveryService",
    "FlextOracleTableFilterService",
    "FlextOracleTapService",
    "create_oracle_discovery_service",
    "create_oracle_tap_service",
]
