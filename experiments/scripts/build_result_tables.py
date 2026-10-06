#!/usr/bin/env python3
"""Build a provenance-preserving, run-level metrics CSV from the experiment registry."""

from __future__ import annotations

import argparse
import csv
import hashlib
import io
import json
import math
import os
import re
import sys
import tempfile
from pathlib import Path
from typing import Any


DEFAULT_OUTPUT = Path("results/tables/run_metrics.csv")
METADATA_COLUMNS = [
    "experiment_id",
    "status",
    "claim_id",
    "dataset_version",
    "split",
    "seed",
    "code_revision",
    "config_sha256",
    "result_path",
    "result_sha256",
]
REQUIRED_REGISTRY_COLUMNS = {"experiment_id", "status", "result_path"}
PROVENANCE_COLUMNS = {
    "claim_id", "config_path", "config_sha256", "dataset_version", "split", "seed",
    "code_revision", "environment", "hardware", "command", "started_at", "ended_at", "log_path",
}


def verify_provenance(project: Path, record: dict, result_path: Path, digest: str) -> None:
    """Compare inputs with hashes frozen by the runner or an external scheduler."""
    experiment_id = record["experiment_id"]
    missing = sorted(name for name in PROVENANCE_COLUMNS if not (record.get(name) or "").strip())
    if missing:
        raise ValueError(f"Incomplete provenance for {experiment_id}: {', '.join(missing)}")
    config_hash = record["config_sha256"].strip().lower()
    config = confined_path(project, Path(record["config_path"]), must_exist=True)
    if not re.fullmatch(r"[0-9a-f]{64}", config_hash) or sha256_file(config) != config_hash:
        raise ValueError(f"Config hash mismatch for {experiment_id}")

    expected_hash = (record.get("result_sha256") or "").strip().lower()
    state_ref = (record.get("state_path") or "").strip()
    state_path = confined_path(
        project, Path(state_ref) if state_ref else Path(record["log_path"]) / "state.json",
        must_exist=bool(state_ref),
    )
    if state_path.is_file():
        state = json.loads(state_path.read_text(encoding="utf-8-sig"))
        if (not isinstance(state, dict) or state.get("experiment_id") != experiment_id
                or state.get("status") != "COMPLETE" or state.get("exit_code") != 0
                or state.get("config_sha256") != config_hash):
            raise ValueError(f"Invalid terminal state for {experiment_id}")
        output_hashes = state.get("output_hashes")
        frozen_hash = output_hashes.get(result_path.relative_to(project).as_posix()) if isinstance(output_hashes, dict) else None
        if not isinstance(frozen_hash, str) or (expected_hash and expected_hash != frozen_hash.lower()):
            raise ValueError(f"Missing or conflicting frozen result hash for {experiment_id}")
        expected_hash = frozen_hash.lower()
    if not re.fullmatch(r"[0-9a-f]{64}", expected_hash):
        raise ValueError(f"No frozen result hash for {experiment_id}; record it at run completion")
    if expected_hash != digest:
        raise ValueError(f"Result hash mismatch for {experiment_id}; source changed after completion")


