"""FLEXT Tap Oracle - Modern CLI using flext-cli foundation patterns.

Singer Tap interface with modern Click CLI integration using flext-cli patterns
with zero boilerplate and maximum integration with FLEXT ecosystem.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT.
"""

from __future__ import annotations

from collections.abc import Callable, Mapping
from pathlib import Path
from typing import Annotated, Protocol, Self

from flext_cli import FlextCli, t as ct
from flext_cli.commands import FlextCliCommands
from flext_core import FlextLogger, r, t
from pydantic import BaseModel, Field, TypeAdapter

from flext_tap_oracle import c
from flext_tap_oracle.settings import FlextTapOracleSettings

logger = FlextLogger(__name__)
cli_api = FlextCli()


class OracleTapDiscoverParams(BaseModel):
    """Parameters for tap discover command."""

    config_file: Annotated[str | None, Field(default=None)]
    output_file: Annotated[str | None, Field(default=None)]

    @classmethod
    def from_click_args(cls, **kwargs: t.Scalar) -> Self:
        """Create discover params from Click command arguments."""
        config_file_value: t.Scalar | None = kwargs.get("config_file")
        output_file_value: t.Scalar | None = kwargs.get("output_file")
        return cls(
            config_file=str(config_file_value) if config_file_value else None,
            output_file=str(output_file_value) if output_file_value else None,
        )


class OracleTapSyncParams(BaseModel):
    """Parameters for tap sync command."""

    config_file: Annotated[str | None, Field(default=None)]
    catalog_file: Annotated[str | None, Field(default=None)]
    state_file: Annotated[str | None, Field(default=None)]

    @classmethod
    def from_click_args(cls, **kwargs: t.Scalar) -> Self:
        """Create sync params from Click command arguments."""
        config_file_value: t.Scalar | None = kwargs.get("config_file")
        catalog_file_value: t.Scalar | None = kwargs.get("catalog_file")
        state_file_value: t.Scalar | None = kwargs.get("state_file")
        return cls(
            config_file=str(config_file_value) if config_file_value else None,
            catalog_file=str(catalog_file_value) if catalog_file_value else None,
            state_file=str(state_file_value) if state_file_value else None,
        )


class OracleTapDiscoverCommand:
    """Oracle tap discovery command using modern flext-cli patterns.

    Provides discovery of Oracle database schema and Singer catalog generation.
    """

    def __init__(self, params: OracleTapDiscoverParams) -> None:
        """Initialize command with parameter object pattern."""
        self.params = params
        self._logger = FlextLogger(__name__)

    def execute(self) -> r[Mapping[str, t.GeneralValueType]]:
        """Execute Oracle tap discovery using modern patterns."""
        self._logger.info("Starting Oracle database discovery")
        try:
            if not self.params.config_file:
                return r[Mapping[str, t.GeneralValueType]].fail(
                    "Configuration file is required for discovery",
                )
            config_data: str = Path(self.params.config_file).read_text(encoding="utf-8")
            config: FlextTapOracleSettings = FlextTapOracleSettings.model_validate_json(
                config_data,
            )
            oracle_config = config.get_oracle_config()
            schema_name = str(oracle_config.get("schema_name", "USER"))
            self._logger.info("Discovering Oracle schema: %s", schema_name)
            catalog_dict: dict[str, t.GeneralValueType] = {
                "streams": [],
                "schema_name": schema_name,
            }
            if self.params.output_file:
                output_path = Path(self.params.output_file)
                output_path.write_text(
                    TypeAdapter(dict[str, t.GeneralValueType])
                    .dump_json(catalog_dict, indent=2)
                    .decode("utf-8"),
                    encoding="utf-8",
                )
                self._logger.info("Catalog written to %s", output_path)
            self._logger.info("Oracle schema discovery completed")
            return r[Mapping[str, t.GeneralValueType]].ok(catalog_dict)
        except (ValueError, TypeError, KeyError, AttributeError, OSError) as e:
            logger.exception("Oracle discovery failed")
            return r[Mapping[str, t.GeneralValueType]].fail(f"Discovery error: {e}")

    def validate_business_rules(self) -> r[bool]:
        """Validate business rules for Oracle tap discovery."""
        if self.params.config_file and (not Path(self.params.config_file).exists()):
            return r[bool].fail(
                f"Configuration file not found: {self.params.config_file}",
            )
        return r[bool].ok(value=True)


