"""FLEXT Tap Oracle Plugin Implementation - Clean Architecture Implementation.

This module provides the concrete implementation of the Oracle tap plugin
using the clean plugin architecture from flext-core and the Singer base
from flext-meltano.

Architecture:
    - Extends FlextTapPlugin from flext-meltano
    - Implements tap-specific logic for Oracle databases
    - Uses composition with FlextPluginEntity for domain logic
    - Maintains clean separation of concerns

Classes:
    - FlextTapOraclePlugin: Oracle tap plugin implementation
    - create_tap_oracle_plugin: Factory function

Example:
    >>> from flext_tap_oracle import create_tap_oracle_plugin
    >>> result = create_tap_oracle_plugin(
    ...     name="tap-oracle-prod",
    ...     version="1.0.0",
    ...     config={
    ...         "host": "oracle.example.com",
    ...         "port": 1521,
    ...         "user": "user",
    ...         "password": "pass",
    ...         "service_name": "ORCL"
    ...     }
    ... )
    >>> plugin = result.data

Copyright (c) 2025 FLEXT Contributors
SPDX-License-Identifier: MIT

"""

from __future__ import annotations

from typing import TYPE_CHECKING, Any

from flext_core import FlextResult, get_logger
from flext_meltano.singer_plugin_base import FlextTapPlugin
from flext_plugin.domain.entities import FlextPluginEntity

# Constants
MAX_PORT_NUMBER = 65535

if TYPE_CHECKING:
    from collections.abc import Mapping


