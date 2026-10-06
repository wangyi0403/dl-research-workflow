---
name: "result-to-claim"
description: "Assess which completed experiments support, weaken, reject, or leave claims unresolved; separate performance, mechanism, and generalization evidence."
---

# Result-to-Claim Gate

Use completed, traceable experiment records to set each Claim ID's permissible wording. This is an evidence gate, not a way to turn positive metrics into a stronger story.

1. Start from `docs/00_start.md` and the Claim IDs under review. Read their entries in 03, planned comparisons in 05, source index in 06, and linked structured results and registry rows. Consult 07, logs and configurations for relevant deviations or provenance gaps; do not load every run. Record absent or incompatible sources rather than filling gaps from memory. Rebuild reported tables with their recorded aggregation command; keep numeric outputs generated from structured data, with 06 as the schema/source index.
2. For every Claim ID, identify the planned comparison, analysis unit, data split, metric, uncertainty treatment, baseline, and failure or stopping condition.
3. Classify the result as `promote`, `weaken`, `reject`, or `collect-more-evidence`. State the exact supported result, the unsupported extrapolation, and the smallest discriminating next check.
4. For engineering research, decide separately whether the result supports: (a) the target engineering task under its stated operating constraints; (b) the proposed measurement, physical, or inference mechanism; and (c) any transfer claim. A task improvement alone does not establish (b) or (c).
5. Write the decision, supporting Experiment IDs, confidence/uncertainty, and next action into `docs/08_analysis.md`. Preserve failed and null results. Update the same Claim ID in `docs/03_idea_report.md`: promote → promoted, weaken → weakened, reject → rejected, collect-more-evidence → needs-evidence. Analysis retains the decision evidence; do not maintain a second current-status ledger.

## Decision rules

- A reported number is admissible only when its experiment ID, configuration, data version/split, seed treatment, and output path are traceable.
- Do not call a mechanism established unless an intervention, ablation, counterfactual, condition shift, or similarly discriminating test supports it.
- Do not call a result generalizable from one site, dataset, condition, or seed. State the actual scope.
- When protocol validity is doubtful, route to design repair or rerun; when evidence is insufficient, weaken the claim; when the core mechanism fails, route to pivot or reject.
- Do not silently edit the manuscript or rerun costly experiments. Report the decision and required authorization.

Report the Claim ID table, gate decision, unresolved conflicts, and the next smallest verifiable action.
