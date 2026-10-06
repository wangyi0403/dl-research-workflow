---
name: "academic-humanizer"
description: "Polish scholarly prose for clarity, evidence-aligned claims, calibrated limitations, and venue voice. Use for Stage 4 language review; do not optimize for AI detectors."
---

# Academic Humanizer

Improve academic clarity and voice while preserving scholarly precision. Every empirical claim needs an appropriate evidence pointer or an explicit unresolved status. No verb should imply stronger evidence than the study provides. An AI-writing tell is a contextual diagnostic signal, not proof of authorship: do not change a passage unless the pattern creates vagueness, repetition, inflated emphasis, awkward reader modeling, or a mismatch with the author's or venue's voice.

## Core Principle

There is no single correct academic voice. Match the author's established usage, discipline, article type, and current venue guidance while keeping claims precise and traceable. Stock phrasing is a diagnostic signal, not proof of AI authorship and not an automatic deletion rule.

## Process

```
Read → Audit internally (don't edit yet) → Rewrite → Verify → Return
```

1. **Read**: the manuscript and any author writing sample. Note the document type, language, venue, and whether the text is a paper, report, teaching explanation, or dialogue.
2. **Audit**: do not edit yet. Internally list each detected pattern with location, context, and one of four decisions: keep, revise, remove, or author decision. List each empirical claim's evidence status. Expose this audit only when the user requests it or a material evidence risk needs explanation.
3. **Rewrite**: preserve the manuscript's macro-structure, propositions, evidence, and scope; sentence-level edits may merge or split sentences when claim–citation coverage remains clear. Revise only confirmed tells, match over-claims to evidence, and keep legitimate hedging. Every edit must have a stated reason; if no rule or evidence supports it, leave the text unchanged.
4. **Verify**: check protected elements, information preservation, claim strength, paragraph/heading structure, citation coverage, and whether the revision introduced a new voice, detail, limitation, or explanation.
5. **Report**: return the cleaned text by default. Add a concise change note only when requested or needed to surface evidence risk; do not force a full diagnostic report or per-sentence narration.

For defensive writing, read `references/defensive-writing.md`. Recover the author's intended supported judgment before editing; calibrate the proposition rather than adding caveats to an inflated version. Check underclaiming as well as overclaiming, and reread the paragraph so that its scientific purpose still completes.

## Layer 1: General AI-Tell Catalog

Scan for these potential symptoms, subject to Layer 3 academic exceptions. Change them only when they create vagueness, repetition, inflated emphasis, or poor flow in context:

- **Inflated significance**: "marking a pivotal moment", "groundbreaking", "revolutionary"
- **Superficial -ing tails**: "..., highlighting the importance of..."
- **Promotional/figurative language**: "rich", "vibrant", "robust" (as filler, not technical term)
- **Vague attributions**: "experts argue" with no citation
- **Stock vocabulary used as filler**: words such as delve, underscore, intricate, pivotal, showcase, leverage, seamless, crucial, notably, or moreover are not banned; replace or remove them only when they add no precise meaning
- **Copula avoidance**: "serves as" → "is", "functions as" → "acts as"
- **Negative parallelisms**: "not just X, but Y"
- **Rule-of-three padding**: forced triads that add no information
- **Elegant variation**: cycling synonyms for one referent (pick one term, stick to it)
- **Filler phrases**: "it is worth noting that", "in order to", "it should be emphasized that"
- **Clause-stacked sentences**: split when the logical relationships or referents become hard to follow; do not use a fixed clause count
- **Em-dashes**: review repetitive, reveal-style, or unnecessary parenthetical use; do not remove an em dash merely because it is an em dash. Follow the confirmed venue and author style.

When the manuscript contains Chinese prose, read [the Chinese structural and discourse catalog](references/ai-tell-catalog.md) before editing. It covers canned reversal contrasts, dense ideographic-comma enumeration, reveal-style em dashes, empty lead-in colons, repeated adjacent sentence skeletons, numbered-heading templates, idealized occupational metaphors, paragraph-open comments without a referent, slogan-like openers, defensive report scaffolding, and unprompted question-and-answer or self-explanation. These are contextual signals, not automatic deletions.

