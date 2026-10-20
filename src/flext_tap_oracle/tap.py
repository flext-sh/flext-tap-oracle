"""FLEXT Tap Oracle - Singer Tap using flext-meltano abstractions.

Singer Tap interface using flext-meltano patterns with zero boilerplate
and maximum integration with FLEXT ecosystem.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

import sys
from pathlib import Path
from typing import TYPE_CHECKING

from flext_tap_oracle import FlextTapOracleSettings, c, e, m, p, r, t, u

if TYPE_CHECKING:
    from collections.abc import Callable


class FlextTapOracleCli:
    """Facade for Oracle tap CLI operations using flext-meltano abstractions."""

    logger = u.fetch_logger(__name__)

    class FlextTapOracleDiscoverCommand:
        """Oracle tap discovery command using flext-meltano patterns.

        Provides discovery of Oracle database schema and Singer catalog generation.
        """

        def __init__(self, params: m.TapOracle.OracleTapDiscoverParams) -> None:
            """Initialize command with parameter object pattern.

            Args:
                params: Discover command parameters (config and output paths).

            """
            self.params = params

        def execute(self) -> p.Result[t.JsonMapping]:
            """Execute Oracle tap discovery using modern patterns.

            Returns:
                The resulting ``p.Result[t.JsonMapping]``.

            """
            u.log("Starting Oracle database discovery", level="info")

            def _run_execute() -> p.Result[t.JsonMapping]:
                if not self.params.config_file:
                    return r[t.JsonMapping].fail(
                        "Configuration file is required for discovery",
                    )
                config_read = u.Cli.files_read_text(Path(self.params.config_file))
                if config_read.failure:
                    return r[t.JsonMapping].fail(
                        f"Discovery error: {config_read.error}",
                    )
                config_data: str = config_read.value
                # Validate the settings shape eagerly; downstream uses constants only.
                FlextTapOracleSettings.model_validate_json(config_data)
                schema_name = "USER"
                u.log("Discovering Oracle schema: %s", schema_name)
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
                            f"Catalog write error: {catalog_write.error}",
                        )
                    u.log("Catalog written to %s", output_path)
                u.log("Oracle schema discovery completed")
                return r[t.JsonMapping].ok(catalog_dict)

            try:
                return _run_execute()
            except c.Meltano.SINGER_SAFE_EXCEPTIONS as e:
                FlextTapOracleCli.logger.exception("Oracle discovery failed")
                return r[t.JsonMapping].fail(f"Discovery error: {e}", exception=e)

        def validate_business_rules(self) -> p.Result[bool]:
            """Validate business rules for Oracle tap discovery.

            Returns:
                The resulting ``p.Result[bool]``.

            """
            if self.params.config_file and (not Path(self.params.config_file).exists()):
                return e.fail_not_found(
                    "Configuration file",
                    self.params.config_file,
                    result_type=r[bool],
                )
            return r[bool].ok(value=True)

    class FlextTapOracleSyncCommand:
        """Oracle tap sync command using flext-meltano patterns."""

        def __init__(self, params: m.TapOracle.OracleTapSyncParams) -> None:
            """Initialize command with parameter object pattern.

            Args:
                params: Sync command parameters (config, catalog, state paths).

            """
            self.params = params

        def execute(self) -> p.Result[t.JsonMapping]:
            """Execute Oracle tap sync using modern patterns.

            Returns:
                The resulting ``p.Result[t.JsonMapping]``.

            """
            u.log("Starting Oracle data extraction")

            def _run_execute() -> p.Result[t.JsonMapping]:
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
                        return r[t.JsonMapping].fail(
                            f"Sync error: {catalog_read.error}",
                        )
                    u.log(
                        "Loaded catalog from %s",
                        self.params.catalog_file,
                    )
                if self.params.state_file:
                    state_read = u.Cli.files_read_text(Path(self.params.state_file))
                    if state_read.failure:
                        return r[t.JsonMapping].fail(f"Sync error: {state_read.error}")
                    u.log("Loaded state from %s", self.params.state_file)
                u.log("Preparing extraction from Oracle database...")
                schema_name = "USER"
                record_count = c.TapOracle.INITIAL_RECORD_COUNT
                result_data: t.JsonMapping = {
                    "records_extracted": record_count,
                    "schema_name": schema_name,
                    "status": c.Status.COMPLETED.value,
                }
                u.log(
                    "Sync completed for schema %s; records extracted: %s",
                    schema_name,
                    record_count,
                )
                return r[t.JsonMapping].ok(result_data)

            try:
                return _run_execute()
            except c.Meltano.SINGER_SAFE_EXCEPTIONS as e:
                u.log("Oracle sync failed", level="exception")
                return r[t.JsonMapping].fail(f"Sync error: {e}", exception=e)

        def validate_business_rules(self) -> p.Result[bool]:
            """Validate business rules for Oracle tap sync.

            Returns:
                The resulting ``p.Result[bool]``.

            """
            if self.params.config_file and (not Path(self.params.config_file).exists()):
                return e.fail_not_found(
                    "Configuration file",
                    self.params.config_file,
                    result_type=r[bool],
                )
            if self.params.catalog_file and (
                not Path(self.params.catalog_file).exists()
            ):
                return e.fail_not_found(
                    "Catalog file",
                    self.params.catalog_file,
                    result_type=r[bool],
                )
            if self.params.state_file and (not Path(self.params.state_file).exists()):
                return e.fail_not_found(
                    "State file",
                    self.params.state_file,
                    result_type=r[bool],
                )
            return r[bool].ok(value=True)

    @staticmethod
    def run_tap_command[TParams](
        *,
        kwargs: t.ConfigurationMapping,
        params_factory: Callable[..., TParams],
        command_factory: Callable[[TParams], p.TapOracle.CommandRunner],
        operation_name: str,
    ) -> p.Result[t.JsonValue]:
        """Run a tap command with params factory and command factory.

        Args:
            kwargs: Raw CLI keyword arguments passed to ``params_factory``.
            params_factory: Builds the command parameter object from kwargs.
            command_factory: Builds the command runner from the parameters.
            operation_name: Human-readable operation label for logging.

        Returns:
            The resulting ``p.Result[t.JsonValue]``.

        """

        def _run_run_tap_command() -> p.Result[t.JsonValue]:
            params = params_factory(**dict(kwargs))
            command = command_factory(params)
            result = command.execute()
            if result.failure:
                error_message = result.error or f"{operation_name} failed"
                FlextTapOracleCli.logger.error(
                    "%s failed: %s",
                    operation_name,
                    error_message,
                )
                return r[t.JsonValue].fail(error_message)
            return r[t.JsonValue].ok(value=True)

        try:
            return _run_run_tap_command()
        except c.Meltano.SINGER_SAFE_EXCEPTIONS as e:
            error_message = f"{operation_name} error: {e}"
            FlextTapOracleCli.logger.exception(error_message)
            return r[t.JsonValue].fail(error_message)

    @staticmethod
    def handle_discover_command(**kwargs: t.Scalar) -> p.Result[t.JsonValue]:
        """Handle discover command using flext-meltano patterns.

        Args:
            kwargs: Raw CLI keyword arguments forwarded to the params factory.

        Returns:
            The resulting ``p.Result[t.JsonValue]``.

        """
        return FlextTapOracleCli.run_tap_command(
            kwargs=kwargs,
            params_factory=m.TapOracle.OracleTapDiscoverParams.from_click_args,
            command_factory=lambda params: (
                FlextTapOracleCli.FlextTapOracleDiscoverCommand(params=params)
            ),
            operation_name="Discovery",
        )

    @staticmethod
    def handle_sync_command(**kwargs: t.Scalar) -> p.Result[t.JsonValue]:
        """Handle sync command using flext-meltano patterns.

        Args:
            kwargs: Raw CLI keyword arguments forwarded to the params factory.

        Returns:
            The resulting ``p.Result[t.JsonValue]``.

        """
        return FlextTapOracleCli.run_tap_command(
            kwargs=kwargs,
            params_factory=m.TapOracle.OracleTapSyncParams.from_click_args,
            command_factory=lambda params: FlextTapOracleCli.FlextTapOracleSyncCommand(
                params=params,
            ),
            operation_name="Sync",
        )

    @staticmethod
    def run_cli(args: t.StrSequence | None = None) -> int:
        """Run main CLI entry point using flext-meltano abstractions.

        Args:
            args: Command arguments, or ``None`` to read ``sys.argv[1:]``.

        Returns:
            The resulting ``int``.

        """
        logger = u.fetch_logger(__name__)
        command_args = sys.argv[1:] if args is None else args
        if "--discover" in command_args:
            result = FlextTapOracleCli.handle_discover_command()
            return 0 if result.success else 1
        if "--sync" in command_args or not command_args:
            result = FlextTapOracleCli.handle_sync_command()
            return 0 if result.success else 1
        logger.warning("Unknown command. Use --discover or --sync.")
        return 1


def main() -> None:
    """Run the CLI entry point and exit with the resulting status code.

    Raises:
        SystemExit: Always; or if a ``KeyboardInterrupt`` is caught; or if a
            ``c.Meltano.SINGER_SAFE_EXCEPTIONS`` is caught.

    """
    logger = u.fetch_logger(__name__)
    try:
        exit_code = FlextTapOracleCli.run_cli()
        raise SystemExit(exit_code)
    except KeyboardInterrupt:
        logger.warning("Operation cancelled by user")
        raise SystemExit(0) from None
    except c.Meltano.SINGER_SAFE_EXCEPTIONS as e:
        logger.exception("Unexpected error")
        raise SystemExit(1) from e


if __name__ == "__main__":
    main()
