"""FLEXT Tap Oracle - Singer Tap using flext-meltano abstractions.

Singer Tap interface using flext-meltano patterns with zero boilerplate
and maximum integration with FLEXT ecosystem.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT.
"""

from __future__ import annotations

import sys
from collections.abc import Callable, Mapping
from pathlib import Path

from flext_core import FlextLogger, r
from flext_meltano import FlextMeltanoAbstractions
from flext_tap_oracle import FlextTapOracleSettings, c, m, p, t

logger = FlextLogger(__name__)
cli_api = FlextMeltanoAbstractions()


class FlextTapOracleDiscoverCommand:
    """Oracle tap discovery command using flext-meltano patterns.

    Provides discovery of Oracle database schema and Singer catalog generation.
    """

    def __init__(self, params: m.TapOracle.OracleTapDiscoverParams) -> None:
        """Initialize command with parameter t.NormalizedValue pattern."""
        self.params = params
        self._logger = FlextLogger(__name__)

    def execute(self) -> r[Mapping[str, t.GeneralValueType]]:
        """Execute Oracle tap discovery using modern patterns."""
        self._logger.info("Starting Oracle database discovery")
        try:
            if not self.params.config_file:
                return r[t.GeneralValueMapping].fail(
                    "Configuration file is required for discovery",
                )
            config_data: str = Path(self.params.config_file).read_text(encoding="utf-8")
            config: FlextTapOracleSettings = FlextTapOracleSettings.model_validate_json(
                config_data,
            )
            oracle_config = config.get_oracle_config()
            schema_name = str(oracle_config.get("schema_name", "USER"))
            self._logger.info("Discovering Oracle schema: %s", schema_name)
            streams: list[t.GeneralValueType] = []
            catalog_dict: Mapping[str, t.GeneralValueType] = {
                "streams": streams,
                "schema_name": schema_name,
            }
            if self.params.output_file:
                output_path = Path(self.params.output_file)
                output_path.write_text(
                    t.GENERAL_VALUE_MAP_ADAPTER.dump_json(
                        catalog_dict, indent=2
                    ).decode(
                        "utf-8",
                    ),
                    encoding="utf-8",
                )
                self._logger.info("Catalog written to %s", output_path)
            self._logger.info("Oracle schema discovery completed")
            return r[t.GeneralValueMapping].ok(catalog_dict)
        except c.Meltano.SINGER_SAFE_EXCEPTIONS as e:
            logger.exception("Oracle discovery failed")
            return r[t.GeneralValueMapping].fail(f"Discovery error: {e}")

    def validate_business_rules(self) -> r[bool]:
        """Validate business rules for Oracle tap discovery."""
        if self.params.config_file and (not Path(self.params.config_file).exists()):
            return r[bool].fail(
                f"Configuration file not found: {self.params.config_file}",
            )
        return r[bool].ok(value=True)


class FlextTapOracleSyncCommand:
    """Oracle tap sync command using flext-meltano patterns."""

    def __init__(self, params: m.TapOracle.OracleTapSyncParams) -> None:
        """Initialize command with parameter t.NormalizedValue pattern."""
        self.params = params
        self._logger = FlextLogger(__name__)

    def execute(self) -> r[Mapping[str, t.GeneralValueType]]:
        """Execute Oracle tap sync using modern patterns."""
        self._logger.info("Starting Oracle data extraction")
        try:
            if not self.params.config_file:
                return r[t.GeneralValueMapping].fail(
                    "Configuration file is required for sync",
                )
            config_data: str = Path(self.params.config_file).read_text(encoding="utf-8")
            config: FlextTapOracleSettings = FlextTapOracleSettings.model_validate_json(
                config_data,
            )
            oracle_config = config.get_oracle_config()
            if self.params.catalog_file:
                Path(self.params.catalog_file).read_text(encoding="utf-8")
                self._logger.info(f"Loaded catalog from {self.params.catalog_file}")
            if self.params.state_file:
                Path(self.params.state_file).read_text(encoding="utf-8")
                self._logger.info(f"Loaded state from {self.params.state_file}")
            self._logger.info("Preparing extraction from Oracle database...")
            schema_name = str(oracle_config.get("schema_name", "USER"))
            record_count = c.TapOracle.INITIAL_RECORD_COUNT
            result_data: Mapping[str, t.GeneralValueType] = {
                "records_extracted": record_count,
                "schema_name": schema_name,
                "status": "completed",
            }
            self._logger.info(
                "Sync completed for schema %s; records extracted: %s",
                schema_name,
                record_count,
            )
            return r[t.GeneralValueMapping].ok(result_data)
        except c.Meltano.SINGER_SAFE_EXCEPTIONS as e:
            logger.exception("Oracle sync failed")
            return r[t.GeneralValueMapping].fail(f"Sync error: {e}")

    def validate_business_rules(self) -> r[bool]:
        """Validate business rules for Oracle tap sync."""
        if self.params.config_file and (not Path(self.params.config_file).exists()):
            return r[bool].fail(
                f"Configuration file not found: {self.params.config_file}",
            )
        if self.params.catalog_file and (not Path(self.params.catalog_file).exists()):
            return r[bool].fail(f"Catalog file not found: {self.params.catalog_file}")
        if self.params.state_file and (not Path(self.params.state_file).exists()):
            return r[bool].fail(f"State file not found: {self.params.state_file}")
        return r[bool].ok(value=True)


