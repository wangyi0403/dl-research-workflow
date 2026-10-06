"""Read-only figure file audit; this does not inspect scientific or visual layout.

check_figure(path, min_dpi=300, target_inches=None) returns (issues, info).
Strict CLI exits 2 for FAIL, 3 for incomplete required checks (UNKNOWN), and
0 otherwise. A zero exit code can include WARN and is not full publication QA.
"""
from __future__ import annotations

import argparse
import glob
import math
import os
import sys
import xml.etree.ElementTree as ET
from typing import Any

JPEG_FORMATS = {"jpg", "jpeg"}
VECTOR_FORMATS = {"pdf", "svg", "eps"}
RASTER_OK_FORMATS = {"png", "tiff", "tif"}
SEVERITY = {"INFO": 0, "WARN": 1, "UNKNOWN": 2, "FAIL": 3}
SIZE_TOLERANCE_IN = 0.1


def _ext(path: str) -> str:
    return os.path.splitext(path)[1].lower().lstrip(".")


def _check_raster(path: str, ext: str, min_dpi: int,
                  target_inches: tuple[float, float] | None) -> tuple[list, dict]:
    issues: list[tuple[str, str]] = []
    info: dict[str, Any] = {"category": "raster", "ext": ext}
    if ext in JPEG_FORMATS:
        issues.append(("WARN", "JPEG is lossy; use lossless/vector output for text and line art. Check venue requirements for photographs."))
    try:
        from PIL import Image
    except ImportError:
        return issues + [("UNKNOWN", "Pixel/DPI checks not run: Pillow is unavailable.")], info
    try:
        with Image.open(path) as img:
            img.load()
            info["size_px"] = img.size
            info["dpi"] = img.info.get("dpi")
    except Exception as exc:
        return issues + [("FAIL", f"Cannot read image: {exc}")], info

    dpi = info["dpi"]
    if dpi is None:
        level = "WARN" if target_inches else "UNKNOWN"
        issues.append((level, "No DPI metadata. Effective DPI can only be verified with a target display size."))
    else:
        try:
            dx, dy = (float(dpi[0]), float(dpi[1])) if isinstance(dpi, (tuple, list)) else (float(dpi), float(dpi))
            if not all(math.isfinite(v) and v > 0 for v in (dx, dy)):
                raise ValueError("DPI must be finite and positive")
            info["size_inches"] = (info["size_px"][0] / dx, info["size_px"][1] / dy)
            if target_inches is None and min(round(dx), round(dy)) < min_dpi:
                issues.append(("FAIL", f"DPI = {dx:.2f} x {dy:.2f}, below {min_dpi}."))
            if target_inches and any(abs(a - b) > SIZE_TOLERANCE_IN for a, b in zip(info["size_inches"], target_inches)):
                issues.append(("WARN", f"Metadata size {info['size_inches']} in differs from display target {target_inches} in; effective DPI is checked at the target size."))
        except (TypeError, ValueError, IndexError) as exc:
            issues.append(("WARN" if target_inches else "UNKNOWN", f"Invalid DPI metadata: {exc}"))
    if target_inches:
        effective = tuple(px / inches for px, inches in zip(info["size_px"], target_inches))
        info["effective_dpi"] = effective
        if min(round(v) for v in effective) < min_dpi:
            issues.append(("FAIL", f"Effective DPI at target size = {effective[0]:.2f} x {effective[1]:.2f}, below {min_dpi}."))
    return issues, info


def _pdf_reader(path: str):
    try:
        from pypdf import PdfReader
    except ImportError:
        from PyPDF2 import PdfReader
    return PdfReader(path)


