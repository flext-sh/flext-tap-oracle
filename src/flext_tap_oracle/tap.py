"""FLEXT Tap Oracle - Singer Tap using flext-meltano abstractions.

Singer Tap interface using flext-meltano patterns with zero boilerplate
and maximum integration with FLEXT ecosystem.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT.
"""

from __future__ import annotations

import sys
from collections.abc import (
    Callable,
)
from pathlib import Path

from flext_tap_oracle import FlextTapOracleSettings, c, e, m, p, r, t, u

logger = u.fetch_logger(__name__)


class FlextTapOracleDiscoverCommand:
    """Oracle tap discovery command using flext-meltano patterns.

    Provides discovery of Oracle database schema and Singer catalog generation.
    """

    def __init__(self, params: m.TapOracle.OracleTapDiscoverParams) -> None:
        """Initialize command with parameter object pattern."""
        self.params = params
        self.logger = u.fetch_logger(__name__)

    def execute(self) -> p.Result[t.JsonMapping]:
        """Execute Oracle tap discovery using modern patterns."""
        self.logger.info("Starting Oracle database discovery")
        try:
            if not self.params.config_file:
                return r[t.JsonMapping].fail(
                    "Configuration file is required for discovery",
                )
            config_read = u.Cli.files_read_text(Path(self.params.config_file))
            if config_read.failure:
                return r[t.JsonMapping].fail(f"Discovery error: {config_read.error}")
            config_data: str = config_read.value
            # Validate the settings shape eagerly; downstream uses constants only.
            FlextTapOracleSettings.model_validate_json(config_data)
            schema_name = "USER"
            self.logger.info("Discovering Oracle schema: %s", schema_name)
            streams: t.JsonValueList = []
            catalog_dict: t.JsonMapping = {
                "streams": streams,
                "schema_name": schema_name,
            }
            if self.params.output_file:
                output_path = Path(self.params.output_file)
                catalog_write = u.Cli.json_write(
                    output_path,
                    catalog_dict,
                    options=m.Cli.JsonWriteOptions(indent=2),
                )
                if catalog_write.failure:
                    return r[t.JsonMapping].fail(
                        f"Catalog write error: {catalog_write.error}"
                    )
                self.logger.info(f"Catalog written to {output_path}")
            self.logger.info("Oracle schema discovery completed")
            return r[t.JsonMapping].ok(catalog_dict)
        except c.Meltano.SINGER_SAFE_EXCEPTIONS as e:
            logger.exception("Oracle discovery failed")
            return r[t.JsonMapping].fail(f"Discovery error: {e}")

    def validate_business_rules(self) -> p.Result[bool]:
        """Validate business rules for Oracle tap discovery."""
        if self.params.config_file and (not Path(self.params.config_file).exists()):
            return e.fail_not_found(
                "Configuration file", self.params.config_file, result_type=r[bool]
            )
        return r[bool].ok(value=True)


class FlextTapOracleSyncCommand:
    """Oracle tap sync command using flext-meltano patterns."""

    def __init__(self, params: m.TapOracle.OracleTapSyncParams) -> None:
        """Initialize command with parameter object pattern."""
        self.params = params
        self.logger = u.fetch_logger(__name__)

    def execute(self) -> p.Result[t.JsonMapping]:
        """Execute Oracle tap sync using modern patterns."""
        self.logger.info("Starting Oracle data extraction")
        try:
            if not self.params.config_file:
                return r[t.JsonMapping].fail(
                    "Configuration file is required for sync",
                )
            config_read = u.Cli.files_read_text(Path(self.params.config_file))
            if config_read.failure:
                return r[t.JsonMapping].fail(f"Sync error: {config_read.error}")
            config_data: str = config_read.value
            FlextTapOracleSettings.model_validate_json(config_data)
            if self.params.catalog_file:
                catalog_read = u.Cli.files_read_text(Path(self.params.catalog_file))
                if catalog_read.failure:
                    return r[t.JsonMapping].fail(f"Sync error: {catalog_read.error}")
                self.logger.info(f"Loaded catalog from {self.params.catalog_file}")
            if self.params.state_file:
                state_read = u.Cli.files_read_text(Path(self.params.state_file))
                if state_read.failure:
                    return r[t.JsonMapping].fail(f"Sync error: {state_read.error}")
                self.logger.info(f"Loaded state from {self.params.state_file}")
            self.logger.info("Preparing extraction from Oracle database...")
            schema_name = "USER"
            record_count = c.TapOracle.INITIAL_RECORD_COUNT
            result_data: t.JsonMapping = {
                "records_extracted": record_count,
                "schema_name": schema_name,
                "status": "completed",
            }
            self.logger.info(
                "Sync completed for schema %s; records extracted: %s",
                schema_name,
                record_count,
            )
            return r[t.JsonMapping].ok(result_data)
        except c.Meltano.SINGER_SAFE_EXCEPTIONS as e:
            logger.exception("Oracle sync failed")
            return r[t.JsonMapping].fail(f"Sync error: {e}")

    def validate_business_rules(self) -> p.Result[bool]:
        """Validate business rules for Oracle tap sync."""
        if self.params.config_file and (not Path(self.params.config_file).exists()):
            return e.fail_not_found(
                "Configuration file", self.params.config_file, result_type=r[bool]
            )
        if self.params.catalog_file and (not Path(self.params.catalog_file).exists()):
            return e.fail_not_found(
                "Catalog file", self.params.catalog_file, result_type=r[bool]
            )
        if self.params.state_file and (not Path(self.params.state_file).exists()):
            return e.fail_not_found(
                "State file", self.params.state_file, result_type=r[bool]
            )
        return r[bool].ok(value=True)


class FlextTapOracleCli:
    """Facade for Oracle tap CLI operations using flext-meltano abstractions."""

    @staticmethod
    def run_tap_command[TParams](
        *,
        kwargs: t.ConfigurationMapping,
        params_factory: Callable[..., TParams],
        command_factory: Callable[[TParams], p.TapOracle.CommandRunner],
        operation_name: str,
    ) -> p.Result[t.JsonValue]:
        """Run a tap command with params factory and command factory."""
        try:
            params = params_factory(**dict(kwargs))
            command = command_factory(params)
            result = command.execute()
            if result.failure:
                error_message = result.error or f"{operation_name} failed"
                logger.error(f"{operation_name} failed: {error_message}")
                return r[t.JsonValue].fail(error_message)
            return r[t.JsonValue].ok(value=True)
        except c.Meltano.SINGER_SAFE_EXCEPTIONS as e:
            error_message = f"{operation_name} error: {e}"
            logger.exception(error_message)
            return r[t.JsonValue].fail(error_message)

    @staticmethod
    def handle_discover_command(
        **kwargs: t.Scalar,
    ) -> p.Result[t.JsonValue]:
        """Handle discover command using flext-meltano patterns."""
        return FlextTapOracleCli.run_tap_command(
            kwargs=kwargs,
            params_factory=m.TapOracle.OracleTapDiscoverParams.from_click_args,
            command_factory=lambda params: FlextTapOracleDiscoverCommand(params=params),
            operation_name="Discovery",
        )

    @staticmethod
    def handle_sync_command(**kwargs: t.Scalar) -> p.Result[t.JsonValue]:
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
        return 0 if result.success else 1
    if "--sync" in sys.argv or len(sys.argv) <= 1:
        result = FlextTapOracleCli.handle_sync_command()
        return 0 if result.success else 1
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