def confined_path(root: Path, candidate: Path, *, must_exist: bool) -> Path:
    """Resolve a path and reject paths (including symlinks) outside the project."""
    path = candidate if candidate.is_absolute() else root / candidate
    resolved = path.resolve(strict=must_exist)
    try:
        resolved.relative_to(root)
    except ValueError as exc:
        raise ValueError(f"Path is outside the project: {candidate}") from exc
    return resolved


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def load_completed_runs(
    project: Path, claim_id: str | None, *, strict: bool = False,
    required_metrics: list[str] | None = None,
    expected_runs: list[str] | None = None,
) -> tuple[list[dict[str, Any]], int, list[str]]:
    registry = confined_path(
        project, Path("experiments/registry/experiments.csv"), must_exist=True
    )
    completed: list[dict[str, Any]] = []
    skipped = 0
    metric_names: set[str] = set()
    experiment_ids: set[str] = set()
    expected_ids = set(expected_runs or [])
    if any(not name.strip() or name != name.strip() for name in expected_ids):
        raise ValueError("Expected run IDs must be nonempty and have no surrounding whitespace")
    expected_seen: set[str] = set()
    coverage_gaps: dict[str, str] = {}

    with registry.open("r", encoding="utf-8-sig", newline="") as handle:
        reader = csv.DictReader(handle)
        missing = REQUIRED_REGISTRY_COLUMNS - set(reader.fieldnames or [])
        if missing:
            raise ValueError(
                "Experiment registry is missing columns: " + ", ".join(sorted(missing))
            )

        for line_number, record in enumerate(reader, start=2):
            experiment_id = (record.get("experiment_id") or "").strip()
            status = (record.get("status") or "").strip().upper()
            if expected_ids:
                if experiment_id not in expected_ids:
                    continue
                if experiment_id in expected_seen:
                    raise ValueError(f"Duplicate expected experiment_id: {experiment_id}")
                expected_seen.add(experiment_id)
                if status != "COMPLETE":
                    coverage_gaps[experiment_id] = f"status={status or 'empty'}"
                elif claim_id and (record.get("claim_id") or "").strip() != claim_id:
                    coverage_gaps[experiment_id] = "excluded by --claim-id"
            if status != "COMPLETE":
                skipped += 1
                continue
            if claim_id and (record.get("claim_id") or "").strip() != claim_id:
                continue
            if not experiment_id:
                raise ValueError(f"Registry line {line_number} has no experiment_id")
            if experiment_id in experiment_ids:
                raise ValueError(f"Duplicate completed experiment_id: {experiment_id}")
            experiment_ids.add(experiment_id)

            raw_result_path = (record.get("result_path") or "").strip()
            if not raw_result_path:
                raise ValueError(
                    f"Completed experiment {experiment_id} has no result_path"
                )
            result_path = confined_path(
                project, Path(raw_result_path), must_exist=True
            )
            try:
                result_bytes = result_path.read_bytes()
                result = json.loads(result_bytes.decode("utf-8-sig"))
            except (OSError, json.JSONDecodeError) as exc:
                raise ValueError(
                    f"Cannot read JSON result for {experiment_id}: {raw_result_path}: {exc}"
                ) from exc

            metrics = result.get("metrics") if isinstance(result, dict) else None
            if not isinstance(metrics, dict) or not metrics:
                raise ValueError(
                    f"Result for {experiment_id} must contain a nonempty metrics object"
                )
            result_hash = hashlib.sha256(result_bytes).hexdigest()
            if strict:
                verify_provenance(project, record, result_path, result_hash)
                missing_metrics = set(required_metrics or []) - set(metrics)
                if missing_metrics:
                    raise ValueError(f"Missing required metrics for {experiment_id}: {', '.join(sorted(missing_metrics))}")
            clean_metrics: dict[str, int | float] = {}
            for name, value in metrics.items():
                if not isinstance(name, str) or not name.strip():
                    raise ValueError(f"Result for {experiment_id} has an empty metric name")
                if isinstance(value, bool) or not isinstance(value, (int, float)):
                    raise ValueError(
                        f"Metric {name!r} for {experiment_id} is not a numeric scalar"
                    )
                if not math.isfinite(value):
                    raise ValueError(f"Metric {name!r} for {experiment_id} is not finite")
                clean_metrics[name] = value
                metric_names.add(name)

            completed.append(
                {
                    "registry": record,
                    "experiment_id": experiment_id,
                    "result_path": result_path,
                    "result_relative_path": result_path.relative_to(project).as_posix(),
                    "result_sha256": result_hash,
                    "metrics": clean_metrics,
                }
            )

    if expected_ids:
        for missing_id in expected_ids - expected_seen:
            coverage_gaps[missing_id] = "missing registry record"
        if coverage_gaps:
            gaps = "; ".join(f"{name} ({coverage_gaps[name]})" for name in sorted(coverage_gaps))
            raise ValueError(f"Expected run coverage incomplete: {gaps}")
    if strict and not completed:
        raise ValueError("No COMPLETE runs match the requested analysis")
    return completed, skipped, sorted(metric_names, key=lambda value: (value.casefold(), value))


def render_csv(
    runs: list[dict[str, Any]], metric_names: list[str], project: Path
) -> str:
    output = io.StringIO(newline="")
    columns = METADATA_COLUMNS + [f"metric:{name}" for name in metric_names]
    writer = csv.DictWriter(output, fieldnames=columns, extrasaction="raise", lineterminator="\n")
    writer.writeheader()

    for run in runs:
        record = run["registry"]
        row: dict[str, Any] = {
            "experiment_id": run["experiment_id"],
            "status": (record.get("status") or "").strip().upper(),
            "claim_id": record.get("claim_id", ""),
            "dataset_version": record.get("dataset_version", ""),
            "split": record.get("split", ""),
            "seed": record.get("seed", ""),
            "code_revision": record.get("code_revision", ""),
            "config_sha256": record.get("config_sha256", ""),
            "result_path": run["result_relative_path"],
            "result_sha256": run["result_sha256"],
        }
        for name in metric_names:
            row[f"metric:{name}"] = run["metrics"].get(name, "")
        writer.writerow(row)
    return output.getvalue()


