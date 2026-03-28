"""Re-export shim — canonical implementation lives in _utilities.tap."""

from __future__ import annotations

from flext_tap_oracle._utilities.tap import (
    FlextTapOracleCli,
    FlextTapOracleDiscoverCommand,
    FlextTapOracleSyncCommand,
    cli_api,
    logger,
    main,
    run_cli,
)

__all__ = [
    "FlextTapOracleCli",
    "FlextTapOracleDiscoverCommand",
    "FlextTapOracleSyncCommand",
    "cli_api",
    "logger",
    "main",
    "run_cli",
]
