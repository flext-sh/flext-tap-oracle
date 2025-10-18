"""Singer Oracle tap protocols for FLEXT ecosystem."""

from typing import Protocol, runtime_checkable

from flext_core import FlextProtocols, FlextResult


class FlextMeltanoTapOracleProtocols:
    """Singer Tap Oracle protocols with explicit re-exports from FlextProtocols foundation.

    Domain Extension Pattern (Phase 3):
    - Explicit re-export of foundation protocols (not inheritance)
    - Domain-specific protocols organized in TapOracle namespace
    - 100% backward compatibility through aliases
    """

    class TapOracle:
        """Singer Tap Oracle domain protocols for Oracle database extraction."""

        @runtime_checkable
        class OracleConnectionProtocol(FlextProtocols.Service, Protocol):
            """Protocol for Oracle database connection management."""

            def connect(self, config: dict[str, object]) -> FlextResult[object]: ...
            def disconnect(self) -> FlextResult[None]: ...
            def test_connection(
                self, config: dict[str, object]
            ) -> FlextResult[bool]: ...

        @runtime_checkable
        class SchemaDiscoveryProtocol(FlextProtocols.Service, Protocol):
            """Protocol for Oracle schema discovery."""

            def discover_schemas(
                self, config: dict[str, object]
            ) -> FlextResult[list[dict[str, object]]]: ...
            def discover_tables(
                self, schema: str
            ) -> FlextResult[list[dict[str, object]]]: ...
            def get_table_metadata(
                self, schema: str, table: str
            ) -> FlextResult[dict[str, object]]: ...

        @runtime_checkable
        class DataExtractionProtocol(FlextProtocols.Service, Protocol):
            """Protocol for Oracle data extraction."""

            def extract_table_data(
                self, table: str, config: dict[str, object]
            ) -> FlextResult[list[dict[str, object]]]: ...
            def extract_incremental(
                self, table: str, state: dict[str, object]
            ) -> FlextResult[list[dict[str, object]]]: ...

        @runtime_checkable
        class TypeMappingProtocol(FlextProtocols.Service, Protocol):
            """Protocol for Oracle to Singer type mapping."""

            def map_oracle_type(self, oracle_type: str) -> FlextResult[str]: ...
            def convert_value(
                self, value: object, oracle_type: str
            ) -> FlextResult[object]: ...

        @runtime_checkable
        class StreamGenerationProtocol(FlextProtocols.Service, Protocol):
            """Protocol for Singer stream generation."""

            def generate_catalog(
                self, config: dict[str, object]
            ) -> FlextResult[dict[str, object]]: ...
            def sync_stream(
                self, stream: str, state: dict[str, object]
            ) -> FlextResult[dict[str, object]]: ...

        @runtime_checkable
        class PerformanceProtocol(FlextProtocols.Service, Protocol):
            """Protocol for Oracle extraction performance."""

            def optimize_query(self, query: str) -> FlextResult[str]: ...
            def configure_batch_size(self, size: int) -> FlextResult[bool]: ...

        @runtime_checkable
        class ValidationProtocol(FlextProtocols.Service, Protocol):
            """Protocol for Oracle data validation."""

            def validate_config(
                self, config: dict[str, object]
            ) -> FlextResult[bool]: ...
            def validate_schema(
                self, schema: dict[str, object]
            ) -> FlextResult[bool]: ...

        @runtime_checkable
        class MonitoringProtocol(FlextProtocols.Service, Protocol):
            """Protocol for Oracle extraction monitoring."""

            def track_progress(self, table: str, records: int) -> FlextResult[None]: ...
            def get_statistics(self) -> FlextResult[dict[str, object]]: ...

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
