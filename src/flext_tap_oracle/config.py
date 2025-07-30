"""Oracle Tap Configuration using flext-db-oracle types.

This module provides Oracle tap configuration by extending flext-db-oracle
configuration classes to avoid duplication and ensure consistency.
"""

from __future__ import annotations

from pydantic import BaseModel, Field, SecretStr

# Import Oracle config from flext-db-oracle
from flext_db_oracle import FlextDbOracleConfig


class TapOracleConfig(BaseModel):
    """Oracle Tap configuration extending flext-db-oracle config."""

    # Oracle connection - use flext-db-oracle config directly
    host: str = Field(..., description="Oracle database host")
    port: int = Field(default=1521, description="Oracle database port")
    service_name: str | None = Field(None, description="Oracle service name")
    username: str = Field(..., description="Oracle username")
    password: str = Field(..., description="Oracle password")
    schema_name: str | None = Field(None, description="Oracle schema name")

    # Tap-specific configuration
    tables: list[str] | None = Field(None, description="List of tables to extract")
    exclude_tables: list[str] | None = Field(
        None, description="List of tables to exclude",
    )
    replication_method: str = Field(
        default="FULL_TABLE", description="Replication method",
    )
    batch_size: int = Field(default=10000, description="Batch size for data extraction")
    environment: str = Field(default="development", description="Environment")

    def to_oracle_config(self) -> FlextDbOracleConfig:
        """Convert to FlextDbOracleConfig for database connectivity."""
        return FlextDbOracleConfig(
            host=self.host,
            port=self.port,
            service_name=self.service_name,
            username=self.username,
            password=SecretStr(self.password),
        )


# Alias for backward compatibility
Config = TapOracleConfig

__all__ = [
    "Config",
    "TapOracleConfig",
]
