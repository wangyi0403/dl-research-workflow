---
name: "cover-letter"
description: "Prepare a journal submission cover letter when requested or during Stage 6."
---

# Cover Letter

Generate a submission cover letter tailored to the target journal and manuscript contributions.

## Input

- `paper/main.tex` — the manuscript (for key contributions and results)
- `docs/02_journal_scouting.md` — target journal scope, recent papers, editor expectations
- `docs/03_idea_report.md` — core contributions and novelty

## Typical structure

Use the target journal's current requirements when they exist. The following sequence is a compact default, not a mandatory paragraph count.

### P1: Submission Statement
One sentence: what you are submitting, the title, and to which journal.

**Done when**: Submission statement written in one sentence specifying title, manuscript type, and target journal.

### P2: Problem + Context
What real problem does this work solve? Why does it matter now? Use concrete, verified context; include scale or numbers only when the source supports them. Keep it tight — this is a cover letter, not the introduction.

**Done when**: The problem and relevance are stated concisely using supported facts; no number is invented to fill a template.

### P3: Scientific Question + Gap
What fundamental obstacle makes this problem unsolved? State the research question. If possible, abstract it beyond the specific domain to show why the answer matters to readers outside your subfield.

**Done when**: Research question stated with gap identified; significance articulated beyond the specific domain.

### P4: Contributions (with Evidence)
Present only the manuscript's verified contribution set. Number contributions when that improves readability. Each one:
- Has a **name**, not "Module A"
- States the **mechanism** or **finding**, not just the module name
- Includes a **number** when available
- Is verifiable from the manuscript

Pattern:
> 1. **[Finding/Insight name]**. [One sentence describing what was discovered and how]. [Evidence: N samples, metric = value].
> 2. **[Method/System name]**. [One sentence on what it does and why it's transferable].
> 3. **[Capability/Impact name]**. [One sentence on what this enables that couldn't be done before].

**Done when**: every stated contribution matches the manuscript, has the appropriate evidence, and no extra contribution was invented for the letter.

### P5: Fit with Journal (Specific, Not Generic)
Don't say "this fits the scope of your journal." Show it:
- When verified and genuinely relevant, reference specific recent work from this journal; do not add token citations merely to flatter the venue.
- Name the sub-area or theme within the journal's scope that this work extends
- Close the loop: how does this work advance the conversation already happening in this journal?

**Done when**: the journal-fit paragraph names the relevant scope or conversation and uses only verified, genuinely relevant examples when needed.

### P6: Declarations
- Original, not published elsewhere, not under consideration
- All authors approved
- No competing interests (or declare them)
- Any AI usage disclosure if required

**Done when**: Each required declaration has a recorded author/policy source. Never infer originality, non-simultaneous submission, author approval or absence of competing interests. Mark unconfirmed items in a review draft and block the final letter until resolved; reuse existing confirmations when still applicable.

## Rules

1. Follow the journal's stated length and format; absent a rule, keep the letter concise and normally near one page.
2. Address the appropriate editor by name only when the current role and spelling have been verified; otherwise use a neutral editorial salutation.
3. **Every claim in the CL must match the manuscript.** No exaggeration in the CL that the paper can't back up.
4. **Don't summarize the paper.** State the contribution and its significance. The editor will read the abstract for summary.
5. **Make journal fit specific and evidence-based.** Avoid generic praise or unsupported assumptions about editorial preference.
6. **Match contribution count to the paper.** If the paper has 3 contributions, the CL has 3. Don't invent extra ones for the CL.

## References

| File | Open when |
|------|-----------|
| `references/cover-letter-patterns.md` | Writing the cover letter. 5-paragraph structure, common mistakes, length guidelines. |

## Output

Use the target journal's confirmed format and the project's existing toolchain. For a LaTeX deliverable, `paper/cover_letter.tex` with the standard `letter` class is a suitable default; compile with the existing compatible engine and inspect the output. If the journal requires plain text or another document format, prepare that format directly. Do not introduce a LaTeX or engine dependency solely to produce a cover letter.
