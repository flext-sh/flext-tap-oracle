"""Behavioral tests for the public FlextTapOracleSettings contract (ADR-005)."""

from __future__ import annotations

from collections.abc import Sequence

import pytest
from pydantic import ValidationError

from flext_tap_oracle import FlextTapOracleSettings
from tests import c, m, u


class TestsFlextTapOracleEnterpriseTap:
    """Validate observable settings behavior through the public API only."""

    def test_fetch_global_applies_overrides_to_public_fields(
        self,
        tap_oracle_settings_overrides: dict[str, dict[str, str | int]],
    ) -> None:
        config = FlextTapOracleSettings.fetch_global(
            overrides=tap_oracle_settings_overrides,
        )
        assert config.TapOracle.oracle_host == c.TapOracle.Tests.UNIT_ORACLE_HOST
        assert config.TapOracle.oracle_port == c.TapOracle.Tests.UNIT_ORACLE_PORT
        assert (
            config.TapOracle.oracle_service_name
            == c.TapOracle.Tests.UNIT_ORACLE_SERVICE_NAME
        )
        assert config.TapOracle.batch_size == c.TapOracle.Tests.UNIT_BATCH_SIZE

    def test_oracle_namespace_exposes_full_connection_contract(
        self,
        tap_oracle_settings_overrides: dict[str, dict[str, str | int]],
    ) -> None:
        config = FlextTapOracleSettings.fetch_global(
            overrides=tap_oracle_settings_overrides,
        )
        oracle = config.TapOracle
        assert oracle.oracle_host == c.TapOracle.Tests.UNIT_ORACLE_HOST
        assert oracle.oracle_port == c.TapOracle.Tests.UNIT_ORACLE_PORT
        assert oracle.oracle_service_name == c.TapOracle.Tests.UNIT_ORACLE_SERVICE_NAME
        assert oracle.oracle_user == c.TapOracle.Tests.UNIT_ORACLE_USER
        assert oracle.oracle_password == c.TapOracle.Tests.UNIT_ORACLE_PASSWORD

    def test_oracle_credentials_are_plaintext_scalars(
        self,
        tap_oracle_settings_overrides: dict[str, dict[str, str | int]],
    ) -> None:
        config = FlextTapOracleSettings.fetch_global(
            overrides=tap_oracle_settings_overrides,
        )
        # Namespaced credential fields are plain scalars, not SecretStr wrappers.
        assert isinstance(config.TapOracle.oracle_user, str)
        assert isinstance(config.TapOracle.oracle_password, str)
        assert "SecretStr" not in repr(config.TapOracle.oracle_password)

    def test_fetch_global_is_idempotent(self) -> None:
        assert (
            FlextTapOracleSettings.fetch_global()
            is FlextTapOracleSettings.fetch_global()
        )

    def test_model_validate_returns_validated_settings(
        self,
        tap_oracle_create_params: dict[str, str | int],
    ) -> None:
        config = FlextTapOracleSettings.model_validate(
            {"TapOracle": tap_oracle_create_params},
        )
        assert config.TapOracle.oracle_host == c.TapOracle.Tests.CREATE_CONFIG_HOST
        assert config.TapOracle.oracle_port == c.TapOracle.Tests.CREATE_CONFIG_PORT
        assert (
            config.TapOracle.oracle_service_name
            == c.TapOracle.Tests.CREATE_CONFIG_SERVICE_NAME
        )

    def test_model_validate_applies_default_batch_and_prefix(
        self,
        tap_oracle_create_params: dict[str, str | int],
    ) -> None:
        config = FlextTapOracleSettings.model_validate(
            {"TapOracle": tap_oracle_create_params},
        )
        # Grouped defaults are part of the settings contract, not caller-supplied.
        assert config.TapOracle.batch_size == 1000
        assert config.TapOracle.stream_prefix == ""

    def test_model_validate_rejects_out_of_range_port(self) -> None:
        with pytest.raises(ValidationError):
            FlextTapOracleSettings.model_validate(
                {"TapOracle": {"oracle_port": 0}},
            )

    def test_filter_tables_returns_configured_table_names(
        self,
        tap_oracle_settings_overrides: dict[str, dict[str, str | int]],
    ) -> None:
        config = FlextTapOracleSettings.fetch_global(
            overrides=tap_oracle_settings_overrides,
        )
        discovered_tables: Sequence[p.DbOracle.Table] = [
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
        tap_oracle_settings_overrides: dict[str, dict[str, str | int]],
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
