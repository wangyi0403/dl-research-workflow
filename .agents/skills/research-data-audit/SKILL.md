---
name: "research-data-audit"
description: "Audit research data provenance, licensing, schema, quality, leakage, split integrity, and sensitive-data risks before modeling or after dataset changes."
---

# Research Data Audit

1. Read `AGENTS.md`, `docs/00_start.md`, and the current `docs/01_data_analysis.md`. Treat raw data as immutable. Record source, acquisition date, license, checksum, access restrictions, and release constraints.
2. Profile schema, units, ranges, missingness, duplicates, class/group balance, and suspicious identifiers.
3. Test leakage across train/validation/test, including entity, temporal, spatial, route, device, and near-duplicate leakage.
4. Validate label origin, adjudication, uncertainty, and post-outcome information.
5. Record every derived dataset as a reproducible transformation with input/output hashes. Separate sensitive or licensed data from shareable artifacts.
6. Stop and report when provenance, consent, license, or split integrity is insufficient; do not transform, delete, publish, or approve the affected data silently.

Update `docs/01_data_analysis.md` with the data-card fields, issue table, split audit, transformation ledger, and approved modeling view. Link unresolved risks to the Stage 1E experiment plan rather than creating parallel audit files.
