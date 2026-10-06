"""Exercise successful, failed and interrupted commands without training dependencies."""
import csv
import json
import os
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

RUNNER = Path(__file__).resolve().parents[1] / "scripts/run_recorded.py"
TEMPLATE = Path(__file__).resolve().parents[4] / "experiments/registry/experiments.csv"


class RecordedRunTests(unittest.TestCase):
    def setUp(self):
        self.temporary = tempfile.TemporaryDirectory(prefix="agenthub-run-", dir=os.environ.get("AGENTHUB_TEST_ROOT"))
        self.root = Path(self.temporary.name)
        for folder in ["experiments/configs", "experiments/registry", "results/data"]:
            (self.root / folder).mkdir(parents=True)
        (self.root / "experiments/configs/run.json").write_text('{"seed":7}', encoding="utf-8")
        (self.root / "experiments/registry/experiments.csv").write_bytes(TEMPLATE.read_bytes())

    def tearDown(self):
        self.temporary.cleanup()

    def execute(self, code, *, run_id="test-run", timeout=None):
        args = [sys.executable, "-B", str(RUNNER), "run", "--project", str(self.root), "--id", run_id,
                "--config", "experiments/configs/run.json", "--claim", "C1", "--dataset-version", "synthetic-v1",
                "--split", "test", "--seed", "7", "--code-revision", "fixture-v1",
                "--expect", "results/data/output.json"]
        if timeout is not None:
            args += ["--timeout", str(timeout)]
        return subprocess.run(args + ["--", sys.executable, "-B", "-c", code], capture_output=True, text=True, timeout=10)

    def state(self):
        return json.loads((self.root / "results/logs/test-run/state.json").read_text(encoding="utf-8"))

    def rows(self):
        with (self.root / "experiments/registry/experiments.csv").open(newline="", encoding="utf-8") as handle:
            return list(csv.DictReader(handle))

    def test_success_has_output_hash_and_complete_registry(self):
        result = self.execute("from pathlib import Path; Path('results/data/output.json').write_text('{\"value\":1}')")
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(self.state()["status"], "COMPLETE")
        self.assertIn("results/data/output.json", self.state()["output_hashes"])
        self.assertEqual(self.rows()[0]["status"], "COMPLETE")

    def test_failed_child_keeps_traceback_and_registry(self):
        result = self.execute("raise RuntimeError('deliberate failure')")
        self.assertEqual(result.returncode, 1)
        self.assertEqual(self.state()["status"], "FAILED")
        self.assertEqual(self.rows()[0]["status"], "FAILED")
        self.assertIn("deliberate failure", (self.root / "results/logs/test-run/stderr.log").read_text())

    def test_missing_output_does_not_pass(self):
        result = self.execute("print('finished')")
        self.assertEqual(result.returncode, 1)
        self.assertIn("missing", self.state()["failure_reason"])

    def test_stale_output_prevents_execution(self):
        output = self.root / "results/data/output.json"
        output.write_text("prior evidence", encoding="utf-8")
        result = self.execute("raise RuntimeError('must not execute')")
        self.assertEqual(result.returncode, 2)
        self.assertEqual(output.read_text(), "prior evidence")
        self.assertEqual(self.rows(), [])

    def test_timeout_records_failure(self):
        result = self.execute("import time; time.sleep(30)", timeout=0.15)
        self.assertEqual(result.returncode, 124)
        self.assertEqual(self.state()["status"], "FAILED")
        self.assertLess(self.state()["elapsed_seconds"], 5)

    def test_duplicate_id_preserves_first_failure(self):
        self.execute("raise RuntimeError('original')")
        state_path = self.root / "results/logs/test-run/state.json"
        before = state_path.read_bytes()
        result = self.execute("print('must not execute')")
        self.assertEqual(result.returncode, 2)
        self.assertEqual(state_path.read_bytes(), before)
        self.assertEqual(len(self.rows()), 1)

    def test_config_change_invalidates_result(self):
        result = self.execute("from pathlib import Path; Path('experiments/configs/run.json').write_text('{}'); Path('results/data/output.json').write_text('{}')")
        self.assertEqual(result.returncode, 1)
        self.assertIn("Config changed", self.state()["failure_reason"])
        self.assertEqual((self.root / "results/logs/test-run/config.snapshot").read_text(), '{"seed":7}')

    def test_registry_identity_survives_missing_logs(self):
        registry = self.root / "experiments/registry/experiments.csv"
        with registry.open(encoding="utf-8-sig") as handle:
            fields = next(csv.reader(handle))
        with registry.open("a", newline="", encoding="utf-8") as handle:
            csv.DictWriter(handle, fieldnames=fields).writerow({"experiment_id": "test-run", "status": "COMPLETE"})
        result = self.execute("print('must not run')")
        self.assertEqual(result.returncode, 2)
        self.assertFalse((self.root / "results/logs/test-run").exists())
        self.assertEqual(self.rows()[0]["status"], "COMPLETE")

    def test_status_reads_without_relaunch(self):
        self.execute("raise RuntimeError('original')")
        result = subprocess.run([sys.executable, "-B", str(RUNNER), "status", "--project", str(self.root), "--id", "test-run"], capture_output=True, text=True, timeout=10)
        self.assertEqual(result.returncode, 0)
        self.assertEqual(json.loads(result.stdout)["status"], "FAILED")
        self.assertEqual(len(self.rows()), 1)


if __name__ == "__main__":
    unittest.main()
