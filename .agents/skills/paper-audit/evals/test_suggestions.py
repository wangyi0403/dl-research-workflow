"""Behavioral checks for optional suggestions versus actionable review defects."""
import json
import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))
from consolidate_review_findings import consolidate_findings, sanitize_issue
from diff_review_issues import diff_issues
from report_generator import (
    AuditResult, DeepReviewIssue, audit_exit_code, build_revision_roadmap,
    coerce_deep_review_issue, render_deep_review_report, render_deep_review_summary,
    render_json_report, render_peer_review_report,
)


def finding(**overrides):
    payload = dict(title="Traceable comparison", quote="shared source text",
                   explanation="The denominator is inconsistent.", comment_type="claim_accuracy",
                   severity="major", source_kind="llm", source_section="results",
                   root_cause_key="comparison")
    return {**payload, **overrides}


class SuggestionTests(unittest.TestCase):
    def test_legacy_defaults_and_roundtrip(self):
        self.assertEqual(sanitize_issue(finding())["type"], "issue")
        optional = sanitize_issue(finding(type="suggestion", gate_blocker=True))
        self.assertFalse(optional["gate_blocker"])
        loaded = DeepReviewIssue.from_dict(optional)
        self.assertEqual(loaded.to_dict()["type"], "suggestion")
        self.assertFalse(loaded.gate_blocker)
        direct = coerce_deep_review_issue(finding(type="suggestion", gate_blocker=True))
        self.assertFalse(direct.gate_blocker)

    def test_mixed_duplicates_preserve_actual_issue_in_either_order(self):
        for real_severity in ("major", "minor"):
            real = finding(severity=real_severity, gate_blocker=real_severity == "major")
            optional = finding(type="suggestion", severity="major", gate_blocker=True,
                               explanation="A longer optional alternative without a demonstrated defect.")
            for incoming in ([real, optional], [optional, real]):
                with self.subTest(severity=real_severity, first=incoming[0].get("type")):
                    merged = consolidate_findings(incoming)
                    self.assertEqual(len(merged), 1)
                    self.assertEqual(merged[0]["type"], "issue")
                    self.assertEqual(merged[0]["severity"], real_severity)
                    self.assertEqual(merged[0]["explanation"], real["explanation"])
                    self.assertEqual(merged[0]["gate_blocker"], real["gate_blocker"])

    def test_optional_item_is_visible_but_not_a_blocker_or_required_repair(self):
        optional = coerce_deep_review_issue(finding(type="suggestion", gate_blocker=True))
        result = AuditResult(file_path="paper.tex", language="en", mode="deep-review",
                             issue_bundle=[optional])
        self.assertEqual(audit_exit_code(result), 0)
        result.mode = "gate"
        self.assertEqual(audit_exit_code(result), 0)
        result.mode = "deep-review"
        self.assertEqual(build_revision_roadmap([optional.to_dict()]), [])
        for renderer in (render_deep_review_report, render_peer_review_report, render_deep_review_summary):
            report = renderer(result)
            self.assertIn("## Optional Suggestions", report)
            self.assertIn(optional.title, report.split("## Optional Suggestions", 1)[1])
            self.assertNotIn(optional.title, report.split("## Optional Suggestions", 1)[0])
            self.assertNotIn("## Revision Roadmap", report)
        data = json.loads(render_json_report(result))
        self.assertEqual(data["issue_bundle"][0]["type"], "suggestion")
        self.assertEqual(data["revision_roadmap"], [])
        deep = render_deep_review_report(result)
        self.assertIn("**Major**: 0", deep)

    def test_reaudit_tracks_optional_items_separately(self):
        optional = finding(type="suggestion")
        result = diff_issues([optional], [optional])
        self.assertEqual(result["statuses"], [])
        self.assertEqual(result["new_issues"], [])
        self.assertEqual(result["optional_suggestions"], [optional])


if __name__ == "__main__":
    unittest.main()
