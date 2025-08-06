"""Oracle tap configuration module for FLEXT Tap Oracle using flext-db-oracle infrastructure.

This module provides configuration management for Oracle data extraction
using the flext-db-oracle infrastructure.
"""

from __future__ import annotations

from typing import Any

# Import base configuration from flext-db-oracle
from flext_db_oracle import FlextDbOracleConfig

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
    default_replication_method: str = FlextTapOracleSemanticConstants.Singer.REPLICATION_METHOD_FULL_TABLE

    # Performance settings
    parallel_streams: int = FlextTapOracleSemanticConstants.Performance.DEFAULT_PARALLEL_STREAMS
    max_parallel_streams: int = FlextTapOracleSemanticConstants.Performance.MAX_PARALLEL_STREAMS
    fetch_size: int = FlextTapOracleSemanticConstants.Performance.DEFAULT_FETCH_SIZE

    # Discovery settings
    discovery_batch_size: int = FlextTapOracleSemanticConstants.Performance.DEFAULT_DISCOVERY_BATCH_SIZE

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
        oracle_config = FlextDbOracleConfig(
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
        return oracle_config

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
        schema_name: str | None = None
    ) -> str:
        """Build optimized SELECT query for Oracle table extraction.
        
        Args:
            table_name: Name of the table to query
            schema_name: Optional schema name
            
        Returns:
            Optimized SQL query string

        """
        # Use provided schema or default from config
        effective_schema = schema_name or self.schema_name

        # Build fully qualified table name
        if effective_schema:
            full_table_name = f"{effective_schema}.{table_name}"
        else:
            full_table_name = table_name

        # Build query with Oracle-specific optimizations
        query = f"SELECT * FROM {full_table_name}"

        # Add fetch size hint for performance
        if self.fetch_size and self.fetch_size > 0:
            query = f"{query} /*+ FIRST_ROWS({self.fetch_size}) */"

        return query


# Legacy alias for backward compatibility
Config = TapOracleConfig
