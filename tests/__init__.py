# AUTO-GENERATED FILE — DO NOT EDIT MANUALLY.
# Regenerate with: make gen
#
"""Tests package."""

from __future__ import annotations

from collections.abc import Mapping, Sequence
from typing import TYPE_CHECKING as _TYPE_CHECKING

from flext_core.lazy import install_lazy_exports

if _TYPE_CHECKING:
    from flext_core import FlextTypes
    from flext_core.decorators import FlextDecorators as d
    from flext_core.exceptions import FlextExceptions as e
    from flext_core.handlers import FlextHandlers as h
    from flext_core.mixins import FlextMixins as x
    from flext_core.result import FlextResult as r
    from flext_core.service import FlextService as s
    from tests import (
        conftest,
        constants,
        models,
        protocols,
        test_enterprise_tap,
        typings,
        utilities,
    )
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

_LAZY_IMPORTS: FlextTypes.LazyImportIndex = {
    "FlextTapOracleTestConstants": "tests.constants",
    "FlextTapOracleTestModels": "tests.models",
    "FlextTapOracleTestProtocols": "tests.protocols",
    "FlextTapOracleTestTypes": "tests.typings",
    "FlextTapOracleTestUtilities": "tests.utilities",
    "TestFlextOracleTapSettingsAndHelpers": "tests.test_enterprise_tap",
    "c": ("tests.constants", "FlextTapOracleTestConstants"),
    "conftest": "tests.conftest",
    "constants": "tests.constants",
    "d": ("flext_core.decorators", "FlextDecorators"),
    "discovery_config": "tests.conftest",
    "docker_control": "tests.conftest",
    "e": ("flext_core.exceptions", "FlextExceptions"),
    "error_scenarios": "tests.conftest",
    "h": ("flext_core.handlers", "FlextHandlers"),
    "m": ("tests.models", "FlextTapOracleTestModels"),
    "mock_oracle_connection": "tests.conftest",
    "mock_oracle_tap": "tests.conftest",
    "models": "tests.models",
    "oracle_queries": "tests.conftest",
    "oracle_shared_container_environment": "tests.conftest",
    "oracle_tap": "tests.conftest",
    "oracle_tap_config": "tests.conftest",
    "p": ("tests.protocols", "FlextTapOracleTestProtocols"),
    "performance_test_config": "tests.conftest",
    "protocols": "tests.protocols",
    "pytest_configure": "tests.conftest",
    "r": ("flext_core.result", "FlextResult"),
    "s": ("flext_core.service", "FlextService"),
    "sample_oracle_data": "tests.conftest",
    "sample_oracle_tables": "tests.conftest",
    "set_test_environment": "tests.conftest",
    "shared_oracle_container": "tests.conftest",
    "singer_catalog": "tests.conftest",
    "singer_record_messages": "tests.conftest",
    "singer_schema_message": "tests.conftest",
    "singer_state": "tests.conftest",
    "singer_state_message": "tests.conftest",
    "skip_e2e_if_no_oracle": "tests.conftest",
    "stream_config": "tests.conftest",
    "t": ("tests.typings", "FlextTapOracleTestTypes"),
    "test_enterprise_tap": "tests.test_enterprise_tap",
    "typings": "tests.typings",
    "u": ("tests.utilities", "FlextTapOracleTestUtilities"),
    "utilities": "tests.utilities",
    "x": ("flext_core.mixins", "FlextMixins"),
}


install_lazy_exports(__name__, globals(), _LAZY_IMPORTS)
