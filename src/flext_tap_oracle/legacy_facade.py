"""LEGACY FACADE - Temporary compatibility layer during refactoring.

⚠️ DEPRECATED: Esta facade é TEMPORÁRIA durante a refatoração.
Use FlextOracleTapService diretamente da base_service.py

SERÁ REMOVIDO após validação completa da nova implementação.

Copyright (c) 2025 FLEXT Contributors
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

import warnings
from typing import TYPE_CHECKING

from flext_tap_oracle.base_service import FlextOracleTapService

if TYPE_CHECKING:
    from flext_core import FlextResult
    from flext_db_oracle import FlextDbOracleTable

    from flext_tap_oracle.config import FlextOracleTapConfig


class FlextOracleTapBaseService:
    """⚠️ DEPRECATED: Legacy facade for FlextOracleTapService.

    Esta classe é uma FACADE TEMPORÁRIA para manter compatibilidade
    durante a refatoração. Use FlextOracleTapService diretamente.

    SERÁ REMOVIDO após validação.
    """

    def __init__(self, config: FlextOracleTapConfig) -> None:
        """Initialize legacy facade with deprecation warning."""
        warnings.warn(
            "FlextOracleTapBaseService is deprecated. "
            "Use FlextOracleTapService directly from base_service",
            DeprecationWarning,
            stacklevel=2
        )
        # DELEGATION: Delegate to new implementation
        self._service = FlextOracleTapService(config)

    # FACADE: Delegate all methods to new service
    @property
    def config(self) -> FlextOracleTapConfig:
        """Get Oracle tap configuration."""
        return self._service.config

    @property
    def oracle_api(self) -> object:
        """Get Oracle API."""
        return self._service.oracle_api

    def validate_service(self) -> FlextResult[bool]:
        """Validate service."""
        return self._service.validate_service()

    def get_health_status(self) -> FlextResult[dict[str, object]]:
        """Get health status."""
        return self._service.get_health_status()

    def discover_catalog(self) -> FlextResult[dict[str, object]]:
        """Discover catalog."""
        return self._service.discover_catalog()

    def discover_oracle_tables(
        self,
        schema_name: str | None = None,
    ) -> FlextResult[list[FlextDbOracleTable]]:
        """Discover Oracle tables."""
        return self._service.discover_oracle_tables(schema_name)

    def test_oracle_connection(self) -> FlextResult[bool]:
        """Test Oracle connection."""
        return self._service.test_oracle_connection()

    def get_filtered_tables(self) -> FlextResult[list[str]]:
        """Get filtered table list."""
        return self._service.get_filtered_tables()


__all__: list[str] = [
    "FlextOracleTapBaseService",  # TEMPORARY FACADE - TO BE REMOVED
]
