---
name: "paper-write"
description: "Draft or revise an academic manuscript from an approved plan and verified evidence. Use for Stage 4, translation, section drafting, or LaTeX preparation."
---

# Paper Write

Turn approved research artifacts into a coherent manuscript without changing the evidence, results, or author decisions. The default template workflow is Chinese review followed by English LaTeX, but the user or target venue may require another language or sequence.

## Readiness check

Before full drafting, read `AGENTS.md` and the relevant analysis, paper plan, figure report, result tables, verified citations, and current venue guidance needed to establish the manuscript's evidence and structure. The template records these in `docs/08_analysis.md` through `docs/10_figure_report.md`. For a section or local prose edit, use the corresponding material and sufficient surrounding context; reuse unchanged, already-verified evidence and check only the claims or sources affected by the revision.

Confirm:

- the central claims and their maximum permissible wording;
- the numerical truth source and experiment IDs;
- the figure/table inventory, sources, and Gate E status;
- unresolved evidence, policy, author, and disclosure decisions;
- the existing LaTeX/document structure and files that must not be overwritten.

If a central result, figure, citation, or author decision is missing, mark the exact gap and draft only the unaffected material. Do not invent a bridge, number, reference, or completed experiment.

Gate E may permit initial drafting as `CONDITIONAL` only when scientific validity, data provenance, reproducibility, and the required checks on the figures/tables themselves pass, and the remaining checks concern consistency with prose that does not yet exist. Record the input version, each affected item, owner, permitted drafting scope, and closure trigger in the existing figure report. Close these items in the Gate E record after drafting and before Gate F passes; Gate F references valid checks rather than repeating them. Recheck only affected items when their inputs change. A material scientific `unknown` or `fail` blocks the affected drafting scope; assigning an owner does not resolve it.

## Writing decisions

- **Structure:** Follow the approved paper plan, study design, and venue requirements. When present, read `docs/WRITING_STANDARD.md` for the user's project-specific section order, budgets, and editorial defaults; do not impose that preference on unrelated users or automatically restructure approved manuscripts. Record actual section word/figure/table counts and justified departures in the existing paper plan.
- **Voice:** Match the author's established voice and the venue's accepted usage. First person, plural first person, and passive voice are all conditional choices; do not enforce a universal ban.
- **Author stance:** Recover the intended reader judgment from the current manuscript, evidence and accepted decisions. Draft that supported proposition directly, with its actual scope and modality. Do not create an overstrong proposition and then retract it, invent weaknesses, or carry internal audit history into the prose. Read `references/writing-principles.md` for defensive-writing calibration when drafting or substantively revising.
- **Language:** Use the user-approved workflow. In the research template, Chinese v1/v2 review followed by English is the default, not an irreversible rule.
- **Source layout:** Preserve the established single-file or multi-file structure unless a confirmed venue rule or explicit user request requires migration.
- **Figures:** Preserve vector/raster formats, stable filenames, and source links. Copy, convert, flatten, or rename only when the submission package requires it, and re-verify the rendered manuscript afterward.
- **Citations:** Draft placeholders may identify unresolved citations, but the final manuscript uses only verified records whose source supports the attached claim.
- **Editorial format:** Apply the project's writing standard and applicable editor requirements recorded in `docs/02_journal_scouting.md`. Keep titles concise, define abbreviations, separate short captions, essential reading notes, and substantive prose, and ensure the conclusion includes evidence-supported insight, application implications, and testable future work. Preserve independent figure readability and scientific scope. Check article self-reference and tense semantically; do not globally replace every occurrence of `study` or force one tense throughout.

## Workflow

### 1. Build the section evidence map

Use `references/doc-to-paper-mapping.md` to map each planned section to Claim IDs, Evidence IDs, result artifacts, figures/tables, citations, limitations, and reader questions. Resolve contradictions before prose generation.

### 2. Draft from evidence modules

For each section:

