# AUTO-GENERATED FILE — DO NOT EDIT MANUALLY.
# Regenerate with: make gen
#
"""Test module for flext-tap-oracle.

This module provides test infrastructure for flext-tap-oracle with subnamespaces .Tests
following FLEXT ecosystem patterns.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT

"""

from __future__ import annotations

from collections.abc import Mapping, MutableMapping, Sequence
from typing import TYPE_CHECKING

from flext_core.lazy import cleanup_submodule_namespace, lazy_getattr

if TYPE_CHECKING:
    from flext_core import FlextTypes
    from flext_tests import d, e, h, r, s, x

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
        FlextTapOracleTestConstants,
        FlextTapOracleTestConstants as c,
    )
    from tests.models import FlextTapOracleTestModels, FlextTapOracleTestModels as m
    from tests.protocols import (
        FlextTapOracleTestProtocols,
        FlextTapOracleTestProtocols as p,
    )
    from tests.test_enterprise_tap import TestFlextOracleTapSettingsAndHelpers
    from tests.typings import FlextTapOracleTestTypes, FlextTapOracleTestTypes as t
    from tests.utilities import (
        FlextTapOracleTestUtilities,
        FlextTapOracleTestUtilities as u,
    )

_LAZY_IMPORTS: Mapping[str, Sequence[str]] = {
    "FlextTapOracleTestConstants": ["tests.constants", "FlextTapOracleTestConstants"],
    "FlextTapOracleTestModels": ["tests.models", "FlextTapOracleTestModels"],
    "FlextTapOracleTestProtocols": ["tests.protocols", "FlextTapOracleTestProtocols"],
    "FlextTapOracleTestTypes": ["tests.typings", "FlextTapOracleTestTypes"],
    "FlextTapOracleTestUtilities": ["tests.utilities", "FlextTapOracleTestUtilities"],
    "TestFlextOracleTapSettingsAndHelpers": [
        "tests.test_enterprise_tap",
        "TestFlextOracleTapSettingsAndHelpers",
    ],
    "c": ["tests.constants", "FlextTapOracleTestConstants"],
    "d": ["flext_tests", "d"],
    "discovery_config": ["tests.conftest", "discovery_config"],
    "docker_control": ["tests.conftest", "docker_control"],
    "e": ["flext_tests", "e"],
    "error_scenarios": ["tests.conftest", "error_scenarios"],
    "h": ["flext_tests", "h"],
    "m": ["tests.models", "FlextTapOracleTestModels"],
    "mock_oracle_connection": ["tests.conftest", "mock_oracle_connection"],
    "mock_oracle_tap": ["tests.conftest", "mock_oracle_tap"],
    "oracle_queries": ["tests.conftest", "oracle_queries"],
    "oracle_shared_container_environment": [
        "tests.conftest",
        "oracle_shared_container_environment",
    ],
    "oracle_tap": ["tests.conftest", "oracle_tap"],
    "oracle_tap_config": ["tests.conftest", "oracle_tap_config"],
    "p": ["tests.protocols", "FlextTapOracleTestProtocols"],
    "performance_test_config": ["tests.conftest", "performance_test_config"],
    "pytest_configure": ["tests.conftest", "pytest_configure"],
    "r": ["flext_tests", "r"],
    "s": ["flext_tests", "s"],
    "sample_oracle_data": ["tests.conftest", "sample_oracle_data"],
    "sample_oracle_tables": ["tests.conftest", "sample_oracle_tables"],
    "set_test_environment": ["tests.conftest", "set_test_environment"],
    "shared_oracle_container": ["tests.conftest", "shared_oracle_container"],
    "singer_catalog": ["tests.conftest", "singer_catalog"],
    "singer_record_messages": ["tests.conftest", "singer_record_messages"],
    "singer_schema_message": ["tests.conftest", "singer_schema_message"],
    "singer_state": ["tests.conftest", "singer_state"],
    "singer_state_message": ["tests.conftest", "singer_state_message"],
    "skip_e2e_if_no_oracle": ["tests.conftest", "skip_e2e_if_no_oracle"],
    "stream_config": ["tests.conftest", "stream_config"],
    "t": ["tests.typings", "FlextTapOracleTestTypes"],
    "u": ["tests.utilities", "FlextTapOracleTestUtilities"],
    "x": ["flext_tests", "x"],
}

__all__ = [
    "FlextTapOracleTestConstants",
    "FlextTapOracleTestModels",
    "FlextTapOracleTestProtocols",
    "FlextTapOracleTestTypes",
    "FlextTapOracleTestUtilities",
    "TestFlextOracleTapSettingsAndHelpers",
    "c",
    "d",
    "discovery_config",
    "docker_control",
    "e",
    "error_scenarios",
    "h",
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
    "r",
    "s",
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
    "u",
    "x",
]


_LAZY_CACHE: MutableMapping[str, FlextTypes.ModuleExport] = {}


def __getattr__(name: str) -> FlextTypes.ModuleExport:
    """Lazy-load module attributes on first access (PEP 562).

    A local cache ``_LAZY_CACHE`` persists resolved objects across repeated
    accesses during process lifetime.

    Args:
        name: Attribute name requested by dir()/import.

    Returns:
        Lazy-loaded module export type.

    Raises:
        AttributeError: If attribute not registered.

    """
    if name in _LAZY_CACHE:
        return _LAZY_CACHE[name]

    value = lazy_getattr(name, _LAZY_IMPORTS, globals(), __name__)
    _LAZY_CACHE[name] = value
    return value


def __dir__() -> Sequence[str]:
    """Return list of available attributes for dir() and autocomplete.

    Returns:
        List of public names from module exports.

    """
    return sorted(__all__)


cleanup_submodule_namespace(__name__, _LAZY_IMPORTS)
