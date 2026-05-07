#!/usr/bin/env python3
"""Initialize a PyTorch Lightning project scaffold.

Usage:
    python init_project.py /path/to/project --task-type classification
    python init_project.py /path/to/project --task-type regression
    python init_project.py /path/to/project --task-type timeseries
    python init_project.py /path/to/project --task-type timeseries --force
"""

import argparse
import os
import sys
from pathlib import Path
from textwrap import dedent

TASK_TYPES = ("classification", "regression", "timeseries")

# ---------------------------------------------------------------------------
# Template content generators
# ---------------------------------------------------------------------------

LOSS_MAP = {
    "classification": "cross_entropy",
    "regression": "mse",
    "timeseries": "mse",
}

METRIC_MAP = {
    "classification": "accuracy",
    "regression": "mae",
    "timeseries": "mae",
}


def _main_py(task_type: str) -> str:
    return dedent(f"""\
        import pytorch_lightning as pl
        from argparse import ArgumentParser
        from pytorch_lightning.callbacks import (
            EarlyStopping,
            ModelCheckpoint,
            LearningRateMonitor,
        )

        from model import MInterface
        from data import DInterface
        from utils import load_config


        def main():
            parser = ArgumentParser()

            # --- general ---
            parser.add_argument("--seed", default=42, type=int)
            parser.add_argument("--config", default="configs/default.yaml", type=str)

            # --- data ---
            parser.add_argument("--dataset", default="standard_dataset", type=str)
            parser.add_argument("--batch_size", default=32, type=int)
            parser.add_argument("--num_workers", default=4, type=int)

            # --- model ---
            parser.add_argument("--model_name", default="standard_model", type=str)
            parser.add_argument("--loss", default="{LOSS_MAP[task_type]}", type=str)
            parser.add_argument("--lr", default=1e-3, type=float)
            parser.add_argument("--weight_decay", default=0.0, type=float)

            # --- trainer ---
            parser.add_argument("--max_epochs", default=100, type=int)
            parser.add_argument("--accelerator", default="auto", type=str)
            parser.add_argument("--devices", default=1, type=int)

            args = parser.parse_args()
            args = load_config(args)

            pl.seed_everything(args.seed)

            data_module = DInterface(**vars(args))
            model = MInterface(**vars(args))

            callbacks = [
                EarlyStopping(monitor="val_loss", patience=10, mode="min"),
                ModelCheckpoint(
                    dirpath="train_log/checkpoints",
                    monitor="val_loss",
                    save_top_k=3,
                    mode="min",
                ),
                LearningRateMonitor(logging_interval="epoch"),
            ]

            trainer = pl.Trainer(
                max_epochs=args.max_epochs,
                accelerator=args.accelerator,
                devices=args.devices,
                callbacks=callbacks,
                default_root_dir="train_log",
            )

            trainer.fit(model, datamodule=data_module)
            trainer.test(model, datamodule=data_module)


        if __name__ == "__main__":
            main()
    """)


def _utils_py() -> str:
    return dedent("""\
        import yaml
        from argparse import Namespace


        def load_config(args):
            \"\"\"Merge YAML config into argparse Namespace (CLI takes precedence).\"\"\"
            if hasattr(args, "config") and args.config:
                try:
                    with open(args.config, "r") as f:
                        cfg = yaml.safe_load(f) or {}
                    for k, v in cfg.items():
                        if not hasattr(args, k) or getattr(args, k) is None:
                            setattr(args, k, v)
                except FileNotFoundError:
                    pass
            return args
    """)


