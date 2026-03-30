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

from collections.abc import Mapping, Sequence
from typing import TYPE_CHECKING

from flext_core.lazy import install_lazy_exports

if TYPE_CHECKING:
    from tests import (
        conftest as conftest,
        constants as constants,
        models as models,
        protocols as protocols,
        test_enterprise_tap as test_enterprise_tap,
        typings as typings,
        utilities as utilities,
    )
    from tests.conftest import (
        discovery_config as discovery_config,
        docker_control as docker_control,
        error_scenarios as error_scenarios,
        mock_oracle_connection as mock_oracle_connection,
        mock_oracle_tap as mock_oracle_tap,
        oracle_queries as oracle_queries,
        oracle_shared_container_environment as oracle_shared_container_environment,
        oracle_tap as oracle_tap,
        oracle_tap_config as oracle_tap_config,
        performance_test_config as performance_test_config,
        pytest_configure as pytest_configure,
        sample_oracle_data as sample_oracle_data,
        sample_oracle_tables as sample_oracle_tables,
        set_test_environment as set_test_environment,
        shared_oracle_container as shared_oracle_container,
        singer_catalog as singer_catalog,
        singer_record_messages as singer_record_messages,
        singer_schema_message as singer_schema_message,
        singer_state as singer_state,
        singer_state_message as singer_state_message,
        skip_e2e_if_no_oracle as skip_e2e_if_no_oracle,
        stream_config as stream_config,
    )
    from tests.constants import (
        FlextTapOracleTestConstants as FlextTapOracleTestConstants,
        FlextTapOracleTestConstants as c,
    )
    from tests.models import (
        FlextTapOracleTestModels as FlextTapOracleTestModels,
        FlextTapOracleTestModels as m,
    )
    from tests.protocols import (
        FlextTapOracleTestProtocols as FlextTapOracleTestProtocols,
        FlextTapOracleTestProtocols as p,
    )
    from tests.test_enterprise_tap import (
        TestFlextOracleTapSettingsAndHelpers as TestFlextOracleTapSettingsAndHelpers,
    )
    from tests.typings import (
        FlextTapOracleTestTypes as FlextTapOracleTestTypes,
        FlextTapOracleTestTypes as t,
    )
    from tests.utilities import (
        FlextTapOracleTestUtilities as FlextTapOracleTestUtilities,
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
    "conftest": ["tests.conftest", ""],
    "constants": ["tests.constants", ""],
    "d": ["flext_tests", "d"],
    "discovery_config": ["tests.conftest", "discovery_config"],
    "docker_control": ["tests.conftest", "docker_control"],
    "e": ["flext_tests", "e"],
    "error_scenarios": ["tests.conftest", "error_scenarios"],
    "h": ["flext_tests", "h"],
    "m": ["tests.models", "FlextTapOracleTestModels"],
    "mock_oracle_connection": ["tests.conftest", "mock_oracle_connection"],
    "mock_oracle_tap": ["tests.conftest", "mock_oracle_tap"],
    "models": ["tests.models", ""],
    "oracle_queries": ["tests.conftest", "oracle_queries"],
    "oracle_shared_container_environment": [
        "tests.conftest",
        "oracle_shared_container_environment",
    ],
    "oracle_tap": ["tests.conftest", "oracle_tap"],
    "oracle_tap_config": ["tests.conftest", "oracle_tap_config"],
    "p": ["tests.protocols", "FlextTapOracleTestProtocols"],
    "performance_test_config": ["tests.conftest", "performance_test_config"],
    "protocols": ["tests.protocols", ""],
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
    "test_enterprise_tap": ["tests.test_enterprise_tap", ""],
    "typings": ["tests.typings", ""],
    "u": ["tests.utilities", "FlextTapOracleTestUtilities"],
    "utilities": ["tests.utilities", ""],
    "x": ["flext_tests", "x"],
}

_EXPORTS: Sequence[str] = [
    "FlextTapOracleTestConstants",
    "FlextTapOracleTestModels",
    "FlextTapOracleTestProtocols",
    "FlextTapOracleTestTypes",
    "FlextTapOracleTestUtilities",
    "TestFlextOracleTapSettingsAndHelpers",
    "c",
    "conftest",
    "constants",
    "d",
    "discovery_config",
    "docker_control",
    "e",
    "error_scenarios",
    "h",
    "m",
    "mock_oracle_connection",
    "mock_oracle_tap",
    "models",
    "oracle_queries",
    "oracle_shared_container_environment",
    "oracle_tap",
    "oracle_tap_config",
    "p",
    "performance_test_config",
    "protocols",
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
    "test_enterprise_tap",
    "typings",
    "u",
    "utilities",
    "x",
]


install_lazy_exports(__name__, globals(), _LAZY_IMPORTS, _EXPORTS)
