"""Render a deep-review Markdown report from workspace artifacts."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

from report_generator import (
    AuditResult,
    build_revision_roadmap,
    coerce_deep_review_issue,
    render_deep_review_report,
    render_peer_review_report,
)


def _read_json_if_exists(
    path: Path, default: list[dict] | dict | None = None
) -> list[dict] | dict | None:
    """Load JSON from path when present, otherwise return the provided default."""
    if not path.exists():
        return default
    return json.loads(path.read_text(encoding="utf-8"))


def _read_text_if_exists(path: Path, *, strip: bool = False) -> str:
    """Load text from path when present, otherwise return an empty string."""
    if not path.exists():
        return ""
    text = path.read_text(encoding="utf-8")
    return text.strip() if strip else text



def load_result(review_dir: Path) -> AuditResult:
    """Load workspace artifacts into an AuditResult for rendering."""
    metadata = _read_json_if_exists(review_dir / "metadata.json", {}) or {}
    final_issues = _read_json_if_exists(review_dir / "final_issues.json", []) or []
    section_index = _read_json_if_exists(review_dir / "section_index.json", []) or []

    return AuditResult(
        file_path=metadata.get("source_path", metadata.get("title", "paper")),
        language=metadata.get("language", "en"),
        mode="deep-review",
        review_focus=metadata.get("review_focus", "full"),
        review_status=(_read_json_if_exists(review_dir / "review_status.json", {}) or {}).get("status", "review_required"),
        issue_bundle=[coerce_deep_review_issue(issue) for issue in final_issues],
        summary=_read_text_if_exists(review_dir / "paper_summary.md"),
        overall_assessment=_read_text_if_exists(review_dir / "committee/consensus.md", strip=True),
        section_index=section_index,
        revision_roadmap=build_revision_roadmap(final_issues),
        artifact_dir=str(review_dir),
    )


def main() -> int:
    parser = argparse.ArgumentParser(description="Render deep-review report from workspace")
    parser.add_argument("review_dir", help="Path to the deep-review workspace")
    parser.add_argument(
        "--style",
        choices=("deep-review", "peer-review"),
        default="deep-review",
        help="Report style to render (defaults to deep-review)",
    )
    parser.add_argument(
        "--output",
        "-o",
        help="Optional output path (defaults to <review_dir>/review_report.md or peer_review_report.md)",
    )
    args = parser.parse_args()

    review_dir = Path(args.review_dir).resolve()
    result = load_result(review_dir)
    if args.style == "peer-review":
        report = render_peer_review_report(result)
        default_output = review_dir / "peer_review_report.md"
    else:
        report = render_deep_review_report(result)
        default_output = review_dir / "review_report.md"
    output_path = Path(args.output).resolve() if args.output else default_output
    output_path.write_text(report, encoding="utf-8")
    print(f"Report written to {output_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
