"""Singer Oracle tap protocols for FLEXT ecosystem.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from typing import Protocol, runtime_checkable

from flext_core import FlextTypes as t
from flext_db_oracle.protocols import FlextDbOracleProtocols
from flext_meltano import FlextMeltanoModels as m
from flext_meltano.protocols import FlextMeltanoProtocols


class FlextMeltanoTapOracleProtocols(FlextMeltanoProtocols, FlextDbOracleProtocols):
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

    class TapOracle:
        """Tap Oracle  namespace for cross-project access."""

        @runtime_checkable
        class OracleConnectionProtocol(
            FlextDbOracleProtocols.Service[object], Protocol
        ):
            """Protocol for Oracle database connection management."""

            def connect(
                self,
                config: dict[str, t.GeneralValueType],
            ) -> FlextMeltanoProtocols.Result[object]:
                """Connect to Oracle database with provided configuration."""
                ...

            def disconnect(self) -> FlextMeltanoProtocols.Result[bool]:
                """Disconnect from Oracle database."""
                ...

            def test_connection(
                self,
                config: dict[str, t.GeneralValueType],
            ) -> FlextMeltanoProtocols.Result[bool]:
                """Test Oracle database connection with validation."""
                ...

        @runtime_checkable
        class SchemaDiscoveryProtocol(FlextDbOracleProtocols.Service[object], Protocol):
            """Protocol for Oracle schema discovery."""

            def discover_schemas(
                self,
                config: dict[str, t.GeneralValueType],
            ) -> FlextMeltanoProtocols.Result[list[dict[str, t.GeneralValueType]]]:
                """Discover accessible Oracle schemas."""
                ...

            def discover_tables(
                self,
                schema: str,
            ) -> FlextMeltanoProtocols.Result[list[dict[str, t.GeneralValueType]]]:
                """Discover Oracle tables in specified schema."""
                ...

            def get_table_metadata(
                self,
                schema: str,
                table: str,
            ) -> FlextMeltanoProtocols.Result[dict[str, t.GeneralValueType]]:
                """Get Oracle table metadata and column definitions."""
                ...

        @runtime_checkable
        class DataExtractionProtocol(FlextDbOracleProtocols.Service[object], Protocol):
            """Protocol for Oracle data extraction."""

            def extract_table_data(
                self,
                table: str,
                config: dict[str, t.GeneralValueType],
            ) -> FlextMeltanoProtocols.Result[list[dict[str, t.GeneralValueType]]]:
                """Extract all data from Oracle table."""
                ...

            def extract_incremental(
                self,
                table: str,
                state: dict[str, t.GeneralValueType],
            ) -> FlextMeltanoProtocols.Result[list[dict[str, t.GeneralValueType]]]:
                """Extract incremental data from Oracle table using state."""
                ...

        @runtime_checkable
        class TypeMappingProtocol(FlextDbOracleProtocols.Service[object], Protocol):
            """Protocol for Oracle to Singer type mapping."""

            def map_oracle_type(
                self, oracle_type: str
            ) -> FlextMeltanoProtocols.Result[str]:
                """Map Oracle data type to Singer type."""
                ...

            def convert_value(
                self,
                value: object,
                oracle_type: str,
            ) -> FlextMeltanoProtocols.Result[object]:
                """Convert Oracle value to Singer-compatible format."""
                ...

        @runtime_checkable
        class StreamGenerationProtocol(
            FlextDbOracleProtocols.Service[object], Protocol
        ):
            """Protocol for Singer stream generation."""

            def generate_catalog(
                self,
                config: dict[str, t.GeneralValueType],
            ) -> FlextMeltanoProtocols.Result[m.Meltano.SingerCatalog]:
                """Generate Singer catalog from Oracle schema."""
                ...

            def sync_stream(
                self,
                stream: str,
                state: dict[str, t.GeneralValueType],
            ) -> FlextMeltanoProtocols.Result[m.Meltano.SingerStateMessage]:
                """Sync Singer stream from Oracle table."""
                ...

        @runtime_checkable
        class PerformanceProtocol(FlextDbOracleProtocols.Service[object], Protocol):
            """Protocol for Oracle extraction performance."""

            def optimize_query(self, query: str) -> FlextMeltanoProtocols.Result[str]:
                """Optimize Oracle query for performance."""
                ...

            def configure_batch_size(
                self, size: int
            ) -> FlextMeltanoProtocols.Result[bool]:
                """Configure extraction batch size."""
                ...

        @runtime_checkable
        class ValidationProtocol(FlextDbOracleProtocols.Service[object], Protocol):
            """Protocol for Oracle data validation."""

            def validate_config(
                self,
                config: dict[str, t.GeneralValueType],
            ) -> FlextMeltanoProtocols.Result[bool]:
                """Validate tap configuration."""
                ...

            def validate_schema(
                self,
                schema: dict[str, t.GeneralValueType],
            ) -> FlextMeltanoProtocols.Result[bool]:
                """Validate Oracle schema definition."""
                ...

        @runtime_checkable
        class MonitoringProtocol(FlextDbOracleProtocols.Service[object], Protocol):
            """Protocol for Oracle extraction monitoring."""

            def track_progress(
                self,
                table: str,
                records: int,
            ) -> FlextMeltanoProtocols.Result[bool]:
                """Track Oracle table extraction progress."""
                ...

            def get_statistics(
                self,
            ) -> FlextMeltanoProtocols.Result[dict[str, t.GeneralValueType]]:
                """Get extraction statistics."""
                ...


# Runtime alias for simplified usage
p = FlextMeltanoTapOracleProtocols

__all__ = [
    "FlextMeltanoTapOracleProtocols",
    "p",
]
