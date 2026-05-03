"""Test configuration for flext-tap-oracle.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT

"""

from __future__ import annotations

import os
import socket
from collections.abc import Generator
from pathlib import Path

import pytest
from flext_tests import tk


@pytest.fixture(scope="session")
def docker_control() -> tk:
    """Provide Docker control instance for tests."""
    return tk.shared(
        "flext-oracle-db-test",
        workspace_root=Path(__file__).resolve().parents[2],
    )


@pytest.fixture(scope="session")
def shared_oracle_container(docker_control: tk) -> str:
    """Managed Oracle container using tk with auto-start."""
    container_name = "flext-oracle-db-test"
    ensure_result = docker_control.execute()
    if ensure_result.failure:
        pytest.skip(
            ensure_result.error or f"Oracle container {container_name} is unavailable",
        )
    resolved_port = next(
        (
            int(host_port)
            for container_port, host_port in ensure_result.value.ports.items()
            if container_port.startswith("1521") and host_port.isdigit()
        ),
        1522,
    )
    os.environ.update({
        "FLEXT_TAP_ORACLE_HOST": "localhost",
        "FLEXT_TAP_ORACLE_PORT": str(resolved_port),
        "FLEXT_TAP_ORACLE_USERNAME": "flext_test",
        "FLEXT_TAP_ORACLE_PASSWORD": "flext_test_password",
        "FLEXT_TAP_ORACLE_SERVICE_NAME": "FLEXTDB",
        "FLEXT_TAP_ORACLE_SCHEMA_NAME": "FLEXT_TEST",
    })
    return container_name


@pytest.fixture(scope="session", autouse=True)
def oracle_shared_container_environment(shared_oracle_container: str) -> None:
    """Setup Oracle environment variables for shared container."""
    _ = shared_oracle_container
    os.environ.setdefault("ORACLE_HOST", os.environ["FLEXT_TAP_ORACLE_HOST"])
    os.environ.setdefault("ORACLE_PORT", os.environ["FLEXT_TAP_ORACLE_PORT"])
    os.environ.setdefault("ORACLE_USERNAME", os.environ["FLEXT_TAP_ORACLE_USERNAME"])
    os.environ.setdefault("ORACLE_PASSWORD", os.environ["FLEXT_TAP_ORACLE_PASSWORD"])
    os.environ.setdefault(
        "ORACLE_SERVICE_NAME",
        os.environ["FLEXT_TAP_ORACLE_SERVICE_NAME"],
    )


@pytest.fixture(autouse=True)
def set_test_environment() -> Generator[None]:
    """Set test environment variables."""
    os.environ["FLEXT_ENV"] = "test"
    os.environ["FLEXT_LOG_LEVEL"] = "DEBUG"
    os.environ["SINGER_SDK_LOG_LEVEL"] = "DEBUG"
    os.environ["ORACLE_TAP_TEST_MODE"] = "true"
    yield
    os.environ.pop("FLEXT_ENV", None)
    os.environ.pop("FLEXT_LOG_LEVEL", None)
    os.environ.pop("SINGER_SDK_LOG_LEVEL", None)
    os.environ.pop("ORACLE_TAP_TEST_MODE", None)


def _can_connect(host: str, port: int, timeout: float = 0.5) -> bool:
    try:
        with socket.create_connection((host, port), timeout=timeout):
            return True
    except OSError:
        return False


@pytest.fixture(autouse=True)
def skip_e2e_if_no_oracle() -> None:
    """Skip E2E tests gracefully when Oracle is not available locally."""
    fspath = os.environ.get("PYTEST_CURRENT_TEST", "")
    if "/e2e/" not in fspath and "\\e2e\\" not in fspath:
        return
    host = os.environ.get(
        "ORACLE_HOST",
        os.environ.get("FLEXT_TAP_ORACLE_HOST", "localhost"),
    )
    port_str = os.environ.get(
        "ORACLE_PORT",
        os.environ.get("FLEXT_TAP_ORACLE_PORT", "1521"),
    )
    try:
        port = int(port_str)
    except ValueError:
        port = 1521
    if not _can_connect(host, port):
        pytest.skip(
            f"Oracle indisponível em {host}:{port}. Ignorando E2E que requer DB.",
            allow_module_level=False,
        )
