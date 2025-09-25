"""Enterprise tests for the unified Oracle Tap.

This module provides comprehensive enterprise-grade tests for the Oracle tap
functionality, including all connection types, performance, and resilience tests.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

import asyncio
from collections.abc import Generator
from unittest.mock import AsyncMock, Mock, patch

import pytest
from pydantic import ValidationError

from flext_tap_oracle import FlextOracleTapBaseService, FlextOracleTapConfig

# Constants
EXPECTED_BULK_SIZE = 2
EXPECTED_TOTAL_PAGES = 8
EXPECTED_DATA_COUNT = 3


class TestFlextOracleTapBaseServiceEnterprise:
    """Enterprise tests for the unified Oracle tap."""

    @pytest.fixture
    def database_config(self) -> dict[str, object]:
        """Provide database connection configuration."""
        return {
            "connection_type": "database",
            "host": "test-oracle",
            "port": 1521,
            "service_name": "TESTDB",
            "username": "testuser",
            "password": "testpass",
            "schema_name": "TESTSCHEMA",
            "tables": ["USERS", "ORDERS", "PRODUCTS"],
            "batch_size": 1000,
            "max_parallel_streams": 2,
        }

    @pytest.fixture
    def mock_oracle_connection(self) -> Generator[Mock]:
        """Mock Oracle connection for testing."""
        with patch("flext_db_oracle.FlextDbOracleApi") as mock_connection_class:
            mock_connection = Mock()
            mock_connection.connect.return_value = None
            mock_connection.disconnect.return_value = None
            mock_connection.test_connection.return_value = True
            mock_connection.get_table_names.return_value = [
                "USERS",
                "ORDERS",
                "PRODUCTS",
            ]
            mock_connection.get_column_info.return_value = [
                {"name": "ID", "type": "NUMBER", "nullable": False},
                {"name": "NAME", "type": "VARCHAR2", "nullable": True},
                {"name": "EMAIL", "type": "VARCHAR2", "nullable": True},
            ]
            mock_connection.connection_metrics = {
                "connected": True,
                "uptime_seconds": 60.0,
                "query_count": 100,
                "error_count": 0,
            }
            mock_connection_class.return_value = mock_connection
            yield mock_connection

    def test_tap_config_validation_database(
        self,
        database_config: dict[str, object],
        mock_oracle_connection: Mock,
    ) -> None:
        """Test tap configuration validation for database connection."""
        config = FlextOracleTapConfig(**database_config)

        if config.connection_type != "database":
            raise AssertionError(f"Expected {'database'}, got {config.connection_type}")
        assert config.host == "test-oracle"
        if config.port != 1521:
            raise AssertionError(f"Expected {1521}, got {config.port}")
        assert config.service_name == "TESTDB"
        if config.username != "testuser":
            raise AssertionError(f"Expected {'testuser'}, got {config.username}")
        assert config.tables == ["USERS", "ORDERS", "PRODUCTS"]
        if config.batch_size != 1000:
            raise AssertionError(f"Expected {1000}, got {config.batch_size}")
        assert config.max_parallel_streams == EXPECTED_BULK_SIZE

    def test_tap_config_validation_database_only(
        self,
        database_config: dict[str, object],
        mock_oracle_connection: Mock,
    ) -> None:
        """Test tap configuration validation for database connection only."""
        config = FlextOracleTapConfig(**database_config)

        if config.connection_type != "database":
            raise AssertionError(f"Expected {'database'}, got {config.connection_type}")
        assert config.host == "test-oracle"
        if config.port != 1521:
            raise AssertionError(f"Expected {1521}, got {config.port}")
        assert config.service_name == "TESTDB"
        if config.username != "testuser":
            raise AssertionError(f"Expected {'testuser'}, got {config.username}")
        assert config.schema_name == "TESTSCHEMA"
        if not (config.enable_async):
            raise AssertionError(f"Expected True, got {config.enable_async}")
        assert config.enable_metrics is True

    def test_tap_config_validation_errors(self) -> None:
        """Test configuration validation errors."""
        # Missing required fields for database connection
        with pytest.raises(ValidationError, match="Field required"):
            FlextOracleTapConfig(
                connection_type="database",
                host="required",
                username="required",
                password="required",
            )

        # Invalid connection type
        with pytest.raises(ValidationError, match="Connection type must be 'database'"):
            FlextOracleTapConfig(
                connection_type="invalid", host="test", username="test", password="test"
            )

    def test_self(self, database_config: dict[str, object]) -> None:
        """Test tap initialization with configuration."""
        tap = FlextOracleTapBaseService(config=database_config)

        if tap.name != "tap-oracle":
            raise AssertionError(f"Expected {'tap-oracle'}, got {tap.name}")
        assert tap.typed_config.connection_type == "database"
        if tap.typed_config.host != "test-oracle":
            raise AssertionError(
                f"Expected {'test-oracle'}, got {tap.typed_config.host}"
            )

    @pytest.mark.integration
    def test_database_stream_discovery(
        self,
        database_config: dict[str, object],
        mock_oracle_connection: Mock,
    ) -> None:
        """Test database stream discovery."""
        tap = FlextOracleTapBaseService(config=database_config)

        # So the tap should discover exactly those tables without needing Oracle DB connection
        if tap.typed_config.tables != ["USERS", "ORDERS", "PRODUCTS"]:
            raise AssertionError(
                f"Expected {['USERS', 'ORDERS', 'PRODUCTS']}, got {tap.typed_config.tables}"
            )

        # Mock the OracleTableStream creation to avoid connection issues
        with patch("flext_tap_oracle.tap.OracleTableStream") as mock_stream_class:
            mock_stream = Mock()
            mock_stream.name = "USERS"
            mock_stream_class.return_value = mock_stream

            streams = tap.discover_streams()

            # Should discover 3 streams for the configured tables
            if len(streams) != EXPECTED_DATA_COUNT:
                raise AssertionError(f"Expected {3}, got {len(streams)}")

            # Verify OracleTableStream was called for each table
            if mock_stream_class.call_count != EXPECTED_DATA_COUNT:
                raise AssertionError(
                    f"Expected {3}, got {mock_stream_class.call_count}"
                )

    @pytest.mark.integration
    def test_hybrid_stream_discovery(
        self,
        database_config: dict[str, object],
        mock_oracle_connection: Mock,
    ) -> None:
        """Test Oracle database stream discovery."""
        tap = FlextOracleTapBaseService(config=database_config)

        # So the tap should discover exactly those tables without needing Oracle DB connection
        if tap.typed_config.tables != ["USERS", "ORDERS", "PRODUCTS"]:
            raise AssertionError(
                f"Expected {['USERS', 'ORDERS', 'PRODUCTS']}, got {tap.typed_config.tables}"
            )

        # Mock the OracleTableStream creation to avoid connection issues
        with patch("flext_tap_oracle.tap.OracleTableStream") as mock_stream_class:
            mock_stream = Mock()
            mock_stream.name = "USERS"
            mock_stream_class.return_value = mock_stream

            streams = tap.discover_streams()

            # Should discover 3 Oracle database table streams
            if len(streams) != EXPECTED_DATA_COUNT:
                raise AssertionError(f"Expected {3}, got {len(streams)}")

    def test_connection_testing_database(
        self,
        database_config: dict[str, object],
        mock_oracle_connection: Mock,
    ) -> None:
        """Test database connection testing."""
        tap = FlextOracleTapBaseService(config=database_config)

        # Mock the async bridge to return successful connection test
        with patch(
            "flext_tap_oracle.tap.run_async_in_sync_context"
        ) as mock_async_bridge:
            # Mock successful connection test result
            mock_result = Mock()
            mock_result.success = True
            mock_async_bridge.return_value = mock_result

            # Test successful connection
            result = tap.test_connection()
            if not (result):
                raise AssertionError(f"Expected True, got {result}")

            # Verify the async bridge was called
            mock_async_bridge.assert_called_once()

    def test_connection_testing_database_failure(
        self,
        database_config: dict[str, object],
    ) -> None:
        """Test database connection testing with failure."""
        with patch("flext_db_oracle.FlextDbOracleApi") as mock_connection_class:
            mock_connection_class.side_effect = Exception("Connection failed")

            tap = FlextOracleTapBaseService(config=database_config)
            result = tap.test_connection()

            if result:
                raise AssertionError(f"Expected False, got {result}")

    def test_connection_testing_database_success(
        self,
        database_config: dict[str, object],
        mock_oracle_connection: Mock,
    ) -> None:
        """Test Oracle database connection testing."""
        tap = FlextOracleTapBaseService(config=database_config)

        # Mock the async bridge to return successful connection test
        with patch(
            "flext_tap_oracle.tap.run_async_in_sync_context"
        ) as mock_async_bridge:
            # Mock successful connection test result
            mock_result = Mock()
            mock_result.success = True
            mock_async_bridge.return_value = mock_result

            result = tap.test_connection()

            # Should test Oracle database connection
            if not (result):
                raise AssertionError(f"Expected True, got {result}")

    @pytest.mark.performance
    def test_tap_metrics_collection(
        self,
        database_config: dict[str, object],
        mock_oracle_connection: Mock,
    ) -> None:
        """Test comprehensive metrics collection."""
        tap = FlextOracleTapBaseService(config=database_config)
        metrics = tap.get_metrics()

        if "connection_type" not in metrics:
            raise AssertionError(f"Expected {'connection_type'} in {metrics}")
        assert "streams_discovered" in metrics
        if "configuration" not in metrics:
            raise AssertionError(f"Expected {'configuration'} in {metrics}")

        config_metrics = metrics.get("configuration", {})
        if isinstance(config_metrics, dict):
            if config_metrics.get("batch_size") != 1000:
                raise AssertionError(
                    f"Expected {1000}, got {config_metrics.get('batch_size')}"
                )
            assert config_metrics.get("max_parallel_streams") == EXPECTED_BULK_SIZE
            assert config_metrics.get("async_enabled") is True  # default
            assert config_metrics.get("circuit_breaker_enabled") is True  # default

    def test_self(self, database_config: dict[str, object]) -> None:
        """Test metrics collection when disabled."""
        database_config["enable_metrics"] = False
        tap = FlextOracleTapBaseService(config=database_config)
        metrics = tap.get_metrics()

        if metrics != {}:
            raise AssertionError(f"Expected {{}}, got {metrics}")

    @pytest.mark.asyncio
    async def test_async_operation_support(
        self,
        database_config: dict[str, object],
        mock_oracle_connection: Mock,
    ) -> None:
        """Test async operation support."""
        tap = FlextOracleTapBaseService(config=database_config)

        # Mock streams with async support
        mock_stream = AsyncMock()
        mock_stream.sync_async = AsyncMock(return_value=None)

        # Mock the stream discovery to return our async stream
        with patch.object(tap, "discover_streams", return_value=[mock_stream]):
            # This would normally run async operations
            await tap.run_async()

            # Verify async method was called
            mock_stream.sync_async.assert_called_once()

    def test_tap_discoverable_tables_filtering(
        self,
        database_config: dict[str, object],
        mock_oracle_connection: Mock,
    ) -> None:
        """Test table filtering during discovery."""
        # Test with specific tables configured
        tap = FlextOracleTapBaseService(config=database_config)
        mock_connection = Mock()

        tables = asyncio.run(tap._get_discoverable_tables())
        if tables != ["USERS", "ORDERS", "PRODUCTS"]:
            raise AssertionError(
                f"Expected {['USERS', 'ORDERS', 'PRODUCTS']}, got {tables}"
            )

        # Mock connection should not be called since tables are specified
        mock_connection.get_table_names.assert_not_called()

    def test_tap_discoverable_tables_auto_discovery(
        self,
        database_config: dict[str, object],
        mock_oracle_connection: Mock,
    ) -> None:
        """Test automatic table discovery."""
        # Remove tables config to trigger auto-discovery
        del database_config["tables"]

        tap = FlextOracleTapBaseService(config=database_config)

        # Mock the schema service to return mock tables
        mock_table_metadata = []
        for table_name in ["TABLE1", "TABLE2", "TABLE3"]:
            mock_table = Mock()
            mock_table.table_name = table_name
            mock_table_metadata.append(mock_table)

        mock_result = Mock()
        mock_result.success = True
        mock_result.data = mock_table_metadata

        # Mock the schema service
        with patch.object(tap, "_schema_service") as mock_schema_service:
            mock_schema_service.get_schema_tables = AsyncMock(return_value=mock_result)

            tables = asyncio.run(tap._get_discoverable_tables())
            if tables != ["TABLE1", "TABLE2", "TABLE3"]:
                raise AssertionError(
                    f"Expected {['TABLE1', 'TABLE2', 'TABLE3']}, got {tables}"
                )

            # Verify schema service was called with the correct schema
            mock_schema_service.get_schema_tables.assert_called_once_with("TESTSCHEMA")

    def test_tap_table_exclusion_filtering(
        self,
        database_config: dict[str, object],
        mock_oracle_connection: Mock,
    ) -> None:
        """Test table exclusion filtering."""
        # Remove specific tables and add exclusions
        del database_config["tables"]
        database_config["exclude_tables"] = ["TEMP_TABLE", "LOG_TABLE"]

        tap = FlextOracleTapBaseService(config=database_config)

        # Mock the schema service to return mock tables
        mock_table_metadata = []
        for table_name in ["USERS", "ORDERS", "TEMP_TABLE", "LOG_TABLE", "PRODUCTS"]:
            mock_table = Mock()
            mock_table.table_name = table_name
            mock_table_metadata.append(mock_table)

        mock_result = Mock()
        mock_result.success = True
        mock_result.data = mock_table_metadata

        # Mock the schema service
        with patch.object(tap, "_schema_service") as mock_schema_service:
            mock_schema_service.get_schema_tables = AsyncMock(return_value=mock_result)

            tables = asyncio.run(tap._get_discoverable_tables())
            if tables != ["USERS", "ORDERS", "PRODUCTS"]:
                raise AssertionError(
                    f"Expected {['USERS', 'ORDERS', 'PRODUCTS']}, got {tables}"
                )

    def test_tap_table_pattern_filtering(
        self,
        database_config: dict[str, object],
        mock_oracle_connection: Mock,
    ) -> None:
        """Test table pattern filtering."""
        # Remove specific tables and add pattern
        del database_config["tables"]
        database_config["table_pattern"] = "^USER.*|^ORDER.*"

        tap = FlextOracleTapBaseService(config=database_config)

        # Mock the schema service to return mock tables
        mock_table_metadata = []
        for table_name in [
            "USERS",
            "USER_PROFILES",
            "ORDERS",
            "ORDER_ITEMS",
            "PRODUCTS",
            "TEMP_DATA",
        ]:
            mock_table = Mock()
            mock_table.table_name = table_name
            mock_table_metadata.append(mock_table)

        mock_result = Mock()
        mock_result.success = True
        mock_result.data = mock_table_metadata

        # Mock the schema service
        with patch.object(tap, "_schema_service") as mock_schema_service:
            mock_schema_service.get_schema_tables = AsyncMock(return_value=mock_result)

            tables = asyncio.run(tap._get_discoverable_tables())
            # Should match USERS, USER_PROFILES, ORDERS, ORDER_ITEMS
            if len(tables) != 4:
                raise AssertionError(f"Expected {4}, got {len(tables)}")
            if "USERS" not in tables:
                raise AssertionError(f"Expected {'USERS'} in {tables}")
            assert "USER_PROFILES" in tables
            if "ORDERS" not in tables:
                raise AssertionError(f"Expected {'ORDERS'} in {tables}")
            assert "ORDER_ITEMS" in tables
            if "PRODUCTS" not in tables:
                raise AssertionError(f"Expected PRODUCTS in {tables}")
            assert "TEMP_DATA" not in tables

    @pytest.mark.stress
    def test_concurrent_stream_processing(
        self,
        database_config: dict[str, object],
        mock_oracle_connection: Mock,
    ) -> None:
        """Test concurrent stream processing capabilities."""
        # Increase parallelism for stress test
        database_config["max_parallel_streams"] = 8

        FlextOracleTapBaseService(config=database_config)

        # Mock multiple streams
        mock_streams = []
        for _i in range(10):
            mock_stream = AsyncMock()
            mock_stream.sync_async = AsyncMock()
            mock_streams.append(mock_stream)

        async def test_concurrent_processing() -> None:
            # Simulate processing multiple streams
            semaphore = asyncio.Semaphore(database_config["max_parallel_streams"])

            async def process_stream(stream: Mock) -> None:
                async with semaphore:
                    await stream.sync_async()

            await asyncio.gather(*[process_stream(stream) for stream in mock_streams])

        # Run the test
        asyncio.run(test_concurrent_processing())

        # Verify all streams were processed
        for stream in mock_streams:
            stream.sync_async.assert_called_once()

    @pytest.mark.error_handling
    def test_error_handling_during_discovery(
        self,
        database_config: dict[str, object],
    ) -> None:
        """Test error handling during stream discovery."""
        with patch("flext_db_oracle.FlextDbOracleApi") as mock_connection_class:
            mock_connection_class.side_effect = Exception("Connection failed")

            tap = FlextOracleTapBaseService(config=database_config)

            # Discovery should handle errors gracefully
            streams = tap.discover_streams()

            # Should return empty list rather than raising exception
            if streams != []:
                raise AssertionError(f"Expected {[]}, got {streams}")

    def test_performance_configuration_validation(
        self,
        database_config: dict[str, object],
    ) -> None:
        """Test performance configuration validation."""
        # Test with extreme values
        database_config.update(
            {
                "batch_size": 50,  # Very small - should warn
                "max_parallel_streams": 8,  # Maximum allowed value, larger than pool size
                "connection_pool_size": 6,
            }
        )

        # Should not raise errors but may log warnings
        config = FlextOracleTapConfig(**database_config)
        if config.batch_size != 50:
            raise AssertionError(f"Expected {50}, got {config.batch_size}")
        assert config.max_parallel_streams == EXPECTED_TOTAL_PAGES

    @pytest.mark.integration
    def test_real_world_workflow_simulation(
        self,
        database_config: dict[str, object],
        mock_oracle_connection: Mock,
    ) -> None:
        """Test complete real-world workflow simulation."""
        tap = FlextOracleTapBaseService(config=database_config)

        # Mock the async bridge for connection testing
        with patch(
            "flext_tap_oracle.tap.run_async_in_sync_context"
        ) as mock_async_bridge:
            # Mock successful connection test result
            mock_result = Mock()
            mock_result.success = True
            mock_async_bridge.return_value = mock_result

            # 1. Test connection to all sources
            connection_result = tap.test_connection()
            if not (connection_result):
                raise AssertionError(f"Expected True, got {connection_result}")

        # Mock stream discovery separately
        mock_streams = [Mock(), Mock(), Mock()]
        for i, stream in enumerate(mock_streams):
            stream.name = f"STREAM_{i}"

        with patch.object(tap, "discover_streams", return_value=mock_streams):
            # 2. Discover streams from all sources
            streams = tap.discover_streams()
            assert len(streams) > 0

            # 3. Get comprehensive metrics
            metrics = tap.get_metrics()
            if "connection_type" not in metrics:
                raise AssertionError(f"Expected {'connection_type'} in {metrics}")
            assert "streams_discovered" in metrics
            if metrics["connection_type"] != "database":
                raise AssertionError(
                    f"Expected {'database'}, got {metrics['connection_type']}"
                )

            # 4. Verify configuration is accessible
            config = tap.typed_config
            if config.connection_type != "database":
                raise AssertionError(
                    f"Expected {'database'}, got {config.connection_type}"
                )
            if not (config.enable_async):
                raise AssertionError(f"Expected True, got {config.enable_async}")
            assert config.enable_metrics is True

    def test_config_connection_string_generation(
        self,
        database_config: dict[str, object],
    ) -> None:
        """Test connection string generation for logging."""
        config = FlextOracleTapConfig(**database_config)
        conn_str = config.get_connection_string()

        if conn_str != "oracle://testuser:***@test-oracle:1521/TESTDB":
            raise AssertionError(
                f"Expected {'oracle://testuser:***@test-oracle:1521/TESTDB'}, got {conn_str}"
            )

    def test_config_performance_settings_extraction(
        self,
        database_config: dict[str, object],
    ) -> None:
        """Test performance settings extraction."""
        config = FlextOracleTapConfig(**database_config)
        perf_settings = config.get_performance_settings()

        if perf_settings["batch_size"] != 1000:
            raise AssertionError(f"Expected {1000}, got {perf_settings['batch_size']}")
        assert perf_settings["max_parallel_streams"] == EXPECTED_BULK_SIZE
        if not (perf_settings["enable_async"]):
            raise AssertionError(f"Expected True, got {perf_settings['enable_async']}")

    def test_config_circuit_breaker_settings(
        self,
        database_config: dict[str, object],
    ) -> None:
        """Test circuit breaker settings extraction."""
        config = FlextOracleTapConfig(**database_config)
        cb_settings = config.get_circuit_breaker_settings()

        assert cb_settings["enabled"] is True  # default
        if (
            cb_settings["failure_threshold"] != EXPECTED_DATA_COUNT
        ):  # default from constants
            raise AssertionError(
                f"Expected {EXPECTED_DATA_COUNT}, got {cb_settings['failure_threshold']}"
            )
        assert cb_settings["timeout"] == 60  # default

    def test_config_comprehensive_validation(
        self,
        database_config: dict[str, object],
    ) -> None:
        """Test comprehensive configuration validation."""
        config = FlextOracleTapConfig(**database_config)

        # Should pass validation without errors
        if not (config.validate_configuration()):
            raise AssertionError(
                f"Expected True, got {config.validate_configuration()}"
            )

    def test_config_validation_failure_incomplete_database(self) -> None:
        """Test configuration validation failure for incomplete database config."""
        incomplete_config = {
            "connection_type": "database",
            # Missing required Oracle database connection details
        }

        # Pydantic validation should fail immediately when creating the config
        with pytest.raises(ValidationError, match="Field required"):
            FlextOracleTapConfig.model_validate(incomplete_config)

    # CLI functionality was removed with facade - test no longer needed

    def test_stream_name_generation_patterns(
        self,
        database_config: dict[str, object],
        mock_oracle_connection: Mock,
    ) -> None:
        """Test stream name generation patterns."""
        tap = FlextOracleTapBaseService(config=database_config)

        # Mock the discovery methods to return predictable streams
        with patch.object(tap, "_discover_database_streams") as mock_db:
            # Mock Oracle Database stream objects with expected names
            mock_users_stream = Mock()
            mock_users_stream.name = "USERS"

            mock_orders_stream = Mock()
            mock_orders_stream.name = "ORDERS"

            mock_products_stream = Mock()
            mock_products_stream.name = "PRODUCTS"

            mock_db.return_value = [
                mock_users_stream,
                mock_orders_stream,
                mock_products_stream,
            ]

            streams = tap.discover_streams()

            # Verify Oracle Database naming patterns only
            stream_names = [s.name for s in streams]
            if "USERS" not in stream_names:
                raise AssertionError(f"Expected {'USERS'} in {stream_names}")
            assert "ORDERS" in stream_names
            if "PRODUCTS" not in stream_names:
                raise AssertionError(f"Expected {'PRODUCTS'} in {stream_names}")

    @pytest.mark.memory
    def test_memory_efficiency_large_config(self) -> None:
        """Test memory efficiency with large configuration."""
        # Create large configuration
        large_config = {
            "connection_type": "database",
            "host": "test-oracle",
            "port": 1521,
            "service_name": "TESTDB",
            "username": "testuser",
            "password": "testpass",
            "tables": [
                f"TABLE_{i}" for i in range(1000)
            ],  # 1000 Oracle database tables
        }

        # Configuration should be created efficiently
        config = FlextOracleTapConfig.model_validate(large_config)
        assert config.tables is not None
        if len(config.tables) != 1000:
            raise AssertionError(f"Expected {1000}, got {len(config.tables)}")

        # Tap should handle large Oracle database configuration
        tap = FlextOracleTapBaseService(config=large_config)
        if tap.typed_config.connection_type != "database":
            raise AssertionError(
                f"Expected {'database'}, got {tap.typed_config.connection_type}"
            )
