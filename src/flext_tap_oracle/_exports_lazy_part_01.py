# AUTO-GENERATED FILE — Regenerate with: make gen
"""Lazy export map part."""

from __future__ import annotations

from flext_core.lazy import build_lazy_import_map

FLEXT_TAP_ORACLE_LAZY_IMPORTS_PART_01 = build_lazy_import_map(
    {
        "._utilities": ("_utilities",),
        ".api": (
            "FlextTapOracleService",
            "tap_oracle",
        ),
        ".constants": (
            "FlextTapOracleConstants",
            "c",
        ),
        ".models": (
            "FlextTapOracleModels",
            "m",
        ),
        ".protocols": (
            "FlextTapOracleProtocols",
            "p",
        ),
        ".settings": ("FlextTapOracleSettings",),
        ".tap": (
            "FlextTapOracleCli",
            "FlextTapOracleDiscoverCommand",
            "FlextTapOracleSyncCommand",
        ),
        ".typings": (
            "FlextTapOracleTypes",
            "t",
        ),
        ".utilities": (
            "FlextTapOracleUtilities",
            "u",
        ),
    },
)

__all__: list[str] = ["FLEXT_TAP_ORACLE_LAZY_IMPORTS_PART_01"]
