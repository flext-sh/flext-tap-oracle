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
    from flext_tap_oracle import (
        conftest,
        constants,
        models,
        protocols,
        test_enterprise_tap,
        typings,
        utilities,
    )
    from flext_tap_oracle.conftest import (
        config_result,
        discovery_config,
        docker_control,
        error_msg,
        error_scenarios,
        fallback_result,
        mock_oracle_connection,
        mock_oracle_tap,
        oracle_params,
        oracle_queries,
        oracle_shared_container_environment,
        oracle_tap,
        oracle_tap_config,
        performance_test_config,
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
    from flext_tap_oracle.constants import (
        FlextTapOracleTestConstants,
        FlextTapOracleTestConstants as c,
    )
    from flext_tap_oracle.models import (
        FlextTapOracleTestModels,
        FlextTapOracleTestModels as m,
    )
    from flext_tap_oracle.protocols import (
        FlextTapOracleTestProtocols,
        FlextTapOracleTestProtocols as p,
    )
    from flext_tap_oracle.typings import (
        FlextTapOracleTestTypes,
        FlextTapOracleTestTypes as t,
    )
    from flext_tap_oracle.utilities import (
        FlextTapOracleTestUtilities,
        FlextTapOracleTestUtilities as u,
    )

_LAZY_IMPORTS: FlextTypes.LazyImportIndex = {
    "FlextTapOracleTestConstants": "flext_tap_oracle.constants",
    "FlextTapOracleTestModels": "flext_tap_oracle.models",
    "FlextTapOracleTestProtocols": "flext_tap_oracle.protocols",
    "FlextTapOracleTestTypes": "flext_tap_oracle.typings",
    "FlextTapOracleTestUtilities": "flext_tap_oracle.utilities",
    "c": ("flext_tap_oracle.constants", "FlextTapOracleTestConstants"),
    "config_result": "flext_tap_oracle.conftest",
    "conftest": "flext_tap_oracle.conftest",
    "constants": "flext_tap_oracle.constants",
    "d": ("flext_core.decorators", "FlextDecorators"),
    "discovery_config": "flext_tap_oracle.conftest",
    "docker_control": "flext_tap_oracle.conftest",
    "e": ("flext_core.exceptions", "FlextExceptions"),
    "error_msg": "flext_tap_oracle.conftest",
    "error_scenarios": "flext_tap_oracle.conftest",
    "fallback_result": "flext_tap_oracle.conftest",
    "h": ("flext_core.handlers", "FlextHandlers"),
    "m": ("flext_tap_oracle.models", "FlextTapOracleTestModels"),
    "mock_oracle_connection": "flext_tap_oracle.conftest",
    "mock_oracle_tap": "flext_tap_oracle.conftest",
    "models": "flext_tap_oracle.models",
    "oracle_params": "flext_tap_oracle.conftest",
    "oracle_queries": "flext_tap_oracle.conftest",
    "oracle_shared_container_environment": "flext_tap_oracle.conftest",
    "oracle_tap": "flext_tap_oracle.conftest",
    "oracle_tap_config": "flext_tap_oracle.conftest",
    "p": ("flext_tap_oracle.protocols", "FlextTapOracleTestProtocols"),
    "performance_test_config": "flext_tap_oracle.conftest",
    "protocols": "flext_tap_oracle.protocols",
    "r": ("flext_core.result", "FlextResult"),
    "s": ("flext_core.service", "FlextService"),
    "sample_oracle_data": "flext_tap_oracle.conftest",
    "sample_oracle_tables": "flext_tap_oracle.conftest",
    "set_test_environment": "flext_tap_oracle.conftest",
    "shared_oracle_container": "flext_tap_oracle.conftest",
    "singer_catalog": "flext_tap_oracle.conftest",
    "singer_record_messages": "flext_tap_oracle.conftest",
    "singer_schema_message": "flext_tap_oracle.conftest",
    "singer_state": "flext_tap_oracle.conftest",
    "singer_state_message": "flext_tap_oracle.conftest",
    "skip_e2e_if_no_oracle": "flext_tap_oracle.conftest",
    "stream_config": "flext_tap_oracle.conftest",
    "t": ("flext_tap_oracle.typings", "FlextTapOracleTestTypes"),
    "test_enterprise_tap": "flext_tap_oracle.test_enterprise_tap",
    "typings": "flext_tap_oracle.typings",
    "u": ("flext_tap_oracle.utilities", "FlextTapOracleTestUtilities"),
    "utilities": "flext_tap_oracle.utilities",
    "x": ("flext_core.mixins", "FlextMixins"),
}


install_lazy_exports(__name__, globals(), _LAZY_IMPORTS)
