#!/usr/bin/env python3
"""Lossless scan filing: copy original PDF pages (400 DPI images untouched).

- Math A-level: split on cover pages (footer/year-paper via light OCR on thumbnails only)
- Physics revision: rotate pages upright via /Rotate (no re-encode); do NOT split 2-up A5
- Revision packages: chapter + data-booklet indexing via light OCR
- Hard abort if cumulative OCR wall time exceeds OCR_BUDGET_SEC
"""

from __future__ import annotations

import argparse
import io
import json
import re
import sys
import time
from collections import defaultdict
from dataclasses import dataclass, asdict, field
from datetime import datetime, timezone
from pathlib import Path

import fitz
import numpy as np
import pytesseract
from PIL import Image, ImageOps

REPO = Path(__file__).resolve().parents[1]
RAW = REPO / "raw files"
WORK = REPO / "tools" / "_scan_work"
TESS = Path(r"C:\Program Files\Tesseract-OCR\tesseract.exe")
if TESS.is_file():
    pytesseract.pytesseract.tesseract_cmd = str(TESS)

OCR_BUDGET_SEC = 9 * 60  # leave margin under 10 minutes
_ocr_t0 = time.perf_counter()
_ocr_seconds = 0.0


class OcrBudgetExceeded(RuntimeError):
    pass


def ocr_spent() -> float:
    return _ocr_seconds


def check_budget():
    if _ocr_seconds > OCR_BUDGET_SEC:
        raise OcrBudgetExceeded(f"OCR budget exceeded: {_ocr_seconds:.1f}s > {OCR_BUDGET_SEC}s")


def ocr_text(im: Image.Image, config: str = "--psm 6") -> str:
    global _ocr_seconds
    check_budget()
    t0 = time.perf_counter()
    try:
        return pytesseract.image_to_string(im, config=config)
    finally:
        _ocr_seconds += time.perf_counter() - t0
        check_budget()


PHYS_CH = {
    1: "Quantities and Measurement",
    2: "Forces and Moments",
    3: "Motion and Forces",
    4: "Energy and Fields",
    5: "Projectile Motion",
    6: "Collisions",
    7: "Circular Motion",
    8: "Gravitational Fields",
    9: "Oscillations",
    10: "Wave Motion",
    11: "Superposition",
    12: "Temperature and Ideal Gases",
    13: "Thermodynamic Systems",
    14: "Electric Fields",
    15: "Currents",
    16: "Circuits",
    17: "Electromagnetic Forces",
    18: "Electromagnetic Induction",
    19: "Quantum Physics",
    20: "Nuclear Physics",
}

MATH_CH = {
    1: "Equations and Inequalities",
    2: "Differentiation Techniques",
    3: "Integration Techniques",
    4: "Sequences and Series AP and GP",
    5: "Complex Numbers",
    6: "Vectors 1",
    7: "Vectors 2 and 3 Lines and Planes",
    8: "Applications of Differentiation",
    9: "Graphing Techniques and Transformations",
    10: "Functions",
    11: "Applications of Integration",
    12: "Differential Equations",
    13: "Permutations Combinations Probability",
    14: "Discrete Random Variable Binomial Normal",
    15: "Sampling Estimation Hypothesis Testing",
    16: "Graphing Calculators Review",
}


@dataclass
class Flag:
    source: str
    page: int
    issue: str
    detail: str = ""


@dataclass
class Report:
    started: str = ""
    finished: str = ""
    ocr_seconds: float = 0.0
    outputs: list = field(default_factory=list)
    flags: list = field(default_factory=list)
    sources: dict = field(default_factory=dict)


def page_pil(doc: fitz.Document, i: int) -> Image.Image:
    imgs = doc[i].get_images(full=True)
    if not imgs:
        # fallback render only for OCR classification (never written out)
        pix = doc[i].get_pixmap(matrix=fitz.Matrix(0.35, 0.35), alpha=False)
        return Image.open(io.BytesIO(pix.tobytes("png"))).convert("RGB")
    raw = doc.extract_image(imgs[0][0])["image"]
    return Image.open(io.BytesIO(raw)).convert("RGB")


def thumb(im: Image.Image, width: int = 480) -> Image.Image:
    h = max(1, int(im.height * width / im.width))
    return im.resize((width, h), Image.Resampling.BILINEAR)


