"""Oracle Tap Domain Services - USING FlextDomainService[T] from flext-core.

Este módulo implementa serviços de domínio Oracle usando CORRETAMENTE o
FlextDomainService[T] do flext-core, seguindo DDD e SOLID principles.

PRINCÍPIO: USAR bases do flext-core, NÃO duplicar funcionalidades.

Copyright (c) 2025 FLEXT Contributors
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from typing import TYPE_CHECKING

# Import CORRECT domain service base from flext-core
from flext_core import FlextDomainService, FlextLoggerFactory, FlextResult

# Import Oracle infrastructure - NEVER duplicate
from flext_db_oracle import (
    FlextDbOracleApi,
    FlextDbOracleMetadataManager,
    FlextDbOracleTable,
)

logger = FlextLoggerFactory.get_logger(__name__)

if TYPE_CHECKING:
    from flext_tap_oracle.config import FlextOracleTapConfig


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
                logger.info("Using configured table filter: %s", tap_configuration.tables_filter)
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


__all__: list[str] = [
    "FlextOracleConnectionTestService",
    "FlextOracleDiscoveryService",
    "FlextOracleTableFilterService",
]
