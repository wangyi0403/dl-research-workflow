# Pre-Registration Protocol for Hypothesis Testing

> Use BEFORE running experiments that test a predictive claim.
> Pre-registration prevents HARKing (Hypothesizing After Results are Known).

## When to Pre-Register

Pre-register when:
- You have a **predictive claim** tested on a NEW dataset (not the one that generated the hypothesis)
- A reviewer might ask "did you come up with this explanation after seeing the results?"
- The claim is stronger if you can say "we predicted this before running the experiment"

Don't pre-register for:
- Standard ablation studies (removing your own modules)
- Main comparison experiments (Proposed vs Baselines)
- Hypotheses already tested on the data that generated them

## Hypothesis Chain Template

Build hypotheses as a derivation chain. Each H depends on prior H being correct:

```
H1 (baseline condition) + H2 (method performance) → H3 (derived gap) → H4 (main predicted effect)
```

### H1 — Baseline Condition

**Prediction**: [Variable] expected in range **[min, max]**.
**Justification**: Based on [prior data / theory / calibration from similar domains].
**Point estimate**: **[value]** ± [uncertainty].
**Falsification check**: If outside range → this dataset is not a valid test bed for H4.

### H2-H3 — Intermediate Derivations

Chain from H1 to the headline hypothesis. Each step must be falsifiable independently.

### H4 — HEADLINE FALSIFICATION TEST

**Prediction**: [Main effect] ∈ **[lower, upper]**.
**Point estimate**: **[value]**.

**Pre-define ALL four outcomes**:
- **Confirmed**: Effect in predicted window → claim strengthened
- **Partial**: Effect positive but outside window → report deviation + identify moderating variables
- **Falsified**: Effect ≤ 0 or trivial → revise claim to descriptive-only; do NOT re-fit
- **Invalid test**: Pre-condition (H1) not met → report as untested regime

## Experiment Protocol (Binding)

1. **Hardware/software**: exactly as reference experiments
2. **Hyperparameters**: identical to the configuration that generated the hypothesis
3. **Pipeline**: documented step-by-step before execution
4. **Reporting**: pre-fill result table upon completion; no selective reporting
5. **Blind**: no tuning after seeing partial results
6. **Timestamp**: record git commit hash at experiment start

## Post-Experiment Outcome Handling

Define the response for each scenario BEFORE running:

### Scenario A: Confirmed
Claim promoted from "post-hoc observation" to "predictively tested." Pre-registration cited as evidence of honest inference.

### Scenario B: Partially Confirmed
Report deviation magnitude honestly. Identify candidate moderating variables (data scale, domain difficulty, class cardinality, training size). Weaken confidence language accordingly.

### Scenario C: Falsified
**Revise the claim.** Do NOT search for a new functional form that fits (that's HARKing). Pivot to: what WAS confirmed? What CAN you still claim honestly? The falsified prediction itself is publishable — it's honest science.

### Scenario D: Invalid Test
Report as untested regime. Do not claim or revise based on this data. Seek alternative test bed if the question remains important.

## Deviation Report

Required disclosure when any hypothesis is falsified:
1. Original pre-registered windows (verbatim, timestamped)
2. Realized values (verbatim)
3. Falsification verdict per hypothesis
4. Framing revision rationale
5. **Withdrawn claims** — explicit list
6. **New claims** — with appropriately weaker confidence language

## Key Principle

**Better to pre-register and be wrong than to post-hoc rationalize.**
A falsified pre-registered prediction is honest, publishable science.
A post-hoc "we found what we expected" is HARKing.
