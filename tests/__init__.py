# AUTO-GENERATED FILE — DO NOT EDIT MANUALLY.
# Regenerate with: make codegen
#
"""Test module for flext-tap-oracle.

This module provides test infrastructure for flext-tap-oracle with subnamespaces .Tests
following FLEXT ecosystem patterns.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT

"""

from __future__ import annotations

from typing import TYPE_CHECKING

from flext_core.lazy import cleanup_submodule_namespace, lazy_getattr

if TYPE_CHECKING:
    from flext_core.typings import FlextTypes

    from tests.conftest import (
        discovery_config,
        docker_control,
        error_scenarios,
        mock_oracle_connection,
        mock_oracle_tap,
        oracle_queries,
        oracle_shared_container_environment,
        oracle_tap,
        oracle_tap_config,
        performance_test_config,
        pytest_configure,
        sample_oracle_data,
        sample_oracle_tables,
        set_test_environment,
        shared_oracle_container,
        singer_catalog,
        singer_record_messages,
        singer_schema_message,
        singer_state,
        singer_state_message,
        skip_e2e_if_no_oracle,
        stream_config,
    )
    from tests.constants import (
        TestsFlextTapOracleConstants,
        TestsFlextTapOracleConstants as c,
    )
    from tests.models import TestsFlextTapOracleModels, m, tm
    from tests.protocols import TestsFlextTapOracleProtocols, p
    from tests.test_enterprise_tap import TestFlextOracleTapSettingsAndHelpers
    from tests.typings import (
        TestsFlextTapOracleTypes,
        TestsFlextTapOracleTypes as t,
        tt,
    )
    from tests.utilities import TestsFlextTapOracleUtilities, u

# Lazy import mapping: export_name -> (module_path, attr_name)
_LAZY_IMPORTS: dict[str, tuple[str, str]] = {
    "TestFlextOracleTapSettingsAndHelpers": (
        "tests.test_enterprise_tap",
        "TestFlextOracleTapSettingsAndHelpers",
    ),
    "TestsFlextTapOracleConstants": ("tests.constants", "TestsFlextTapOracleConstants"),
    "TestsFlextTapOracleModels": ("tests.models", "TestsFlextTapOracleModels"),
    "TestsFlextTapOracleProtocols": ("tests.protocols", "TestsFlextTapOracleProtocols"),
    "TestsFlextTapOracleTypes": ("tests.typings", "TestsFlextTapOracleTypes"),
    "TestsFlextTapOracleUtilities": ("tests.utilities", "TestsFlextTapOracleUtilities"),
    "c": ("tests.constants", "TestsFlextTapOracleConstants"),
    "discovery_config": ("tests.conftest", "discovery_config"),
    "docker_control": ("tests.conftest", "docker_control"),
    "error_scenarios": ("tests.conftest", "error_scenarios"),
    "m": ("tests.models", "m"),
    "mock_oracle_connection": ("tests.conftest", "mock_oracle_connection"),
    "mock_oracle_tap": ("tests.conftest", "mock_oracle_tap"),
    "oracle_queries": ("tests.conftest", "oracle_queries"),
    "oracle_shared_container_environment": (
        "tests.conftest",
        "oracle_shared_container_environment",
    ),
    "oracle_tap": ("tests.conftest", "oracle_tap"),
    "oracle_tap_config": ("tests.conftest", "oracle_tap_config"),
    "p": ("tests.protocols", "p"),
    "performance_test_config": ("tests.conftest", "performance_test_config"),
    "pytest_configure": ("tests.conftest", "pytest_configure"),
    "sample_oracle_data": ("tests.conftest", "sample_oracle_data"),
    "sample_oracle_tables": ("tests.conftest", "sample_oracle_tables"),
    "set_test_environment": ("tests.conftest", "set_test_environment"),
    "shared_oracle_container": ("tests.conftest", "shared_oracle_container"),
    "singer_catalog": ("tests.conftest", "singer_catalog"),
    "singer_record_messages": ("tests.conftest", "singer_record_messages"),
    "singer_schema_message": ("tests.conftest", "singer_schema_message"),
    "singer_state": ("tests.conftest", "singer_state"),
    "singer_state_message": ("tests.conftest", "singer_state_message"),
    "skip_e2e_if_no_oracle": ("tests.conftest", "skip_e2e_if_no_oracle"),
    "stream_config": ("tests.conftest", "stream_config"),
    "t": ("tests.typings", "TestsFlextTapOracleTypes"),
    "tm": ("tests.models", "tm"),
    "tt": ("tests.typings", "tt"),
    "u": ("tests.utilities", "u"),
}

__all__ = [
    "TestFlextOracleTapSettingsAndHelpers",
    "TestsFlextTapOracleConstants",
    "TestsFlextTapOracleModels",
    "TestsFlextTapOracleProtocols",
    "TestsFlextTapOracleTypes",
    "TestsFlextTapOracleUtilities",
    "c",
    "discovery_config",
    "docker_control",
    "error_scenarios",
    "m",
    "mock_oracle_connection",
    "mock_oracle_tap",
    "oracle_queries",
    "oracle_shared_container_environment",
    "oracle_tap",
    "oracle_tap_config",
    "p",
    "performance_test_config",
    "pytest_configure",
    "sample_oracle_data",
    "sample_oracle_tables",
    "set_test_environment",
    "shared_oracle_container",
    "singer_catalog",
    "singer_record_messages",
    "singer_schema_message",
    "singer_state",
    "singer_state_message",
    "skip_e2e_if_no_oracle",
    "stream_config",
    "t",
    "tm",
    "tt",
    "u",
]


def __getattr__(name: str) -> FlextTypes.ModuleExport:
    """Lazy-load module attributes on first access (PEP 562)."""
    return lazy_getattr(name, _LAZY_IMPORTS, globals(), __name__)


def __dir__() -> list[str]:
    """Return list of available attributes for dir() and autocomplete."""
    return sorted(__all__)


cleanup_submodule_namespace(__name__, _LAZY_IMPORTS)
