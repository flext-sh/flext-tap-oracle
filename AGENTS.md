# AGENTS.md — flext-tap-oracle

> **Parent workspace law** lives in [`../AGENTS.md`](../AGENTS.md) — read it first.
> Universal engineering core: `~/.agents/UNIVERSAL_CORE.md`. Composition: global skills + parent/root `AGENTS.md` + this scope delta. Do not re-embed universal law.
>
> **Standalone / independent mode:** when `../AGENTS.md` does not resolve, pin the parent raw `AGENTS.md` URL to the same branch/release as this package (never `main`).

<!-- AIHUB-AGENTS-SCOPE-LOCAL-BEGIN -->
**Package:** `flext_tap_oracle` · deps: `flext-core`, `flext-db-oracle`, `flext-meltano`, `flext-observability`

## Overview

Singer **tap** (extractor) for Oracle Database. Thin driver over `flext-meltano` (ADR-006), delegating connectivity to `flext-db-oracle`.

## Structure

```text
src/flext_tap_oracle/
├── api.py            # FlextTapOracleService(FlextMeltanoTapServiceBase)
├── tap.py            # discovery commands + catalog generation
├── streams.py rules.json
├── constants.py typings.py protocols.py models.py utilities.py   # AUTO-GENERATED facets
└── _utilities/
```

## Code Map

| Symbol | Kind | Location | Role |
|--------|------|----------|------|
| `FlextTapOracleService` | class | `api.py` | `FlextMeltanoTapServiceBase` |
| discovery | code | `tap.py` | command-driven catalog generation |

## Conventions (specific to this package)

- Discovery is **command-driven** (not a minimal tap class); `rules.json` + `streams.py` define stream topology.
- Oracle settings are namespaced — `settings.DbOracle.*`.

## Commands

```bash
make check PROJECT=flext-tap-oracle
make test  PROJECT=flext-tap-oracle       # tests/unit
```
<!-- AIHUB-AGENTS-SCOPE-LOCAL-END -->