**Done when**: Every relevant general AI-tell candidate is internally classified; only material edits or evidence risks need to be reported.

## Layer 2: Academic-Specific AI Tells

- Template openers: "In recent years, ... has attracted increasing attention"
- Vague gap statements: "However, existing methods still face challenges"
- Over-summarizing section closers: "In summary, this paper has demonstrated..."
- Hollow forward-looking: "Future work will explore..."
- Unprompted reader-question shells: "What does this mean? The answer is..." or "You may ask..." when no real question, dialogue, or teaching need exists
- Defensive report framing: stacked "it is important to note", "strictly speaking", "it should be emphasized", or similar caveats that do not change the claim's scope or interpretation
- Empty process narration: "the following section will discuss..." when it repeats the visible structure rather than helping navigation

**Done when**: All academic-specific tells (template openers, vague gaps, over-summarizing closers, hollow forward-looking, unprompted question shells, defensive report framing, and empty process narration) are identified and internally classified.

## Layer 3: Academic Exceptions — What NOT to Touch

**Never modify**:
- **Field-specific terminology**: even if it looks like AI vocabulary, if it's the standard term in the field, keep it
- **Mathematical notation, equations, variable names**
- **Citation markers** (`\cite{...}`)
- **Figure/table references** (`\ref{...}`)
- **Legitimate uncertainty**: preserve the meaning and strength of warranted "may", "suggest", "potentially", or "appears to"; duplicated wording may be compressed without changing uncertainty
- **LaTeX commands and environments**
- **Numbers, results, data values** — never change a number
- **Section titles** (`\section{...}`)
- **Legitimate punctuation and structure** — preserve em dashes, Chinese enumeration, colons, numbered headings, questions, and roadmaps when they encode a real relation, complete a required list, match the author's voice, or serve the venue
- **Genuine limitations and scope conditions** — do not delete a caveat merely because it sounds defensive; retain the condition and its effect on interpretation

**Done when**: All protected elements confirmed untouched: terminology, math, citations, refs, hedging, LaTeX commands, numbers, section titles.

## Layer 4: Claim-Evidence Discipline

For every empirical claim in the manuscript:

1. **Is it backed?** — number, figure, table, or citation in the immediate context?
2. **Does the verb match the evidence?**
   - "prove" is appropriate only for a valid formal proof or a context with an explicitly justified proof standard
   - "demonstrate" / "show" require direct, reproducible support under the stated design; statistical significance alone is neither necessary nor sufficient in every study
   - "indicate" / "suggest" fit partial, indirect, uncertain, or exploratory evidence
   - "may" / "might" fit hypotheses, bounded possibilities, or uncertainty when the sentence states the relevant conditions

3. **Marking**:
   - 🟠 Orange: claim has some evidence but verb is too strong → soften
   - 🔴 Red: supplied materials establish no support for an empirical claim → flag for author, suggest adding evidence or removing claim
   - Support not yet inspected: record a verification gap; do not classify the claim as unsupported merely because the check is pending
   - Supported claim weakened by editorial caution: restore the evidence-calibrated statement without expanding its scope

Never invent evidence. Never change a number to make a claim stronger.

Also inspect unwarranted underclaiming: remove editorial self-doubt when the supplied evidence and accepted author position support a direct statement, without raising scientific strength. Do not weaken an author-supplied interpretation just because its cited support has not yet been checked; flag that verification gap outside the prose when necessary.

**Done when**: Every empirical claim has an evidence status and matching scientific strength; supported claims are kept or restored, actual overclaims are narrowed, and missing support is distinguished from pending verification.

## Layer 4A: Calibrated Limitations — Neither Self-Defeat nor Spin

Audit every limitation, caveat, and future-work sentence for its evidence status and rhetorical effect.

