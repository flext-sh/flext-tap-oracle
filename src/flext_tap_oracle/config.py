"""Oracle tap configuration module for FLEXT Tap Oracle using flext-db-oracle infrastructure.

This module provides configuration management for Oracle data extraction
using the flext-db-oracle infrastructure.
"""

from __future__ import annotations

from typing import Any

# Import base configuration from flext-db-oracle
from flext_db_oracle import FlextDbOracleApi, FlextDbOracleConfig

# Import constants for defaults
from flext_tap_oracle.constants import FlextTapOracleSemanticConstants


class TapOracleConfig(FlextDbOracleConfig):
    """Oracle Tap configuration extending FlextDbOracleConfig.

    This configuration class extends the base Oracle database configuration
    with tap-specific settings for Singer protocol implementation.
    """

    # Singer-specific configuration
    tables: list[str] | None = None
    exclude_tables: list[str] | None = None
    batch_size: int = FlextTapOracleSemanticConstants.Performance.DEFAULT_BATCH_SIZE
    stream_prefix: str = FlextTapOracleSemanticConstants.Singer.DEFAULT_STREAM_PREFIX

    # Replication settings
    default_replication_method: str = (
        FlextTapOracleSemanticConstants.Singer.REPLICATION_METHOD_FULL_TABLE
    )

    # Performance settings
    parallel_streams: int = (
        FlextTapOracleSemanticConstants.Performance.DEFAULT_PARALLEL_STREAMS
    )
    max_parallel_streams: int = (
        FlextTapOracleSemanticConstants.Performance.MAX_PARALLEL_STREAMS
    )
    fetch_size: int = FlextTapOracleSemanticConstants.Performance.DEFAULT_FETCH_SIZE

    # Discovery settings
    discovery_batch_size: int = (
        FlextTapOracleSemanticConstants.Performance.DEFAULT_DISCOVERY_BATCH_SIZE
    )

    # Schema settings
    schema_name: str | None = None  # Use default schema if not specified

    # Async and advanced features
    enable_async: bool = False
    enable_metrics: bool = True
    connection_type: str = "standard"
    circuit_breaker_enabled: bool = True

    def to_oracle_config(self) -> FlextDbOracleConfig:
        """Convert to base Oracle config for FlextDbOracleApi.

        Returns:
            FlextDbOracleConfig instance compatible with FlextDbOracleApi

        """
        # Create base config with all inherited fields
        return FlextDbOracleConfig(
            host=self.host,
            port=self.port,
            username=self.username,
            password=self.password,
            service_name=self.service_name,
            sid=self.sid,
            pool_min=self.pool_min,
            pool_max=self.pool_max,
            pool_increment=self.pool_increment,
            timeout=self.timeout,
            encoding=self.encoding,
            ssl_enabled=self.ssl_enabled,
            protocol=self.protocol,
        )

    def get_performance_settings(self) -> dict[str, Any]:
        """Get performance-related settings as dictionary.

        Returns:
            Dictionary with performance settings

        """
        return {
            "batch_size": self.batch_size,
            "parallel_streams": self.parallel_streams,
            "max_parallel_streams": self.max_parallel_streams,
            "fetch_size": self.fetch_size,
            "discovery_batch_size": self.discovery_batch_size,
            "enable_async": self.enable_async,
            "circuit_breaker_enabled": self.circuit_breaker_enabled,
            "connection_type": self.connection_type,
        }

    def build_select_query(
        self,
        table_name: str,
        schema_name: str | None = None,
    ) -> str:
        """Build optimized SELECT query for Oracle table extraction.

        This method delegates to flext-db-oracle for consistent SQL generation
        and adds Singer-specific optimizations.

        Args:
            table_name: Name of the table to query
            schema_name: Optional schema name

        Returns:
            Optimized SQL query string

        """
        # Create Oracle API instance for SQL building (no connection needed)
        oracle_api = FlextDbOracleApi()

        # Use flext-db-oracle to build base SELECT query
        base_query_result = oracle_api.build_select(
            table_name=table_name,
            columns=None,  # SELECT * equivalent
            conditions=None,
            schema=schema_name or self.schema_name,
        )

        if base_query_result.is_failure:
            # No fallback - delegate SQL construction to flext-db-oracle only
            # Singer taps should not construct SQL directly
            msg = f"Failed to build Oracle query via flext-db-oracle: {base_query_result.error}"
            raise ValueError(msg)

        base_query = base_query_result.data
        if base_query is None:
            msg = "Failed to build Oracle query: base query is None"
            raise ValueError(msg)

        # Add Singer-specific Oracle performance hints
        if self.fetch_size and self.fetch_size > 0:
            # Add Oracle hint for Singer tap performance optimization
            base_query = f"{base_query} /*+ FIRST_ROWS({self.fetch_size}) */"

        return base_query


# Legacy alias for backward compatibility
Config = TapOracleConfig
