"""CLI entrypoint for flext-tap-oracle — canonical ``cli:main`` bridge.

Dispatches to the tap module's real Singer CLI runner so the declared console
script resolves and behaves as the running tap.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT

"""

from __future__ import annotations

from typing import TYPE_CHECKING

from flext_tap_oracle.tap import FlextTapOracleCli

if TYPE_CHECKING:
    from flext_tap_oracle import t


def main(args: t.StrSequence | None = None) -> int:
    """Run the canonical tap-oracle Singer CLI.

    Args:
        args: Accepted for the canonical bridge signature; ignored — the
            underlying runner dispatches on ``sys.argv``.

    Returns:
        The resulting ``int``.

    """
    _ = args
    exit_code: int = FlextTapOracleCli.run_cli()
    return exit_code


__all__: list[str] = ["main"]
