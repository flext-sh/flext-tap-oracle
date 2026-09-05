"""Observable contracts of the public Oracle tap facade."""

from __future__ import annotations

from flext_tap_oracle import (
    FlextTapOracleConfig,
    FlextTapOracleService,
    FlextTapOracleSettings,
    FlextTapOracleStreams,
    config,
    m,
    settings,
)
from flext_tests import tm


class TestsFlextTapOracleEnterpriseTap:
    """Validate public settings, config, service, and stream behavior."""

    def test_settings_fixture_consumes_the_public_owner(
        self, tap_oracle_settings: FlextTapOracleSettings
    ) -> None:
        """The fixture exposes production's typed settings singleton."""
        tm.that(tap_oracle_settings, is_=FlextTapOracleSettings)
        tm.that(tap_oracle_settings.model_dump(), eq=settings.model_dump())

    def test_settings_round_trip_preserves_the_public_state(
        self, tap_oracle_settings: FlextTapOracleSettings
    ) -> None:
        """Pydantic ingress preserves every value owned by settings."""
        restored = FlextTapOracleSettings.model_validate(
            tap_oracle_settings.model_dump(mode="python")
        )

        tm.that(restored.model_dump(), eq=tap_oracle_settings.model_dump())

    def test_config_fixture_consumes_the_public_owner(
        self, tap_oracle_config: FlextTapOracleConfig
    ) -> None:
        """The fixture exposes production's validated config singleton."""
        tm.that(tap_oracle_config, is_=FlextTapOracleConfig)
        tm.that(tap_oracle_config.model_dump(), eq=config.model_dump())

    def test_service_executes_through_the_public_facade(
        self, tap_oracle_service: FlextTapOracleService
    ) -> None:
        """The real service reports its own public tap identity."""
        result = tap_oracle_service.execute()

        tm.ok(result)
        tm.that(result.unwrap().get("service"), eq=tap_oracle_service.tap_name)

    def test_stream_transform_preserves_numeric_and_converts_oracle_lobs(
        self,
    ) -> None:
        """The public stream facade applies Oracle's observable type contract."""
        cases = (
            ("NUMBER", 42, 42),
            ("CLOB", 42, "42"),
            ("NCLOB", 42, "42"),
            ("BLOB", 42, "42"),
        )
        for oracle_type, value, expected in cases:
            transformed = (
                FlextTapOracleStreams.OracleStream.transform_oracle_types(
                    {"VALUE": value},
                    [
                        m.DbOracle.ColumnMetadata(
                            name="VALUE", data_type=oracle_type
                        )
                    ],
                )
            )

            tm.that(transformed["VALUE"], eq=expected)
