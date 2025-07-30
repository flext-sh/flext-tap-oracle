"""FLEXT Tap Oracle - Oracle Database Singer Tap Implementation.

This project implements Oracle Database specific logic using generic flext-meltano interfaces
and flext-db-oracle for database connectivity. No implementation should be duplicated from
other FLEXT projects.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

# Import generic interfaces from flext-meltano
from flext_meltano import Stream, Tap, singer_typing as th

# Import specific Oracle implementations from this project
from .config import Config, TapOracleConfig
from .oracle_stream import OracleStream
from .tap import TapOracle

__version__ = "0.9.0"

__all__ = [
    "Config",
    "OracleStream",
    "Stream",
    "Tap",
    "TapOracle",
    "TapOracleConfig",
    "__version__",
    "th",
]
