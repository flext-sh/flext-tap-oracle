"""Singer Oracle tap protocols for FLEXT ecosystem."""

from typing import Protocol, runtime_checkable

from flext_db_oracle.protocols import p_db_oracle
from flext_meltano.protocols import p_meltano


class FlextMeltanoTapOracleProtocols(p_meltano, p_db_oracle):
    """Singer Tap Oracle protocols extending Oracle and Meltano protocols.

    Extends both FlextDbOracleProtocols and FlextMeltanoProtocols via multiple inheritance
    to inherit all Oracle protocols, Meltano protocols, and foundation protocols.

    Architecture:
    - EXTENDS: FlextDbOracleProtocols (inherits .Database.* protocols)
    - EXTENDS: FlextMeltanoProtocols (inherits .Meltano.* protocols)
    - ADDS: Tap Oracle-specific protocols in Tap.Oracle namespace
    - PROVIDES: Root-level alias `p` for convenient access

    Usage:
    from flext_tap_oracle.protocols import p

    # Foundation protocols (inherited)
    result: p.Result[str]
    service: p.Service[str]

    # Oracle protocols (inherited)
    connection: p.Database.ConnectionProtocol

    # Meltano protocols (inherited)
    tap: p.Meltano.TapProtocol

    # Tap Oracle-specific protocols
    oracle_connection: p.Tap.Oracle.OracleConnectionProtocol
    """

    class Tap:
        """Singer Tap domain protocols."""

        class Oracle:
            """Singer Tap Oracle domain protocols for Oracle database extraction."""

            @runtime_checkable
            class OracleConnectionProtocol(p_db_oracle.Service[object], Protocol):
                """Protocol for Oracle database connection management."""

                def connect(
                    self, config: dict[str, object]
                ) -> p_meltano.Result[object]:
                    """Connect to Oracle database with provided configuration."""
                    ...

                def disconnect(self) -> p_meltano.Result[bool]:
                    """Disconnect from Oracle database."""
                    ...

                def test_connection(
                    self, config: dict[str, object]
                ) -> p_meltano.Result[bool]:
                    """Test Oracle database connection with validation."""
                    ...

            @runtime_checkable
            class SchemaDiscoveryProtocol(p_db_oracle.Service[object], Protocol):
                """Protocol for Oracle schema discovery."""

                def discover_schemas(
                    self,
                    config: dict[str, object],
                ) -> p_meltano.Result[list[dict[str, object]]]:
                    """Discover accessible Oracle schemas."""
                    ...

                def discover_tables(
                    self,
                    schema: str,
                ) -> p_meltano.Result[list[dict[str, object]]]:
                    """Discover Oracle tables in specified schema."""
                    ...

                def get_table_metadata(
                    self,
                    schema: str,
                    table: str,
                ) -> p_meltano.Result[dict[str, object]]:
                    """Get Oracle table metadata and column definitions."""
                    ...

            @runtime_checkable
            class DataExtractionProtocol(p_db_oracle.Service[object], Protocol):
                """Protocol for Oracle data extraction."""

                def extract_table_data(
                    self,
                    table: str,
                    config: dict[str, object],
                ) -> p_meltano.Result[list[dict[str, object]]]:
                    """Extract all data from Oracle table."""
                    ...

                def extract_incremental(
                    self,
                    table: str,
                    state: dict[str, object],
                ) -> p_meltano.Result[list[dict[str, object]]]:
                    """Extract incremental data from Oracle table using state."""
                    ...

            @runtime_checkable
            class TypeMappingProtocol(p_db_oracle.Service[object], Protocol):
                """Protocol for Oracle to Singer type mapping."""

                def map_oracle_type(self, oracle_type: str) -> p_meltano.Result[str]:
                    """Map Oracle data type to Singer type."""
                    ...

                def convert_value(
                    self,
                    value: object,
                    oracle_type: str,
                ) -> p_meltano.Result[object]:
                    """Convert Oracle value to Singer-compatible format."""
                    ...

            @runtime_checkable
            class StreamGenerationProtocol(p_db_oracle.Service[object], Protocol):
                """Protocol for Singer stream generation."""

                def generate_catalog(
                    self,
                    config: dict[str, object],
                ) -> p_meltano.Result[dict[str, object]]:
                    """Generate Singer catalog from Oracle schema."""
                    ...

                def sync_stream(
                    self,
                    stream: str,
                    state: dict[str, object],
                ) -> p_meltano.Result[dict[str, object]]:
                    """Sync Singer stream from Oracle table."""
                    ...

            @runtime_checkable
            class PerformanceProtocol(p_db_oracle.Service[object], Protocol):
                """Protocol for Oracle extraction performance."""

                def optimize_query(self, query: str) -> p_meltano.Result[str]:
                    """Optimize Oracle query for performance."""
                    ...

                def configure_batch_size(self, size: int) -> p_meltano.Result[bool]:
                    """Configure extraction batch size."""
                    ...

            @runtime_checkable
            class ValidationProtocol(p_db_oracle.Service[object], Protocol):
                """Protocol for Oracle data validation."""

                def validate_config(
                    self, config: dict[str, object]
                ) -> p_meltano.Result[bool]:
                    """Validate tap configuration."""
                    ...

                def validate_schema(
                    self, schema: dict[str, object]
                ) -> p_meltano.Result[bool]:
                    """Validate Oracle schema definition."""
                    ...

            @runtime_checkable
            class MonitoringProtocol(p_db_oracle.Service[object], Protocol):
                """Protocol for Oracle extraction monitoring."""

                def track_progress(
                    self, table: str, records: int
                ) -> p_meltano.Result[bool]:
                    """Track Oracle table extraction progress."""
                    ...

                def get_statistics(
                    self,
                ) -> p_meltano.Result[dict[str, object]]:
                    """Get extraction statistics."""
                    ...


# Runtime alias for simplified usage
p = FlextMeltanoTapOracleProtocols

__all__ = [
    "FlextMeltanoTapOracleProtocols",
    "p",
]