1. identify the reader question and section claim internally;
2. assemble the evidence, method details, figure/table role, and any material limitation relevant to the claim;
3. write connected paragraphs that establish the supported author position; keep necessary inferential links visible without forcing each paragraph to announce its purpose or end in a caveat;
4. keep observation, interpretation, mechanism claim, and speculation distinct;
5. leave an explicit unresolved marker rather than completing a sentence from memory.

Use the section-specific references only when that section is being drafted. Read `references/paragraph-flow.md` for structural repair, `references/related-work.md` for positioning, and `references/discussion-conclusion.md` for interpretation. Examples are optional reasoning patterns; their facts, counts and suggested phrasing are not requirements for this manuscript.

### 3. Chinese review rounds when applicable

For the template's default workflow:

- **v1:** produce a complete Chinese draft for structure, argument, contribution, and evidence review.
- **Round 1:** incorporate the user's decisions on large issues and record unresolved evidence.
- **v2:** revise for terminology, paragraph logic, figure/table consistency, limitations, and venue fit.
- **Round 2:** incorporate detailed user review and freeze the approved content before English drafting.

Use stable project filenames; the conventional names `paper/draft_cn_v1.*` and `paper/draft_cn_v2.*` are defaults only when they do not conflict with an existing source tree.

### 4. English manuscript and LaTeX

Translate or draft from the approved content rather than independently rewriting the scientific story. Obtain the current official template only after the venue and version are confirmed. Preserve terminology, notation, citations, values, figures, and claim scope across languages.

Compile the actual submission source and visually inspect affected pages. A successful compiler exit does not prove that equations, tables, figures, references, or page layout are correct.

### 5. Integrity and handoff

Before declaring Stage 4 complete:

- run citation and numerical audits;
- check every figure/table reference and source;
- reverse-outline the manuscript to confirm each paragraph advances the approved narrative;
- reconcile the title, abstract, introduction, decisive displays and conclusion against the same Claim state; verify methods as performed, comparison classes, analysis units and uncertainty definitions;
- verify terminology, notation, abstract/conclusion claims, limitations, disclosures, and venue scope;
- record remaining `pass/warn/fail/unknown` items in `docs/11_pre_submission_audit.md`;
- route the manuscript to `research-quality-gate` Gate F and `paper-audit`, rather than self-certifying it inside the writing pass.

## Rules

- Never strengthen a claim because the prose sounds weak.
- Do not weaken a supported claim merely to sound cautious. Preserve a possible explanation instead of rewriting it as necessary proof followed by a warning. State a given uncertainty once unless distinct conditions require separate treatment.
- Never change a number, unit, split, significance result, citation identity, or figure content without returning to its source artifact.
- Do not turn a method name, module list, benchmark score, or system implementation into a contribution unless the approved evidence supports that framing.
- Preserve real limitations where they affect interpretation; do not mechanically append limitations to every paragraph. Remove only unsupported self-defeat, repetition, or generic filler.
- Follow current venue guidance over generic examples, historical templates, or remembered formatting rules.

## References

| File | Open when |
|---|---|
| `references/writing-principles.md` | Framing contribution, evidence-led paragraphs, related work, limitations, and conclusion. |
| `references/writing-prep-checklist.md` | Confirming claim, number, figure, citation, source-layout, and policy readiness before drafting. |
| `references/doc-to-paper-mapping.md` | Mapping numbered project artifacts into the approved paper plan. |
| `references/abstract.md` | Drafting or revising the abstract. |
| `references/introduction.md` | Drafting or revising the introduction. |
| `references/method.md` | Drafting or revising methods. |
| `references/experiments.md` | Drafting setup, results, and analyses. |
| `references/paragraph-flow.md` | Repairing paragraph function, inferential links, information order and section handoffs. |
| `references/related-work.md` | Synthesizing closest work by scientific question and verified comparison dimensions. |
| `references/discussion-conclusion.md` | Interpreting mixed evidence, scope, implications and the final research answer. |
| `references/examples/` | A concrete pattern is needed after the paper type and section purpose are known. |
