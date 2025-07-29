"""End-to-End tests for FLEXT Oracle Tap with real Oracle Database.

# Constants
EXPECTED_BULK_SIZE = 2

These tests require a running Oracle Database instance and verify
complete functionality of the tap against real Oracle data.
"""

from __future__ import annotations

import json
import os
import subprocess

import pytest

from flext_db_oracle import FlextDbOracleConfig as OracleConfig
from flext_db_oracle.application import FlextDbOracleConnectionService as OracleConnectionService, FlextDbOracleQueryService as OracleQueryService


class TestOracleE2E:
    """End-to-End tests for Oracle Database tap."""

    @pytest.fixture(scope="class")
    def oracle_config(self) -> OracleConfig:
        """Create Oracle configuration from environment."""
        return OracleConfig(
            host=os.getenv("ORACLE_HOST", "localhost"),
            port=int(os.getenv("ORACLE_PORT", "1521")),
            sid=None,
            service_name=os.getenv("ORACLE_SERVICE_NAME", "TESTDB"),
            username=os.getenv("ORACLE_USERNAME", "flext_test"),
            password=os.getenv("ORACLE_PASSWORD", "flext_test"),
            protocol="tcp",
            pool_min_size=1,
            pool_max_size=10,
            pool_increment=1,
            query_timeout=300,
            fetch_size=10000,
            connect_timeout=60,
            retry_attempts=3,
            retry_delay=1,
        )

    @pytest.fixture(scope="class")
    def connection_service(
        self, oracle_config: OracleConfig
    ) -> OracleConnectionService:
        """Create Oracle connection service."""
        return OracleConnectionService(oracle_config)

    @pytest.fixture(scope="class")
    def query_service(
        self, connection_service: OracleConnectionService
    ) -> OracleQueryService:
        """Create Oracle query service."""
        return OracleQueryService(connection_service)

    @pytest.mark.asyncio
    async def test_connection_health(
        self, connection_service: OracleConnectionService
    ) -> None:
        """Test that we can connect to Oracle database."""
        result = await connection_service.test_connection()
        assert result.success, f"Connection failed: {result.error}"

    @pytest.mark.asyncio
    async def test_create_test_data(self, query_service: OracleQueryService) -> None:
        """Create test tables and data for E2E testing."""
        # Create test table
        create_table_sql = """
        CREATE TABLE EMPLOYEES (
            ID NUMBER PRIMARY KEY,
            NAME VARCHAR2(100) NOT NULL,
            EMAIL VARCHAR2(255) UNIQUE,
            DEPARTMENT VARCHAR2(50),
            SALARY NUMBER(10,2),
            HIRE_DATE DATE,
            ACTIVE NUMBER(1) DEFAULT 1
        )
        """

        # Drop table if exists
        drop_sql = "DROP TABLE EMPLOYEES"
        try:
            await query_service.execute_query(drop_sql)
        except (RuntimeError, ValueError, TypeError):
            pass  # Table might not exist

        # Create table
        result = await query_service.execute_query(create_table_sql)
        assert result.success, f"Failed to create table: {result.error}"

        # Insert test data
        insert_sql = """
        INSERT INTO EMPLOYEES (ID, NAME, EMAIL, DEPARTMENT, SALARY, HIRE_DATE, ACTIVE)
        VALUES (:id, :name, :email, :department, :salary, TO_DATE(:hire_date, 'YYYY-MM-DD'), :active)
        """

        test_data = [
            (
                1,
                "John Doe",
                "john.doe@company.com",
                "Engineering",
                75000.00,
                "2023-01-15",
                1,
            ),
            (
                2,
                "Jane Smith",
                "jane.smith@company.com",
                "Marketing",
                65000.00,
                "2023-02-20",
                1,
            ),
            (
                3,
                "Bob Johnson",
                "bob.johnson@company.com",
                "Sales",
                55000.00,
                "2023-03-10",
                0,
            ),
            (
                4,
                "Alice Brown",
                "alice.brown@company.com",
                "Engineering",
                80000.00,
                "2023-01-05",
                1,
            ),
            (
                5,
                "Charlie Wilson",
                "charlie.wilson@company.com",
                "HR",
                60000.00,
                "2023-04-01",
                1,
            ),
        ]

        for row in test_data:
            # Convert tuple to dict for query parameters
            params = {
                "id": row[0],
                "name": row[1],
                "email": row[2],
                "department": row[3],
                "salary": row[4],
                "hire_date": row[5],
                "active": row[6],
            }
            result = await query_service.execute_query(insert_sql, params)
            assert result.success, f"Failed to insert row {row}: {result.error}"

    def test_tap_discovery(self) -> None:
        """Test tap stream discovery."""
        config = {
            "connection_type": "database",
            "host": os.getenv("ORACLE_HOST", "localhost"),
            "port": int(os.getenv("ORACLE_PORT", "1521")),
            "service_name": os.getenv("ORACLE_SERVICE_NAME", "TESTDB"),
            "username": os.getenv("ORACLE_USERNAME", "flext_test"),
            "password": os.getenv("ORACLE_PASSWORD", "flext_test"),
            "schema": os.getenv("ORACLE_SCHEMA", "FLEXT_TEST"),
            "tables": ["EMPLOYEES"],
        }

        # Write config file
        with open("/tmp/tap_config.json", "w") as f:
            json.dump(config, f)

        # Run discovery
        result = subprocess.run(
            [
                "poetry",
                "run",
                "tap-oracle",
                "--config",
                "/tmp/tap_config.json",
                "--discover",
            ],
            check=False,
            capture_output=True,
            text=True,
            timeout=60,
        )

        if result.returncode != 0, f"Discovery failed: {result.stderr}":

            raise AssertionError(f"Expected {0, f"Discovery failed: {result.stderr}"}, got {result.returncode}")

        # Parse catalog
        catalog = json.loads(result.stdout)
        if "streams" not in catalog:
            raise AssertionError(f"Expected {"streams"} in {catalog}")

        # Find employees stream
        employees_stream = None
        for stream in catalog["streams"]:
            if stream["tap_stream_id"] == "EMPLOYEES":
                employees_stream = stream
                break

        if employees_stream is not None, "EMPLOYEES stream not found not in catalog":

            raise AssertionError(f"Expected {employees_stream is not None, "EMPLOYEES stream not found} in {catalog"}")

        # Verify schema
        schema = employees_stream["schema"]
        if "properties" not in schema:
            raise AssertionError(f"Expected {"properties"} in {schema}")

        # Check expected columns
        expected_columns = [
            "ID",
            "NAME",
            "EMAIL",
            "DEPARTMENT",
            "SALARY",
            "HIRE_DATE",
            "ACTIVE",
        ]
        for col in expected_columns:
            if col in schema["properties"], f"Column {col} not found not in schema":
                raise AssertionError(f"Expected {col in schema["properties"], f"Column {col} not found} in {schema"}")

    def test_tap_extraction(self) -> None:
        """Test full data extraction."""
        config = {
            "connection_type": "database",
            "host": os.getenv("ORACLE_HOST", "localhost"),
            "port": int(os.getenv("ORACLE_PORT", "1521")),
            "service_name": os.getenv("ORACLE_SERVICE_NAME", "TESTDB"),
            "username": os.getenv("ORACLE_USERNAME", "flext_test"),
            "password": os.getenv("ORACLE_PASSWORD", "flext_test"),
            "schema": os.getenv("ORACLE_SCHEMA", "FLEXT_TEST"),
            "tables": ["EMPLOYEES"],
            "batch_size": 1000,
        }

        # Create catalog with selected stream
        catalog = {
            "streams": [
                {
                    "tap_stream_id": "EMPLOYEES",
                    "schema": {
                        "type": "object",
                        "properties": {
                            "ID": {"type": "integer"},
                            "NAME": {"type": "string"},
                            "EMAIL": {"type": "string"},
                            "DEPARTMENT": {"type": "string"},
                            "SALARY": {"type": "number"},
                            "HIRE_DATE": {"type": "string", "format": "date-time"},
                            "ACTIVE": {"type": "integer"},
                        },
                    },
                    "metadata": [
                        {
                            "breadcrumb": [],
                            "metadata": {"inclusion": "available", "selected": True},
                        }
                    ],
                }
            ]
        }

        # Write files
        with open("/tmp/tap_config.json", "w") as f:
            json.dump(config, f)
        with open("/tmp/catalog.json", "w") as f:
            json.dump(catalog, f)

        # Run extraction
        result = subprocess.run(
            [
                "poetry",
                "run",
                "tap-oracle",
                "--config",
                "/tmp/tap_config.json",
                "--catalog",
                "/tmp/catalog.json",
            ],
            check=False,
            capture_output=True,
            text=True,
            timeout=120,
        )

        if result.returncode != 0, f"Extraction failed: {result.stderr}":

            raise AssertionError(f"Expected {0, f"Extraction failed: {result.stderr}"}, got {result.returncode}")

        # Parse output lines
        lines = result.stdout.strip().split("\n")
        schema_messages = []
        record_messages = []
        state_messages = []

        for line in lines:
            if line.strip():
                message = json.loads(line)
                if message["type"] == "SCHEMA":
                    schema_messages.append(message)
                elif message["type"] == "RECORD":
                    record_messages.append(message)
                elif message["type"] == "STATE":
                    state_messages.append(message)

        # Verify schema message
        if len(schema_messages) < 1, "No schema messages found":
            raise AssertionError(f"Expected {len(schema_messages)} >= {1, "No schema messages found"}")
        schema_msg = schema_messages[0]
        if schema_msg["stream"] != "EMPLOYEES":
            raise AssertionError(f"Expected {"EMPLOYEES"}, got {schema_msg["stream"]}")

        # Verify record messages
        if len(record_messages) != 5, (:
            raise AssertionError(f"Expected {5, (}, got {len(record_messages)}")
            f"Expected 5 records, got {len(record_messages)}"
        )

        # Verify record content
        record_ids = {rec["record"]["ID"] for rec in record_messages}
        if record_ids != {1, 2, 3, 4, 5}, f"Unexpected record IDs: {record_ids}":
            raise AssertionError(f"Expected {{1, 2, 3, 4, 5}, f"Unexpected record IDs: {record_ids}"}, got {record_ids}")

        # Verify specific record
        john_doe = next(
            rec for rec in record_messages if rec["record"]["NAME"] == "John Doe"
        )
        if john_doe["record"]["EMAIL"] != "john.doe@company.com":
            raise AssertionError(f"Expected {"john.doe@company.com"}, got {john_doe["record"]["EMAIL"]}")
        assert john_doe["record"]["DEPARTMENT"] == "Engineering"
        if john_doe["record"]["SALARY"] != 75000.00:
            raise AssertionError(f"Expected {75000.00}, got {john_doe["record"]["SALARY"]}")
        assert john_doe["record"]["ACTIVE"] == 1

    @pytest.mark.asyncio
    async def test_incremental_extraction(
        self, query_service: OracleQueryService
    ) -> None:
        """Test incremental extraction with bookmarks."""
        # Add more test data with different dates
        insert_sql = """
        INSERT INTO EMPLOYEES (ID, NAME, EMAIL, DEPARTMENT, SALARY, HIRE_DATE, ACTIVE)
        VALUES (:id, :name, :email, :department, :salary, TO_DATE(:hire_date, 'YYYY-MM-DD'), :active)
        """

        new_data = [
            (
                6,
                "David Lee",
                "david.lee@company.com",
                "Engineering",
                85000.00,
                "2024-01-15",
                1,
            ),
            (
                7,
                "Emma Davis",
                "emma.davis@company.com",
                "Marketing",
                70000.00,
                "2024-02-20",
                1,
            ),
        ]

        for row in new_data:
            # Convert tuple to dict for query parameters
            params = {
                "id": row[0],
                "name": row[1],
                "email": row[2],
                "department": row[3],
                "salary": row[4],
                "hire_date": row[5],
                "active": row[6],
            }
            result = await query_service.execute_query(insert_sql, params)
            assert result.success, (
                f"Failed to insert incremental row {row}: {result.error}"
            )

        # Test incremental extraction with state
        config = {
            "connection_type": "database",
            "host": os.getenv("ORACLE_HOST", "localhost"),
            "port": int(os.getenv("ORACLE_PORT", "1521")),
            "service_name": os.getenv("ORACLE_SERVICE_NAME", "TESTDB"),
            "username": os.getenv("ORACLE_USERNAME", "flext_test"),
            "password": os.getenv("ORACLE_PASSWORD", "flext_test"),
            "schema": os.getenv("ORACLE_SCHEMA", "FLEXT_TEST"),
            "tables": ["EMPLOYEES"],
        }

        catalog = {
            "streams": [
                {
                    "tap_stream_id": "EMPLOYEES",
                    "schema": {
                        "type": "object",
                        "properties": {
                            "ID": {"type": "integer"},
                            "NAME": {"type": "string"},
                            "EMAIL": {"type": "string"},
                            "DEPARTMENT": {"type": "string"},
                            "SALARY": {"type": "number"},
                            "HIRE_DATE": {"type": "string", "format": "date-time"},
                            "ACTIVE": {"type": "integer"},
                        },
                    },
                    "metadata": [
                        {
                            "breadcrumb": [],
                            "metadata": {
                                "inclusion": "available",
                                "selected": True,
                                "replication-method": "INCREMENTAL",
                                "replication-key": "ID",
                            },
                        }
                    ],
                }
            ]
        }

        # State to simulate previous extraction (up to ID 5)
        state = {
            "bookmarks": {
                "EMPLOYEES": {"replication_key": "ID", "replication_key_value": 5}
            }
        }

        # Write files
        with open("/tmp/tap_config_inc.json", "w") as f:
            json.dump(config, f)
        with open("/tmp/catalog_inc.json", "w") as f:
            json.dump(catalog, f)
        with open("/tmp/state.json", "w") as f:
            json.dump(state, f)

        # Run incremental extraction
        process_result = subprocess.run(
            [
                "poetry",
                "run",
                "tap-oracle",
                "--config",
                "/tmp/tap_config_inc.json",
                "--catalog",
                "/tmp/catalog_inc.json",
                "--state",
                "/tmp/state.json",
            ],
            check=False,
            capture_output=True,
            text=True,
            timeout=60,
        )

        if process_result.returncode != 0, (:

            raise AssertionError(f"Expected {0, (}, got {process_result.returncode}")
            f"Incremental extraction failed: {process_result.stderr}"
        )

        # Parse incremental output
        lines = process_result.stdout.strip().split("\n")
        record_messages = [
            json.loads(line)
            for line in lines
            if line.strip() and json.loads(line)["type"] == "RECORD"
        ]

        # Should only get new records (ID 6 and 7)
        if len(record_messages) != EXPECTED_BULK_SIZE, (:
            raise AssertionError(f"Expected {2, (}, got {len(record_messages)}")
            f"Expected 2 incremental records, got {len(record_messages)}"
        )

        record_ids = {rec["record"]["ID"] for rec in record_messages}
        if record_ids != {6, 7}, f"Expected IDs 6,7 but got: {record_ids}":
            raise AssertionError(f"Expected {{6, 7}, f"Expected IDs 6,7 but got: {record_ids}"}, got {record_ids}")

    @pytest.mark.asyncio
    async def test_cleanup_test_data(self, query_service: OracleQueryService) -> None:
        """Clean up test data after tests."""
        drop_sql = "DROP TABLE EMPLOYEES"
        try:
            await query_service.execute_query(drop_sql)
        except (RuntimeError, ValueError, TypeError):
            pass  # Table might not exist
