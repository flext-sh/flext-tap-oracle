"""Models for flext-tap-oracle tests - uses composition with TestsFlextModels.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT

"""

from __future__ import annotations

from typing import Annotated

from flext_tests import FlextTestsModels

from flext_tap_oracle import m, u


class TestsFlextTapOracleModels(FlextTestsModels, m):
    """Models for flext-tap-oracle tests - uses composition with TestsFlextModels.

    Architecture: Uses composition (not inheritance) with TestsFlextModels and m
    for flext-tap-oracle-specific model definitions.

    Access patterns:
    - TestsFlextTapOracleModels.Tests.* = flext_tests test models (via composition)
    - TestsFlextTapOracleModels.TapOracle.* = flext-tap-oracle-specific test models
    - TestsFlextTapOracleModels.Entity, .Value, etc. = m domain models (via composition)

    Rules:
    - Use composition, not inheritance (TestsFlextModels deprecates subclassing)
    - flext-tap-oracle-specific models go in TapOracle namespace
    - Generic models accessed via Tests namespace
    """

    class Tests(FlextTestsModels.Tests):
        """Tap Oracle test models - domain-specific for Oracle tap testing.

        Contains test models specific to Oracle tap functionality including:
        - Singer protocol test models
        - Oracle database test models
        - Stream processing test models
        - Configuration test models
        """

        class TestOracleConnection(m.Entity):
            """Test model for Oracle database connections."""

            host: Annotated[str, u.Field(description="Oracle database hostname")]
            port: Annotated[int, u.Field(description="Oracle database port")]
            service_name: Annotated[str, u.Field(description="Oracle service name")]
            username: Annotated[
                str,
                u.Field(description="Oracle database username"),
            ]
            password: Annotated[
                str,
                u.Field(description="Oracle database password"),
            ]

            @property
            def connection_string(self) -> str:
                """The Oracle connection string."""
                return f"oracle://{self.username}:***@{self.host}:{self.port}/{self.service_name}"

        class TestSingerStream(m.Entity):
            """Test model for Singer streams."""

            stream_name: Annotated[
                str,
                u.Field(description="Name of the Singer stream"),
            ]
            table_name: Annotated[
                str,
                u.Field(description="Name of the source table"),
            ]
            replication_method: Annotated[
                str,
                u.Field(description="Replication method for the stream"),
            ]
            is_selected: Annotated[
                bool,
                u.Field(description="Whether the stream is selected"),
            ] = True

        class TestOracleTable(m.Entity):
            """Test model for Oracle tables."""

            table_name: Annotated[
                str,
                u.Field(description="Name of the Oracle table"),
            ]
            schema_name: Annotated[
                str,
                u.Field(description="Schema containing the table"),
            ]
            column_count: Annotated[
                int,
                u.Field(description="Number of columns in the table"),
            ]
            row_count: Annotated[
                int | None,
                u.Field(description="Number of rows in the table"),
            ] = None

        class TestExtractionConfig(m.Entity):
            """Test model for extraction configurations."""

            batch_size: Annotated[
                int,
                u.Field(description="Number of rows per batch"),
            ]
            parallel_streams: Annotated[
                int,
                u.Field(description="Number of parallel streams for extraction"),
            ]
            timeout_seconds: Annotated[
                int,
                u.Field(description="Query timeout in seconds"),
            ]
            max_rows: Annotated[
                int | None,
                u.Field(description="Maximum number of rows to extract"),
            ] = None


m = TestsFlextTapOracleModels

__all__: list[str] = [
    "TestsFlextTapOracleModels",
    "m",
]
