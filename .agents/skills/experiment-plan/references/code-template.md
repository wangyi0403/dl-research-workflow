# Experiment Code Organization Template

Standard directory structure for ML/DL experiment code. All code lives in `experiments/` (server-mounted directory).

## Directory Structure

```
experiments/
├── configs/                 ← YAML/JSON experiment configs
│   ├── baseline.yaml        ← One config per experiment variant
│   ├── proposed.yaml
│   └── ablation_*.yaml
│
├── src/                     ← Python source code
│   ├── model/               ← Model architecture code
│   │   ├── backbone.py      ← Base encoder/feature extractor
│   │   └── modules.py       ← Custom modules (attention, fusion, etc.)
│   ├── data/                ← Data loading and preprocessing
│   │   ├── dataset.py       ← PyTorch Dataset subclass
│   │   └── transforms.py    ← Augmentation, normalization
│   ├── training/            ← Training loop, loss functions
│   │   ├── trainer.py       ← Main training logic
│   │   └── losses.py        ← Custom loss functions
│   └── evaluation/          ← Inference and evaluation
│       ├── inference.py     ← Model inference on test set
│       └── metrics.py       ← Metric computation (F1, AUROC, etc.)
│
├── scripts/                 ← Shell scripts for batch runs
│   ├── train.sh             ← Launch training
│   ├── eval.sh              ← Run evaluation
│   └── run_all.sh           ← Sequential pipeline: train → eval → aggregate
│
├── registry/                ← Run identity and provenance (experiments.csv)
└── requirements.txt         ← Python dependencies
```

## Key Conventions

1. **One config file per experiment variant**. Don't edit configs between runs — create a new YAML for each variant.
2. **Immutable naming**: use Experiment IDs in root-level `results/data/`, `results/logs/` and `results/checkpoints/`; never reuse an earlier run's outputs.
3. **Seed management**: record seeds, data/split, configuration, code, environment and hardware. A matching seed alone does not establish reproducibility.
4. **Config completeness**: A config file alone should fully specify an experiment. No hidden defaults in code that differ between variants.
5. **One result authority**: project-root `results/` owns local artifacts. An authorized remote job may use a documented staging directory; record its mapping to the local result paths and preserve completion-time hashes during transfer.

## Server Sync Pattern

```bash
# Sync code to server (exclude data and checkpoints)
rsync -avz --exclude '__pycache__/' \
  experiments/ user@host:/project/experiments/

# After training completes, pull results back
rsync -avz user@host:/project/results/ results/
```

These are path examples for an already-authorized destination, not an instruction to launch or overwrite remote work. Synchronize only the approved scope; reconcile the returned run registry and immutable artifacts before strict result-table validation. Keep data acquisition/transfer separate from code sync.
