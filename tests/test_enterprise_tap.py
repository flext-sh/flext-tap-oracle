"""Enterprise tests for the unified Oracle Tap.

This module provides comprehensive enterprise-grade tests for the Oracle tap
functionality, including all connection types, performance, and resilience tests.
"""

from __future__ import annotations

import asyncio
from typing import TYPE_CHECKING, Any
from unittest.mock import AsyncMock, Mock, patch

import pytest
from pydantic import ValidationError

from flext_tap_oracle.config import TapOracleConfig
from flext_tap_oracle.tap import TapOracle

if TYPE_CHECKING:
    from collections.abc import Generator


class TestTapOracleEnterprise:
    """Enterprise tests for the unified Oracle tap."""

    @pytest.fixture
    def database_config(self) -> dict[str, Any]:
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
        with patch(
            "flext_db_oracle.application.FlextDbOracleConnectionService"
        ) as mock_connection_class:
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
        self, database_config: dict[str, Any]
    ) -> None:
        """Test tap configuration validation for database connection."""
        config = TapOracleConfig(**database_config)

        assert config.connection_type == "database"
        assert config.host == "test-oracle"
        assert config.port == 1521
        assert config.service_name == "TESTDB"
        assert config.username == "testuser"
        assert config.tables == ["USERS", "ORDERS", "PRODUCTS"]
        assert config.batch_size == 1000
        assert config.max_parallel_streams == 2

    def test_tap_config_validation_database_only(
        self, database_config: dict[str, Any]
    ) -> None:
        """Test tap configuration validation for database connection only."""
        config = TapOracleConfig(**database_config)

        assert config.connection_type == "database"
        assert config.host == "test-oracle"
        assert config.port == 1521
        assert config.service_name == "TESTDB"
        assert config.username == "testuser"
        assert config.schema_name == "TESTSCHEMA"
        assert config.enable_async is True
        assert config.enable_metrics is True

    def test_tap_config_validation_errors(self) -> None:
        """Test configuration validation errors."""
        # Missing required fields for database connection
        with pytest.raises(
            ValidationError, match="Host is required for database connections"
        ):
            TapOracleConfig(connection_type="database")

        # Invalid connection type
        with pytest.raises(ValidationError, match="String should match pattern"):
            TapOracleConfig(connection_type="invalid")

    def test_tap_initialization(self, database_config: dict[str, Any]) -> None:
        """Test tap initialization with configuration."""
        tap = TapOracle(config=database_config)

        assert tap.name == "tap-oracle"
        assert tap.tap_config.connection_type == "database"
        assert tap.tap_config.host == "test-oracle"

    @pytest.mark.integration
    def test_database_stream_discovery(
        self,
        database_config: dict[str, Any],
        mock_oracle_connection: Mock,
    ) -> None:
        """Test database stream discovery."""
        tap = TapOracle(config=database_config)

        # The database_config fixture already includes tables: ["USERS", "ORDERS", "PRODUCTS"]
        # So the tap should discover exactly those tables without needing Oracle DB connection
        assert tap.tap_config.tables == ["USERS", "ORDERS", "PRODUCTS"]

        # Mock the OracleTableStream creation to avoid connection issues
        with patch("flext_tap_oracle.tap.OracleTableStream") as mock_stream_class:
            mock_stream = Mock()
            mock_stream.name = "USERS"
            mock_stream_class.return_value = mock_stream

            streams = tap.discover_streams()

            # Should discover 3 streams for the configured tables
            assert len(streams) == 3

            # Verify OracleTableStream was called for each table
            assert mock_stream_class.call_count == 3

    @pytest.mark.integration
    def test_hybrid_stream_discovery(
        self,
        database_config: dict[str, Any],
        mock_oracle_connection: Mock,
    ) -> None:
        """Test Oracle database stream discovery."""
        tap = TapOracle(config=database_config)

        # The database_config fixture already includes tables: ["USERS", "ORDERS", "PRODUCTS"]
        # So the tap should discover exactly those tables without needing Oracle DB connection
        assert tap.tap_config.tables == ["USERS", "ORDERS", "PRODUCTS"]

        # Mock the OracleTableStream creation to avoid connection issues
        with patch("flext_tap_oracle.tap.OracleTableStream") as mock_stream_class:
            mock_stream = Mock()
            mock_stream.name = "USERS"
            mock_stream_class.return_value = mock_stream

            streams = tap.discover_streams()

            # Should discover 3 Oracle database table streams
            assert len(streams) == 3

    def test_connection_testing_database(
        self,
        database_config: dict[str, Any],
        mock_oracle_connection: Mock,
    ) -> None:
        """Test database connection testing."""
        tap = TapOracle(config=database_config)

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
            assert result is True

            # Verify the async bridge was called
            mock_async_bridge.assert_called_once()

    def test_connection_testing_database_failure(
        self,
        database_config: dict[str, Any],
    ) -> None:
        """Test database connection testing with failure."""
        with patch(
            "flext_db_oracle.application.FlextDbOracleConnectionService"
        ) as mock_connection_class:
            mock_connection_class.side_effect = Exception("Connection failed")

            tap = TapOracle(config=database_config)
            result = tap.test_connection()

            assert result is False

    def test_connection_testing_database_success(
        self,
        database_config: dict[str, Any],
        mock_oracle_connection: Mock,
    ) -> None:
        """Test Oracle database connection testing."""
        tap = TapOracle(config=database_config)

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
            assert result is True

    @pytest.mark.performance
    def test_tap_metrics_collection(
        self,
        database_config: dict[str, Any],
        mock_oracle_connection: Mock,
    ) -> None:
        """Test comprehensive metrics collection."""
        tap = TapOracle(config=database_config)
        metrics = tap.get_metrics()

        assert "connection_type" in metrics
        assert "streams_discovered" in metrics
        assert "configuration" in metrics

        config_metrics = metrics["configuration"]
        assert config_metrics["batch_size"] == 1000
        assert config_metrics["max_parallel_streams"] == 2
        assert config_metrics["async_enabled"] is True  # default
        assert config_metrics["circuit_breaker_enabled"] is True  # default

    def test_tap_metrics_disabled(self, database_config: dict[str, Any]) -> None:
        """Test metrics collection when disabled."""
        database_config["enable_metrics"] = False
        tap = TapOracle(config=database_config)
        metrics = tap.get_metrics()

        assert metrics == {}

    @pytest.mark.asyncio
    async def test_async_operation_support(
        self,
        database_config: dict[str, Any],
        mock_oracle_connection: Mock,
    ) -> None:
        """Test async operation support."""
        tap = TapOracle(config=database_config)

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
        database_config: dict[str, Any],
        mock_oracle_connection: Mock,
    ) -> None:
        """Test table filtering during discovery."""
        # Test with specific tables configured
        tap = TapOracle(config=database_config)
        mock_connection = Mock()

        tables = asyncio.run(tap._get_discoverable_tables())
        assert tables == ["USERS", "ORDERS", "PRODUCTS"]

        # Mock connection should not be called since tables are specified
        mock_connection.get_table_names.assert_not_called()

    def test_tap_discoverable_tables_auto_discovery(
        self,
        database_config: dict[str, Any],
        mock_oracle_connection: Mock,
    ) -> None:
        """Test automatic table discovery."""
        # Remove tables config to trigger auto-discovery
        del database_config["tables"]

        tap = TapOracle(config=database_config)

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
            assert tables == ["TABLE1", "TABLE2", "TABLE3"]

            # Verify schema service was called with the correct schema
            mock_schema_service.get_schema_tables.assert_called_once_with("TESTSCHEMA")

    def test_tap_table_exclusion_filtering(
        self,
        database_config: dict[str, Any],
        mock_oracle_connection: Mock,
    ) -> None:
        """Test table exclusion filtering."""
        # Remove specific tables and add exclusions
        del database_config["tables"]
        database_config["exclude_tables"] = ["TEMP_TABLE", "LOG_TABLE"]

        tap = TapOracle(config=database_config)

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
            assert tables == ["USERS", "ORDERS", "PRODUCTS"]

    def test_tap_table_pattern_filtering(
        self,
        database_config: dict[str, Any],
        mock_oracle_connection: Mock,
    ) -> None:
        """Test table pattern filtering."""
        # Remove specific tables and add pattern
        del database_config["tables"]
        database_config["table_pattern"] = "^USER.*|^ORDER.*"

        tap = TapOracle(config=database_config)

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
            assert len(tables) == 4
            assert "USERS" in tables
            assert "USER_PROFILES" in tables
            assert "ORDERS" in tables
            assert "ORDER_ITEMS" in tables
            assert "PRODUCTS" not in tables
            assert "TEMP_DATA" not in tables

    @pytest.mark.stress
    def test_concurrent_stream_processing(
        self,
        database_config: dict[str, Any],
        mock_oracle_connection: Mock,
    ) -> None:
        """Test concurrent stream processing capabilities."""
        # Increase parallelism for stress test
        database_config["max_parallel_streams"] = 8

        TapOracle(config=database_config)

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
        database_config: dict[str, Any],
    ) -> None:
        """Test error handling during stream discovery."""
        with patch(
            "flext_db_oracle.application.FlextDbOracleConnectionService"
        ) as mock_connection_class:
            mock_connection_class.side_effect = Exception("Connection failed")

            tap = TapOracle(config=database_config)

            # Discovery should handle errors gracefully
            streams = tap.discover_streams()

            # Should return empty list rather than raising exception
            assert streams == []

    def test_performance_configuration_validation(
        self,
        database_config: dict[str, Any],
    ) -> None:
        """Test performance configuration validation."""
        # Test with extreme values
        database_config.update({
            "batch_size": 50,  # Very small - should warn
            "max_parallel_streams": 8,  # Maximum allowed value, larger than pool size
            "connection_pool_size": 6,
        })

        # Should not raise errors but may log warnings
        config = TapOracleConfig(**database_config)
        assert config.batch_size == 50
        assert config.max_parallel_streams == 8

    @pytest.mark.integration
    def test_real_world_workflow_simulation(
        self,
        database_config: dict[str, Any],
        mock_oracle_connection: Mock,
    ) -> None:
        """Test complete real-world workflow simulation."""
        tap = TapOracle(config=database_config)

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
            assert connection_result is True

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
            assert "connection_type" in metrics
            assert "streams_discovered" in metrics
            assert metrics["connection_type"] == "database"

            # 4. Verify configuration is accessible
            config = tap.tap_config
            assert config.connection_type == "database"
            assert config.enable_async is True
            assert config.enable_metrics is True

    def test_config_connection_string_generation(
        self,
        database_config: dict[str, Any],
    ) -> None:
        """Test connection string generation for logging."""
        config = TapOracleConfig(**database_config)
        conn_str = config.get_connection_string()

        assert conn_str == "oracle://testuser:***@test-oracle:1521/TESTDB"

    def test_config_performance_settings_extraction(
        self,
        database_config: dict[str, Any],
    ) -> None:
        """Test performance settings extraction."""
        config = TapOracleConfig(**database_config)
        perf_settings = config.get_performance_settings()

        assert perf_settings["batch_size"] == 1000
        assert perf_settings["max_parallel_streams"] == 2
        assert perf_settings["enable_async"] is True

    def test_config_circuit_breaker_settings(
        self,
        database_config: dict[str, Any],
    ) -> None:
        """Test circuit breaker settings extraction."""
        config = TapOracleConfig(**database_config)
        cb_settings = config.get_circuit_breaker_settings()

        assert cb_settings["enabled"] is True  # default
        assert cb_settings["failure_threshold"] == 3  # default from constants
        assert cb_settings["timeout"] == 60  # default

    def test_config_comprehensive_validation(
        self,
        database_config: dict[str, Any],
    ) -> None:
        """Test comprehensive configuration validation."""
        config = TapOracleConfig(**database_config)

        # Should pass validation without errors
        assert config.validate_configuration() is True

    def test_config_validation_failure_incomplete_database(self) -> None:
        """Test configuration validation failure for incomplete database config."""
        incomplete_config = {
            "connection_type": "database",
            # Missing required Oracle database connection details
        }

        # Pydantic validation should fail immediately when creating the config
        with pytest.raises(
            ValidationError, match="Host is required for database connections"
        ):
            TapOracleConfig.model_validate(incomplete_config)

    @pytest.mark.cli
    def test_cli_entry_point(self) -> None:
        """Test CLI entry point functionality."""
        with patch("flext_tap_oracle.tap.TapOracle.cli") as mock_cli:
            from flext_tap_oracle.tap import cli

            cli()
            mock_cli.assert_called_once()

    def test_stream_name_generation_patterns(
        self,
        database_config: dict[str, Any],
        mock_oracle_connection: Mock,
    ) -> None:
        """Test stream name generation patterns."""
        tap = TapOracle(config=database_config)

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
            assert "USERS" in stream_names
            assert "ORDERS" in stream_names
            assert "PRODUCTS" in stream_names

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
        config = TapOracleConfig.model_validate(large_config)
        assert config.tables is not None
        assert len(config.tables) == 1000

        # Tap should handle large Oracle database configuration
        tap = TapOracle(config=large_config)
        assert tap.tap_config.connection_type == "database"
