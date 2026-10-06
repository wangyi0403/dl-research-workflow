---
name: "journal-scout"
description: "Find and compare target journals after the research question and data are defined. Use for Stage 1B or explicit venue-selection requests."
---

# Journal Scout

Find, evaluate, and select target journals based on research direction, data characteristics, and publication goals.

## Process

### Phase 1: Bounded Candidate Search

Given the research direction, data characteristics, and user's domain suggestions, cast a wide net:

1. Use the available scholarly-search capability, then verify venue metadata and author guidance against official journal, publisher, or conference sources.
2. Begin with 3–5 plausible candidates. Expand only when coverage, disciplinary fit, or fallback needs remain unresolved; do not fill a quota.
3. Use journal recommendation tools only for discovery. Treat their matches as candidates, not verified fit.
4. Record impact metrics, review time, or acceptance rate only when a current authoritative source provides them; otherwise mark them unavailable instead of estimating.

**Output**: Candidate comparison table

```markdown
| # | Journal | Publisher | Current metric/source | Scope Match | Review Time/source | Acceptance Rate/source | Notes |
|---|---------|-----------|-----------------------|-------------|--------------------|------------------------|-------|
| 1 | ... | ... | ... | High/Med/Low | ... / unavailable | ... / unavailable | ... |
```

**Done when**: the comparison table contains enough verified candidates to support a defensible shortlist, with unavailable metadata stated explicitly.

### Phase 2: Discussion & Selection

Present the comparison table to the user. Discuss:
- Which journals best match the research scope?
- Which have reasonable review timelines?
- Which are realistic given the current idea maturity?

Reuse any target set already selected in the current task. Otherwise ask for the ranked target set only when it affects the work; a scope-limited discovery or local test may record no submission target.

**Done when**: User has confirmed the target set and ranking.

### Phase 3: Deep Dive

For each confirmed target journal:

1. **Author Guidelines**: Read the current official journal or publisher page using the available official-web/browser route. Extract:
   - Scope and aims
   - Page/word limits
   - Abstract structure requirements
   - Figure/table specifications
   - Reference format
   - Any special requirements (data availability, ethics, etc.)

2. **Recent Papers Scan** (abstract level — deep reading happens in 1C):
   - Search for papers similar to the research direction, published in the last 2 years
   - Confirm this journal actually publishes this type of work
   - Note common methodological standards and baseline choices

3. **Journal Intelligence Card** for each confirmed target:

```yaml
journal: [Name]
publisher: [Publisher]
scope_match: [How well the research fits]
author_guidelines_summary: [Key formatting rules]
recent_relevant_papers: [Count + example titles]
suggested_ranking: 1st/2nd/3rd choice
```

**Done when**: each confirmed target has an intelligence card with current guidance, recent-paper evidence, and ranking.

### Phase 4: Final Output

Consolidate into `docs/02_journal_scouting.md`:

1. Candidate comparison table (bounded set, expanded only when justified)
2. Ranked target-journal intelligence cards
3. Final recommendation: primary venue and any justified backups
4. Key formatting requirements for the primary target

**Done when**: `docs/02_journal_scouting.md` records the relevant candidates, one card per actual selected target, verified requirements and unresolved choices. Do not invent three cards or recommend submission when the study lacks a suitable contribution.

## References

| File | Open when |
|------|-----------|
| `references/venue-routing.md` | BEFORE starting the scout. Classify your manuscript type and match to journal categories. Quick-elimination heuristics. |
| `references/domain-journal-profiles.md` | Understanding journal archetypes and common rejection patterns in civil/transport engineering + AI. |
| `references/journal-card-template.md` | Phase 3 deep dive. Fill one card per target journal. |
