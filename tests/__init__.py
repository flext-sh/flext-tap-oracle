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
from typing import TYPE_CHECKING as _TYPE_CHECKING

from flext_core.lazy import install_lazy_exports

if _TYPE_CHECKING:
    from flext_core import FlextTypes
    from flext_tests import d, e, h, r, s, x

    from tests.conftest import *
    from tests.constants import *
    from tests.models import *
    from tests.protocols import *
    from tests.test_enterprise_tap import *
    from tests.typings import *
    from tests.utilities import *

_LAZY_IMPORTS: Mapping[str, str | Sequence[str]] = {
    "FlextTapOracleTestConstants": "tests.constants",
    "FlextTapOracleTestModels": "tests.models",
    "FlextTapOracleTestProtocols": "tests.protocols",
    "FlextTapOracleTestTypes": "tests.typings",
    "FlextTapOracleTestUtilities": "tests.utilities",
    "TestFlextOracleTapSettingsAndHelpers": "tests.test_enterprise_tap",
    "c": ("tests.constants", "FlextTapOracleTestConstants"),
    "conftest": "tests.conftest",
    "constants": "tests.constants",
    "d": "flext_tests",
    "discovery_config": "tests.conftest",
    "docker_control": "tests.conftest",
    "e": "flext_tests",
    "error_scenarios": "tests.conftest",
    "h": "flext_tests",
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
    "r": "flext_tests",
    "s": "flext_tests",
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
    "x": "flext_tests",
}


install_lazy_exports(__name__, globals(), _LAZY_IMPORTS)
