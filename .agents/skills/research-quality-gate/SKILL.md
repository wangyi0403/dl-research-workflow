---
name: "research-quality-gate"
description: "Evaluate evidence-based Gate A-F decisions against project records. Use at research checkpoints; identify decisive gaps and route failures to concrete repairs."
---

# Research Quality Gate

Assess whether a research stage has enough reliable evidence and complete artifacts to continue. One skill serves Gates A-F, but the review effort must match the consequence and uncertainty of the decision.

## Gate map

| Gate | Stage | Focus | Main artifacts |
|---|---|---|---|
| A | Stage 1C | Question, novelty boundary, feasibility, and journal fit | `docs/02_journal_scouting.md`, `docs/03_idea_report.md` |
| B | Stage 1E | Claim-driven experiment design | `docs/03_idea_report.md` through `docs/06_result_tables.md` |
| C | Stage 2C | Protocol integrity, results, and permissible claims | `docs/06_result_tables.md`, `docs/07_experiment_tracker.md`, `docs/08_analysis.md` |
| D | Stage 3A | Narrative and evidence placement | `docs/09_paper_plan.md` |
| E | Stage 3B | Figure/table truthfulness, completeness, and consistency | `results/figures/`, `results/tables/`, `docs/10_figure_report.md` |
| F | Stage 4 end | Citation, numerical, manuscript, and submission readiness | `paper/main.*`, `docs/11_pre_submission_audit.md` |

## Review strategy

- Use a focused reviewer or deterministic check for a narrow, low-risk checkpoint.
- Use multiple independent local perspectives for important gates, ambiguous evidence, or cross-disciplinary claims. Select only roles that address a real risk; five roles are not mandatory for every gate.
- Give reviewers the artifact and rubric without the expected conclusion or other reviewers' answers. Merge findings only after independent review.
- Preserve a justified singleton or minority finding. The final decision follows evidence and blockers, not majority vote.
- Use an actually available external model when explicitly requested or covered by existing project authorization for the same purpose, data scope, and cost boundary. Reuse that authorization across gates; obtain authorization only for missing or changed scope. Minimize or de-identify supplied material. Treat the result as a second opinion, never as scientific evidence.

## Finding and verdict contract

Record each material criterion or finding with:

- `status`: `pass`, `warn`, `fail`, or `unknown`;
- evidence pointer and source role;
- consequence for the current claim or stage;
- required fix, owner, and smallest next action;
- exception and rollback path when applicable.

`unknown` is not a pass. Use it when the required source, experiment, permission, or interpretation is unavailable. The overall gate verdict remains:

- `PASS`: no unresolved blocker; required evidence and artifacts are present;
- `CONDITIONAL`: bounded repairs or explicit unknowns remain, and the permitted next action is stated;
- `FAIL`: a blocker invalidates advancement or requires redesign, rerun, or a return to an earlier stage.

## Cross-gate failure checks

Check the relevant items rather than mechanically ticking all of them:

1. implementation does not match the described method;
2. a number lacks a real experiment source;
3. the easiest test replaced the decisive test;
4. a bug or data leak is being narrated as insight;
5. a claimed method or analysis was not executed;
6. only one frame or explanation was considered;
7. a citation does not exist or does not support the attached claim;
8. a result depends on an unstated reference, conflict, exclusion, or abstention rule.

## Gate-specific checks

### Gate A — Question and direction

Read the relevant good-question references. Check importance, testability, nearest-work collisions, data/compute feasibility, linchpin assumptions, alternatives, and author decision. A fixed idea count, paper count, novelty score, or pilot quota is not a gate criterion.

Route failure to a narrower question, additional evidence, a revised mechanism, hold, or reject.

### Gate B — Experiment design

Read `references/statistical_reporting_standards.md` when inferential statistics matter. Check that each claim has a decisive comparison, strong and fair baselines, appropriate metrics, uncertainty treatment, ablations or alternative explanations, explicit success/failure criteria, run order, cost ceiling, and empty traceable result slots.

For generative/agent evaluations or engineering numerical/surrogate models, invoke `$experiment-plan` and apply its conditional evaluation extension before approving the gate.

### Gate C — Results and claims

Check analysis unit, exclusions, protocol deviations, effect magnitude, uncertainty, failed/null runs, inconsistencies, and the link from Experiment ID to Claim ID. Statistical significance is not required for every study; use the comparison rule appropriate to the design.

Route failure to protocol repair/rerun, design revision, claim weakening, more evidence, pivot, or rejection.

### Gate D — Paper plan

Check the central claim, reader questions, evidence location, transitions, closest-work positioning, figure/table plan, limitations, target-venue fit, and consistency of any Running Example. Do not enforce a universal paper section order.

### Gate E — Figures and tables

Check that planned figures/tables exist, are traceable to data or a documented source, use honest scales and uncertainty, remain interpretable without color alone, match manuscript terminology, and pass programmatic plus visual QA. Preserve an established project palette unless it is misleading or inaccessible; do not impose universal role colors.

For initial drafting, `CONDITIONAL` may defer only consistency checks that depend on prose not yet written. Scientific validity, data provenance, reproducibility, and required checks on the figures/tables themselves must pass. Record the input version, each deferred item, owner, permitted drafting scope, and closure trigger in `docs/10_figure_report.md`; close them in the Gate E record after drafting and before Gate F passes. Gate F references these valid checks rather than repeating them; input changes invalidate only affected items under the project rules. Material scientific `unknown` or `fail` findings block the affected scope and cannot be deferred under this exception.

### Gate F — Pre-submission

Run `citation-verification` and `claim-numerics-audit`. Use `paper-audit` in `gate` mode for its automated blocker screen. A full `deep-review` belongs to the requested manuscript review stage; reuse that review rather than creating a second committee here. Read `check_runs` and `review_status`: exit 0, empty findings or a diagnostic score do not establish scientific acceptance, author consent, or completion of skipped checks. Confirm the target venue's current official guidance, compiled artifact, figure/table references, disclosures, and unresolved author decisions.

## References

| File | Use |
|---|---|
| `references/good-question/heilmeier-catechism.md` | Gate A question self-test |
| `references/good-question/hamming-nielsen-research-taste.md` | Gate A significance assessment |
| `references/good-question/platt-strong-inference.md` | Gate A testability and competing hypotheses |
| `references/statistical_reporting_standards.md` | Gates B-C when statistical inference applies |
| `references/editorial_decision_standards.md` | Gates C/F editorial thresholds |
| `references/review_criteria_framework.md` | Gates D-E structure and figure/table criteria |
| `references/quality_rubrics.md` | Gate F readiness rubric |
| `agents/*.md` | Load only reviewer roles selected for the current risk |

## Output

Report:

1. Gate and overall verdict;
2. criterion/finding table with `pass/warn/fail/unknown`;
3. evidence-backed disagreements and unresolved unknowns;
4. blocker or minimum repair;
5. permitted next action, owner, approval need, and rollback path.
