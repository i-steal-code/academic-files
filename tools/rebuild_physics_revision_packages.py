#!/usr/bin/env python3
"""Rebuild H2 physics revision packages from origin scans (v2).

Uses content headers ``Revision Package (H2 Physics) N – Topic`` as the
primary chapter signal; chapter-cover pages (Physics Department + topic)
as secondary. Main package covers dropped. Data booklet preserved.

Layout:
  raw files/H2 physics/revision packages/
    Chap {N} {Title}/
      Revision Package {1|2}.pdf
      Revision Package 3.pdf
    Data and Formulae Booklet.pdf
"""

from __future__ import annotations

import json
import re
import shutil
import sys
import time
from pathlib import Path

import fitz
from PIL import Image, ImageOps

REPO = Path(__file__).resolve().parents[1]
RAW = REPO / "raw files" / "H2 physics"
ORIGIN = RAW / "origin"
OUT = RAW / "revision packages"
OLD = RAW / "base syllabus" / "revision packages"
WORK = REPO / "tools" / "_scan_work"
CONV = REPO / "converted packages" / "H2 physics"
CACHE = WORK / "physics_rev_ocr_cache.json"

sys.path.insert(0, str(REPO / "tools"))
import process_scans_lossless as lsl  # noqa: E402

lsl.OCR_BUDGET_SEC = 10**9
lsl._ocr_seconds = 0.0

PHYS_CH = dict(lsl.PHYS_CH)

SIGNATURES: list[tuple[int, tuple[str, ...]]] = [
    (20, ("nuclear",)),
    (19, ("quantum",)),
    (18, ("induction",)),
    (17, ("electromagnetic",)),
    (16, ("circuit",)),
    (15, ("current",)),
    (14, ("electric",)),
    (13, ("thermodynamic",)),
    (12, ("temperature",)),
    (11, ("superpos",)),
    (10, ("wave", "motion")),
    (9, ("oscillat",)),
    (8, ("gravit",)),
    (7, ("circular",)),
    (6, ("collision",)),
    (5, ("projectile",)),
    (4, ("energy",)),
    (3, ("motion", "force")),
    (2, ("moment",)),
    (1, ("quantit",)),
]

PKG_SOURCES = {
    1: ["physics revision package 1 (flipped 180deg).pdf"],
    2: ["physics revision package 2 (flipped 180deg).pdf"],
    3: [
        "physics revision package 3 first half.pdf",
        "physics revision package 3 second half.pdf",
    ],
}

ROT_HINT = {1: 270, 2: 270, 3: 90}


def norm(t: str) -> str:
    t = t.lower().replace("–", "-").replace("—", "-").replace("�", "-")
    t = re.sub(r"[^a-z0-9]+", " ", t)
    return re.sub(r"\s+", " ", t).strip()


def match_signature(t: str) -> int | None:
    n = norm(t)
    for ch, stems in SIGNATURES:
        if all(s in n for s in stems):
            if ch == 3 and "circular" in n:
                continue
            if ch == 17 and "induction" in n:
                continue
            return ch
    return None


def parse_h2_chapter(t: str) -> int | None:
    """Parse 'Revision Package (H2 Physics) 12 - Temperature…' style headers."""
    n = norm(t)
    m = re.search(
        r"revision\s*package\s*(?:h\s*2\s*physics)?\s*(\d{1,2})\s*(?:temperature|thermodynamic|electric|current|circuit|electromagnetic|quantum|nuclear|quantit|force|moment|motion|energy|projectile|collision|circular|gravit|oscillat|wave|superpos|[a-z])",
        n,
    )
    if m:
        ch = int(m.group(1))
        if 1 <= ch <= 20:
            return ch
    m = re.search(r"revision\s*package\s*h\s*2\s*physics\s*(\d{1,2})\b", n)
    if m:
        ch = int(m.group(1))
        if 1 <= ch <= 20:
            return ch
    return None


def is_data(t: str) -> bool:
    n = norm(t)
    return any(
        k in n
        for k in (
            "permeability of free space",
            "planck constant",
            "elementary charge",
            "list of formulae",
            "speed of light in free space",
        )
    )


def is_main_cover(t: str) -> bool:
    n = norm(t)
    if any(k in n for k in ("guardians", "homecoming", "endgame")):
        return True
    if "name" in n and "class" in n and "revision package" in n:
        nums = sum(1 for i in range(1, 21) if re.search(rf"\b{i}\b", n))
        if nums >= 8:
            return True
    return False


