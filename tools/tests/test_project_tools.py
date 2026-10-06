"""Check deployment boundaries, profile selection and native adapter copies."""
from pathlib import Path
import json
import subprocess
import sys
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[2]
TOOL = ROOT / "tools/project.py"

class DeploymentTests(unittest.TestCase):
    def setUp(self):
        self.temporary = tempfile.TemporaryDirectory(prefix="research-deployment-")
        self.addCleanup(self.temporary.cleanup)
        self.target = Path(self.temporary.name) / "study"

    def command(self, *args):
        return subprocess.run([sys.executable, "-B", str(TOOL), *map(str, args)], capture_output=True, text=True, encoding="utf-8")

    def test_dry_run_creates_nothing(self):
        result = self.command("init", self.target, "--profile", "research", "--dry-run")
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertFalse(self.target.exists())

    def test_conflict_is_detected_before_writes(self):
        self.target.mkdir()
        existing = self.target / "AGENTS.md"
        existing.write_text("Existing study rules", encoding="utf-8")
        result = self.command("init", self.target)
        self.assertNotEqual(result.returncode, 0)
        self.assertEqual(existing.read_text(encoding="utf-8"), "Existing study rules")
        self.assertEqual(list(self.target.iterdir()), [existing])

    def test_research_then_writing_adds_runtime_without_rewriting_state(self):
        result = self.command("init", self.target, "--profile", "research")
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(len(list((self.target / ".agents/skills").iterdir())), 8)
        self.assertFalse((self.target / ".agenthub/runtime").exists())
        record = self.target / "docs/00_start.md"
        record.write_text(record.read_text(encoding="utf-8") + "\nStudy-specific decision\n", encoding="utf-8")
        before = record.read_bytes()
        result = self.command("add", self.target, "--profile", "writing")
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(record.read_bytes(), before)
        self.assertEqual(len(list((self.target / ".agenthub/runtime/latex-paper-en/scripts").glob("*.py"))), 10)
        result = self.command("check", self.target)
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)

    def test_claude_adapter_matches_canonical_skills(self):
        result = self.command("init", self.target, "--agent", "claude", "--profile", "research")
        self.assertEqual(result.returncode, 0, result.stderr)
        for source in (self.target / ".agents/skills").rglob("SKILL.md"):
            counterpart = self.target / ".claude/skills" / source.relative_to(self.target / ".agents/skills")
            self.assertEqual(source.read_bytes(), counterpart.read_bytes())
        state = json.loads((self.target / ".agenthub/project.json").read_text(encoding="utf-8"))
        self.assertEqual(state["agent"], "claude")
        self.assertNotIn(str(ROOT), json.dumps(state))

    def test_repository_self_target_is_rejected(self):
        result = self.command("init", ROOT, "--dry-run")
        self.assertNotEqual(result.returncode, 0)

    def test_file_contract_interfaces_do_not_create_vendor_global_configuration(self):
        for agent in ("codex", "dsh", "zcode", "generic"):
            with self.subTest(agent=agent):
                target = self.target.parent / agent
                result = self.command("init", target, "--agent", agent, "--profile", "research")
                self.assertEqual(result.returncode, 0, result.stderr)
                self.assertTrue((target / "AGENTS.md").is_file())
                self.assertTrue((target / "AI_START.md").is_file())
                self.assertFalse((target / ".zcode").exists())
                self.assertFalse((target / ".dsh").exists())
                self.assertFalse((target / ".claude").exists())

    def test_add_without_agent_preserves_existing_native_adapter(self):
        result = self.command("init", self.target, "--agent", "claude", "--profile", "research")
        self.assertEqual(result.returncode, 0, result.stderr)
        result = self.command("add", self.target, "--profile", "writing")
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertTrue((self.target / ".claude/skills/paper-audit/SKILL.md").is_file())
        state = json.loads((self.target / ".agenthub/project.json").read_text(encoding="utf-8"))
        self.assertEqual(state["agent"], "claude")

if __name__ == "__main__":
    unittest.main()
