# Audit Guide

Use the modes and runtime contract in `SKILL.md`. Run from the project with its existing Python and resolved Skill path.

| Requested scope | Mode | Actual completion |
|---|---|---|
| Fast source consistency screen | `quick-audit` | Executed checks and their limits |
| Scientific peer review | `deep-review` | Workspace preparation, actual review, verified findings and consolidation |
| Automated blocker check | `gate` | PASS / FAIL / UNKNOWN within the executed scope |
| Compare revised evidence | `re-audit` | Addressed, partial, unresolved and new findings |
| Prose precheck | `polish` | Diagnostic handoff to authorized writing |

`audit.py --mode deep-review` prepares evidence and prompts. It does not execute a reviewer committee or complete the scientific review. Follow `SKILL.md` to create actual findings, verify quotes, record review scope/status and render one requested view. Duplicate report views are not required.

## Read results by evidence

Inspect `check_runs` before interpreting findings. A skipped check is not a pass; an empty issue list does not establish novelty, correctness or submission readiness. Read optional scores under `SCORING_SYSTEMS.md`; do not map them to acceptance.

Gate exit codes are PASS 0, detected blockers 1 and incomplete coverage/runtime failure 2. A script PASS does not replace scientific review or the responsible author's submission decision.

PDF extraction, macro-heavy source and multi-file documents need checks against the actual manuscript. No parser provides complete mathematical verification or guaranteed section detection. Use the available format-specific tools where required and record extraction limits.

## Repair and re-audit

Prioritize verified validity, evidence, numerical consistency and reproducibility concerns. Assess severity by consequence and applicable requirements, not by the presence of a style pattern. Preserve uncertainty and negative results.

An already-authorized repair workflow may address findings. Re-audit the changed manuscript and affected evidence, using `--mode re-audit --previous-report <path>` where applicable. Compare resolved causes and coverage; an increased score alone is not evidence of a successful repair.
