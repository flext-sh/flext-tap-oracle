"""FLEXT Tap Oracle - Oracle Database Singer Tap for FLEXT ecosystem.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from flext_db_oracle import (
    FlextDbOracleApi,
    FlextDbOracleConfig,
)
from flext_meltano import (
    FlextMeltanoBridge,
    FlextMeltanoConfig,
)
from flext_tap_oracle.config import (
    FlextTapOracleConfig,
    create_oracle_tap_config,
)
from flext_tap_oracle.models import (
    FlextTapOracleModels,
    TapOracleColumn,
    TapOracleSchema,
    TapOracleTable,
    TapReplicationMethod,
)
from flext_tap_oracle.protocols import FlextTapOracleProtocols
from flext_tap_oracle.tap_client import (
    FlextOracleConnectionTestService,
    FlextOracleDiscoveryService,
    FlextOracleTableFilterService,
    FlextOracleTapService,
    create_oracle_discovery_service,
    create_oracle_tap_service,
)
from flext_tap_oracle.tap_exceptions import (
    FlextTapOracleConfigurationError,
    FlextTapOracleConnectionError,
    FlextTapOracleDiscoveryError,
    FlextTapOracleError,
    FlextTapOracleExtractionError,
    FlextTapOracleMetadataError,
    FlextTapOracleProcessingError,
    FlextTapOracleQueryError,
    FlextTapOracleStreamError,
    FlextTapOracleValidationError,
)
from flext_tap_oracle.tap_streams import (
    FlextOracleStream,
    create_oracle_stream,
    create_oracle_stream_from_table,
)
from flext_tap_oracle.typings import FlextTapOracleTypes
from flext_tap_oracle.utilities import FlextTapOracleUtilities

__all__ = [
    "FlextDbOracleApi",
    "FlextDbOracleConfig",
    "FlextMeltanoBridge",
    "FlextMeltanoConfig",
    "FlextOracleConnectionTestService",
    "FlextOracleDiscoveryService",
    "FlextOracleStream",
    "FlextOracleTableFilterService",
    "FlextOracleTapService",
    "FlextTapOracleConfig",
    "FlextTapOracleConfigurationError",
    "FlextTapOracleConnectionError",
    "FlextTapOracleDiscoveryError",
    "FlextTapOracleError",
    "FlextTapOracleExtractionError",
    "FlextTapOracleMetadataError",
    "FlextTapOracleModels",
    "FlextTapOracleProcessingError",
    "FlextTapOracleProtocols",
    "FlextTapOracleQueryError",
    "FlextTapOracleStreamError",
    "FlextTapOracleTypes",
    "FlextTapOracleUtilities",
    "FlextTapOracleValidationError",
    "TapOracleColumn",
    "TapOracleSchema",
    "TapOracleTable",
    "TapReplicationMethod",
    "create_oracle_discovery_service",
    "create_oracle_stream",
    "create_oracle_stream_from_table",
    "create_oracle_tap_config",
    "create_oracle_tap_service",
]
