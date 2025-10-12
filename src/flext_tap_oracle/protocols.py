"""Singer Oracle tap protocols for FLEXT ecosystem."""

from typing import Protocol, runtime_checkable

from flext_core import FlextCore


class FlextMeltanoTapOracleProtocols:
    """Singer Tap Oracle protocols with explicit re-exports from FlextCore.Protocols foundation.

    Domain Extension Pattern (Phase 3):
    - Explicit re-export of foundation protocols (not inheritance)
    - Domain-specific protocols organized in TapOracle namespace
    - 100% backward compatibility through aliases
    """

    Foundation = FlextCore.Protocols.Foundation
    Domain = FlextCore.Protocols.Domain
    Application = FlextCore.Protocols.Application
    Infrastructure = FlextCore.Protocols.Infrastructure
    Extensions = FlextCore.Protocols.Extensions
    Commands = FlextCore.Protocols.Commands

    class TapOracle:
        """Singer Tap Oracle domain protocols for Oracle database extraction."""

        @runtime_checkable
        class OracleConnectionProtocol(FlextCore.Protocols.Domain.Service, Protocol):
            """Protocol for Oracle database connection management."""

            def connect(
                self, config: FlextCore.Types.Dict
            ) -> FlextCore.Result[object]: ...
            def disconnect(self) -> FlextCore.Result[None]: ...
            def test_connection(
                self, config: FlextCore.Types.Dict
            ) -> FlextCore.Result[bool]: ...

        @runtime_checkable
        class SchemaDiscoveryProtocol(FlextCore.Protocols.Domain.Service, Protocol):
            """Protocol for Oracle schema discovery."""

            def discover_schemas(
                self, config: FlextCore.Types.Dict
            ) -> FlextCore.Result[list[FlextCore.Types.Dict]]: ...
            def discover_tables(
                self, schema: str
            ) -> FlextCore.Result[list[FlextCore.Types.Dict]]: ...
            def get_table_metadata(
                self, schema: str, table: str
            ) -> FlextCore.Result[FlextCore.Types.Dict]: ...

        @runtime_checkable
        class DataExtractionProtocol(FlextCore.Protocols.Domain.Service, Protocol):
            """Protocol for Oracle data extraction."""

            def extract_table_data(
                self, table: str, config: FlextCore.Types.Dict
            ) -> FlextCore.Result[list[FlextCore.Types.Dict]]: ...
            def extract_incremental(
                self, table: str, state: FlextCore.Types.Dict
            ) -> FlextCore.Result[list[FlextCore.Types.Dict]]: ...

        @runtime_checkable
        class TypeMappingProtocol(FlextCore.Protocols.Domain.Service, Protocol):
            """Protocol for Oracle to Singer type mapping."""

            def map_oracle_type(self, oracle_type: str) -> FlextCore.Result[str]: ...
            def convert_value(
                self, value: object, oracle_type: str
            ) -> FlextCore.Result[object]: ...

        @runtime_checkable
        class StreamGenerationProtocol(FlextCore.Protocols.Domain.Service, Protocol):
            """Protocol for Singer stream generation."""

            def generate_catalog(
                self, config: FlextCore.Types.Dict
            ) -> FlextCore.Result[FlextCore.Types.Dict]: ...
            def sync_stream(
                self, stream: str, state: FlextCore.Types.Dict
            ) -> FlextCore.Result[FlextCore.Types.Dict]: ...

        @runtime_checkable
        class PerformanceProtocol(FlextCore.Protocols.Domain.Service, Protocol):
            """Protocol for Oracle extraction performance."""

            def optimize_query(self, query: str) -> FlextCore.Result[str]: ...
            def configure_batch_size(self, size: int) -> FlextCore.Result[bool]: ...

        @runtime_checkable
        class ValidationProtocol(FlextCore.Protocols.Domain.Service, Protocol):
            """Protocol for Oracle data validation."""

            def validate_config(
                self, config: FlextCore.Types.Dict
            ) -> FlextCore.Result[bool]: ...
            def validate_schema(
                self, schema: FlextCore.Types.Dict
            ) -> FlextCore.Result[bool]: ...

        @runtime_checkable
        class MonitoringProtocol(FlextCore.Protocols.Domain.Service, Protocol):
            """Protocol for Oracle extraction monitoring."""

            def track_progress(
                self, table: str, records: int
            ) -> FlextCore.Result[None]: ...
            def get_statistics(self) -> FlextCore.Result[FlextCore.Types.Dict]: ...

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
