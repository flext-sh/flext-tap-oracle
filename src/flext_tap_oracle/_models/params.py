"""Tap Oracle command parameter models.

Copyright (c) 2026 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from typing import TYPE_CHECKING, Annotated, Self

from flext_meltano import FlextMeltanoModels, u

if TYPE_CHECKING:
    from flext_tap_oracle import t


class FlextTapOracleModelsParams:
    """Tap command parameter models composed into ``m.TapOracle``."""

    class OracleTapDiscoverParams(FlextMeltanoModels.Entity):
        """Parameters for Oracle tap discover command."""

        config_file: Annotated[
            str | None,
            u.Field(description="Path to configuration file", default=None),
        ]
        output_file: Annotated[
            str | None,
            u.Field(description="Path to output file", default=None),
        ]

        @classmethod
        def from_click_args(cls, **kwargs: t.Scalar) -> Self:
            """Create discover params from Click command arguments.

            Args:
                kwargs: Click command arguments keyed by parameter name;
                    ``config_file`` and ``output_file`` are consumed.

            Returns:
                The resulting ``Self``.

            """
            config_file_value: t.Scalar | None = kwargs.get("config_file")
            output_file_value: t.Scalar | None = kwargs.get("output_file")
            return cls(
                config_file=str(config_file_value) if config_file_value else None,
                output_file=str(output_file_value) if output_file_value else None,
            )

    class OracleTapSyncParams(FlextMeltanoModels.Entity):
        """Parameters for Oracle tap sync command."""

        config_file: Annotated[
            str | None,
            u.Field(description="Path to configuration file", default=None),
        ]
        catalog_file: Annotated[
            str | None,
            u.Field(description="Path to catalog file", default=None),
        ]
        state_file: Annotated[
            str | None,
            u.Field(description="Path to state file", default=None),
        ]

        @classmethod
        def from_click_args(cls, **kwargs: t.Scalar) -> Self:
            """Create sync params from Click command arguments.

            Args:
                kwargs: Click command arguments keyed by parameter name;
                    ``config_file``, ``catalog_file``, and ``state_file``
                    are consumed.

            Returns:
                The resulting ``Self``.

            """
            config_file_value: t.Scalar | None = kwargs.get("config_file")
            catalog_file_value: t.Scalar | None = kwargs.get("catalog_file")
            state_file_value: t.Scalar | None = kwargs.get("state_file")
            return cls(
                config_file=str(config_file_value) if config_file_value else None,
                catalog_file=str(catalog_file_value) if catalog_file_value else None,
                state_file=str(state_file_value) if state_file_value else None,
            )


__all__: list[str] = [
    "FlextTapOracleModelsParams",
]