def _model_interface_py(task_type: str) -> str:
    extra_metrics = ""
    if task_type == "classification":
        extra_metrics = dedent("""\
            import torchmetrics

                    self.train_acc = torchmetrics.Accuracy(task="multiclass", num_classes=self.hparams.get("num_classes", 10))
                    self.val_acc = torchmetrics.Accuracy(task="multiclass", num_classes=self.hparams.get("num_classes", 10))
        """)

    return dedent(f"""\
        import inspect
        import importlib

        import torch
        import torch.nn as nn
        import pytorch_lightning as pl


        class MInterface(pl.LightningModule):
            \"\"\"Universal model interface — dynamically loads any model by name.\"\"\"

            def __init__(self, **kwargs):
                super().__init__()
                self.save_hyperparameters()
                self.load_model()
                self.configure_loss()

            def load_model(self):
                name = self.hparams["model_name"]
                camel = "".join([w.capitalize() for w in name.split("_")])
                Model = getattr(
                    importlib.import_module("." + name, package="model"), camel
                )
                self.model = self.instancialize(Model)

            def instancialize(self, Model, **other_args):
                class_args = inspect.getfullargspec(Model.__init__).args[1:]
                args1 = {{
                    arg: self.hparams[arg]
                    for arg in class_args
                    if arg in self.hparams
                }}
                args1.update(other_args)
                return Model(**args1)

            def configure_loss(self):
                loss_name = self.hparams.get("loss", "{LOSS_MAP[task_type]}")
                mapping = {{
                    "mse": nn.MSELoss,
                    "l1": nn.L1Loss,
                    "bce": nn.BCEWithLogitsLoss,
                    "cross_entropy": nn.CrossEntropyLoss,
                }}
                self.loss_fn = mapping.get(loss_name, nn.MSELoss)()

            def forward(self, x):
                return self.model(x)

            def training_step(self, batch, batch_idx):
                x, y = batch
                y_hat = self(x)
                loss = self.loss_fn(y_hat, y)
                self.log("train_loss", loss, prog_bar=True)
                return loss

            def validation_step(self, batch, batch_idx):
                x, y = batch
                y_hat = self(x)
                loss = self.loss_fn(y_hat, y)
                self.log("val_loss", loss, prog_bar=True)

            def test_step(self, batch, batch_idx):
                x, y = batch
                y_hat = self(x)
                loss = self.loss_fn(y_hat, y)
                self.log("test_loss", loss)

            def configure_optimizers(self):
                optimizer = torch.optim.Adam(
                    self.parameters(),
                    lr=self.hparams.get("lr", 1e-3),
                    weight_decay=self.hparams.get("weight_decay", 0.0),
                )
                scheduler = torch.optim.lr_scheduler.CosineAnnealingLR(
                    optimizer, T_max=self.hparams.get("max_epochs", 100)
                )
                return {{"optimizer": optimizer, "lr_scheduler": scheduler}}
    """)


def _data_interface_py() -> str:
    return dedent("""\
        import inspect
        import importlib

        import pytorch_lightning as pl
        from torch.utils.data import DataLoader


        class DInterface(pl.LightningDataModule):
            \"\"\"Universal data interface — dynamically loads any dataset by name.\"\"\"

            def __init__(self, **kwargs):
                super().__init__()
                self.save_hyperparameters()
                self.load_data_module()
                self.batch_size = self.hparams.get("batch_size", 32)
                self.num_workers = self.hparams.get("num_workers", 4)

            def load_data_module(self):
                name = self.hparams["dataset"]
                camel = "".join([w.capitalize() for w in name.split("_")])
                self.DatasetClass = getattr(
                    importlib.import_module("." + name, package="data"), camel
                )

            def instancialize(self, **other_args):
                class_args = inspect.getfullargspec(self.DatasetClass.__init__).args[1:]
                args1 = {
                    arg: self.hparams[arg]
                    for arg in class_args
                    if arg in self.hparams
                }
                args1.update(other_args)
                return self.DatasetClass(**args1)

            def setup(self, stage=None):
                if stage == "fit" or stage is None:
                    self.train_dataset = self.instancialize(train=True)
                    self.val_dataset = self.instancialize(train=False)
                if stage == "test" or stage is None:
                    self.test_dataset = self.instancialize(train=False)

            def train_dataloader(self):
                return DataLoader(
                    self.train_dataset,
                    batch_size=self.batch_size,
                    num_workers=self.num_workers,
                    shuffle=True,
                )

            def val_dataloader(self):
                return DataLoader(
                    self.val_dataset,
                    batch_size=self.batch_size,
                    num_workers=self.num_workers,
                )

            def test_dataloader(self):
                return DataLoader(
                    self.test_dataset,
                    batch_size=self.batch_size,
                    num_workers=self.num_workers,
                )
    """)


