"""Singer Oracle tap protocols for FLEXT ecosystem.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from collections.abc import Mapping, Sequence
from typing import Protocol, runtime_checkable

from flext_db_oracle import FlextDbOracleProtocols
from flext_meltano import m
from flext_tap_oracle import t


class FlextTapOracleProtocols(m, FlextDbOracleProtocols):
    """Singer Tap Oracle protocols extending Oracle and Meltano protocols.

    Extends both FlextDbOracleProtocols and m via multiple inheritance
    to inherit all Oracle protocols, Meltano protocols, and foundation protocols.

    Architecture:
    - EXTENDS: FlextDbOracleProtocols (inherits .Database.* protocols)
    - EXTENDS: m (inherits .Meltano.* protocols)
    - ADDS: Tap Oracle-specific protocols in Tap.Oracle namespace
    - PROVIDES: Root-level alias `p` for convenient access

    Usage:
    from flext_tap_oracle import p

    # Foundation protocols (inherited)
    result: p.Result[str]
    service: p.Service[str]

    # Oracle protocols (inherited)
    connection: p.Database.Connection

    # Meltano protocols (inherited)
    tap: p.Meltano.Tap

    # Tap Oracle-specific protocols
    oracle_connection: p.Tap.Oracle.OracleConnection
    """

    class TapOracle:
        """Tap Oracle  namespace for cross-project access."""

        @runtime_checkable
        class OracleConnection(
            FlextDbOracleProtocols.Service[t.GeneralValueType],
            Protocol,
        ):
            """Protocol for Oracle database connection management."""

            def connect(
                self,
                settings: Mapping[str, t.GeneralValueType],
            ) -> p.Result[t.GeneralValueType]:
                """Connect to Oracle database with provided configuration."""
                ...

            def disconnect(self) -> p.Result[bool]:
                """Disconnect from Oracle database."""
                ...

            def test_connection(
                self,
                settings: Mapping[str, t.GeneralValueType],
            ) -> p.Result[bool]:
                """Test Oracle database connection with validation."""
                ...

        @runtime_checkable
        class SchemaDiscovery(
            FlextDbOracleProtocols.Service[t.GeneralValueType],
            Protocol,
        ):
            """Protocol for Oracle schema discovery."""

            def discover_schemas(
                self,
                settings: Mapping[str, t.GeneralValueType],
            ) -> p.Result[Sequence[t.GeneralValueType]]:
                """Discover accessible Oracle schemas."""
                ...

            def discover_tables(
                self,
                schema: str,
            ) -> p.Result[Sequence[t.GeneralValueType]]:
                """Discover Oracle tables in specified schema."""
                ...

            def get_table_metadata(
                self,
                schema: str,
                table: str,
            ) -> p.Result[t.GeneralValueType]:
                """Get Oracle table metadata and column definitions."""
                ...

        @runtime_checkable
        class DataExtraction(
            FlextDbOracleProtocols.Service[t.GeneralValueType],
            Protocol,
        ):
            """Protocol for Oracle data extraction."""

            def extract_incremental(
                self,
                table: str,
                state: Mapping[str, t.GeneralValueType],
            ) -> p.Result[Sequence[t.GeneralValueType]]:
                """Extract incremental data from Oracle table using state."""
                ...

            def extract_table_data(
                self,
                table: str,
                settings: Mapping[str, t.GeneralValueType],
            ) -> p.Result[Sequence[t.GeneralValueType]]:
                """Extract all data from Oracle table."""
                ...

        @runtime_checkable
        class TypeMapping(FlextDbOracleProtocols.Service[t.GeneralValueType], Protocol):
            """Protocol for Oracle to Singer type mapping."""

            def convert_value(
                self,
                value: t.GeneralValueType,
                oracle_type: str,
            ) -> p.Result[t.GeneralValueType]:
                """Convert Oracle value to Singer-compatible format."""
                ...

            def map_oracle_type(
                self,
                oracle_type: str,
            ) -> p.Result[str]:
                """Map Oracle data type to Singer type."""
                ...

        @runtime_checkable
        class StreamGeneration(
            FlextDbOracleProtocols.Service[t.GeneralValueType],
            Protocol,
        ):
            """Protocol for Singer stream generation."""

            def generate_catalog(
                self,
                settings: Mapping[str, t.GeneralValueType],
            ) -> p.Result[m.Meltano.SingerCatalog]:
                """Generate Singer catalog from Oracle schema."""
                ...

            def sync_stream(
                self,
                stream: str,
                state: Mapping[str, t.GeneralValueType],
            ) -> p.Result[m.Meltano.SingerStateMessage]:
                """Sync Singer stream from Oracle table."""
                ...

        @runtime_checkable
        class Performance(FlextDbOracleProtocols.Service[t.GeneralValueType], Protocol):
            """Protocol for Oracle extraction performance."""

            def configure_batch_size(
                self,
                size: int,
            ) -> p.Result[bool]:
                """Configure extraction batch size."""
                ...

            def optimize_query(self, query: str) -> p.Result[str]:
                """Optimize Oracle query for performance."""
                ...

        @runtime_checkable
        class Validation(FlextDbOracleProtocols.Service[t.GeneralValueType], Protocol):
            """Protocol for Oracle data validation."""

            def validate_config(
                self,
                settings: Mapping[str, t.GeneralValueType],
            ) -> p.Result[bool]:
                """Validate tap configuration."""
                ...

            def validate_schema(
                self,
                schema: Mapping[str, t.GeneralValueType],
            ) -> p.Result[bool]:
                """Validate Oracle schema definition."""
                ...

        @runtime_checkable
        class Monitoring(FlextDbOracleProtocols.Service[t.GeneralValueType], Protocol):
            """Protocol for Oracle extraction monitoring."""

            def get_statistics(
                self,
            ) -> p.Result[t.GeneralValueType]:
                """Get extraction statistics."""
                ...

            def track_progress(
                self,
                table: str,
                records: int,
            ) -> p.Result[bool]:
                """Track Oracle table extraction progress."""
                ...

    class TapOraclePrivate:
        """Private structural protocols for internal flext-tap-oracle use."""

        @runtime_checkable
        class CommandRunner(Protocol):
            """Structural protocol for Oracle tap command execution."""

            def execute(self) -> p.Result[Mapping[str, t.GeneralValueType]]:
                """Execute the Oracle tap command and return results."""
                ...

        @runtime_checkable
        class Tap(Protocol):
            """Structural protocol for Oracle tap t.RecursiveContainer used in stream context."""

            typed_config: t.RecursiveContainer


p = FlextTapOracleProtocols
__all__: list[str] = ["FlextTapOracleProtocols", "p"]
