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
        try:
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
        try:
            logger.info("Testing Oracle connection")
            test_result = oracle_api.test_connection()
            if test_result.success:
                logger.info("Oracle connection test successful")
                return r[bool].ok(value=True)

            error_msg = test_result.error or "Connection test failed"
            logger.error("Oracle connection test failed: %s", error_msg)
            return r[bool].fail(error_msg)
        except c.Meltano.SINGER_SAFE_EXCEPTIONS as exc:
            logger.exception("Oracle connection test error")
            return r[bool].fail(f"Connection test error: {exc}")

    @staticmethod
    def tap_oracle_client_filter_tables(
        tap_config: FlextTapOracleSettings,
        discovered_tables: t.SequenceOf[FlextDbOracleModels.DbOracle.Table],
    ) -> p.Result[t.StrSequence]:
        """Execute table filtering based on tap configuration."""
        try:
            tap_configuration: t.ConfigurationMapping = tap_config.get_tap_config()
            tables_filter: t.Scalar | t.ScalarList | None = tap_configuration.get(
                "tables_filter"
            )

            if isinstance(tables_filter, list) and tables_filter:
                tables_filter_list: t.StrSequence = list(map(str, tables_filter))
                logger.info(
                    "Using configured table filter: %s", ", ".join(tables_filter_list)
                )
                return r[t.StrSequence].ok(tables_filter_list)

            if not discovered_tables:
                return e.fail_not_found("oracle_tables", "discovered")

            table_names: t.StrSequence = [table.name for table in discovered_tables]
            exclude_tables_raw: t.Scalar | t.ScalarList | None = tap_configuration.get(
                "exclude_tables"
            )
            exclude_tables: t.StrSequence = []

            if isinstance(exclude_tables_raw, list):
                exclude_tables = list(map(str, exclude_tables_raw))

            if exclude_tables:
                filtered_tables = [
                    table for table in table_names if table not in exclude_tables
                ]
                logger.info(
                    "Applied exclusion filter: %d tables excluded, %d remaining",
                    len(exclude_tables),
                    len(filtered_tables),
                )
                return r[t.StrSequence].ok(filtered_tables)

            logger.info(
                "No table exclusions configured, using all %d tables", len(table_names)
            )
            return r[t.StrSequence].ok(table_names)
        except c.Meltano.SINGER_SAFE_EXCEPTIONS as exc:
            logger.exception("Table filtering error")
            return r[t.StrSequence].fail(f"Table filtering error: {exc}")

    @staticmethod
    def tap_oracle_client_initialize_tap(
        oracle_api: FlextDbOracleApi,
        _tap_config: FlextTapOracleSettings,
        schema_name: str | None = None,
    ) -> p.Result[bool]:
        """Initialize Oracle tap by testing connection and discovering tables."""
        try:
            logger.info("Initializing Oracle tap service")
            connection_result = (
                FlextTapOracleUtilitiesClientMixin.tap_oracle_client_test_connection(
                    oracle_api
                )
            )
            if connection_result.failure:
                return r[bool].fail(
                    f"Connection test failed: {connection_result.error}"
                )

            discovery_result = (
                FlextTapOracleUtilitiesClientMixin.tap_oracle_client_discover_tables(
                    oracle_api, schema_name
                )
            )
            if discovery_result.failure:
                return r[bool].fail(f"Table discovery failed: {discovery_result.error}")

            logger.info("Oracle tap initialization completed successfully")
            return r[bool].ok(value=True)
        except c.Meltano.SINGER_SAFE_EXCEPTIONS as exc:
            logger.exception("Oracle tap initialization failed")
            return r[bool].fail(f"Initialization failed: {exc}")


__all__: list[str] = ["FlextTapOracleUtilitiesClientMixin"]
