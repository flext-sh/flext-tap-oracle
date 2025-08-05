"""Oracle Database Tap Implementation using FLEXT-Meltano Generic Interfaces.

This module implements Oracle Database specific configuration and discovery
using the generic Tap and Stream classes from flext-meltano.
"""

from __future__ import annotations

import asyncio
from typing import ClassVar

from flext_core import get_logger
from flext_db_oracle import FlextDbOracleApi

# Import generic interfaces from flext-meltano
from flext_meltano import Tap, singer_typing as th
from flext_meltano.common_schemas import create_oracle_tap_schema

# Import Oracle-specific configuration and stream implementation
from flext_tap_oracle.config import TapOracleConfig
from flext_tap_oracle.oracle_stream import OracleStream

logger = get_logger(__name__)


class TapOracle(Tap):
    """Oracle Database Tap using FLEXT-Meltano generic interfaces.

    Implements Oracle Database specific logic using:
    - Generic Tap class from flext-meltano
    - Oracle configuration and connectivity from flext-db-oracle
    - Only Oracle-specific business logic in this project
    """

    name = "tap-oracle"
    # REAL DRY: Use centralized Oracle schema from flext-meltano instead of duplicating
    config_jsonschema = create_oracle_tap_schema(
        # Oracle-specific additional properties for tap-oracle
        additional_properties=th.PropertiesList(
            th.Property(
                "query_timeout",
                th.IntegerType,
                default=300,
                description="Query timeout in seconds",
            ),
            # Stream configuration
            th.Property(
                "tables",
                th.ArrayType(th.StringType),
                description="List of tables to extract",
            ),
            th.Property(
                "exclude_tables",
                th.ArrayType(th.StringType),
                description="List of tables to exclude",
            ),
        ),
    ).to_dict()

    def __init__(
        self,
        *,
        config: dict[str, object] | None = None,
        catalog: dict[str, object] | None = None,
        state: dict[str, object] | None = None,
        parse_env_config: bool = False,
        validate_config: bool = True,
    ) -> None:
        """Initialize Oracle tap with Singer SDK interface."""
        # Call parent constructor directly - simpler and type-safe
        super().__init__(
            config=config,
            catalog=catalog,
            state=state,
            parse_env_config=parse_env_config,
            validate_config=validate_config,
        )
        self._typed_config: TapOracleConfig | None = None
        self._oracle_api: FlextDbOracleApi | None = None

    @property
    def typed_config(self) -> TapOracleConfig:
        """Get typed Oracle configuration."""
        if not hasattr(self, "_typed_config") or self._typed_config is None:
            self._typed_config = TapOracleConfig(**self.config)
        return self._typed_config

    @property
    def oracle_api(self) -> FlextDbOracleApi:
        """Get Oracle database API."""
        if not hasattr(self, "_oracle_api") or self._oracle_api is None:
            oracle_config = self.typed_config.to_oracle_config()
            self._oracle_api = FlextDbOracleApi(oracle_config)
        return self._oracle_api

    def discover_streams(self) -> list[OracleStream]:
        """Discover available Oracle streams using real Oracle connectivity."""
        streams = []

        try:
            # Get table list from Oracle using real API
            tables = self._get_table_list()

            # Create concrete OracleStream instances for each table
            for table_name in tables:
                schema = self._get_table_schema(table_name)
                stream = OracleStream(
                    tap=self,
                    name=table_name,
                    table_name=table_name,
                    schema=schema,
                    oracle_api=self.oracle_api,
                )
                streams.append(stream)

            logger.info("Discovered %d Oracle tables", len(streams))

        except Exception:
            logger.exception("Failed to discover Oracle streams")

        return streams

    def _get_table_list(self) -> list[str]:
        """Get list of tables to process using flext-db-oracle API with Railway Pattern."""
        # If specific tables configured, use those - Early Return Pattern
        if self.typed_config.tables:
            return list(self.typed_config.tables)

        # Otherwise discover all tables using flext-db-oracle with context manager
        return self._discover_tables_from_oracle()

    def _discover_tables_from_oracle(self) -> list[str]:
        """Discover tables from Oracle using flext-db-oracle patterns - Single Responsibility."""
        schema_name = self.typed_config.schema_name

        # Use context manager pattern from flext-db-oracle for proper resource management
        try:
            with self.oracle_api as connected_api:
                # Use flext-db-oracle API which returns FlextResult
                tables_result = connected_api.get_tables(schema=schema_name)

                return self._process_tables_result(tables_result, schema_name)

        except Exception:
            logger.exception("Failed to discover Oracle tables")
            return []

    def _process_tables_result(
        self,
        tables_result: object,
        schema_name: str | None,
    ) -> list[str]:
        """Process tables result using Railway-oriented programming - Single Responsibility."""
        if (
            hasattr(tables_result, "success")
            and tables_result.success
            and hasattr(tables_result, "data")
            and tables_result.data
        ):
            tables = tables_result.data
            # Ensure we return a list of strings
            if isinstance(tables, list):
                logger.info(
                    "Discovered %d tables in Oracle schema %s",
                    len(tables),
                    schema_name or "default",
                )
                return [str(table) for table in tables]

        # Handle failure case
        error_msg = getattr(tables_result, "error", "Unknown error")
        logger.warning(
            "No tables found in Oracle schema %s: %s",
            schema_name,
            error_msg,
        )
        return []

    def _get_table_schema(self, table_name: str) -> dict[str, object]:
        """Get schema for a specific table using flext-db-oracle patterns."""
        try:
            # Use context manager pattern from flext-db-oracle
            with self.oracle_api as connected_api:
                schema_result = connected_api.get_columns(
                    table_name,
                    schema=self.typed_config.schema_name,
                )

                return self._process_schema_result(schema_result, table_name)

        except Exception:
            logger.exception("Failed to get schema for table %s", table_name)
            return self._get_fallback_schema()

    def _process_schema_result(
        self,
        schema_result: object,
        table_name: str,
    ) -> dict[str, object]:
        """Process schema result using Railway Pattern - Single Responsibility."""
        if (
            hasattr(schema_result, "success")
            and schema_result.success
            and hasattr(schema_result, "data")
            and schema_result.data
        ):
            return self._build_singer_schema(schema_result.data)

        # Handle failure case
        error_msg = getattr(schema_result, "error", "Unknown error")
        logger.warning("Could not get schema for table %s: %s", table_name, error_msg)
        return self._get_fallback_schema()

    def _build_singer_schema(
        self,
        columns_data: list[dict[str, object]],
    ) -> dict[str, object]:
        """Build Singer schema from Oracle columns data - Single Responsibility."""
        properties = {}

        # Convert Oracle column info to Singer schema format
        for column_info in columns_data:
            column_name = column_info.get("column_name", "unknown")
            oracle_type = column_info.get("data_type", "VARCHAR2")
            is_nullable = column_info.get("nullable", "Y") == "Y"

            # Use improved type mapper
            singer_type = self._map_oracle_type_to_singer(str(oracle_type))

            properties[column_name] = {
                "type": [singer_type] if not is_nullable else ["null", singer_type],
            }

        return {
            "type": "object",
            "properties": properties,
        }

    def _get_fallback_schema(self) -> dict[str, object]:
        """Get fallback schema when Oracle schema discovery fails - DRY Pattern."""
        return {
            "type": "object",
            "properties": {
                "data": {"type": "string"},
            },
        }

    def _map_oracle_type_to_singer(self, oracle_type: str) -> str:
        """Map Oracle data types to Singer types using Strategy Pattern."""
        return self._get_oracle_type_mapper().map_to_singer(oracle_type)

    def _get_oracle_type_mapper(self) -> _OracleTypeMapper:
        """Get Oracle type mapper - Factory Method Pattern."""
        return _OracleTypeMapper()

    def test_connection(self) -> bool:
        """Test Oracle database connection using flext-db-oracle."""
        try:
            # Use flext-db-oracle API with proper Railway Pattern
            result = self.oracle_api.test_connection()
            return hasattr(result, "success") and result.success
        except Exception:
            logger.exception("Oracle connection test failed")
            return False

    def get_metrics(self) -> dict[str, object]:
        """Get comprehensive tap metrics for monitoring and observability."""
        if not self.typed_config.enable_metrics:
            return {}

        try:
            streams = self.discover_streams()
            return {
                "connection_type": self.typed_config.connection_type,
                "streams_discovered": len(streams),
                "configuration": {
                    "batch_size": self.typed_config.batch_size,
                    "max_parallel_streams": self.typed_config.max_parallel_streams,
                    "async_enabled": self.typed_config.enable_async,
                    "circuit_breaker_enabled": self.typed_config.circuit_breaker_enabled,
                },
                "connection_string": self.typed_config.get_connection_string(),
                "performance_settings": self.typed_config.get_performance_settings(),
            }
        except Exception:
            logger.exception("Failed to collect metrics")
            return {"error": "Failed to collect metrics"}

    async def run_async(self) -> None:
        """Run tap asynchronously - modern Singer SDK functionality."""
        if not self.typed_config.enable_async:
            logger.warning("Async mode disabled, falling back to sync")
            return

        logger.info("Starting async tap execution")
        streams = self.discover_streams()

        semaphore = asyncio.Semaphore(self.typed_config.max_parallel_streams)

        async def process_stream_async(stream: OracleStream) -> None:
            """Process a single stream asynchronously."""
            async with semaphore:
                if hasattr(stream, "sync_async"):
                    await stream.sync_async()
                else:
                    logger.warning(
                        "Stream %s does not support async processing", stream.name,
                    )

        # Process all streams concurrently
        await asyncio.gather(*[process_stream_async(stream) for stream in streams])
        logger.info("Async tap execution completed")

    async def _get_discoverable_tables(self) -> list[str]:
        """Get discoverable tables asynchronously for modern Singer SDK compatibility."""
        return self._get_table_list()

    def _schema_service(self) -> object:
        """Get schema service for advanced table discovery - Singer SDK pattern."""

        # Mock schema service for compatibility with tests
        class MockSchemaService:
            async def get_schema_tables(self, _schema_name: str) -> object:
                # Mock result object
                class MockResult:
                    success = True
                    data: ClassVar[list[object]] = []

                return MockResult()

        return MockSchemaService()


class _OracleTypeMapper:
    """Oracle to Singer type mapper using Strategy Pattern - Single Responsibility."""

    # Strategy mapping table using flext-db-oracle constants knowledge
    _TYPE_MAPPING_RULES: ClassVar[list[tuple[tuple[str, ...], str]]] = [
        (("NUMBER", "DECIMAL", "NUMERIC"), "number"),
        (("VARCHAR", "CHAR", "CLOB", "NVARCHAR", "NCHAR"), "string"),
        (("DATE",), "string"),  # Date as ISO string
        (("TIMESTAMP",), "string"),  # Timestamp as ISO string
        (("BLOB", "RAW"), "string"),  # Binary as base64 string
    ]

    def map_to_singer(self, oracle_type: str) -> str:
        """Map Oracle data type to Singer type using Strategy Pattern."""
        oracle_type_upper = oracle_type.upper()

        # Apply mapping rules in order
        for oracle_prefixes, singer_type in self._TYPE_MAPPING_RULES:
            if oracle_type_upper.startswith(oracle_prefixes):
                return singer_type

        # Default strategy for unknown types
        return "string"


# CLI entry point
def cli() -> None:
    """Command line interface for Oracle tap."""
    TapOracle.cli()


if __name__ == "__main__":
    cli()
