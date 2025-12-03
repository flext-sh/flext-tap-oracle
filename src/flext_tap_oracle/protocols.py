"""Singer Oracle tap protocols for FLEXT ecosystem."""

from typing import Protocol, runtime_checkable

from flext_core import FlextResult, p


class FlextMeltanoTapOracleProtocols:
    """Singer Tap Oracle protocols with explicit re-exports from p foundation.

    Domain Extension Pattern (Phase 3):
    - Explicit re-export of foundation protocols (not inheritance)
    - Domain-specific protocols organized in TapOracle namespace
    - 100% backward compatibility through aliases
    """

    class TapOracle:
        """Singer Tap Oracle domain protocols for Oracle database extraction."""

        @runtime_checkable
        class OracleConnectionProtocol(p.Service, Protocol):
            """Protocol for Oracle database connection management."""

            def connect(self, config: dict[str, object]) -> FlextResult[object]:
                """Connect to Oracle database with provided configuration."""

            def disconnect(self) -> FlextResult[None]:
                """Disconnect from Oracle database."""

            def test_connection(self, config: dict[str, object]) -> FlextResult[bool]:
                """Test Oracle database connection with validation."""

        @runtime_checkable
        class SchemaDiscoveryProtocol(p.Service, Protocol):
            """Protocol for Oracle schema discovery."""

            def discover_schemas(
                self, config: dict[str, object]
            ) -> FlextResult[list[dict[str, object]]]:
                """Discover accessible Oracle schemas."""

            def discover_tables(
                self, schema: str
            ) -> FlextResult[list[dict[str, object]]]:
                """Discover Oracle tables in specified schema."""

            def get_table_metadata(
                self, schema: str, table: str
            ) -> FlextResult[dict[str, object]]:
                """Get Oracle table metadata and column definitions."""

        @runtime_checkable
        class DataExtractionProtocol(p.Service, Protocol):
            """Protocol for Oracle data extraction."""

            def extract_table_data(
                self, table: str, config: dict[str, object]
            ) -> FlextResult[list[dict[str, object]]]:
                """Extract all data from Oracle table."""

            def extract_incremental(
                self, table: str, state: dict[str, object]
            ) -> FlextResult[list[dict[str, object]]]:
                """Extract incremental data from Oracle table using state."""

        @runtime_checkable
        class TypeMappingProtocol(p.Service, Protocol):
            """Protocol for Oracle to Singer type mapping."""

            def map_oracle_type(self, oracle_type: str) -> FlextResult[str]:
                """Map Oracle data type to Singer type."""

            def convert_value(
                self, value: object, oracle_type: str
            ) -> FlextResult[object]:
                """Convert Oracle value to Singer-compatible format."""

        @runtime_checkable
        class StreamGenerationProtocol(p.Service, Protocol):
            """Protocol for Singer stream generation."""

            def generate_catalog(
                self, config: dict[str, object]
            ) -> FlextResult[dict[str, object]]:
                """Generate Singer catalog from Oracle schema."""

            def sync_stream(
                self, stream: str, state: dict[str, object]
            ) -> FlextResult[dict[str, object]]:
                """Sync Singer stream from Oracle table."""

        @runtime_checkable
        class PerformanceProtocol(p.Service, Protocol):
            """Protocol for Oracle extraction performance."""

            def optimize_query(self, query: str) -> FlextResult[str]:
                """Optimize Oracle query for performance."""

            def configure_batch_size(self, size: int) -> FlextResult[bool]:
                """Configure extraction batch size."""

        @runtime_checkable
        class ValidationProtocol(p.Service, Protocol):
            """Protocol for Oracle data validation."""

            def validate_config(self, config: dict[str, object]) -> FlextResult[bool]:
                """Validate tap configuration."""

            def validate_schema(self, schema: dict[str, object]) -> FlextResult[bool]:
                """Validate Oracle schema definition."""

        @runtime_checkable
        class MonitoringProtocol(p.Service, Protocol):
            """Protocol for Oracle extraction monitoring."""

            def track_progress(self, table: str, records: int) -> FlextResult[None]:
                """Track Oracle table extraction progress."""

            def get_statistics(self) -> FlextResult[dict[str, object]]:
                """Get extraction statistics."""

    OracleConnectionProtocol = TapOracle.OracleConnectionProtocol
    SchemaDiscoveryProtocol = TapOracle.SchemaDiscoveryProtocol
    DataExtractionProtocol = TapOracle.DataExtractionProtocol
    TypeMappingProtocol = TapOracle.TypeMappingProtocol
    StreamGenerationProtocol = TapOracle.StreamGenerationProtocol
    PerformanceProtocol = TapOracle.PerformanceProtocol
    ValidationProtocol = TapOracle.ValidationProtocol
    MonitoringProtocol = TapOracle.MonitoringProtocol

    TapOracleConnectionProtocol = TapOracle.OracleConnectionProtocol
    TapOracleSchemaDiscoveryProtocol = TapOracle.SchemaDiscoveryProtocol
    TapOracleDataExtractionProtocol = TapOracle.DataExtractionProtocol
    TapOracleTypeMappingProtocol = TapOracle.TypeMappingProtocol
    TapOracleStreamGenerationProtocol = TapOracle.StreamGenerationProtocol
    TapOraclePerformanceProtocol = TapOracle.PerformanceProtocol
    TapOracleValidationProtocol = TapOracle.ValidationProtocol
    TapOracleMonitoringProtocol = TapOracle.MonitoringProtocol


__all__ = [
    "FlextMeltanoTapOracleProtocols",
]
