"""Test configuration for flext-tap-oracle.

Provides pytest fixtures and configuration for testing Oracle Singer tap functionality
using real Oracle connections and Singer SDK patterns.


Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT

"""

from __future__ import annotations

import os
import socket
from collections.abc import Generator

import pytest
from flext_tests import FlextTestsDocker

from flext import FlextResult
from flext_tap_oracle import (
    FlextMeltanoTapOracleSettings,
    FlextOracleTapService,
    create_oracle_tap_config,
)


# Docker container management with FlextTestsDocker
@pytest.fixture(scope="session")
def docker_control() -> FlextTestsDocker:
    """Provide Docker control instance for tests."""
    return FlextTestsDocker()


@pytest.fixture(scope="session")
def shared_oracle_container(docker_control: FlextTestsDocker) -> Generator[str]:
    """Managed Oracle container using FlextTestsDocker with auto-start."""
    result = docker_control.start_container("flext-oracle-db-test")
    if result.is_failure:
        pytest.skip(f"Failed to start Oracle container: {result.error}")

    yield "flext-oracle-db-test"

    docker_control.stop_container("flext-oracle-db-test", remove=False)


# Test environment setup
@pytest.fixture(scope="session", autouse=True)
def oracle_shared_container_environment(shared_oracle_container: str) -> None:
    """Setup Oracle environment variables for shared container (pytest-oracle-xe)."""
    _ = shared_oracle_container  # Acknowledge parameter usage
    # Use the container name to ensure it's available
    _ = shared_oracle_container
    # Set Oracle environment variables for shared container on port 10521
    os.environ.update(
        {
            "FLEXT_TAP_ORACLE_HOST": "localhost",
            "FLEXT_TAP_ORACLE_PORT": "10521",
            "FLEXT_TAP_ORACLE_USERNAME": "system",
            "FLEXT_TAP_ORACLE_PASSWORD": "oracle",
            "FLEXT_TAP_ORACLE_SERVICE_NAME": "XE",
            "FLEXT_TAP_ORACLE_SCHEMA_NAME": "FLEXT_TEST",
        },
    )
    # Align generic ORACLE_* variables used by some tests
    os.environ.setdefault("ORACLE_HOST", os.environ["FLEXT_TAP_ORACLE_HOST"])
    os.environ.setdefault("ORACLE_PORT", os.environ["FLEXT_TAP_ORACLE_PORT"])
    os.environ.setdefault("ORACLE_USERNAME", os.environ["FLEXT_TAP_ORACLE_USERNAME"])
    os.environ.setdefault("ORACLE_PASSWORD", os.environ["FLEXT_TAP_ORACLE_PASSWORD"])
    os.environ.setdefault(
        "ORACLE_SERVICE_NAME",
        os.environ["FLEXT_TAP_ORACLE_SERVICE_NAME"],
    )


@pytest.fixture(autouse=True)
def set_test_environment() -> Generator[None]:
    """Set test environment variables."""
    os.environ["FLEXT_ENV"] = "test"
    os.environ["FLEXT_LOG_LEVEL"] = "debug"
    os.environ["SINGER_SDK_LOG_LEVEL"] = "DEBUG"
    os.environ["ORACLE_TAP_TEST_MODE"] = "true"
    yield
    # Cleanup
    os.environ.pop("FLEXT_ENV", None)
    os.environ.pop("FLEXT_LOG_LEVEL", None)
    os.environ.pop("SINGER_SDK_LOG_LEVEL", None)
    os.environ.pop("ORACLE_TAP_TEST_MODE", None)


def _can_connect(host: str, port: int, timeout: float = 0.5) -> bool:
    try:
        with socket.create_connection((host, port), timeout=timeout):
            return True
    except OSError:
        return False


@pytest.fixture(autouse=True)
def skip_e2e_if_no_oracle(request: pytest.FixtureRequest) -> None:
    """Skip E2E tests gracefully when Oracle is not available locally.

    We only skip tests under the e2e/ directory to avoid hiding other failures.
    """
    fspath = str(request.node.fspath) if hasattr(request.node, "fspath") else ""
    if "/e2e/" not in fspath and "\\e2e\\" not in fspath:
        return

    host = os.environ.get(
        "ORACLE_HOST",
        os.environ.get("FLEXT_TAP_ORACLE_HOST", "localhost"),
    )
    port_str = os.environ.get(
        "ORACLE_PORT",
        os.environ.get("FLEXT_TAP_ORACLE_PORT", "1521"),
    )
    try:
        port = int(port_str)
    except ValueError:
        port = 1521

    if not _can_connect(host, port):
        pytest.skip(
            f"Oracle indisponível em {host}:{port}. Ignorando E2E que requer DB.",
            allow_module_level=False,
        )


