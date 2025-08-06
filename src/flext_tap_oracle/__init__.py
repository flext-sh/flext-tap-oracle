"""FLEXT Tap Oracle - Oracle Database Singer Tap Implementation.

This project implements Oracle Database specific logic using generic flext-meltano interfaces
and flext-db-oracle for database connectivity. No implementation should be duplicated from
other FLEXT projects.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

# === FLEXT-MELTANO COMPLETE INTEGRATION ===
# Re-export ALL flext-meltano facilities for full ecosystem integration
# Import singer_typing as th for backward compatibility
from flext_meltano import (
    BatchSink,
    FlextMeltanoBaseService,
    # Bridge integration
    FlextMeltanoBridge,
    # Configuration and validation
    FlextMeltanoConfig,
    FlextMeltanoEvent,
    # Enterprise services from flext-meltano.base
    FlextMeltanoTapService,
    # Authentication patterns
    OAuthAuthenticator,
    # Typing definitions
    PropertiesList,
    Property,
    Sink,
    SQLSink,
    # Core Singer SDK classes (centralized from flext-meltano)
    Stream,
    Tap,
    Target,
    create_meltano_tap_service,
    # Testing utilities
    get_tap_test_class,
    # Singer typing utilities (centralized)
    singer_typing,
    singer_typing as th,
)

# Import specific Oracle implementations from this project
from flext_tap_oracle.config import Config, TapOracleConfig
from flext_tap_oracle.oracle_stream import OracleStream
from flext_tap_oracle.tap import TapOracle

__version__ = "0.9.0"

__all__: list[str] = [
    "BatchSink",
    "Config",
    "FlextMeltanoBaseService",
    # Bridge integration
    "FlextMeltanoBridge",
    # Configuration patterns
    "FlextMeltanoConfig",
    "FlextMeltanoEvent",
    # Enterprise services
    "FlextMeltanoTapService",
    # Authentication
    "OAuthAuthenticator",
    "OracleStream",
    "PropertiesList",
    "Property",
    "SQLSink",
    "Sink",
    # === FLEXT-MELTANO COMPLETE RE-EXPORTS ===
    # Singer SDK core classes
    "Stream",
    "Tap",
    # === PRIMARY TAP CLASSES ===
    "TapOracle",
    "TapOracleConfig",
    "Target",
    # === METADATA ===
    "__version__",
    "create_meltano_tap_service",
    # Testing
    "get_tap_test_class",
    # Singer typing
    "singer_typing",
    "th",  # Backward compatibility alias
]
