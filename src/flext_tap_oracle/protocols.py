"""Singer Oracle tap protocols for FLEXT ecosystem."""

from typing import Any, Protocol, runtime_checkable

from flext_core import FlextProtocols, FlextResult, FlextTypes


class FlextTapOracleProtocols:
    """Singer Tap Oracle protocols with explicit re-exports from FlextProtocols foundation.

    Domain Extension Pattern (Phase 3):
    - Explicit re-export of foundation protocols (not inheritance)
    - Domain-specific protocols organized in TapOracle namespace
    - 100% backward compatibility through aliases
    """

    Foundation = FlextProtocols.Foundation
    Domain = FlextProtocols.Domain
    Application = FlextProtocols.Application
    Infrastructure = FlextProtocols.Infrastructure
    Extensions = FlextProtocols.Extensions
    Commands = FlextProtocols.Commands

    class TapOracle:
        """Singer Tap Oracle domain protocols for Oracle database extraction."""

        @runtime_checkable
        class OracleConnectionProtocol(FlextProtocols.Domain.Service, Protocol):
            """Protocol for Oracle database connection management."""

            def connect(self, config: FlextTypes.Dict) -> FlextResult[Any]: ...
            def disconnect(self) -> FlextResult[None]: ...
            def test_connection(self, config: FlextTypes.Dict) -> FlextResult[bool]: ...

        @runtime_checkable
        class SchemaDiscoveryProtocol(FlextProtocols.Domain.Service, Protocol):
            """Protocol for Oracle schema discovery."""

            def discover_schemas(
                self, config: FlextTypes.Dict
            ) -> FlextResult[list[FlextTypes.Dict]]: ...
            def discover_tables(
                self, schema: str
            ) -> FlextResult[list[FlextTypes.Dict]]: ...
            def get_table_metadata(
                self, schema: str, table: str
            ) -> FlextResult[FlextTypes.Dict]: ...

        @runtime_checkable
        class DataExtractionProtocol(FlextProtocols.Domain.Service, Protocol):
            """Protocol for Oracle data extraction."""

            def extract_table_data(
                self, table: str, config: FlextTypes.Dict
            ) -> FlextResult[list[FlextTypes.Dict]]: ...
            def extract_incremental(
                self, table: str, state: FlextTypes.Dict
            ) -> FlextResult[list[FlextTypes.Dict]]: ...

        @runtime_checkable
        class TypeMappingProtocol(FlextProtocols.Domain.Service, Protocol):
            """Protocol for Oracle to Singer type mapping."""

            def map_oracle_type(self, oracle_type: str) -> FlextResult[str]: ...
            def convert_value(
                self, value: Any, oracle_type: str
            ) -> FlextResult[Any]: ...

        @runtime_checkable
        class StreamGenerationProtocol(FlextProtocols.Domain.Service, Protocol):
            """Protocol for Singer stream generation."""

            def generate_catalog(
                self, config: FlextTypes.Dict
            ) -> FlextResult[FlextTypes.Dict]: ...
            def sync_stream(
                self, stream: str, state: FlextTypes.Dict
            ) -> FlextResult[FlextTypes.Dict]: ...

        @runtime_checkable
        class PerformanceProtocol(FlextProtocols.Domain.Service, Protocol):
            """Protocol for Oracle extraction performance."""

            def optimize_query(self, query: str) -> FlextResult[str]: ...
            def configure_batch_size(self, size: int) -> FlextResult[bool]: ...

        @runtime_checkable
        class ValidationProtocol(FlextProtocols.Domain.Service, Protocol):
            """Protocol for Oracle data validation."""

            def validate_config(self, config: FlextTypes.Dict) -> FlextResult[bool]: ...
            def validate_schema(self, schema: FlextTypes.Dict) -> FlextResult[bool]: ...

        @runtime_checkable
        class MonitoringProtocol(FlextProtocols.Domain.Service, Protocol):
            """Protocol for Oracle extraction monitoring."""

            def track_progress(self, table: str, records: int) -> FlextResult[None]: ...
            def get_statistics(self) -> FlextResult[FlextTypes.Dict]: ...

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
    "FlextTapOracleProtocols",
]
