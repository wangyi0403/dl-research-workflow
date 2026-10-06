"""Behavioral checks for paper-table provenance and local-runner interoperability."""
from __future__ import annotations

import csv
import hashlib
import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest


PROJECT = Path(__file__).resolve().parents[2]
BUILDER = PROJECT / "experiments/scripts/build_result_tables.py"
REGISTRY_TEMPLATE = PROJECT / "experiments/registry/experiments.csv"


def find_runner() -> Path | None:
    candidates = [PROJECT / ".agents/skills/experiment-runner/scripts/run_recorded.py"]
    candidates.extend(
        parent / "library/skills/experiment-runner/scripts/run_recorded.py"
        for parent in PROJECT.parents
    )
    return next((path for path in candidates if path.is_file()), None)


RUNNER = find_runner()


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


class ResultTableTests(unittest.TestCase):
    def setUp(self) -> None:
        self.temporary = tempfile.TemporaryDirectory(prefix="research-result-tables-")
        self.addCleanup(self.temporary.cleanup)
        self.root = Path(self.temporary.name)
        self.registry = self.root / "experiments/registry/experiments.csv"
        self.registry.parent.mkdir(parents=True)
        with REGISTRY_TEMPLATE.open(encoding="utf-8-sig", newline="") as handle:
            self.fields = next(csv.reader(handle))
        self.write_records([])

    def write_records(self, records: list[dict]) -> None:
        with self.registry.open("w", encoding="utf-8", newline="") as handle:
            writer = csv.DictWriter(handle, fieldnames=self.fields)
            writer.writeheader()
            writer.writerows(records)

    def read_records(self) -> list[dict]:
        with self.registry.open(encoding="utf-8-sig", newline="") as handle:
            return list(csv.DictReader(handle))

    def execute(self, script: Path, *arguments: str) -> subprocess.CompletedProcess:
        environment = os.environ.copy()
        environment["PYTHONDONTWRITEBYTECODE"] = "1"
        return subprocess.run(
            [sys.executable, "-B", str(script), *map(str, arguments)],
            cwd=self.root, env=environment, capture_output=True, text=True,
            encoding="utf-8", timeout=30, check=False,
            creationflags=subprocess.CREATE_NO_WINDOW if os.name == "nt" else 0,
        )

    def build(self, *arguments: str) -> subprocess.CompletedProcess:
        return self.execute(BUILDER, "--project", self.root, *arguments)

    def assert_success(self, result: subprocess.CompletedProcess) -> None:
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)

    def assert_rejected(self, result: subprocess.CompletedProcess, message: str) -> None:
        self.assertNotEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertIn(message, result.stderr)

    def recorded_run(self, experiment: str = "run-1", metrics: dict | None = None) -> dict:
        if RUNNER is None:
            self.skipTest("Install the experiment-runner profile to run integration checks")
        config = self.root / f"experiments/configs/{experiment}.json"
        config.parent.mkdir(parents=True, exist_ok=True)
        config.write_text('{"seed": 7}', encoding="utf-8")
        result_relative = f"results/data/{experiment}.json"
        payload = {"metrics": {"accuracy": 0.8, "loss": 0.2} if metrics is None else metrics}
        code = (
            "import json; from pathlib import Path; "
            f"p = Path({result_relative!r}); "
            "p.parent.mkdir(parents=True, exist_ok=True); "
            f"p.write_text(json.dumps({payload!r}), encoding='utf-8')"
        )
        outcome = self.execute(
            RUNNER, "run", "--project", self.root, "--id", experiment,
            "--config", config.relative_to(self.root).as_posix(),
            "--claim", "C-1", "--dataset-version", "D-1", "--split", "S-1",
            "--seed", "7", "--code-revision", "fixture-revision",
            "--environment", "stdlib-only fixture", "--hardware", "local CPU",
            "--expect", result_relative, "--timeout", "10", "--",
            sys.executable, "-B", "-c", code,
        )
        self.assert_success(outcome)
        return next(row for row in self.read_records() if row["experiment_id"] == experiment)

    def scheduler_run(
        self, experiment: str = "scheduler-1", *, metrics: dict | None = None,
        result_relative: str | None = None, claim: str = "C-1",
    ) -> dict:
        config = self.root / f"experiments/configs/{experiment}.json"
        config.parent.mkdir(parents=True, exist_ok=True)
        config.write_text('{"seed": 11}', encoding="utf-8")
        result = self.root / (result_relative or f"results/data/{experiment}.json")
        result.parent.mkdir(parents=True, exist_ok=True)
        result.write_text(json.dumps({"metrics": {"accuracy": 0.75} if metrics is None else metrics}), encoding="utf-8")
        row = {name: "" for name in self.fields}
        row.update(
            experiment_id=experiment, status="COMPLETE", claim_id=claim,
            config_path=config.relative_to(self.root).as_posix(), config_sha256=digest(config),
            dataset_version="D-1", split="S-1", seed="11", code_revision="fixture-revision",
            environment="stdlib-only fixture", hardware="local CPU", command="external-scheduler fixture",
            started_at="2026-01-01T00:00:00Z", ended_at="2026-01-01T00:00:01Z",
            log_path=f"results/logs/{experiment}", result_path=result.relative_to(self.root).as_posix(),
            result_sha256=digest(result), state_path="",
        )
        self.write_records([*self.read_records(), row])
        return row

    def test_real_recorded_runs_pass_strict_metrics_and_frozen_hashes(self) -> None:
        first = self.recorded_run()
        second = self.recorded_run("run-2", {"accuracy": 0.9, "loss": 0.1})
        self.assert_success(self.build("--strict", "--metric", "accuracy", "--metric", "loss"))
        with (self.root / "results/tables/run_metrics.csv").open(newline="", encoding="utf-8") as handle:
            rows = list(csv.DictReader(handle))
        self.assertEqual([row["experiment_id"] for row in rows], ["run-1", "run-2"])
        for output, source in zip(rows, [first, second]):
            self.assertEqual(output["result_sha256"], digest(self.root / source["result_path"]))
            self.assertEqual(output["config_sha256"], source["config_sha256"])
            self.assertTrue(output["metric:accuracy"])
            self.assertTrue(output["metric:loss"])

    def test_result_rewrite_is_rejected(self) -> None:
        row = self.recorded_run()
        (self.root / row["result_path"]).write_text('{"metrics": {"accuracy": 1.0}}', encoding="utf-8")
        self.assert_rejected(self.build("--strict", "--metric", "accuracy"), "Result hash mismatch")

    def test_config_rewrite_is_rejected(self) -> None:
        row = self.recorded_run()
        (self.root / row["config_path"]).write_text('{"seed": 99}', encoding="utf-8")
        self.assert_rejected(self.build("--strict", "--metric", "accuracy"), "Config hash mismatch")

    def test_missing_provenance_is_rejected(self) -> None:
        row = self.scheduler_run()
        row["environment"] = ""
        self.write_records([row])
        self.assert_rejected(self.build("--strict", "--metric", "accuracy"), "Incomplete provenance")

    def test_empty_metrics_are_rejected(self) -> None:
        self.scheduler_run(metrics={})
        for options in [[], ["--strict", "--metric", "accuracy"]]:
            with self.subTest(options=options):
                self.assert_rejected(self.build(*options), "nonempty metrics object")

    def test_primary_metrics_are_required_on_every_selected_run(self) -> None:
        self.scheduler_run("complete", metrics={"accuracy": 0.8, "loss": 0.2})
        self.scheduler_run("incomplete", metrics={"accuracy": 0.9})
        self.assert_rejected(self.build("--strict", "--metric", "accuracy", "--metric", "loss"), "Missing required metrics for incomplete")

    def test_empty_claim_selection_is_rejected(self) -> None:
        self.scheduler_run()
        self.assert_rejected(self.build("--strict", "--metric", "accuracy", "--claim-id", "absent"), "No COMPLETE runs")

    def test_expected_batch_is_selected_and_complete(self) -> None:
        self.scheduler_run("planned-1")
        self.scheduler_run("planned-2")
        self.scheduler_run("unrelated", claim="C-2", metrics={"other": 0.1})
        outcome = self.build("--strict", "--metric", "accuracy", "--expect-run", "planned-1", "--expect-run", "planned-2")
        self.assert_success(outcome)
        self.assertIn("2/2 COMPLETE", outcome.stdout)
        with (self.root / "results/tables/run_metrics.csv").open(newline="", encoding="utf-8") as handle:
            self.assertEqual([row["experiment_id"] for row in csv.DictReader(handle)], ["planned-1", "planned-2"])

    def test_expected_missing_or_unfinished_run_blocks_output(self) -> None:
        first = self.scheduler_run("planned-1")
        second = self.scheduler_run("planned-2")
        for status in ["FAILED", "RUNNING", "CANCELLED", ""]:
            with self.subTest(status=status):
                second["status"] = status
                self.write_records([first, second])
                outcome = self.build("--strict", "--metric", "accuracy", "--expect-run", "planned-1", "--expect-run", "planned-2")
                self.assert_rejected(outcome, "Expected run coverage incomplete")
                self.assertIn("planned-2", outcome.stderr)
                self.assertFalse((self.root / "results/tables/run_metrics.csv").exists())
        self.write_records([first])
        self.assert_rejected(self.build("--strict", "--metric", "accuracy", "--expect-run", "planned-2"), "missing registry record")

    def test_expected_run_claim_conflict_is_not_silently_filtered(self) -> None:
        self.scheduler_run("planned", claim="C-2")
        self.assert_rejected(self.build("--strict", "--metric", "accuracy", "--claim-id", "C-1", "--expect-run", "planned"), "excluded by --claim-id")

    def test_duplicate_expected_registry_id_is_ambiguous(self) -> None:
        row = self.scheduler_run("planned")
        failed = dict(row, status="FAILED")
        self.write_records([failed, row])
        self.assert_rejected(self.build("--strict", "--metric", "accuracy", "--expect-run", "planned"), "Duplicate expected experiment_id")

    def test_invalid_expected_id_and_missing_coverage_declaration(self) -> None:
        self.scheduler_run("planned")
        self.assert_rejected(self.build("--expect-run", " "), "Expected run IDs must be nonempty")
        outcome = self.build("--strict", "--metric", "accuracy", "--dry-run")
        self.assert_success(outcome)
        self.assertIn("Planned run coverage is not checked", outcome.stderr)
        self.assertFalse((self.root / "results/tables/run_metrics.csv").exists())

    def test_strict_mode_requires_predeclared_metrics(self) -> None:
        self.scheduler_run()
        self.assert_rejected(self.build("--strict"), "requires --metric")

    def test_scheduler_frozen_hash_without_state_is_accepted(self) -> None:
        row = self.scheduler_run()
        self.assertFalse((self.root / row["log_path"] / "state.json").exists())
        self.assert_success(self.build("--strict", "--metric", "accuracy"))

    def test_legacy_runner_uses_log_directory_terminal_hash(self) -> None:
        row = self.recorded_run()
        row["result_sha256"] = ""
        row["state_path"] = ""
        self.write_records([row])
        self.assert_success(self.build("--strict", "--metric", "accuracy"))

    def test_missing_frozen_hash_is_rejected(self) -> None:
        row = self.scheduler_run()
        row["result_sha256"] = ""
        self.write_records([row])
        self.assert_rejected(self.build("--strict", "--metric", "accuracy"), "No frozen result hash")

    def test_terminal_state_conflicts_are_rejected(self) -> None:
        row = self.recorded_run()
        state_path = self.root / row["state_path"]
        state = json.loads(state_path.read_text(encoding="utf-8"))
        state["status"] = "FAILED"
        state_path.write_text(json.dumps(state), encoding="utf-8")
        self.assert_rejected(self.build("--strict", "--metric", "accuracy"), "Invalid terminal state")

    def test_registry_and_state_hash_disagreement_is_rejected(self) -> None:
        row = self.recorded_run()
        row["result_sha256"] = "0" * 64
        self.write_records([row])
        self.assert_rejected(self.build("--strict", "--metric", "accuracy"), "conflicting frozen result hash")

    def test_output_cannot_overwrite_registry_or_raw_result(self) -> None:
        row = self.scheduler_run()
        for relative in ["experiments/registry/experiments.csv", row["result_path"]]:
            with self.subTest(path=relative):
                asset = self.root / relative
                before = asset.read_bytes()
                self.assert_rejected(self.build("--strict", "--metric", "accuracy", "--overwrite", "--output", relative), "Output must be a CSV")
                self.assertEqual(asset.read_bytes(), before)

    def test_output_cannot_overwrite_selected_source_inside_tables(self) -> None:
        row = self.scheduler_run(result_relative="results/tables/source.csv")
        before = (self.root / row["result_path"]).read_bytes()
        self.assert_rejected(self.build("--strict", "--metric", "accuracy", "--overwrite", "--output", row["result_path"]), "source result file")
        self.assertEqual((self.root / row["result_path"]).read_bytes(), before)

    def test_output_cannot_overwrite_excluded_source_inside_tables(self) -> None:
        self.scheduler_run("included", claim="C-1")
        excluded = self.scheduler_run("excluded", claim="C-2", result_relative="results/tables/excluded.csv")
        before = (self.root / excluded["result_path"]).read_bytes()
        outcome = self.build("--strict", "--metric", "accuracy", "--claim-id", "C-1", "--overwrite", "--output", excluded["result_path"])
        self.assertNotEqual(outcome.returncode, 0, "A filtered-out source result must remain protected")
        self.assertEqual((self.root / excluded["result_path"]).read_bytes(), before)

    def test_exploratory_mode_supports_legacy_sparse_provenance(self) -> None:
        first = self.scheduler_run("first", metrics={"accuracy": 0.8})
        second = self.scheduler_run("second", metrics={"loss": 0.3})
        for row in [first, second]:
            row["result_sha256"] = ""
            row["environment"] = ""
        self.write_records([first, second])
        outcome = self.build()
        self.assert_success(outcome)
        self.assertIn("Exploratory mode", outcome.stderr)
        with (self.root / "results/tables/run_metrics.csv").open(newline="", encoding="utf-8") as handle:
            rows = list(csv.DictReader(handle))
        self.assertEqual(rows[0]["metric:loss"], "")
        self.assertEqual(rows[1]["metric:accuracy"], "")


if __name__ == "__main__":
    unittest.main()
