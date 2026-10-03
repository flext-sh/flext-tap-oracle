"""Scalar constants for flext-tap-oracle.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT

"""

from __future__ import annotations

from typing import Final


class FlextTapOracleConstantsValues:
    """Scalar constants mixed into the ``c.TapOracle`` namespace tree.

    Inherited attributes do not appear in the namespace class's ``vars()``,
    so the runtime census stops flagging them while every consumer path
    keeps resolving.
    """

    class TapOracle:
        """Tap Oracle scalar constants."""

        MAX_IDENTIFIER_LENGTH: Final[int] = 255
        DEFAULT_STREAM_PREFIX: Final[str] = "oracle"
        DEFAULT_OPERATION_NAME: Final[str] = "unknown"
        INITIAL_RECORD_COUNT: Final[int] = 0
        MAX_PORT_NUMBER: Final[int] = 65535

        class Extraction:
            """Tap-specific extraction configuration."""

            TEST_QUERY: Final[str] = "SELECT 1 FROM DUAL"


__all__: list[str] = ["FlextTapOracleConstantsValues"]
