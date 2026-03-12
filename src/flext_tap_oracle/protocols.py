"""Singer Oracle tap protocols for FLEXT ecosystem.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from collections.abc import Mapping
from typing import Protocol, runtime_checkable

from flext_db_oracle.protocols import FlextDbOracleProtocols
from flext_meltano import FlextMeltanoModels as m, FlextMeltanoProtocols

from flext_tap_oracle.typings import t


class FlextTapOracleProtocols(FlextMeltanoProtocols, FlextDbOracleProtocols):
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
    tap: p.Meltano.Tap

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
                self, config: Mapping[str, object]
            ) -> FlextMeltanoProtocols.Result[object]:
                """Connect to Oracle database with provided configuration."""
                ...

            def disconnect(self) -> FlextMeltanoProtocols.Result[bool]:
                """Disconnect from Oracle database."""
                ...

            def test_connection(
                self, config: Mapping[str, object]
            ) -> FlextMeltanoProtocols.Result[bool]:
                """Test Oracle database connection with validation."""
                ...

        @runtime_checkable
        class SchemaDiscoveryProtocol(FlextDbOracleProtocols.Service[object], Protocol):
            """Protocol for Oracle schema discovery."""

            def discover_schemas(
                self, config: Mapping[str, object]
            ) -> FlextMeltanoProtocols.Result[list[t.ConfigurationMapping]]:
                """Discover accessible Oracle schemas."""
                ...

            def discover_tables(
                self, schema: str
            ) -> FlextMeltanoProtocols.Result[list[t.ConfigurationMapping]]:
                """Discover Oracle tables in specified schema."""
                ...

            def get_table_metadata(
                self, schema: str, table: str
            ) -> FlextMeltanoProtocols.Result[t.ConfigurationMapping]:
                """Get Oracle table metadata and column definitions."""
                ...

        @runtime_checkable
        class DataExtractionProtocol(FlextDbOracleProtocols.Service[object], Protocol):
            """Protocol for Oracle data extraction."""

            def extract_incremental(
                self, table: str, state: Mapping[str, object]
            ) -> FlextMeltanoProtocols.Result[list[t.ConfigurationMapping]]:
                """Extract incremental data from Oracle table using state."""
                ...

            def extract_table_data(
                self, table: str, config: Mapping[str, object]
            ) -> FlextMeltanoProtocols.Result[list[t.ConfigurationMapping]]:
                """Extract all data from Oracle table."""
                ...

        @runtime_checkable
        class TypeMappingProtocol(FlextDbOracleProtocols.Service[object], Protocol):
            """Protocol for Oracle to Singer type mapping."""

            def convert_value(
                self, value: object, oracle_type: str
            ) -> FlextMeltanoProtocols.Result[object]:
                """Convert Oracle value to Singer-compatible format."""
                ...

            def map_oracle_type(
                self, oracle_type: str
            ) -> FlextMeltanoProtocols.Result[str]:
                """Map Oracle data type to Singer type."""
                ...

        @runtime_checkable
        class StreamGenerationProtocol(
            FlextDbOracleProtocols.Service[object], Protocol
        ):
            """Protocol for Singer stream generation."""

            def generate_catalog(
                self, config: Mapping[str, object]
            ) -> FlextMeltanoProtocols.Result[m.Meltano.SingerCatalog]:
                """Generate Singer catalog from Oracle schema."""
                ...

            def sync_stream(
                self, stream: str, state: Mapping[str, object]
            ) -> FlextMeltanoProtocols.Result[m.Meltano.SingerStateMessage]:
                """Sync Singer stream from Oracle table."""
                ...

        @runtime_checkable
        class PerformanceProtocol(FlextDbOracleProtocols.Service[object], Protocol):
            """Protocol for Oracle extraction performance."""

            def configure_batch_size(
                self, size: int
            ) -> FlextMeltanoProtocols.Result[bool]:
                """Configure extraction batch size."""
                ...

            def optimize_query(self, query: str) -> FlextMeltanoProtocols.Result[str]:
                """Optimize Oracle query for performance."""
                ...

        @runtime_checkable
        class ValidationProtocol(FlextDbOracleProtocols.Service[object], Protocol):
            """Protocol for Oracle data validation."""

            def validate_config(
                self, config: Mapping[str, object]
            ) -> FlextMeltanoProtocols.Result[bool]:
                """Validate tap configuration."""
                ...

            def validate_schema(
                self, schema: Mapping[str, object]
            ) -> FlextMeltanoProtocols.Result[bool]:
                """Validate Oracle schema definition."""
                ...

        @runtime_checkable
        class MonitoringProtocol(FlextDbOracleProtocols.Service[object], Protocol):
            """Protocol for Oracle extraction monitoring."""

            def get_statistics(
                self,
            ) -> FlextMeltanoProtocols.Result[t.ConfigurationMapping]:
                """Get extraction statistics."""
                ...

            def track_progress(
                self, table: str, records: int
            ) -> FlextMeltanoProtocols.Result[bool]:
                """Track Oracle table extraction progress."""
                ...


p = FlextTapOracleProtocols
__all__ = ["FlextTapOracleProtocols", "p"]
