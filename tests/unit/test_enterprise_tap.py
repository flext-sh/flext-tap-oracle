"""Behavioral tests for the public FlextTapOracleSettings contract."""

from __future__ import annotations

from collections.abc import Sequence

import pytest

from flext_tap_oracle import FlextTapOracleSettings
from tests.constants import c
from tests.models import m
from tests.utilities import u


class TestsFlextTapOracleEnterpriseTap:
    """Validate observable settings behavior through the public API only."""

    def test_fetch_global_applies_overrides_to_public_fields(
        self,
        tap_oracle_settings_overrides: dict[str, str | int],
    ) -> None:
        config = FlextTapOracleSettings.fetch_global(
            overrides=tap_oracle_settings_overrides,
        )
        assert config.oracle_host == c.TapOracle.Tests.UNIT_ORACLE_HOST
        assert config.oracle_port == c.TapOracle.Tests.UNIT_ORACLE_PORT
        assert (
            config.oracle_service_name
            == c.TapOracle.Tests.UNIT_ORACLE_SERVICE_NAME
        )
        assert config.batch_size == c.TapOracle.Tests.UNIT_BATCH_SIZE

    def test_get_oracle_config_exposes_full_connection_contract(
        self,
        tap_oracle_settings_overrides: dict[str, str | int],
    ) -> None:
        config = FlextTapOracleSettings.fetch_global(
            overrides=tap_oracle_settings_overrides,
        )
        oracle_config = config.get_oracle_config()
        assert oracle_config == {
            "host": c.TapOracle.Tests.UNIT_ORACLE_HOST,
            "port": c.TapOracle.Tests.UNIT_ORACLE_PORT,
            "service_name": c.TapOracle.Tests.UNIT_ORACLE_SERVICE_NAME,
            "user": c.TapOracle.Tests.UNIT_ORACLE_USER,
            "password": c.TapOracle.Tests.UNIT_ORACLE_PASSWORD,
        }

    def test_get_oracle_config_resolves_secret_values_to_plaintext(
        self,
        tap_oracle_settings_overrides: dict[str, str | int],
    ) -> None:
        config = FlextTapOracleSettings.fetch_global(
            overrides=tap_oracle_settings_overrides,
        )
        oracle_config = config.get_oracle_config()
        # Secret fields must surface as usable plaintext, not SecretStr wrappers.
        assert oracle_config["user"] == c.TapOracle.Tests.UNIT_ORACLE_USER
        assert oracle_config["password"] == c.TapOracle.Tests.UNIT_ORACLE_PASSWORD
        assert "SecretStr" not in repr(oracle_config["password"])

    def test_get_oracle_config_is_idempotent(
        self,
        tap_oracle_settings_overrides: dict[str, str | int],
    ) -> None:
        config = FlextTapOracleSettings.fetch_global(
            overrides=tap_oracle_settings_overrides,
        )
        assert config.get_oracle_config() == config.get_oracle_config()

    def test_validate_business_rules_succeeds_for_complete_config(
        self,
        tap_oracle_settings_overrides: dict[str, str | int],
    ) -> None:
        config = FlextTapOracleSettings.fetch_global(
            overrides=tap_oracle_settings_overrides,
        )
        result = config.validate_business_rules()
        assert result.success
        assert result.value is True

    def test_validate_oracle_tap_configuration_delegates_to_business_rules(
        self,
        tap_oracle_settings_overrides: dict[str, str | int],
    ) -> None:
        config = FlextTapOracleSettings.fetch_global(
            overrides=tap_oracle_settings_overrides,
        )
        result = FlextTapOracleSettings.validate_oracle_tap_configuration(config)
        assert result.success
        assert result.value is True

    def test_create_oracle_tap_config_returns_validated_settings(
        self,
        tap_oracle_create_params: dict[str, str | int],
    ) -> None:
        result = FlextTapOracleSettings.create_oracle_tap_config(
            oracle_params=tap_oracle_create_params,
        )
        assert result.success
        config = result.unwrap()
        assert config.oracle_host == c.TapOracle.Tests.CREATE_CONFIG_HOST
        assert config.oracle_port == c.TapOracle.Tests.CREATE_CONFIG_PORT
        assert (
            config.oracle_service_name
            == c.TapOracle.Tests.CREATE_CONFIG_SERVICE_NAME
        )

    def test_create_oracle_tap_config_applies_default_batch_and_prefix(
        self,
        tap_oracle_create_params: dict[str, str | int],
    ) -> None:
        result = FlextTapOracleSettings.create_oracle_tap_config(
            oracle_params=tap_oracle_create_params,
        )
        assert result.success
        config = result.unwrap()
        # Grouped defaults are part of the create contract, not caller-supplied.
        assert config.batch_size == 1000
        assert config.stream_prefix == c.TapOracle.DEFAULT_STREAM_PREFIX

    def test_create_oracle_tap_config_fails_when_credentials_missing(
        self,
        monkeypatch: pytest.MonkeyPatch,
    ) -> None:
        monkeypatch.delenv(c.TapOracle.Tests.SHARED_ORACLE_USER_ENV, raising=False)
        monkeypatch.delenv(
            c.TapOracle.Tests.SHARED_ORACLE_PASSWORD_ENV,
            raising=False,
        )
        FlextTapOracleSettings.reset_for_testing()
        result = FlextTapOracleSettings.create_oracle_tap_config(
            oracle_params={
                "oracle_host": c.TapOracle.Tests.CREATE_CONFIG_HOST,
                "oracle_port": c.TapOracle.Tests.CREATE_CONFIG_PORT,
                "oracle_service_name": c.TapOracle.Tests.CREATE_CONFIG_SERVICE_NAME,
            }
        )
        assert result.failure
        assert "creation failed" in str(result.error).lower()

    def test_filter_tables_returns_configured_table_names(
        self,
        tap_oracle_settings_overrides: dict[str, str | int],
    ) -> None:
        config = FlextTapOracleSettings.fetch_global(
            overrides=tap_oracle_settings_overrides,
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
        assert result.success
        assert result.value == ["USERS", "ORDERS", "PRODUCTS"]

    def test_filter_tables_on_empty_discovery_reports_not_found(
        self,
        tap_oracle_settings_overrides: dict[str, str | int],
    ) -> None:
        config = FlextTapOracleSettings.fetch_global(
            overrides=tap_oracle_settings_overrides,
        )
        result = u.TapOracle.tap_oracle_client_filter_tables(
            tap_config=config,
            discovered_tables=[],
        )
        # No discovered tables is a failure, not a silent empty success.
        assert result.failure
        assert "not found" in str(result.error).lower()
