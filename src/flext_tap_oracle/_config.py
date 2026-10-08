"""FlextTapOracleConfig — frozen config singleton for flext-tap-oracle (ADR-005 §7).

Model-less: business rules live in ``config/*.yaml`` under the ``TapOracle:`` key and
are exposed through the open ``config.TapOracle`` namespace (``extra="allow"``), with
no per-domain model. Access is ``config.TapOracle.<domain>[<key>...]``.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from typing import Annotated, Self

from flext_meltano import FlextMeltanoConfig

from flext_tap_oracle import m


class _TapOracleNamespace(m.BaseModel):
    """Open, frozen namespace exposing every ``config/*.yaml`` domain model-less."""

    model_config = m.ConfigDict(extra="allow", frozen=True)


class FlextTapOracleConfig(FlextMeltanoConfig):
    """TapOracle config auto-loaded model-less from ``config/*.yaml``.

    MRO carries ``FlextSettings`` FIRST (ENFORCE-042); the class stays a frozen,
    YAML-validated config singleton.
    """

    # ENFORCE-042 namespace-holder contract: ``FlextSettings`` contributes
    # namespacing only — instance machinery stays plain object semantics so the
    # settings singleton ``__new__`` cannot leak into the config singleton.
    # The inherited pydantic ``__init__`` still runs the frozen, YAML-validated
    # construction, and the inherited pydantic ``__setattr__`` keeps the frozen
    # guard.
    def __new__(cls, *args: object, **kwargs: object) -> Self:
        _ = args, kwargs
        return object.__new__(cls)

    def __eq__(self, other: object) -> bool:
        """Preserve identity equality for the config namespace holder.

        Returns:
            True if the other object is the same instance as this one, False otherwise.

        """
        return object.__eq__(self, other)

    def __hash__(self) -> int:
        """Preserve the identity hash paired with identity equality.

        Returns:
            The identity hash of the config object.

        """
        return object.__hash__(self)

    TapOracle: Annotated[
        _TapOracleNamespace,
        m.Field(
            description=(
                "Open namespace exposing ``config/*.yaml`` under ``TapOracle``."
            ),
        ),
    ] = _TapOracleNamespace()


config: FlextTapOracleConfig = FlextTapOracleConfig.fetch_global()
"""Pre-instantiated frozen config — ``from flext_tap_oracle import config``."""

__all__: list[str] = ["FlextTapOracleConfig", "config"]