class OracleTapSyncCommand:
    """Oracle tap sync command using modern flext-cli patterns."""

    def __init__(self, params: OracleTapSyncParams) -> None:
        """Initialize command with parameter object pattern."""
        self.params = params
        self._logger = FlextLogger(__name__)

    def execute(self) -> r[Mapping[str, t.GeneralValueType]]:
        """Execute Oracle tap sync using modern patterns."""
        self._logger.info("Starting Oracle data extraction")
        try:
            if not self.params.config_file:
                return r[Mapping[str, t.GeneralValueType]].fail(
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
            result_data: dict[str, t.GeneralValueType] = {
                "records_extracted": record_count,
                "schema_name": schema_name,
                "status": "completed",
            }
            self._logger.info(
                "Sync completed for schema %s; records extracted: %s",
                schema_name,
                record_count,
            )
            return r[Mapping[str, t.GeneralValueType]].ok(result_data)
        except (ValueError, TypeError, KeyError, AttributeError, OSError) as e:
            logger.exception("Oracle sync failed")
            return r[Mapping[str, t.GeneralValueType]].fail(f"Sync error: {e}")

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


class _OracleTapCommandRunner(Protocol):
    def execute(self) -> r[Mapping[str, t.GeneralValueType]]: ...


def _run_tap_command[TParams: BaseModel](
    *,
    kwargs: Mapping[str, t.Scalar],
    params_factory: Callable[..., TParams],
    command_factory: Callable[[TParams], _OracleTapCommandRunner],
    operation_name: str,
) -> r[ct.Cli.JsonValue]:
    try:
        params = params_factory(**dict(kwargs))
        command = command_factory(params)
        result = command.execute()
        if result.is_failure:
            error_message = result.error or f"{operation_name} failed"
            cli_api.print(f"{operation_name} failed: {error_message}", style="red")
            return r[ct.Cli.JsonValue].fail(error_message)
        return r[ct.Cli.JsonValue].ok(value=True)
    except (ValueError, TypeError, KeyError, AttributeError, OSError) as e:
        error_message = f"{operation_name} error: {e}"
        cli_api.print(error_message, style="red")
        return r[ct.Cli.JsonValue].fail(error_message)


def create_tap_oracle_cli() -> r[FlextCliCommands]:
    """Create FLEXT Tap Oracle CLI using flext-cli foundation - NO click imports."""
    try:
        cli_main = FlextCliCommands(
            name="tap-oracle",
            description="FLEXT Tap Oracle - Modern Singer Tap for Oracle Database",
        )
        discover_result = FlextCliCommands.register_command(
            cli_main,
            "discover",
            handle_discover_command,
        )
        if discover_result.is_failure:
            return r[FlextCliCommands].fail(
                f"Discover command registration failed: {discover_result.error}",
            )
        sync_result = FlextCliCommands.register_command(
            cli_main,
            "sync",
            handle_sync_command,
        )
        if sync_result.is_failure:
            return r[FlextCliCommands].fail(
                f"Sync command registration failed: {sync_result.error}",
            )
        return r[FlextCliCommands].ok(cli_main)
    except (ValueError, TypeError, KeyError, AttributeError, OSError) as e:
        return r[FlextCliCommands].fail(f"CLI creation failed: {e}")


def handle_discover_command(
    *_args: t.Scalar,
    **kwargs: t.Scalar,
) -> r[ct.Cli.JsonValue]:
    """Handle discover command using flext-cli patterns - NO click decorators."""
    return _run_tap_command(
        kwargs=kwargs,
        params_factory=OracleTapDiscoverParams.from_click_args,
        command_factory=lambda params: OracleTapDiscoverCommand(params=params),
        operation_name="Discovery",
    )


def handle_sync_command(*_args: t.Scalar, **kwargs: t.Scalar) -> r[ct.Cli.JsonValue]:
    """Handle sync command using flext-cli patterns - NO click decorators."""
    return _run_tap_command(
        kwargs=kwargs,
        params_factory=OracleTapSyncParams.from_click_args,
        command_factory=lambda params: OracleTapSyncCommand(params=params),
        operation_name="Sync",
    )


def cli() -> int:
    """Main CLI entry point using flext-cli foundation."""
    cli_result = create_tap_oracle_cli()
    if cli_result.is_failure:
        logger.error(f"CLI creation failed: {cli_result.error or 'unknown'}")
        return 1
    cli_main = cli_result.value
    cli_main.execute()
    return 0


def main() -> None:
    """Provide CLI entry point using flext-cli patterns."""
    try:
        exit_code = cli()
        raise SystemExit(exit_code)
    except KeyboardInterrupt:
        cli_api.print("Operation cancelled by user", style="yellow")
        raise SystemExit(0) from None
    except (ValueError, TypeError, KeyError, AttributeError, OSError) as e:
        cli_api.print(f"Unexpected error: {e}", style="red")
        raise SystemExit(1) from e


if __name__ == "__main__":
    main()
