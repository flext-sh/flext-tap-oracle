"""FLEXT Tap Oracle - Oracle Database Singer Tap for FLEXT ecosystem.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT

"""

from __future__ import annotations

from flext_tap_oracle.__version__ import __version__, __version_info__
from flext_tap_oracle.client import (
    FlextOracleConnectionTestService,
    FlextOracleDiscoveryService,
    FlextOracleTableFilterService,
    FlextOracleTapService,
)
from flext_tap_oracle.constants import FlextMeltanoTapOracleConstants, c
from flext_tap_oracle.models import FlextMeltanoTapOracleModels, m
from flext_tap_oracle.protocols import FlextMeltanoTapOracleProtocols, p
from flext_tap_oracle.settings import FlextMeltanoTapOracleSettings
from flext_tap_oracle.streams import FlextOracleStream
from flext_tap_oracle.typings import FlextMeltanoTapOracleTypes, t
from flext_tap_oracle.utilities import FlextMeltanoTapOracleUtilities, u

__all__ = [
    "FlextMeltanoTapOracleConstants",
    "FlextMeltanoTapOracleModels",
    "FlextMeltanoTapOracleProtocols",
    "FlextMeltanoTapOracleSettings",
    "FlextMeltanoTapOracleTypes",
    "FlextMeltanoTapOracleUtilities",
    "FlextOracleConnectionTestService",
    "FlextOracleDiscoveryService",
    "FlextOracleStream",
    "FlextOracleTableFilterService",
    "FlextOracleTapService",
    "__version__",
    "__version_info__",
    "c",
    "m",
    "p",
    "t",
    "u",
]
