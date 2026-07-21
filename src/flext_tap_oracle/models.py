"""Models for flext-tap-oracle.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT

"""

from __future__ import annotations

from typing import TYPE_CHECKING, Annotated, Self

from flext_db_oracle import m, u
from flext_meltano import FlextMeltanoModels

if TYPE_CHECKING:
    from collections.abc import MutableSequence

    from flext_tap_oracle import t


class FlextTapOracleModels(FlextMeltanoModels, m):
    """Complete models for Oracle tap operations extending m.

    Provides standardized models for all Oracle tap domain entities including:
    - Singer stream metadata and configuration
    - Oracle table extraction configuration
    - Replication and discovery operations
    - Performance monitoring and metrics
    - Singer protocol compliance models

    All nested classes inherit m validation and patterns.
    """

    class TapOracle:
        """Tap Oracle  namespace for cross-project access."""

        class _MetricsBase(m.Entity):
            """Shared metrics fields for Oracle tap operations."""

            total_records: Annotated[
                t.NonNegativeInt,
                u.Field(description="Total records extracted"),
            ] = 0
            total_bytes: Annotated[
                t.NonNegativeInt,
                u.Field(description="Total bytes processed"),
            ] = 0
            streams_processed: Annotated[
                t.NonNegativeInt,
                u.Field(description="Number of streams processed"),
            ] = 0
            avg_records_per_second: Annotated[
                t.NonNegativeFloat,
                u.Field(description="Average records per second"),
            ] = 0.0
            avg_bytes_per_second: Annotated[
                t.NonNegativeFloat,
                u.Field(description="Average bytes per second"),
            ] = 0.0
            oracle_connection_time: Annotated[
                t.NonNegativeFloat,
                u.Field(description="Oracle connection time"),
            ] = 0.0
            oracle_query_time: Annotated[
                t.NonNegativeFloat,
                u.Field(description="Total Oracle query time"),
            ] = 0.0

        class OracleTapExecutionStats(_MetricsBase):
            """Oracle tap execution statistics and metrics.

            Tracks runtime statistics for tap execution, performance metrics,
            and operational information.
            """

            # Execution metadata
            execution_id: Annotated[
                t.NonEmptyStr,
                u.Field(..., description="Unique execution identifier"),
            ]
            start_timestamp: Annotated[
                str,
                u.Field(..., description="Execution start time"),
            ]
            end_timestamp: Annotated[
                str | None,
                u.Field(None, description="Execution end time"),
            ]

            # Execution-specific metrics
            duration_seconds: Annotated[
                t.NonNegativeFloat,
                u.Field(
                    description="Total execution duration",
                ),
            ] = 0.0

            # Error tracking
            errors_encountered: Annotated[
                t.NonNegativeInt,
                u.Field(
                    description="Number of errors encountered",
                ),
            ] = 0
            failed_streams: Annotated[
                MutableSequence[str],
                u.Field(
                    description="Names of failed streams",
                ),
            ] = u.Field(default_factory=list)

            # Oracle-specific execution metrics
            oracle_result_processing_time: Annotated[
                t.NonNegativeFloat,
                u.Field(
                    description="Result processing time",
                ),
            ] = 0.0

            @u.computed_field()
            @property
            def execution_stats_summary(self) -> t.TapOracle.SummaryData:
                """Oracle tap execution statistics summary."""
                success_rate = 0.0
                if self.streams_processed > 0:
                    successful_streams = self.streams_processed - len(
                        self.failed_streams,
                    )
                    success_rate = successful_streams / self.streams_processed

                return {
                    "execution_overview": {
                        "execution_id": self.execution_id,
                        "duration_seconds": self.duration_seconds,
                        "status": "completed" if self.end_timestamp else "running",
                    },
                    "volume_metrics": {
                        "streams_processed": self.streams_processed,
                        "total_records": self.total_records,
                        "total_bytes": self.total_bytes,
                        "avg_records_per_stream": self.total_records
                        / self.streams_processed
                        if self.streams_processed > 0
                        else 0,
                    },
                    "performance_metrics": {
                        "records_per_second": self.avg_records_per_second,
                        "bytes_per_second": self.avg_bytes_per_second,
                        "mbps": self.avg_bytes_per_second / (1024 * 1024),
                    },
                    "quality_metrics": {
                        "success_rate": success_rate,
                        "errors_encountered": self.errors_encountered,
                        "failed_streams": len(self.failed_streams),
                        "error_rate": self.errors_encountered / self.total_records
                        if self.total_records > 0
                        else 0,
                    },
                    "oracle_metrics": {
                        "connection_time": self.oracle_connection_time,
                        "query_time": self.oracle_query_time,
                        "processing_time": self.oracle_result_processing_time,
                        "query_efficiency": self.oracle_query_time
                        / self.duration_seconds
                        if self.duration_seconds > 0
                        else 0,
                    },
                }

            def add_stream_stats(
                self,
                records: int,
                bytes_processed: int,
                processing_time: float,
            ) -> FlextTapOracleModels.TapOracle.OracleTapExecutionStats:
                """Return new instance with added statistics for a processed stream."""
                updated: FlextTapOracleModels.TapOracle.OracleTapExecutionStats = self.model_copy(
                    update={
                        "streams_processed": self.streams_processed + 1,
                        "total_records": self.total_records + records,
                        "total_bytes": self.total_bytes + bytes_processed,
                        "oracle_result_processing_time": self.oracle_result_processing_time
                        + processing_time,
                    },
                )
                return updated.update_performance_metrics()

            def mark_stream_error(
                self,
                stream_name: str,
            ) -> FlextTapOracleModels.TapOracle.OracleTapExecutionStats:
                """Return new instance with marked stream error."""
                new_failed_streams: MutableSequence[str] = (
                    [*self.failed_streams] if self.failed_streams else []
                )
                if stream_name not in new_failed_streams:
                    new_failed_streams.append(stream_name)
                updated: FlextTapOracleModels.TapOracle.OracleTapExecutionStats = (
                    self.model_copy(
                        update={
                            "errors_encountered": self.errors_encountered + 1,
                            "failed_streams": new_failed_streams,
                        },
                    )
                )
                return updated

            def to_summary(self) -> t.TapOracle.SummaryData:
                """Create execution summary."""
                return {
                    "execution_id": self.execution_id,
                    "duration_seconds": self.duration_seconds,
                    "streams_processed": self.streams_processed,
                    "total_records": self.total_records,
                    "avg_records_per_second": self.avg_records_per_second,
                    "errors": self.errors_encountered,
                    "success_rate": (
                        (self.streams_processed - len(self.failed_streams))
                        / max(self.streams_processed, 1)
                    )
                    * 100,
                }

            def update_performance_metrics(
                self,
            ) -> FlextTapOracleModels.TapOracle.OracleTapExecutionStats:
                """Return new instance with updated calculated performance metrics."""
                if self.duration_seconds > 0:
                    updated: FlextTapOracleModels.TapOracle.OracleTapExecutionStats = (
                        self.model_copy(
                            update={
                                "avg_records_per_second": self.total_records
                                / self.duration_seconds,
                                "avg_bytes_per_second": self.total_bytes
                                / self.duration_seconds,
                            },
                        )
                    )
                    return updated
                return self

        class OracleTapDiscoverParams(m.Entity):
            """Parameters for Oracle tap discover command."""

            config_file: Annotated[
                str | None,
                u.Field(description="Path to configuration file", default=None),
            ]
            output_file: Annotated[
                str | None,
                u.Field(description="Path to output file", default=None),
            ]

            @classmethod
            def from_click_args(cls, **kwargs: t.Scalar) -> Self:
                """Create discover params from Click command arguments."""
                config_file_value: t.Scalar | None = kwargs.get("config_file")
                output_file_value: t.Scalar | None = kwargs.get("output_file")
                return cls(
                    config_file=str(config_file_value) if config_file_value else None,
                    output_file=str(output_file_value) if output_file_value else None,
                )

        class OracleTapSyncParams(m.Entity):
            """Parameters for Oracle tap sync command."""

            config_file: Annotated[
                str | None,
                u.Field(description="Path to configuration file", default=None),
            ]
            catalog_file: Annotated[
                str | None,
                u.Field(description="Path to catalog file", default=None),
            ]
            state_file: Annotated[
                str | None,
                u.Field(description="Path to state file", default=None),
            ]

            @classmethod
            def from_click_args(cls, **kwargs: t.Scalar) -> Self:
                """Create sync params from Click command arguments."""
                config_file_value: t.Scalar | None = kwargs.get("config_file")
                catalog_file_value: t.Scalar | None = kwargs.get("catalog_file")
                state_file_value: t.Scalar | None = kwargs.get("state_file")
                return cls(
                    config_file=str(config_file_value) if config_file_value else None,
                    catalog_file=str(catalog_file_value)
                    if catalog_file_value
                    else None,
                    state_file=str(state_file_value) if state_file_value else None,
                )


m = FlextTapOracleModels

__all__: list[str] = ["FlextTapOracleModels", "m"]
