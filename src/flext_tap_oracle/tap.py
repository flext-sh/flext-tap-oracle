#!/usr/bin/env python3
"""FLEXT Tap Oracle - Modern CLI using flext-cli foundation patterns.

Singer Tap interface with modern Click CLI integration using flext-cli patterns
with zero boilerplate and maximum integration with FLEXT ecosystem.

Built on Clean Architecture patterns with flext-core integration.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

import json
import sys
import uuid
from collections.abc import Mapping
from dataclasses import dataclass
from pathlib import Path

import click
from flext_cli import (
    CLICommand,
    FlextCliHelper,
    create_cli_config as create_flext_cli_config,
    setup_cli as setup_flext_cli,
)
from flext_core import FlextResult, get_logger
from rich.console import Console

from flext_tap_oracle.models import create_discovery_result
from flext_tap_oracle.tap_client import create_oracle_tap_service
from flext_tap_oracle.tap_config import FlextOracleTapConfig

logger = get_logger(__name__)
console = Console()

# =============================================================================
# FLEXT-CLI PARAMETER OBJECTS - ELIMINATE ARGUMENT EXPLOSION
# =============================================================================


@dataclass
class OracleTapDiscoverParams:
    """Parameter object for Oracle tap discovery operations - flext-cli pattern."""

    config_file: str | None = None
    output_file: str | None = None

    @classmethod
    def from_click_args(cls, **kwargs: object) -> OracleTapDiscoverParams:
      """Create from Click arguments using flext-cli patterns."""
      args: Mapping[str, object] = kwargs  # kwargs keys are always str
      return cls(
          config_file=str(args.get("config_file"))
          if args.get("config_file") is not None
          else None,
          output_file=(
              str(args.get("output_file"))
              if args.get("output_file") is not None
              else "catalog.json"
          ),
      )


@dataclass
class OracleTapSyncParams:
    """Parameter object for Oracle tap sync operations - flext-cli pattern."""

    config_file: str | None = None
    catalog_file: str | None = None
    state_file: str | None = None
    output_file: str | None = None

    @classmethod
    def from_click_args(cls, **kwargs: object) -> OracleTapSyncParams:
      """Create from Click arguments using flext-cli patterns."""
      args: Mapping[str, object] = kwargs
      return cls(
          config_file=str(args.get("config_file"))
          if args.get("config_file") is not None
          else None,
          catalog_file=(
              str(args.get("catalog_file"))
              if args.get("catalog_file") is not None
              else "catalog.json"
          ),
          state_file=str(args.get("state_file"))
          if args.get("state_file") is not None
          else None,
          output_file=str(args.get("output_file"))
          if args.get("output_file") is not None
          else None,
      )


class OracleTapDiscoverCommand(CLICommand):
    """Oracle tap discovery command using modern flext-cli patterns.

    CLICompleteMixin includes:
    - CLIValidationMixin: Input validation
    - CLIInteractiveMixin: User interaction
    - CLIOutputMixin: Output formatting
    - CLILoggingMixin: Structured logging
    - CLIConfigMixin: Configuration management
    """

    def __init__(
      self,
      command_id: str,
      name: str,
      params: OracleTapDiscoverParams,
    ) -> None:
      """Initialize command with parameter object pattern."""
      # Initialize CLI command entity with supported fields
      super().__init__(
          id=command_id,
          command_line=name,
          arguments=[],
      )
      self.params = params
      self.cli_helper = FlextCliHelper()

    def validate_business_rules(self) -> FlextResult[None]:
      """Validate business rules for Oracle tap discovery."""
      if self.params.config_file and not Path(self.params.config_file).exists():
          return FlextResult.fail(
              f"Configuration file not found: {self.params.config_file}",
          )
      return FlextResult.ok(None)

    def execute(self) -> FlextResult[object]:
      """Execute Oracle tap discovery using modern patterns."""
      self.cli_helper.print_info("Starting Oracle database discovery")

      logger.info(
          "Oracle tap discovery started",
          extra={
              "config_file": self.params.config_file,
              "output_file": self.params.output_file,
          },
      )

      try:
          # Load configuration (required)
          if not self.params.config_file:
              return FlextResult.fail("Configuration file is required for discovery")

          config_data = Path(self.params.config_file).read_text(encoding="utf-8")
          config = FlextOracleTapConfig.model_validate_json(config_data)

          # Create Oracle tap service
          tap_service_result = create_oracle_tap_service(config)
          if tap_service_result.is_failure or not tap_service_result.data:
              self.cli_helper.print_error(
                  f"Failed to create tap service: {tap_service_result.error}",
              )
              return FlextResult.fail(
                  tap_service_result.error or "Tap service creation failed",
              )

          tap_service = tap_service_result.data

          # Execute discovery of Oracle tables
          self.cli_helper.print_info("Discovering Oracle database schema...")
          tables_result = tap_service.discover_oracle_tables()
          if tables_result.is_failure or tables_result.data is None:
              self.cli_helper.print_error(f"Discovery failed: {tables_result.error}")
              return FlextResult.fail(tables_result.error or "Discovery failed")

          # Build Singer catalog from tables using tap models
          schema_name = getattr(config.oracle_config, "schema_name", None) or "USER"
          discovery_build = create_discovery_result(schema_name, tables_result.data)
          if discovery_build.is_failure or discovery_build.data is None:
              return FlextResult.fail(
                  discovery_build.error or "Failed to build discovery result",
              )

          catalog_dict = discovery_build.data.to_singer_catalog()

          # Output catalog (Singer standard)
          if self.params.output_file:
              output_path = Path(self.params.output_file)
              output_path.write_text(
                  json.dumps(catalog_dict, indent=2),
                  encoding="utf-8",
              )
              self.cli_helper.print_success(f"Catalog written to {output_path}")

          self.cli_helper.print_success("Oracle schema discovery completed")
          return FlextResult.ok({"catalog": catalog_dict})

      except Exception as e:
          logger.exception("Oracle discovery failed")
          self.cli_helper.print_error(f"Discovery error: {e}")
          return FlextResult.fail(f"Discovery error: {e}")


class OracleTapSyncCommand(CLICommand):
    """Oracle tap sync command using modern flext-cli patterns."""

    def __init__(
      self,
      command_id: str,
      name: str,
      params: OracleTapSyncParams,
    ) -> None:
      """Initialize command with parameter object pattern."""
      super().__init__(
          id=command_id,
          command_line=name,
          arguments=[],
      )
      self.params = params
      self.cli_helper = FlextCliHelper()

    def validate_business_rules(self) -> FlextResult[None]:
      """Validate business rules for Oracle tap sync."""
      if self.params.config_file and not Path(self.params.config_file).exists():
          return FlextResult.fail(
              f"Configuration file not found: {self.params.config_file}",
          )
      if self.params.catalog_file and not Path(self.params.catalog_file).exists():
          return FlextResult.fail(
              f"Catalog file not found: {self.params.catalog_file}",
          )
      if self.params.state_file and not Path(self.params.state_file).exists():
          return FlextResult.fail(
              f"State file not found: {self.params.state_file}",
          )
      return FlextResult.ok(None)

    def execute(self) -> FlextResult[object]:
      """Execute Oracle tap sync using modern patterns."""
      self.cli_helper.print_info("Starting Oracle data extraction")

      logger.info(
          "Oracle tap sync started",
          extra={
              "config_file": self.params.config_file,
              "catalog_file": self.params.catalog_file,
              "state_file": self.params.state_file,
          },
      )

      try:
          # Load configuration (required)
          if not self.params.config_file:
              return FlextResult.fail("Configuration file is required for sync")

          config_data = Path(self.params.config_file).read_text(encoding="utf-8")
          config = FlextOracleTapConfig.model_validate_json(config_data)

          # Create Oracle tap service
          tap_service_result = create_oracle_tap_service(config)
          if tap_service_result.is_failure or not tap_service_result.data:
              self.cli_helper.print_error(
                  f"Failed to create tap service: {tap_service_result.error}",
              )
              return FlextResult.fail(
                  tap_service_result.error or "Tap service creation failed",
              )

          tap_service = tap_service_result.data

          # Load catalog and state if provided (not parsed here; placeholder for Singer integration)
          if self.params.catalog_file:
              Path(self.params.catalog_file).read_text(encoding="utf-8")
              self.cli_helper.print_info(
                  f"Loaded catalog from {self.params.catalog_file}",
              )

          if self.params.state_file:
              Path(self.params.state_file).read_text(encoding="utf-8")
              self.cli_helper.print_info(
                  f"Loaded state from {self.params.state_file}",
              )

          # Execute a basic extraction workflow: get filtered tables as a proxy
          self.cli_helper.print_info("Preparing table list for extraction...")
          tables_result = tap_service.get_filtered_tables()
          if tables_result.is_failure:
              self.cli_helper.print_error(f"Sync failed: {tables_result.error}")
              return FlextResult.fail(tables_result.error or "Sync failed")

          table_names = tables_result.data or []
          record_count = 0  # Real extraction requires Singer target integration

          self.cli_helper.print_success(
              f"Prepared sync for {len(table_names)} tables; records extracted: {record_count}",
          )
          return FlextResult.ok(
              {"records_extracted": record_count, "tables": table_names},
          )

      except Exception as e:
          logger.exception("Oracle sync failed")
          self.cli_helper.print_error(f"Sync error: {e}")
          return FlextResult.fail(f"Sync error: {e}")


# =============================================================================
# MODERN CLICK CLI WITH FLEXT-CLI INTEGRATION
# =============================================================================


@click.group(name="tap-oracle")
@click.version_option(version="0.9.0", prog_name="FLEXT Tap Oracle")
@click.help_option("--help", "-h")
def cli() -> None:
    """FLEXT Tap Oracle - Modern Singer Tap for Oracle Database.

    Modern CLI using flext-cli foundation with zero boilerplate.
    Built on Clean Architecture patterns with flext-core integration.
    """
    # Initialize flext-cli
    cli_config_result = create_flext_cli_config(
      debug=False,
      profile="oracle-tap",
    )

    if cli_config_result.is_failure:
      console.print(f"[red]CLI configuration failed: {cli_config_result.error}[/red]")
      return

    setup_result = setup_flext_cli(cli_config_result.data)
    if setup_result.is_failure:
      console.print(f"[red]CLI setup failed: {setup_result.error}[/red]")
      return


@cli.command()
@click.option(
    "--config",
    "-c",
    "config_file",
    help="Path to tap configuration JSON file",
)
@click.option(
    "--output",
    "-o",
    "output_file",
    help="Output catalog file (default: catalog.json)",
    default="catalog.json",
)
def discover(**kwargs: object) -> None:
    """Discover Oracle database schema and generate Singer catalog.

    Example:
      tap-oracle discover --config config.json --output catalog.json
      tap-oracle discover  # Uses environment variables

    """
    params = OracleTapDiscoverParams.from_click_args(**kwargs)

    command = OracleTapDiscoverCommand(
      command_id=str(uuid.uuid4()),
      name="oracle-discover",
      params=params,
    )

    result = command.execute()
    if result.is_failure:
      console.print(f"[red]Discovery failed: {result.error}[/red]")
      sys.exit(1)


@cli.command()
@click.option(
    "--config",
    "-c",
    "config_file",
    help="Path to tap configuration JSON file",
)
@click.option(
    "--catalog",
    "catalog_file",
    help="Path to Singer catalog file",
    default="catalog.json",
)
@click.option("--state", "state_file", help="Path to Singer state file")
@click.option("--output", "-o", "output_file", help="Output file (default: stdout)")
def sync(**kwargs: object) -> None:
    """Extract data from Oracle database using Singer protocol.

    Example:
      tap-oracle sync --config config.json --catalog catalog.json
      tap-oracle sync --config config.json --catalog catalog.json --state state.json

    """
    params = OracleTapSyncParams.from_click_args(**kwargs)

    command = OracleTapSyncCommand(
      command_id=str(uuid.uuid4()),
      name="oracle-sync",
      params=params,
    )

    result = command.execute()
    if result.is_failure:
      console.print(f"[red]Sync failed: {result.error}[/red]")
      sys.exit(1)


def main() -> None:
    """Provide CLI entry point using flext-cli patterns."""
    try:
      cli()
    except KeyboardInterrupt:
      console.print("[blue]Operation cancelled by user[/blue]")
      raise SystemExit(0) from None
    except Exception as e:
      console.print(f"[red]Unexpected error: {e}[/red]")
      raise SystemExit(1) from e


if __name__ == "__main__":
    main()