def is_dept_cover(t: str) -> bool:
    n = norm(t)
    return "revision package" in n and ("depart" in n or "physics department" in n)


def ocr_left_header(im: Image.Image) -> str:
    w, h = im.size
    strip = im.crop((0, 0, max(1, w // 2), max(140, h // 3)))
    nw = min(1400, strip.width)
    nh = max(1, int(strip.height * nw / max(1, strip.width)))
    strip = ImageOps.autocontrast(strip.resize((nw, nh), Image.Resampling.BILINEAR), 1)
    return lsl.ocr_text(strip)


def ocr_full_top(im: Image.Image) -> str:
    w, h = im.size
    strip = im.crop((0, 0, w, max(120, h // 4)))
    nw = min(1600, strip.width)
    nh = max(1, int(strip.height * nw / max(1, strip.width)))
    strip = ImageOps.autocontrast(strip.resize((nw, nh), Image.Resampling.BILINEAR), 1)
    return lsl.ocr_text(strip)


def detect_rot(pdf: Path, hint: int) -> int:
    doc = fitz.open(pdf)
    n = doc.page_count
    sample = sorted({0, 1, min(2, n - 1), n // 4, n // 2, min(n - 1, 3 * n // 4)})
    try:
        rot = lsl.detect_physics_rotation(doc, sample)
    except Exception:
        rot = hint
    doc.close()
    if rot in (0, 180):
        rot = hint
    return rot


def index_pdf(pdf: Path, rot: int, cache: dict) -> list[dict]:
    key = f"{pdf.name}|rot={rot}"
    if key in cache:
        print(f"  cache hit {pdf.name}", flush=True)
        return cache[key]

    doc = fitz.open(pdf)
    pages: list[dict] = []
    n = doc.page_count
    print(f"  indexing {pdf.name} pages={n} rot={rot}", flush=True)
    t0 = time.perf_counter()
    last_ch: int | None = None

    for i in range(n):
        im = lsl.page_pil(doc, i)
        if rot:
            im = im.rotate(-rot, expand=True, fillcolor=(255, 255, 255))
        text = ocr_left_header(im)
        nt = norm(text)
        if len(nt) < 25:
            text = ocr_full_top(im)
            nt = norm(text)

        kind = "content"
        ch: int | None = None

        if is_data(text):
            kind = "data"
            last_ch = None
        elif is_main_cover(text):
            kind = "main_cover"
            last_ch = None
        else:
            ch = parse_h2_chapter(text)
            if ch is None and is_dept_cover(text):
                kind = "chapter_cover"
                ch = match_signature(text)
                if ch is None:
                    wider = ocr_full_top(im)
                    ch = match_signature(wider) or parse_h2_chapter(wider)
                    text = wider
            if ch is None:
                ch = match_signature(text) if is_dept_cover(text) else None
            if ch is not None:
                last_ch = ch
            elif last_ch is not None and kind == "content":
                ch = last_ch

        pages.append(
            {
                "idx": i,
                "kind": kind,
                "chapter": ch,
                "text": " ".join(text.split())[:200],
            }
        )
        if (i + 1) % 20 == 0:
            print(f"    … {i+1}/{n} ({time.perf_counter()-t0:.0f}s)", flush=True)

    doc.close()
    cache[key] = pages
    CACHE.write_text(json.dumps(cache), encoding="utf-8")
    print(f"  done {pdf.name} in {time.perf_counter()-t0:.0f}s", flush=True)
    return pages


def chapter_indices(pages: list[dict]) -> dict[int, list[int]]:
    by: dict[int, list[int]] = {c: [] for c in PHYS_CH}
    for p in pages:
        if p["kind"] in {"main_cover", "data"}:
            continue
        ch = p["chapter"]
        if ch in by:
            by[ch].append(p["idx"])
    return {c: idxs for c, idxs in by.items() if idxs}


def emit_chapter(pdf: Path, indices: list[int], dest: Path, rot: int) -> None:
    doc = fitz.open(pdf)
    lsl.copy_pages(doc, indices, dest, rotation=rot)
    doc.close()


def merge_pdfs(parts: list[Path], dest: Path) -> None:
    out = fitz.open()
    for p in parts:
        doc = fitz.open(p)
        out.insert_pdf(doc)
        doc.close()
    dest.parent.mkdir(parents=True, exist_ok=True)
    out.save(dest, deflate=True, garbage=3)
    out.close()


def robust_rmtree(path: Path) -> None:
    if not path.exists():
        return
    try:
        shutil.rmtree(path)
        print(f"removed {path}", flush=True)
        return
    except PermissionError:
        aside = path.with_name(path.name + ".__trash")
        if aside.exists():
            shutil.rmtree(aside, ignore_errors=True)
        path.rename(aside)
        print(f"renamed locked tree aside -> {aside.name}", flush=True)


def main() -> int:
    WORK.mkdir(parents=True, exist_ok=True)
    cache: dict = {}
    if CACHE.is_file():
        try:
            cache = json.loads(CACHE.read_text(encoding="utf-8"))
        except json.JSONDecodeError:
            cache = {}

    # Fresh output
    if OUT.exists():
        robust_rmtree(OUT)
    OUT.mkdir(parents=True, exist_ok=True)

    assembled: dict[int, dict[int, list[tuple[Path, list[int], int]]]] = {1: {}, 2: {}, 3: {}}
    index_log: dict = {}

    for pkg, names in PKG_SOURCES.items():
        for name in names:
            pdf = ORIGIN / name
            rot = detect_rot(pdf, ROT_HINT[pkg])
            pages = index_pdf(pdf, rot, cache)
            ranges = chapter_indices(pages)
            index_log[name] = {
                "rotation": rot,
                "chapters": {str(c): len(v) for c, v in sorted(ranges.items())},
                "covers": [p for p in pages if p["kind"] != "content"],
            }
            print(f"  chapters: {sorted(ranges)}", flush=True)
            for c, idxs in ranges.items():
                # sanity: RP1 should only be 12-20; RP2 only 1-11
                if pkg == 1 and c < 12:
                    print(f"  WARN dropping ch{c} from RP1 ({len(idxs)}p)", flush=True)
                    continue
                if pkg == 2 and c > 11:
                    print(f"  WARN dropping ch{c} from RP2 ({len(idxs)}p)", flush=True)
                    continue
                assembled[pkg].setdefault(c, []).append((pdf, idxs, rot))

    missing: list[str] = []
    for ch, title in PHYS_CH.items():
        folder = OUT / f"Chap {ch} {title}"
        folder.mkdir(parents=True, exist_ok=True)
        primary = 2 if ch <= 11 else 1
        for pkg in (primary, 3):
            parts = assembled[pkg].get(ch, [])
            dest = folder / f"Revision Package {pkg}.pdf"
            if not parts:
                missing.append(f"Chap {ch} missing RP{pkg}")
                continue
            if len(parts) == 1:
                emit_chapter(parts[0][0], parts[0][1], dest, parts[0][2])
            else:
                temps = []
                for i, (pdf, idxs, rot) in enumerate(parts):
                    tmp = WORK / f"_tmp_rp{pkg}_ch{ch}_{i}.pdf"
                    emit_chapter(pdf, idxs, tmp, rot)
                    temps.append(tmp)
                merge_pdfs(temps, dest)
                for t in temps:
                    t.unlink(missing_ok=True)
            d = fitz.open(dest)
            print(f"wrote {dest.relative_to(REPO)} pages={d.page_count}", flush=True)
            d.close()

    # Data booklet: prefer old tree, then WORK backup, then existing
    data_src = None
    if OLD.exists():
        cands = list(OLD.glob("Data and Formulae Booklet*.pdf"))
        if cands:
            data_src = max(cands, key=lambda p: p.stat().st_size)
    backup = WORK / "Data and Formulae Booklet.pdf"
    if data_src is None and backup.is_file():
        data_src = backup
    if data_src:
        shutil.copy2(data_src, OUT / "Data and Formulae Booklet.pdf")
        print(f"data booklet from {data_src}", flush=True)
    else:
        missing.append("Data and Formulae Booklet not found")

    robust_rmtree(OLD)
    robust_rmtree(CONV / "base syllabus" / "revision packages")
    robust_rmtree(CONV / "revision packages")

    report = {"missing": missing, "index": {k: {"rotation": v["rotation"], "chapters": v["chapters"]} for k, v in index_log.items()}}
    (WORK / "physics_revision_rebuild.json").write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
    # full cover dump
    (WORK / "physics_revision_rebuild_full.json").write_text(json.dumps(index_log, indent=2) + "\n", encoding="utf-8")
    print("MISSING:", missing)
    return 1 if missing else 0


if __name__ == "__main__":
    raise SystemExit(main())
