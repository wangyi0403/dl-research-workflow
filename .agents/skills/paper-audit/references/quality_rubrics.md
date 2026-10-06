# Evidence-Based Review Rubric

Judge the manuscript against its research question, study type, evidence and confirmed target venue. Use findings to choose causal repairs. Numeric diagnostics do not predict editorial acceptance and cannot override a verified blocker or an unknown.

| Dimension | Evidence to inspect | Material unresolved concern |
|---|---|---|
| Soundness / quality | Assumptions, derivations, data splits, controls, evaluation and statistics | A flaw invalidates the central inference or comparison |
| Clarity | Definitions, notation, paragraph logic and claim wording | A reader cannot determine what was done or what a result supports |
| Presentation | Rendered figures, tables, captions, references and venue instructions | A key result is unreadable, inconsistent or misrepresented |
| Novelty / originality | Verified prior work and direct mechanism or capability comparisons | The stated distinction is contradicted or unsupported |
| Significance | Problem importance, effect size, uncertainty and demonstrated scope | The claimed consequence exceeds the evidence |
| Reproducibility | Data provenance, configuration, code, environment, logs and artifacts | An independent reader cannot reconstruct a reported result |
| Ethics | Applicable consent, permissions, privacy, safety and disclosure | An applicable requirement is unmet or unverifiable |
| Literature grounding | Original sources, current versions and claim-to-source support | A necessary premise, attribution or research gap lacks support |

## Finding severity

- **Critical:** invalidates a central result, violates an applicable requirement, or prevents checking decisive evidence.
- **Major:** materially weakens a claim or evaluation and needs a substantive repair.
- **Minor:** a localized presentation or clarity issue that does not change the scientific conclusion.

For each finding, cite its location, explain the consequence, check surrounding evidence and propose the minimum repair. Record extraction failures and unavailable evidence as uncertainty rather than invented defects. A supported minority finding remains relevant; reviewer agreement does not establish truth.

## Optional scores

The runtime can emit four-dimension (1–6) and ScholarEval (1–10) diagnostics for compatibility. Script-derived scores measure only the checks actually executed. Novelty, significance and scientific validity require source-grounded judgment; style heuristics and issue counts cannot establish them.

If the user requests scores, explain the supporting findings, checked scope and limits for each rated dimension. Leave unassessed dimensions unknown. Do not start from a perfect scientific score merely because no script warning occurred, average away a blocker, or map a numerical threshold to acceptance at a named venue.

## Overall assessment

Separate deterministic check status, actual reviewer assessment and the responsible author's decision. State decisive repairs, the evidence needed to verify them and whether the requested review scope is complete. Follow `SKILL.md` and `CONSOLIDATION_RULES.md` when recording a verdict; screening alone is not completed review.
