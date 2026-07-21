# AGENTS.md — flext-tap-oracle

> **General FLEXT law & workspace conventions live in the root [`../AGENTS.md`](../AGENTS.md) — read it first.** SSOT for facade layering, config/settings, `make`-only workflow, testing law, git discipline. This file adds ONLY `flext-tap-oracle`-specific knowledge.
>
> **Standalone / independent mode:** if this package is checked out on its own (imported as a dependency, vendored, or cloned solo) there is no parent workspace, so `../AGENTS.md` does not resolve. Then read the root law from the raw file on the SAME branch/release the project is on: <https://raw.githubusercontent.com/flext-sh/flext/0.12.0-dev/AGENTS.md> (pin the branch/tag to your working line, never `main`).

**Package:** `flext_tap_oracle` · deps: `flext-core`, `flext-db-oracle`, `flext-meltano`, `flext-observability`

## Overview

Singer **tap** (extractor) for Oracle Database. Thin driver over `flext-meltano` (ADR-006), delegating connectivity to `flext-db-oracle`.

## Structure

```
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
