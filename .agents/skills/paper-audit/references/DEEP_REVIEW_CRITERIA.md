# Deep Review Criteria

Use this file when running `deep-review`. Select criteria from the manuscript's study type, stated contribution and verified venue requirements. A missing feature is an issue only when its absence undermines the actual claim or violates an applicable requirement; record non-applicable criteria without creating findings.

## What to check

1. **Formula / derivation errors**
2. **Notation inconsistency**
3. **Prose vs formal object mismatch**
4. **Numerical inconsistency**
5. **Insufficient justification**
6. **Claim accuracy / overclaim**
7. **Misleading ambiguity**
8. **Missing information / reproducibility gap**
9. **Internal contradiction**
10. **Self-consistency of standards**
11. **Table interpretability or confirmed format violations** — unclear units, misleading precision, missing uncertainty definitions, or a layout that violates the actual venue requirements. Three-line tables, rule placement and caption position are conditional formatting choices.
12. **Abstract information gaps** — the abstract does not convey the actual question, approach, supported finding or scope needed for this article type. Apply structured headings and word limits only when required by the venue; theoretical or qualitative findings need not contain a numerical result.
13. **Concept or contribution gaps** — core concepts are ambiguous, or the stated contribution is unsupported. Assess theory dialogue and theoretical increment when theoretical novelty is claimed; a supported empirical, benchmark or methodological contribution need not become a theory paper (see A5-A7 in domain_reviewer_agent.md).
14. **Qualitative methodology opacity** — the sampling rationale or analysis process is insufficient to assess the chosen qualitative approach. Evaluate saturation, coding procedures and reflexivity when relevant to that approach and claim, without requiring every qualitative practice in every study (see B6-B10 in methodology_reviewer_agent.md).
15. **Pseudo-innovation / straw man** — fabricated research gap, mischaracterized prior work, selective citation that hides overlap with existing methods (see prior_art_reviewer_agent.md)
16. **Paragraph-level argument incoherence** — logical jumps between adjacent paragraphs, causal inversions, evidence that does not support the stated claim (see C5 in critical_reviewer_agent.md)

## Editor-in-Chief screening (gate mode)

If an editorial screening pass is included in the requested review, consult `agents/editor_in_chief_agent.md` and evaluate:

- Research framing: can the intended reader identify the question and contribution from the opening material?
- Venue fit: is the paper appropriate for the target journal/conference?
- Fatal flaws: any issue that guarantees rejection regardless of technical merit?
- Presentation baseline: does the manuscript meet minimum professional standards?

A script-only `gate` run does not perform this reviewer judgment. A reviewer may identify a blocker only with the applicable requirement or evidence and its consequence; a speculative prediction of desk rejection is not itself a blocker.

## Reasoning style

For each finding:

- state what initially raised concern
- explain what context you checked
- say what remains unresolved
- keep the strongest evidence
- prefer one well-developed finding over several shallow duplicates

## What not to do

- do not report copy-editing trivia
- do not report obvious OCR glitches as author errors unless the issue survives the most charitable correction
- do not criticize a section for omitting content that clearly appears later

## Reviewer calibration

A strong paper may still have several major issues if they each threaten different conclusions. Do not over-merge distinct arguments.
