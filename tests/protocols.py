"""Protocols for flext-tap-oracle tests - uses composition with FlextTestsProtocols.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT

"""

from __future__ import annotations

from collections.abc import Sequence
from typing import Protocol, runtime_checkable

from flext_tests import FlextTestsProtocols

from flext_tap_oracle import FlextTapOracleProtocols
from tests import t


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
                    self,
                    query: str,
                    parameters: t.ContainerMapping | None = None,
                ) -> Sequence[t.ContainerMapping]:
                    """Execute query on mock database."""
                    ...

            @runtime_checkable
            class TestDataProvider(Protocol):
                """Protocol for test data providers."""

                def get_test_tables(self) -> Sequence[t.ContainerMapping]:
                    """Get test table definitions."""
                    ...

                def get_test_data(
                    self,
                    table_name: str,
                ) -> Sequence[t.ContainerMapping]:
                    """Get test data for a table."""
                    ...

                def get_test_config(self) -> t.ContainerMapping:
                    """Get test configuration."""
                    ...

            @runtime_checkable
            class TestAssertion(Protocol):
                """Protocol for test assertions."""

                def assert_oracle_connection_successful(
                    self,
                    config: t.ContainerMapping,
                ) -> None:
                    """Assert Oracle connection was successful."""
                    ...

                def assert_singer_stream_valid(
                    self,
                    stream: t.ContainerMapping,
                ) -> None:
                    """Assert Singer stream is valid."""
                    ...

                def assert_extraction_results_match(
                    self,
                    expected: Sequence[t.ContainerMapping],
                    actual: Sequence[t.ContainerMapping],
                ) -> None:
                    """Assert extraction results match expected data."""
                    ...


p = FlextTapOracleTestProtocols
__all__ = ["FlextTapOracleTestProtocols", "p"]
