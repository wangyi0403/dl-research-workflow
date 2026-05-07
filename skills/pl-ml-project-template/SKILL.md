---
name: pl-ml-project-template
description: Scaffold a PyTorch Lightning project for classification, regression, or timeseries research. Triggers on "新建项目", "initialize project", "scaffold", "create PL project". Not for LLM/PEFT/RAG/agent stacks.
argument-hint: [task-type: classification|regression|timeseries] [--force]
allowed-tools: Bash(*), Write
---

# PL ML Project Template

Use this skill when the user wants a reusable PyTorch Lightning project structure for standard supervised research tasks.

Supported template types:
- `classification`
- `regression`
- `timeseries`

Do not use this skill for:
- LLM pretraining or instruction tuning
- PEFT / LoRA / QLoRA projects
- RAG, agents, MCP services
- inference-serving repositories
- pure scikit-learn projects that do not need Lightning

## Workflow

1. Confirm the target task type from the user request or infer the closest one:
   - image/tabular category prediction -> `classification`
   - continuous target prediction -> `regression`
   - sequential prediction / sensor forecasting -> `timeseries`
2. Run `scripts/init_project.py` to scaffold the project.
3. Tell the user which files must be edited first:
   - `configs/default.yaml`
   - `data/dataset/standard_dataset.py`
   - `model/standard_model.py`
   - `model/model_interface.py`
4. If the task is domain-specific, adapt metrics and losses after scaffold generation rather than inventing a brand new structure.

## Commands

Initialize a classification project:

```bash
python scripts/init_project.py /path/to/project --task-type classification
```

Initialize a regression project:

```bash
python scripts/init_project.py /path/to/project --task-type regression
```

Initialize a time series project:

```bash
python scripts/init_project.py /path/to/project --task-type timeseries
```

Overwrite existing template files only when explicitly requested:

```bash
python scripts/init_project.py /path/to/project --task-type timeseries --force
```

## Generated Scripts

| Script | Purpose | Command |
|--------|---------|---------|
| `scripts/train.sh` | Train model | `make train` |
| `scripts/test.sh` | Test model | `make test` |
| `scripts/visualize.py` | Plot training curves to `figures/` | `make visualize` |
| `scripts/export_results.py` | Results JSON → LaTeX table | `make export` |
| `scripts/run_all.sh` | One-click reproduce: train→test→viz→export | `make all` |
| `scripts/ablation.sh` | Ablation study with parameter sweep | `make ablation` |

## Open-Source Readiness

The scaffold generates all files needed for a publishable repo:
- `README.md` with quick start, structure, citation
- `Makefile` for one-command workflows
- `.env.example` for environment configuration
- `.gitignore` covering logs, checkpoints, secrets
- `docs/doc/` for paper materials with naming convention
- `results/` for experiment outputs

## Document Version Convention

Files in `docs/doc/` follow: `YYYY-MM-DD_description_vN.ext`
- Example: `2026-04-27_ablation_results_v1.tex`
- Increment `vN` for revisions, never reuse version numbers

## Design Notes

This skill intentionally follows a project-interface pattern:
- `main.py` stays thin
- `data/data_interface.py` owns the `LightningDataModule`
- `model/model_interface.py` owns the `LightningModule`
- dataset and model files remain replaceable units

Naming convention:
- file names use `snake_case`
- classes use `CamelCase`
- `standard_model.py` -> `StandardModel`
- `standard_dataset.py` -> `StandardDataset`

Read [references/template-design.md](references/template-design.md) when you need the rationale or want to extend the scaffold.

## Post-Scaffold Verification

After scaffolding, run a quick smoke test:

```bash
cd /path/to/project
python -c "from model import MInterface; from data import DInterface; print('OK')"
```

If using a GPU environment, also verify training wiring:

```bash
python main.py --max_epochs 1 --devices 1
```

## Common Pitfalls

| Problem | Cause | Fix |
|---------|-------|-----|
| `ModuleNotFoundError` on import | File named `my_net.py` but class is `MyNetwork` | Class must be `MyNet` — strict `snake_case` → `CamelCase` conversion |
| Model not found | `--model_name` doesn't match file name | `--model_name foo_bar` expects `model/foo_bar.py` with `class FooBar` |
| Config not applied | CLI args override YAML | YAML only fills args that are `None`; explicit CLI wins |
| `train=True/False` ignored | Dataset `__init__` doesn't accept `train` param | Add `train` parameter to your custom dataset |
