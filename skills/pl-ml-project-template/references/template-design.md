# PL ML Project Template — Design Rationale

Reference: [miracleyoo/pytorch-lightning-template](https://github.com/miracleyoo/pytorch-lightning-template)

## Core Philosophy: Interface Pattern

The template decouples **training logic** from **model/dataset implementation** via two Interface classes:

```
main.py (orchestration)
  ├── MInterface (LightningModule)  ──dynamic import──>  my_net.py (pure nn.Module)
  └── DInterface (LightningDataModule) ──dynamic import──>  my_data.py (pure Dataset)
```

Benefits:
- Adding a new model = adding one `.py` file, no Interface/main changes needed
- Training boilerplate (optimizer, scheduler, loss, logging) is written once
- CLI-driven, suitable for batch experiment scripts

## Dynamic Loading Mechanism

Both Interfaces use the same technique: convert a `snake_case` file name to `CamelCase` class name, then `importlib` loads it:

```python
# --model_name standard_net -> model.standard_net.StandardNet
camel_name = ''.join([i.capitalize() for i in name.split('_')])
Model = getattr(importlib.import_module('.' + name, package=__package__), camel_name)
```

**Convention**: file `foo_bar.py` must define class `FooBar`.

## Parameter Passthrough — `instancialize()`

Interfaces inspect target class `__init__` signatures and auto-match from global `hparams`:

```python
def instancialize(self, Model, **other_args):
    class_args = inspect.getfullargspec(Model.__init__).args[1:]
    args1 = {arg: getattr(self.hparams, arg) for arg in class_args if arg in self.hparams}
    args1.update(other_args)
    return Model(**args1)
```

This means: add a CLI arg in `main.py`, accept same-named param in model/dataset `__init__`, done.

## MInterface (`model/model_interface.py`)

- Inherits `pl.LightningModule`
- `load_model()`: dynamic import + `instancialize()`
- `configure_loss()`: selects loss via `--loss` arg (mse, l1, bce, cross_entropy)
- `configure_optimizers()`: built-in Adam/SGD + StepLR/CosineAnnealing
- `training_step` / `validation_step`: generic forward + loss + metrics

## DInterface (`data/data_interface.py`)

- Inherits `pl.LightningDataModule`
- `load_data_module()`: dynamic import of dataset class
- `setup()`: `instancialize(train=True/False)` for train/val/test splits
- Standard `DataLoader` configuration with `num_workers`, `batch_size`

## Directory Structure

```
project/
├── main.py                     # Entry: argparse + Trainer assembly
├── utils.py                    # Helpers (checkpoint path, seed, etc.)
├── Makefile                    # One-command workflows (make train/test/all)
├── README.md                   # Project description, quick start, citation
├── requirements.txt
├── .env.example                # Environment variable template
├── .gitignore
├── configs/
│   └── default.yaml            # Default hyperparameters
├── data/
│   ├── __init__.py             # exports DInterface
│   ├── data_interface.py       # LightningDataModule interface
│   └── standard_dataset.py     # Concrete dataset (user edits this)
├── model/
│   ├── __init__.py             # exports MInterface
│   ├── model_interface.py      # LightningModule interface
│   └── standard_model.py       # Concrete model (user edits this)
├── scripts/
│   ├── train.sh                # Training entry
│   ├── test.sh                 # Testing entry
│   ├── run_all.sh              # One-click reproduce pipeline
│   ├── ablation.sh             # Ablation parameter sweep
│   ├── visualize.py            # Plot training curves → figures/
│   └── export_results.py       # Results JSON → LaTeX table
├── docs/
│   └── doc/                    # Paper materials (naming: YYYY-MM-DD_desc_vN.ext)
├── results/                    # Experiment output JSONs
├── figures/                    # Generated plots
├── train_log/
└── test_log/
```

## Adding a New Model or Dataset

1. **New model**: create `model/my_model.py` with `class MyModel(nn.Module)`
2. **New dataset**: create `data/my_data.py` with `class MyData(Dataset)`
3. **Run**: `--model_name my_model --dataset my_data`
4. No Interface or main.py changes needed (unless new CLI args are required)

## Task-Type Variations

| Task Type      | Default Loss       | Default Metric | Notes                         |
| -------------- | ------------------ | -------------- | ----------------------------- |
| classification | cross_entropy      | accuracy       | Softmax output                |
| regression     | mse                | mae, r2        | Single/multi-target           |
| timeseries     | mse                | mae, rmse      | Adds window/horizon params    |

Each task type pre-configures the MInterface with appropriate loss, metrics, and output activation.

## Known Limitations

- `training_step` assumes single-optimizer; GAN-style dual-optimizer needs MInterface modification
- Parameter matching relies on naming consistency, no type checking
- Use `inspect.getfullargspec` (not deprecated `getargspec`) for Python 3.11+