- **Remove unsupported self-defeat**: do not retain blanket statements that the study, data, model, or results are meaningless, unreliable, or unusable when the manuscript's evidence does not establish that conclusion.
- **Preserve real boundaries**: retain limitations supported by the study design or evidence, including sample/site coverage, data quality, label uncertainty, untested operating conditions, causal limits, and missing comparisons.
- **Compress defensive scaffolding**: delete or merge only semantically redundant caveat markers. Retain independent conditions even when they appear close together, and integrate each condition next to the claim it limits. Do not turn a valid limitation into a confident claim, and do not remove uncertainty simply to make the prose sound decisive.
- **Write the complete unit when the manuscript supplies it**: retain the observed constraint and its stated effect on the claim. A missing next validation is not itself a scientific defect; include one only when supplied or requested. Flag a missing effect only when it prevents a meaningful limitation statement. Do not invent a next study or turn a limitation into promotional future work.
- **Separate evidence types**: an engineering task improvement does not by itself prove a physical mechanism, causal explanation, or cross-domain generalization. Keep these scopes distinct.
- **Protect scientific hedging**: words such as “may,” “suggest,” and “under the evaluated conditions” are retained when they accurately reflect the evidence; do not remove them merely to sound confident.

**Done when**: Each material limitation retains its evidence and claim impact; optional next verification is supported; no rewrite hides a real boundary, adds an unsupported disclaimer, or leaves the paragraph unable to establish its intended judgment.

## Layer 4B: Reader Model and Discourse Stance

Treat these as discourse decisions rather than word substitutions:

- **Unprompted question-and-answer**: if the text invents a reader question and immediately answers it, remove the question shell and state the supported point directly. Keep genuine research questions, dialogue, FAQ material, and explanations needed by the intended audience.
- **Redundant self-explanation**: "this means", "this shows", "in other words", or their Chinese equivalents are candidates only when they merely repeat the previous sentence. Keep them when they add a nontrivial inference, scope condition, or interpretation.
- **Report-like throat clearing**: retain a concise roadmap when the venue benefits from navigation; remove or compress generic announcements that simply restate the headings or promise a "detailed discussion" without content.
- **Over-defensive tone**: do not pile up disclaimers, appeals to rigor, or self-protective qualifiers. Preserve the one that changes interpretation, and flag the rest for removal or author choice.

**Done when**: the prose addresses the actual reader and genre, not an invented questioner; explanations add information; caveats are calibrated; and no revision has added a personal stance, example, or detail that the author did not supply.

## Layer 5: Voice and Venue Matching

If the author supplies prior accepted papers:
- Read a sample first
- Note: sentence rhythm, connective habits, hedging level and placement, section openers, notation conventions, recurring phrasings
- Match them in the rewrite

Use actual recent papers and official venue guidance to infer register; do not rely on publisher-wide or conference-wide stereotypes. Absent a reliable sample, default to clean, precise prose and report the uncertainty rather than inventing a house voice.

**Done when**: Writing style matches the author's prior work or venue register; the internal audit or requested concise note records material voice-matching decisions.

## Output

After processing, produce:
1. Rewritten manuscript (macro-structure and information preserved)
2. If the user requested an audit or a material evidence risk was found, add a concise change note:
   - If an audit was requested: patterns kept/revised/removed, with only material locations
   - Claims softened or given evidence pointers
   - 🟠/🔴 flagged claims with recommendations
   - Limitations retained, narrowed, or flagged with evidence and claim impact
   - Voice notes (what was matched, what was defaulted)

## References

| File | Open when |
|------|-----------|
| `references/ai-tell-catalog.md` | Context-sensitive catalog: general tells, Chinese structural/discourse signals, narrow translationese screen, academic patterns, and protected exceptions. Read for Chinese prose or a focused de-AI review. |
| `references/before-after-examples.md` | Concrete examples of AI text → humanized text. Full paragraph transformations. |
| `references/voice-matching.md` | Matching author voice from prior papers or venue register. 6 dimensions + venue-specific profiles. |
| `references/defensive-writing.md` | Repair assert-then-retract structure, unsupported self-weakening and redundant caveats while preserving author intent and scientific boundaries. |
