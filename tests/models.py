"""Models for flext-tap-oracle tests - uses composition with FlextTestsModels.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT

"""

from __future__ import annotations

from flext_core import FlextModels
from flext_tests import FlextTestsModels


class TestsFlextTapOracleModels(FlextTestsModels):
    """Models for flext-tap-oracle tests - uses composition with FlextTestsModels.

    Architecture: Uses composition (not inheritance) with FlextTestsModels and FlextModels
    for flext-tap-oracle-specific model definitions.

    Access patterns:
    - TestsFlextTapOracleModels.Tests.* = flext_tests test models (via composition)
    - TestsFlextTapOracleModels.TapOracle.* = flext-tap-oracle-specific test models
    - TestsFlextTapOracleModels.Entity, .Value, etc. = FlextModels domain models (via composition)

    Rules:
    - Use composition, not inheritance (FlextTestsModels deprecates subclassing)
    - flext-tap-oracle-specific models go in TapOracle namespace
    - Generic models accessed via Tests namespace
    """

    # Composition: expose FlextTestsModels namespaces
    Tests = FlextTestsModels.Tests

    # Composition: expose FlextModels domain model classes
    Entity = FlextModels.Entity
    Value = FlextModels.Value
    AggregateRoot = FlextModels.AggregateRoot
    DomainEvent = FlextModels.DomainEvent
    Collections = FlextModels.Collections

    # TapOracle-specific test models namespace
    class TapOracle:
        """Tap Oracle test models - domain-specific for Oracle tap testing.

        Contains test models specific to Oracle tap functionality including:
        - Singer protocol test models
        - Oracle database test models
        - Stream processing test models
        - Configuration test models
        """

        class TestOracleConnection(FlextModels.Entity):
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

        class TestSingerStream(FlextModels.Entity):
            """Test model for Singer streams."""

            stream_name: str
            table_name: str
            replication_method: str
            is_selected: bool = True

        class TestOracleTable(FlextModels.Entity):
            """Test model for Oracle tables."""

            table_name: str
            schema_name: str
            column_count: int
            row_count: int | None = None

        class TestExtractionConfig(FlextModels.Entity):
            """Test model for extraction configurations."""

            batch_size: int
            parallel_streams: int
            timeout_seconds: int
            max_rows: int | None = None


# Alias for simplified usage
tm = TestsFlextTapOracleModels
m = TestsFlextTapOracleModels

__all__ = [
    "TestsFlextTapOracleModels",
    "m",
    "tm",
]
