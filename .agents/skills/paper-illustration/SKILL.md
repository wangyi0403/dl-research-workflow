---
name: "paper-illustration"
description: "Create non-data scientific figures such as method diagrams, mechanisms, and conceptual schematics; use editable vector tools when appropriate."
---

# Paper Illustration

Create or guide the creation of non-data scientific figures while preserving an editable source, claim linkage, and visual verification. A prompt is an intermediate artifact, not the default final deliverable.

## Principles

- Choose colors, typography, and encodings from the project style and target venue; do not impose universal role colors or a universal font family.
- Preserve consistent terminology, visual hierarchy, line weights, and accessible redundant encodings across the manuscript.
- Choose editable vector diagrams when precise structure or future editing matters. For non-data concept, method or workflow figures, honor an explicit user preference for built-in image generation; verify every label and relationship against the figure contract. Generated pixels are not an editable vector source.
- Every figure must identify its Claim/Chain ID, narrative role, source material, and limits of interpretation.

## Process

For each figure in the paper plan:

### 1. Freeze the figure contract

Record:
- Figure content and layout
- project/venue style constraints
- Spatial arrangement
- What each element represents

Save the contract or generation notes to `results/figures/0X_xxx.md` when a persistent artifact is needed.

**Done when**: the figure purpose, claim, content, layout, terminology, style constraints, and acceptance criteria are explicit.

### 2. Select the production route

- Architecture, flow, process, concept, or editable schematic: choose a diagram capability when editability is required; an explicitly requested image-generation route may supply the visual version. If both versions are retained, keep their semantics consistent.
- Composed product/UI view: use the available design capability when appropriate.
- Scientific illustration or bitmap material: use the available image-generation capability when it matches the content or the user's requested visual style. Quantitative charts remain generated from verified data and code.
- User hand-drawing: use a detailed prompt/reference pack only when the user explicitly chooses that route.

**Done when**: the selected route matches the scientific content and required editability.

### 3. Produce the figure

Create the requested final asset and a reviewable preview using the selected capability. Retain an editable source when required; do not describe a generated bitmap as editable. For a cropped draw.io figure intended for LaTeX, use the installed CLI's `--crop` PDF export when supported; inspect the complete diagram and its PDF page bounds before inclusion, because a default page export may clip wide diagrams. Keep generated assets, prompts, and sources under `results/figures/` with stable descriptive names. Do not fabricate scientific objects, causal links, quantitative values, or experimental outcomes for visual completeness.

**Done when**: the requested asset and preview exist, any required editable source is available, or the user has explicitly requested a prompt-only handoff.

### 4. Verify

Inspect the rendered figure at expected manuscript size. Check clipping, overlap, reading order, terminology, arrow meaning, color accessibility, caption consistency, and whether the visual supports no stronger claim than the evidence permits.

**Done when**: programmatic or visual QA is complete and material uncertainties are recorded.

### 5. Record and hand off

Update `docs/10_figure_report.md` with the Claim/Chain ID, source path, preview/export path, caption status, QA result, and remaining author decisions.

**Done when**: the final figure and editable source are traceable and pass the Figure Design Checklist.

## Figure Design Checklist

Before final production, verify the figure contract addresses:
- [ ] Clear visual hierarchy (most important element largest/most prominent)
- [ ] Color semantics consistent with paper conventions
- [ ] All text readable at expected print size and compliant with the target venue
- [ ] No unnecessary decorative elements
- [ ] Self-contained: understandable without reading the paper
- [ ] Journal-compliant: no color-only information (colorblind-safe)

## Output

- `results/figures/0X_xxx.md` — figure contract or prompt/reference pack when needed
- editable vector/design source for structured figures
- reviewable PNG/PDF/SVG export as appropriate
- optional `results/figures/0X_material_*` assets with provenance
- corresponding entry in `docs/10_figure_report.md`

## References

| File | Open when |
|------|-----------|
| `references/figure-type-selection.md` | Deciding which figure type fits the content. |
| `references/architecture-patterns.md` | Choosing visual layout. 7 common scientific figure motifs (pipeline, comparison, zoom-in, etc.) with rules and anti-patterns. |
| `references/color-palette.md` | Selecting a project-appropriate accessible palette and checking grayscale interpretation. |
