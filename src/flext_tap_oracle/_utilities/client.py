"""Oracle Tap Client Services Utilities.

Utilities for Oracle tap operations: discovery, connection testing,
table filtering.

Copyright (c) 2025 FLEXT Contributors
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from collections.abc import (
    Sequence,
)

from flext_db_oracle import FlextDbOracleApi, FlextDbOracleModels
from flext_meltano import e, p, r, t, u
from flext_tap_oracle.constants import c
from flext_tap_oracle.settings import FlextTapOracleSettings

logger = u.fetch_logger(__name__)


class FlextTapOracleUtilitiesClientMixin:
    """Mixin providing Oracle tap client utility methods."""

    @staticmethod
    def tap_oracle_client_discover_tables(
        oracle_api: FlextDbOracleApi,
        schema_name: str | None = None,
    ) -> p.Result[Sequence[FlextDbOracleModels.DbOracle.Table]]:
        """Execute Oracle table discovery using Layer 2 flext-db-oracle API."""

        def _run_tap_oracle_client_discover_tables() -> p.Result[
            Sequence[FlextDbOracleModels.DbOracle.Table]
        ]:
            target_schema = schema_name or "USER"
            logger.info("Discovering Oracle tables in schema: %s", target_schema)
            tables_result = oracle_api.fetch_tables(schema=target_schema)
            if tables_result.failure:
                error_msg = tables_result.error or "Table discovery failed"
                logger.warning("Oracle table discovery failed: %s", error_msg)
                return r[Sequence[FlextDbOracleModels.DbOracle.Table]].fail(error_msg)

            table_names = tables_result.value or []
            tables: t.SequenceOf[FlextDbOracleModels.DbOracle.Table] = [
                FlextDbOracleModels.DbOracle.Table(
                    name=name,
                    owner=target_schema,
                    columns=[],
                )
                for name in table_names
            ]

            logger.info(
                "Discovered %d Oracle tables in schema %s", len(tables), target_schema
            )
            return r[Sequence[FlextDbOracleModels.DbOracle.Table]].ok(tables)

        try:
            return _run_tap_oracle_client_discover_tables()
        except c.Meltano.SINGER_SAFE_EXCEPTIONS as exc:
            logger.exception("Oracle table discovery error")
            return r[Sequence[FlextDbOracleModels.DbOracle.Table]].fail(
                f"Table discovery error in schema {schema_name}: {exc}"
            )

    @staticmethod
    def tap_oracle_client_test_connection(
        oracle_api: FlextDbOracleApi,
    ) -> p.Result[bool]:
        """Execute Oracle connection test using Layer 2 flext-db-oracle API."""

        def _run_tap_oracle_client_test_connection() -> p.Result[bool]:
            logger.info("Testing Oracle connection")
            test_result = oracle_api.test_connection()
            if test_result.success:
                logger.info("Oracle connection test successful")
                return r[bool].ok(value=True)

            error_msg = test_result.error or "Connection test failed"
            logger.error("Oracle connection test failed: %s", error_msg)
            return r[bool].fail(error_msg)

        try:
            return _run_tap_oracle_client_test_connection()
        except c.Meltano.SINGER_SAFE_EXCEPTIONS as exc:
            logger.exception("Oracle connection test error")
            return r[bool].fail(f"Connection test error: {exc}")

    @staticmethod
    def tap_oracle_client_filter_tables(
        tap_config: FlextTapOracleSettings,
        discovered_tables: t.SequenceOf[FlextDbOracleModels.DbOracle.Table],
    ) -> p.Result[t.StrSequence]:
        """Return discovered Oracle table names.

        FlextTapOracleSettings exposes no ``tables_filter`` / ``exclude_tables``
        fields, so the previous filter branches were unreachable — kept signature
        for stable API.
        """
        _ = tap_config
        if not discovered_tables:
            return e.fail_not_found("oracle_tables", "discovered")
        return r[t.StrSequence].ok([table.name for table in discovered_tables])

    @staticmethod
    def tap_oracle_client_initialize_tap(
        oracle_api: FlextDbOracleApi,
        _tap_config: FlextTapOracleSettings,
        schema_name: str | None = None,
    ) -> p.Result[bool]:
        """Initialize Oracle tap by testing connection and discovering tables."""

        def _run_tap_oracle_client_initialize_tap() -> p.Result[bool]:
            logger.info("Initializing Oracle tap service")
            connection_result = (
                FlextTapOracleUtilitiesClientMixin.tap_oracle_client_test_connection(
                    oracle_api
                )
            )
            if connection_result.failure:
                return r[bool].fail_op("Connection test", connection_result.error)

            discovery_result = (
                FlextTapOracleUtilitiesClientMixin.tap_oracle_client_discover_tables(
                    oracle_api, schema_name
                )
            )
            if discovery_result.failure:
                return r[bool].fail_op("Table discovery", discovery_result.error)

            logger.info("Oracle tap initialization completed successfully")
            return r[bool].ok(value=True)

        try:
            return _run_tap_oracle_client_initialize_tap()
        except c.Meltano.SINGER_SAFE_EXCEPTIONS as exc:
            logger.exception("Oracle tap initialization failed")
            return r[bool].fail_op("Initialization", exc)


__all__: list[str] = ["FlextTapOracleUtilitiesClientMixin"]
