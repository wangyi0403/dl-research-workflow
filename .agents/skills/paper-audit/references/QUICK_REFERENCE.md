# Paper Audit Quick Reference

| Mode | Purpose |
|---|---|
| `quick-audit` | Deterministic readiness screen |
| `deep-review` | Evidence-anchored reviewer judgment |
| `gate` | PASS/FAIL/UNKNOWN for executed check scope |
| `re-audit` | Compare a revision with recorded findings |
| `polish` | Diagnostic handoff before authorized editing |

Use the resolved project Skill directory and existing Python:

```text
python -B <skill-dir>/scripts/audit.py <paper> --mode quick-audit --format json
python -B <skill-dir>/scripts/audit.py <paper> --mode deep-review --focus methodology
python -B <skill-dir>/scripts/audit.py <paper> --mode gate --format json
python -B <skill-dir>/scripts/audit.py <paper> --mode re-audit --previous-report <recorded-audit>
```

For a deep review, preparation produces a workspace and prompts. Read the actual evidence, write findings, consolidate and verify quote anchors, then record completed scope and the matching input hash. Consult [the main workflow](../SKILL.md) for the exact sequence and selected rendering command.

`final_issues.json` contains consolidated findings; `review_status.json` contains completion status; `committee/consensus.md` contains the evidence-based decision. `paper/review_notes.md` is the concise project handoff. Render only the report view needed by the user. Workspace creation, a score, or exit 0 does not certify scientific quality or submission readiness.
