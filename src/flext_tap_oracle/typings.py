# AUTO-GENERATED FILE — Regenerate with: make gen
"""FLEXT Tap Oracle Types.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT

"""

from __future__ import annotations

from flext_db_oracle import t
from flext_meltano import t as flext_meltano_t

from flext_tap_oracle._typings import FlextTapOracleTypingsBase


class FlextTapOracleTypes(flext_meltano_t, t):
    """MRO facade composing Meltano + DbOracle type namespaces."""

    class TapOracle(FlextTapOracleTypingsBase):
        """Tap Oracle domain namespace composing the ``_typings`` family base."""


t = FlextTapOracleTypes
__all__: list[str] = ["FlextTapOracleTypes", "t"]
