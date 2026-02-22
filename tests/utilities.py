"""Utilities for flext-tap-oracle tests - uses composition with FlextTestsUtilities.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT

"""

from __future__ import annotations

from flext_tests import FlextTestsUtilities

from flext_tap_oracle import t


class TestsFlextMeltanoTapOracleUtilities(FlextTestsUtilities):
    """Utilities for flext-tap-oracle tests - uses composition with FlextTestsUtilities.

    Architecture: Uses composition (not inheritance) with FlextTestsUtilities and FlextMeltanoTapOracleUtilities
    for flext-tap-oracle-specific utility definitions.

    Access patterns:
    - TestsFlextMeltanoTapOracleUtilities.Tests.* = flext_tests test utilities (via composition)
    - TestsFlextMeltanoTapOracleUtilities.TapOracle.* = flext-tap-oracle-specific test utilities
    - TestsFlextMeltanoTapOracleUtilities.* = FlextTestsUtilities methods (via composition)

    Rules:
    - Use composition, not inheritance (FlextTestsUtilities deprecates subclassing)
    - flext-tap-oracle-specific utilities go in TapOracle namespace
    - Generic utilities accessed via Tests namespace
    """

    # Composition: expose FlextTestsUtilities namespaces
    Tests = FlextTestsUtilities.Tests

    # TapOracle-specific test utilities namespace
    class TapOracle:
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
            **kwargs: t.GeneralValueType,
        ) -> dict[str, t.GeneralValueType]:
            """Create test Oracle configuration."""
            config = {
                "host": host,
                "port": port,
                "service_name": service_name,
                "username": username,
                "password": password,
            }
            config.update(kwargs)
            return config

        @staticmethod
        def create_test_singer_stream(
            stream_name: str,
            table_name: str,
            replication_method: str = "FULL_TABLE",
            **kwargs: t.GeneralValueType,
        ) -> dict[str, t.GeneralValueType]:
            """Create test Singer stream configuration."""
            stream = {
                "stream_name": stream_name,
                "table_name": table_name,
                "replication_method": replication_method,
                "is_selected": True,
            }
            stream.update(kwargs)
            return stream

        @staticmethod
        def validate_oracle_connection_config(
            config: dict[str, t.GeneralValueType],
        ) -> bool:
            """Validate Oracle connection configuration for testing."""
            required_fields = ["host", "port", "service_name", "username", "password"]
            return all(field in config and config[field] for field in required_fields)

        @staticmethod
        def generate_mock_oracle_data(
            table_name: str,
            row_count: int = 10,
            **kwargs: t.GeneralValueType,
        ) -> list[dict[str, t.GeneralValueType]]:
            """Generate mock Oracle data for testing."""
            data = []
            for i in range(row_count):
                row = {"id": i + 1, "name": f"Test Record {i + 1}"}
                row.update(kwargs)
                data.append(row)
            return data


# Alias for simplified usage
tu = TestsFlextMeltanoTapOracleUtilities

__all__ = [
    "TestsFlextMeltanoTapOracleUtilities",
    "tu",
]
