# Paper Audit Troubleshooting

| Observed problem | Next action |
|---|---|
| Missing or ambiguous manuscript | Locate the authoritative project file and requested scope; clarify only when they cannot be inferred |
| A script fails | Record the command, exit code and relevant error; diagnose locally before an evidence-based retry |
| Parser or English check unavailable | Check the installed project support at `.agenthub/runtime/latex-paper-en/scripts/`; use the supported installed sibling path when present; report skipped checks explicitly |
| PDF, scan, macro or multi-file extraction is incomplete | Compare extracted content with the source/rendered PDF; narrow the reviewed coverage or use the relevant format workflow |
| A venue preset does not fit | Use current official instructions and the user's rubric; a stored preset is not proof of an applicable requirement |
| Online literature access fails or is rate limited | Reuse verified local sources or currently available research tools; distinguish access failure from absence of evidence; do not create credentials or install another service automatically |
| A numerical or model-based score is unavailable | Perform the relevant evidence judgment directly; an unavailable score is neither a pass nor a scientific defect |
| Re-audit lacks a valid input baseline | Locate the prior recorded findings and version; do not manufacture a resolved state from prose similarities |
| Rendered report disagrees with findings | Verify `final_issues.json` and the input hash, then regenerate the requested view; exported reports are snapshots |

Tool or extraction failure limits the affected path. Continue independent checks, preserve actual completion status and state the exact missing coverage.
