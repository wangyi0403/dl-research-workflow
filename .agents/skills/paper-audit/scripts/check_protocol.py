"""Normalize checker findings while keeping diagnostics separate from evidence."""
from __future__ import annotations

import json
import re

from report_generator import AuditIssue


def parse_script_output(module_name: str, stdout: str) -> list[AuditIssue]:
    if not stdout.strip():
        return []
    try:
        payload = json.loads(stdout)
    except (ValueError, TypeError):
        payload = None
    if isinstance(payload, list):
        payload = {"issues": payload}
    if isinstance(payload, dict) and isinstance(payload.get("issues"), list):
        findings = []
        for record in payload["issues"]:
            if not isinstance(record, dict):
                continue
            level = str(record.get("severity", record.get("level", "warning"))).lower()
            if level in {"info", "information", "pass", "ok"}:
                continue
            severity = {"error": "Critical", "critical": "Critical", "major": "Major"}.get(level, "Minor")
            findings.append(AuditIssue(
                module=module_name.upper(), line=record.get("line"), severity=severity,
                priority=record.get("priority", {"Critical": "P0", "Major": "P1", "Minor": "P2"}[severity]),
                message=str(record.get("message", record.get("description", "Unspecified checker finding"))),
            ))
        if str(payload.get("status", "")).upper() in {"ERROR", "FAIL"} and not findings:
            findings.append(AuditIssue(module_name.upper(), None, "Critical", "P0",
                                       str(payload.get("message", "Checker reported failure without findings"))))
        return findings

    findings = []
    active = None
    structured = re.compile(r"\[Severity:\s*(Critical|Major|Minor)\]\s*\[Priority:\s*(P[012])\]")
    location = re.compile(r"(?:\(Line\s+|\bLine\s+)(\d+)(?:[^)]*\))?\s*:?")
    for raw in stdout.splitlines():
        line = re.sub(r"^\s*(?:%|//|>)\s*", "", raw).strip()
        match = structured.search(line)
        if match:
            found_line = location.search(line)
            text = structured.sub("", line)
            text = location.sub("", text)
            text = re.sub(r"^\[?[A-Z][A-Z_ -]*\]?\s*:?\s*", "", text)
            active = AuditIssue(module_name.upper(), int(found_line.group(1)) if found_line else None,
                                match.group(1), match.group(2), text.strip(" :-") or "Checker finding")
            findings.append(active)
            continue
        detail = re.match(r"(Original|Suggested|Revised|Rationale):\s*(.*)", line, re.I)
        if detail and active is not None:
            attribute = {"original": "original", "suggested": "revised", "revised": "revised", "rationale": "rationale"}[detail.group(1).lower()]
            setattr(active, attribute, detail.group(2))
            continue
        flag = re.match(r"\[(ERROR|FAIL|WARN|WARNING)\]\s*(.*)", line)
        if flag:
            found_line = location.search(flag.group(2))
            severity = "Critical" if flag.group(1) in {"ERROR", "FAIL"} else "Minor"
            active = AuditIssue(module_name.upper(), int(found_line.group(1)) if found_line else None,
                                severity, "P0" if severity == "Critical" else "P2",
                                location.sub("", flag.group(2)).strip())
            findings.append(active)
            continue
        if active is not None and raw.startswith("        - "):
            active.message += "; " + raw.strip().lstrip("- ")
        if not line:
            active = None
    return findings


def output_status(stdout: str, returncode: int, stderr: str, findings: list[AuditIssue]) -> str:
    if returncode not in (0, 1) or "Traceback (most recent call last)" in stderr:
        return "error"
    if returncode != 0 and not findings:
        return "error"
    try:
        payload = json.loads(stdout)
    except ValueError:
        payload = None
    if isinstance(payload, dict):
        status = str(payload.get("status", "")).upper()
        if status == "SKIP" or payload.get("fallback"):
            return "skipped"
        if status == "NOT_APPLICABLE":
            return "not_applicable"
    return "findings" if findings else "pass"
