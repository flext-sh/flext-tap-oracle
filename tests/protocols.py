"""Protocols for flext-tap-oracle tests - uses composition with FlextTestsProtocols.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT

"""

from __future__ import annotations

from typing import Protocol, runtime_checkable

from flext_tests import FlextTestsProtocols

from flext_tap_oracle import FlextTapOracleProtocols


class FlextTapOracleTestProtocols(FlextTestsProtocols, FlextTapOracleProtocols):
    """Protocols for flext-tap-oracle tests - uses composition with FlextTestsProtocols.

    Architecture: Uses composition (not inheritance) with FlextTestsProtocols and FlextTapOracleProtocols
    for flext-tap-oracle-specific protocol definitions.

    Access patterns:
    - FlextTapOracleTestProtocols.Tests.* = flext_tests test protocols (via composition)
    - FlextTapOracleTestProtocols.TapOracle.* = flext-tap-oracle-specific test protocols
    - FlextTapOracleTestProtocols.* = FlextTestsProtocols protocols (via composition)

    Rules:
    - Use composition, not inheritance (FlextTestsProtocols deprecates subclassing)
    - flext-tap-oracle-specific protocols go in TapOracle namespace
    - Generic protocols accessed via Tests namespace
    """

    class TapOracle(FlextTapOracleProtocols.TapOracle):
        """Tap Oracle test protocols - domain-specific for Oracle tap testing.

        Contains test protocols specific to Oracle tap functionality including:
        - Mock service protocols for testing
        - Test data provider protocols
        - Test assertion protocols
        """

        class Tests:
            """Internal tests declarations."""

            @runtime_checkable
            class MockOracleConnection(Protocol):
                """Protocol for mock Oracle connections in tests."""

                def connect(self) -> bool:
                    """Connect to mock Oracle database."""
                    ...

                def disconnect(self) -> bool:
                    """Disconnect from mock Oracle database."""
                    ...

                def execute_query(
                    self, query: str, parameters: dict[str, object] | None = None
                ) -> list[dict[str, object]]:
                    """Execute query on mock database."""
                    ...

            @runtime_checkable
            class TestDataProvider(Protocol):
                """Protocol for test data providers."""

                def get_test_tables(self) -> list[dict[str, object]]:
                    """Get test table definitions."""
                    ...

                def get_test_data(self, table_name: str) -> list[dict[str, object]]:
                    """Get test data for a table."""
                    ...

                def get_test_config(self) -> dict[str, object]:
                    """Get test configuration."""
                    ...

            @runtime_checkable
            class TestAssertion(Protocol):
                """Protocol for test assertions."""

                def assert_oracle_connection_successful(
                    self, config: dict[str, object]
                ) -> None:
                    """Assert Oracle connection was successful."""
                    ...

                def assert_singer_stream_valid(self, stream: dict[str, object]) -> None:
                    """Assert Singer stream is valid."""
                    ...

                def assert_extraction_results_match(
                    self,
                    expected: list[dict[str, object]],
                    actual: list[dict[str, object]],
                ) -> None:
                    """Assert extraction results match expected data."""
                    ...


p = FlextTapOracleTestProtocols
__all__ = ["FlextTapOracleTestProtocols", "p"]
