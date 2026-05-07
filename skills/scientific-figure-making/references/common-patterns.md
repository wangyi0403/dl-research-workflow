# Common Patterns

## Pattern 1: Grouped Bar Comparison

The most common figure in ML papers. Shows multiple methods across multiple metrics/datasets.

```python
import matplotlib.pyplot as plt
import numpy as np

# Setup
apply_publication_style(font_size=20)
colors = get_colors("microsoft")  # or "google", "xiaomi", "default"

categories = ["Dataset A", "Dataset B", "Dataset C"]
methods = {
    "Proposed": [95.2, 89.1, 92.7],
    "Baseline 1": [91.0, 85.3, 88.4],
    "Baseline 2": [88.5, 82.1, 86.9],
}

fig, ax = create_subplots(1, 1, figsize=(10, 6))
make_grouped_bar(ax[0], categories, methods, colors=colors[:len(methods)])
ax[0].set_ylabel("Accuracy (%)")
finalize_figure(fig, "figures/comparison", dpi=300)
```

## Pattern 2: Ultra-Wide Multi-Metric

For 4+ metrics side by side. Width = 3-4x height.

```python
fig, axes = create_subplots(1, 4, figsize=(36, 8))
for ax, metric_name, metric_data in zip(axes, metrics, data_list):
    make_grouped_bar(ax, categories, metric_data, colors=colors)
    ax.set_title(metric_name, fontsize=18, fontweight="bold")

# Dedicated legend in a 5th invisible subplot
handles, labels = axes[0].get_legend_handles_labels()
fig.legend(handles, labels, loc="lower center", ncol=len(methods),
           fontsize=16, bbox_to_anchor=(0.5, -0.02))
finalize_figure(fig, "figures/multi_metric", dpi=600, pad=1)
```

## Pattern 3: Trend Lines with Uncertainty

Training curves, performance vs parameter, etc.

```python
fig, ax = create_subplots(1, 1, figsize=(10, 7))
make_trend(ax[0], epochs, {"Ours": acc_ours, "Baseline": acc_base},
           colors=[colors[0], colors[2]],
           fill_between={"Ours": (acc_low, acc_high)})
ax[0].set_xlabel("Epoch")
ax[0].set_ylabel("Validation Accuracy")
finalize_figure(fig, "figures/training_curve")
```

## Pattern 4: Heatmap / Correlation Matrix

```python
fig, ax = create_subplots(1, 1, figsize=(8, 6))
make_heatmap(ax[0], correlation_matrix, row_labels, col_labels,
             cmap="RdYlBu_r", annotate=True, fmt=".2f")
finalize_figure(fig, "figures/correlation")
```

## Pattern 5: Ablation with Alpha Gradient

Show ablation variants of the same method with decreasing opacity.

```python
base_color = colors[0]  # proposed method color
alphas = [1.0, 0.7, 0.4, 0.2]  # full → minimal
for i, (variant, alpha) in enumerate(zip(ablation_variants, alphas)):
    ax.bar(x + i*width, variant["values"], width,
           color=base_color, alpha=alpha,
           edgecolor="black", linewidth=1.5,
           label=variant["name"])
```

## Pattern 6: Dedicated Legend Panel

When many series make inline legends cluttered.

```python
fig, axes = plt.subplots(1, 4, figsize=(40, 10),
                         gridspec_kw={"width_ratios": [1, 1, 1, 0.3]})
# Plot on axes[0:3]
# ...
# Legend on axes[3]
axes[3].set_axis_off()
handles, labels = axes[0].get_legend_handles_labels()
axes[3].legend(handles, labels, loc="center", fontsize=16)
```

## Anti-Patterns (Avoid)

| Bad | Good |
|-----|------|
| Y-axis 0-100 when data is 85-95 | Dynamic range matching data |
| Legend overlapping data | Dedicated legend panel or `bbox_to_anchor` |
| No edge color on bars | `edgecolor='black', linewidth=1.5` |
| Rainbow colormap for sequential | Use perceptual colormaps (`viridis`, `RdYlBu_r`) |
| Tiny font in multi-panel | Scale font with figure size |