def _standard_model_py(task_type: str) -> str:
    if task_type == "classification":
        return dedent("""\
            import torch.nn as nn


            class StandardModel(nn.Module):
                \"\"\"Simple classification network. Replace with your architecture.\"\"\"

                def __init__(self, input_dim=784, num_classes=10, hidden_dim=256):
                    super().__init__()
                    self.net = nn.Sequential(
                        nn.Linear(input_dim, hidden_dim),
                        nn.ReLU(),
                        nn.Linear(hidden_dim, hidden_dim),
                        nn.ReLU(),
                        nn.Linear(hidden_dim, num_classes),
                    )

                def forward(self, x):
                    return self.net(x.flatten(1))
        """)
    elif task_type == "regression":
        return dedent("""\
            import torch.nn as nn


            class StandardModel(nn.Module):
                \"\"\"Simple regression network. Replace with your architecture.\"\"\"

                def __init__(self, input_dim=10, output_dim=1, hidden_dim=128):
                    super().__init__()
                    self.net = nn.Sequential(
                        nn.Linear(input_dim, hidden_dim),
                        nn.ReLU(),
                        nn.Linear(hidden_dim, hidden_dim),
                        nn.ReLU(),
                        nn.Linear(hidden_dim, output_dim),
                    )

                def forward(self, x):
                    return self.net(x)
        """)
    else:  # timeseries
        return dedent("""\
            import torch
            import torch.nn as nn


            class StandardModel(nn.Module):
                \"\"\"Simple LSTM for time series forecasting. Replace with your architecture.\"\"\"

                def __init__(self, input_dim=1, hidden_dim=64, num_layers=2,
                             output_dim=1, horizon=1):
                    super().__init__()
                    self.lstm = nn.LSTM(input_dim, hidden_dim, num_layers, batch_first=True)
                    self.fc = nn.Linear(hidden_dim, output_dim * horizon)
                    self.horizon = horizon
                    self.output_dim = output_dim

                def forward(self, x):
                    # x: (batch, seq_len, input_dim)
                    out, _ = self.lstm(x)
                    pred = self.fc(out[:, -1, :])
                    return pred.view(-1, self.horizon, self.output_dim).squeeze(-1)
        """)


def _standard_dataset_py(task_type: str) -> str:
    if task_type == "classification":
        return dedent("""\
            import torch
            from torch.utils.data import Dataset


            class StandardDataset(Dataset):
                \"\"\"Placeholder classification dataset. Replace with your data loading logic.\"\"\"

                def __init__(self, train=True, input_dim=784, num_classes=10,
                             num_samples=1000, **kwargs):
                    super().__init__()
                    self.data = torch.randn(num_samples, input_dim)
                    self.targets = torch.randint(0, num_classes, (num_samples,))

                def __len__(self):
                    return len(self.data)

                def __getitem__(self, idx):
                    return self.data[idx], self.targets[idx]
        """)
    elif task_type == "regression":
        return dedent("""\
            import torch
            from torch.utils.data import Dataset


            class StandardDataset(Dataset):
                \"\"\"Placeholder regression dataset. Replace with your data loading logic.\"\"\"

                def __init__(self, train=True, input_dim=10, output_dim=1,
                             num_samples=1000, **kwargs):
                    super().__init__()
                    self.data = torch.randn(num_samples, input_dim)
                    self.targets = torch.randn(num_samples, output_dim)

                def __len__(self):
                    return len(self.data)

                def __getitem__(self, idx):
                    return self.data[idx], self.targets[idx]
        """)
    else:  # timeseries
        return dedent("""\
            import torch
            from torch.utils.data import Dataset


            class StandardDataset(Dataset):
                \"\"\"Placeholder time series dataset. Replace with your data loading logic.\"\"\"

                def __init__(self, train=True, input_dim=1, window=24,
                             horizon=1, num_samples=1000, **kwargs):
                    super().__init__()
                    self.window = window
                    self.horizon = horizon
                    # Generate synthetic sequential data
                    series = torch.randn(num_samples + window + horizon, input_dim).cumsum(0)
                    self.x = torch.stack(
                        [series[i : i + window] for i in range(num_samples)]
                    )
                    self.y = torch.stack(
                        [series[i + window : i + window + horizon, 0] for i in range(num_samples)]
                    )

                def __len__(self):
                    return len(self.x)

                def __getitem__(self, idx):
                    return self.x[idx], self.y[idx]
        """)


