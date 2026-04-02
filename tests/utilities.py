"""Utilities for flext-tap-oracle tests - uses composition with FlextTestsUtilities.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT

"""

from __future__ import annotations

from collections.abc import Sequence

from flext_tests import FlextTestsUtilities

from flext_core import FlextTypes as _t
from flext_tap_oracle import FlextTapOracleUtilities
from tests import t


class FlextTapOracleTestUtilities(FlextTestsUtilities, FlextTapOracleUtilities):
    """Utilities for flext-tap-oracle tests - uses composition with FlextTestsUtilities.

    Architecture: Uses composition (not inheritance) with FlextTestsUtilities and FlextTapOracleUtilities
    for flext-tap-oracle-specific utility definitions.

    Access patterns:
    - FlextTapOracleTestUtilities.Tests.* = flext_tests test utilities (via composition)
    - FlextTapOracleTestUtilities.TapOracle.* = flext-tap-oracle-specific test utilities
    - FlextTapOracleTestUtilities.* = FlextTestsUtilities methods (via composition)

    Rules:
    - Use composition, not inheritance (FlextTestsUtilities deprecates subclassing)
    - flext-tap-oracle-specific utilities go in TapOracle namespace
    - Generic utilities accessed via Tests namespace
    """

    class TapOracle(FlextTapOracleUtilities.TapOracle):
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
            **kwargs: _t.Scalar,
        ) -> t.ContainerMapping:
            """Create test Oracle configuration."""
            config: t.MutableContainerMapping = {
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
            **kwargs: _t.Scalar,
        ) -> t.ContainerMapping:
            """Create test Singer stream configuration."""
            stream: t.MutableContainerMapping = {
                "stream_name": stream_name,
                "table_name": table_name,
                "replication_method": replication_method,
                "is_selected": True,
            }
            stream.update(kwargs)
            return stream

        @staticmethod
        def validate_oracle_connection_config(
            config: t.ContainerMapping,
        ) -> bool:
            """Validate Oracle connection configuration for testing."""
            required_fields = ["host", "port", "service_name", "username", "password"]
            return all(field in config and config[field] for field in required_fields)

        @staticmethod
        def generate_mock_oracle_data(
            table_name: str,
            row_count: int = 10,
            **kwargs: _t.Scalar,
        ) -> Sequence[t.ContainerMapping]:
            """Generate mock Oracle data for testing."""
            data: list[t.ContainerMapping] = []
            for i in range(row_count):
                row: t.MutableContainerMapping = {
                    "id": i + 1,
                    "name": f"Test Record {i + 1}",
                    "table_name": table_name,
                }
                row.update(kwargs)
                data.append(row)
            return data


u = FlextTapOracleTestUtilities
__all__ = ["FlextTapOracleTestUtilities", "u"]
