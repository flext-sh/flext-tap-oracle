# AUTO-GENERATED FILE — Regenerate with: make gen
"""Package version and metadata for flext-tap-oracle.

Subclass of ``FlextVersion`` — overrides only ``_metadata``.
All derived attributes (``__version__``, ``__title__``, etc.) are
computed automatically via ``FlextVersion.__init_subclass__``.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from importlib.metadata import PackageMetadata, metadata

from flext_core.__version__ import FlextVersion


class FlextTapOracleVersion(FlextVersion):
    """flext-tap-oracle version — MRO-derived from FlextVersion."""

    _metadata: PackageMetadata = metadata("flext-tap-oracle")


__version__ = FlextTapOracleVersion.__version__
__version_info__ = FlextTapOracleVersion.__version_info__
__title__ = FlextTapOracleVersion.__title__
__description__ = FlextTapOracleVersion.__description__
__author__ = FlextTapOracleVersion.__author__
__author_email__ = FlextTapOracleVersion.__author_email__
__license__ = FlextTapOracleVersion.__license__
__url__ = FlextTapOracleVersion.__url__
__all__: list[str] = [
    "FlextTapOracleVersion",
    "__author__",
    "__author_email__",
    "__description__",
    "__license__",
    "__title__",
    "__url__",
    "__version__",
    "__version_info__",
]
