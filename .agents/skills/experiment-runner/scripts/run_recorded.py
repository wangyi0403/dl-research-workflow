"""Run an authorized local command with immutable identity and durable failure evidence."""
from __future__ import annotations

import argparse
import contextlib
import csv
import hashlib
import json
import os
import platform
import re
import subprocess
import sys
import tempfile
import time
from datetime import datetime, timezone
from pathlib import Path


def timestamp() -> str:
    return datetime.now(timezone.utc).isoformat()


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def inside(root: Path, relative: str) -> Path:
    path = (root / relative).resolve()
    if not path.is_relative_to(root) or path == root:
        raise ValueError(f"Path escapes the project: {relative}")
    return path


def atomic_json(path: Path, data: dict) -> None:
    descriptor, name = tempfile.mkstemp(prefix=".state-", suffix=".tmp", dir=path.parent)
    temporary = Path(name)
    try:
        with os.fdopen(descriptor, "w", encoding="utf-8") as handle:
            json.dump(data, handle, indent=2, ensure_ascii=False, allow_nan=False)
            handle.flush(); os.fsync(handle.fileno())
        os.replace(temporary, path)
    finally:
        temporary.unlink(missing_ok=True)


@contextlib.contextmanager
def registry_lock(registry: Path):
    lock = registry.with_suffix(".csv.lock")
    try:
        descriptor = os.open(lock, os.O_WRONLY | os.O_CREAT | os.O_EXCL, 0o600)
    except FileExistsError as exc:
        raise RuntimeError("Registry is locked; inspect its owner before retrying, do not delete an active lock") from exc
    try:
        with os.fdopen(descriptor, "w", encoding="ascii") as handle:
            handle.write(str(os.getpid()))
        yield
    finally:
        lock.unlink(missing_ok=True)


def update_registry(registry: Path, row: dict, *, insert: bool) -> None:
    with registry_lock(registry):
        with registry.open(encoding="utf-8-sig", newline="") as handle:
            reader = csv.DictReader(handle)
            fields = reader.fieldnames
            records = list(reader)
        required = {"experiment_id", "status", "config_sha256", "result_path", "log_path"}
        if not fields or not required.issubset(fields):
            raise ValueError("Experiment registry does not have the required provenance fields")
        matches = [index for index, record in enumerate(records) if record["experiment_id"] == row["experiment_id"]]
        if insert and matches:
            raise ValueError("Experiment ID already exists; use a new ID")
        if not insert and len(matches) != 1:
            raise ValueError("Cannot update an absent or ambiguous Experiment ID")
        if insert:
            records.append({name: row.get(name, "") for name in fields})
        else:
            records[matches[0]].update({name: value for name, value in row.items() if name in fields})
        descriptor, name = tempfile.mkstemp(prefix=".registry-", suffix=".tmp", dir=registry.parent)
        temporary = Path(name)
        try:
            with os.fdopen(descriptor, "w", newline="", encoding="utf-8") as handle:
                writer = csv.DictWriter(handle, fieldnames=fields)
                writer.writeheader(); writer.writerows(records)
                handle.flush(); os.fsync(handle.fileno())
            os.replace(temporary, registry)
        finally:
            temporary.unlink(missing_ok=True)


