#!/usr/bin/env python3
"""Re-split RI math prelim QPs from origin compilation (lossless page copy).

Root cause of prior bad splits (process_scans_lossless.process_math_prelim):
cover detection relied on sparse OCR + ink heuristics, so boundaries drifted and
front pages were attached to the previous paper or dropped.

Cover starts below were verified by OCR of YEAR 6 PRELIMINARY EXAMINATION
headers (0-based page indices into origin/math prelim RI 2018-2025.pdf).

Policy: born-digital / text-layer editions always win over scan splits.
If the working-tree file already has substantial selectable text, it is left
untouched unless --force-scan is passed.
"""

from __future__ import annotations

import argparse
import io
import json
from datetime import datetime, timezone
from pathlib import Path

import fitz
import numpy as np
from PIL import Image, ImageOps

REPO = Path(__file__).resolve().parents[1]
ORIGIN = REPO / "raw files" / "H2 math" / "origin" / "math prelim RI 2018-2025.pdf"
QP_DIR = REPO / "raw files" / "H2 math" / "prelim QP"

# Verified cover page starts (0-based) → (year, paper)
COVERS: list[tuple[int, int, int]] = [
    (2, 2018, 1),
    (12, 2018, 2),
    (22, 2019, 1),
    (28, 2019, 2),
    (36, 2020, 1),
    (42, 2020, 2),
    (48, 2021, 1),
    (54, 2021, 2),
    (60, 2022, 1),
    (66, 2022, 2),
    (74, 2023, 1),
    (80, 2023, 2),
    (86, 2024, 1),
    (94, 2024, 2),
    (100, 2025, 1),
    # 2025 P2 cover is missing from the origin scan (jumps to P2 page 2 at p108)
]

DIGITAL_CHAR_FLOOR = 500  # selectable text → treat as digital edition


def is_digital_edition(path: Path) -> bool:
    """True if PDF has a real text layer (born-digital preferred over scan)."""
    if not path.is_file():
        return False
    doc = fitz.open(path)
    try:
        chars = sum(len(p.get_text()) for p in doc)
    finally:
        doc.close()
    return chars >= DIGITAL_CHAR_FLOOR


def ink_ratio(doc: fitz.Document, i: int, dpi: int = 50) -> float:
    pix = doc[i].get_pixmap(dpi=dpi)
    im = Image.open(io.BytesIO(pix.tobytes("png"))).convert("L")
    arr = np.asarray(ImageOps.autocontrast(im))
    return float((arr < 200).mean())


def segment_ranges(doc: fitz.Document) -> list[tuple[int, int, int, int]]:
    """Return list of (year, paper, start, end) inclusive, blanks trimmed."""
    out: list[tuple[int, int, int, int]] = []
    for bi, (start, year, paper) in enumerate(COVERS):
        end = COVERS[bi + 1][0] - 1 if bi + 1 < len(COVERS) else doc.page_count - 1
        # For 2025 P1, stop before P2 body (origin p108 = index 107 is already P2 p2)
        if year == 2025 and paper == 1:
            end = min(end, 106)  # p101–p107; p108 is P2 content without cover
        while end > start and ink_ratio(doc, end) < 0.008:
            end -= 1
        out.append((year, paper, start, end))
    return out


def copy_pages(src: fitz.Document, start: int, end: int, dest: Path) -> int:
    out = fitz.open()
    out.insert_pdf(src, from_page=start, to_page=end)
    dest.parent.mkdir(parents=True, exist_ok=True)
    out.save(dest, deflate=True, garbage=4)
    n = out.page_count
    out.close()
    return n


def first_page_looks_like_cover(path: Path) -> dict:
    """Cheap post-check for text-layer covers."""
    doc = fitz.open(path)
    page = doc[0]
    text = page.get_text("text").upper()
    pix = page.get_pixmap(dpi=60)
    im = Image.open(io.BytesIO(pix.tobytes("png"))).convert("L")
    arr = np.asarray(ImageOps.autocontrast(im))
    ink = float((arr < 200).mean())
    pages = doc.page_count
    doc.close()
    return {
        "has_raffles": "RAFFLES" in text,
        "has_prelim": "PRELIM" in text,
        "has_mathematics": "MATHEMATICS" in text or "9758" in text,
        "ink": round(ink, 4),
        "pages": pages,
        "ok_text_cover": ("RAFFLES" in text) or ("MATHEMATICS" in text) or ("9758" in text),
    }


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--apply", action="store_true", help="Write re-split PDFs (default dry-run)")
    ap.add_argument(
        "--force-scan",
        action="store_true",
        help="Overwrite digital/text-layer editions with scan splits (discouraged)",
    )
    args = ap.parse_args()

    if not ORIGIN.is_file():
        print(f"Missing origin: {ORIGIN}")
        return 1

    doc = fitz.open(ORIGIN)
    segs = segment_ranges(doc)
    report = {
        "started": datetime.now(timezone.utc).isoformat(),
        "origin": str(ORIGIN.relative_to(REPO)),
        "origin_pages": doc.page_count,
        "segments": [],
        "policy": "prefer_digital_over_scan",
        "notes": [
            "Prior splitter: tools/process_scans_lossless.py::process_math_prelim",
            "Failure mode: OCR cover misses → next paper starts mid-body",
            "2025 P2 cover absent from origin scan (p108 is already 9758/02 page 2)",
            "Digital/text-layer working copies are never overwritten unless --force-scan",
        ],
    }

    print(f"Origin: {ORIGIN.name} ({doc.page_count} pages)")
    print("Policy: preserve digital editions over scan splits")
    for year, paper, start, end in segs:
        name = f"{year} RI P{paper} prelim H2 math.pdf"
        dest = QP_DIR / name
        n = end - start + 1
        digital = is_digital_edition(dest)
        skip = digital and not args.force_scan
        if skip:
            action = "skip_keep_digital"
        elif args.apply:
            action = "write_scan"
        else:
            action = "dry_run_would_write_scan"
        entry = {
            "file": name,
            "origin_range": f"p{start+1}-p{end+1}",
            "pages": n,
            "digital_existing": digital,
            "action": action,
        }
        print(f"  {name}: origin p{start+1}-{end+1} ({n}p) -> {action}")
        if action == "write_scan":
            copy_pages(doc, start, end, dest)
            entry["check"] = first_page_looks_like_cover(dest)
            print(f"    wrote {dest.name}; check={entry['check']}")
        elif dest.exists():
            entry["existing"] = first_page_looks_like_cover(dest)
        report["segments"].append(entry)

    report["origin_gaps"] = [
        {
            "item": "2025 RI P2 cover (page 1)",
            "detail": "Origin jumps from 2025 P1 page 7 (p107) to 2025 P2 page 2 (p108)",
        }
    ]

    doc.close()
    report["finished"] = datetime.now(timezone.utc).isoformat()
    out_json = REPO / "tools" / "_scan_work" / "math_ri_prelim_resplit_report.json"
    out_json.parent.mkdir(parents=True, exist_ok=True)
    out_json.write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
    print(f"Report: {out_json.relative_to(REPO)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
