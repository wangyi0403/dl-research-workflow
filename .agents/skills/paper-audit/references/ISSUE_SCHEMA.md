# Issue Schema

Canonical schema for `deep-review` findings.

```json
{
  "title": "short issue title",
  "type": "issue|suggestion",
  "quote": "exact quote from paper",
  "explanation": "reasoned explanation",
  "comment_type": "methodology|claim_accuracy|presentation|missing_information",
  "severity": "major|moderate|minor",
  "confidence": "high|medium|low",
  "source_kind": "script|llm",
  "source_section": "methods",
  "related_sections": ["results", "appendix"],
  "root_cause_key": "normalized-shared-key",
  "review_lane": "claims_vs_evidence",
  "gate_blocker": false,
  "quote_verified": true
}
```

## Required fields

- `title`
- `quote`
- `explanation`
- `comment_type`
- `severity`
- `source_kind`

## Guidance

- `type` is optional and defaults to `issue` for existing records. Use `suggestion` for an optional improvement that is not a demonstrated defect; retain `comment_type` for its subject area.
- Suggestions always have `gate_blocker: false`. Their `severity` field is retained for compatibility but does not enter issue counts, required revision roadmaps or gate decisions. Reports list them separately under Optional Suggestions.
- If an issue and a suggestion share the same deduplication key, preserve the actual issue's type, evidence and severity. A suggestion cannot weaken or inflate a demonstrated issue.
- `root_cause_key` should stay stable across re-audits when the same issue persists.
- `gate_blocker` is only for issues that should fail a submission gate.
- `quote_verified` should be added after running `verify_quotes.py`.
