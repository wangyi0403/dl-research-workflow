# Scientific Figure Color Palette

Choose accessible, internally consistent colors for the actual scientific roles. These palettes are examples, not universal role assignments.

## Example Semantic Color Assignments

Use this mapping only when it matches an established project convention. Otherwise define a project-specific mapping and keep it stable across related figures.

| Role | Color | Hex | Use |
|------|-------|-----|-----|
| **Proposed Method** | Blue | `#2171B5` | Your method's bars/lines/regions |
| **Strong Baseline** | Red/Orange | `#D73027` | Best competing method |
| **Other Baselines** | Gray scale | `#969696` → `#D9D9D9` | Progressively lighter for weaker methods |
| **Improvement/Highlight** | Green | `#1B9E77` | Regions where your method improves |
| **Reference/Ground Truth** | Black/Dark Gray | `#252525` | Ground truth values, reference lines |
| **Ablation Variants** | Blue gradient | `#2171B5` → `#9ECAE1` | Darkest = full model, lightest = most ablated |

## Colorblind-Safe Palette

Use when ≥3 categories need distinction. Optimized for deuteranopia/protanopia:

```
#2166AC (Blue)    — Category 1 / Proposed
#D6604D (Red)     — Category 2 / Baseline
#4DAF4A (Green)   — Category 3 / Improvement
#FFD92F (Yellow)  — Category 4 (use sparingly)
#A6CEE3 (L.Blue)  — Category 5
#B2DF8A (L.Green) — Category 6
```

## Sequential Palettes

For ordered data (low→high, few→many):

**Single-hue blue** (preferred for most journals):
```
#F7FBFF → #DEEBF7 → #C6DBEF → #9ECAE1 → #6BAED6 → #4292C6 → #2171B5 → #08519C
```

**Viridis** (perceptually uniform, colorblind-safe):
```
#440154 → #482878 → #3E4A89 → #31688E → #26828E → #1F9E89 → #35B779 → #6DCD59 → #B4DE2C → #FDE725
```

## Diverging Palettes

For data with a meaningful midpoint (difference, change, correlation):

```
#2166AC → #92C5DE → #D1E5F0 → #F7F7F7 → #FDDBC7 → #F4A582 → #D6604D
(Blue = negative change, White = no change, Red = positive change)
```

## Journal-Specific Preferences

| Journal | Preference | Notes |
|---------|-----------|-------|
| Nature | Muted, minimal colors | ≤3 colors per figure; avoid pure red/green |
| Science | Similar to Nature | Prefer grayscale + 1 highlight color |
| IEEE | Color allowed | Ensure grayscale printability |
| Elsevier (most) | Color allowed, grayscale backup | Figures work in both color and B&W |
| CV/ML conferences | Full color, no restrictions | But still: redundant encoding for accessibility |

## Anti-Patterns

1. **Rainbow/Jet colormap**: Perceptually distorting, not colorblind-safe. Never use.
2. **Red-Green only**: ~8% of males can't distinguish. Use Blue-Orange instead.
3. **>6 colors**: Beyond 6 categories, switch to faceting or use direct labels.
4. **Pure primaries** (`#FF0000`, `#00FF00`, `#0000FF`): Looks like a spreadsheet, not a publication.
5. **Inconsistent semantics**: Reusing one color for conflicting roles across related figures without a clear legend confuses the reader.

## Quick Reference

```python
# Example palette; bind colors to project roles explicitly.
BLUE      = '#2171B5'
ORANGE    = '#D73027'
GREEN     = '#1B9E77'
GRAY      = '#969696'
BLACK     = '#252525'

# Colorblind-safe 4-class
CB_BLUE   = '#2166AC'
CB_RED    = '#D6604D'
CB_GREEN  = '#4DAF4A'
CB_YELLOW = '#FFD92F'

# Sequential blue
BLUE_9 = ['#F7FBFF','#DEEBF7','#C6DBEF','#9ECAE1','#6BAED6','#4292C6','#2171B5','#08519C']
```

## Grayscale Check

Before finalizing, convert every figure to grayscale. If any information is lost:
- Add different line styles (solid, dashed, dotted)
- Add different marker shapes (●, ▲, ■, ◆)
- Add direct text labels instead of relying on color alone

## Brand Palettes (3 Sets)

From the `get_colors()` function. Pick one set and use consistently.

### Microsoft
| Role | Hex | Use |
|------|-----|-----|
| Blue `#3E9FEF` | Proposed / main method |
| Red `#E74D23` | Baseline / comparison |
| Green `#80B800` | Improvement |
| Yellow `#F7B700` | Emphasis / accent |
| Olive `#9A7D28` | Auxiliary |
| Gray `#6A7279` | Neutral / reference |

### Google
Blue `#5586F5` (Proposed) · Green `#47A74F` (Improvement) · Yellow `#F4BC00` (Emphasis) · Red `#E04639` (Baseline) · Light Gray `#929292` (Aux) · Dark Gray `#787878` (Neutral)

### Xiaomi
Orange `#F4690E` (Proposed) · Coral `#ED524F` (Baseline) · Teal `#43A69A` (Improvement) · Blue `#3957B6` (Aux) · Brown-Gray `#5E5750` (Neutral) · Dark Red `#5A1616` (Emphasis)

**Fill rule**: use light version (original color + 70-80% white overlay). **Stroke/text/arrows**: use original or one shade darker.

## Hand-Drawn Figure Conventions

Optional conventions for a user-requested hand-drawn route. Do not apply them to vector diagrams or another established project style.

**Typography**: Arial (or Arimo as free clone). Body 12-16pt, panel titles 18-22pt bold. All sans-serif. Variable names in italic, color-matched to their module.

**Layout vocabulary**:
- Left→right horizontal pipeline or (a)(b)(c) multi-panel
- Rounded rectangles (radius 8-10), light low-saturation fill, white background, thin edges (~2.5px)
- Encoder/layers: 3D trapezoid or stacked layer blocks with subtle gradient
- Tokens/patches: row of evenly-spaced small colored squares
- Graph structure: node-link with colored dot nodes + curved edges
- Arrows: main flow = thin black solid (~1.5px solid arrowhead); auxiliary/feedback/loss = colored dashed; distinguish forward vs backward by color
- Icons: 🔥=trainable ❄️=frozen 🔒=fixed; always include symbol legend

**Flag-ship level restraint** (for top-tier journals):
- ≤3-4 colors locked to semantics → almost no legend needed
- Background color-block zoning (like LDM's Pixel/Latent/Conditioning) > dashed grouping
- N× fold to avoid drawing all layers; skip arcs (ResNet style)
- One signature motif per figure (ResNet skip arc / CLIP dot-product matrix / ViT patch sequence)
- Overview + detail inset: left overview, right one-block zoom
- Less is more: emptier, fewer colors, larger blocks > dense, multi-color, multi-dashed

**Three-figure synergy** (Teaser → Architecture → Detail):
- Same color semantics across all three
- Teaser (Fig.1): sell the PROBLEM, not the architecture. Before/after comparison (left=pain❌ right=solution✅). One core contrast, minimal text.
- Architecture overview: input→…→output single-axis. Contribution module = largest, brightest, centered + annotated. Dimension labels on arrows.
- Detail zoom: enlarge the novel block. Formula→shape mapping (Q/K/V, softmax, matrix multiply, residual add — one graphic element per operator). Readable without the formula.
