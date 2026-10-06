# Baseline Selection Guide

## Why Baseline Choice Matters

Weak baselines = inflated gains = rejected paper. The reviewer's first question: "Did you compare against the right methods?"

## Baseline Categories

### Tier 1: Classic Methods (Must Include)
Methods that defined the problem. Even if they perform poorly, they establish the problem's history.
- **Count**: 1-2
- **Example**: LSTM for sequence tasks, ResNet-50 for image classification, XGBoost for tabular data

### Tier 2: Recent SOTA (Must Include)
Best published results from the last 2 years. These are your real competition.
- **Count**: 2-4
- **Source**: Target journal's recent papers + top venues in your field

### Tier 3: Closest Competitor (Must Include)
The ONE method most similar to yours. This is the direct comparison.
- **Count**: 1
- **How to find**: Which paper would a reviewer say "this is just X with Y added"?

### Tier 4: Ablation Baselines (Must Include)
Simplified versions of your own method. Prove each component matters.
- **Count**: 2-4
- **Types**: Your method minus key components; your method with standard alternatives

## Selection Rules

### Rule 1: Match the Target Journal
If your target journal's recent papers use 8 baselines, you should too. Don't submit with 3 baselines to a journal that expects 8.

### Rule 2: Include at Least One from Target Journal
Shows you've done your homework and respect the journal's community.

### Rule 3: Fair Implementation
- Use authors' official code when available
- If re-implementing, verify you match reported numbers (±1%)
- If you can't reproduce reported results, document your attempt

### Rule 4: Same Data, Same Metrics
All baselines evaluated on identical train/val/test splits with identical metrics. No exceptions.

### Rule 5: Statistical Rigor
- Report mean ± std over ≥3 random seeds
- Statistical test (Wilcoxon or paired t-test) for main comparison
- Effect size, not just p-value

## Common Reviewer Criticisms

| Criticism | Prevention |
|-----------|-----------|
| "Why didn't you compare with [X]?" | Search for X before finalizing baselines |
| "Baseline [Y] is not well-tuned" | Use official code or report your tuning budget |
| "Your method uses more parameters" | Report parameter counts + inference time |
| "The gain over [Z] is not significant" | Report p-values + effect sizes |
| "These baselines are outdated" | Check publication years; all within 3 years |

## Baseline Budget

| Paper Type | Minimum Baselines | Ideal |
|-----------|-------------------|-------|
| Technique paper | 5-7 | 8-12 |
| Benchmark paper | N/A (you're the baseline) | Cover all major method families |
| Short paper / workshop | 3-5 | 5-7 |

## Pre-Submission Check

- [ ] At least one classic method included
- [ ] At least one SOTA from last 2 years
- [ ] Closest competitor identified and compared
- [ ] At least one baseline from target journal
- [ ] All baselines use same data splits and metrics
- [ ] Parameter counts and inference time reported
- [ ] Statistical significance tested for main comparison
