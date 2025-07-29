"""Basic E2E tests for FLEXT Oracle Tap.

These tests verify core functionality without complex dependencies.
"""

from flext_tap_oracle.tap import TapOracle
from flext_tap_oracle.streams import OracleTableStream
from flext_tap_oracle.config import TapOracleConfig


from __future__ import annotations

import os

import pytest

from flext_db_oracle import FlextDbOracleConfig as OracleConfig
from flext_db_oracle.application import FlextDbOracleConnectionService as OracleConnectionService


class TestBasicE2E:
    """Basic E2E tests for Oracle Database tap."""

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

    @pytest.mark.asyncio
    async def test_basic_connection(
        self, connection_service: OracleConnectionService
    ) -> None:
        """Test basic Oracle database connection."""
        result = await connection_service.test_connection()
        assert result.success, f"Connection failed: {result.error}"

    def test_tap_module_import(self) -> None:
        """Test that tap module can be imported."""


        assert TapOracle is not None
        if TapOracle.name != "tap-oracle":
            raise AssertionError(f"Expected {"tap-oracle"}, got {TapOracle.name}")

    def test_stream_module_import(self) -> None:
        """Test that stream modules can be imported."""


        assert OracleTableStream is not None

    def test_config_module_import(self) -> None:
        """Test that config module can be imported."""


        assert TapOracleConfig is not None
