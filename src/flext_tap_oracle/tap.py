"""Oracle Database Tap Implementation using FLEXT-Meltano Generic Interfaces.

This module implements Oracle Database specific configuration and discovery
using the generic Tap and Stream classes from flext-meltano.
"""

from __future__ import annotations

# Import generic interfaces from flext-meltano
from flext_meltano import Tap, singer_typing as th

from flext_core import get_logger
from flext_db_oracle import FlextDbOracleApi

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
    config_jsonschema = th.PropertiesList(
        # Basic Oracle connection
        th.Property(
            "host", th.StringType, required=True, description="Oracle database host",
        ),
        th.Property(
            "port", th.IntegerType, default=1521, description="Oracle database port",
        ),
        th.Property("service_name", th.StringType, description="Oracle service name"),
        th.Property(
            "username", th.StringType, required=True, description="Oracle username",
        ),
        th.Property(
            "password",
            th.StringType,
            secret=True,
            required=True,
            description="Oracle password",
        ),
        th.Property("schema_name", th.StringType, description="Oracle schema name"),
        # Performance settings
        th.Property(
            "batch_size",
            th.IntegerType,
            default=10000,
            description="Batch size for data extraction",
        ),
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
        if self._typed_config is None:
            self._typed_config = TapOracleConfig(**self.config)
        return self._typed_config

    @property
    def oracle_api(self) -> FlextDbOracleApi:
        """Get Oracle database API."""
        if self._oracle_api is None:
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
        """Get list of tables to process using real Oracle API."""
        # If specific tables configured, use those
        if self.typed_config.tables:
            return list(self.typed_config.tables)

        # Otherwise discover all tables in schema using real Oracle API
        try:
            connected_api = self.oracle_api.connect()
            schema_name = self.typed_config.schema_name

            # Use real Oracle API to get table names
            result = connected_api.get_tables(schema=schema_name)

            if result.is_success and result.data:
                tables = result.data
                logger.info(
                    "Discovered %d tables in Oracle schema %s",
                    len(tables),
                    schema_name or "default",
                )
                return tables
            logger.warning(
                "No tables found in Oracle schema %s: %s", schema_name, result.error,
            )
            return []

        except Exception:
            logger.exception("Failed to discover Oracle tables")
            return []

    def _get_table_schema(self, table_name: str) -> dict[str, object]:
        """Get schema for a specific table using real Oracle API."""
        try:
            connected_api = self.oracle_api.connect()
            schema_name = self.typed_config.schema_name

            # Get column information from Oracle using real API
            result = connected_api.get_columns(table_name, schema=schema_name)

            if result.is_success and result.data:
                properties = {}

                # Convert Oracle column info to Singer schema format
                for column_info in result.data:
                    column_name = column_info.get("column_name", "unknown")
                    oracle_type = column_info.get("data_type", "VARCHAR2")
                    is_nullable = column_info.get("nullable", "Y") == "Y"

                    # Map Oracle types to Singer types
                    singer_type = self._map_oracle_type_to_singer(oracle_type)

                    properties[column_name] = {
                        "type": singer_type
                        if not is_nullable
                        else ["null", singer_type],
                    }

                return {
                    "type": "object",
                    "properties": properties,
                }
            logger.warning(
                "Could not get schema for table %s: %s", table_name, result.error,
            )
            # Return minimal schema as fallback
            return {
                "type": "object",
                "properties": {
                    "data": {"type": "string"},
                },
            }

        except Exception:
            logger.exception("Failed to get schema for table %s", table_name)
            # Return minimal schema as fallback
            return {
                "type": "object",
                "properties": {
                    "data": {"type": "string"},
                },
            }

    def _map_oracle_type_to_singer(self, oracle_type: str) -> str:
        """Map Oracle data types to Singer types."""
        oracle_type_upper = oracle_type.upper()

        if oracle_type_upper.startswith(("NUMBER", "DECIMAL", "NUMERIC")):
            return "number"
        if oracle_type_upper.startswith(
            ("VARCHAR", "CHAR", "CLOB", "NVARCHAR", "NCHAR"),
        ):
            return "string"
        if oracle_type_upper.startswith("DATE"):
            return "string"  # Date as ISO string
        if oracle_type_upper.startswith("TIMESTAMP"):
            return "string"  # Timestamp as ISO string
        if oracle_type_upper.startswith(("BLOB", "RAW")):
            return "string"  # Binary as base64 string
        return "string"  # Default to string for unknown types

    def test_connection(self) -> bool:
        """Test Oracle database connection."""
        try:
            # Test connection using oracle_api
            result = self.oracle_api.test_connection()
        except Exception:
            logger.exception("Oracle connection test failed")
            return False
        else:
            return result.is_success


# CLI entry point
def cli() -> None:
    """Command line interface for Oracle tap."""
    TapOracle.cli()


if __name__ == "__main__":
    cli()
