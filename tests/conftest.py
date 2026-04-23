"""Test configuration for flext-tap-oracle.

Provides pytest fixtures and configuration for testing Oracle Singer tap functionality
using real Oracle connections and Singer SDK patterns.


Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT

"""

from __future__ import annotations

import os
import socket
from abc import ABC, abstractmethod
from collections.abc import (
    Generator,
    Mapping,
    Sequence,
)
from typing import TypeGuard, override

import pytest
from flext_tests import tk

from flext_tap_oracle import FlextTapOracleService, FlextTapOracleSettings
from tests import t


@pytest.fixture
def tap_oracle_settings() -> FlextTapOracleSettings:
    """Provide clean FlextTapOracleSettings for tap-oracle tests."""
    return FlextTapOracleSettings(debug=True)


@pytest.fixture(scope="session")
def docker_control() -> tk:
    """Provide Docker control instance for tests."""
    return tk()


@pytest.fixture(scope="session")
def shared_oracle_container(docker_control: tk) -> str:
    """Managed Oracle container using tk with auto-start."""
    _ = docker_control
    return "flext-oracle-db-test"


@pytest.fixture(scope="session", autouse=True)
def oracle_shared_container_environment(shared_oracle_container: str) -> None:
    """Setup Oracle environment variables for shared container (pytest-oracle-xe)."""
    _ = shared_oracle_container
    _ = shared_oracle_container
    os.environ.update({
        "FLEXT_TAP_ORACLE_HOST": "localhost",
        "FLEXT_TAP_ORACLE_PORT": "10521",
        "FLEXT_TAP_ORACLE_USERNAME": "system",
        "FLEXT_TAP_ORACLE_PASSWORD": "oracle",
        "FLEXT_TAP_ORACLE_SERVICE_NAME": "XE",
        "FLEXT_TAP_ORACLE_SCHEMA_NAME": "FLEXT_TEST",
    })
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
    os.environ["FLEXT_LOG_LEVEL"] = "DEBUG"
    os.environ["SINGER_SDK_LOG_LEVEL"] = "DEBUG"
    os.environ["ORACLE_TAP_TEST_MODE"] = "true"
    yield
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


def _is_json_mapping_sequence(
    value: t.JsonValue | None,
) -> TypeGuard[list[t.JsonMapping]]:
    return isinstance(value, list) and all(isinstance(item, dict) for item in value)


@pytest.fixture(autouse=True)
def skip_e2e_if_no_oracle() -> None:
    """Skip E2E tests gracefully when Oracle is not available locally.

    We only skip tests under the e2e/ directory to avoid hiding other failures.
    """
    fspath = os.environ.get("PYTEST_CURRENT_TEST", "")
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


@pytest.fixture
def oracle_tap_config() -> t.JsonMapping:
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
        "batch_config": {"encoding": {"format": "jsonl", "compression": "gzip"}},
    }


@pytest.fixture
def oracle_tap(
    oracle_tap_config: t.JsonMapping,
) -> FlextTapOracleService:
    """Oracle tap service instance for testing."""
    settings = FlextTapOracleSettings.model_validate(oracle_tap_config)
    return FlextTapOracleService(settings=settings)


@pytest.fixture
def singer_catalog() -> t.JsonMapping:
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
def singer_state() -> t.JsonMapping:
    """Singer state for testing."""
    return {
        "bookmarks": {
            "employees": {
                "replication_key": "hire_date",
                "replication_key_value": "2023-01-01T00:00:00Z",
                "version": 1,
            },
            "departments": {"version": 1},
        },
    }


