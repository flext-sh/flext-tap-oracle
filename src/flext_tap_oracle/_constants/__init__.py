# AUTO-GENERATED FILE — Regenerate with: make gen
"""Flext Tap Oracle. Constants package.

Copyright (c) 2026 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from types import MappingProxyType
from typing import TYPE_CHECKING

from flext_core.lazy import install_lazy_exports

if TYPE_CHECKING:
    from flext_tap_oracle._constants.base import FlextTapOracleConstantsBase
    from flext_tap_oracle._constants.replication import (
        FlextTapOracleConstantsReplication,
    )
    from flext_tap_oracle._constants.values import FlextTapOracleConstantsValues


__all__: tuple[str, ...] = (
    "FlextTapOracleConstantsBase",
    "FlextTapOracleConstantsReplication",
    "FlextTapOracleConstantsValues",
)

install_lazy_exports(
    __name__,
    globals(),
    MappingProxyType({
        "FlextTapOracleConstantsBase": ".base",
        "FlextTapOracleConstantsReplication": ".replication",
        "FlextTapOracleConstantsValues": ".values",
    }),
    public_exports=__all__,
)
