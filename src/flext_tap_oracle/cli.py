"""CLI entrypoint for flext-tap-oracle — canonical ``cli:main`` bridge.

Dispatches to the tap module's real Singer CLI runner so the declared console
script resolves and behaves as the running tap.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT

"""

from __future__ import annotations

from collections.abc import Sequence

from flext_tap_oracle.tap import FlextTapOracleCli


def main(args: Sequence[str] | None = None) -> int:
    """Run the canonical tap-oracle Singer CLI.

    Args:
        args: Command arguments, or ``None`` to read ``sys.argv[1:]``.

    Returns:
        The resulting ``int``.

    """
    exit_code: int = FlextTapOracleCli.run_cli(args)
    return exit_code


__all__: list[str] = ["main"]
