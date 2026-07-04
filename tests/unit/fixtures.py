"""Shared pytest fixtures for flext-tap-oracle tests."""

from __future__ import annotations

import os
import socket
from collections.abc import Generator
from pathlib import Path

import pytest
from flext_tests import reset_settings as _shared_reset_settings, tk

from flext_tap_oracle import FlextTapOracleSettings
from tests.constants import c
from tests.settings import TestsFlextTapOracleSettings
from tests.utilities import u

reset_settings = _shared_reset_settings


@pytest.fixture(scope="session")
def docker_control() -> tk:
    """Provide Docker control instance for tests."""
    return tk.shared(
        c.TapOracle.Tests.SHARED_CONTAINER_NAME,
        workspace_root=Path(__file__).resolve().parents[2],
    )


@pytest.fixture(scope="session")
def shared_oracle_container(docker_control: tk) -> Generator[str]:
    """Managed Oracle container using tk with auto-start."""
    ensure_result = docker_control.execute()
    if ensure_result.failure:
        pytest.skip(
            ensure_result.error
            or (
                "Oracle container "
                f"{c.TapOracle.Tests.SHARED_CONTAINER_NAME} is unavailable"
            ),
        )
    resolved_port = next(
        (
            int(host_port)
            for container_port, host_port in ensure_result.value.ports.items()
            if container_port.startswith(c.TapOracle.Tests.SHARED_CONTAINER_PORT_PREFIX)
            and host_port.isdigit()
        ),
        c.TapOracle.Tests.SHARED_CONTAINER_DEFAULT_PORT,
    )
    with u.Tests.env_vars_context({
        c.TapOracle.Tests.SHARED_ORACLE_HOST_ENV: c.TapOracle.Tests.SHARED_CONTAINER_HOST,
        c.TapOracle.Tests.SHARED_ORACLE_PORT_ENV: str(resolved_port),
        c.TapOracle.Tests.SHARED_ORACLE_USER_ENV: c.TapOracle.Tests.SHARED_CONTAINER_USER,
        c.TapOracle.Tests.SHARED_ORACLE_PASSWORD_ENV: c.TapOracle.Tests.SHARED_CONTAINER_PASSWORD,
        c.TapOracle.Tests.SHARED_ORACLE_SERVICE_ENV: c.TapOracle.Tests.SHARED_CONTAINER_SERVICE_NAME,
        c.TapOracle.Tests.SHARED_ORACLE_SCHEMA_ENV: c.TapOracle.Tests.SHARED_CONTAINER_SCHEMA_NAME,
    }):
        yield c.TapOracle.Tests.SHARED_CONTAINER_NAME


@pytest.fixture(scope="session")
def oracle_shared_container_environment(
    shared_oracle_container: str,
) -> Generator[None]:
    """Setup Oracle environment variables for shared container."""
    _ = shared_oracle_container
    oracle_env_names: tuple[tuple[str, str], ...] = (
        (
            c.TapOracle.Tests.ORACLE_HOST_ENV,
            c.TapOracle.Tests.SHARED_ORACLE_HOST_ENV,
        ),
        (
            c.TapOracle.Tests.ORACLE_PORT_ENV,
            c.TapOracle.Tests.SHARED_ORACLE_PORT_ENV,
        ),
        (
            c.TapOracle.Tests.ORACLE_USERNAME_ENV,
            c.TapOracle.Tests.SHARED_ORACLE_USER_ENV,
        ),
        (
            c.TapOracle.Tests.ORACLE_PASSWORD_ENV,
            c.TapOracle.Tests.SHARED_ORACLE_PASSWORD_ENV,
        ),
        (
            c.TapOracle.Tests.ORACLE_SERVICE_NAME_ENV,
            c.TapOracle.Tests.SHARED_ORACLE_SERVICE_ENV,
        ),
    )
    with u.Tests.env_vars_context({
        env_name: os.environ.get(env_name, os.environ[fallback_name])
        for env_name, fallback_name in oracle_env_names
    }):
        yield