def band(im: Image.Image, y0: float, y1: float, width: int = 1000) -> Image.Image:
    w, h = im.size
    crop = im.crop((0, int(h * y0), w, int(h * y1)))
    if crop.width > width:
        nh = max(1, int(crop.height * width / crop.width))
        crop = crop.resize((width, nh), Image.Resampling.BILINEAR)
    return ImageOps.autocontrast(crop, cutoff=1)


def best_ocr(im: Image.Image, rots=(0, 180), config: str = "--psm 6") -> tuple[str, int]:
    best_t, best_s, best_rot = "", -1, 0
    for rot in rots:
        x = im.rotate(rot, expand=True, fillcolor=(255, 255, 255)) if rot else im
        t = ocr_text(x, config=config)
        sc = sum(c.isalnum() for c in t)
        if sc > best_s:
            best_t, best_s, best_rot = t, sc, rot
        # early exit if first orientation already looks good
        if rot == rots[0] and sc >= 25:
            break
    return best_t, best_rot


def copy_pages(src: fitz.Document, indices: list[int], dest: Path, rotation: int | None = None):
    """Lossless page copy; optional /Rotate metadata only."""
    dest.parent.mkdir(parents=True, exist_ok=True)
    out = fitz.open()
    for i in indices:
        out.insert_pdf(src, from_page=i, to_page=i)
        if rotation is not None:
            out[-1].set_rotation(rotation)
    out.save(dest, deflate=True, garbage=3)
    out.close()


def write_flags(flags: list[Flag]):
    WORK.mkdir(parents=True, exist_ok=True)
    lines = [
        "# Lossless scan filing flags",
        "",
        f"Generated: {datetime.now(timezone.utc).isoformat()}",
        f"OCR seconds: {_ocr_seconds:.1f} / budget {OCR_BUDGET_SEC}",
        "",
        "| Source | Page | Issue | Detail |",
        "|---|---:|---|---|",
    ]
    for f in flags:
        lines.append(f"| `{f.source}` | {f.page} | {f.issue} | {f.detail.replace('|', '/')} |")
    if not flags:
        lines.append("| — | — | none | — |")
    (WORK / "FLAGS_LOSSLESS.md").write_text("\n".join(lines) + "\n", encoding="utf-8")


# ---------- Math A-level ----------

def parse_cover_text(t: str) -> dict:
    tl = t.lower()
    out = {"is_cover": False, "year": None, "paper": None}
    if (
        "ministry of education" in tl
        or ("cambridge" in tl and "mathematics" in tl)
        or ("general certificate" in tl and "9758" in tl)
        or ("candidate" in tl and "9758" in tl and "paper" in tl)
    ):
        out["is_cover"] = True
    m = re.search(r"9758/0([12])", tl)
    if m:
        out["paper"] = int(m.group(1))
        out["is_cover"] = True
    m = re.search(r"october/november\s*(20\d{2})", tl)
    if m:
        out["year"] = int(m.group(1))
    if out["year"] is None:
        m = re.search(r"(20\d{2})", tl)
        # only trust year on cover-like pages
        if m and out["is_cover"]:
            y = int(m.group(1))
            if 2010 <= y <= 2030:
                out["year"] = y
    m = re.search(r"paper\s*([12])", tl)
    if m and out["paper"] is None:
        out["paper"] = int(m.group(1))
    return out


