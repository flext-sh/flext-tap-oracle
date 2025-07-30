"""Oracle Stream Implementation using flext-meltano generic Stream class.

This module implements a concrete Oracle stream that extends the generic Stream
class from flext-meltano with Oracle-specific data extraction logic.
"""

from __future__ import annotations

from typing import TYPE_CHECKING

from flext_meltano import Stream

from flext_core import get_logger

if TYPE_CHECKING:
    from collections.abc import Iterable, Mapping

    from flext_meltano import Tap

    from flext_db_oracle import FlextDbOracleApi

logger = get_logger(__name__)


class OracleStream(Stream):
    """Concrete Oracle stream implementation that extracts data from Oracle tables."""

    def __init__(
        self,
        tap: Tap,
        name: str,
        table_name: str,
        schema: dict[str, object],
        oracle_api: FlextDbOracleApi,
    ) -> None:
        """Initialize Oracle stream with real Oracle connectivity."""
        super().__init__(tap, name=name, schema=schema)
        self.table_name = table_name
        self.oracle_api = oracle_api

    def get_records(
        self, _context: Mapping[str, object] | None,
    ) -> Iterable[dict[str, object]]:
        """Extract records from Oracle table using real flext-db-oracle API."""
        try:
            # Connect to Oracle database first
            connected_api = self.oracle_api.connect()

            # Build real Oracle query using the actual table name
            sql = f"SELECT * FROM {self.table_name}"

            # Execute query using real Oracle API - returns FlextResult[list[tuple[Any, ...]]]
            result = connected_api.query(sql)

            if result.is_success and result.data:
                # Get column names from schema to convert tuples to dicts
                column_names = list(self.schema.get("properties", {}).keys())

                # Convert each tuple to dict using column names
                for row_tuple in result.data:
                    if column_names:
                        # Convert tuple to dict using column names from schema
                        record = dict(zip(column_names, row_tuple, strict=False))
                    else:
                        # Fallback: create generic column names
                        record = {
                            f"col_{i}": value for i, value in enumerate(row_tuple)
                        }

                    yield record
            else:
                logger.warning(
                    "No data returned from Oracle table %s: %s",
                    self.table_name,
                    result.error if result.is_failure else "Empty result",
                )

        except Exception:
            logger.exception(
                "Failed to extract records from Oracle table %s", self.table_name,
            )
            # Don't yield anything on error - let the tap handle it
