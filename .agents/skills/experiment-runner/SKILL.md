---
name: experiment-runner
description: "Run planned local-first training or evaluation with provenance and immutable run records. Use for Stage 2 execution; cloud launches need authorization."
---

# Experiment Runner

Execute approved experiments from immutable configuration to verified artifacts. Start with
the current project environment and a minimal local smoke; remote or paid execution is an
explicitly authorized extension, not the default.

## Inputs

- `docs/05_experiment_plan.md` — claim, run order, baselines, metrics, stop rules;
- `docs/06_result_tables.md` — result cells and provenance links to fill;
- `docs/07_experiment_tracker.md` — run history and deviations;
- `docs/04_methodology.md` and `docs/03_idea_report.md` — method and claims;
- project code, data contract, immutable configs, and environment description.

## Execution contract

### 1. Discover

1. Read the project `AGENTS.md`, environment files, entry points, configs, tests, registry,
   data boundary, and expected outputs.
2. Detect the active project environment and available hardware. Do not assume a global Conda
   environment, reconfigure global package mirrors, or install into an unrelated interpreter.
3. Resolve the exact claim, config, dataset/split, baseline, metric, seed policy, cost limit,
   and stop condition for the next run.

### 2. Preflight

1. Create a new experiment ID and freeze the config; never edit a config tied to a reported run.
2. Validate imports, configuration parsing, data schema/shape/unit checks, split leakage,
   output/log/checkpoint paths, metric implementation, and available disk/memory/accelerator.
3. Record missing dependencies and proposed environment changes before applying them.
4. Distinguish static plausibility from runtime evidence. A lint, import, or compile pass is not
   proof that training or evaluation works.

### 3. Local smoke

Run the smallest meaningful authorized check first:

- tiny or synthetic sample where scientifically valid;
- one forward pass and backward pass when applicable;
- one metric calculation and aggregation-unit check;
- checkpoint save/load round-trip;
- expected exit code, log, structured metric, and artifact creation.

If local hardware cannot run the smoke, report the exact limitation and obtain authorization
before using remote or paid compute.

### 4. Formal execution

For a local command without an existing scheduler/registry integration, use `scripts/run_recorded.py` to register STARTING/RUNNING before execution and preserve terminal status, stdout/stderr, config snapshot and output hashes. It refuses reused IDs and pre-existing output paths. Example (paths are project-relative except the resolved Skill script):

```text
python -B <skill-dir>/scripts/run_recorded.py run --project . --id EXP-001 --config experiments/configs/EXP-001.json --claim C1 --dataset-version <version-or-hash> --split <split-id> --seed 7 --code-revision <commit-or-code-hash> --expect results/data/EXP-001.json --timeout 600 -- python experiments/src/train.py --config experiments/configs/EXP-001.json
python -B <skill-dir>/scripts/run_recorded.py status --project . --id EXP-001
```

Use a timeout only when termination of this newly launched child is covered by the resource contract. It does not terminate remote jobs or descendant process trees. The status command reads the last recorded state; after a supervisor crash, verify liveness and reconcile the registry from `state.json` before resubmitting. The helper is not a scheduler or a scientific-result validator. Keep the existing scheduler when it already provides these guarantees; do not wrap a program that independently owns the same registry. Record package versions, hardware and checkpoint paths in addition to the helper's defaults.

At successful completion the helper freezes output hashes in `state.json` and, when the registry has these columns, writes `result_sha256` and `state_path`. External schedulers must likewise freeze hashes at completion. For manuscript tables run the project's result builder with `--strict --metric <predeclared-primary-metric>`; do not backfill a historical hash from a changed result. Older registries can use the recorded `log_path/state.json` terminal hashes.


1. Launch in the approved local or remote environment with the immutable run ID and config.
2. For SSH, SLURM, cloud, or paid GPU, check existing authorization for destination, resources, upload scope, command and recovery/termination method. Request only missing or changed scope before launch.
3. Monitor concise completion and error signals at a fixed sensible interval; do not churn on
   full logs or repeatedly shorten polling.
4. Accept evidence only from the same real run: exit code, log, checkpoint, structured metrics,
   config hash, code revision, dataset/split, environment, and hardware.
5. Fill result tables and tracker with paths and provenance, including failed and null results.

### 5. Diagnose and recover

1. Diagnose from the traceback, logs, metrics, config, data, and resource evidence.
2. Propose the smallest causal repair. Do not blindly divide learning rate, increase epochs,
   change the split, or weaken evaluation until a target metric appears.
3. Any repair creates a new immutable config and run ID linked to the failed run.
4. Make at most three evidence-based repairs for the same fault and stage, cumulatively across run IDs and handoffs; then stop that path and obtain any additional authorization.

### 6. Verify and hand off

- Verify expected artifacts, metric definitions, checkpoint readability, result-table agreement,
  and experiment-registry completeness.
- Report what was statically checked, smoke-tested, and formally executed as separate evidence.
- Continue to Gate C only when protocol integrity holds; otherwise route to rerun, design repair,
  claim weakening, or Stage 1.

## Completion report

For every run report: run ID, claim, status, config/hash, environment/hardware, dataset/split,
seed, command, duration, exit code, log, outputs/checkpoint, metrics/uncertainty, deviation,
diagnosis, and next action.

## References

| File | Open when |
|---|---|
| `references/research-discipline.md` | Planning run order, project structure, or evidence discipline |
| `references/dl-failure-patterns.md` | Diagnosing training failures without blind tuning |
| `references/gpu-setup.md` | A user-authorized remote GPU path is actually required |
| `scripts/run_recorded.py` | A local command needs durable run identity, provenance and failure records |
| `scripts/validate.sh` | Checking a generated Bash monitor of its documented format; not a heartbeat/scheduler validator |
