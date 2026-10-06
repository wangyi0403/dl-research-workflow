---
name: "paper-plan"
description: "Plan an evidence-led paper from verified claims, results, and venue constraints. Use before drafting to map its narrative, sections, figures, limitations, and evidence."
---

# Paper Plan

Build the narrative before drafting. The plan must make it possible to trace every central statement to evidence and to distinguish the contribution from its implementation.

## Inputs and output

Read `AGENTS.md`, `docs/03_idea_report.md`, `docs/04_methodology.md`, `docs/05_experiment_plan.md`, `docs/06_result_tables.md`, `docs/08_analysis.md`, verified citations, and the target venue's actual author guidance. Read `docs/10_figure_report.md` only if it already contains an earlier figure inventory; Stage 3A must not depend on a later Stage 3B artifact. Update `docs/09_paper_plan.md` and its Gate D record.

## Workflow

1. Select the paper type, target reader and central claim. State the comparison or knowledge gap, tested conditions, evidence status and maximum permissible wording. Method, measurement, benchmark, theory, negative-result and systems contributions may require different evidence and ordering.
2. Build the contribution chain: problem → evidence gap → mechanism or design principle → method as a testable implementation → decisive evidence → scope and limitations.
3. For engineering research, make the chain explicit: real field problem and consequence → why existing engineering paths are inadequate → reusable measurement/physical/inference question → supported new knowledge or principle → concrete method → separate engineering and scientific validation. Do not frame a VLM, model family, or a collection of modules as the contribution by itself.
4. Organize necessary supporting claims around the central answer. For each, identify the reader question, required evidence, strongest concrete alternative, exact readout and any open evidence gap; reuse the project's existing Claim and analysis records. Order sections by the reader's dependencies rather than the project chronology. If the project provides `docs/WRITING_STANDARD.md`, instantiate its user-specific budgets in `docs/09_paper_plan.md`; current user instructions, approved structure and verified venue constraints take precedence. Do not invent content to fill quotas.
5. Select representations by reader task: prose for a simple fact, a table for exact lookup, a plot for patterns, an equation for a relation, and an algorithm for consequential sequence/state. Pair them only for distinct jobs. Put decisive evidence and interpretation-critical conditions in the main text; the supplement can hold exhaustive reproducibility detail. Quantitative displays must be reproducible, and method names agree with the methodology.
6. Prewrite the limitations and permitted claims. Preserve evidence-supported boundaries, including coverage, weak signals, data quality, causal scope, and generalization limits; do not add generic disclaimers or promotional future work.
7. Conduct an independent local review using `$research-quality-gate` or a clearly separated critic pass. Check logical flow, claim-evidence alignment, missing decisive tests, closest-work positioning, figure plan, and venue feasibility. Record minimum fixes in the Gate D section.

## Rules

- A good outline is not an abstract expanded into headings. Each central claim needs a known evidence location.
- A task-performance gain does not automatically establish a mechanism explanation or transfer claim.
- A missing experiment is proposed only when positive, negative or inconclusive outcomes can change a claim or decision. Narrow a claim when that is the sufficient evidence-based repair; do not add every possible control or fix a paper around a favorable post hoc subset.
- Title, abstract, introduction, principal displays and conclusion express the same supported promise at different levels of detail. A scoped trade-off or a negative finding can be central when the actual evidence supports it.
- Use exact citation metadata only after verification; leave unresolved sources marked for verification rather than generating BibTeX from memory.
- Do not write the full manuscript, alter results, or submit material as part of planning.

Report the narrative spine, Claim/Chain-to-section matrix, figure/table plan, limitations, unresolved evidence, and Gate D decision.

When an engineering method paper needs a concrete introduction pattern, consult `references/intro-flowchart.md` as an optional example. Use it only where it fits the selected paper type and evidence; it does not set contribution counts or a mandatory section structure.
