"""Oracle Tap Client - Complete Tap Implementation with Services.

Copyright (c) 2025 FLEXT Contributors
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from typing import override

from flext_core import FlextLogger, FlextResult, FlextService
from flext_db_oracle import (
    FlextDbOracleApi,
    FlextDbOracleModels,
    FlextDbOracleSettings,
)

from flext_tap_oracle.settings import FlextMeltanoTapOracleSettings

logger = FlextLogger(__name__)
# =====================================================
# DOMAIN SERVICES - Using FlextService[T] pattern
# =====================================================


class FlextOracleDiscoveryService:
    """Oracle table discovery service - simplified without Pydantic validation."""

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
        self.oracle_api: FlextDbOracleApi = oracle_api
        self.schema_name: str | None = schema_name

    def execute(self) -> FlextResult[list[FlextDbOracleModels.DbOracle.Table]]:
        """Execute Oracle table discovery using Layer 2 flext-db-oracle API."""
        try:
            schema_name = self.schema_name or "USER"  # Default Oracle schema
            logger.info("Discovering Oracle tables in schema: %s", schema_name)

            # Use Layer 2 API directly to discover tables
            tables_result = self.oracle_api.services.get_tables(schema=schema_name)
            if tables_result.is_failure:
                error_msg = tables_result.error or "Table discovery failed"
                logger.warning("Oracle table discovery failed: %s", error_msg)
                return FlextResult[list[FlextDbOracleModels.DbOracle.Table]].fail(
                    error_msg
                )

            # Convert string table names to FlextDbOracleModels.DbOracle.Table objects
            table_names = tables_result.value or []
            tables: list[FlextDbOracleModels.DbOracle.Table] = [
                FlextDbOracleModels.DbOracle.Table(name=table_name, schema=schema_name)
                for table_name in table_names
            ]

            logger.info(
                "Discovered %d Oracle tables in schema %s",
                len(tables),
                schema_name,
            )
            return FlextResult[list[FlextDbOracleModels.DbOracle.Table]].ok(tables)

        except (ValueError, TypeError, KeyError, AttributeError, OSError) as e:
            # Use FlextResult error handling pattern
            logger.exception("Oracle table discovery error")
            error_msg = f"Table discovery error in schema {self.schema_name}: {e}"
            return FlextResult[list[FlextDbOracleModels.DbOracle.Table]].fail(error_msg)


class FlextOracleConnectionTestService:
    """Oracle connection test service - simplified without Pydantic validation."""

    def __init__(self, oracle_api: FlextDbOracleApi) -> None:
        """Initialize the instance."""
        self.oracle_api = oracle_api

    def execute(self) -> FlextResult[bool]:
        """Execute Oracle connection test using Layer 2 flext-db-oracle API."""
        try:
            logger.info("Testing Oracle connection")

            # Use Layer 2 API directly to test connection
            test_result = self.oracle_api.test_connection()

            if test_result.is_success:
                logger.info("Oracle connection test successful")
                return FlextResult[bool].ok(value=True)

            error_msg = test_result.error or "Connection test failed"
            logger.error("Oracle connection test failed: %s", error_msg)
            return FlextResult[bool].fail(error_msg)

        except (ValueError, TypeError, KeyError, AttributeError, OSError) as e:
            # Use FlextResult error handling pattern
            logger.exception("Oracle connection test error")
            error_msg = f"Connection test error: {e}"
            return FlextResult[bool].fail(error_msg)


class FlextOracleTableFilterService:
    """Oracle table filtering service - simplified without Pydantic validation."""

    def __init__(
        self,
        tap_config: FlextMeltanoTapOracleSettings,
        discovery_service: FlextOracleDiscoveryService,
    ) -> None:
        """Initialize Oracle table filtering service.

        Args:
        tap_config: FLEXT Oracle tap configuration
        discovery_service: Oracle table discovery service

        """
        self.tap_config = tap_config
        self.discovery_service = discovery_service

    def execute(self) -> FlextResult[list[str]]:
        """Execute table filtering based on tap configuration using Layer 2 API."""
        try:
            tap_configuration = self.tap_config.get_tap_config()

            # If specific tables are configured, use them directly
            tables_filter = tap_configuration.get("tables_filter")
            if isinstance(tables_filter, list) and tables_filter:
                logger.info(
                    "Using configured table filter: %s",
                    tables_filter,
                )
                return FlextResult[list[str]].ok(
                    [str(table_name) for table_name in tables_filter],
                )

            # Otherwise discover all tables from Oracle using Layer 2 API
            tables_result = self.discovery_service.execute()
            if tables_result.is_failure:
                error_msg = tables_result.error or "Table discovery failed"
                logger.warning("Table discovery failed: %s", error_msg)
                return FlextResult[list[str]].fail(error_msg)

            if not tables_result.data:
                return FlextResult[list[str]].fail("No Oracle tables discovered")

            # Extract table names from discovered tables
            table_names = [table.name for table in tables_result.data]

            # Apply exclusion filter if configured
            exclude_tables_raw = tap_configuration.get("exclude_tables")
            exclude_tables: list[str] = []
            if isinstance(exclude_tables_raw, list):
                exclude_tables = [str(table_name) for table_name in exclude_tables_raw]
            if exclude_tables:
                filtered_tables = [
                    table for table in table_names if table not in exclude_tables
                ]
                logger.info(
                    "Applied exclusion filter: %d tables excluded, %d remaining",
                    len(exclude_tables),
                    len(filtered_tables),
                )
                return FlextResult[list[str]].ok(filtered_tables)

            logger.info(
                "No table exclusions configured, using all %d tables",
                len(table_names),
            )
            return FlextResult[list[str]].ok(table_names)

        except (ValueError, TypeError, KeyError, AttributeError, OSError) as e:
            logger.exception("Table filtering error")
            error_msg = f"Table filtering error: {e}"
            return FlextResult[list[str]].fail(error_msg)


# =====================================================
# MAIN TAP SERVICE - Using INHERITANCE pattern
# =====================================================


class FlextOracleTapService(FlextService[list[FlextDbOracleModels.DbOracle.Table]]):
    """Oracle Tap Service using FLEXT Service Pattern.

    This class extends FlextService[T] to provide Oracle-specific
    database operations and domain services using the FLEXT architecture pattern.
    Leverages Layer 2 (flext-db-oracle) for all Oracle operations.

    SOLID Principles:
    - Single Responsibility: Each domain service has one responsibility
    - Open/Closed: Extensible via new domain services
    - Liskov Substitution: Substitutable for FlextService[FlextMeltanoTapOracleSettings]
    - Interface Segregation: Specific interfaces per domain service
    - Dependency Inversion: Depends on abstractions (FlextService[T])
    """

    @override
    def __init__(self, config: FlextMeltanoTapOracleSettings) -> None:
        """Initialize Oracle tap service with FLEXT Service Pattern."""
        # Validate configuration - check required fields
        if not config:
            error_msg = "Configuration is required"
            raise ValueError(error_msg)

        # Initialize parent class
        super().__init__(config=config)

        # Initialize Oracle-specific components
        oracle_config = config.get_oracle_config()
        # Convert config to FlextDbOracleSettings

        oracle_settings = FlextDbOracleSettings.model_validate(oracle_config)
        self._oracle_api = FlextDbOracleApi(oracle_settings)

        # Create domain services for Oracle operations
        # Get schema name from configuration
        schema_name = oracle_config.get("schema_name") or oracle_config.get(
            "service_name",
        )

        self._discovery_service = FlextOracleDiscoveryService(
            oracle_api=self._oracle_api,
            schema_name=str(schema_name) if schema_name else None,
        )
        self._connection_test_service = FlextOracleConnectionTestService(
            oracle_api=self._oracle_api,
        )
        self._table_filter_service = FlextOracleTableFilterService(
            tap_config=config,
            discovery_service=self._discovery_service,
        )

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

    # Service methods - using direct domain services
    @override
    def execute(self) -> FlextResult[list[FlextDbOracleModels.DbOracle.Table]]:
        """Execute Oracle tap service - discover tables."""
        return self._discovery_service.execute()

    def validate_service(self) -> FlextResult[bool]:
        """Validate service using connection test."""
        return self._connection_test_service.execute()

    def get_health_status(self) -> FlextResult[bool]:
        """Get service health status using connection test."""
        return self._connection_test_service.execute()

    # ORACLE-SPECIFIC: Use domain services for Oracle functionality
    def discover_oracle_tables(
        self,
        schema_name: str | None = None,
    ) -> FlextResult[list[FlextDbOracleModels.DbOracle.Table]]:
        """Discover Oracle tables using domain service."""
        if schema_name:
            # Create new service with specific schema_name (FlextService[T] is immutable)
            discovery_service = FlextOracleDiscoveryService(
                oracle_api=self._oracle_api,
                schema_name=schema_name,
            )
            return discovery_service.execute()
        return self._discovery_service.execute()

    def test_oracle_connection(self) -> FlextResult[bool]:
        """Test Oracle connection using domain service."""
        return self._connection_test_service.execute()

    def get_filtered_tables(
        self,
    ) -> FlextResult[list[str]]:
        """Get filtered table list using domain service."""
        return self._table_filter_service.execute()

    # HIGH-LEVEL ORCHESTRATION METHODS
    def initialize_tap(self) -> FlextResult[bool]:
        """Initialize Oracle tap by testing connection and discovering tables."""
        try:
            logger.info("Initializing Oracle tap service")

            # Test Oracle connection
            connection_result = self.test_oracle_connection()
            if connection_result.is_failure:
                logger.error(
                    f"Oracle connection test failed: {connection_result.error}",
                )
                return FlextResult[bool].fail(
                    f"Connection test failed: {connection_result.error}",
                )

            # Discover tables
            tables_result = self.get_filtered_tables()
            if tables_result.is_failure:
                logger.error(f"Table discovery failed: {tables_result.error}")
                return FlextResult[bool].fail(
                    f"Table discovery failed: {tables_result.error}",
                )

            logger.info("Oracle tap initialization completed successfully")
            return FlextResult[bool].ok(value=True)

        except (ValueError, TypeError, KeyError, AttributeError, OSError) as e:
            logger.exception("Oracle tap initialization failed")
            error_msg = f"Initialization failed: {e}"
            return FlextResult[bool].fail(error_msg)

    def get_tap_status(self) -> FlextResult[bool]:
        """Get Oracle tap status by testing connection."""
        try:
            # Test Oracle connection using domain service
            connection_test_result = self._connection_test_service.execute()

            if connection_test_result.is_success:
                logger.info("Oracle tap status: healthy")
                return FlextResult[bool].ok(value=True)

            logger.warning(
                f"Oracle tap status check failed: {connection_test_result.error}",
            )
            return FlextResult[bool].fail(
                f"Connection test failed: {connection_test_result.error}",
            )

        except (ValueError, TypeError, KeyError, AttributeError, OSError) as e:
            logger.exception("Failed to get tap status")
            return FlextResult[bool].fail(f"Status check failed: {e}")


# =====================================================
# FACTORY FUNCTIONS
# =====================================================


def create_oracle_tap_service(
    config: FlextMeltanoTapOracleSettings,
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

    except (ValueError, TypeError, KeyError, AttributeError, OSError) as e:
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

    except (ValueError, TypeError, KeyError, AttributeError, OSError) as e:
        return FlextResult[FlextOracleDiscoveryService].fail(
            f"Oracle discovery service creation failed: {e}",
        )


__all__: list[str] = [
    "FlextOracleConnectionTestService",
    "FlextOracleDiscoveryService",
    "FlextOracleTableFilterService",
    "FlextOracleTapService",
    "create_oracle_discovery_service",
    "create_oracle_tap_service",
]
