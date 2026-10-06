# DL Training Failure Patterns & Self-Healing

Common failure modes during DL training, their diagnosis, and automated fixes.

## Error Categories

### 1. NaN/Inf Loss

**Symptoms**: Loss becomes NaN or Inf, typically within first 100 steps.
**Root causes**:

| Cause | Diagnosis | Fix |
|-------|-----------|-----|
| LR too high | Loss spikes then NaN | Reduce LR by 10x, restart from last checkpoint |
| Gradient explosion | `grad_norm > 1000` | Enable gradient clipping (`max_norm=1.0`) |
| Log of zero/negative | NaN in first forward pass | Add epsilon (1e-8) to log/softmax inputs |
| Division by zero | NaN in specific operation | Add epsilon in normalization layers |
| FP16 overflow | NaN with mixed precision | Switch to FP32 for unstable ops; use loss scaling |

**Self-heal protocol**:
1. Check `grad_norm` → if >1000, clip gradients
2. Halve LR → restart from last valid checkpoint
3. If still NaN → switch to FP32, restart
4. If still NaN → flag for human review

### 2. Out of Memory (OOM)

**Symptoms**: `CUDA out of memory`, `RuntimeError: CUDA error: out of memory`
**Root causes**:

| Cause | Diagnosis | Fix |
|-------|-----------|-----|
| Batch too large | OOM on first iteration | Halve `batch_size` |
| Gradient accumulation insufficient | Large model, small GPU | Increase `gradient_accumulation_steps` |
| Memory leak | OOM after N steps (not first) | Check for detached tensors accumulating |
| Validation with `torch.no_grad()` missing | OOM during validation | Wrap validation in `@torch.no_grad()` |
| Too many workers | OOM in dataloader | Reduce `num_workers` |

**Self-heal protocol**:
1. Halve `batch_size` → restart
2. If still OOM → enable gradient checkpointing
3. If still OOM → reduce model size (hidden_dim / num_layers)
4. If still OOM → flag for human review

### 3. Loss Not Decreasing

**Symptoms**: Training loss flat or oscillating after warmup.
**Root causes**:

| Cause | Diagnosis | Fix |
|-------|-----------|-----|
| LR too low | Loss barely changes | Increase LR by 5x |
| LR too high | Loss oscillates wildly | Decrease LR by 5x |
| Bad initialization | Loss stuck at random baseline | Use better init (xavier_uniform, kaiming_normal) |
| Dead ReLU | Many neurons output zero | Switch to LeakyReLU / GELU |
| Data issue | Loss doesn't decrease on ANY split | Check data loading; verify labels |

**Self-heal protocol**:
1. Run LR range test (1e-5 to 1.0) for 100 steps → find steepest descent LR
2. If no improvement → check data pipeline integrity
3. If data OK → try different optimizer (AdamW → SGD with momentum)
4. Flag for human review if no improvement after 3 attempts

### 4. Overfitting

**Symptoms**: Train loss ↓, val loss ↑ (gap widening after epoch N).
**Root causes**:

| Cause | Diagnosis | Fix |
|-------|-----------|-----|
| Insufficient regularization | Large train/val gap | Increase weight_decay, add dropout |
| Model too large for data | Train acc → 100%, val acc << train | Reduce model size |
| Data leakage | Val performance too good, then unexplained | Check train/val split for contamination |
| Too few augmentations | Small dataset, large model | Add data augmentation |

### 5. Slow Convergence

**Symptoms**: Loss decreasing but very slowly; estimated completion > budget.
**Root causes**: LR schedule too conservative, bad initialization, or model capacity insufficient.

### 6. Reproducibility Failure

**Symptoms**: Same config, different runs → significantly different results.
**Root causes**: Missing random seed, non-deterministic ops (CUDA conv), data shuffling.

## General Self-Healing Protocol

```
1. Catch error → classify into category
2. Apply first fix from category-specific protocol
3. Restart from last valid checkpoint
4. If same error within 10% of previous failure step → escalate to next fix
5. Max 3 attempts per error → then flag for human
6. Log: error type, attempted fixes, final state
```

## Monitoring Keywords

Watch log output for these patterns to trigger self-healing early:
- `nan`, `inf`, `NaN`, `Inf`, `INF`
- `CUDA out of memory`, `RuntimeError`, `CUBLAS_STATUS`
- `loss` followed by no change for 500+ steps
- `accuracy` stuck at `1/n_classes` (random baseline)
