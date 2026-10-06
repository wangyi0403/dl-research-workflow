# Scientific Narrative Construction

> How to build a paper narrative that distinguishes "engineering problem" from "scientific question."
> Generic pattern — adapt to your domain, data, and contribution type.

## The 6-Layer Narrative Pyramid

Bottom (concrete) → Top (abstract). Each layer justifies the one above it.

```
Layer 6: Dual Validation (engineering impact + scientific knowledge)
Layer 5: Implementation (evidence vehicle, NOT the contribution itself)
Layer 4: New Understanding (C1 = insight, C2 = recipe, C3 = capability)
Layer 3: Macro Scientific Question (generalizable beyond your domain)
Layer 2: Why Worth Studying (engineering infeasibility + research gap)
Layer 1: On-Site Engineering Problem (real, scaled, consequential)
```

## Layer-by-Layer

### Layer 1: Engineering Problem

**What**: The real-world problem. Ground the paper in something that actually happens.

**Rules**:
- MUST be real (not "consider a scenario where...")
- MUST have scale (numbers: volume, frequency, cost)
- MUST have consequence (what breaks if unsolved)
- Use concrete context, not generic domain description

❌ "[Domain] inspection is important for safety."
✅ "A single [system] generates [N] data points per cycle. [Failure mode X] (~[Y]% of cases) triggers cascading failures in [downstream components]. Resources are finite — wrong prioritization means missed interventions."

### Layer 2: Why Worth Studying

**What**: Prove this is NOT "AI looking for a problem to solve."

**Part A — Engineering infeasibility**: Why can't current practice handle it?
- Missing instrumentation (no per-point sensors)
- Physics/modeling too expensive at operational scale
- Labels scarce or expensive (give numbers: N labeled out of M total)
- Existing automation misses the decision-relevant pattern

**Part B — Research gap**: What hasn't been FORMULATED yet?
- State as a question, not a statement
- Abstract from the specific domain: "Can [observable signal X] support [decision Y] when [driver Z] is unobservable?"
- This is a RESEARCH question, not an engineering specification

**Golden rule**: If you can't name BOTH infeasibility AND a gap, the paper reads as "we applied [technique] to [domain]."

### Layer 3: Macro Scientific Question

**What**: The question abstracted from your domain. Someone in a different field should understand it.

**Rule**: Strip all domain vocabulary. If the question only makes sense in your specific subfield, you haven't abstracted far enough.

❌ "How to detect [domain-specific object] from [domain-specific sensor]?"
✅ "When the [causal driver] of [phenomenon] is unobservable in the available modality, how can [observable proxy patterns] support reliable [decision type]?"

**Test**: Can a researcher in a related but different field understand the question without knowing your domain's specifics?

### Layer 4: New Understanding — Insight-First Contributions

**What**: What the reader can CITE, not what you BUILT.

**C1 = Insight / New Understanding** (most important, most citable)
- What did you LEARN that wasn't known before?
- Must be falsifiable — someone could test it on their own data
- Must be specific enough to cite, general enough to transfer
- ❌ "Our method achieves X% accuracy"
- ✅ "[Phenomenon P] is governed by [factor F], not [commonly assumed factor G], because [mechanism]"

**C2 = Method Recipe** (transferable pattern)
- What PATTERN can others reuse, and why does it work?
- Not "we used Module A + Module B"
- But "the recipe of [doing X before Y with constraint Z] works because [reason]"
- The recipe must be implementable without reading your code

**C3 = New Capability** (what the system enables)
- What can now be DONE that couldn't before?
- Evidence (numbers, tables, figures) supports C3 — it IS NOT C3 itself
- ❌ "Achieved [metric] of [value]" — this is evidence
- ✅ "Enables [decision/action] from [input type] that previously required [expensive/unavailable resource]"

### Layer 5: Implementation (Evidence Vehicle)

**What**: The system/model built to TEST the ideas in Layer 4.

**Rule**: The implementation IS NOT a contribution. It IS the evidence that C1-C3 are real.

Wrong framing: "We propose [SystemName], a [N]-stage architecture with [components]."
Right framing: "To test whether [C1 claim], we implement [SystemName] as a concrete instantiation of the [C2 recipe]. [SystemName] serves as evidence for C1-C3, not as the contribution itself."

### Layer 6: Dual Validation

**What**: Two explicit closing statements in abstract + conclusion.

1. **Engineering value**: What practical problem got solved? Give the concrete, domain-specific answer.
2. **Scientific knowledge**: What did the research community learn? Close the loop on the macro scientific question from Layer 3.

**Rule**: Never end with "we got good numbers." Always close the scientific question loop.

## Contribution Anti-Patterns

| Wrong Pattern | Right Pattern |
|--------------|---------------|
| "We propose a novel framework..." | "We find that [insight]. To leverage this, we design a method that [recipe]." |
| Contribution 1 = Module A, Contribution 2 = Module B | Contribution 1 = what was LEARNED, Contribution 2 = what PATTERN enables it |
| "Our method achieves SOTA on 3 benchmarks" | "[System] demonstrates that [C1 insight] enables [C3 capability], as evidenced by [metrics]" |
| Engineering problem = scientific question | Distinguish: problem is context (Layer 1), question is abstraction (Layer 3) |
| Numbers listed as contributions | Numbers are evidence FOR the capability claim (C3) |
| No dual validation | Always close both engineering AND science loops in conclusion |
