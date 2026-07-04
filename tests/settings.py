"""Runtime settings for flext-tap-oracle tests."""

from __future__ import annotations

from typing import Annotated

from flext_tests.settings import FlextTestsSettings

from flext_core import u
from flext_tap_oracle import FlextTapOracleSettings, t
from tests.constants import TestsFlextTapOracleConstants as c


class TestsFlextTapOracleSettings(FlextTapOracleSettings, FlextTestsSettings):
    """Tap Oracle settings extended with the shared test namespace.

    Supplies non-secret default credentials so the test-runtime singleton is
    instantiable without live Oracle env vars. The production
    ``FlextTapOracleSettings`` keeps these fields required.
    """

    oracle_user: Annotated[
        t.SecretStr,
        u.Field(description="Oracle database username"),
    ] = t.SecretStr(c.TapOracle.Tests.UNIT_ORACLE_USER)
    oracle_password: Annotated[
        t.SecretStr,
        u.Field(description="Oracle database password"),
    ] = t.SecretStr(c.TapOracle.Tests.UNIT_ORACLE_PASSWORD)


__all__: list[str] = ["TestsFlextTapOracleSettings"]
