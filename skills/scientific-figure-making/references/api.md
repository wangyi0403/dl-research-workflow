# API Reference

## Color Palettes

### Default palette (figures4papers semantic)

```python
PALETTE = {
    "blue_main": "#0F4D92",
    "blue_secondary": "#3775BA",
    "green_1": "#DDF3DE",
    "green_2": "#AADCA9",
    "green_3": "#8BCF8B",
    "red_1": "#F6CFCB",
    "red_2": "#E9A6A1",
    "red_strong": "#B64342",
    "neutral": "#CFCECE",
    "gray_mid": "#767676",
    "gray_dark": "#4D4D4D",
    "gray_darkest": "#272727",
    "highlight": "#FFD700",
    "accent_magenta": "#EA84DD",
    "accent_teal": "#42949E",
    "accent_violet": "#9A4D8E",
}
```

Semantic usage: blue = proposed method, green = improvement, red/pink = baseline, gray = reference.

### Microsoft palette (Adobe Color)

```python
PALETTE_MICROSOFT = {
    "red": "#E74D23",
    "green": "#80B800",
    "blue": "#3E9FEF",
    "yellow": "#F7B700",
    "olive": "#9A7D28",
    "gray": "#6A7279",
}
COLORS_MICROSOFT = ["#3E9FEF", "#E74D23", "#80B800", "#F7B700", "#9A7D28", "#6A7279"]
```

### Google palette (Adobe Color)

```python
PALETTE_GOOGLE = {
    "blue": "#5586F5",
    "green": "#47A74F",
    "yellow": "#F4BC00",
    "red": "#E04639",
    "gray_light": "#929292",
    "gray_dark": "#787878",
}
COLORS_GOOGLE = ["#5586F5", "#E04639", "#F4BC00", "#47A74F", "#929292", "#787878"]
```

### Xiaomi palette (Adobe Color)

```python
PALETTE_XIAOMI = {
    "orange": "#F4690E",
    "coral": "#ED524F",
    "teal": "#43A69A",
    "blue": "#3957B6",
    "brown_gray": "#5E5750",
    "dark_red": "#5A1616",
}
COLORS_XIAOMI = ["#F4690E", "#ED524F", "#43A69A", "#3957B6", "#5E5750", "#5A1616"]
```

### Quick palette selector

```python
def get_palette(name="default"):
    palettes = {
        "default": PALETTE,
        "microsoft": PALETTE_MICROSOFT,
        "google": PALETTE_GOOGLE,
        "xiaomi": PALETTE_XIAOMI,
    }
    return palettes.get(name, PALETTE)

def get_colors(name="default"):
    color_lists = {
        "default": ["#0F4D92", "#8BCF8B", "#B64342", "#42949E", "#9A4D8E", "#CFCECE"],
        "microsoft": COLORS_MICROSOFT,
        "google": COLORS_GOOGLE,
        "xiaomi": COLORS_XIAOMI,
    }
    return color_lists.get(name, color_lists["default"])
```

---

## Configuration

```python
from dataclasses import dataclass

@dataclass(frozen=True)
class FigureStyle:
    font_family: list = ("Arial", "Helvetica", "DejaVu Sans", "sans-serif")
    font_size: int = 16
    axes_linewidth: float = 2.5
    use_tex: bool = False

PUBLICATION_RCPARAMS = {
    "font.family": ["Arial", "Helvetica", "DejaVu Sans", "sans-serif"],
    "font.size": 16,
    "axes.spines.right": False,
    "axes.spines.top": False,
    "axes.linewidth": 2.5,
    "legend.frameon": False,
    "svg.fonttype": "none",
}
```

---

## Core Functions

### apply_publication_style

```python
def apply_publication_style(font_size=16, axes_linewidth=2.5):
    """Call BEFORE creating any figure. Sets global rcParams."""
    import matplotlib.pyplot as plt
    plt.rcParams.update(PUBLICATION_RCPARAMS)
    plt.rcParams["font.size"] = font_size
    plt.rcParams["axes.linewidth"] = axes_linewidth
```

### create_subplots

```python
def create_subplots(rows=1, cols=1, figsize=None, **kwargs):
    """Returns (fig, flat_axes_array). Default figsize: (8*cols, 6*rows)."""
    import matplotlib.pyplot as plt
    if figsize is None:
        figsize = (8 * cols, 6 * rows)
    fig, axes = plt.subplots(rows, cols, figsize=figsize, **kwargs)
    if rows * cols == 1:
        axes = [axes]
    else:
        axes = axes.flatten()
    return fig, axes
```

### finalize_figure

```python
def finalize_figure(fig, path, dpi=300, formats=("png", "pdf"), pad=2):
    """Export figure. Applies tight_layout, saves in all requested formats."""
    from pathlib import Path
    fig.tight_layout(pad=pad)
    base = Path(path).with_suffix("")
    for fmt in formats:
        fig.savefig(f"{base}.{fmt}", dpi=dpi, bbox_inches="tight")
```

---

## Plot Builders

### make_grouped_bar

```python
def make_grouped_bar(ax, categories, series_dict, colors=None, annotate=True,
                     bar_width=0.15, edgecolor="black", linewidth=1.5):
    """
    ax: matplotlib Axes
    categories: list of x-axis labels
    series_dict: {"Method A": [v1, v2, ...], "Method B": [...]}
    colors: list of colors (one per series), or None for default
    annotate: if True, place values above bars
    """
```

### make_trend

```python
def make_trend(ax, x, series_dict, colors=None, markers=None,
               fill_between=None, linewidth=2.5):
    """
    x: shared x-axis values
    series_dict: {"Method": y_values}
    fill_between: {"Method": (y_low, y_high)} for uncertainty bands
    """
```

### make_heatmap

```python
def make_heatmap(ax, matrix, row_labels, col_labels, cmap="RdYlBu_r",
                 annotate=True, fmt=".2f", vmin=None, vmax=None):
    """Render 2D matrix with colorbar and optional cell text."""
```

### make_scatter

```python
def make_scatter(ax, x, y, colors=None, sizes=None, alpha=0.7,
                 edgecolors="black", linewidths=0.5):
    """Single-series scatter plot."""
```

---

## Validation Rules

1. All series in `series_dict` must have same length as `categories`
2. `finalize_figure` must be called after all plotting
3. `apply_publication_style` must be called before `create_subplots`
4. Output files go to `figures/` directory with stable names
