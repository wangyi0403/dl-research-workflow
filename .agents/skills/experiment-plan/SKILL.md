---
name: "experiment-plan"
description: "Design claim-driven experiments, baselines, metrics, ablations, statistics, run order, compute budget, and stop rules after method refinement."
---

# Experiment Plan

Turn an evidence-backed method into a compact, falsifiable experiment contract. Reuse the current scope, author decisions and resource authorization; ask only about missing boundaries that change the next action.

## Inputs

Read `AGENTS.md`, the current state in `docs/00_start.md`, the approved data view in `01_data_analysis.md`, Claim/Evidence IDs in `03_idea_report.md`, and the method in `04_methodology.md`. Consult `02_journal_scouting.md` only when a selected venue changes evaluation or reporting. For reproduction work, use the verified reproduction contract rather than reconstructing details from memory.

## Freeze the decisive comparisons

For each claim, specify:

- Exact permitted claim, competing explanation and minimum discriminating evidence.
- Dataset version, independent analysis unit, leakage-safe split and preprocessing fit boundary.
- Strong and relevant baselines, fair tuning/information/compute budgets and required controls. Identical optimizers or parameter counts are not universally fair across model families.
- Primary metric, direction, unit, aggregation, repetitions and uncertainty. Separate dataset, subject and initialization variability; choose repetition counts for the actual design rather than a fixed seed quota.
- Immutable configuration, planned Experiment IDs, source/output paths and table/figure slots.
- Success and falsification thresholds, expected failure interpretation, resource ceiling and next action for each outcome.

Prefer the smallest set that can change the decision. Include ablations, stronger simpler alternatives, robustness or external validation only when needed for a stated claim. A performance gain alone does not establish mechanism or transfer. Skip frontier-model, physical-model and generative-evaluation requirements when they do not apply.

## Execution order and stopping

Order work by decisive information and cost: data/metric checks and a small local smoke, strong controls, the candidate method, then the necessary discriminating checks. A different order is valid when it tests a linchpin more cheaply. Separate must-run from optional experiments.

Distinguish an estimated or between-run time budget from an enforced process timeout. State which process/job may be stopped, how partial artifacts are preserved, and who resumes the workflow. A decisive failure or budget ceiling blocks the affected path; it does not authorize unlimited tuning, weaker comparisons or a new research direction.

## Update existing project artifacts

| Artifact | Owns |
|---|---|
| `docs/05_experiment_plan.md` | Claim-to-experiment matrix, evaluation contract, priority, cost and Gate B |
| `docs/06_result_tables.md` | Traceable result-table skeletons; values remain pending until executed |
| `experiments/registry/experiments.csv` | Per-run identity, configuration/data/code versions, status and provenance |
| `docs/07_experiment_tracker.md` | Active controller binding, failure diagnosis, cumulative repair count and approved deviations |

Preserve established headings and records. Never replace `07_experiment_tracker.md` with a second TODO/Running/Complete table or overwrite prior run/config evidence. Link to the registry by Experiment ID. Each planned result cell identifies its metric, analysis unit, uncertainty and intended source; do not insert expected numbers as results.

Run `research-quality-gate` Gate B once the contract is reviewable. State the highest-risk assumption, permitted first run and any remaining blocker. A filled plan is not execution evidence.

## Conditional references

- `references/baseline-selection.md`: closest-work and baseline choice needs further detail.
- `references/ablation-design-guide.md`: a component or mechanism needs a discriminating intervention.
- `references/evaluation-extensions.md`: generative/agent, physics-informed/numerical, or uncertainty-aware engineering surrogate evaluation.
- `references/code-template.md`: implementation scaffolding is needed; adapt it to the approved project and retain its provenance.
