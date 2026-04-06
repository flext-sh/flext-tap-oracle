"""Integration-focused tests for Oracle tap settings helpers."""

from __future__ import annotations

import os
from collections.abc import Sequence

import pytest

from flext_tap_oracle import (
    FlextTapOracleSettings,
    u,
)
from tests import m


class TestFlextOracleTapSettingsAndHelpers:
    """Validate settings model behavior and helper service wiring."""

    @pytest.fixture(autouse=True)
    def reset_settings_singleton(self) -> None:
        """Ensure deterministic tests by resetting singleton settings state."""
        FlextTapOracleSettings.reset_for_testing()
        os.environ["FLEXT_ORACLE_SERVICE_NAME"] = "XE"
        os.environ["FLEXT_ORACLE_USER"] = "testuser"
        os.environ["FLEXT_ORACLE_PASSWORD"] = "testpass"

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
        oracle_config = config.get_oracle_config()
        assert oracle_config["user"] == "testuser"
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
        result = FlextTapOracleSettings.create_oracle_tap_config(
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

    def test_create_oracle_tap_config_failure_when_missing_credentials(
        self,
        monkeypatch: pytest.MonkeyPatch,
    ) -> None:
        monkeypatch.delenv("FLEXT_ORACLE_USER", raising=False)
        monkeypatch.delenv("FLEXT_ORACLE_PASSWORD", raising=False)
        result = FlextTapOracleSettings.create_oracle_tap_config(
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
        discovered_tables: Sequence[m.DbOracle.Table] = [
            m.DbOracle.Table(
                name="USERS", owner="TESTDB", domain_events=[], columns=[]
            ),
            m.DbOracle.Table(
                name="ORDERS", owner="TESTDB", domain_events=[], columns=[]
            ),
            m.DbOracle.Table(
                name="PRODUCTS", owner="TESTDB", domain_events=[], columns=[]
            ),
        ]
        result = u.TapOracle.tap_oracle_client_filter_tables(
            tap_config=config,
            discovered_tables=discovered_tables,
        )
        assert result.is_success
        assert result.value == ["USERS", "ORDERS", "PRODUCTS"]
