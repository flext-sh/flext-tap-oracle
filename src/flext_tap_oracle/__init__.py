# AUTO-GENERATED FILE — DO NOT EDIT MANUALLY.
# Regenerate with: make gen
#
"""FLEXT Tap Oracle - Oracle Database Singer Tap for FLEXT ecosystem.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from collections.abc import Mapping, Sequence
from typing import TYPE_CHECKING as _TYPE_CHECKING

from flext_core.lazy import install_lazy_exports, merge_lazy_imports

if _TYPE_CHECKING:
    from flext_db_oracle import d, e, h, r, s, x

    from flext_tap_oracle.__version__ import *
    from flext_tap_oracle._utilities import *
    from flext_tap_oracle.constants import *
    from flext_tap_oracle.models import *
    from flext_tap_oracle.protocols import *
    from flext_tap_oracle.settings import *
    from flext_tap_oracle.streams import *
    from flext_tap_oracle.tap import *
    from flext_tap_oracle.typings import *
    from flext_tap_oracle.utilities import *

_LAZY_IMPORTS: Mapping[str, str | Sequence[str]] = merge_lazy_imports(
    ("flext_tap_oracle._utilities",),
    {
        "FlextTapOracleCli": "flext_tap_oracle.tap",
        "FlextTapOracleConstants": "flext_tap_oracle.constants",
        "FlextTapOracleDiscoverCommand": "flext_tap_oracle.tap",
        "FlextTapOracleModels": "flext_tap_oracle.models",
        "FlextTapOracleProtocols": "flext_tap_oracle.protocols",
        "FlextTapOracleSettings": "flext_tap_oracle.settings",
        "FlextTapOracleStreams": "flext_tap_oracle.streams",
        "FlextTapOracleSyncCommand": "flext_tap_oracle.tap",
        "FlextTapOracleTypes": "flext_tap_oracle.typings",
        "FlextTapOracleUtilities": "flext_tap_oracle.utilities",
        "__author__": "flext_tap_oracle.__version__",
        "__author_email__": "flext_tap_oracle.__version__",
        "__description__": "flext_tap_oracle.__version__",
        "__license__": "flext_tap_oracle.__version__",
        "__title__": "flext_tap_oracle.__version__",
        "__url__": "flext_tap_oracle.__version__",
        "__version__": "flext_tap_oracle.__version__",
        "__version_info__": "flext_tap_oracle.__version__",
        "_utilities": "flext_tap_oracle._utilities",
        "c": ("flext_tap_oracle.constants", "FlextTapOracleConstants"),
        "cli_api": "flext_tap_oracle.tap",
        "constants": "flext_tap_oracle.constants",
        "d": "flext_db_oracle",
        "e": "flext_db_oracle",
        "h": "flext_db_oracle",
        "logger": "flext_tap_oracle.tap",
        "m": ("flext_tap_oracle.models", "FlextTapOracleModels"),
        "main": "flext_tap_oracle.tap",
        "models": "flext_tap_oracle.models",
        "p": ("flext_tap_oracle.protocols", "FlextTapOracleProtocols"),
        "protocols": "flext_tap_oracle.protocols",
        "r": "flext_db_oracle",
        "run_cli": "flext_tap_oracle.tap",
        "s": "flext_db_oracle",
        "settings": "flext_tap_oracle.settings",
        "streams": "flext_tap_oracle.streams",
        "t": ("flext_tap_oracle.typings", "FlextTapOracleTypes"),
        "tap": "flext_tap_oracle.tap",
        "typings": "flext_tap_oracle.typings",
        "u": ("flext_tap_oracle.utilities", "FlextTapOracleUtilities"),
        "utilities": "flext_tap_oracle.utilities",
        "x": "flext_db_oracle",
    },
)


install_lazy_exports(__name__, globals(), _LAZY_IMPORTS)
