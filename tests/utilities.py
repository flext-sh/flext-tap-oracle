"""Utilities for flext-tap-oracle tests - uses composition with TestsFlextUtilities.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT

"""

from __future__ import annotations

from typing import TYPE_CHECKING

from flext_tests import FlextTestsUtilities

from flext_tap_oracle import FlextTapOracleUtilities

if TYPE_CHECKING:
    from tests import t


class TestsFlextTapOracleUtilities(FlextTestsUtilities, FlextTapOracleUtilities):
    """Utilities for flext-tap-oracle tests - uses composition with TestsFlextUtilities.

    Architecture: Uses composition (not inheritance) with TestsFlextUtilities and FlextTapOracleUtilities
    for flext-tap-oracle-specific utility definitions.

    Access patterns:
    - TestsFlextTapOracleUtilities.Tests.* = flext_tests test utilities (via composition)
    - TestsFlextTapOracleUtilities.TapOracle.* = flext-tap-oracle-specific test utilities
    - TestsFlextTapOracleUtilities.* = TestsFlextUtilities methods (via composition)

    Rules:
    - Use composition, not inheritance (TestsFlextUtilities deprecates subclassing)
    - flext-tap-oracle-specific utilities go in TapOracle namespace
    - Generic utilities accessed via Tests namespace
    """

    class Tests(FlextTestsUtilities.Tests):
        """Tap Oracle test utilities - domain-specific for Oracle tap testing.

        Contains test utilities specific to Oracle tap functionality including:
        - Oracle connection test helpers
        - Singer protocol test helpers
        - Stream processing test helpers
        - Configuration validation test helpers
        """

        @staticmethod
        def create_test_oracle_config(
            host: str = "localhost",
            port: int = 1521,
            service_name: str = "XE",
            username: str = "test",
            password: str = "test",
            **kwargs: t.JsonValue,
        ) -> t.JsonMapping:
            """Create test Oracle configuration."""
            settings: dict[str, t.JsonValue] = {
                "host": host,
                "port": port,
                "service_name": service_name,
                "username": username,
                "password": password,
            }
            settings.update(kwargs)
            return settings

        @staticmethod
        def create_test_singer_stream(
            stream_name: str,
            table_name: str,
            replication_method: str = "FULL_TABLE",
            **kwargs: t.JsonValue,
        ) -> t.JsonMapping:
            """Create test Singer stream configuration."""
            stream: dict[str, t.JsonValue] = {
                "stream_name": stream_name,
                "table_name": table_name,
                "replication_method": replication_method,
                "is_selected": True,
            }
            stream.update(kwargs)
            return stream

        @staticmethod
        def validate_oracle_connection_config(
            settings: t.JsonMapping,
        ) -> bool:
            """Validate Oracle connection configuration for testing."""
            required_fields = ["host", "port", "service_name", "username", "password"]
            return all(
                field in settings and settings[field] for field in required_fields
            )

        @staticmethod
        def generate_mock_oracle_data(
            table_name: str,
            row_count: int = 10,
            **kwargs: t.JsonValue,
        ) -> t.SequenceOf[t.JsonMapping]:
            """Generate mock Oracle data for testing."""
            data: list[t.JsonMapping] = []
            for i in range(row_count):
                row: dict[str, t.JsonValue] = {
                    "id": i + 1,
                    "name": f"Test Record {i + 1}",
                    "table_name": table_name,
                }
                row.update(kwargs)
                data.append(row)
            return data


u = TestsFlextTapOracleUtilities

__all__: list[str] = ["TestsFlextTapOracleUtilities", "u"]