# Oracle connection fixtures
@pytest.fixture
def oracle_tap_config() -> dict[str, object]:
    """Oracle tap configuration for testing."""
    return {
        "host": "localhost",
        "port": 1521,
        "database": "ORCL",
        "username": "tap_user",
        "password": "tap_pass",
        "service_name": "XEPDB1",
        "default_replication_method": "INCREMENTAL",
        "filter_schemas": ["TAP_SCHEMA"],
        "batch_config": {
            "encoding": {
                "format": "jsonl",
                "compression": "gzip",
            },
        },
    }


@pytest.fixture
def oracle_tap(oracle_tap_config: dict[str, object]) -> FlextOracleTapService:
    """Oracle tap service instance for testing."""
    # Convert dict[str, object] to proper config and create service
    config_result = FlextResult[FlextMeltanoTapOracleSettings].ok(
        FlextMeltanoTapOracleSettings.get_global_instance().model_validate(
            oracle_tap_config,
        ),
    )
    if config_result.is_success:
        return FlextOracleTapService(config=config_result.value)

    # Fallback for test compatibility
    fallback_result = create_oracle_tap_config(
        oracle_params={
            "host": str(oracle_tap_config.get("host", "localhost")),
            "username": str(oracle_tap_config.get("username", "test")),
            "password": str(oracle_tap_config.get("password", "test")),
        },
    )
    if fallback_result.is_success:
        return FlextOracleTapService(config=fallback_result.value)

    error_msg = "Failed to create oracle tap service for testing"
    raise RuntimeError(error_msg)


# Singer protocol fixtures
@pytest.fixture
def singer_catalog() -> dict[str, object]:
    """Singer catalog for testing."""
    return {
        "streams": [
            {
                "tap_stream_id": "employees",
                "schema": {
                    "type": "object",
                    "properties": {
                        "id": {"type": "integer"},
                        "name": {"type": "string"},
                        "email": {"type": ["string", "null"]},
                        "department_id": {"type": ["integer", "null"]},
                        "hire_date": {"type": "string", "format": "date-time"},
                        "salary": {"type": "number"},
                    },
                },
                "metadata": [
                    {
                        "breadcrumb": [],
                        "metadata": {
                            "inclusion": "available",
                            "table-key-properties": ["id"],
                            "forced-replication-method": "INCREMENTAL",
                            "replication-key": "hire_date",
                        },
                    },
                    {
                        "breadcrumb": ["properties", "id"],
                        "metadata": {"inclusion": "automatic"},
                    },
                    {
                        "breadcrumb": ["properties", "name"],
                        "metadata": {"inclusion": "available"},
                    },
                ],
            },
            {
                "tap_stream_id": "departments",
                "schema": {
                    "type": "object",
                    "properties": {
                        "id": {"type": "integer"},
                        "name": {"type": "string"},
                        "manager_id": {"type": ["integer", "null"]},
                        "created_at": {"type": "string", "format": "date-time"},
                    },
                },
                "metadata": [
                    {
                        "breadcrumb": [],
                        "metadata": {
                            "inclusion": "available",
                            "table-key-properties": ["id"],
                            "forced-replication-method": "FULL_TABLE",
                        },
                    },
                ],
            },
        ],
    }


@pytest.fixture
def singer_state() -> dict[str, object]:
    """Singer state for testing."""
    return {
        "bookmarks": {
            "employees": {
                "replication_key": "hire_date",
                "replication_key_value": "2023-01-01T00:00:00Z",
                "version": 1,
            },
            "departments": {
                "version": 1,
            },
        },
    }


