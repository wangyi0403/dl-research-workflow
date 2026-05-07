---
name: scientific-figure-making
description: >-
  Publication-ready matplotlib figures for papers—grouped bars, trends, scatter,
  heatmaps, multi-panel layouts—with house style (Arial, semantic palette, clean
  spines). Triggers on "画数据图", "plot results", "publication figure",
  "paper-ready chart". Not for interactive dashboards, 3D/GIS, or Figma workflows.
argument-hint: [chart-type] [data-source] [--palette microsoft|google|xiaomi|default]
allowed-tools: Bash(*), Write, Read
---

# Scientific Figure Making

Adapted from [ChenLiu-1996/figures4papers](https://github.com/ChenLiu-1996/figures4papers) with custom palette presets.

Open `references/` only as needed; start from the table below.

## When to use

- Matplotlib figures for **papers, slides, or reports** needing publication look
- **Grouped bars, trend lines, heatmaps, scatter, multi-panel grids**
- **PDF/SVG/high-DPI** output in scientific context

## When NOT to use

- Plotly / Altair / Bokeh (interactive/web)
- EDA-only (use seaborn directly)
- Architecture diagrams (use `paper-illustration` or `fireworks-tech-graph`)
- 3D / GIS / non-matplotlib

## Reference files

| File | Open when |
|------|-----------|
| [references/api.md](references/api.md) | Function signatures, PALETTE, color presets |
| [references/design-theory.md](references/design-theory.md) | Typography, export DPI, palette rationale |
| [references/common-patterns.md](references/common-patterns.md) | Layout patterns, legend panel, print-safe bars |

## Quick workflow

1. `apply_publication_style()` — set global rcParams
2. `create_subplots(rows, cols, figsize)` — get fig + flat axes
3. Plot with semantic colors from chosen PALETTE preset
4. `finalize_figure(fig, path, dpi, formats)` — export
