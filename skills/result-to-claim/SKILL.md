---
name: result-to-claim
description: Use when experiments complete to judge what claims the results support, what they don't, and what evidence is still missing. Agent self-review evaluates results against intended claims and routes to next action (pivot, supplement, or confirm). Use after experiments finish — before writing the paper or running ablations.
argument-hint: [experiment-description-or-wandb-run]
allowed-tools: Bash(*), Read, Grep, Glob, Write, Edit, Agent
---

# Result-to-Claim Gate

Experiments produce numbers; this gate decides what those numbers *mean*. Collect results from available sources, get an Agent self-review judgment, then auto-route based on the verdict.

## Context: $ARGUMENTS

## When to Use

- After a set of experiments completes (main results, not just sanity checks)
- Before committing to claims in a paper or review response
- When results are ambiguous and you need an objective second opinion

## Workflow

### Step 1: Collect Results

Gather experiment data from whatever sources are available in the project:

1. **W&B** (preferred): `wandb.Api().run("<entity>/<project>/<run_id>").history()` — metrics, training curves, comparisons
2. **docs/07_result_record.md**: full results table with baselines and verdicts (逐条实验数值记录)
3. **docs/06_experiment_tracker.md**: check which experiments are DONE vs still running
4. **Log files**: `ssh server "tail -100 /path/to/training.log"` if no other source
5. **docs/05_experiment_plan.md**: intended claims and experiment design

Assemble the key information:
- What experiments were run (method, dataset, config)
- Main metrics and baseline comparisons (deltas)
- The intended claim these experiments were designed to test
- Any known confounds or caveats

### Step 2: Self-Review Judgment

Use the **Agent tool** to spawn a critic sub-agent for objective evaluation:

```
Agent prompt:
  You are a rigorous ML research evaluator. Your job is to judge whether
  experimental results actually support the intended claim. Be conservative
  and honest — do not inflate claims beyond what the data shows.

  RESULT-TO-CLAIM EVALUATION

  Intended claim: [the claim these experiments test]

  Experiments run:
  [list experiments with method, dataset, metrics]

  Results:
  [paste key numbers, comparison deltas, significance]

  Baselines:
  [baseline numbers and sources — reproduced or from paper]

  Known caveats:
  [any confounding factors, limited datasets, missing comparisons]

  Please evaluate and respond with:
  1. claim_supported: yes | partial | no
  2. what_results_support: what the data actually shows
  3. what_results_dont_support: where the data falls short of the claim
  4. missing_evidence: specific evidence gaps
  5. suggested_claim_revision: if the claim should be strengthened, weakened, or reframed
  6. next_experiments_needed: specific experiments to fill gaps (if any)
  7. confidence: high | medium | low

  Be honest. A single positive result on one dataset does not support a general claim.
```

### Step 3: Parse and Normalize

Extract structured fields from Agent response:

```markdown
- claim_supported: yes | partial | no
- what_results_support: "..."
- what_results_dont_support: "..."
- missing_evidence: "..."
- suggested_claim_revision: "..."
- next_experiments_needed: "..."
- confidence: high | medium | low
```

### Step 4: Route Based on Verdict

#### `no` — Claim not supported

1. Record postmortem in docs/08_findings.md (Research Findings section):
   - What was tested, what failed, hypotheses for why
   - Constraints for future attempts (what NOT to try again)
2. Update CLAUDE.md Pipeline Status
3. Decide whether to pivot to next idea from docs/idea_candidates.md or try an alternative approach

#### `partial` — Claim partially supported

1. Update the working claim to reflect what IS supported
2. Write partially-confirmed claims to `docs/09_claims.md` (mark confidence as "partial")
3. Record the gap in docs/08_findings.md
4. Design and run supplementary experiments to fill evidence gaps
5. Re-run result-to-claim after supplementary experiments complete
6. **Multiple rounds of `partial` on the same claim** → record analysis in docs/08_findings.md, consider whether to narrow the claim scope or switch ideas

#### `yes` — Claim supported

1. Write confirmed claims to `docs/09_claims.md` in structured format:
   ```markdown
   # Confirmed Claims
   | Claim ID | Statement | Supporting Evidence | Confidence |
   |----------|-----------|-------------------|------------|
   | C1 | ... | Block B1 result: ... | high |
   ```
2. Record summary in docs/08_findings.md
3. If ablation studies are incomplete → trigger `/ablation-planner`
4. If all evidence is in → ready for paper writing

## Rules

- **The Agent critic is the judge, not the main CC session.** CC collects evidence and routes; the Agent sub-agent evaluates. This prevents post-hoc rationalization.
- Do not inflate claims beyond what the data supports. If the Agent says "partial", do not round up to "yes".
- A single positive result on one dataset does not support a general claim. Be honest about scope.
- If `confidence` is low, treat the judgment as inconclusive and add experiments rather than committing to a claim.
- If Agent tool fails (call fails), CC makes its own judgment and marks it `[pending Agent review]` — do not block the pipeline.
- Always record the verdict and reasoning in docs/08_findings.md, regardless of outcome.