@pytest.fixture
def sample_oracle_tables() -> list[dict[str, object]]:
    """Sample Oracle table definitions for testing."""
    return [
        {
            "table_name": "EMPLOYEES",
            "owner": "TAP_SCHEMA",
            "table_type": "TABLE",
            "columns": [
                {
                    "column_name": "ID",
                    "data_type": "NUMBER",
                    "data_length": 22,
                    "data_precision": 10,
                    "data_scale": 0,
                    "nullable": "N",
                    "column_id": 1,
                },
                {
                    "column_name": "NAME",
                    "data_type": "VARCHAR2",
                    "data_length": 100,
                    "nullable": "N",
                    "column_id": 2,
                },
                {
                    "column_name": "EMAIL",
                    "data_type": "VARCHAR2",
                    "data_length": 255,
                    "nullable": "Y",
                    "column_id": 3,
                },
                {
                    "column_name": "HIRE_DATE",
                    "data_type": "TIMESTAMP",
                    "data_length": 11,
                    "nullable": "N",
                    "column_id": 4,
                },
            ],
            "primary_key": ["ID"],
            "indexes": [
                {
                    "index_name": "PK_EMPLOYEES",
                    "uniqueness": "UNIQUE",
                    "columns": ["ID"],
                },
                {
                    "index_name": "IDX_EMPLOYEES_EMAIL",
                    "uniqueness": "NONUNIQUE",
                    "columns": ["EMAIL"],
                },
            ],
        },
        {
            "table_name": "DEPARTMENTS",
            "owner": "TAP_SCHEMA",
            "table_type": "TABLE",
            "columns": [
                {
                    "column_name": "ID",
                    "data_type": "NUMBER",
                    "data_precision": 10,
                    "data_scale": 0,
                    "nullable": "N",
                    "column_id": 1,
                },
                {
                    "column_name": "NAME",
                    "data_type": "VARCHAR2",
                    "data_length": 100,
                    "nullable": "N",
                    "column_id": 2,
                },
            ],
            "primary_key": ["ID"],
        },
    ]


@pytest.fixture
def sample_oracle_data() -> dict[str, list[dict[str, object]]]:
    """Sample Oracle data for testing."""
    return {
        "employees": [
            {
                "id": 1,
                "name": "John Doe",
                "email": "john.doe@example.com",
                "department_id": 1,
                "hire_date": "2022-01-15T09:00:00Z",
                "salary": 75000.00,
            },
            {
                "id": 2,
                "name": "Jane Smith",
                "email": "jane.smith@example.com",
                "department_id": 2,
                "hire_date": "2022-03-01T09:00:00Z",
                "salary": 82000.00,
            },
            {
                "id": 3,
                "name": "Bob Johnson",
                "email": "bob.johnson@example.com",
                "department_id": 1,
                "hire_date": "2023-01-10T09:00:00Z",
                "salary": 68000.00,
            },
        ],
        "departments": [
            {
                "id": 1,
                "name": "Engineering",
                "manager_id": 1,
                "created_at": "2021-01-01T00:00:00Z",
            },
            {
                "id": 2,
                "name": "Marketing",
                "manager_id": 2,
                "created_at": "2021-01-01T00:00:00Z",
            },
        ],
    }


# Stream configuration fixtures
@pytest.fixture
def stream_config() -> dict[str, object]:
    """Stream configuration for testing."""
    return {
        "selected": True,
        "replication_method": "INCREMENTAL",
        "replication_key": "hire_date",
        "key_properties": ["id"],
        "batch_size": 1000,
        "datetime_error_treatment": "max",
    }


@pytest.fixture
def discovery_config() -> dict[str, object]:
    """Discovery configuration for testing."""
    return {
        "include_views": False,
        "include_system_tables": False,
        "filter_schemas": ["TAP_SCHEMA"],
        "filter_tables": None,
        "max_table_scan": 100,
        "discover_pk": True,
        "discover_fk": True,
    }


# SQL query fixtures
@pytest.fixture
def oracle_queries() -> dict[str, str]:
    """Oracle SQL queries for testing."""
    return {
        "list_tables": """

          SELECT table_name, owner, table_type
          FROM all_tables
          WHERE owner = :schema_name
          ORDER BY table_name
      """,
        "table_columns": """

          SELECT column_name, data_type, data_length, data_precision,
                 data_scale, nullable, column_id
          FROM all_tab_columns
          WHERE table_name = :table_name
          AND owner = :schema_name
          ORDER BY column_id
      """,
        "primary_keys": """

          SELECT cols.column_name
          FROM all_constraints cons
          JOIN all_cons_columns cols ON cons.constraint_name = cols.constraint_name
          WHERE cons.constraint_type = 'P'
          AND cons.table_name = :table_name
          AND cons.owner = :schema_name
          ORDER BY cols.position
      """,
        "select_with_replication_key": """

          SELECT {columns}
          FROM {schema}.{table}
          WHERE {replication_key} >= :bookmark_value
          ORDER BY {replication_key}
      """,
        "full_table_select": """

          SELECT {columns}
          FROM {schema}.{table}
          ORDER BY {key_properties}
      """,
    }


