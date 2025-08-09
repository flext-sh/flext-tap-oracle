"""Oracle Tap Protocols - USANDO classes reais do FLEXT ecosystem.

Este módulo define protocolos específicos do Oracle Tap usando classes que
REALMENTE existem no flext-core e flext-meltano.

Princípio: NUNCA duplicar, sempre usar o que existe realmente.

Copyright (c) 2025 FLEXT Contributors
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from typing import TYPE_CHECKING, Protocol

if TYPE_CHECKING:
    from collections.abc import Mapping

    from flext_core import FlextResult
    from flext_db_oracle import FlextDbOracleTable


class FlextOracleTapProtocol(Protocol):
    """Oracle-specific tap protocol using Python Protocol.

    Define interface Oracle-específica usando Protocol padrão.
    """

    def discover_oracle_tables(
        self,
        schema_name: str | None = None,
    ) -> FlextResult[list[FlextDbOracleTable]]:
        """Discover Oracle tables using flext-db-oracle metadata.

        Args:
            schema_name: Optional schema name filter

        Returns:
            FlextResult containing Oracle table metadata

        """
        ...

    def test_oracle_connection(self) -> FlextResult[bool]:
        """Test Oracle connection using flext-db-oracle infrastructure.

        Returns:
            FlextResult containing connection test result

        """
        ...


class FlextOracleStreamProtocol(Protocol):
    """Oracle stream protocol for data extraction.

    Define interface para streams Oracle usando Protocol padrão.
    """

    def extract_oracle_data(
        self,
        context: Mapping[str, object] | None = None,
    ) -> FlextResult[list[dict[str, object]]]:
        """Extract data from Oracle table.

        Args:
            context: Optional extraction context

        Returns:
            FlextResult containing extracted records

        """
        ...


# Export apenas protocolos Oracle-específicos
__all__: list[str] = [
    "FlextOracleStreamProtocol",
    "FlextOracleTapProtocol",
]
