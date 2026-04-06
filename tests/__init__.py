# AUTO-GENERATED FILE — DO NOT EDIT MANUALLY.
# Regenerate with: make gen
#
"""Tests package."""

from __future__ import annotations

import typing as _t

from flext_core.lazy import install_lazy_exports

if _t.TYPE_CHECKING:
    import tests.conftest as _tests_conftest

    conftest = _tests_conftest
    import tests.constants as _tests_constants
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
        pytest_plugins,
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
        tap_oracle_settings,
    )

    constants = _tests_constants
    import tests.models as _tests_models
    from tests.constants import (
        FlextTapOracleTestConstants,
        FlextTapOracleTestConstants as c,
    )

    models = _tests_models
    import tests.protocols as _tests_protocols
    from tests.models import FlextTapOracleTestModels, FlextTapOracleTestModels as m

    protocols = _tests_protocols
    import tests.test_enterprise_tap as _tests_test_enterprise_tap
    from tests.protocols import (
        FlextTapOracleTestProtocols,
        FlextTapOracleTestProtocols as p,
    )

    test_enterprise_tap = _tests_test_enterprise_tap
    import tests.typings as _tests_typings
    from tests.test_enterprise_tap import TestFlextOracleTapSettingsAndHelpers

    typings = _tests_typings
    import tests.utilities as _tests_utilities
    from tests.typings import FlextTapOracleTestTypes, FlextTapOracleTestTypes as t

    utilities = _tests_utilities
    from flext_core.decorators import FlextDecorators as d
    from flext_core.exceptions import FlextExceptions as e
    from flext_core.handlers import FlextHandlers as h
    from flext_core.mixins import FlextMixins as x
    from flext_core.result import FlextResult as r
    from flext_core.service import FlextService as s
    from tests.utilities import (
        FlextTapOracleTestUtilities,
        FlextTapOracleTestUtilities as u,
    )
_LAZY_IMPORTS = {
    "FlextTapOracleTestConstants": ("tests.constants", "FlextTapOracleTestConstants"),
    "FlextTapOracleTestModels": ("tests.models", "FlextTapOracleTestModels"),
    "FlextTapOracleTestProtocols": ("tests.protocols", "FlextTapOracleTestProtocols"),
    "FlextTapOracleTestTypes": ("tests.typings", "FlextTapOracleTestTypes"),
    "FlextTapOracleTestUtilities": ("tests.utilities", "FlextTapOracleTestUtilities"),
    "TestFlextOracleTapSettingsAndHelpers": (
        "tests.test_enterprise_tap",
        "TestFlextOracleTapSettingsAndHelpers",
    ),
    "c": ("tests.constants", "FlextTapOracleTestConstants"),
    "conftest": "tests.conftest",
    "constants": "tests.constants",
    "d": ("flext_core.decorators", "FlextDecorators"),
    "discovery_config": ("tests.conftest", "discovery_config"),
    "docker_control": ("tests.conftest", "docker_control"),
    "e": ("flext_core.exceptions", "FlextExceptions"),
    "error_scenarios": ("tests.conftest", "error_scenarios"),
    "h": ("flext_core.handlers", "FlextHandlers"),
    "m": ("tests.models", "FlextTapOracleTestModels"),
    "mock_oracle_connection": ("tests.conftest", "mock_oracle_connection"),
    "mock_oracle_tap": ("tests.conftest", "mock_oracle_tap"),
    "models": "tests.models",
    "oracle_queries": ("tests.conftest", "oracle_queries"),
    "oracle_shared_container_environment": (
        "tests.conftest",
        "oracle_shared_container_environment",
    ),
    "oracle_tap": ("tests.conftest", "oracle_tap"),
    "oracle_tap_config": ("tests.conftest", "oracle_tap_config"),
    "p": ("tests.protocols", "FlextTapOracleTestProtocols"),
    "performance_test_config": ("tests.conftest", "performance_test_config"),
    "protocols": "tests.protocols",
    "pytest_configure": ("tests.conftest", "pytest_configure"),
    "pytest_plugins": ("tests.conftest", "pytest_plugins"),
    "r": ("flext_core.result", "FlextResult"),
    "s": ("flext_core.service", "FlextService"),
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
    "t": ("tests.typings", "FlextTapOracleTestTypes"),
    "tap_oracle_settings": ("tests.conftest", "tap_oracle_settings"),
    "test_enterprise_tap": "tests.test_enterprise_tap",
    "typings": "tests.typings",
    "u": ("tests.utilities", "FlextTapOracleTestUtilities"),
    "utilities": "tests.utilities",
    "x": ("flext_core.mixins", "FlextMixins"),
}

__all__ = [
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
    "pytest_plugins",
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
    "tap_oracle_settings",
    "test_enterprise_tap",
    "typings",
    "u",
    "utilities",
    "x",
]


install_lazy_exports(__name__, globals(), _LAZY_IMPORTS)
