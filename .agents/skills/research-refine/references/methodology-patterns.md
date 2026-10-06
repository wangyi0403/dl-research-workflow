# Methodology Design Patterns

Common methodology patterns for ML/DL research. Match your idea to the closest pattern, then adapt.

## 1. Pipeline / Sequential

```
Input → Module A → Module B → Module C → Output
```

**When**: Problem naturally decomposes into sequential stages (e.g., detect → classify → refine).
**Key question**: Why must B come after A? What happens if you swap order?
**Ablation**: Remove each module; measure degradation at each stage.
**Example**: Two-stage object detectors (R-CNN family), cascaded error correction.

## 2. Multi-Branch / Parallel

```
          ┌→ Branch A ─┐
Input ────┼→ Branch B ─┼──→ Fusion → Output
          └→ Branch C ─┘
```

**When**: Multiple information sources need independent processing before fusion.
**Key question**: What does each branch capture that others don't?
**Ablation**: Remove one branch at a time; try all pairwise combinations.
**Example**: Multi-modal fusion, multi-scale feature extractors.

## 3. Encoder-Decoder

```
Input → Encoder → Latent → Decoder → Output
```

**When**: Input and output have different dimensionalities or modalities.
**Key question**: What information is preserved in the latent representation?
**Ablation**: Vary latent size; visualize latent space; probe what's encoded.
**Example**: Seq2seq, VAE, image segmentation (U-Net).

## 4. Attention / Gating

```
Input → Select/Weight → Focused Processing → Output
```

**When**: Not all input parts are equally important; model must learn what to attend to.
**Key question**: Does attention actually attend to meaningful regions, or just learns a fixed pattern?
**Ablation**: Replace learned attention with uniform weights; visualize attention maps.
**Example**: Transformers, channel attention (SENet), gated RNNs.

## 5. Auxiliary Task / Multi-Task

```
                    ┌→ Aux Output 1
Shared Backbone ────┼→ Main Output
                    └→ Aux Output 2
```

**When**: Related tasks can provide useful training signal for each other.
**Key question**: Does the auxiliary task genuinely help the main task, or just add compute?
**Ablation**: Train with/without auxiliary loss; vary auxiliary loss weight.
**Example**: Depth estimation as auxiliary for segmentation, pretext tasks in self-supervised learning.

## 6. Iterative / Recursive

```
Input → Process → Check → [not done] → Refine → Process → ...
                         → [done] → Output
```

**When**: One-shot processing is insufficient; refinement needs feedback.
**Key question**: How many iterations are needed? Is there a convergence guarantee?
**Ablation**: Vary iteration count; compare with one-shot baseline.
**Example**: Iterative refinement networks, diffusion models, gradient-based optimization unrolling.

## 7. Contrastive / Metric Learning

```
Anchor ─┐
         ├→ Embed → Pull close / Push apart → Loss
Sample ─┘
```

**When**: The key challenge is learning a good representation space, not a classifier.
**Key question**: What defines "similar" and "dissimilar" in your problem?
**Ablation**: Vary negative sampling strategy; test with different similarity metrics.
**Example**: SimCLR, triplet loss, metric learning for few-shot.

## Pattern Selection Checklist

1. Does your problem decompose into sequential stages? → Pipeline
2. Do you have multiple independent input modalities? → Multi-Branch
3. Is input-output dimensionality different? → Encoder-Decoder
4. Is selective focus the core mechanism? → Attention/Gating
5. Do related tasks share information? → Auxiliary Task
6. Does the problem need iterative refinement? → Iterative
7. Is representation learning the core goal? → Contrastive

## Anti-Patterns

- **Kitchen sink**: Combining 3+ patterns without ablating each. If you need all of them, prove it.
- **Attention for attention's sake**: Adding self-attention without explaining what it should attend to.
- **Fake multi-task**: Auxiliary tasks with loss weight → 0 in practice.
- **Over-engineering**: A 2-module pipeline that works is better than a 5-module one that's uninterpretable.
