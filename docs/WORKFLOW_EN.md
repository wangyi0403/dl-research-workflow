# Evidence-driven workflow

[English](WORKFLOW_EN.md) · [中文完整流程](WORKFLOW.md)

This guide explains the Stage 0–6 contracts. Numbered records own their evidence;
`00_start.md` points to the current stage, authority and next action. Preserve an
existing study's approved question, methods and artifacts before continuing.

## Stage 0 — Scope and setup

Define the research question, success and falsification criteria, data access,
resource limits, permissions and expected deliverables in `00_start.md`. Verify
the project environment and available tools. A seed idea is not novelty evidence.
The researcher determines scientific direction and external-action authorization.

## Stage 1 — Evidence, questions, methods and experiments

**1A: Data.** Use `research-data-audit` to examine observation units, missingness,
leakage, splits, balance and temporal/spatial structure. Record dataset identities,
sources, transformations and a representative running example in record 01.
Keep raw data immutable and distinguish public, restricted and licensed assets.

**1B: Venue.** Use `journal-scout` when venue constraints affect the study. Verify
the current scope, article type, author instructions, data/code policy and relevant
recent work; record requirements and versions in 02. Reuse an already chosen
venue and check changed requirements instead of restarting selection.

**1C: Questions.** Use `research-ideation` to generate evidence-backed candidates,
compare recent work, test feasibility and keep alternatives. Record each question,
claim, source identity, support location and unresolved assumption in 03.
For engineering work, connect a consequential practical problem to a transferable
measurement, physical or inferential question and falsifiable predictions.

**Gate A:** Check question substance, credible evidence gap, testability, data
availability, feasibility and alternatives. An untested mechanism is unresolved;
a mechanism contradicted by decisive evidence cannot be rescued by larger compute.
Failing A routes back to evidence, scope or a different question.

**1D: Method.** `research-refine` formalizes the problem, assumptions, notation,
minimal mechanism, comparisons, limitations and resource needs in 04. Add a module
only when it supports a claim or diagnostic purpose; established components alone
do not establish scientific novelty.

**1E: Design.** `experiment-plan` maps claims to datasets, fair baselines, metrics,
uncertainty, ablations, robustness and failure-first decisions. Prepare 05–07 before
formal runs. Reproduction requires a reviewed contract; seeing a repository is not
a successful reproduction.

**Gate B:** Verify leakage-free splits, validation/model selection and final-test
rules, meaningful baselines, declared metrics and inclusion rules, independent units,
statistical treatment, frozen configurations, budget and interpretation of negative
results. Engineering and mechanism claims require their corresponding evidence,
not decorative extra datasets.

## Stage 2 — Run and interpret experiments

Verify a minimal batch, metrics, checkpoints, logs, seeds and expected costs before
training. External servers or paid compute require matching authorization.

`experiment-runner` records each actual run with a new immutable experiment ID,
configuration hash, data/split identity, code revision, environment, hardware,
command, timestamps, log/result paths and terminal state. The CSV registry points
to the run's original state file. The tracker in 07 explains decisions and deviations;
its active-run view is derived from real run records.

Keep one registry/scheduler owner. Monitoring requires a real run or pending request
and explicit user intent; an unchanged running state stays quiet. A bounded,
evidence-based repair is permitted within authorization, with at most three attempts
for the same failure and phase unless additional attempts are approved.

Record estimates, uncertainty, failures, contradictions, resource use and provenance
in 08. `result-to-claim` assigns promote, weaken, reject or collect-more-evidence
to the relevant claims. Group quantitative analyses by the correct independent unit.

**Gate C:** Check the frozen protocol or disclosed deviations, statistical meanings,
traceability, contradictions and evidence-calibrated conclusions. Protocol errors
route to corrected design/runs; insufficient evidence routes to a narrower claim;
a failed idea can return to Stage 1. Do not silently drop failed or missing runs.

## Stage 3 — Argument, figures and tables

`paper-plan` defines article type, central answer, contribution chain, reader path,
evidence positions and figure/table functions in 09. Organize by scientific
questions and dependencies, not the order in which the project happened.
Adapt the writing structure to the article, venue and already approved manuscript.

