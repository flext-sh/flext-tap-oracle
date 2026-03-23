"""Oracle Tap Client - Complete Tap Implementation with Services.

Copyright (c) 2025 FLEXT Contributors
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from collections.abc import Mapping, Sequence
from typing import override

from flext_core import FlextLogger, FlextService, r, t
from flext_db_oracle import FlextDbOracleApi, FlextDbOracleModels, FlextDbOracleSettings

from flext_tap_oracle.settings import FlextTapOracleSettings

logger = FlextLogger(__name__)


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

    def execute(self) -> r[Sequence[FlextDbOracleModels.DbOracle.Table]]:
        """Execute Oracle table discovery using Layer 2 flext-db-oracle API."""
        try:
            schema_name = self.schema_name or "USER"
            logger.info("Discovering Oracle tables in schema: %s", schema_name)
            tables_result = self.oracle_api.get_tables(schema=schema_name)
            if tables_result.is_failure:
                error_msg = tables_result.error or "Table discovery failed"
                logger.warning("Oracle table discovery failed: %s", error_msg)
                return r[Sequence[FlextDbOracleModels.DbOracle.Table]].fail(error_msg)
            table_names = tables_result.value or []
            tables: Sequence[FlextDbOracleModels.DbOracle.Table] = [
                FlextDbOracleModels.DbOracle.Table(
                    name=table_name, owner=schema_name, columns=[]
                )
                for table_name in table_names
            ]
            logger.info(
                "Discovered %d Oracle tables in schema %s",
                len(tables),
                schema_name,
            )
            return r[Sequence[FlextDbOracleModels.DbOracle.Table]].ok(tables)
        except (ValueError, TypeError, KeyError, AttributeError, OSError) as e:
            logger.exception("Oracle table discovery error")
            error_msg = f"Table discovery error in schema {self.schema_name}: {e}"
            return r[Sequence[FlextDbOracleModels.DbOracle.Table]].fail(error_msg)


class FlextOracleConnectionTestService:
    """Oracle connection test service - simplified without Pydantic validation."""

    def __init__(self, oracle_api: FlextDbOracleApi) -> None:
        """Initialize the instance."""
        self.oracle_api = oracle_api

    def execute(self) -> r[bool]:
        """Execute Oracle connection test using Layer 2 flext-db-oracle API."""
        try:
            logger.info("Testing Oracle connection")
            test_result = self.oracle_api.test_connection()
            if test_result.is_success:
                logger.info("Oracle connection test successful")
                return r[bool].ok(value=True)
            error_msg = test_result.error or "Connection test failed"
            logger.error("Oracle connection test failed: %s", error_msg)
            return r[bool].fail(error_msg)
        except (ValueError, TypeError, KeyError, AttributeError, OSError) as e:
            logger.exception("Oracle connection test error")
            error_msg = f"Connection test error: {e}"
            return r[bool].fail(error_msg)


class FlextOracleTableFilterService:
    """Oracle table filtering service - simplified without Pydantic validation."""

    def __init__(
        self,
        tap_config: FlextTapOracleSettings,
        discovery_service: FlextOracleDiscoveryService,
    ) -> None:
        """Initialize Oracle table filtering service.

        Args:
        tap_config: FLEXT Oracle tap configuration
        discovery_service: Oracle table discovery service

        """
        self.tap_config = tap_config
        self.discovery_service = discovery_service

    def execute(self) -> r[Sequence[str]]:
        """Execute table filtering based on tap configuration using Layer 2 API."""
        try:
            tap_configuration: Mapping[str, t.Scalar] = self.tap_config.get_tap_config()
            tables_filter: t.Scalar | Sequence[t.Scalar] | None = tap_configuration.get(
                "tables_filter",
            )
            if isinstance(tables_filter, list) and tables_filter:
                tables_filter_list: Sequence[str] = list(map(str, tables_filter))
                logger.info(
                    "Using configured table filter: %s",
                    ", ".join(tables_filter_list),
                )
                return r[Sequence[str]].ok(tables_filter_list)
            tables_result = self.discovery_service.execute()
            if tables_result.is_failure:
                error_msg = tables_result.error or "Table discovery failed"
                logger.warning("Table discovery failed: %s", error_msg)
                return r[Sequence[str]].fail(error_msg)
            if not tables_result.value:
                return r[Sequence[str]].fail("No Oracle tables discovered")
            discovered_tables: Sequence[FlextDbOracleModels.DbOracle.Table] = (
                tables_result.value
            )
            table_names: Sequence[str] = [table.name for table in discovered_tables]
            exclude_tables_raw: t.Scalar | Sequence[t.Scalar] | None = (
                tap_configuration.get("exclude_tables")
            )
            exclude_tables: Sequence[str] = []
            if isinstance(exclude_tables_raw, list):
                exclude_tables = list(map(str, exclude_tables_raw))
            if exclude_tables:
                filtered_tables = [
                    table for table in table_names if table not in exclude_tables
                ]
                logger.info(
                    "Applied exclusion filter: %d tables excluded, %d remaining",
                    len(exclude_tables),
                    len(filtered_tables),
                )
                return r[Sequence[str]].ok(filtered_tables)
            logger.info(
                "No table exclusions configured, using all %d tables",
                len(table_names),
            )
            return r[Sequence[str]].ok(table_names)
        except (ValueError, TypeError, KeyError, AttributeError, OSError) as e:
            logger.exception("Table filtering error")
            error_msg = f"Table filtering error: {e}"
            return r[Sequence[str]].fail(error_msg)


class FlextOracleTapService(FlextService[Sequence[FlextDbOracleModels.DbOracle.Table]]):
    """Oracle Tap Service using FLEXT Service Pattern.

    This class extends FlextService[T] to provide Oracle-specific
    database operations and domain services using the FLEXT architecture pattern.
    Leverages Layer 2 (flext-db-oracle) for all Oracle operations.

    SOLID Principles:
    - Single Responsibility: Each domain service has one responsibility
    - Open/Closed: Extensible via new domain services
    - Liskov Substitution: Substitutable for FlextService[FlextTapOracleSettings]
    - Interface Segregation: Specific interfaces per domain service
    - Dependency Inversion: Depends on abstractions (FlextService[T])
    """

    @override
    def __init__(self, config: FlextTapOracleSettings) -> None:
        """Initialize Oracle tap service with FLEXT Service Pattern."""
        if not config:
            error_msg = "Configuration is required"
            raise ValueError(error_msg)
        super().__init__()
        oracle_config: Mapping[str, t.Scalar] = config.get_oracle_config()
        oracle_settings = FlextDbOracleSettings.model_validate(oracle_config)
        self._oracle_api = FlextDbOracleApi(oracle_settings)
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
    def connection_test_service(self) -> FlextOracleConnectionTestService:
        """Get Oracle connection test domain service."""
        return self._connection_test_service

    @property
    def discovery_service(self) -> FlextOracleDiscoveryService:
        """Get Oracle discovery domain service."""
        return self._discovery_service

    @property
    def oracle_api(self) -> FlextDbOracleApi:
        """Get Oracle API."""
        return self._oracle_api

    @property
    def table_filter_service(self) -> FlextOracleTableFilterService:
        """Get Oracle table filter domain service."""
        return self._table_filter_service

    def discover_oracle_tables(
        self,
        schema_name: str | None = None,
    ) -> r[Sequence[FlextDbOracleModels.DbOracle.Table]]:
        """Discover Oracle tables using domain service."""
        if schema_name:
            discovery_service = FlextOracleDiscoveryService(
                oracle_api=self._oracle_api,
                schema_name=schema_name,
            )
            return discovery_service.execute()
        return self._discovery_service.execute()

    @override
    def execute(self) -> r[Sequence[FlextDbOracleModels.DbOracle.Table]]:
        """Execute Oracle tap service - discover tables."""
        return self._discovery_service.execute()

    def get_filtered_tables(self) -> r[Sequence[str]]:
        """Get filtered table list using domain service."""
        return self._table_filter_service.execute()

    def get_health_status(self) -> r[bool]:
        """Get service health status using connection test."""
        return self._connection_test_service.execute()

    def get_tap_status(self) -> r[bool]:
        """Get Oracle tap status by testing connection."""
        try:
            connection_test_result = self._connection_test_service.execute()
            if connection_test_result.is_success:
                logger.info("Oracle tap status: healthy")
                return r[bool].ok(value=True)
            logger.warning(
                f"Oracle tap status check failed: {connection_test_result.error}",
            )
            return r[bool].fail(
                f"Connection test failed: {connection_test_result.error}",
            )
        except (ValueError, TypeError, KeyError, AttributeError, OSError) as e:
            logger.exception("Failed to get tap status")
            return r[bool].fail(f"Status check failed: {e}")

    def initialize_tap(self) -> r[bool]:
        """Initialize Oracle tap by testing connection and discovering tables."""
        try:
            logger.info("Initializing Oracle tap service")
            connection_result = self.test_oracle_connection()
            if connection_result.is_failure:
                logger.error(
                    f"Oracle connection test failed: {connection_result.error}",
                )
                return r[bool].fail(
                    f"Connection test failed: {connection_result.error}",
                )
            tables_result = self.get_filtered_tables()
            if tables_result.is_failure:
                logger.error(f"Table discovery failed: {tables_result.error}")
                return r[bool].fail(f"Table discovery failed: {tables_result.error}")
            logger.info("Oracle tap initialization completed successfully")
            return r[bool].ok(value=True)
        except (ValueError, TypeError, KeyError, AttributeError, OSError) as e:
            logger.exception("Oracle tap initialization failed")
            error_msg = f"Initialization failed: {e}"
            return r[bool].fail(error_msg)

    def test_oracle_connection(self) -> r[bool]:
        """Test Oracle connection using domain service."""
        return self._connection_test_service.execute()

    def validate_service(self) -> r[bool]:
        """Validate service using connection test."""
        return self._connection_test_service.execute()


def create_oracle_tap_service(
    config: FlextTapOracleSettings,
) -> r[FlextOracleTapService]:
    """Create Oracle tap service using COMPOSITION.

    Args:
    config: Oracle tap configuration

    Returns:
    r containing Oracle tap service

    """
    try:
        service = FlextOracleTapService(config=config)
        return r[FlextOracleTapService].ok(service)
    except (ValueError, TypeError, KeyError, AttributeError, OSError) as e:
        return r[FlextOracleTapService].fail(f"Oracle tap service creation failed: {e}")


def create_oracle_discovery_service(
    oracle_api: FlextDbOracleApi,
    schema_name: str | None = None,
) -> r[FlextOracleDiscoveryService]:
    """Create Oracle discovery service.

    Args:
    oracle_api: Oracle database API instance
    schema_name: Optional schema name for discovery

    Returns:
    r containing Oracle discovery service

    """
    try:
        service = FlextOracleDiscoveryService(
            oracle_api=oracle_api,
            schema_name=schema_name,
        )
        return r[FlextOracleDiscoveryService].ok(service)
    except (ValueError, TypeError, KeyError, AttributeError, OSError) as e:
        return r[FlextOracleDiscoveryService].fail(
            f"Oracle discovery service creation failed: {e}",
        )


__all__: Sequence[str] = [
    "FlextOracleConnectionTestService",
    "FlextOracleDiscoveryService",
    "FlextOracleTableFilterService",
    "FlextOracleTapService",
    "create_oracle_discovery_service",
    "create_oracle_tap_service",
]
