# Project Artifacts to Manuscript Mapping

Map approved project artifacts into the section plan in `docs/09_paper_plan.md`. Paper section names and order depend on the study and target venue.

| Project artifact | What it contributes |
|---|---|
| `docs/00_start.md` | Scope, authorization, environment, data governance, target deliverable, and disclosure constraints |
| `docs/01_data_analysis.md` | Data object, units, leakage risks, splits, observed patterns, and representative example |
| `docs/02_journal_scouting.md` | Current scope, article type, author guidance, policy, and formatting decisions; not evidence for a scientific claim |
| `docs/03_idea_report.md` | Research question, evidence boundary, closest work, selected claims, rejected alternatives, and Gate A decision |
| `docs/04_methodology.md` | Formal problem, assumptions, mechanism hypothesis, method, failure modes, and notation |
| `docs/05_experiment_plan.md` | Claim-driven comparisons, baselines, metrics, evaluation contracts, statistics, and run order |
| `docs/06_result_tables.md` | Result schema, source index, aggregation commands, and links to generated tables; not a manually maintained numerical ledger |
| `experiments/registry/experiments.csv` | Per-run configuration, provenance and terminal status |
| `docs/07_experiment_tracker.md` | Active supervision, cumulative repair count, deviations and links to run evidence |
| `docs/08_analysis.md` | Result interpretation, uncertainty, claim disposition, failures, and limitations |
| `docs/09_paper_plan.md` | The authoritative narrative, section reader questions, evidence placement, and figure/table plan |
| `docs/10_figure_report.md` | Figure/table source, takeaway, visual QA, and manuscript mapping |
| `docs/11_pre_submission_audit.md` | Citation, numerical, policy, and Gate F findings |
| `results/data/` | Machine-readable result truth source |
| `results/figures/`, `results/tables/` | Reproducible visual and tabular evidence |

## Section assembly

For every planned section, build a small matrix before prose:

| Reader question | Claim/Chain ID | Evidence/Experiment ID | Figure/Table | Citation | Limitation/unknown |
|---|---|---|---|---|---|

Use the matrix to detect empty claims, evidence without a narrative role, and figures that do not answer a reader question.

## Direction of truth

Numbers and scientific claims flow from raw/structured results through the formal analysis and claim decision into the manuscript:

`logs/configs/data → results/data → generated tables/figures → manuscript`

`docs/06_result_tables.md` indexes the sources and reproduction commands; `docs/08_analysis.md` records interpretation and claim decisions. Read numerical values from the indexed structured results or their reproducible generated outputs, rather than copying a second numerical truth source into 06.

Do not reverse this direction by changing an experiment record to match prose. If manuscript text conflicts with the source chain, freeze the statement, record the conflict, and resolve it at the evidence artifact.