def write_output(path: Path, content: str, *, overwrite: bool) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if not overwrite:
        with path.open("x", encoding="utf-8", newline="") as handle:
            handle.write(content)
        return

    temporary_path: Path | None = None
    try:
        with tempfile.NamedTemporaryFile(
            mode="w",
            encoding="utf-8",
            newline="",
            prefix=f".{path.name}.",
            suffix=".tmp",
            dir=path.parent,
            delete=False,
        ) as handle:
            temporary_path = Path(handle.name)
            handle.write(content)
        os.replace(temporary_path, path)
    finally:
        if temporary_path is not None and temporary_path.exists():
            temporary_path.unlink()


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description=(
            "Build one CSV row per COMPLETE experiment from result JSON metrics. "
            "The script does not aggregate seeds or calculate statistical tests."
        )
    )
    parser.add_argument(
        "--project",
        type=Path,
        default=Path(__file__).resolve().parents[2],
        help="Project root (default: the template/project containing this script).",
    )
    parser.add_argument(
        "--output",
        type=Path,
        default=DEFAULT_OUTPUT,
        help="CSV destination under results/tables (default: results/tables/run_metrics.csv).",
    )
    parser.add_argument("--claim-id", help="Include only this exact Claim ID.")
    parser.add_argument(
        "--expect-run", action="append", dest="expected_runs",
        help="Select a predeclared run ID and require it to be COMPLETE; repeat for every planned run in this table.",
    )
    parser.add_argument(
        "--strict", action="store_true",
        help="Require complete provenance, frozen input/output hashes and --metric values on every run; use for paper tables.",
    )
    parser.add_argument(
        "--metric",
        action="append",
        dest="metrics",
        help="Include a metric column; repeat to select multiple metrics (default: all).",
    )
    parser.add_argument(
        "--overwrite",
        action="store_true",
        help="Replace an existing output CSV atomically.",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Validate inputs and report the planned output without writing it.",
    )
    return parser


def main() -> int:
    parser = build_parser()
    args = parser.parse_args()
    try:
        project = args.project.resolve(strict=True)
        if not project.is_dir():
            raise ValueError(f"Project path is not a directory: {project}")

        if args.strict and not args.metrics:
            raise ValueError("Strict analysis requires --metric for each predeclared primary metric")
        runs, skipped, available_metrics = load_completed_runs(
            project, args.claim_id, strict=args.strict, required_metrics=args.metrics,
            expected_runs=args.expected_runs,
        )
        metric_names = list(dict.fromkeys(args.metrics or available_metrics))
        unknown_metrics = sorted(set(metric_names) - set(available_metrics))
        if unknown_metrics:
            raise ValueError("Requested metric(s) not found: " + ", ".join(unknown_metrics))

        output_path = confined_path(project, args.output, must_exist=False)
        table_root = project / "results" / "tables"
        if not output_path.is_relative_to(table_root) or output_path == table_root or output_path.suffix.lower() != ".csv":
            raise ValueError("Output must be a CSV under results/tables; source assets cannot be overwritten")
        protected_paths = {
            confined_path(
                project, Path("experiments/registry/experiments.csv"), must_exist=True
            )
        }
        protected_paths.update(run["result_path"] for run in runs)
        # A filtered-out or failed run still owns its source assets.
        registry_path = project / "experiments/registry/experiments.csv"
        with registry_path.open(encoding="utf-8-sig", newline="") as handle:
            for record in csv.DictReader(handle):
                for field in ("result_path", "config_path", "checkpoint_path", "state_path"):
                    raw_path = (record.get(field) or "").strip()
                    if raw_path:
                        protected_paths.add((project / raw_path).resolve())
                raw_log_path = (record.get("log_path") or "").strip()
                if raw_log_path and output_path.is_relative_to((project / raw_log_path).resolve()):
                    raise ValueError("Output path overlaps a run's log/state directory")
        if output_path in protected_paths:
            raise ValueError("Output path matches the registry or a source result file")
        if output_path.exists() and not args.overwrite and not args.dry_run:
            raise FileExistsError(
                f"Output already exists; pass --overwrite to replace it: {output_path}"
            )

        content = render_csv(runs, metric_names, project)
        if not args.strict:
            print("Exploratory mode: frozen provenance is not verified; use --strict --metric NAME before citing in a paper.", file=sys.stderr)
        if args.expected_runs:
            print(f"Expected run coverage verified: {len(set(args.expected_runs))}/{len(set(args.expected_runs))} COMPLETE.")
        else:
            print("Planned run coverage is not checked; pass --expect-run for every predeclared run in this table.", file=sys.stderr)
        if args.dry_run:
            print(
                f"Validated {len(runs)} completed run(s); skipped {skipped} non-COMPLETE "
                f"registry row(s); {len(metric_names)} metric column(s)."
            )
            print(f"Would write: {output_path.relative_to(project).as_posix()}")
            if output_path.exists() and not args.overwrite:
                print("Output exists; a normal run would refuse to overwrite it.")
            return 0

        write_output(output_path, content, overwrite=args.overwrite)
        print(
            f"Wrote {len(runs)} completed run(s); skipped {skipped} non-COMPLETE "
            f"registry row(s); {len(metric_names)} metric column(s)."
        )
        print(f"Output: {output_path.relative_to(project).as_posix()}")
        return 0
    except (OSError, ValueError) as exc:
        print(f"Error: {exc}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
