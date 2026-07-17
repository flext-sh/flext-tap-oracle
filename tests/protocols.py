"""Protocols for flext-tap-oracle tests - uses composition with TestsFlextProtocols.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT

"""

from __future__ import annotations

from typing import TYPE_CHECKING, Protocol, runtime_checkable

from flext_tests import FlextTestsProtocols

from flext_tap_oracle import p

if TYPE_CHECKING:
    from tests import t


class TestsFlextTapOracleProtocols(FlextTestsProtocols, p):
    """Protocols for flext-tap-oracle tests - uses composition with TestsFlextProtocols.

    Architecture: Uses composition (not inheritance) with TestsFlextProtocols and p
    for flext-tap-oracle-specific protocol definitions.

    Access patterns:
    - TestsFlextTapOracleProtocols.Tests.* = flext_tests test protocols (via composition)
    - TestsFlextTapOracleProtocols.TapOracle.* = flext-tap-oracle-specific test protocols
    - TestsFlextTapOracleProtocols.* = TestsFlextProtocols protocols (via composition)

    Rules:
    - Use composition, not inheritance (TestsFlextProtocols deprecates subclassing)
    - flext-tap-oracle-specific protocols go in TapOracle namespace
    - Generic protocols accessed via Tests namespace
    """

    class Tests(FlextTestsProtocols.Test):
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
                parameters: t.JsonMapping | None = None,
            ) -> t.SequenceOf[t.JsonMapping]:
                """Execute query on mock database."""
                ...

        @runtime_checkable
        class TestDataProvider(Protocol):
            """Protocol for test data providers."""

            def get_test_tables(self) -> t.SequenceOf[t.JsonMapping]:
                """Get test table definitions."""
                ...

            def get_test_data(
                self,
                table_name: str,
            ) -> t.SequenceOf[t.JsonMapping]:
                """Get test data for a table."""
                ...

            def get_test_config(self) -> t.JsonMapping:
                """Get test configuration."""
                ...

        @runtime_checkable
        class TestAssertion(Protocol):
            """Protocol for test assertions."""

            def assert_oracle_connection_successful(
                self,
                settings: t.JsonMapping,
            ) -> None:
                """Assert Oracle connection was successful."""
                ...

            def assert_singer_stream_valid(
                self,
                stream: t.JsonMapping,
            ) -> None:
                """Assert Singer stream is valid."""
                ...

            def assert_extraction_results_match(
                self,
                expected: t.SequenceOf[t.JsonMapping],
                actual: t.SequenceOf[t.JsonMapping],
            ) -> None:
                """Assert extraction results match expected data."""
                ...


p = TestsFlextTapOracleProtocols

__all__: list[str] = ["TestsFlextTapOracleProtocols", "p"]
