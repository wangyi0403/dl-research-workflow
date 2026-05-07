"""
Parser re-exports for Paper Audit skill.
Provides unified access to DocumentParser, LatexParser, TypstParser,
and the get_parser factory from sibling skills.

Falls back to minimal built-in parsers when sibling skill
``latex-paper-en`` is not installed.
"""

import importlib.util
import re
from pathlib import Path
from typing import Any

_SKILLS_ROOT = Path(__file__).resolve().parent.parent.parent
_PARSER_CACHE: dict[str, Any] = {}


# ---------------------------------------------------------------------------
# Minimal fallback parsers (used when latex-paper-en is absent)
# ---------------------------------------------------------------------------

class _FallbackDocumentParser:
    """Base parser that reads raw text."""

    def parse(self, path: str | Path) -> str:
        return Path(path).read_text(encoding="utf-8", errors="replace")


class _FallbackLatexParser(_FallbackDocumentParser):
    """Lightweight LaTeX parser — strips comments, returns body text."""

    def parse(self, path: str | Path) -> str:
        raw = Path(path).read_text(encoding="utf-8", errors="replace")
        lines = [l for l in raw.splitlines() if not l.lstrip().startswith("%")]
        return "\n".join(lines)


class _FallbackTypstParser(_FallbackDocumentParser):
    """Lightweight Typst parser — reads raw text."""
    pass


def _fallback_extract_title(text: str) -> str:
    m = re.search(r"\\title\{([^}]+)\}", text)
    return m.group(1).strip() if m else ""


def _fallback_extract_abstract(text: str) -> str:
    m = re.search(
        r"\\begin\{abstract\}(.*?)\\end\{abstract\}", text, re.DOTALL
    )
    return m.group(1).strip() if m else ""


# ---------------------------------------------------------------------------
# Sibling loader (lazy, cached)
# ---------------------------------------------------------------------------

def _load_sibling_parsers() -> Any | None:
    """
    Try to load the full-featured parsers from latex-paper-en.
    Returns the module on success, None on failure.
    """
    if "sibling" in _PARSER_CACHE:
        return _PARSER_CACHE["sibling"]

    candidates = [_SKILLS_ROOT / "latex-paper-en" / "scripts" / "parsers.py"]
    for path in candidates:
        try:
            spec = importlib.util.spec_from_file_location(
                "_sibling_parsers", path
            )
            if spec is None or spec.loader is None:
                continue
            mod = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(mod)  # type: ignore[union-attr]
            for attr in ("LatexParser", "TypstParser", "DocumentParser"):
                assert hasattr(mod, attr), f"{attr} missing in {path}"
            _PARSER_CACHE["sibling"] = mod
            return mod
        except Exception:
            continue

    _PARSER_CACHE["sibling"] = None
    return None


_sibling = _load_sibling_parsers()

if _sibling is not None:
    DocumentParser = _sibling.DocumentParser
    LatexParser = _sibling.LatexParser
    TypstParser = _sibling.TypstParser
    extract_title = _sibling.extract_title
    extract_abstract = _sibling.extract_abstract
    extract_latex_citation_keys = getattr(
        _sibling, "extract_latex_citation_keys", None
    )
else:
    DocumentParser = _FallbackDocumentParser
    LatexParser = _FallbackLatexParser
    TypstParser = _FallbackTypstParser
    extract_title = _fallback_extract_title
    extract_abstract = _fallback_extract_abstract
    extract_latex_citation_keys = None


def get_parser(
    file_path: Any,
    pdf_mode: str = "basic",
    heading_pt: float = 14.0,
    body_pt: float = 12.0,
) -> "DocumentParser":
    """
    Factory supporting PDF in addition to LaTeX/Typst.
    """
    path_str = str(file_path).lower()

    if path_str.endswith(".typ"):
        return TypstParser()
    elif path_str.endswith(".tex"):
        return LatexParser()
    elif path_str.endswith(".pdf"):
        from pdf_parser import PdfParser

        return PdfParser(mode=pdf_mode, heading_pt=heading_pt, body_pt=body_pt)
    else:
        raise ValueError(
            f"Unsupported format: {Path(file_path).suffix}. "
            "Supported: .tex, .typ, .pdf"
        )


__all__ = [
    "DocumentParser",
    "LatexParser",
    "TypstParser",
    "get_parser",
    "extract_title",
    "extract_abstract",
    "extract_latex_citation_keys",
]
