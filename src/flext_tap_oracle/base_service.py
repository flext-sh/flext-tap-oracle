"""Oracle Tap Service - COMPOSITION using FlextMeltanoTapService + Domain Services.

Este módulo implementa Oracle tap service usando COMPOSIÇÃO correta com:
- FlextMeltanoTapService (do flext-meltano) para funcionalidade base
- FlextDomainService[T] (do flext-core) para lógica Oracle-específica

PRINCÍPIO: COMPOSIÇÃO > HERANÇA. Usar bases existentes corretamente.

Copyright (c) 2025 FLEXT Contributors
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from typing import TYPE_CHECKING

# Import CORRECT base service from flext-meltano + logger + FlextResult from flext-core
from flext_core import FlextLoggerFactory, FlextResult

# Import Oracle infrastructure - NEVER duplicate
from flext_db_oracle import FlextDbOracleApi
from flext_meltano import FlextMeltanoTapService

# Import our CORRECT domain services
from flext_tap_oracle.domain_services import (
    FlextOracleConnectionTestService,
    FlextOracleDiscoveryService,
    FlextOracleTableFilterService,
)

logger = FlextLoggerFactory.get_logger(__name__)

if TYPE_CHECKING:
    from flext_db_oracle import FlextDbOracleTable

    from flext_tap_oracle.config import FlextOracleTapConfig


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
        schema_name = getattr(oracle_config, "schema_name", None) or oracle_config.service_name
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


# Factory function using dependency injection pattern
def create_oracle_tap_service(
    config: FlextOracleTapConfig,
) -> FlextResult[FlextOracleTapService]:
    """Factory to create Oracle tap service using COMPOSITION.

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


__all__: list[str] = [
    "FlextOracleTapService",  # RENAMED: Remove "Base" - it's not a base class anymore
    "create_oracle_tap_service",
]