**Gate D:** The argument and contribution match verified evidence and recent work;
each section and figure supports the central answer; meaningful limitations have a
place; wording agrees with the claim status.

Use `scientific-figure-making` for data figures and `paper-illustration` for conceptual
figures. Preserve numerical inputs, plotting code, units, uncertainty, labels and
claim identities. Record reproducibility and actual-size visual checks in 10.

**Gate E:** Figures and tables are reproducible, accurate, traceable and legible,
with consistent captions and scientific meaning. If only checks requiring a complete
manuscript remain, record CONDITIONAL with named tasks and a deadline before Gate F.
Critical unknown scientific evidence or failed figure validity cannot use this route.

## Stage 4 — Draft and verify the manuscript

`paper-write` starts after the argument and critical evidence are ready and the
appropriate D/E conditions hold. Use the project's chosen drafting language; a
Chinese review draft followed by English LaTeX is the default workflow, not a
requirement for every venue. `academic-humanizer` improves prose while preserving
scientific meaning, evidence strength and the author's intended judgment.

Keep title, abstract, introduction, principal displays and conclusion aligned to
one supported promise. Verify references and numerical consistency using
`citation-verification` and `claim-numerics-audit`; record checks in 11. Current
institution/venue rules determine AI use and disclosure. Do not optimize for AI
detector scores or invent author, ethics or availability statements.

**Gate F:** The target-language source is stable, references and numbers are checked,
evidence links are complete, pending E tasks are closed, applicable format and
disclosure requirements are verified and the manuscript compiles. A script pass
alone is not scientific or editorial approval.

## Stage 5 — Review and repair

`paper-audit` combines relevant methodological, editorial, domain, literature or
critical perspectives. Keep script screening separate from actual review findings.
Reviewers see evidence and rubrics rather than the desired verdict. Consolidate
by evidence and consequence, retain supported disagreement and separate reviewer
and editor roles when independence matters.

Classify severity as major, moderate or minor, and distinguish an issue from an
optional suggestion. Connect real reviewer replies to completed revisions, their
locations and affected checks. Plans cannot be reported as completed changes.

Use at most four evidence-based review/repair rounds and stop early when decisive
issues are resolved. Escalate stagnant scientific tradeoffs to the researcher.
Recheck changed evidence and bind each review outcome to the actual manuscript version.

## Stage 6 — Local submission and release readiness

`cover-letter` and `research-publication` prepare reviewable local materials after
the venue and manuscript are stable. Check authorship, conflicts, funding, ethics,
data/code rights, references, figures, files, reproduction commands and checksums.
Separate public, restricted and non-redistributable assets in 12.

Uploading, submitting, creating a DOI or sending messages requires the relevant
user authorization. Preparation is not publication and a generated release checklist
does not establish that its requirements were met.

## Gate outcomes and changes

Findings use pass/warn/fail/unknown, with evidence, impact, owner and next action.
Overall gate decisions are PASS, CONDITIONAL or FAIL for the reviewed artifact version.
CONDITIONAL names allowed progress, outstanding tasks and expiry conditions. A
critical unknown or blocker prevents dependent work.

| Change | First gate to revisit | Consequence |
|---|---|---|
| Question, mechanism, novelty or decisive feasibility | A | Revisit B and affected downstream contracts |
| Data, split, baseline, metric, model selection or statistical protocol | B | Update design before dependent runs; recheck existing results at C |
| New evidence, corrected analysis, conflicts or claim strength | C | Update claims, then affected D–F items |
| Article type, argument or evidence position | D | Recheck affected E/F items |
| Figure data, plotting code or visual encoding | E | Also revisit C when numbers or interpretations change |
| Manuscript, citations, numerics or disclosures | F | Return upstream if the change exposes an earlier problem |

Keep unaffected checks. On resumption, compare the next action to the frozen
question, criteria, protocol and artifact versions. Reuse existing records rather
than create parallel memory or scheduling state. Completion requires the actual
deliverables and applicable verification, not merely initialization or run startup.
