# Design Theory

## Typography

**Primary font:** Arial (user preference, cross-platform safe)
**Fallback chain:** `["Arial", "Helvetica", "DejaVu Sans", "sans-serif"]`

| Context | font.size | axes.linewidth |
|---------|-----------|----------------|
| Large comparison bars | 24 | 3 |
| Standard figures | 16 | 2.5 |
| Compact analytic plots | 14 | 2 |

**Spine rule:** Always remove right and top spines. Only left and bottom remain.

## Export Standards

| Use case | DPI | Format | Layout |
|----------|-----|--------|--------|
| Draft review | 150 | PNG | `tight_layout(pad=2)` |
| Paper submission | 300 | PDF + PNG | `tight_layout(pad=2)` |
| Dense multi-panel | 600 | PDF | `tight_layout(pad=1)` |
| Poster / slide | 150 | PNG | `tight_layout(pad=3)` |

**Vector formats** (PDF, SVG, EPS): preferred for LaTeX `\includegraphics`.
**Raster formats** (PNG, TIFF, JPG): fallback or journal requirement.

Always save both PDF and PNG unless told otherwise.

## Color Semantics

| Role | Default color | Microsoft | Google | Xiaomi |
|------|---------------|-----------|--------|--------|
| Proposed method | Blue `#0F4D92` | Blue `#3E9FEF` | Blue `#5586F5` | Orange `#F4690E` |
| Improvement | Green `#8BCF8B` | Green `#80B800` | Green `#47A74F` | Teal `#43A69A` |
| Baseline / competitor | Red `#B64342` | Red `#E74D23` | Red `#E04639` | Coral `#ED524F` |
| Reference / neutral | Gray `#CFCECE` | Gray `#6A7279` | Gray `#929292` | Brown-gray `#5E5750` |
| Accent 1 | Yellow `#FFD700` | Yellow `#F7B700` | Yellow `#F4BC00` | Blue `#3957B6` |
| Accent 2 | Teal `#42949E` | Purple `#68217A` | Dark Blue `#1A73E8` | Purple `#9C27B0` |

**Rule:** Within one paper, pick ONE palette and use it consistently across all figures.

## Grayscale Safety

Figures must be distinguishable in B&W print:
- Use `edgecolor='black'` on all bars (`linewidth=1.5`)
- Add hatching patterns (`'/'`, `'\\'`, `'.'`, `'x'`) when >4 series
- Ensure sufficient luminance contrast between adjacent colors

## Multi-Panel Layout Strategies

- **Ultra-wide canvases** (`figsize=(36, 12)`) prevent vertical crowding
- **Dedicated legend subplots** (`ax.set_axis_off()` + `fig.legend()`) keep data areas clean
- **Dynamic y-axis** — tighten to data range (85-95 not 0-100) to show differences
- **Direct annotation** — place values above bars in large font for readability
- **Alpha gradients** (0.2 → 1.0) for ablation variants of same method