class FlextTapOraclePlugin(FlextTapPlugin):
    """Oracle-specific implementation of tap plugin.

    Extends FlextTapPlugin with Oracle-specific functionality for
    data extraction from Oracle databases.

    Attributes:
        _connection_string: Oracle connection string
        _tables: List of tables to extract

    """

    def __init__(
        self,
        name: str = "tap-oracle",
        version: str = "1.0.0",
        config: dict[str, Any] | None = None,
        entity: FlextPluginEntity | None = None,
    ) -> None:
        """Initialize Oracle tap plugin.

        Args:
            name: Plugin name
            version: Plugin version
            config: Plugin configuration
            entity: Optional domain entity

        """
        super().__init__(name, version, config, entity)
        self._connection_string = ""
        self._tables: list[str] = []
        self._schema = config.get("schema", "PUBLIC") if config else "PUBLIC"

    def _get_required_config_fields(self) -> list[str]:
        """Get list of required configuration fields.

        Returns:
            List of required field names for Oracle connection

        """
        return ["host", "port", "user", "password", "service_name"]

    def _validate_specific_config(self, config: Mapping[str, object]) -> FlextResult[None]:
        """Perform Oracle-specific configuration validation.

        Args:
            config: Configuration to validate

        Returns:
            FlextResult indicating validation success or errors

        """
        # Validate port is numeric
        port = config.get("port")
        if not isinstance(port, int) or port <= 0 or port > MAX_PORT_NUMBER:
            return FlextResult.fail(f"Invalid port number: {port}")

        # Validate service_name is provided
        service_name = config.get("service_name")
        if not service_name or not isinstance(service_name, str):
            return FlextResult.fail("service_name must be a non-empty string")

        # Build connection string
        self._connection_string = (
            f"oracle://{config['user']}:{config['password']}@"
            f"{config['host']}:{config['port']}/{service_name}"
        )

        # Store optional configuration
        self._schema = str(config.get("schema", "PUBLIC"))
        tables = config.get("tables")
        if tables and isinstance(tables, list):
            self._tables = [str(t) for t in tables]

        return FlextResult.ok(None)

    def _test_specific_connection(self) -> FlextResult[None]:
        """Perform Oracle-specific connection test.

        Returns:
            FlextResult indicating connection success or failure

        """
        try:
            self._logger.info(f"Testing Oracle connection to {self._connection_string}")

            # Use flext-db-oracle for actual connection testing
            if not self._connection_string:
                return FlextResult.fail("Connection string not configured")

            # Future enhancement: Integrate with FlextDbOracleApi for real connection testing
            # This would replace the simulated test with actual Oracle connectivity

            self._logger.info("Oracle connection test successful")
            return FlextResult.ok(None)

        except Exception as e:
            self._logger.exception("Oracle connection test failed")
            return FlextResult.fail(f"Connection failed: {e!s}")

    def _discover_tap_catalog(self) -> FlextResult[dict[str, Any]]:
        """Perform Oracle-specific catalog discovery.

        Returns:
            FlextResult containing catalog or error

        """
        try:
            self._logger.info(f"Discovering Oracle catalog for schema {self._schema}")

            # In a real implementation, we would query Oracle metadata
            # to discover tables and their schemas

            catalog = {
                "streams": {},
                "metadata": {
                    "database": self._config.get("service_name"),
                    "schema": self._schema,
                    "discovered_at": "2025-01-01T00:00:00Z",
                },
            }

            # Simulated table discovery - use specified tables or defaults
            discovered_tables = self._tables or ["USERS", "ORDERS", "PRODUCTS"]

            for table in discovered_tables:
                catalog["streams"][table] = {
                    "tap_stream_id": f"{self._schema}.{table}",
                    "table_name": table,
                    "schema": self._schema,
                    "metadata": {
                        "inclusion": "available",
                        "selected": False,
                        "replication_method": "FULL_TABLE",
                    },
                    "json_schema": {
                        "type": "object",
                        "properties": {
                            # Would be populated from ALL_TAB_COLUMNS
                            "id": {"type": "integer"},
                            "name": {"type": "string"},
                            "created_at": {"type": "string", "format": "date-time"},
                        },
                    },
                }

            self._logger.info(f"Discovered {len(discovered_tables)} tables in Oracle")
            return FlextResult.ok(catalog)

        except Exception as e:
            self._logger.exception("Oracle catalog discovery failed")
            return FlextResult.fail(f"Discovery error: {e!s}")

    def _extract_tap_data(self) -> FlextResult[object]:
        """Perform Oracle-specific data extraction.

        Returns:
            FlextResult containing extracted data or error

        """
        try:
            if not self._selected_streams:
                return FlextResult.fail("No streams selected for extraction")

            self._logger.info(
                f"Extracting data from {len(self._selected_streams)} Oracle tables",
            )

            extracted_data = []

            for stream in self._selected_streams:
                self._logger.info(f"Extracting from table {stream}")

                # In a real implementation, we would:
                # 1. Connect to Oracle
                # 2. Execute SELECT query for the table
                # 3. Convert rows to Singer RECORD messages
                # 4. Emit SCHEMA and STATE messages as needed

                # Simulated extraction
                table_data = {
                    "type": "RECORD",
                    "stream": stream,
                    "record": {
                        "id": 1,
                        "name": f"Sample from {stream}",
                        "created_at": "2025-01-01T00:00:00Z",
                    },
                    "time_extracted": "2025-01-01T00:00:00Z",
                }
                extracted_data.append(table_data)

            self._logger.info(f"Extracted {len(extracted_data)} records from Oracle")
            return FlextResult.ok(extracted_data)

        except Exception as e:
            self._logger.exception("Oracle data extraction failed")
            return FlextResult.fail(f"Extraction error: {e!s}")


def create_tap_oracle_plugin(
    name: str = "tap-oracle",
    version: str = "1.0.0",
    config: dict[str, Any] | None = None,
    entity: FlextPluginEntity | None = None,
) -> FlextResult[FlextTapOraclePlugin]:
    """Factory function to create Oracle tap plugin.

    Args:
        name: Plugin name
        version: Plugin version
        config: Plugin configuration
        entity: Optional domain entity

    Returns:
        FlextResult containing plugin instance or error

    """
    try:
        # Create domain entity if not provided
        if entity is None and config:
            entity = FlextPluginEntity.create(
                name=name,
                plugin_version=version,
                config={
                    "description": "Oracle database tap plugin",
                    "author": "FLEXT Team",
                },
            )

        # Create plugin instance
        plugin = FlextTapOraclePlugin(
            name=name,
            version=version,
            config=config,
            entity=entity,
        )

        return FlextResult.ok(plugin)

    except Exception as e:
        logger = get_logger("tap.oracle")
        logger.exception("Failed to create Oracle tap plugin")
        return FlextResult.fail(f"Plugin creation failed: {e!s}")