def _default_yaml(task_type: str) -> str:
    base = dedent(f"""\
        # Default configuration for {task_type} task
        seed: 42
        dataset: standard_dataset
        model_name: standard_model
        loss: {LOSS_MAP[task_type]}
        lr: 0.001
        weight_decay: 0.0
        batch_size: 32
        num_workers: 4
        max_epochs: 100
        accelerator: auto
        devices: 1
    """)
    if task_type == "classification":
        base += "input_dim: 784\nnum_classes: 10\nhidden_dim: 256\n"
    elif task_type == "regression":
        base += "input_dim: 10\noutput_dim: 1\nhidden_dim: 128\n"
    else:
        base += "input_dim: 1\nwindow: 24\nhorizon: 1\nhidden_dim: 64\nnum_layers: 2\noutput_dim: 1\n"
    return base


def _init_py_model() -> str:
    return "from .model_interface import MInterface\n"


def _init_py_data() -> str:
    return "from .data_interface import DInterface\n"


def _requirements_txt() -> str:
    return dedent("""\
        torch>=2.0
        pytorch-lightning>=2.0
        torchmetrics
        pyyaml
    """)


def _gitignore() -> str:
    return dedent("""\
        __pycache__/
        *.pyc
        .venv/
        train_log/
        test_log/
        *.ckpt
        wandb/
        .DS_Store
        .env
        results/*.json
    """)


def _train_sh() -> str:
    return dedent("""\
        #!/usr/bin/env bash
        python main.py --config configs/default.yaml "$@"
    """)


def _test_sh() -> str:
    return dedent("""\
        #!/usr/bin/env bash
        # Provide --ckpt_path to load a trained checkpoint
        python main.py --config configs/default.yaml "$@"
    """)


def _visualize_py(task_type: str) -> str:
    return dedent(f"""\
        #!/usr/bin/env python3
        \"\"\"Visualize training results: loss curves, metrics, and predictions.\"\"\"

        import argparse
        import json
        from pathlib import Path

        import matplotlib.pyplot as plt
        import torch
        import yaml


        def plot_training_curves(log_dir: str, output_dir: str):
            metrics_path = Path(log_dir) / "metrics.csv"
            out = Path(output_dir)
            out.mkdir(parents=True, exist_ok=True)

            if not metrics_path.exists():
                # Try tensorboard event files via CSV export
                print(f"No metrics.csv at {{metrics_path}}, check TensorBoard logs.")
                return

            import csv
            with open(metrics_path) as f:
                reader = csv.DictReader(f)
                rows = list(reader)

            if not rows:
                print("Empty metrics file.")
                return

            keys = [k for k in rows[0].keys() if k not in ("step", "epoch")]
            for key in keys:
                vals = [(int(r.get("epoch", i)), float(r[key])) for i, r in enumerate(rows) if r.get(key)]
                if not vals:
                    continue
                epochs, values = zip(*vals)
                plt.figure(figsize=(8, 5))
                plt.plot(epochs, values, marker="o", markersize=3)
                plt.xlabel("Epoch")
                plt.ylabel(key)
                plt.title(key)
                plt.tight_layout()
                plt.savefig(out / f"{{key}}.pdf", dpi=150)
                plt.savefig(out / f"{{key}}.png", dpi=150)
                plt.close()
                print(f"Saved {{key}} plot to {{out}}")


        if __name__ == "__main__":
            parser = argparse.ArgumentParser()
            parser.add_argument("--log_dir", default="train_log", help="Training log directory")
            parser.add_argument("--output_dir", default="figures", help="Output directory for figures")
            args = parser.parse_args()
            plot_training_curves(args.log_dir, args.output_dir)
    """)