def parse_footer_text(t: str) -> dict:
    """Parse bottom 'YYYY Paper N' + page number; tolerate OCR noise."""
    raw = t.lower()
    s = re.sub(r"\s+", "", raw)
    for a, b in [
        ("zo2", "202"),
        ("ao2", "202"),
        ("oza", "202"),
        ("ozs", "202"),
        ("zos", "202"),
        ("ro2", "202"),
        ("r02", "202"),
        ("papert", "paper1"),
        ("paperi", "paper1"),
        ("poper", "paper"),
        ("roper", "paper"),
        ("soper", "paper"),
        ("raper", "paper"),
        ("peper", "paper"),
        ("p0per", "paper"),
    ]:
        s = s.replace(a, b)
    out = {"year": None, "paper": None, "pageno": None}
    m = re.search(r"(20\d{2})paper([12])", s)
    if m:
        out["year"], out["paper"] = int(m.group(1)), int(m.group(2))
    else:
        m = re.search(r"paper([12])", s)
        if m:
            out["paper"] = int(m.group(1))
        m = re.search(r"(20\d{2})", s)
        if m:
            y = int(m.group(1))
            if 2010 <= y <= 2030:
                out["year"] = y
    # page number: prefer trailing number after paper token
    m = re.search(r"paper[12][^\d]*(\d{1,2})(?:\D|$)", s)
    if m:
        out["pageno"] = int(m.group(1))
    else:
        nums = [int(x) for x in re.findall(r"\d{1,2}", s)]
        if nums:
            out["pageno"] = nums[-1]
    return out


def likely_cover_ink(im: Image.Image) -> bool:
    a = np.asarray(ImageOps.grayscale(im))
    h = a.shape[0]
    bot = (a[int(h * 0.85) :] < 200).mean()
    top = (a[: int(h * 0.35)] < 200).mean()
    mid = (a[int(h * 0.35) : int(h * 0.7)] < 200).mean()
    # covers: almost blank footer strip, some header/body ink
    return bot < 0.008 and top > 0.02 and mid > 0.015


def split_math_alvl(pdf: Path, report: Report, flags: list[Flag]):
    print(f"\n== MATH TYS {pdf.name} (lossless)", flush=True)
    doc = fitz.open(pdf)
    n = doc.page_count
    # Pass 1: cheap ink prefilter + sparse OCR for covers; always OCR footer lightly
    covers: list[tuple[int, int | None, int | None]] = []  # index, year, paper
    footers: list[dict] = []
    for i in range(n):
        im = page_pil(doc, i)
        # footer OCR (single band, 2 rots) — user asked for bottom text / page number
        ft, _ = best_ocr(band(im, 0.90, 1.0, width=900), rots=(0, 180), config="--psm 7")
        meta_f = parse_footer_text(ft)
        footers.append(meta_f)

        do_cover_ocr = i == 0 or likely_cover_ink(im) or (meta_f.get("pageno") == 1)
        if do_cover_ocr:
            # thumbnail whole page first (fast reject)
            th = thumb(im, 450)
            tquick, _ = best_ocr(th, rots=(0, 180))
            meta = parse_cover_text(tquick)
            if not meta["is_cover"]:
                # try header band more carefully
                th2, _ = best_ocr(band(im, 0.0, 0.40, width=1100), rots=(0, 180))
                meta = parse_cover_text(th2)
            if meta["is_cover"]:
                year = meta["year"] or meta_f.get("year")
                paper = meta["paper"] or meta_f.get("paper")
                covers.append((i, year, paper))
                print(f"  cover @ p{i+1}: year={year} paper={paper}", flush=True)
        if (i + 1) % 25 == 0:
            print(f"  ... {i+1}/{n} ocr={_ocr_seconds:.0f}s", flush=True)

    # Build segments from covers; fill year/paper from footers when missing
    if not covers:
        flags.append(Flag(pdf.name, 0, "no_covers_found", "entire PDF unassigned"))
        dest = WORK / "math_unassigned" / f"{pdf.stem}_all.pdf"
        copy_pages(doc, list(range(n)), dest)
        report.outputs.append(str(dest.relative_to(REPO)))
        doc.close()
        return

    # Ensure sorted unique starts
    starts = sorted({c[0] for c in covers})
    cover_meta = {i: (y, p) for i, y, p in covers}

    segs = []
    for si, start in enumerate(starts):
        end = starts[si + 1] - 1 if si + 1 < len(starts) else n - 1
        year, paper = cover_meta[start]
        # enrich from footers in segment
        for j in range(start, end + 1):
            if year is None and footers[j].get("year"):
                year = footers[j]["year"]
            if paper is None and footers[j].get("paper"):
                paper = footers[j]["paper"]
        segs.append((start, end, year, paper))

    out_dir = RAW / "H2 math" / "TYS QP"
    out_dir.mkdir(parents=True, exist_ok=True)
    wrote = 0
    for start, end, year, paper in segs:
        idxs = list(range(start, end + 1))
        if not year or not paper:
            dest = WORK / "math_unassigned" / f"{pdf.stem}_{start+1}-{end+1}.pdf"
            copy_pages(doc, idxs, dest)
            flags.append(Flag(pdf.name, start + 1, "unassigned_exam_segment", f"{dest.name} ({len(idxs)}p)"))
            report.outputs.append(str(dest.relative_to(REPO)))
            print(f"  FLAG unassigned p{start+1}-{end+1} ({len(idxs)}p)", flush=True)
            continue
        name = f"{year} P{paper} A-level H2 math.pdf"
        dest = out_dir / name
        if dest.exists():
            dest = out_dir / name.replace(".pdf", " SCAN.pdf")
            flags.append(Flag(pdf.name, start + 1, "dest_exists_wrote_scan", dest.name))
        copy_pages(doc, idxs, dest)
        report.outputs.append(str(dest.relative_to(REPO)))
        print(f"  wrote {dest.name} ({len(idxs)}p) from src p{start+1}-{end+1}", flush=True)
        if len(idxs) < 5 or len(idxs) > 40:
            flags.append(Flag(pdf.name, start + 1, "unusual_page_count", f"{dest.name}={len(idxs)}p"))
        wrote += 1
    report.sources[pdf.name] = {"segments": wrote, "covers": len(covers)}
    doc.close()


