# AUTO-GENERATED FILE — Regenerate with: make gen
"""Flext Tap Oracle. Protocols package.

Copyright (c) 2026 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

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
    from flext_tap_oracle._protocols.params import FlextTapOracleProtocolsParams


__all__: tuple[str, ...] = (
    "FlextTapOracleProtocolsBase",
    "FlextTapOracleProtocolsGeneratedModelsDomainEvent",
    "FlextTapOracleProtocolsGeneratedModelsEntity",
    "FlextTapOracleProtocolsParams",
)

install_lazy_exports(
    __name__,
    globals(),
    {
        "FlextTapOracleProtocolsBase": ".base",
        "FlextTapOracleProtocolsGeneratedModelsDomainEvent": (
            ".generated_models_domainevent"
        ),
        "FlextTapOracleProtocolsGeneratedModelsEntity": ".generated_models_entity",
        "FlextTapOracleProtocolsParams": ".params",
    },
    public_exports=__all__,
)
