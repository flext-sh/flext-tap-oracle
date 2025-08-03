"""Oracle Tap Configuration using flext-db-oracle types.

This module provides Oracle tap configuration by extending flext-db-oracle
configuration classes to avoid duplication and ensure consistency.
"""

from __future__ import annotations

from pydantic import BaseModel, Field, SecretStr, field_validator

# Import Oracle config from flext-db-oracle
from flext_db_oracle import FlextDbOracleConfig


class TapOracleConfig(BaseModel):
    """Oracle Tap configuration extending flext-db-oracle config with modern Singer SDK functionality."""

    # Oracle connection - use flext-db-oracle config directly
    connection_type: str = Field(
        default="database",
        description="Connection type - database only",
    )
    host: str = Field(..., description="Oracle database host")
    port: int = Field(default=1521, description="Oracle database port")
    service_name: str | None = Field(None, description="Oracle service name")
    username: str = Field(..., description="Oracle username")
    password: str = Field(..., description="Oracle password")
    schema_name: str | None = Field(None, description="Oracle schema name")

    # Tap-specific configuration
    tables: list[str] | None = Field(None, description="List of tables to extract")
    exclude_tables: list[str] | None = Field(
        None,
        description="List of tables to exclude",
    )
    table_pattern: str | None = Field(
        None,
        description="Regex pattern for table filtering",
    )
    replication_method: str = Field(
        default="FULL_TABLE",
        description="Replication method",
    )
    batch_size: int = Field(default=10000, description="Batch size for data extraction")

    # Performance settings
    max_parallel_streams: int = Field(default=2, description="Maximum parallel streams")
    connection_pool_size: int = Field(default=5, description="Connection pool size")

    # Modern Singer SDK features
    enable_async: bool = Field(default=True, description="Enable async operations")
    enable_metrics: bool = Field(default=True, description="Enable metrics collection")
    circuit_breaker_enabled: bool = Field(
        default=True,
        description="Enable circuit breaker",
    )
    circuit_breaker_failure_threshold: int = Field(
        default=3,
        description="Circuit breaker failure threshold",
    )
    circuit_breaker_timeout: int = Field(
        default=60,
        description="Circuit breaker timeout seconds",
    )

    environment: str = Field(default="development", description="Environment")

    @field_validator("connection_type")
    @classmethod
    def validate_connection_type(cls, v: str) -> str:
        """Validate connection type."""
        if v != "database":
            msg = "Connection type must be 'database'"
            raise ValueError(msg)
        return v

    @field_validator("port")
    @classmethod
    def validate_port(cls, v: int) -> int:
        """Validate port range."""
        if not 1 <= v <= 65535:
            msg = "Port must be between 1 and 65535"
            raise ValueError(msg)
        return v

    def to_oracle_config(self) -> FlextDbOracleConfig:
        """Convert to FlextDbOracleConfig for database connectivity."""
        return FlextDbOracleConfig(
            host=self.host,
            port=self.port,
            service_name=self.service_name,
            username=self.username,
            password=SecretStr(self.password),
        )

    def validate_configuration(self) -> bool:
        """Validate complete configuration for Singer tap functionality."""
        try:
            return self._validate_required_fields() and self._validate_port_range()
        except Exception:
            return False

    def _validate_required_fields(self) -> bool:
        """Validate all required database connection fields."""
        required_fields = [self.host, self.username, self.password, self.service_name]
        return all(field for field in required_fields)

    def _validate_port_range(self) -> bool:
        """Validate port is within valid range."""
        return 1 <= self.port <= 65535

    def get_connection_string(self) -> str:
        """Generate connection string for logging (password masked)."""
        return (
            f"oracle://{self.username}:***@{self.host}:{self.port}/{self.service_name}"
        )

    def get_performance_settings(self) -> dict[str, object]:
        """Get performance settings for optimization."""
        return {
            "batch_size": self.batch_size,
            "max_parallel_streams": self.max_parallel_streams,
            "connection_pool_size": self.connection_pool_size,
            "enable_async": self.enable_async,
        }

    def get_circuit_breaker_settings(self) -> dict[str, object]:
        """Get circuit breaker settings for resilience."""
        return {
            "enabled": self.circuit_breaker_enabled,
            "failure_threshold": self.circuit_breaker_failure_threshold,
            "timeout": self.circuit_breaker_timeout,
        }


# Alias for backward compatibility
Config = TapOracleConfig

__all__ = [
    "Config",
    "TapOracleConfig",
]
