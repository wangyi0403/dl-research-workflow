# Ablation Design Guide

## Why Ablations Matter

Ablations answer: "Did each component of your method actually help?"
Without them, reviewers assume you threw everything in and only the simplest part mattered.

## Core Principles

### 1. One Ablation = One Hypothesis

Each ablation tests a specific claim:
- "Module A improves accuracy by handling edge cases" → Remove A, measure degradation on edge cases
- "Module B reduces computation" → Remove B, measure runtime increase
- "Loss term L prevents overfitting" → Remove L, measure train/val gap

### 2. Full Model as Baseline

Always compare against **Full Model** (your complete method), not against the weakest variant:
```
Full Model: 85.3%  ← baseline for all ablations
- Module A:  82.1%  (Δ = -3.2)  → A contributes +3.2
- Module B:  84.0%  (Δ = -1.3)  → B contributes +1.3
- Both A & B: 78.5% (Δ = -6.8) → Combined effect > sum of parts
```

### 3. Ablation Depth by Contribution Type

| Contribution Type | Minimum Ablation |
|-------------------|-----------------|
| New module | Remove module; replace with identity/ skip connection |
| New loss term | Train with λ=0 for that term |
| New data augmentation | Train without it |
| New architecture component | Replace with standard alternative |
| New training strategy | Train with standard strategy |

### 4. Common Ablation Patterns

**Component removal**: Train with component removed, all else equal.
```
Full Model → Full - Module A → Full - Module B → Full - Both
```

**Component replacement**: Replace your component with a standard alternative.
```
Your Attention → Standard Self-Attention → No Attention
```

**Hyperparameter sensitivity**: Vary key hyperparameters; show performance is stable.
```
Learning rate: [1e-5, 5e-5, 1e-4, 5e-4] → all within 2% of best
```

**Data scaling**: How does performance change with more/less data?
```
Train with 25% / 50% / 75% / 100% of data
```

**Model scaling**: How does performance change with model size?
```
Vary hidden dim: 64 / 128 / 256 / 512
```

## Anti-Patterns

1. **Only ablating the weakest component.** Reviewers notice when you skip the hard ablation.
2. **Ablation that doesn't isolate.** "Remove A and B together" — now you don't know which mattered.
3. **Rebuttal-only ablations.** If an ablation is obvious, do it before submission, not in rebuttal.
4. **Non-monotonic claims.** "Module X helps on dataset A but hurts on B" — this needs explanation, not hiding.

## Checklist

- [ ] Every module has a corresponding removal experiment
- [ ] Every loss term has an ablation (λ=0)
- [ ] At least one component-replacement ablation (vs. standard alternative)
- [ ] Hyperparameter sensitivity reported for key parameters
- [ ] Statistical significance reported for all ablations
- [ ] GPU hours budgeted for ablations (typically 30-40% of total)
