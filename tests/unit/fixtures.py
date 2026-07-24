"""Shared pytest fixtures for flext-tap-oracle tests."""

from __future__ import annotations

import os
import socket
from pathlib import Path
from typing import TYPE_CHECKING

import pytest
from flext_tests import reset_settings as _shared_reset_settings, tk

from flext_tap_oracle import FlextTapOracleSettings
from tests import c, u
from tests.settings import TestsFlextTapOracleSettings

if TYPE_CHECKING:
    from collections.abc import Generator

reset_settings = _shared_reset_settings


@pytest.fixture(scope="session")
def docker_control() -> tk:
    """Provide Docker control instance for tests."""
    return tk.shared(
        c.Test.SHARED_CONTAINER_NAME, workspace_root=Path(__file__).resolve().parents[2]
    )


@pytest.fixture(scope="session")
def shared_oracle_container(docker_control: tk) -> Generator[str]:
    """Manage the Oracle container using tk with auto-start."""
    ensure_result = docker_control.execute()
    if ensure_result.failure:
        pytest.skip(
            ensure_result.error
            or (f"Oracle container {c.Test.SHARED_CONTAINER_NAME} is unavailable")
        )
    resolved_port = next(
        (
            int(host_port)
            for container_port, host_port in ensure_result.value.ports.items()
            if container_port.startswith(c.Test.SHARED_CONTAINER_PORT_PREFIX)
            and host_port.isdigit()
        ),
        c.Test.SHARED_CONTAINER_DEFAULT_PORT,
    )
    with u.Tests.env_vars_context({
        c.Test.SHARED_ORACLE_HOST_ENV: c.Test.SHARED_CONTAINER_HOST,
        c.Test.SHARED_ORACLE_PORT_ENV: str(resolved_port),
        c.Test.SHARED_ORACLE_USER_ENV: c.Test.SHARED_CONTAINER_USER,
        c.Test.SHARED_ORACLE_PASSWORD_ENV: c.Test.SHARED_CONTAINER_PASSWORD,
        c.Test.SHARED_ORACLE_SERVICE_ENV: c.Test.SHARED_CONTAINER_SERVICE_NAME,
        c.Test.SHARED_ORACLE_SCHEMA_ENV: c.Test.SHARED_CONTAINER_SCHEMA_NAME,
    }):
        yield c.Test.SHARED_CONTAINER_NAME


@pytest.fixture(scope="session")
def oracle_shared_container_environment(
    shared_oracle_container: str,
) -> Generator[None]:
    """Set up Oracle environment variables for shared container."""
    _ = shared_oracle_container
    oracle_env_names: tuple[tuple[str, str], ...] = (
        (c.Test.ORACLE_HOST_ENV, c.Test.SHARED_ORACLE_HOST_ENV),
        (c.Test.ORACLE_PORT_ENV, c.Test.SHARED_ORACLE_PORT_ENV),
        (c.Test.ORACLE_USERNAME_ENV, c.Test.SHARED_ORACLE_USER_ENV),
        (c.Test.ORACLE_PASSWORD_ENV, c.Test.SHARED_ORACLE_PASSWORD_ENV),
        (c.Test.ORACLE_SERVICE_NAME_ENV, c.Test.SHARED_ORACLE_SERVICE_ENV),
    )
    with u.Tests.env_vars_context({
        env_name: os.environ.get(env_name, os.environ[fallback_name])
        for env_name, fallback_name in oracle_env_names
    }):
        yield


@pytest.fixture
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


@pytest.fixture
def set_test_environment(reset_tap_oracle_settings: None) -> Generator[None]:
    """Set test environment variables."""
    _ = reset_tap_oracle_settings
    with u.Tests.env_vars_context({
        c.Test.FLEXT_ENV_NAME: c.Test.TEST_ENV_VALUE,
        c.Test.FLEXT_LOG_LEVEL_ENV: c.Test.DEBUG_LOG_LEVEL,
        c.Test.SINGER_LOG_LEVEL_ENV: c.Test.DEBUG_LOG_LEVEL,
        c.Test.TEST_MODE_ENV: c.Test.TRUE_VALUE,
        c.Test.SHARED_ORACLE_USER_ENV: c.Test.UNIT_ORACLE_USER,
        c.Test.SHARED_ORACLE_PASSWORD_ENV: (c.Test.UNIT_ORACLE_PASSWORD),
    }):
        yield


@pytest.fixture
def skip_e2e_if_no_oracle() -> None:
    """Skip E2E tests gracefully when Oracle is not available locally."""
    fspath = os.environ.get("PYTEST_CURRENT_TEST", "")
    if "/e2e/" not in fspath and "\\e2e\\" not in fspath:
        return
    host = os.environ.get(
        c.Test.ORACLE_HOST_ENV,
        os.environ.get(c.Test.SHARED_ORACLE_HOST_ENV, c.Test.SHARED_CONTAINER_HOST),
    )
    port_str = os.environ.get(
        c.Test.ORACLE_PORT_ENV,
        os.environ.get(c.Test.SHARED_ORACLE_PORT_ENV, str(c.Test.UNIT_ORACLE_PORT)),
    )
    try:
        port = int(port_str)
    except ValueError:
        port = c.Test.UNIT_ORACLE_PORT
    try:
        with socket.create_connection(
            (host, port), timeout=c.Test.SOCKET_TIMEOUT_SECONDS
        ):
            return
    except OSError:
        pytest.skip(
            f"Oracle indisponível em {host}:{port}. Ignorando E2E que requer DB.",
            allow_module_level=False,
        )


@pytest.fixture
def tap_oracle_settings_overrides() -> dict[str, dict[str, str | int]]:
    """Canonical nested test overrides for the ``TapOracle`` settings namespace."""
    return {
        "TapOracle": {
            "oracle_host": c.Test.UNIT_ORACLE_HOST,
            "oracle_port": c.Test.UNIT_ORACLE_PORT,
            "oracle_service_name": c.Test.UNIT_ORACLE_SERVICE_NAME,
            "oracle_user": c.Test.UNIT_ORACLE_USER,
            "oracle_password": c.Test.UNIT_ORACLE_PASSWORD,
            "batch_size": c.Test.UNIT_BATCH_SIZE,
        }
    }


@pytest.fixture
def tap_oracle_create_params() -> dict[str, str | int]:
    """Canonical ``TapOracle`` namespace payload for model-validate tests."""
    return {
        "oracle_host": c.Test.CREATE_CONFIG_HOST,
        "oracle_port": c.Test.CREATE_CONFIG_PORT,
        "oracle_service_name": c.Test.CREATE_CONFIG_SERVICE_NAME,
        "oracle_user": c.Test.CREATE_CONFIG_USER,
        "oracle_password": c.Test.CREATE_CONFIG_PASSWORD,
    }
