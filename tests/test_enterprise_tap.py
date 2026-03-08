"""Integration-focused tests for Oracle tap settings helpers."""
from __future__ import annotations
import os
import pytest
from flext_core import FlextResult
from flext_db_oracle import FlextDbOracleModels
from flext_tap_oracle import FlextOracleDiscoveryService, FlextOracleTableFilterService, FlextTapOracleSettings
from flext_tap_oracle.settings import create_oracle_tap_config

class _DiscoveryStub(FlextOracleDiscoveryService):

    def __init__(self) -> None:
        pass

    def execute(self) -> FlextResult[list[FlextDbOracleModels.DbOracle.Table]]:
        return FlextResult[list[FlextDbOracleModels.DbOracle.Table]].fail('not used')

class TestFlextOracleTapSettingsAndHelpers:
    """Validate settings model behavior and helper service wiring."""

    @pytest.fixture(autouse=True)
    def reset_settings_singleton(self) -> None:
        """Ensure deterministic tests by resetting singleton settings state."""
        FlextTapOracleSettings.reset_global_instance()
        os.environ['FLEXT_TAP_ORACLE_SERVICE_NAME'] = 'XE'
        os.environ['FLEXT_TAP_ORACLE_ORACLE_SERVICE_NAME'] = 'XE'

    def test_settings_model_validate(self) -> None:
        config = FlextTapOracleSettings(oracle_host='test-oracle', oracle_port=1521, oracle_service_name='TESTDB', oracle_sid='', oracle_username='testuser', oracle_password='testpass', batch_size=1000, max_parallel_streams=2)
        config.tables_filter = ['USERS', 'ORDERS', 'PRODUCTS']
        assert config.oracle_host == 'test-oracle'
        assert config.oracle_port == 1521
        assert config.oracle_service_name == 'TESTDB'
        assert config.oracle_username == 'testuser'
        assert config.batch_size == 1000
        assert config.max_parallel_streams == 2
        assert config.tables_filter == ['USERS', 'ORDERS', 'PRODUCTS']

    def test_settings_connection_string(self) -> None:
        config = FlextTapOracleSettings(oracle_host='test-oracle', oracle_port=1521, oracle_service_name='TESTDB', oracle_sid='', oracle_username='testuser', oracle_password='testpass', batch_size=1000, max_parallel_streams=2)
        config.tables_filter = ['USERS', 'ORDERS', 'PRODUCTS']
        connection_string = config.get_connection_string()
        assert connection_string == 'test-oracle:1521/TESTDB'

    def test_create_oracle_tap_config_success(self) -> None:
        result = create_oracle_tap_config(oracle_params={'oracle_host': 'localhost', 'oracle_port': 1521, 'oracle_service_name': 'XE', 'oracle_sid': '', 'oracle_username': 'tap_user', 'oracle_password': 'secret'})
        if result.is_failure:
            pytest.fail(f'Config creation failed: {result.error}')
        assert result.is_success
        assert result.value is not None
        assert result.value.oracle_host == 'localhost'

    def test_create_oracle_tap_config_failure_when_missing_service_or_sid(self) -> None:
        result = create_oracle_tap_config(oracle_params={'oracle_host': 'localhost', 'oracle_port': 1521, 'oracle_username': 'tap_user', 'oracle_password': 'secret', 'oracle_service_name': '', 'oracle_sid': ''})
        assert result.is_failure
        assert 'Either oracle_service_name or oracle_sid must be provided' in str(result.error)

    def test_table_filter_service_uses_configured_tables(self) -> None:
        config = FlextTapOracleSettings(oracle_host='test-oracle', oracle_port=1521, oracle_service_name='TESTDB', oracle_sid='', oracle_username='testuser', oracle_password='testpass', batch_size=1000, max_parallel_streams=2)
        config.tables_filter = ['USERS', 'ORDERS', 'PRODUCTS']
        service = FlextOracleTableFilterService(tap_config=config, discovery_service=_DiscoveryStub())
        result = service.execute()
        assert result.is_success
        assert result.value == ['USERS', 'ORDERS', 'PRODUCTS']
