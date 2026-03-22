"""Models for flext-tap-oracle tests - uses composition with FlextTestsModels.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT

"""

from __future__ import annotations

from flext_tests import FlextTestsModels

from flext_tap_oracle import FlextTapOracleModels


class FlextTapOracleTestModels(FlextTestsModels, FlextTapOracleModels):
    """Models for flext-tap-oracle tests - uses composition with FlextTestsModels.

    Architecture: Uses composition (not inheritance) with FlextTestsModels and FlextTapOracleModels
    for flext-tap-oracle-specific model definitions.

    Access patterns:
    - FlextTapOracleTestModels.Tests.* = flext_tests test models (via composition)
    - FlextTapOracleTestModels.TapOracle.* = flext-tap-oracle-specific test models
    - FlextTapOracleTestModels.Entity, .Value, etc. = FlextTapOracleModels domain models (via composition)

    Rules:
    - Use composition, not inheritance (FlextTestsModels deprecates subclassing)
    - flext-tap-oracle-specific models go in TapOracle namespace
    - Generic models accessed via Tests namespace
    """

    class TapOracle(FlextTapOracleModels.TapOracle):
        """Tap Oracle test models - domain-specific for Oracle tap testing.

        Contains test models specific to Oracle tap functionality including:
        - Singer protocol test models
        - Oracle database test models
        - Stream processing test models
        - Configuration test models
        """

        class Tests:
            """Test models namespace for flext-tap-oracle tests."""

            class TestOracleConnection(FlextTapOracleModels.Entity):
                """Test model for Oracle database connections."""

                host: str
                port: int
                service_name: str
                username: str
                password: str

                @property
                def connection_string(self) -> str:
                    """Get Oracle connection string."""
                    return f"oracle://{self.username}:***@{self.host}:{self.port}/{self.service_name}"

            class TestSingerStream(FlextTapOracleModels.Entity):
                """Test model for Singer streams."""

                stream_name: str
                table_name: str
                replication_method: str
                is_selected: bool = True

            class TestOracleTable(FlextTapOracleModels.Entity):
                """Test model for Oracle tables."""

                table_name: str
                schema_name: str
                column_count: int
                row_count: int | None = None

            class TestExtractionConfig(FlextTapOracleModels.Entity):
                """Test model for extraction configurations."""

                batch_size: int
                parallel_streams: int
                timeout_seconds: int
                max_rows: int | None = None


m = FlextTapOracleTestModels

__all__ = [
    "FlextTapOracleTestModels",
    "m",
]
