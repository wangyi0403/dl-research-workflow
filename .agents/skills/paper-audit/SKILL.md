---
name: "paper-audit"
description: "Review complete or revised academic manuscripts for scientific, methodological, citation, numerical, and presentation issues. Use for peer-review or readiness audits, not direct editing or compilation."
---

# Paper Audit

Review an existing manuscript against its intended contribution, evidence and confirmed venue. Keep deterministic screening, reviewer judgment and author decisions distinct. This Skill audits; an already-authorized editing workflow handles repairs without silently changing source evidence.

## Modes

| Intent | Mode | Result |
|---|---|---|
| Fast integrity/readiness screen | `quick-audit` | Script findings and explicit check-execution status |
| Reviewer-style critique | `deep-review` | Prepared evidence workspace, reviewer findings and revision priorities |
| Automated blocker check | `gate` | PASS/FAIL/UNKNOWN for the script/checklist scope; scientific and author decisions remain separate |
| Compare a revision with prior findings | `re-audit` | Addressed, partial, unresolved and new issues |
| Precheck before prose work | `polish` | Diagnostic handoff; no manuscript rewrite |

Aliases `self-check` and `review` map to `quick-audit` and `deep-review`. Use the user's language for review text; preserve manuscript quotes verbatim. For a narrow requested dimension, choose `--focus editor|theory|literature|methodology|logic`; otherwise review the material risks across the manuscript.

## Runtime and invocation

Use the existing project Python, normally `python -B`, with the resolved Skill directory; do not require `uv` or install a new environment merely to run checks.

```text
python -B <skill-dir>/scripts/audit.py <paper> --mode quick-audit --format json --output <local-result.json>
python -B <skill-dir>/scripts/audit.py <paper> --mode deep-review --focus methodology
python -B <skill-dir>/scripts/audit.py <paper> --mode gate --format json
python -B <skill-dir>/scripts/audit.py <paper> --mode re-audit --previous-report <prior-result>
```

AgentHub installation resolves this Skill's parser and English checks into `.agenthub/runtime/latex-paper-en/scripts/`. The support bundle is not a discoverable Skill. An installed sibling `latex-paper-en` is also a supported resolver path. Missing format-specific checks are recorded as `skipped`, not passed. Do not search or alter global Skill directories.

Exit 0 means the requested script completed without detected blockers, not scientific acceptance. In gate mode the exit code agrees with PASS (0), FAIL (1), or incomplete checks (2). Runtime failures return 2; they must not be described as clean checks. `check_runs` preserves coverage. Offline bibliography checks resolve actual `.bib` files, includes or inline bibliographies; they do not verify that an original source supports a scientific claim. Use `citation-verification` for that task.

Online bibliography/literature flags are optional and require the current authorized external scope. Never fabricate sources or use an unavailable third-party model.

## Deep review

Read `references/REVIEW_CRITERIA.md`, `DEEP_REVIEW_CRITERIA.md`, `CONSOLIDATION_RULES.md` and `ISSUE_SCHEMA.md`. Consult `CHECKLIST.md` only for applicable requirements; historical venue presets and generic style preferences are not current mandatory rules.

1. **Prepare and screen.** Run `audit.py --mode deep-review`. It prepares `paper/review_workspace/<slug>/`, checks the source and writes deterministic suggestions to `screening/` and `review_prompts.json`. These are review prompts, not confirmed defects or LLM findings. `review_status.json` remains `review_required`; the script does not invent a committee or acceptance score.
2. **Review the evidence.** Select independent local perspectives for the actual uncertainty. The reviewer receives the manuscript, relevant raw artifacts and rubric, not a desired conclusion or another reviewer's answer. A focused review need not instantiate five roles. Use `agents/committee_*_agent.md` or the relevant section/cross-cutting reviewer reference. Delegate when available and appropriate; otherwise record an inline reviewer pass honestly. A deterministic fallback never substitutes for this step.
3. **Write actual findings.** Store reviewer issue arrays in `comments/` and role reasoning in `committee/`. Anchor each finding to an exact quote/section and explain the unresolved consequence after checking surrounding context. Distinguish `[Script]` and `[LLM]`; do not create an issue merely because a keyword, number or negated novelty statement appears.
4. **Consolidate and verify.** Run the following tools on the same review directory:

```text
python -B <skill-dir>/scripts/consolidate_review_findings.py <review-dir>
python -B <skill-dir>/scripts/verify_quotes.py <review-dir> --write-back
```

Merge common root causes, preserve distinct consequences and supported minority findings, and mark unverified quotes explicitly. After the selected review scope has actually been completed, record `status: reviewed`, the matching `input_sha256` from `metadata.json`, reviewer identity/scope and remaining limits in `review_status.json`. Record any evidence-based overall decision in `committee/consensus.md` as `Editor Verdict: ...`; do not derive it from a fixed penalty formula or a count of issues. After recording the decision, render only the requested view with `render_deep_review_report.py <review-dir> --style deep-review|peer-review --output <path>`. Omit rendering when the structured findings and concise handoff suffice.
5. **Hand off.** Consolidate decision-ready issues in `paper/review_notes.md`; keep detailed working material in the review workspace. State the minimum causal repairs, unresolved author/venue decisions and the permitted next step. Re-audit affected evidence after revisions.

Repeated preparation of identical inputs reuses the workspace and preserves reviews. Changed manuscript/include/bibliography/figure inputs create a new versioned workspace; do not erase an earlier review or carry its PASS forward. Check extraction against the real source or rendered PDF, especially for multi-file, macro-heavy and scanned documents; workspace existence does not prove complete extraction.

## Judgment rules

- Prioritize validity, evidence, numerical consistency, evaluation fairness and reproducibility over copy-editing trivia.
- Recover the intended contribution and test its actual scope. Check unsupported strengthening and unsupported self-weakening separately; an uninspected source is a verification gap, not a demonstrated defect. Verify surrounding context and non-prose evidence before confirming a criticism.
- Match severity to the affected scientific judgment and identify the minimum causal repair. An explanation problem, unfair comparison, missing evidence and actual protocol defect require different repairs; more defensive prose cannot resolve an evidence defect.
- A quote match only verifies presence, not correctness of a finding. Resolve negation, cross-section answers and extraction noise before raising an issue.
- Do not force theory novelty, causal interpretation, universal abstract structures, citation quotas or new ablations onto an incompatible study type.
- Preserve failed/null results and real limitations. No score may override an evidence-backed blocker or unknown.
- Respect existing authorization for repairs; manuscript review does not itself authorize external submission or declarations on behalf of authors.

## Output and references

`final_issues.json` is the authoritative consolidated finding set; `comments/` preserves reviewer inputs, `review_status.json` records completion, and `committee/consensus.md` records actual judgment. Use `audit.py --report-style ... --output ...` for one immediate report, or the workspace renderer after reviewer findings are consolidated. Roadmaps derive from current findings during rendering. Exported reports are snapshots and must be explicitly regenerated after findings change; never read them back as current findings. Return only the concise findings needed by the user's request.

For full lane coverage, read `references/REVIEW_LANE_GUIDE.md` and `SUBAGENT_TEMPLATES.md`. For re-audit comparison, use `scripts/diff_review_issues.py`; for an explicit response-to-reviewers task consult `references/cover_letter_and_rebuttal.md`. Never label a screening-only result as a completed deep review.
