---
name: "claim-numerics-audit"
description: "Check manuscript numbers against experiment records, figures, tables, configurations, and units; report mismatches without silent edits."
---

# Claim Numerics Audit

Audit numerical assertions in the manuscript against their traceable research artifacts. The audit distinguishes results, uncertainty, configuration values, and reference noise instead of matching raw numbers mechanically.

1. Read `AGENTS.md`, the LaTeX/Markdown manuscript, `docs/05_experiment_plan.md`, `docs/06_result_tables.md`, `docs/07_experiment_tracker.md`, `docs/08_analysis.md`, `results/data`, and the cited figure/table sources.
2. For each reported numerical claim, record manuscript location, value and unit, comparison direction, Claim ID, and its supporting Experiment ID/table/figure/configuration. Ignore unambiguous equation labels, page numbers, and bibliography years unless they are used as a claim.
3. Check value, rounding, unit, denominator, split, seed aggregation, uncertainty interval, and comparison direction. Treat a real mismatch, stale source, or untraceable number as an issue; do not set arbitrary tolerances that hide a material discrepancy.
4. Verify superlatives and deltas against the appropriate comparison set. A task result may support an engineering claim without supporting a mechanism or generalization claim.
5. Write every verified item, mismatch, and unresolved item into `docs/11_pre_submission_audit.md` under “数字与论断核验”. Include the resolution owner; never silently edit source code, tables, or manuscript text.

## Gate outcome

- Pass only when all material reported values and directions are traceable and no unresolved discrepancy changes the stated claim.
- Otherwise report `conditional` or `fail`, identify the smallest repair, and preserve the original record.
