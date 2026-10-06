# Consolidation Rules

Use these rules when merging lane outputs into `final_issues.json`.

## Merge when

- two findings flag the same underlying defect
- they point to the same quote or the same local text span
- fixing one root cause would resolve both findings

## Keep separate when

- the same root cause creates different paper-level consequences
- the findings require different author actions
- one finding is about methodology and the other about claim accuracy
- one uses evidence from a different section or appendix

## Priority rules

- keep the better explanation
- verify the underlying consequence before selecting severity; do not automatically retain the harsher label
- calibrate confidence to inspected evidence, not a reviewer's self-reported certainty
- preserve all related sections

## False positives

Drop a finding only if it is clearly resolved by context, convention, or parsing noise. Do not drop singleton findings just because they appear only once.
