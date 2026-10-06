# Scientific Figure Architecture Patterns

Common visual motifs for paper illustrations. Pick the pattern that matches your story.

## Pattern 1: Pipeline/Flow

```
[Input] → [Box A] → [Box B] → [Box C] → [Output]
```

**When**: Sequential processing stages. Reader should follow data left-to-right.
**Key rule**: ≤5 boxes. Beyond 5, group into meta-stages.
**Common mistake**: Every box same size → no visual hierarchy. Make the novel component larger/different color.
**Color convention**: distinguish roles consistently using the project palette and redundant encoding; do not assume one universal method color.

## Pattern 2: Comparison (Side-by-Side)

```
Previous Work:        Our Method:
[Diagram A]           [Diagram B]
  ↓                      ↓
[Limitation noted]     [Improvement highlighted]
```

**When**: Your method differs from prior work in a visually obvious way.
**Key rule**: Align vertically. Identical parts look identical; differences are highlighted.
**Common mistake**: Over-stylizing the "previous" side → looks like you're mocking prior work.

## Pattern 3: Module Detail (Zoom-In)

```
[Overview: small version of full system]
         ↓ (zoom indicator)
[Detailed view of ONE module]
```

**When**: The overall architecture is simple, but one module is the innovation.
**Key rule**: The overview must be recognizable as the same system in the detailed view.
**Common mistake**: Overview and detailed view use different notation → reader can't map between them.

## Pattern 4: Attention/Heatmap Overlay

```
[Input image/data] + [Attention/heatmap overlay]
```

**When**: Showing WHERE the model focuses or WHAT features it learns.
**Key rule**: Heatmap color must contrast with underlying data. Use perceptually uniform colormaps (viridis, magma).
**Common mistake**: Heatmap obscures the underlying data → can't see what the model is attending TO.

## Pattern 5: Result Showcase (Gallery)

```
[Example 1]  [Example 2]  [Example 3]
[Example 4]  [Example 5]  [Example 6]
  ↓ Good cases
[Example 7]  [Example 8]  [Example 9]
  ↓ Failure cases
```

**When**: Qualitative results are the main story.
**Key rule**: Include BOTH good and bad cases. Only showing successes is cherry-picking.
**Common mistake**: Images too small to see details. Print at ≥1.5 cm per image.

## Pattern 6: Ablation Ladder

```
Full Model:  ━━━━━━━━━━━━ 85.3%  ← top bar (widest, darkest)
- Module A:  ━━━━━━━━━━   82.1%  ← shorter bar
- Module B:  ━━━━━━━━━━━  84.0%  ← slightly shorter
- Both:      ━━━━━━━━     78.5%  ← shortest bar
```

**When**: Showing ablation results as a visual comparison.
**Key rule**: Always sort by performance (best → worst). Color-code: full model = darkest.
**Common mistake**: Using 3D bars or other chartjunk. Simple horizontal bars are clearest.

## Pattern 7: Two-Column Layout

```
┌─────────────────────┬─────────────────────┐
│ Conceptual Diagram  │ Results Table/Plot   │
│ (WHY it works)      │ (THAT it works)      │
│                     │                     │
│ [illustration]      │ [data]              │
└─────────────────────┴─────────────────────┘
```

**When**: A concept and its proof belong together.
**Key rule**: Left = qualitative/why; Right = quantitative/that. Consistent across all figures.
**Common mistake**: Repeating the same layout for every figure → monotonous. Use only when concept+proof pairing is natural.

## General Rules

1. **Color semantics**: define role mappings for the project and keep them consistent across related figures; do not rely on color alone.
2. **Font**: follow the project and venue typography; verify readability at final display size. Use all-caps only when it is part of the established notation.
3. **Arrows**: Only between boxes that have a real data/control flow. No decorative arrows.
4. **White space**: ≥2mm padding inside boxes. Crowded diagrams look amateur.
5. **Self-contained**: Figure + caption should be understandable without reading the paper body.
6. **Colorblind-safe**: Use redundant encoding (line style, marker shape, pattern) alongside color.
