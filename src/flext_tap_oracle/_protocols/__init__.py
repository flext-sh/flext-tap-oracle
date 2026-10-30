# AUTO-GENERATED FILE — Regenerate with: make gen
"""Flext Tap Oracle. Protocols package.

Copyright (c) 2026 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from types import MappingProxyType
from typing import TYPE_CHECKING

from flext_core.lazy import install_lazy_exports

if TYPE_CHECKING:
    from flext_tap_oracle._protocols.base import FlextTapOracleProtocolsBase
    from flext_tap_oracle._protocols.generated_models_domainevent import (
        FlextTapOracleProtocolsGeneratedModelsDomainEvent,
    )
    from flext_tap_oracle._protocols.generated_models_entity import (
        FlextTapOracleProtocolsGeneratedModelsEntity,
    )


__all__: tuple[str, ...] = (
    "FlextTapOracleProtocolsBase",
    "FlextTapOracleProtocolsGeneratedModelsDomainEvent",
    "FlextTapOracleProtocolsGeneratedModelsEntity",
)

install_lazy_exports(
    __name__,
    globals(),
    MappingProxyType({
        "FlextTapOracleProtocolsBase": ".base",
        "FlextTapOracleProtocolsGeneratedModelsDomainEvent": (
            ".generated_models_domainevent"
        ),
        "FlextTapOracleProtocolsGeneratedModelsEntity": ".generated_models_entity",
    }),
    public_exports=__all__,
)
