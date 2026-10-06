# Optional ScholarEval Diagnostics

Enable with `--scholar-eval` only when useful for the requested review. The output schema contains soundness, clarity, presentation, novelty, significance, reproducibility, ethics, literature grounding and overall fields. Some values are computed from script findings, some require supplied reviewer assessments, and unavailable dimensions remain unknown.

Use `quality_rubrics.md` for the evidence needed to assess each dimension. Script deductions are a diagnostic convention; they do not measure scientific validity, predict acceptance or replace actual review. The aggregate depends on which fields are available and must be reported with that coverage.

## Reviewer input

When `--llm-json` is requested, provide genuinely assessed entries in the supported shape:

```json
{
  "novelty": {"score": 7.0, "evidence": "Specify verified prior work, the actual difference, and its scope."},
  "significance": {"score": 6.0, "evidence": "Specify supported effect size, uncertainty, and demonstrated use."}
}
```

These values illustrate the schema only. Do not reuse example values as manuscript assessments, infer scientific quality from writing style, or force scores for unreviewed dimensions.

Online `--literature-search` is optional. Use only an available authorized route, retain verified identifiers and inspect source support. Missing online access is an explicit coverage limit, not a fabricated literature score. See `LITERATURE_GROUNDING_GUIDE.md` for source-checking details, subject to the evidence and authorization rules in `SKILL.md`.
