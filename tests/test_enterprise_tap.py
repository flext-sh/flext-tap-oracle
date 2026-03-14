"""Integration-focused tests for Oracle tap settings helpers."""

from __future__ import annotations

import os
from typing import override

import pytest
from flext_core import FlextResult
from flext_db_oracle import FlextDbOracleModels

from flext_tap_oracle import (
    FlextOracleDiscoveryService,
    FlextOracleTableFilterService,
    FlextTapOracleSettings,
)
from flext_tap_oracle.settings import create_oracle_tap_config


class _DiscoveryStub(FlextOracleDiscoveryService):
    @override
    def __init__(self) -> None:
        pass

    @override
    def execute(self) -> FlextResult[list[FlextDbOracleModels.DbOracle.Table]]:
        return FlextResult[list[FlextDbOracleModels.DbOracle.Table]].ok([
            FlextDbOracleModels.DbOracle.Table(
                name="USERS", owner="TESTDB", domain_events=[], columns=[]
            ),
            FlextDbOracleModels.DbOracle.Table(
                name="ORDERS", owner="TESTDB", domain_events=[], columns=[]
            ),
            FlextDbOracleModels.DbOracle.Table(
                name="PRODUCTS", owner="TESTDB", domain_events=[], columns=[]
            ),
        ])


class TestFlextOracleTapSettingsAndHelpers:
    """Validate settings model behavior and helper service wiring."""

    @pytest.fixture(autouse=True)
    def reset_settings_singleton(self) -> None:
        """Ensure deterministic tests by resetting singleton settings state."""
        FlextTapOracleSettings.reset_for_testing()
        os.environ["FLEXT_TAP_ORACLE_SERVICE_NAME"] = "XE"
        os.environ["FLEXT_TAP_ORACLE_ORACLE_SERVICE_NAME"] = "XE"

    def test_settings_model_validate(self) -> None:
        config = FlextTapOracleSettings.get_global(
            overrides={
                "oracle_host": "test-oracle",
                "oracle_port": 1521,
                "oracle_service_name": "TESTDB",
                "oracle_user": "testuser",
                "oracle_password": "testpass",
                "batch_size": 1000,
            }
        )
        assert config.oracle_host == "test-oracle"
        assert config.oracle_port == 1521
        assert config.oracle_service_name == "TESTDB"
        assert config.oracle_user.get_secret_value() == "testuser"
        assert config.batch_size == 1000

    def test_settings_connection_string(self) -> None:
        config = FlextTapOracleSettings.get_global(
            overrides={
                "oracle_host": "test-oracle",
                "oracle_port": 1521,
                "oracle_service_name": "TESTDB",
                "oracle_user": "testuser",
                "oracle_password": "testpass",
            }
        )
        oracle_config = config.get_oracle_config()
        assert oracle_config["host"] == "test-oracle"
        assert oracle_config["port"] == 1521
        assert oracle_config["service_name"] == "TESTDB"

    def test_create_oracle_tap_config_success(self) -> None:
        result = create_oracle_tap_config(
            oracle_params={
                "oracle_host": "localhost",
                "oracle_port": 1521,
                "oracle_service_name": "XE",
                "oracle_user": "tap_user",
                "oracle_password": "secret",
            }
        )
        if result.is_failure:
            pytest.fail(f"Config creation failed: {result.error}")
        assert result.is_success
        assert result.value is not None
        assert result.value.oracle_host == "localhost"

    def test_create_oracle_tap_config_failure_when_missing_credentials(self) -> None:
        result = create_oracle_tap_config(
            oracle_params={
                "oracle_host": "localhost",
                "oracle_port": 1521,
                "oracle_service_name": "XE",
            }
        )
        assert result.is_failure
        assert "creation failed" in str(result.error).lower()

    def test_table_filter_service_uses_configured_tables(self) -> None:
        config = FlextTapOracleSettings.get_global(
            overrides={
                "oracle_host": "test-oracle",
                "oracle_port": 1521,
                "oracle_service_name": "TESTDB",
                "oracle_user": "testuser",
                "oracle_password": "testpass",
                "batch_size": 1000,
            }
        )
        service = FlextOracleTableFilterService(
            tap_config=config, discovery_service=_DiscoveryStub()
        )
        result = service.execute()
        assert result.is_success
        assert result.value == ["USERS", "ORDERS", "PRODUCTS"]