# Singer message fixtures
@pytest.fixture
def singer_schema_message() -> dict[str, object]:
    """Singer schema message for testing."""
    return {
        "type": "SCHEMA",
        "stream": "employees",
        "schema": {
            "type": "object",
            "properties": {
                "id": {"type": "integer"},
                "name": {"type": "string"},
                "email": {"type": ["string", "null"]},
                "hire_date": {"type": "string", "format": "date-time"},
            },
        },
        "key_properties": ["id"],
    }


@pytest.fixture
def singer_record_messages() -> list[dict[str, object]]:
    """Singer record messages for testing."""
    return [
        {
            "type": "RECORD",
            "stream": "employees",
            "record": {
                "id": 1,
                "name": "John Doe",
                "email": "john.doe@example.com",
                "hire_date": "2022-01-15T09:00:00Z",
            },
            "time_extracted": "2023-01-01T12:00:00Z",
        },
        {
            "type": "RECORD",
            "stream": "employees",
            "record": {
                "id": 2,
                "name": "Jane Smith",
                "email": "jane.smith@example.com",
                "hire_date": "2022-03-01T09:00:00Z",
            },
            "time_extracted": "2023-01-01T12:00:01Z",
        },
    ]


@pytest.fixture
def singer_state_message() -> dict[str, object]:
    """Singer state message for testing."""
    return {
        "type": "STATE",
        "value": {
            "bookmarks": {
                "employees": {
                    "replication_key": "hire_date",
                    "replication_key_value": "2023-01-01T00:00:00Z",
                    "version": 1,
                },
            },
        },
    }


# Performance test fixtures
@pytest.fixture
def performance_test_config() -> dict[str, object]:
    """Performance test configuration."""
    return {
        "large_table_rows": 100000,
        "batch_sizes": [100, 500, 1000, 5000],
        "concurrent_streams": 3,
        "memory_threshold": "1GB",
        "time_threshold": 300,  # 5 minutes
    }


# Error handling fixtures
@pytest.fixture
def error_scenarios() -> list[dict[str, object]]:
    """Error scenarios for testing."""
    return [
        {
            "name": "connection_failure",
            "error_type": "DatabaseError",
            "oracle_error": "ORA-12541",
            "message": "TNS:no listener",
            "recovery_strategy": "reconnect",
        },
        {
            "name": "invalid_table",
            "error_type": "ProgrammingError",
            "oracle_error": "ORA-00942",
            "message": "table or view does not exist",
            "recovery_strategy": "skip_table",
        },
        {
            "name": "insufficient_privileges",
            "error_type": "DatabaseError",
            "oracle_error": "ORA-00942",
            "message": "insufficient privileges",
            "recovery_strategy": "log_warning",
        },
        {
            "name": "data_type_conversion",
            "error_type": "DataError",
            "oracle_error": "ORA-01722",
            "message": "invalid number",
            "recovery_strategy": "null_value",
        },
    ]


# Pytest markers for test categorization
def pytest_configure(config: pytest.Config) -> None:
    """Configure pytest markers."""
    config.addinivalue_line("markers", "unit: Unit tests")
    config.addinivalue_line("markers", "integration: Integration tests")
    config.addinivalue_line("markers", "e2e: End-to-end tests")
    config.addinivalue_line("markers", "oracle: Oracle database tests")
    config.addinivalue_line("markers", "singer: Singer protocol tests")
    config.addinivalue_line("markers", "discovery: Schema discovery tests")
    config.addinivalue_line("markers", "extraction: Data extraction tests")
    config.addinivalue_line("markers", "performance: Performance tests")
    config.addinivalue_line("markers", "slow: Slow tests")


