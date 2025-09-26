"""Models for flext-tap-oracle.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from typing import Literal, Self

from pydantic import Field, field_validator, model_validator

from flext_core import FlextConstants, FlextModels, FlextResult


class TapOracleModels(FlextModels):
    """Unified models for Oracle tap operations.

    Extends FlextModels to avoid duplication and ensure consistency.
    This class consolidates all Oracle tap domain models following
    the [Project]Models pattern for centralized Pydantic validation.
    """

    # Legacy type aliases for backward compatibility
    OracleRecord = dict["str", "object"]
    OracleRecords = list[OracleRecord]

    class OracleTapStreamMetadata(FlextModels.Entity):
        """Oracle tap stream metadata - ONLY tap-specific fields.

        Extends Oracle table metadata with tap-specific information.
        """

        # Tap-specific metadata (não duplica FlextDbOracleTable)
        stream_name: str = Field(..., description="Singer stream name")
        replication_method: Literal["FULL_TABLE", "INCREMENTAL"] = Field(
            default=FULL_TABLE,
            description="Replication method for this stream",
        )
        replication_key: str | None = Field(
            default=None,
            description="Column used for incremental replication",
        )
        is_selected: bool = Field(
            default=True,
            description="Whether stream is selected for extraction",
        )

        @field_validator("stream_name")
        @classmethod
        def validate_stream_name(cls, v: str) -> str:
            """Validate stream name follows Singer conventions - Python 3.13 enhanced."""
            if not v or not v.strip():
                msg = "Stream name cannot be empty"
                raise ValueError(msg)

            # Enhanced validation with Python 3.13 string methods
            max_length = FlextConstants.Limits.MAX_STRING_LENGTH
            if len(v) > max_length:
                msg = f"Stream name too long: {len(v)} > {max_length} characters"
                raise ValueError(msg)

            if v.startswith(("_", "-")) or v.endswith(("_", "-")):
                msg = "Stream name cannot start/end with underscore or dash"
                raise ValueError(msg)

            # Remove invalid characters for Singer streams using Python 3.13 enhanced string processing
            cleaned = "".join(c if c.isalnum() or c in "_-" else "_" for c in v)
            return cleaned.lower()

        @model_validator(mode="after")
        def validate_replication_consistency(self) -> Self:
            """Validate replication configuration consistency - Python 3.13 Self typing."""
            if self.replication_method == "INCREMENTAL":
                if not self.replication_key:
                    msg = "Incremental replication requires a replication_key"
                    raise ValueError(msg)

                # Advanced validation: check if replication key is reasonable
                max_key_length = FlextConstants.Limits.MAX_STRING_LENGTH
                if len(self.replication_key) > max_key_length:
                    msg = f"Replication key too long: {len(self.replication_key)} > {max_key_length}"
                    raise ValueError(msg)

            elif self.replication_method == "FULL_TABLE" and self.replication_key:
                msg = "Full table replication should not have replication_key"
                raise ValueError(msg)

            return self

        def validate_business_rules(self: object) -> FlextResult[None]:
            """Validate tap-specific business rules - Python 3.13 enhanced."""
            # This method is kept for backward compatibility but
            # most validation moved to model_validator for better Pydantic integration
            return FlextResult[None].ok(None)
