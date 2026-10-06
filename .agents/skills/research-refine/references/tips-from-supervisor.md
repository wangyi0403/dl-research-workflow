# Methodology Design Tips

## Before You Design

1. **Freeze the problem first.** Methodology follows problem, not the reverse. If you can't state the problem in one sentence, don't start designing.
2. **Know your acceptance bar.** Read 5 recent papers from target journal. Their method sections set the expectation.
3. **One dominant contribution.** One sharp thesis + at most one supporting contribution. Three contributions = none stand out.

## While Designing

4. **Smallest adequate mechanism.** Prefer the minimal intervention that directly addresses the bottleneck. A 3-line change that closes the gap beats a 300-line framework that does the same.
5. **Every module earns its place.** Each component must have a clear hypothesis: "Module X exists to solve problem Y, and removing X should degrade metric Z."
6. **Modern leverage is a prior, not decoration.** If LLM/VLM/foundation models naturally fit your problem, use them concretely (e.g., "we use GPT-4V to extract visual features because..."). Don't bolt on "LLM-enhanced" as a buzzword.

## Common Advisor Corrections

7. **"What's the simplest baseline that would also work?"** If a simpler method achieves 95% of your performance, your method is over-engineered.
8. **"Why not just fine-tune X?"** If a pre-trained model + fine-tuning is a plausible alternative, you must compare against it.
9. **"Have you considered the failure cases?"** For every method, list 3 scenarios where it would fail. If you can't think of any, you haven't thought hard enough.
10. **"What's the linchpin assumption?"** Every method has one assumption that, if violated, causes catastrophic failure. State it explicitly.

## Red Flags

- Method described as "a novel framework" without specifying what's novel
- Module names that are just buzzwords ("Context-Aware Semantic Fusion Module")
- Diagrams with >8 boxes — can't all be necessary
- "We adopt [standard technique] as our backbone" without explaining why this backbone
- No comparison against the simplest possible baseline