def run(args) -> int:
    root = args.project.resolve()
    if not re.fullmatch(r"[A-Za-z0-9][A-Za-z0-9_.-]{0,95}", args.id):
        raise ValueError("Experiment ID must be a simple unique name")
    config = inside(root, args.config)
    registry = inside(root, "experiments/registry/experiments.csv")
    if not config.is_file() or not registry.is_file():
        raise ValueError("Config and initialized experiment registry must exist")
    outputs = [inside(root, value) for value in args.expect]
    if any(path.exists() for path in outputs):
        raise ValueError("Expected output already exists; refusing to accept or overwrite a stale artifact")
    command = list(args.command)
    if command and command[0] == "--":
        command.pop(0)
    if not command:
        raise ValueError("An explicit command is required")
    if args.timeout is not None and args.timeout <= 0:
        raise ValueError("Timeout must be positive")
    with registry_lock(registry):
        with registry.open(encoding="utf-8-sig", newline="") as handle:
            if any(row.get("experiment_id") == args.id for row in csv.DictReader(handle)):
                raise ValueError("Experiment ID already exists; use a new ID even when prior logs are absent")
    log_root = inside(root, f"results/logs/{args.id}")
    log_root.mkdir(parents=True, exist_ok=False)
    state_path = log_root / "state.json"
    config_hash = sha256(config)
    (log_root / "config.snapshot").write_bytes(config.read_bytes())
    state = {
        "experiment_id": args.id, "status": "STARTING", "runner_pid": os.getpid(),
        "child_pid": None, "command": command, "config_path": args.config,
        "config_sha256": config_hash, "started_at": timestamp(), "ended_at": None,
        "timeout_seconds": args.timeout, "exit_code": None, "failure_reason": "",
        "stdout": (log_root / "stdout.log").relative_to(root).as_posix(),
        "stderr": (log_root / "stderr.log").relative_to(root).as_posix(),
        "expected_outputs": args.expect,
    }
    row = {
        "experiment_id": args.id, "status": "STARTING", "claim_id": args.claim,
        "config_path": args.config, "config_sha256": config_hash,
        "dataset_version": args.dataset_version, "split": args.split, "seed": args.seed,
        "code_revision": args.code_revision, "environment": args.environment,
        "hardware": args.hardware, "command": json.dumps(command),
        "started_at": state["started_at"], "log_path": log_root.relative_to(root).as_posix(),
        "result_path": args.expect[0],
        "state_path": state_path.relative_to(root).as_posix(),
    }
    atomic_json(state_path, state)
    registered = False
    child = None
    started = time.monotonic()
    exit_code = 1
    try:
        update_registry(registry, row, insert=True)
        registered = True
        with (log_root / "stdout.log").open("wb") as stdout, (log_root / "stderr.log").open("wb") as stderr:
            child = subprocess.Popen(command, cwd=root, stdout=stdout, stderr=stderr, shell=False,
                                     creationflags=subprocess.CREATE_NO_WINDOW if os.name == "nt" else 0)
            state.update(status="RUNNING", child_pid=child.pid)
            atomic_json(state_path, state)
            row["status"] = "RUNNING"
            update_registry(registry, row, insert=False)
            try:
                exit_code = child.wait(timeout=args.timeout)
            except subprocess.TimeoutExpired:
                child.kill(); child.wait()
                exit_code = 124
                state["failure_reason"] = "Authorized wall-clock timeout exceeded; only the launched child was terminated"
        if exit_code:
            state["failure_reason"] = state["failure_reason"] or f"Command exited with {exit_code}"
        elif sha256(config) != config_hash:
            exit_code = 1; state["failure_reason"] = "Config changed during the run"
        elif any(not path.is_file() or path.stat().st_size == 0 for path in outputs):
            exit_code = 1; state["failure_reason"] = "Expected nonempty output is missing"
        else:
            state["output_hashes"] = {path.relative_to(root).as_posix(): sha256(path) for path in outputs}
    except (Exception, KeyboardInterrupt) as exc:
        if child is not None and child.poll() is None:
            child.kill(); child.wait()
        exit_code = 1
        state["failure_reason"] = f"{type(exc).__name__}: {exc}"
    finally:
        state.update(status="COMPLETE" if exit_code == 0 else "FAILED", exit_code=exit_code,
                     ended_at=timestamp(), elapsed_seconds=time.monotonic() - started)
        atomic_json(state_path, state)
        if registered:
            row.update(status=state["status"], ended_at=state["ended_at"],
                       result_sha256=state.get("output_hashes", {}).get(outputs[0].relative_to(root).as_posix(), ""),
                       notes=json.dumps({"exit_code": exit_code, "failure_reason": state["failure_reason"],
                                         "state_path": state_path.relative_to(root).as_posix()}))
            try:
                update_registry(registry, row, insert=False)
            except Exception as exc:
                state["registry_update_error"] = f"{type(exc).__name__}: {exc}"
                state.update(status="FAILED", exit_code=2, failure_reason="Result produced but registry update failed; reconcile from this state before continuing")
                atomic_json(state_path, state)
                exit_code = 2
    print(json.dumps({"experiment_id": args.id, "status": state["status"], "state_path": str(state_path),
                      "failure_reason": state["failure_reason"], "registry_update_error": state.get("registry_update_error")}, ensure_ascii=False))
    return exit_code


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    subparsers = parser.add_subparsers(dest="action", required=True)
    execute = subparsers.add_parser("run")
    execute.add_argument("--project", type=Path, required=True)
    execute.add_argument("--id", required=True)
    execute.add_argument("--config", required=True)
    execute.add_argument("--claim", required=True)
    execute.add_argument("--dataset-version", required=True)
    execute.add_argument("--split", required=True)
    execute.add_argument("--seed", type=int, required=True)
    execute.add_argument("--code-revision", required=True)
    execute.add_argument("--environment", default=f"Python {platform.python_version()}; record package versions in project state")
    execute.add_argument("--hardware", default=f"local {platform.machine()}; accelerator not inferred")
    execute.add_argument("--expect", action="append", required=True, help="New project-relative output file; repeat for multiple outputs")
    execute.add_argument("--timeout", type=float, help="Authorized wall-clock limit for the launched child process only")
    execute.add_argument("command", nargs=argparse.REMAINDER)
    status = subparsers.add_parser("status")
    status.add_argument("--project", type=Path, required=True)
    status.add_argument("--id", required=True)
    args = parser.parse_args()
    try:
        if not re.fullmatch(r"[A-Za-z0-9][A-Za-z0-9_.-]{0,95}", args.id):
            raise ValueError("Experiment ID must be a simple unique name")
        if args.action == "status":
            path = inside(args.project.resolve(), f"results/logs/{args.id}/state.json")
            print(path.read_text(encoding="utf-8"))
            return 0
        return run(args)
    except (OSError, ValueError, RuntimeError) as exc:
        print(str(exc), file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