def _font_issues(reader) -> list[tuple[str, str]]:
    issues: list[tuple[str, str]] = []
    visited: set[int] = set()

    def visit(resource_ref):
        if resource_ref is None:
            return
        resources = resource_ref.get_object()
        identity = id(resources)
        if identity in visited:
            return
        visited.add(identity)
        font_refs = resources.get("/Font")
        if font_refs is not None:
            for reference in font_refs.get_object().values():
                font = reference.get_object()
                subtype = str(font.get("/Subtype", ""))
                base = str(font.get("/BaseFont", "?"))
                if subtype == "/Type3":
                    issues.append(("WARN", f"Type 3 font {base}: confirm venue acceptance; matplotlib pdf.fonttype=42 is a common alternative."))
                    continue
                font_objects = [font]
                if subtype == "/Type0":
                    font_objects = [child.get_object() for child in font.get("/DescendantFonts", [])]
                embedded = bool(font_objects)
                for child in font_objects:
                    descriptor = child.get("/FontDescriptor")
                    embedded = embedded and bool(descriptor) and any(
                        key in descriptor.get_object() for key in ("/FontFile", "/FontFile2", "/FontFile3")
                    )
                if not embedded:
                    issues.append(("WARN", f"Font may not be embedded: {base}. Confirm portability and venue requirements."))
        xobjects = resources.get("/XObject")
        if xobjects is not None:
            for reference in xobjects.get_object().values():
                obj = reference.get_object()
                if obj.get("/Subtype") == "/Form":
                    visit(obj.get("/Resources"))

    for index, page in enumerate(reader.pages, 1):
        try:
            visit(page.get("/Resources"))
        except Exception as exc:
            issues.append(("UNKNOWN", f"Page {index} font inspection incomplete: {exc}"))
    return list(dict.fromkeys(issues))


def _check_pdf(path: str, target_inches=None) -> tuple[list, dict]:
    info: dict[str, Any] = {}
    try:
        reader = _pdf_reader(path)
    except ImportError:
        return [("UNKNOWN", "PDF structure, fonts and dimensions not checked: pypdf/PyPDF2 is unavailable.")], info
    except Exception as exc:
        return [("FAIL", f"Cannot parse PDF: {exc}")], info
    try:
        page_count = len(reader.pages)
        info["page_count"] = page_count
        if not page_count:
            return [("FAIL", "PDF contains no pages.")], info
        issues = _font_issues(reader)
        sizes = []
        for index, page in enumerate(reader.pages, 1):
            # CropBox is the visible page, expressed in default user-space units.
            unit = float(page.get("/UserUnit", 1))
            size = (float(page.cropbox.width) * unit / 72, float(page.cropbox.height) * unit / 72)
            if int(page.get("/Rotate", 0)) % 180:
                size = size[::-1]
            if not all(math.isfinite(v) and v > 0 for v in size):
                issues.append(("FAIL", f"Page {index} has invalid physical dimensions: {size}."))
            elif target_inches and any(abs(a - b) > SIZE_TOLERANCE_IN for a, b in zip(size, target_inches)):
                issues.append(("FAIL", f"Page {index} visible size = {size[0]:.3f} x {size[1]:.3f} in; target export size = {target_inches} in (tolerance {SIZE_TOLERANCE_IN} in). Vector scaling is allowed for manuscript display; separately inspect legibility there."))
            sizes.append(size)
        info["page_sizes_inches"] = sizes
        return issues, info
    except Exception as exc:
        return [("FAIL", f"Cannot inspect PDF pages: {exc}")], info


def _check_pdf_fonts(path: str) -> list[tuple[str, str]]:
    """Compatibility entry point for existing callers."""
    return _check_pdf(path)[0]


def _check_svg(path: str) -> list[tuple[str, str]]:
    try:
        root = ET.parse(path).getroot()
        if root.tag.split("}")[-1] != "svg":
            return [("FAIL", "Document root is not SVG.")]
        if any(element.tag.split("}")[-1] == "image" for element in root.iter()):
            return [("WARN", "SVG contains raster images; verify their resolution at final display size.")]
        return []
    except Exception as exc:
        return [("FAIL", f"Cannot parse SVG: {exc}")]


