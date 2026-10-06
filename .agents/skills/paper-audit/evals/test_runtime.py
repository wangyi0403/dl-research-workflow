"""Regression tests for audit evidence boundaries and real checker integration."""
from __future__ import annotations

import contextlib
import importlib.util
import io
import json
import os
import sys
import subprocess
import tempfile
import unittest
from pathlib import Path

SCRIPTS = Path(__file__).resolve().parents[1] / "scripts"
sys.path.insert(0, str(SCRIPTS))
import audit
from check_bibliography import check_bibliography
from check_protocol import output_status, parse_script_output
from prepare_review_workspace import prepare_workspace
from report_generator import AuditResult, ChecklistItem, audit_exit_code, render_json_report


class AuditRuntimeTests(unittest.TestCase):
    def setUp(self):
        self.temporary = tempfile.TemporaryDirectory(prefix="agenthub-audit-", dir=os.environ.get("AGENTHUB_TEST_ROOT"))
        self.root = Path(self.temporary.name)

    def tearDown(self):
        self.temporary.cleanup()

    def document(self, name="main.tex"):
        source = self.root / name
        source.write_text(r"""\documentclass{article}
\title{Audit fixture}
\begin{document}
\begin{abstract}A local test of evidence handling.\end{abstract}
\section{Introduction}Software identity is documented \cite{a,b}.
\section{Methods}We preserve independent experimental units.
\section{Results}The recorded outcome is limited to the fixture.
\section{Limitations and disclosure}No population inference is made.
\section{Conclusion}The result is a bounded software test.
\bibliography{one,two}
\end{document}
""", encoding="utf-8")
        for key, filename in [("a", "one"), ("b", "two")]:
            (self.root / (filename + ".bib")).write_text(
                "@article{" + key + ", author={Example, A}, title={Fixture}, journal={Test}, year={2020}}",
                encoding="utf-8",
            )
        return source

    def test_clean_messages_are_not_findings(self):
        for text in ["PASS\nTotal entries: 1", "% GRAMMAR: No rule-based issues detected in selected scope.",
                     "[OK] Line 4: figure.pdf\nAll figures passed check.", "No citation stacking issues found."]:
            self.assertEqual(parse_script_output("test", text), [])

    def test_cli_json_stdout_is_machine_readable(self):
        source = self.document()
        completed = subprocess.run(
            [sys.executable, "-B", str(SCRIPTS / "audit.py"), str(source), "--format", "json"],
            capture_output=True, text=True, encoding="utf-8", cwd=self.root,
        )
        self.assertEqual(completed.returncode, 0, completed.stderr)
        payload = json.loads(completed.stdout)
        self.assertEqual(payload["mode"], "quick-audit")
        self.assertIn("[audit]", completed.stderr)

    def test_cli_json_file_does_not_emit_non_json_stdout(self):
        source = self.document()
        report = self.root / "audit.json"
        completed = subprocess.run(
            [sys.executable, "-B", str(SCRIPTS / "audit.py"), str(source), "--format", "json", "--output", str(report)],
            capture_output=True, text=True, encoding="utf-8", cwd=self.root,
        )
        self.assertEqual(completed.returncode, 0, completed.stderr)
        self.assertEqual(completed.stdout, "")
        self.assertEqual(json.loads(report.read_text(encoding="utf-8"))["mode"], "quick-audit")

    def test_structured_details_stay_in_one_finding(self):
        result = parse_script_output("logic", "% LOGIC (Line 12) [Severity: Major] [Priority: P1]: Unsupported statement\n% Original: x = 0.1\n% Suggested: Check source\n% Rationale: Evidence mismatch")
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0].line, 12)
        self.assertEqual(result[0].original, "x = 0.1")
        self.assertEqual(result[0].rationale, "Evidence mismatch")

    def test_failed_process_is_not_clean(self):
        script = self.root / "crash.py"
        script.write_text("import sys\nprint('failure',file=sys.stderr)\nsys.exit(3)\n", encoding="utf-8")
        code, stdout, stderr = audit._run_check_script(script, "unused")
        self.assertEqual(output_status(stdout, code, stderr, []), "error")
        result = AuditResult("fixture.tex", "en", "gate", check_runs=[{"check": "format", "status": "error"}])
        self.assertEqual(audit_exit_code(result), 2)

    def test_gate_json_and_exit_agree(self):
        result = AuditResult("fixture.tex", "en", "gate", checklist=[ChecklistItem("Reference resolves", False)])
        self.assertEqual(audit_exit_code(result), 1)
        self.assertEqual(json.loads(render_json_report(result))["verdict"], "FAIL")

    def test_reference_json_array_retains_blocker(self):
        source = self.root / "broken.tex"
        source.write_text(r"\section{Results}See \ref{missing}.", encoding="utf-8")
        code, stdout, stderr = audit._run_check_script(SCRIPTS / "check_references.py", str(source), ["--json"])
        findings = parse_script_output("references", stdout)
        self.assertEqual(len(findings), 1)
        self.assertEqual(findings[0].severity, "Critical")
        self.assertEqual(output_status(stdout, code, stderr, findings), "findings")

    def test_bibliography_uses_all_referenced_files(self):
        source = self.document()
        result = check_bibliography(source)
        self.assertEqual(result["total_entries"], 2)
        self.assertEqual(result["status"], "PASS")
        source.write_text(source.read_text().replace(r"\cite{a,b}", r"\cite{a,b,missing}"), encoding="utf-8")
        result = check_bibliography(source)
        self.assertEqual(result["status"], "FAIL")
        self.assertTrue(any("missing" in i["message"] for i in result["issues"]))

    def test_included_citations_and_inline_bibliography(self):
        source = self.root / "inline.tex"
        source.write_text(r"\input{section}\begin{thebibliography}{1}\bibitem{x}Fixture\end{thebibliography}", encoding="utf-8")
        (self.root / "section.tex").write_text(r"A source \cite{x}.", encoding="utf-8")
        self.assertEqual(check_bibliography(source)["status"], "PASS")
        (self.root / "section.tex").write_text(r"A source \cite{missing}.", encoding="utf-8")
        self.assertEqual(check_bibliography(source)["status"], "FAIL")

    def test_workspace_reuse_and_input_changes_preserve_reviews(self):
        source = self.document()
        output = self.root / "review"
        first = prepare_workspace(str(source), str(output))
        review = first / "comments/author-review.json"
        review.write_text('[{"note":"preserve this review"}]', encoding="utf-8")
        self.assertEqual(prepare_workspace(str(source), str(output)), first)
        with (self.root / "one.bib").open("a", encoding="utf-8") as handle:
            handle.write("\n% revised bibliography")
        second = prepare_workspace(str(source), str(output))
        self.assertNotEqual(first, second)
        self.assertTrue(review.exists())
        self.assertFalse((second / "comments/author-review.json").exists())

    def test_plural_sections_and_math_are_not_prose(self):
        parser = audit.get_parser(str(self.document()))
        content = self.document().read_text(encoding="utf-8")
        sections = parser.split_sections(content)
        self.assertIn("method", sections)
        self.assertIn("result", sections)
        self.assertIn("limitations", sections)
        self.assertIn("Before", parser.clean_text(r"Before \[x=1\] after"))
        support = SCRIPTS.parents[3] / ".agenthub/runtime/latex-paper-en/scripts/analyze_sentences.py"
        spec = importlib.util.spec_from_file_location("_test_sentences", support)
        module = importlib.util.module_from_spec(spec); spec.loader.exec_module(module)
        fixture = self.root / "math.tex"
        fixture.write_text(r"""\section{Methods}
$$
x, y, z, a, b, c, d, e, f, g
$$
We record seed, split, hardware, command, output, input, hash, time, state.
""", encoding="utf-8")
        findings = module.analyze(fixture, None, 60, 3)
        self.assertEqual(len(findings), 1)
        self.assertIn("No sentences", findings[0])

    def test_real_screen_does_not_invent_a_committee(self):
        source = self.document()
        previous = Path.cwd()
        try:
            os.chdir(self.root)
            with contextlib.redirect_stdout(io.StringIO()):
                result = audit.run_deep_review(str(source), focus="methodology")
            workspace = Path(result.artifact_dir)
            self.assertEqual(result.review_status, "review_required")
            for name in ("review_report.md", "peer_review_report.md", "revision_roadmap.md", "overall_assessment.txt"):
                self.assertFalse((workspace / name).exists(), name)
            # Old exported views must not override the current structured findings.
            (workspace / "revision_roadmap.md").write_text("## Priority 1\n- [ ] STALE ISSUE (old; old)", encoding="utf-8")
            requested = workspace / "requested-review.md"
            completed = subprocess.run(
                [sys.executable, "-B", str(SCRIPTS / "render_deep_review_report.py"), str(workspace),
                 "--style", "peer-review", "--output", str(requested)],
                capture_output=True, text=True, encoding="utf-8",
            )
            self.assertEqual(completed.returncode, 0, completed.stderr)
            self.assertTrue(requested.exists())
            from report_generator import render_report, render_peer_review_report
            self.assertTrue(render_report(result, report_style="peer-review").startswith(render_peer_review_report(result)))
            self.assertIn("Check execution", render_report(result, report_style="peer-review"))
            self.assertNotIn("STALE ISSUE", requested.read_text(encoding="utf-8"))
            self.assertFalse((workspace / "review_report.md").exists())
            self.assertFalse((workspace / "peer_review_report.md").exists())
            self.assertFalse((workspace / "committee/consensus.md").exists())
            self.assertEqual(list((workspace / "comments").glob("*.json")), [])
            self.assertEqual(result.issue_bundle, [])
            prompts = json.loads((workspace / "review_prompts.json").read_text(encoding="utf-8"))
            self.assertTrue(all(x["source_kind"] == "script" for x in prompts))
            payload = json.loads(render_json_report(result))
            self.assertEqual(payload["review_recommendation"], "REVIEW_REQUIRED")
        finally:
            os.chdir(previous)


if __name__ == "__main__":
    unittest.main()
