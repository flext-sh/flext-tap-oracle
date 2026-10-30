# AUTO-GENERATED FILE — Regenerate with: make gen
"""Flext Tap Oracle. Typings package.

Copyright (c) 2026 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from types import MappingProxyType
from typing import TYPE_CHECKING

from flext_core.lazy import install_lazy_exports

if TYPE_CHECKING:
    from flext_tap_oracle._typings.base import FlextTapOracleTypingsBase


__all__: tuple[str, ...] = ("FlextTapOracleTypingsBase",)

install_lazy_exports(
    __name__,
    globals(),
    MappingProxyType({"FlextTapOracleTypingsBase": ".base"}),
    public_exports=__all__,
)
