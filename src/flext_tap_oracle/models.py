"""Oracle Tap Models - ZERO DUPLICAÇÃO usando flext-core + flext-db-oracle.

Este módulo define apenas modelos ESPECÍFICOS do Oracle Tap que NÃO existem
no flext-core ou flext-db-oracle. Todos os modelos base são re-exportados.

Princípio: MAXIMIZAR reutilização, MINIMIZAR duplicação.

Copyright (c) 2025 FLEXT Contributors
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from typing import Literal, Self

# Import base models from flext-core - NEVER duplicate
# Import constants from SINGLE SOURCE - NO duplications
from flext_core import FlextConstants, FlextResult, FlextValueObject

# Import Oracle models from flext-db-oracle - NEVER duplicate
from flext_db_oracle import (
    FlextDbOracleColumn,
    FlextDbOracleSchema,
    FlextDbOracleTable,
)
from pydantic import Field, field_validator, model_validator


class FlextOracleTapStreamMetadata(FlextValueObject):
    """Oracle tap stream metadata - ONLY tap-specific fields.

    Extends Oracle table metadata with tap-specific information.
    """

    # Tap-specific metadata (não duplica FlextDbOracleTable)
    stream_name: str = Field(..., description="Singer stream name")
    replication_method: Literal["FULL_TABLE", "INCREMENTAL"] = Field(
        default="FULL_TABLE",
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

    def validate_business_rules(self) -> FlextResult[None]:
        """Validate tap-specific business rules - Python 3.13 enhanced."""
        # This method is kept for backward compatibility but
        # most validation moved to model_validator for better Pydantic integration
        return FlextResult.ok(None)


class FlextOracleTapConfiguration(FlextValueObject):
    """Oracle tap configuration - ONLY tap-specific settings.

    Complementa FlextDbOracleConfig com configurações específicas do tap.
    """

    # Singer tap specific settings - USE FlextConstants defaults
    batch_size: int = Field(
        default=FlextConstants.Performance.DEFAULT_BATCH_SIZE,
        ge=1,
        le=FlextConstants.Performance.MAX_BATCH_SIZE,
        description="Batch size for data extraction",
    )

    max_parallel_streams: int = Field(
        default=1,  # Oracle-specific default (conservative for database connections)
        ge=1,
        le=FlextConstants.Limits.MAX_THREADS,
        description="Maximum parallel stream processing",
    )

    stream_prefix: str = Field(
        default="oracle",  # Oracle-specific prefix (not duplicating general constants)
        description="Prefix for Singer stream names",
    )

    tables_filter: list[str] | None = Field(
        default=None,
        description="Tables to include (None = all tables)",
    )

    exclude_tables: list[str] | None = Field(
        default=None,
        description="Tables to exclude",
    )

    @model_validator(mode="after")
    def validate_configuration_consistency(self) -> Self:
        """Validate tap configuration consistency - Python 3.13 enhanced validators."""
        # Check for conflicting table filters
        if (
            self.tables_filter
            and self.exclude_tables
            and set(self.tables_filter) & set(self.exclude_tables)
        ):
            conflicting = set(self.tables_filter) & set(self.exclude_tables)
            msg = f"Tables cannot be both included and excluded: {conflicting}"
            raise ValueError(msg)

        # Advanced batch size validation based on parallel streams
        max_load = FlextConstants.Performance.MAX_BATCH_SIZE * 50  # Conservative limit
        total_load = self.batch_size * self.max_parallel_streams
        if total_load > max_load:
            msg = (
                f"Total batch load too high: "
                f"{self.batch_size} x {self.max_parallel_streams} = "
                f"{total_load} > {max_load:,}"
            )
            raise ValueError(msg)

        # Validate table name patterns (Oracle specific)
        if self.tables_filter:
            for table_name in self.tables_filter:
                if not self._is_valid_oracle_table_name(table_name):
                    msg = f"Invalid Oracle table name pattern: {table_name}"
                    raise ValueError(msg)

        return self

    @staticmethod
    def _is_valid_oracle_table_name(name: str) -> bool:
        """Validate Oracle table name pattern - Python 3.13 enhanced."""
        max_length = FlextConstants.Limits.MAX_STRING_LENGTH
        if not name or len(name) > max_length:
            return False

        # Oracle table names: start with letter, contain letters/digits/underscore/dollar/hash
        if not name[0].isalpha():
            return False

        return all(c.isalnum() or c in "_$#" for c in name)

    def validate_business_rules(self) -> FlextResult[None]:
        """Validate tap configuration business rules - backward compatibility."""
        # Kept for backward compatibility, main validation moved to model_validator
        return FlextResult.ok(None)


# Re-export all flext-db-oracle models to avoid import duplication
__all__: list[str] = [
    # Re-export flext-db-oracle models - avoid duplication
    "FlextDbOracleColumn",
    "FlextDbOracleSchema",
    "FlextDbOracleTable",
    "FlextOracleTapConfiguration",
    # Oracle Tap specific models
    "FlextOracleTapStreamMetadata",
]