@pytest.fixture
def sample_oracle_tables() -> Sequence[t.JsonMapping]:
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
def sample_oracle_data() -> Mapping[str, Sequence[t.JsonMapping]]:
    """Sample Oracle data for testing."""
    return {
        "employees": [
            {
                "id": 1,
                "name": "John Doe",
                "email": "john.doe@example.com",
                "department_id": 1,
                "hire_date": "2022-01-15T09:00:00Z",
                "salary": 75000.0,
            },
            {
                "id": 2,
                "name": "Jane Smith",
                "email": "jane.smith@example.com",
                "department_id": 2,
                "hire_date": "2022-03-01T09:00:00Z",
                "salary": 82000.0,
            },
            {
                "id": 3,
                "name": "Bob Johnson",
                "email": "bob.johnson@example.com",
                "department_id": 1,
                "hire_date": "2023-01-10T09:00:00Z",
                "salary": 68000.0,
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


@pytest.fixture
def stream_config() -> t.JsonMapping:
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
def discovery_config() -> t.JsonMapping:
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


@pytest.fixture
def oracle_queries() -> t.StrMapping:
    """Oracle SQL queries for testing."""
    return {
        "list_tables": "\n\n          SELECT table_name, owner, table_type\n          FROM all_tables\n          WHERE owner = :schema_name\n          ORDER BY table_name\n      ",
        "table_columns": "\n\n          SELECT column_name, data_type, data_length, data_precision,\n                 data_scale, nullable, column_id\n          FROM all_tab_columns\n          WHERE table_name = :table_name\n          AND owner = :schema_name\n          ORDER BY column_id\n      ",
        "primary_keys": "\n\n          SELECT cols.column_name\n          FROM all_constraints cons\n          JOIN all_cons_columns cols ON cons.constraint_name = cols.constraint_name\n          WHERE cons.constraint_type = 'P'\n          AND cons.table_name = :table_name\n          AND cons.owner = :schema_name\n          ORDER BY cols.position\n      ",
        "select_with_replication_key": "\n\n          SELECT {columns}\n          FROM {schema}.{table}\n          WHERE {replication_key} >= :bookmark_value\n          ORDER BY {replication_key}\n      ",
        "full_table_select": "\n\n          SELECT {columns}\n          FROM {schema}.{table}\n          ORDER BY {key_properties}\n      ",
    }


@pytest.fixture
def singer_schema_message() -> t.JsonMapping:
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
def singer_record_messages() -> Sequence[t.JsonMapping]:
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
def singer_state_message() -> t.JsonMapping:
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


@pytest.fixture
def performance_test_config() -> t.JsonMapping:
    """Performance test configuration."""
    return {
        "large_table_rows": 100000,
        "batch_sizes": [100, 500, 1000, 5000],
        "concurrent_streams": 3,
        "memory_threshold": "1GB",
        "time_threshold": 300,
    }


@pytest.fixture
def error_scenarios() -> Sequence[t.JsonMapping]:
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


@pytest.fixture
def mock_oracle_tap() -> type:
    """Mock Oracle tap for testing."""

    class MockOracleTap:
        def __init__(self, settings: t.JsonMapping) -> None:
            """Initialize the instance."""
            self.settings = settings
            self._catalog: t.JsonMapping | None = None
            self.__state: t.JsonMapping = {}

        def discover(self) -> t.JsonMapping:
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
            catalog: t.JsonMapping,
            state: t.JsonMapping,
        ) -> Generator[t.JsonMapping]:
            """Sync data using mock extraction."""
            streams_raw = catalog.get("streams")
            if not _is_json_mapping_sequence(streams_raw):
                return
            for stream_raw in streams_raw:
                metadata_raw = stream_raw.get("metadata")
                if not _is_json_mapping_sequence(metadata_raw) or not metadata_raw:
                    continue
                first_metadata = metadata_raw[0]
                metadata_map_raw = first_metadata.get("metadata")
                if not isinstance(metadata_map_raw, dict):
                    continue
                metadata_map = metadata_map_raw
                if not bool(metadata_map.get("selected")):
                    continue
                stream_id_raw = stream_raw.get("tap_stream_id")
                schema_raw = stream_raw.get("schema")
                if not isinstance(stream_id_raw, str):
                    continue
                if not isinstance(schema_raw, dict):
                    continue
                yield {
                    "type": "SCHEMA",
                    "stream": stream_id_raw,
                    "schema": schema_raw,
                    "key_properties": ["id"],
                }
                yield {
                    "type": "RECORD",
                    "stream": stream_id_raw,
                    "record": {"id": 1, "name": "Test Record"},
                    "time_extracted": "2023-01-01T12:00:00Z",
                }
                yield {
                    "type": "STATE",
                    "value": {
                        "bookmarks": {
                            stream_id_raw: {
                                "version": 1,
                                "replication_key_value": "2023-01-01T12:00:00Z",
                            },
                        },
                    },
                }

    return MockOracleTap


@pytest.fixture
def mock_oracle_connection() -> type:
    """Mock Oracle connection for testing."""

    class MockOracleConnection:
        def __init__(self, settings: t.JsonMapping) -> None:
            """Initialize the instance."""
            self.settings = settings
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
            _parameters: t.JsonMapping | None = None,
        ) -> Sequence[t.JsonMapping]:
            """Execute query and return mock results using Strategy Pattern."""
            return self._get_query_strategy(query).execute()

        def _get_query_strategy(self, query: str) -> _MockQueryStrategy:
            """Get appropriate query strategy - Factory Method Pattern."""
            if "all_tables" in query:
                return _TablesQueryStrategy()
            if "all_tab_columns" in query:
                return _ColumnsQueryStrategy()
            return _DefaultQueryStrategy()

        def get_table_schema(self, table_name: str) -> t.JsonMapping:
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


class _MockQueryStrategy(ABC):
    """Base class for mock query strategies - Strategy Pattern."""

    @abstractmethod
    def execute(self) -> Sequence[t.JsonMapping]:
        """Execute mock query and return results."""


class _TablesQueryStrategy(_MockQueryStrategy):
    """Strategy for tables query - Single Responsibility."""

    @override
    def execute(self) -> Sequence[t.JsonMapping]:
        """Return mock table data."""
        return [
            {"table_name": "EMPLOYEES", "owner": "TAP_SCHEMA", "table_type": "TABLE"},
            {"table_name": "DEPARTMENTS", "owner": "TAP_SCHEMA", "table_type": "TABLE"},
        ]


class _ColumnsQueryStrategy(_MockQueryStrategy):
    """Strategy for columns query - Single Responsibility."""

    @override
    def execute(self) -> Sequence[t.JsonMapping]:
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

    @override
    def execute(self) -> Sequence[t.JsonMapping]:
        """Return mock default data."""
        return [{"id": 1, "name": "Test Record"}]