@pytest.fixture(autouse=True)
def reset_tap_oracle_settings(reset_settings: None) -> Generator[None]:
    """Reset the concrete tap settings singletons around every test.

    The shared ``reset_settings`` fixture only clears the root + test base
    singletons. Tests that trigger ``model_validate`` failures (e.g. missing
    credentials) leave a half-initialised ``FlextTapOracleSettings`` singleton
    behind, so it must be reset here to prevent cross-test pollution.
    """
    _ = reset_settings
    FlextTapOracleSettings.reset_for_testing()
    TestsFlextTapOracleSettings.reset_for_testing()
    try:
        yield
    finally:
        FlextTapOracleSettings.reset_for_testing()
        TestsFlextTapOracleSettings.reset_for_testing()


@pytest.fixture(autouse=True)
def set_test_environment(reset_tap_oracle_settings: None) -> Generator[None]:
    """Set test environment variables."""
    _ = reset_tap_oracle_settings
    with u.Tests.env_vars_context({
        c.TapOracle.Tests.FLEXT_ENV_NAME: c.TapOracle.Tests.TEST_ENV_VALUE,
        c.TapOracle.Tests.FLEXT_LOG_LEVEL_ENV: c.TapOracle.Tests.DEBUG_LOG_LEVEL,
        c.TapOracle.Tests.SINGER_LOG_LEVEL_ENV: c.TapOracle.Tests.DEBUG_LOG_LEVEL,
        c.TapOracle.Tests.TEST_MODE_ENV: c.TapOracle.Tests.TRUE_VALUE,
        c.TapOracle.Tests.SHARED_ORACLE_USER_ENV: c.TapOracle.Tests.UNIT_ORACLE_USER,
        c.TapOracle.Tests.SHARED_ORACLE_PASSWORD_ENV: (
            c.TapOracle.Tests.UNIT_ORACLE_PASSWORD
        ),
    }):
        yield


@pytest.fixture(autouse=True)
def skip_e2e_if_no_oracle() -> None:
    """Skip E2E tests gracefully when Oracle is not available locally."""
    fspath = os.environ.get("PYTEST_CURRENT_TEST", "")
    if "/e2e/" not in fspath and "\\e2e\\" not in fspath:
        return
    host = os.environ.get(
        c.TapOracle.Tests.ORACLE_HOST_ENV,
        os.environ.get(
            c.TapOracle.Tests.SHARED_ORACLE_HOST_ENV,
            c.TapOracle.Tests.SHARED_CONTAINER_HOST,
        ),
    )
    port_str = os.environ.get(
        c.TapOracle.Tests.ORACLE_PORT_ENV,
        os.environ.get(
            c.TapOracle.Tests.SHARED_ORACLE_PORT_ENV,
            str(c.TapOracle.Tests.UNIT_ORACLE_PORT),
        ),
    )
    try:
        port = int(port_str)
    except ValueError:
        port = c.TapOracle.Tests.UNIT_ORACLE_PORT
    try:
        with socket.create_connection(
            (host, port),
            timeout=c.TapOracle.Tests.SOCKET_TIMEOUT_SECONDS,
        ):
            return
    except OSError:
        pytest.skip(
            f"Oracle indisponível em {host}:{port}. Ignorando E2E que requer DB.",
            allow_module_level=False,
        )


@pytest.fixture
def tap_oracle_settings_overrides() -> dict[str, str | int]:
    """Canonical test overrides for tap settings fixtures."""
    return {
        "oracle_host": c.TapOracle.Tests.UNIT_ORACLE_HOST,
        "oracle_port": c.TapOracle.Tests.UNIT_ORACLE_PORT,
        "oracle_service_name": c.TapOracle.Tests.UNIT_ORACLE_SERVICE_NAME,
        "oracle_user": c.TapOracle.Tests.UNIT_ORACLE_USER,
        "oracle_password": c.TapOracle.Tests.UNIT_ORACLE_PASSWORD,
        "batch_size": c.TapOracle.Tests.UNIT_BATCH_SIZE,
    }


@pytest.fixture
def tap_oracle_create_params() -> dict[str, str | int]:
    """Canonical create_oracle_tap_config params for tests."""
    return {
        "oracle_host": c.TapOracle.Tests.CREATE_CONFIG_HOST,
        "oracle_port": c.TapOracle.Tests.CREATE_CONFIG_PORT,
        "oracle_service_name": c.TapOracle.Tests.CREATE_CONFIG_SERVICE_NAME,
        "oracle_user": c.TapOracle.Tests.CREATE_CONFIG_USER,
        "oracle_password": c.TapOracle.Tests.CREATE_CONFIG_PASSWORD,
    }