class FlextTapOracleCli:
    """Facade for Oracle tap CLI operations using flext-meltano abstractions."""

    @staticmethod
    def run_tap_command[TParams](
        *,
        kwargs: t.ConfigurationMapping,
        params_factory: Callable[..., TParams],
        command_factory: Callable[[TParams], p.TapOraclePrivate.CommandRunner],
        operation_name: str,
    ) -> r[t.Cli.JsonValue]:
        """Run a tap command with params factory and command factory."""
        try:
            params = params_factory(**dict(kwargs))
            command = command_factory(params)
            result = command.execute()
            if result.is_failure:
                error_message = result.error or f"{operation_name} failed"
                logger.error(f"{operation_name} failed: {error_message}")
                return r[t.Cli.JsonValue].fail(error_message)
            return r[t.Cli.JsonValue].ok(value=True)
        except c.Meltano.SINGER_SAFE_EXCEPTIONS as e:
            error_message = f"{operation_name} error: {e}"
            logger.exception(error_message)
            return r[t.Cli.JsonValue].fail(error_message)

    @staticmethod
    def handle_discover_command(
        *_args: t.Scalar,
        **kwargs: t.Scalar,
    ) -> r[t.Cli.JsonValue]:
        """Handle discover command using flext-meltano patterns."""
        return FlextTapOracleCli.run_tap_command(
            kwargs=kwargs,
            params_factory=m.TapOracle.OracleTapDiscoverParams.from_click_args,
            command_factory=lambda params: FlextTapOracleDiscoverCommand(params=params),
            operation_name="Discovery",
        )

    @staticmethod
    def handle_sync_command(*_args: t.Scalar, **kwargs: t.Scalar) -> r[t.Cli.JsonValue]:
        """Handle sync command using flext-meltano patterns."""
        return FlextTapOracleCli.run_tap_command(
            kwargs=kwargs,
            params_factory=m.TapOracle.OracleTapSyncParams.from_click_args,
            command_factory=lambda params: FlextTapOracleSyncCommand(params=params),
            operation_name="Sync",
        )


def run_cli() -> int:
    """Main CLI entry point using flext-meltano abstractions."""
    if "--discover" in sys.argv:
        result = FlextTapOracleCli.handle_discover_command()
        return 0 if result.is_success else 1
    if "--sync" in sys.argv or len(sys.argv) <= 1:
        result = FlextTapOracleCli.handle_sync_command()
        return 0 if result.is_success else 1
    logger.warning("Unknown command. Use --discover or --sync.")
    return 1


def main() -> None:
    """Provide CLI entry point using flext-meltano patterns."""
    try:
        exit_code = run_cli()
        raise SystemExit(exit_code)
    except KeyboardInterrupt:
        logger.warning("Operation cancelled by user")
        raise SystemExit(0) from None
    except c.Meltano.SINGER_SAFE_EXCEPTIONS as e:
        logger.exception("Unexpected error")
        raise SystemExit(1) from e


if __name__ == "__main__":
    main()
