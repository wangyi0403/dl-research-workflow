"""Audit the bibliography actually referenced by a manuscript, without empty passes."""
from __future__ import annotations

import argparse
import importlib.util
import json
import re
from pathlib import Path

from parsers import extract_latex_citation_keys


def read_sources(source: Path) -> tuple[dict[Path, str], list[dict]]:
    """Follow explicit local TeX includes; report unresolved inputs instead of guessing."""
    documents: dict[Path, str] = {}
    issues: list[dict] = []

    def visit(path: Path) -> None:
        path = path.resolve()
        if path in documents:
            return
        if not path.is_file():
            issues.append({"severity": "error", "message": f"Included TeX file not found: {path}"})
            return
        text = re.sub(r"(?<!\\)%[^\n]*", "", path.read_text(encoding="utf-8"))
        documents[path] = text
        for target in re.findall(r"\\(?:input|include)\s*\{([^}]+)\}", text):
            included = path.parent / target
            if not included.suffix:
                included = included.with_suffix(".tex")
            visit(included)

    visit(source)
    return documents, issues


def bibliography_paths(documents: dict[Path, str]) -> list[Path]:
    found: list[Path] = []
    for source, content in documents.items():
        for command, value in re.findall(
            r"\\(bibliography|addbibresource)(?:\[[^\]]*\])?\s*\{([^}]+)\}", content
        ):
            for target in (value.split(",") if command == "bibliography" else [value]):
                path = source.parent / target.strip()
                if not path.suffix:
                    path = path.with_suffix(".bib")
                path = path.resolve()
                if path not in found:
                    found.append(path)
    return found


def load_verifier():
    skills_root = Path(__file__).resolve().parents[2]
    project_root = skills_root.parent.parent
    candidates = [
        project_root / ".agenthub/runtime/latex-paper-en/scripts/verify_bib.py",
        skills_root / "latex-paper-en/scripts/verify_bib.py",
    ]
    for path in candidates:
        if path.is_file():
            spec = importlib.util.spec_from_file_location("_audit_bib_verifier", path)
            if spec is not None and spec.loader is not None:
                module = importlib.util.module_from_spec(spec)
                spec.loader.exec_module(module)
                return module.BibTeXVerifier
    raise ImportError("The project-local latex-paper-en bibliography verifier is missing")


def check_bibliography(source: Path, *, online: bool = False, email: str = "") -> dict:
    source = source.resolve()
    if source.suffix.lower() not in {".tex", ".bib"}:
        return {"status": "SKIP", "issues": [], "detail": "Source-level bibliography check requires TeX or BibTeX"}
    if source.suffix.lower() == ".bib":
        documents, issues, paths = {}, [], [source]
    else:
        documents, issues = read_sources(source)
        paths = bibliography_paths(documents)
    content = "\n".join(documents.values())
    cited = set(extract_latex_citation_keys(content))
    inline_keys = set(re.findall(r"\\bibitem(?:\[[^\]]*\])?\s*\{([^}]+)\}", content))
    keys = set(inline_keys)
    count = len(inline_keys)
    verifier_class = load_verifier() if paths else None
    for path in paths:
        if not path.is_file():
            issues.append({"severity": "error", "message": f"Bibliography file not found: {path}"})
            continue
        verifier = verifier_class(str(path), online=online, email=email or None, style="default")
        result = verifier.verify()
        for issue in result["issues"]:
            issues.append({**issue, "message": f"{path.name}: {issue['message']}"})
        file_keys = {entry["key"] for entry in verifier.entries}
        duplicates = keys & file_keys
        if duplicates:
            issues.append({"severity": "error", "message": "Duplicate bibliography keys across sources: " + ", ".join(sorted(duplicates))})
        keys.update(file_keys)
        count += len(verifier.entries)
        if not verifier.entries:
            issues.append({"severity": "error", "message": f"Referenced bibliography has no entries: {path.name}"})
    missing = cited - keys
    if missing:
        issues.append({"severity": "error", "message": "Citations not found in bibliography: " + ", ".join(sorted(missing))})
    if issues:
        status = "FAIL" if any(i["severity"] == "error" for i in issues) else "WARNING"
    else:
        status = "PASS" if paths or inline_keys else "NOT_APPLICABLE"
    return {"status": status, "total_entries": count, "cited_keys": sorted(cited),
            "bibliographies": [str(p) for p in paths], "issues": issues,
            "detail": "Local identity/consistency check; scientific support still requires source verification"}


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("file", type=Path)
    parser.add_argument("--online", action="store_true")
    parser.add_argument("--email", default="")
    args = parser.parse_args()
    result = check_bibliography(args.file, online=args.online, email=args.email)
    print(json.dumps(result, indent=2, ensure_ascii=False))
    return 1 if result["status"] == "FAIL" else 0


if __name__ == "__main__":
    raise SystemExit(main())
