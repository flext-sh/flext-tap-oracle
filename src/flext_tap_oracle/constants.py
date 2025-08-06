"""Oracle Tap Constants extending flext-core platform constants.

Oracle Tap-specific constants that extend flext-core patterns.
"""

from __future__ import annotations

from typing import ClassVar, Final

# Import flext-core constants for inheritance
from flext_core.constants import FlextSemanticConstants


class FlextTapOracleSemanticConstants(FlextSemanticConstants):
    """Oracle Tap semantic constants extending FlextSemanticConstants.

    Modern Python 3.13 constants following semantic grouping patterns.
    Extends the FLEXT ecosystem constants with Oracle Tap-specific values
    while maintaining full backward compatibility.
    """

    class ConnectionProtocols:
        """Database connection protocol constants."""

        TCP: Final = "tcp"
        TCPS: Final = "tcps"
        IPC: Final = "ipc"
        ALL: Final = [TCP, TCPS, IPC]
        DEFAULT: Final = TCP

    class OracleDB:
        """Oracle database constants."""

        DEFAULT_PORT: Final = 1521
        DEFAULT_SERVICE_NAME: Final = "XE"
        DEFAULT_SCHEMA: Final = "SYSTEM"
        DEFAULT_ENCODING: Final = "utf-8"

    class OracleDefaults:
        """Oracle default values."""

        CONNECTION_TIMEOUT: Final = 30
        QUERY_TIMEOUT: Final = 300
        POOL_SIZE: Final = 5
        POOL_MAX_OVERFLOW: Final = 10
        BATCH_SIZE: Final = 1000

    class OracleLimits:
        """Oracle limits and constraints."""

        MAX_IDENTIFIER_LENGTH: Final = 128
        MAX_VARCHAR_LENGTH: Final = 4000
        MAX_BATCH_SIZE: Final = 10000
        MIN_BATCH_SIZE: Final = 1

    class Singer:
        """Singer Oracle tap constants."""

        DEFAULT_STREAM_PREFIX: Final = "oracle"
        DEFAULT_BOOKMARK_KEY: Final = "replication_key_value"
        SUPPORTED_REPLICATION_METHODS: Final = ["FULL_TABLE", "INCREMENTAL"]

        # Replication methods
        REPLICATION_METHOD_FULL_TABLE: Final = "FULL_TABLE"
        REPLICATION_METHOD_INCREMENTAL: Final = "INCREMENTAL"
        VALID_REPLICATION_METHODS: ClassVar[set[str]] = {
            REPLICATION_METHOD_FULL_TABLE,
            REPLICATION_METHOD_INCREMENTAL,
        }

    class SSL:
        """SSL mode constants."""

        DISABLE: Final = "disable"
        ALLOW: Final = "allow"
        PREFER: Final = "prefer"
        REQUIRE: Final = "require"
        VERIFY_CA: Final = "verify_ca"
        VERIFY_FULL: Final = "verify_full"
        ALL: Final = [DISABLE, ALLOW, PREFER, REQUIRE, VERIFY_CA, VERIFY_FULL]
        DEFAULT: Final = PREFER

    class Performance:
        """Performance and optimization constants."""

        # Batch sizes
        DEFAULT_BATCH_SIZE: Final = 1000
        MAX_BATCH_SIZE: Final = 10000
        MIN_BATCH_SIZE: Final = 1
        OPTIMAL_BATCH_SIZE: Final = 1000

        # Parallel processing
        DEFAULT_PARALLEL_STREAMS: Final = 1
        MAX_PARALLEL_STREAMS: Final = 8
        OPTIMAL_PARALLEL_STREAMS: Final = 4

        # Connection pooling - CONSUME from flext-core
        DEFAULT_POOL_SIZE: Final = (
            FlextSemanticConstants.Infrastructure.DEFAULT_POOL_SIZE
        )
        MAX_POOL_SIZE: Final = 20
        MIN_POOL_SIZE: Final = 1

        # Discovery
        DEFAULT_DISCOVERY_BATCH_SIZE: Final = 1000
        MAX_DISCOVERY_TIMEOUT: Final = 300

        # State management
        DEFAULT_STATE_INTERVAL: Final = 1000
        STATE_MESSAGE_VERSION: Final = "1.0"

        # Oracle fetch settings
        DEFAULT_FETCH_SIZE: Final = 1000
        DEFAULT_ARRAY_SIZE: Final = 100
        MAX_FETCH_SIZE: Final = 10000
        MAX_ARRAY_SIZE: Final = 10000

    class CircuitBreaker:
        """Circuit breaker constants."""

        FAILURE_THRESHOLD: Final = 3
        TIMEOUT: Final = 60

    class Flattening:
        """Schema flattening constants."""

        DEFAULT_ENABLED: Final = False
        DEFAULT_MAX_DEPTH: Final = 5
        DEFAULT_SEPARATOR: Final = "__"
        MAX_DEPTH: Final = 10
        VALID_SEPARATORS: ClassVar[set[str]] = {"__", "_", "-", "."}


# Backward compatibility aliases
FlextTapOracleConstants = FlextTapOracleSemanticConstants

# Legacy class aliases for backward compatibility
ConnectionProtocols = FlextTapOracleSemanticConstants.ConnectionProtocols
OracleDBConstants = FlextTapOracleSemanticConstants.OracleDB
OracleDefaults = FlextTapOracleSemanticConstants.OracleDefaults
OracleLimits = FlextTapOracleSemanticConstants.OracleLimits
SingerOracleConstants = FlextTapOracleSemanticConstants.Singer
SSLModes = FlextTapOracleSemanticConstants.SSL

# Legacy constants for immediate compatibility (DEPRECATED - use semantic access)
OracleTapConstants = FlextTapOracleSemanticConstants
