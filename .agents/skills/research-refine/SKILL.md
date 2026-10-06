---
name: "research-refine"
description: "Refine an accepted, evidence-backed idea into a minimal method, mechanism hypothesis, failure modes, and claim-driven validation plan."
---

# Research Refine

Refine an approved research direction without allowing it to drift from the problem it is meant to solve. The output is a falsifiable method-and-validation plan, not a feature list.

## Inputs and output

Read `AGENTS.md`, `docs/03_idea_report.md`, data analysis, verified literature/evidence records, and any approved constraints. Update `docs/04_methodology.md`; record material decisions in `docs/03_idea_report.md` or the project decision log.

## Workflow

1. **Freeze the problem anchor.** State the real problem, affected setting, measurable consequence, existing-solution bottleneck, and the exact research question. Mark assumptions and evidence gaps.
2. **State the mechanism hypothesis.** Identify observable signals, nuisance factors, representation or inference failure, and a falsifiable prediction. For engineering work, distinguish a physical/measurement contribution from a useful empirical hypothesis; call it physical only when its mechanism and test are concrete.
3. **Derive one candidate contribution.** Express a transferable design principle or knowledge claim before naming the method. Explain how it differs from closest work using verified evidence.
4. **Design the smallest sufficient method.** Define inputs, outputs, modules, interfaces, training/inference path, and why each part tests or enables the hypothesis. Remove any module with no diagnostic, claim, or control purpose.
5. **Specify failure modes.** List expected non-identifiability, distribution shift, weak-signal, label, data-coverage, and resource failure modes, including how each would be detected.
6. **Build the validation chain.** Map every Claim ID to the required data, baseline/control, metric, ablation or intervention, uncertainty treatment, and stopping condition. Engineering work must separately test operational value, mechanism/design-principle evidence, and any transfer claim.
7. **Run a focused review.** Use the project's local review procedure or `$research-quality-gate` to test problem fidelity, mechanism specificity, parsimony, evidence sufficiency, feasibility, and drift. Record findings in the active Stage artifact; do not assume an unavailable sub-agent or external model.

## Non-negotiable constraints

- Do not turn an unverified observation into a mechanism, law, novelty claim, or physical contribution.
- Do not solve a different, easier problem merely because it makes a cleaner model demo.
- Prefer a small mechanism that can be disproved over a broad system with many loosely connected innovations.
- Do not promise expensive training, external review, upload, or publication without the required authorization.

Report the frozen problem anchor, method chain, rejected additions, claim-to-validation table, residual risks, and the next Stage 1E action.
