from __future__ import annotations

import pytest
from flext_core import FlextResult, t
from flext_db_oracle import FlextDbOracleModels
from flext_tap_oracle import (
    FlextMeltanoTapOracleSettings,
    FlextOracleDiscoveryService,
    FlextOracleTableFilterService,
)
from flext_tap_oracle.settings import create_oracle_tap_config


class _DiscoveryStub(FlextOracleDiscoveryService):
    def __init__(self) -> None:
        pass

    def execute(self) -> FlextResult[list[FlextDbOracleModels.DbOracle.Table]]:
        return FlextResult[list[FlextDbOracleModels.DbOracle.Table]].fail("not used")


class TestFlextOracleTapSettingsAndHelpers:
    @pytest.fixture
    def valid_config(self) -> dict[str, t.GeneralValueType]:
        return {
            "oracle_host": "test-oracle",
            "oracle_port": 1521,
            "oracle_service_name": "TESTDB",
            "oracle_username": "testuser",
            "oracle_password": "testpass",
            "batch_size": 1000,
            "max_parallel_streams": 2,
            "tables_filter": ["USERS", "ORDERS", "PRODUCTS"],
        }

    def test_settings_model_validate(
        self, valid_config: dict[str, t.GeneralValueType]
    ) -> None:
        config = FlextMeltanoTapOracleSettings.model_validate(valid_config)

        assert config.oracle_host == "test-oracle"
        assert config.oracle_port == 1521
        assert config.oracle_service_name == "TESTDB"
        assert config.oracle_username == "testuser"
        assert config.batch_size == 1000
        assert config.max_parallel_streams == 2
        assert config.tables_filter == ["USERS", "ORDERS", "PRODUCTS"]

    def test_settings_connection_string(
        self, valid_config: dict[str, t.GeneralValueType]
    ) -> None:
        config = FlextMeltanoTapOracleSettings.model_validate(valid_config)
        connection_string = config.get_connection_string()

        assert connection_string == "test-oracle:1521/TESTDB"

    def test_create_oracle_tap_config_success(self) -> None:
        result = create_oracle_tap_config(
            oracle_params={
                "oracle_host": "localhost",
                "oracle_port": 1521,
                "oracle_service_name": "XE",
                "oracle_username": "tap_user",
                "oracle_password": "secret",
            }
        )

        assert result.is_success
        assert result.value is not None
        assert result.value.oracle_host == "localhost"

    def test_create_oracle_tap_config_failure_when_missing_service_or_sid(self) -> None:
        result = create_oracle_tap_config(
            oracle_params={
                "oracle_host": "localhost",
                "oracle_port": 1521,
                "oracle_username": "tap_user",
                "oracle_password": "secret",
            }
        )

        assert result.is_failure

    def test_table_filter_service_uses_configured_tables(
        self,
        valid_config: dict[str, t.GeneralValueType],
    ) -> None:
        config = FlextMeltanoTapOracleSettings.model_validate(valid_config)
        service = FlextOracleTableFilterService(
            tap_config=config,
            discovery_service=_DiscoveryStub(),
        )

        result = service.execute()

        assert result.is_success
        assert result.value == ["USERS", "ORDERS", "PRODUCTS"]