def _export_results_py() -> str:
    return dedent("""\
        #!/usr/bin/env python3
        \"\"\"Export experiment results to LaTeX tables and paper-ready figures.\"\"\"

        import argparse
        import json
        from pathlib import Path


        def results_to_latex(results_json: str, output_path: str):
            with open(results_json) as f:
                results = json.load(f)

            if not results:
                print("No results to export.")
                return

            keys = list(results[0].keys())
            header = " & ".join(keys) + " \\\\\\\\"
            rows = []
            for r in results:
                row = " & ".join(str(r.get(k, "")) for k in keys) + " \\\\\\\\"
                rows.append(row)

            table = (
                "\\\\begin{table}[htbp]\\n"
                "\\\\centering\\n"
                "\\\\caption{Experimental Results}\\n"
                "\\\\label{tab:results}\\n"
                f"\\\\begin{{tabular}}{{{' '.join(['c'] * len(keys))}}}\\n"
                "\\\\toprule\\n"
                f"{header}\\n"
                "\\\\midrule\\n"
                + "\\n".join(rows) + "\\n"
                "\\\\bottomrule\\n"
                "\\\\end{tabular}\\n"
                "\\\\end{table}\\n"
            )

            Path(output_path).write_text(table, encoding="utf-8")
            print(f"LaTeX table saved to {output_path}")


        if __name__ == "__main__":
            parser = argparse.ArgumentParser()
            parser.add_argument("--results", default="results/results.json", help="Path to results JSON")
            parser.add_argument("--output", default="docs/doc/results_table.tex", help="Output LaTeX file")
            args = parser.parse_args()
            results_to_latex(args.results, args.output)
    """)


def _run_all_sh() -> str:
    return dedent("""\
        #!/usr/bin/env bash
        set -e

        echo "=== Step 1: Training ==="
        bash scripts/train.sh "$@"

        echo "=== Step 2: Testing ==="
        bash scripts/test.sh "$@"

        echo "=== Step 3: Visualization ==="
        python scripts/visualize.py

        echo "=== Step 4: Export Results ==="
        python scripts/export_results.py

        echo "=== All steps completed ==="
    """)


def _ablation_sh() -> str:
    return dedent("""\
        #!/usr/bin/env bash
        set -e

        # Ablation study: modify parameters below for your experiments
        CONFIGS=(
            "--lr 0.001"
            "--lr 0.0001"
            "--lr 0.01"
        )

        for i in "${!CONFIGS[@]}"; do
            echo "=== Ablation run $((i+1))/${#CONFIGS[@]}: ${CONFIGS[$i]} ==="
            python main.py --config configs/default.yaml ${CONFIGS[$i]} "$@"
        done

        echo "=== Ablation study completed ==="
    """)


def _makefile() -> str:
    return dedent("""\
        .PHONY: train test visualize export all ablation clean

        train:
        \tbash scripts/train.sh

        test:
        \tbash scripts/test.sh

        visualize:
        \tpython scripts/visualize.py

        export:
        \tpython scripts/export_results.py

        all:
        \tbash scripts/run_all.sh

        ablation:
        \tbash scripts/ablation.sh

        clean:
        \trm -rf train_log/ test_log/ figures/*.png figures/*.pdf
    """)


def _readme_md(task_type: str) -> str:
    return dedent(f"""\
        # Project Name

        > One-line description of this project.

        ## Task

        {task_type}

        ## Quick Start

        ```bash
        pip install -r requirements.txt
        make train          # or: bash scripts/train.sh
        make test
        make visualize
        ```

        ## One-Click Reproduce

        ```bash
        make all            # train -> test -> visualize -> export
        ```

        ## Project Structure

        ```
        ├── main.py                 # Entry point
        ├── configs/default.yaml    # Hyperparameters
        ├── data/                   # Dataset interface + implementations
        ├── model/                  # Model interface + implementations
        ├── scripts/                # Train/test/visualize/ablation scripts
        ├── docs/doc/               # Paper materials and experiment notes
        ├── figures/                # Generated plots
        ├── results/                # Experiment results (JSON)
        └── train_log/              # Checkpoints and training logs
        ```

        ## Adding a New Model

        1. Create `model/my_model.py` with `class MyModel(nn.Module)`
        2. Run: `python main.py --model_name my_model`

        ## Citation

        ```bibtex
        @article{{author2026title,
          title={{Your Paper Title}},
          author={{Your Name}},
          year={{2026}},
        }}
        ```

        ## License

        MIT
    """)


