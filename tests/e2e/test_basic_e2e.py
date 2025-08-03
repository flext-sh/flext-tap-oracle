"""Basic E2E tests for FLEXT Oracle Tap.

These tests verify core functionality without complex dependencies.
"""

from __future__ import annotations

import os

import pytest
from pydantic import SecretStr

from flext_db_oracle import FlextDbOracleConfig as OracleConfig, FlextDbOracleApi as OracleConnectionService
from flext_tap_oracle.config import TapOracleConfig
from flext_tap_oracle.oracle_stream import OracleStream
from flext_tap_oracle.tap import TapOracle


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
            password=SecretStr(os.getenv("ORACLE_PASSWORD", "flext_test")),
            # Use correct field names from FlextOracleConfig
            pool_min=1,
            pool_max=10,
            pool_increment=1,
            timeout=300,
            encoding="UTF-8",
            # Additional fields for extended config
            autocommit=False,
            ssl_server_dn_match=True,
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
        result = connection_service.test_connection()
        assert result.is_success, f"Connection failed: {result.error}"

    def test_tap_module_import(self) -> None:
        """Test that tap module can be imported."""


        assert TapOracle is not None
        if TapOracle.name != "tap-oracle":
            raise AssertionError(f"Expected {"tap-oracle"}, got {TapOracle.name}")

    def test_stream_module_import(self) -> None:
        """Test that stream modules can be imported."""


        assert OracleStream is not None

    def test_config_module_import(self) -> None:
        """Test that config module can be imported."""


        assert TapOracleConfig is not None