# ---------- Physics / math revision orientation + chapter index ----------

PHYS_KEYS = [
    "raffles",
    "revision",
    "physics",
    "page",
    "temperature",
    "quantum",
    "electric",
    "circuit",
    "nuclear",
    "guardians",
    "homecoming",
    "endgame",
    "formulae",
    "name",
    "class",
]


def score_keys(t: str, keys: list[str]) -> int:
    tl = t.lower()
    return sum(k in tl for k in keys) * 10 + min(40, sum(c.isalnum() for c in t) // 5)


def detect_rotation(doc: fitz.Document, sample_idxs: list[int], keys: list[str] | None = None) -> int:
    """Generic upright rotation vote for portrait-ish pages."""
    keys = keys or (PHYS_KEYS + ["ministry", "mathematics", "topic", "content", "mf27"])
    votes = defaultdict(int)
    for i in sample_idxs:
        im = thumb(page_pil(doc, i), 520)
        best = (-1, 0)
        for rot in (0, 180, 90, 270):
            x = im.rotate(-rot, expand=True, fillcolor=(255, 255, 255)) if rot else im
            w, h = x.size
            top = x.crop((0, 0, w, max(40, h // 3)))
            nw = min(700, top.width)
            nh = max(1, int(top.height * nw / max(1, top.width)))
            top = ImageOps.autocontrast(top.resize((nw, nh), Image.Resampling.BILINEAR), 1)
            t = ocr_text(top)
            sc = score_keys(t, keys)
            if sc > best[0]:
                best = (sc, rot)
        votes[best[1]] += 1
        print(f"    sample p{i+1} -> rot {best[1]} (score {best[0]})", flush=True)
    return max(votes, key=votes.get) if votes else 0


def detect_physics_rotation(doc: fitz.Document, sample_idxs: list[int]) -> int:
    """Prefer 270/90 when Raffles headers appear; ignore cover-only 0/180 votes."""
    content_votes = defaultdict(int)
    cover_votes = defaultdict(int)
    for i in sample_idxs:
        im = thumb(page_pil(doc, i), 560)
        best = (-1, 0, "")
        for rot in (270, 90, 180, 0):
            x = im.rotate(-rot, expand=True, fillcolor=(255, 255, 255)) if rot else im
            w, h = x.size
            if w > h:
                strip = x.crop((0, 0, w // 2, max(40, h // 5)))
            else:
                strip = x.crop((0, 0, w, max(40, h // 4)))
            nw = min(850, strip.width)
            nh = max(1, int(strip.height * nw / max(1, strip.width)))
            strip = ImageOps.autocontrast(strip.resize((nw, nh), Image.Resampling.BILINEAR), 1)
            t = ocr_text(strip)
            sc = score_keys(t, PHYS_KEYS)
            if "raffles" in t.lower():
                sc += 80
            if re.search(r"\b(1[0-9]|20|[1-9])\s*[~\-–—:.]+\s*[a-z]{4,}", t.lower()):
                sc += 50
            if sc > best[0]:
                best = (sc, rot, t.lower())
        text = best[2]
        is_cover = "guardians" in text or ("name" in text and "class" in text)
        if is_cover or best[1] in (0, 180) and "raffles" not in text:
            cover_votes[best[1]] += max(1, best[0])
        else:
            content_votes[best[1]] += max(1, best[0])
        print(f"    sample p{i+1} -> rot {best[1]} (score {best[0]})", flush=True)
    if content_votes:
        return max(content_votes, key=content_votes.get)
    if cover_votes:
        return max(cover_votes, key=cover_votes.get)
    return 270


def detect_phys_meta(text: str) -> dict:
    t = text.lower().replace("–", "-").replace("—", "-")
    out = {"kind": "content", "chapter": None}
    if re.search(r"list of formulae|permeability of free space|\bdata\b.*\bformulae\b|planck constant", t):
        out["kind"] = "data"
        return out
    if "guardians of the" in t or ("revision package" in t and "name" in t and "class" in t):
        out["kind"] = "cover"
        return out
    if sum(1 for n in PHYS_CH if re.search(rf"\b{n}\b", t)) >= 5 and "content" in t:
        out["kind"] = "cover"
        return out
    # Require a separator so we don't match the '2' in 'H2 Physics'
    m = re.search(
        r"\b(1[0-9]|20|[1-9])\s*[~\-–—:.]+\s*"
        r"(temperature|thermodynamic|electric fields|currents|circuits|"
        r"electromagnetic induction|electromagnetic forces|electromagnetic|"
        r"quantum|nuclear|quantities|forces and moments|motion and forces|"
        r"energy and fields|projectile|collisions|circular|gravitational|"
        r"oscillations|wave motion|superposition|forces|motion|energy|wave)",
        t,
    )
    if m:
        out["chapter"] = int(m.group(1))
    return out


def process_physics_rotate_index(pdf: Path, report: Report, flags: list[Flag]):
    print(f"\n== PHYS {pdf.name} (rotate+index, no A5 split)", flush=True)
    doc = fitz.open(pdf)
    n = doc.page_count
    sample = sorted(set([0, 1, n // 5, n // 2, (3 * n) // 5, n - 1]))
    sample = [i for i in sample if 0 <= i < n]
    rot = detect_physics_rotation(doc, sample)
    print(f"  chosen rotation={rot}", flush=True)

    # Index pages with light OCR on rotated thumbs
    pages = []  # (idx, kind, chapter)
    last_ch = None
    # Stride OCR to stay inside budget; inherit chapter between hits
    stride = 2 if n < 80 else 3
    cached_meta = {}
    for i in range(n):
        if i % stride == 0 or i < 3 or i == n - 1:
            im = page_pil(doc, i)
            if rot:
                im = im.rotate(-rot, expand=True, fillcolor=(255, 255, 255))
            w, h = im.size
            if w > h:
                strip = im.crop((0, 0, w // 2, max(50, h // 5)))
            else:
                strip = im.crop((0, 0, w, max(50, h // 5)))
            nw = min(900, strip.width)
            nh = max(1, int(strip.height * nw / max(1, strip.width)))
            strip = ImageOps.autocontrast(strip.resize((nw, nh), Image.Resampling.BILINEAR), 1)
            meta = detect_phys_meta(ocr_text(strip))
            cached_meta[i] = meta
        else:
            meta = {"kind": "content", "chapter": None}

        if meta["kind"] == "content":
            ch = meta["chapter"] or last_ch
            if meta["chapter"]:
                last_ch = meta["chapter"]
            pages.append((i, "content", ch))
        else:
            pages.append((i, meta["kind"], None))
            if meta["kind"] == "cover":
                last_ch = None
        if (i + 1) % 30 == 0:
            print(f"  ... {i+1}/{n} ocr={_ocr_seconds:.0f}s", flush=True)

    out = RAW / "H2 physics" / "base syllabus" / "revision packages"
    out.mkdir(parents=True, exist_ok=True)

    def emit(indices: list[int], dest: Path):
        if not indices:
            return
        copy_pages(doc, indices, dest, rotation=rot if rot else None)
        report.outputs.append(str(dest.relative_to(REPO)))

    data = [i for i, k, _ in pages if k == "data"]
    cover = [i for i, k, _ in pages if k == "cover"]
    content = [(i, ch) for i, k, ch in pages if k == "content"]

    if data:
        dest = out / f"Data and Formulae Booklet - {pdf.stem[:40]}.pdf"
        emit(data, dest)
        print(f"  data booklet {len(data)}p", flush=True)
    else:
        flags.append(Flag(pdf.name, 0, "missing_data_booklet", ""))

    if cover:
        dest = out / f"Cover - {pdf.stem[:40]}.pdf"
        emit(cover, dest)
        print(f"  cover {len(cover)}p", flush=True)

    by = defaultdict(list)
    un = []
    for i, ch in content:
        if ch in PHYS_CH:
            by[ch].append(i)
        else:
            un.append(i)
    for ch, idxs in sorted(by.items()):
        dest = out / f"Chap {ch} {PHYS_CH[ch]} Revision Package.pdf"
        # if exists, write package-specific file to avoid append re-bake
        if dest.exists():
            dest = out / f"Chap {ch} {PHYS_CH[ch]} Revision Package - {pdf.stem[:24]}.pdf"
        emit(idxs, dest)
        print(f"  chap {ch}: {len(idxs)}p", flush=True)
    if un:
        dest = out / f"_unassigned - {pdf.stem[:40]}.pdf"
        emit(un, dest)
        flags.append(Flag(pdf.name, 0, "unassigned_pages", str(len(un))))
        print(f"  FLAG unassigned={len(un)}", flush=True)

    # Also emit a single rotated full copy for fidelity reference? Skip — user wants sorted files.
    report.sources[pdf.name] = {"rotation": rot, "chapters": sorted(by), "unassigned": len(un)}
    doc.close()


def detect_math_ch(text: str) -> dict:
    t = text.lower()
    out = {"kind": "content", "chapter": None}
    if re.search(r"^\s*content\b", t) or ("preface" in t and "syllabus" in t):
        out["kind"] = "cover"
        return out
    if ("list of formulae" in t or re.search(r"\bmf\s*2[67]\b", t)) and "revision" not in t and "topic:" not in t:
        out["kind"] = "data"
        return out
    m = re.search(r"revision\s*(\d{1,2})[ab]?\s*[_\s:-]+", t)
    if m and int(m.group(1)) in MATH_CH:
        out["chapter"] = int(m.group(1))
        return out
    m = re.search(r"topic\s*:\s*([^\n]+)", t)
    if m:
        topic = m.group(1).strip().lower()
        for n, title in MATH_CH.items():
            if title.lower().split()[0] in topic:
                out["chapter"] = n
                return out
    return out


def process_math_revision(pdf: Path, report: Report, flags: list[Flag]):
    print(f"\n== MATH REV {pdf.name} (lossless index)", flush=True)
    doc = fitz.open(pdf)
    n = doc.page_count
    sample = [0, 1, n // 3, n // 2, n - 1]
    rot = detect_rotation(doc, [i for i in sample if 0 <= i < n])
    print(f"  rotation={rot}", flush=True)

    pages = []
    last = None
    stride = 2
    for i in range(n):
        if i % stride != 0 and i not in (0, 1, n - 1):
            pages.append((i, "content", last))
            continue
        im = page_pil(doc, i)
        if rot:
            im = im.rotate(-rot, expand=True, fillcolor=(255, 255, 255))
        t = ocr_text(ImageOps.autocontrast(thumb(im, 500), 1))
        meta = detect_math_ch(t)
        if meta["kind"] == "content" and meta["chapter"] is None:
            w, h = im.size
            top = im.crop((0, 0, w, max(40, h // 4)))
            nw = min(950, top.width)
            nh = max(1, int(top.height * nw / max(1, top.width)))
            top = ImageOps.autocontrast(top.resize((nw, nh), Image.Resampling.BILINEAR), 1)
            meta = detect_math_ch(ocr_text(top))
        if meta["kind"] == "content":
            ch = meta["chapter"] or last
            if meta["chapter"]:
                last = meta["chapter"]
            pages.append((i, "content", ch))
        else:
            pages.append((i, meta["kind"], None))
            if meta["kind"] == "cover":
                last = None
        if (i + 1) % 20 == 0:
            print(f"  ... {i+1}/{n} ocr={_ocr_seconds:.0f}s", flush=True)

    out = RAW / "H2 math" / "revision packages"
    out.mkdir(parents=True, exist_ok=True)

    def emit(indices, dest):
        if indices:
            copy_pages(doc, indices, dest, rotation=rot if rot else None)
            report.outputs.append(str(dest.relative_to(REPO)))

    data = [i for i, k, _ in pages if k == "data"]
    cover = [i for i, k, _ in pages if k == "cover"]
    content = [(i, ch) for i, k, ch in pages if k == "content"]
    if data:
        emit(data, out / "Data Booklet MF27 and Syllabus Checklist.pdf")
        print(f"  data {len(data)}p", flush=True)
    else:
        flags.append(Flag(pdf.name, 0, "missing_data_booklet", ""))
    if cover:
        emit(cover, out / "Cover and Contents.pdf")
        print(f"  cover {len(cover)}p", flush=True)
    by = defaultdict(list)
    un = []
    for i, ch in content:
        if ch in MATH_CH:
            by[ch].append(i)
        else:
            un.append(i)
    for ch, idxs in sorted(by.items()):
        emit(idxs, out / f"Chap {ch} {MATH_CH[ch]} Revision Package.pdf")
        print(f"  chap {ch}: {len(idxs)}p", flush=True)
    if un:
        emit(un, out / "_unassigned math revision pages.pdf")
        flags.append(Flag(pdf.name, 0, "unassigned_pages", str(len(un))))
        print(f"  FLAG unassigned={len(un)}", flush=True)
    report.sources[pdf.name] = {"rotation": rot, "chapters": sorted(by), "unassigned": len(un)}
    doc.close()


def process_math_prelim(pdf: Path, report: Report, flags: list[Flag]):
    """Light cover/footer split for RI prelim compilation — lossless copy."""
    print(f"\n== MATH PRELIM {pdf.name} (lossless)", flush=True)
    doc = fitz.open(pdf)
    n = doc.page_count
    bounds = []  # (start_idx, year, paper)
    last_y = last_p = None
    for i in range(n):
        im = page_pil(doc, i)
        ft, _ = best_ocr(band(im, 0.88, 1.0, width=950), rots=(0, 180), config="--psm 7")
        fmeta = parse_footer_text(ft)
        # RI footer often: 9758/2018 ... Paper 2
        tl = ft.lower()
        m = re.search(r"9758/(20\d{2})", tl)
        if m:
            fmeta["year"] = int(m.group(1))
        if "preliminary" in tl or "prelim" in tl:
            m = re.search(r"paper\s*([12])", tl)
            if m:
                fmeta["paper"] = int(m.group(1))
        is_new = False
        if likely_cover_ink(im) or (fmeta.get("pageno") == 1) or i == 0:
            top, _ = best_ocr(band(im, 0.0, 0.45, width=1000), rots=(0, 180))
            tll = top.lower()
            if "raffles" in tll and "mathematics" in tll:
                is_new = True
                m = re.search(r"(20\d{2})", tll)
                if m:
                    fmeta["year"] = int(m.group(1))
                m = re.search(r"paper\s*([12])", tll)
                if m:
                    fmeta["paper"] = int(m.group(1))
            if "preliminary" in tll and "paper" in tll:
                is_new = True
        y, p = fmeta.get("year"), fmeta.get("paper")
        if is_new and (y, p) != (last_y, last_p) and (y or p):
            bounds.append((i, y, p))
            last_y, last_p = y or last_y, p or last_p
            print(f"  bound @ p{i+1}: year={last_y} paper={last_p}", flush=True)
        else:
            if y:
                last_y = y
            if p:
                last_p = p
        if (i + 1) % 25 == 0:
            print(f"  ... {i+1}/{n} ocr={_ocr_seconds:.0f}s", flush=True)

    if not bounds:
        bounds = [(0, None, None)]
    out_dir = RAW / "H2 math" / "prelim QP"
    out_dir.mkdir(parents=True, exist_ok=True)
    for bi, (start, year, paper) in enumerate(bounds):
        end = bounds[bi + 1][0] - 1 if bi + 1 < len(bounds) else n - 1
        # propagate ids forward
        if year is None or paper is None:
            # use bound tuple; may still be incomplete
            pass
        idxs = list(range(start, end + 1))
        if not year or not paper:
            dest = WORK / "math_unassigned" / f"{pdf.stem}_{start+1}-{end+1}.pdf"
            copy_pages(doc, idxs, dest)
            flags.append(Flag(pdf.name, start + 1, "unassigned_exam_segment", dest.name))
            report.outputs.append(str(dest.relative_to(REPO)))
            continue
        name = f"{year} RI P{paper} A-level H2 math.pdf"
        dest = out_dir / name
        if dest.exists():
            dest = out_dir / name.replace(".pdf", " SCAN.pdf")
            flags.append(Flag(pdf.name, start + 1, "dest_exists_wrote_scan", dest.name))
        copy_pages(doc, idxs, dest)
        report.outputs.append(str(dest.relative_to(REPO)))
        print(f"  wrote {dest.name} ({len(idxs)}p)", flush=True)
    report.sources[pdf.name] = {"bounds": len(bounds)}
    doc.close()


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--only", choices=["math-tys", "math-prelim", "math-rev", "physics", "all"], default="all")
    ap.add_argument("--physics-files", nargs="*", default=None, help="Optional subset of physics PDF filenames")
    args = ap.parse_args()
    WORK.mkdir(parents=True, exist_ok=True)
    report = Report(started=datetime.now(timezone.utc).isoformat())
    flags: list[Flag] = []

    try:
        if args.only in {"math-tys", "all"}:
            for name in ["math A lvl 2016-2020.pdf", "math A lvl 2021-2025.pdf"]:
                p = RAW / "H2 math" / name
                if p.exists():
                    split_math_alvl(p, report, flags)
                else:
                    flags.append(Flag(name, 0, "missing_source", str(p)))

        if args.only in {"math-prelim", "all"}:
            p = RAW / "H2 math" / "math prelim RI 2018-2025.pdf"
            if p.exists():
                process_math_prelim(p, report, flags)
            else:
                flags.append(Flag(p.name, 0, "missing_source", str(p)))

        if args.only in {"physics", "all"}:
            names = args.physics_files or [
                "physics revision package 1 (flipped 180deg).pdf",
                "physics revision package 2 (flipped 180deg).pdf",
                "physics revision package 3 first half.pdf",
                "physics revision package 3 second half.pdf",
            ]
            for name in names:
                p = RAW / "H2 physics" / name
                if p.exists():
                    process_physics_rotate_index(p, report, flags)
                else:
                    flags.append(Flag(name, 0, "missing_source", str(p)))

        if args.only in {"math-rev", "all"}:
            p = RAW / "H2 math" / "math revision booklet T3.pdf"
            if p.exists():
                process_math_revision(p, report, flags)
            else:
                flags.append(Flag(p.name, 0, "missing_source", str(p)))

    except OcrBudgetExceeded as e:
        print(f"\nABORT: {e}", flush=True)
        flags.append(Flag("_pipeline", 0, "ocr_budget_exceeded", str(e)))
        write_flags(flags)
        report.finished = datetime.now(timezone.utc).isoformat()
        report.ocr_seconds = _ocr_seconds
        report.flags = [asdict(f) for f in flags]
        (WORK / "report_lossless.json").write_text(json.dumps(asdict(report), indent=2), encoding="utf-8")
        return 2

    write_flags(flags)
    report.finished = datetime.now(timezone.utc).isoformat()
    report.ocr_seconds = _ocr_seconds
    report.flags = [asdict(f) for f in flags]
    (WORK / "report_lossless.json").write_text(json.dumps(asdict(report), indent=2), encoding="utf-8")
    print(f"\nOutputs={len(report.outputs)} Flags={len(flags)} OCR={_ocr_seconds:.1f}s", flush=True)
    return 0


if __name__ == "__main__":
    if hasattr(sys.stdout, "reconfigure"):
        try:
            sys.stdout.reconfigure(encoding="utf-8", errors="replace")
        except Exception:
            pass
    raise SystemExit(main())