def _env_example() -> str:
    return dedent("""\
        # Copy to .env and fill in values
        # WANDB_API_KEY=
        # CUDA_VISIBLE_DEVICES=0
    """)


def _docs_readme() -> str:
    return dedent("""\
        # docs/doc

        Store paper materials here:
        - Experiment result tables (LaTeX .tex files)
        - Key figures for the paper
        - Literature notes and references
        - Reviewer feedback and response letters

        Naming convention: `YYYY-MM-DD_description_vN.ext`
        Example: `2026-04-27_ablation_results_v1.tex`
    """)


def _results_gitkeep() -> str:
    return ""


# ---------------------------------------------------------------------------
# Scaffold writer
# ---------------------------------------------------------------------------

FILES_TEMPLATE = {
    "main.py": _main_py,
    "utils.py": lambda _: _utils_py(),
    "model/__init__.py": lambda _: _init_py_model(),
    "model/model_interface.py": _model_interface_py,
    "model/standard_model.py": _standard_model_py,
    "data/__init__.py": lambda _: _init_py_data(),
    "data/data_interface.py": lambda _: _data_interface_py(),
    "data/standard_dataset.py": _standard_dataset_py,
    "configs/default.yaml": _default_yaml,
    "scripts/train.sh": lambda _: _train_sh(),
    "scripts/test.sh": lambda _: _test_sh(),
    "scripts/run_all.sh": lambda _: _run_all_sh(),
    "scripts/ablation.sh": lambda _: _ablation_sh(),
    "scripts/visualize.py": _visualize_py,
    "scripts/export_results.py": lambda _: _export_results_py(),
    "requirements.txt": lambda _: _requirements_txt(),
    ".gitignore": lambda _: _gitignore(),
    ".env.example": lambda _: _env_example(),
    "Makefile": lambda _: _makefile(),
    "README.md": _readme_md,
    "docs/doc/README.md": lambda _: _docs_readme(),
    "results/.gitkeep": lambda _: _results_gitkeep(),
}

DIRS = [
    "configs",
    "data",
    "model",
    "scripts",
    "train_log",
    "test_log",
    "figures",
    "docs/doc",
    "results",
]


def scaffold(root: Path, task_type: str, force: bool = False) -> None:
    root = root.resolve()

    # Create directories
    for d in DIRS:
        (root / d).mkdir(parents=True, exist_ok=True)

    # Write files
    written, skipped = [], []
    for rel_path, gen_fn in FILES_TEMPLATE.items():
        target = root / rel_path
        if target.exists() and not force:
            skipped.append(rel_path)
            continue
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(gen_fn(task_type), encoding="utf-8")
        written.append(rel_path)

    # Report
    print(f"Project scaffolded at: {root}")
    print(f"Task type: {task_type}")
    print(f"Files written: {len(written)}")
    for f in written:
        print(f"  + {f}")
    if skipped:
        print(f"Files skipped (already exist, use --force to overwrite): {len(skipped)}")
        for f in skipped:
            print(f"  ~ {f}")
    print()
    print("Next steps:")
    print(f"  1. cd {root}")
    print("  2. Edit configs/default.yaml")
    print("  3. Replace data/standard_dataset.py with your dataset")
    print("  4. Replace model/standard_model.py with your model")
    print("  5. make all  (or: bash scripts/run_all.sh)")
    print("  6. make ablation  (ablation study)")
    print("  7. Paper materials -> docs/doc/")


def main():
    parser = argparse.ArgumentParser(
        description="Initialize a PyTorch Lightning project scaffold."
    )
    parser.add_argument("project_dir", type=str, help="Target project directory")
    parser.add_argument(
        "--task-type",
        choices=TASK_TYPES,
        default="classification",
        help="Task type (default: classification)",
    )
    parser.add_argument(
        "--force",
        action="store_true",
        help="Overwrite existing files",
    )
    args = parser.parse_args()
    scaffold(Path(args.project_dir), args.task_type, args.force)


if __name__ == "__main__":
    main()