def check_figure(path: str, min_dpi: int = 300,
                 target_inches: tuple[float, float] | None = None
                 ) -> tuple[list[tuple[str, str]], dict]:
    """Return issues (INFO/WARN/UNKNOWN/FAIL) and metadata without modifying files."""
    issues: list[tuple[str, str]] = []
    info: dict[str, Any] = {"path": path}
    if not math.isfinite(min_dpi) or min_dpi <= 0:
        raise ValueError("min_dpi must be finite and positive")
    if target_inches is not None and (len(target_inches) != 2 or not all(math.isfinite(v) and v > 0 for v in target_inches)):
        raise ValueError("target_inches must contain two finite positive values")
    if not os.path.isfile(path):
        return [("FAIL", f"File does not exist: {path}")], info
    ext = _ext(path)
    info.update(ext=ext, size_bytes=os.path.getsize(path))
    if ext in VECTOR_FORMATS:
        info["category"] = "vector"
        if ext == "pdf":
            sub_issues, sub_info = _check_pdf(path, target_inches)
            issues.extend(sub_issues)
            info.update(sub_info)
        elif ext == "svg":
            issues.extend(_check_svg(path))
            if target_inches is not None:
                issues.append(("UNKNOWN", "SVG physical dimensions are not checked by this script."))
        else:
            issues.append(("UNKNOWN", "EPS structural/font/dimension checks are not supported by this script."))
    elif ext in RASTER_OK_FORMATS or ext in JPEG_FORMATS:
        sub_issues, sub_info = _check_raster(path, ext, min_dpi, target_inches)
        issues.extend(sub_issues)
        info.update(sub_info)
    else:
        issues.append(("UNKNOWN", f"Unsupported extension: .{ext}"))
    return issues, info


def print_report(path: str, issues: list, info: dict) -> str:
    """Print and return the file-check verdict, not a publication approval."""
    print(f"\n--- {path} ---")
    for key in ("category", "ext", "size_px", "dpi", "effective_dpi", "page_sizes_inches"):
        if key in info:
            print(f"  {key}: {info[key]}")
    verdict = max((s for s, _ in issues), key=SEVERITY.__getitem__, default="PASS")
    for severity, msg in sorted(issues, key=lambda item: -SEVERITY[item[0]]):
        print(f"  [{severity}] {msg}")
    print(f"  >>> verdict: {verdict} (file checks only)")
    return verdict


def _cli() -> int:
    parser = argparse.ArgumentParser(description="Read-only figure file checker")
    parser.add_argument("paths", nargs="+", help="Figure paths or globs")
    parser.add_argument("--min-dpi", type=int, default=300)
    parser.add_argument("--width-in", type=float, help="PDF export width / raster display width in inches")
    parser.add_argument("--height-in", type=float, help="PDF export height / raster display height in inches")
    parser.add_argument("--strict", action="store_true", help="Exit 2 for FAIL, 3 for incomplete required checks (UNKNOWN)")
    args = parser.parse_args()
    if (args.width_in is None) != (args.height_in is None):
        parser.error("--width-in and --height-in must be supplied together")
    target = None if args.width_in is None else (args.width_in, args.height_in)
    if args.min_dpi <= 0 or (target and not all(math.isfinite(v) and v > 0 for v in target)):
        parser.error("DPI and dimensions must be finite and positive")
    expanded = []
    for pattern in args.paths:
        expanded.extend(glob.glob(pattern) or [pattern])
    verdicts = []
    for path in expanded:
        issues, info = check_figure(path, min_dpi=args.min_dpi, target_inches=target)
        verdicts.append(print_report(path, issues, info))
    if args.strict:
        if "FAIL" in verdicts:
            return 2
        if "UNKNOWN" in verdicts:
            return 3
    return 0


if __name__ == "__main__":
    sys.exit(_cli())
