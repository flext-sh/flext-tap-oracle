"""CLI entrypoint for flext-tap-oracle — canonical ``cli:main`` bridge.

Dispatches to the tap module's real Singer CLI runner so the declared console
script resolves and behaves as the running tap.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from flext_tap_oracle import t
from flext_tap_oracle.tap import run_cli


def main(args: t.StrSequence | None = None) -> int:
    """Run the canonical tap-oracle Singer CLI."""
    _ = args
    exit_code: int = run_cli()
    return exit_code


__all__: list[str] = ["main"]
