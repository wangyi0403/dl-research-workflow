---
name: "scientific-figure-making"
description: "Create publication figures from data with claim-aware charts, honest scales and uncertainty, export, and visual QA. Use for plots, not diagrams."
---

# Scientific Figure Making

Choose what the figure must establish before drawing it. A polished plot that answers the wrong question or hides uncertainty is a failed figure.

## Scope

Use for reproducible quantitative figures such as lines, scatter plots, grouped comparisons, distributions, box/violin/point plots, heatmaps, error bars, and multi-panel layouts.

Do not use for:

- architecture, flow, concept, or process diagrams — route to the relevant diagram/illustration capability;
- interactive dashboards;
- 3D/GIS work;
- bitmap illustration or decorative scientific imagery.

## Workflow

### 1. Freeze purpose and provenance

State the reader question, Claim/Chain ID, takeaway the evidence may support, data source, analysis unit, and intended paper location. A takeaway is provisional until the rendered figure and source data agree.

### 2. Profile the data

Use `scripts/profile_data.py` or an equivalent reproducible inspection to check variable types, units, missingness, sample size, grouping, distribution, outliers, dependence, and uncertainty inputs. Do not silently drop observations or change an analysis unit for visual convenience.

### 3. Select the chart

Read `references/chart_selection.md` and `references/viz_pitfalls.md` when the chart is not already fixed by an approved plan. Choose the chart from the variable relationship and claim, not from a preferred house style.

When sample size is small or distribution shape matters, show observations or distributions instead of hiding them behind a mean bar. Avoid dual axes, rainbow scales, categorical points joined as continuous trends, and other encodings that invite a false comparison unless a documented reason and clear safeguards exist.

### 4. Apply venue and project style

Check the target venue's current dimensions, font, line-art, color, and export requirements. Preserve an established accessible project style when present. Otherwise choose a restrained, colorblind-aware palette with redundant encodings such as markers, line styles, hatching, or direct labels.

Do not impose universal colors for “proposed,” “baseline,” or “improvement.” Semantic mappings must fit the figure and remain consistent within the manuscript.

`scripts/setup_style.py` provides configurable defaults and CJK fallback handling; inspect the rendered fonts and override defaults when venue or project requirements differ.

### 5. Draw from recorded data

Use `references/plot_recipes.md` only for the selected chart. Keep plotting code beside the exported figure or in the project's documented figure source location. Captions state the uncertainty definition, sample size or analysis unit when material, and any transformations or exclusions.

Scales must support an honest comparison:

- bar lengths normally require a meaningful zero baseline;
- line, scatter, distribution, and diagnostic plots may use restricted ranges when this does not misrepresent magnitude;
- any break, normalization, log scale, or truncated range must be visible and explained.

### 6. Verify visually and programmatically

While the plotting code still holds the Matplotlib Figure, call `visual_qa.audit_layout(fig)` for glyph, clipping, and tick-overlap checks. Render a preview and inspect it against `references/visual_review.md`. The `scripts/visual_qa.py <file> --preview ...` CLI only renders an existing file; it does not run the Figure layout audit. Check clipping, overlap, missing glyphs, tick/label meaning, panel alignment, legend obstruction, grayscale interpretation, and whether the visual takeaway matches the source data.

Apply up to two bounded automatic repair passes for layout or rendering defects. If the scientific encoding or interpretation remains disputed, stop and report the decision rather than repeatedly restyling it.

### 7. Export and audit

Prefer vector output for line art and use the venue-required raster format and resolution for images. Run `scripts/check_figure.py --strict` for supported file checks. Strict exits 2 for FAIL and 3 for UNKNOWN (required checks not completed); exit 0 may include WARN and does not certify visual or full venue compliance. See `references/publication_checklist.md` for format coverage and export versus display dimensions. Re-check the figure at its actual manuscript display size after inclusion; scaling a vector graphic is allowed, but unreadable text or altered visual hierarchy is not.

## Completion contract

A figure is complete only when:

- its Claim/Chain ID, source data/code, and manuscript role are recorded;
- its encoding, scale, uncertainty, exclusions, and caption are defensible;
- vector/raster output follows current venue requirements;
- programmatic and visual QA pass at final display size;
- the corresponding entry in `docs/10_figure_report.md` is updated.

## References

| File | Open when |
|---|---|
| `references/chart_selection.md` | Selecting a chart from variables, sample structure, and claim |
| `references/viz_pitfalls.md` | Checking misleading or fragile encodings |
| `references/plot_recipes.md` | Implementing the selected matplotlib/seaborn chart |
| `references/journal_specs.md` | Establishing dimensions, fonts, DPI, and formats; verify current venue guidance before relying on presets |
| `references/data_profiling.md` | Interpreting the profiling report |
| `references/visual_review.md` | Perceptual QA of the rendered preview |
| `references/publication_checklist.md` | Final formal checks |

## Scripts

- `setup_style.py`: configurable style and CJK font handling
- `profile_data.py`: CSV/XLSX/TSV data profiling
- `visual_qa.py`: file preview CLI; `audit_layout(fig)` for in-memory Figure layout audit
- `export_figure.py`: multi-format export and grayscale preview
- `check_figure.py`: strict output audit
- `layout_tools.py`: reusable layout helpers

## Dependencies

Use the existing project environment. See `requirements.txt` for core packages and optional features. XLSX profiling needs `openpyxl`; legacy XLS needs `xlrd`. PDF file audits need `pypdf` (or compatible `PyPDF2`); saved-PDF preview rendering needs `PyMuPDF`. Missing a dependency blocks only that feature and must be reported as incomplete, not passed. Do not install packages without the relevant authorization.
