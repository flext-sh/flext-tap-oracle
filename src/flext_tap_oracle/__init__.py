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

from flext_tap_oracle.__version__ import __version__, __version_info__
from flext_tap_oracle.config import (
    FlextMeltanoTapOracleConfig,
    create_oracle_tap_config,
)
from flext_tap_oracle.models import (
    FlextMeltanoTapOracleModels,
    TapOracleColumn,
    TapOracleSchema,
    TapOracleTable,
    TapReplicationMethod,
)
from flext_tap_oracle.protocols import FlextMeltanoTapOracleProtocols
from flext_tap_oracle.tap_client import (
    FlextOracleConnectionTestService,
    FlextOracleDiscoveryService,
    FlextOracleTableFilterService,
    FlextOracleTapService,
    create_oracle_discovery_service,
    create_oracle_tap_service,
)
from flext_tap_oracle.tap_exceptions import (
    FlextMeltanoTapOracleConfigurationError,
    FlextMeltanoTapOracleConnectionError,
    FlextMeltanoTapOracleDiscoveryError,
    FlextMeltanoTapOracleError,
    FlextMeltanoTapOracleExtractionError,
    FlextMeltanoTapOracleMetadataError,
    FlextMeltanoTapOracleProcessingError,
    FlextMeltanoTapOracleQueryError,
    FlextMeltanoTapOracleStreamError,
    FlextMeltanoTapOracleValidationError,
)
from flext_tap_oracle.tap_streams import (
    FlextOracleStream,
    create_oracle_stream,
    create_oracle_stream_from_table,
)
from flext_tap_oracle.typings import FlextMeltanoTapOracleTypes
from flext_tap_oracle.utilities import FlextMeltanoTapOracleUtilities

# Domain-specific aliases
u = FlextMeltanoTapOracleUtilities  # Utilities (FlextMeltanoTapOracleUtilities extends FlextUtilities)

__all__ = [
    "FlextDbOracleApi",
    "FlextDbOracleConfig",
    "FlextMeltanoBridge",
    "FlextMeltanoConfig",
    "FlextMeltanoTapOracleConfig",
    "FlextMeltanoTapOracleConfigurationError",
    "FlextMeltanoTapOracleConnectionError",
    "FlextMeltanoTapOracleDiscoveryError",
    "FlextMeltanoTapOracleError",
    "FlextMeltanoTapOracleExtractionError",
    "FlextMeltanoTapOracleMetadataError",
    "FlextMeltanoTapOracleModels",
    "FlextMeltanoTapOracleProcessingError",
    "FlextMeltanoTapOracleProtocols",
    "FlextMeltanoTapOracleQueryError",
    "FlextMeltanoTapOracleStreamError",
    "FlextMeltanoTapOracleTypes",
    "FlextMeltanoTapOracleUtilities",
    "FlextMeltanoTapOracleValidationError",
    "FlextOracleConnectionTestService",
    "FlextOracleDiscoveryService",
    "FlextOracleStream",
    "FlextOracleTableFilterService",
    "FlextOracleTapService",
    "TapOracleColumn",
    "TapOracleSchema",
    "TapOracleTable",
    "TapReplicationMethod",
    "__version__",
    "__version_info__",
    "create_oracle_discovery_service",
    "create_oracle_stream",
    "create_oracle_stream_from_table",
    "create_oracle_tap_config",
    "create_oracle_tap_service",
    # Domain-specific aliases
    "u",
]