# Mock services
@pytest.fixture
def mock_oracle_tap() -> type[object]:
    """Mock Oracle tap for testing."""

    class MockOracleTap:
        def __init__(self, config: dict[str, object]) -> None:
            """Initialize the instance."""
            self.config = config
            self._catalog = None
            self.__state: dict[str, object] = {}

        def discover(self) -> dict[str, object]:
            """Discover schema using mock data."""
            return {
                "streams": [
                    {
                        "tap_stream_id": "employees",
                        "schema": {
                            "type": "object",
                            "properties": {
                                "id": {"type": "integer"},
                                "name": {"type": "string"},
                            },
                        },
                        "metadata": [],
                    },
                ],
            }

        def sync(
            self,
            catalog: dict[str, object],
            _state: dict[str, object],
        ) -> Generator[dict[str, object]]:
            """Sync data using mock extraction."""
            if not isinstance(catalog, dict) or "streams" not in catalog:
                return
            streams = catalog["streams"]
            if not isinstance(streams, list):
                return
            for stream in streams:
                if stream.get("metadata", [{}])[0].get("metadata", {}).get("selected"):
                    yield {
                        "type": "SCHEMA",
                        "stream": stream["tap_stream_id"],
                        "schema": stream["schema"],
                        "key_properties": ["id"],
                    }

                    yield {
                        "type": "RECORD",
                        "stream": stream["tap_stream_id"],
                        "record": {"id": 1, "name": "Test Record"},
                        "time_extracted": "2023-01-01T12:00:00Z",
                    }

                    yield {
                        "type": "STATE",
                        "value": {
                            "bookmarks": {
                                stream["tap_stream_id"]: {
                                    "version": 1,
                                    "replication_key_value": "2023-01-01T12:00:00Z",
                                },
                            },
                        },
                    }

    return MockOracleTap


@pytest.fixture
def mock_oracle_connection() -> type[object]:
    """Mock Oracle connection for testing."""

    class MockOracleConnection:
        def __init__(self, config: dict[str, object]) -> None:
            """Initialize the instance."""
            self.config = config
            self.connected = False

        def connect(self) -> bool:
            self.connected = True
            return True

        def disconnect(self) -> bool:
            self.connected = False
            return True

        def execute_query(
            self,
            query: str,
            _parameters: dict[str, object] | None = None,
        ) -> list[dict[str, object]]:
            """Execute query and return mock results using Strategy Pattern."""
            return self._get_query_strategy(query).execute()

        def _get_query_strategy(self, query: str) -> _MockQueryStrategy:
            """Get appropriate query strategy - Factory Method Pattern."""
            if "all_tables" in query:
                return _TablesQueryStrategy()
            if "all_tab_columns" in query:
                return _ColumnsQueryStrategy()
            return _DefaultQueryStrategy()

        def get_table_schema(self, table_name: str) -> dict[str, object]:
            """Get table schema information."""
            return {
                "table_name": table_name,
                "columns": [
                    {"name": "id", "type": "NUMBER", "nullable": False},
                    {"name": "name", "type": "VARCHAR2", "nullable": False},
                ],
                "primary_key": ["id"],
            }

    return MockOracleConnection


class _MockQueryStrategy:
    """Base class for mock query strategies - Strategy Pattern."""

    def execute(self) -> list[dict[str, object]]:
        """Execute mock query and return results."""
        raise NotImplementedError


class _TablesQueryStrategy(_MockQueryStrategy):
    """Strategy for tables query - Single Responsibility."""

    def execute(self) -> list[dict[str, object]]:
        """Return mock table data."""
        return [
            {
                "table_name": "EMPLOYEES",
                "owner": "TAP_SCHEMA",
                "table_type": "TABLE",
            },
            {
                "table_name": "DEPARTMENTS",
                "owner": "TAP_SCHEMA",
                "table_type": "TABLE",
            },
        ]


class _ColumnsQueryStrategy(_MockQueryStrategy):
    """Strategy for columns query - Single Responsibility."""

    def execute(self) -> list[dict[str, object]]:
        """Return mock column data."""
        return [
            {
                "column_name": "ID",
                "data_type": "NUMBER",
                "data_length": 22,
                "nullable": "N",
                "column_id": 1,
            },
            {
                "column_name": "NAME",
                "data_type": "VARCHAR2",
                "data_length": 100,
                "nullable": "N",
                "column_id": 2,
            },
        ]


class _DefaultQueryStrategy(_MockQueryStrategy):
    """Default strategy for generic queries - Single Responsibility."""

    def execute(self) -> list[dict[str, object]]:
        """Return mock default data."""
        return [{"id": 1, "name": "Test Record"}]
