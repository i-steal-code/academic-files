#!/usr/bin/env python3
"""Normalize scanned H2 math/physics PDF bundles, split, file, and flag issues.

Pipeline:
  1) Render pages → detect upright rotation → deskew/crop/clean
  2) Physics revision: split A5-on-A4 (2-up) sheets
  3) OCR headers/footers → chapter / year-paper boundaries
  4) Separate data/formulae booklets from question pages
  5) Write normalised PDFs into canonical folders
  6) Emit FLAGS.md for pages/regions that need human review
"""

from __future__ import annotations

import argparse
import io
import json
import re
import shutil
import sys
import traceback
from collections import defaultdict
from dataclasses import dataclass, field, asdict
from datetime import datetime, timezone
from pathlib import Path

import fitz
import numpy as np
import pytesseract
from PIL import Image, ImageFilter, ImageOps, ImageStat

try:
    import cv2
except ImportError:  # pragma: no cover
    cv2 = None

REPO = Path(__file__).resolve().parents[1]
RAW = REPO / "raw files"
WORK = REPO / "tools" / "_scan_work"
FLAGS_PATH = WORK / "FLAGS.md"
REPORT_PATH = WORK / "report.json"

TESS = Path(r"C:\Program Files\Tesseract-OCR\tesseract.exe")
if TESS.is_file():
    pytesseract.pytesseract.tesseract_cmd = str(TESS)

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

A4_W, A4_H = 595, 842  # PDF points


@dataclass
class Flag:
    source: str
    page: int
    issue: str
    detail: str = ""


@dataclass
class PageOut:
    image: Image.Image
    source: str
    src_page: int  # 1-based
    half: str  # "" | "L" | "R"
    text: str = ""
    kind: str = "content"  # content | data | cover | blank | unknown
    chapter: int | None = None
    year: int | None = None
    paper: int | None = None
    school: str | None = None


@dataclass
class Report:
    started: str = ""
    finished: str = ""
    sources: dict = field(default_factory=dict)
    outputs: list = field(default_factory=list)
    flags: list = field(default_factory=list)


def ensure_dirs() -> None:
    WORK.mkdir(parents=True, exist_ok=True)
    (WORK / "pages").mkdir(exist_ok=True)


def render_page(doc: fitz.Document, idx: int, dpi: int = 180) -> Image.Image:
    zoom = dpi / 72.0
    pix = doc[idx].get_pixmap(matrix=fitz.Matrix(zoom, zoom), alpha=False)
    return Image.open(io.BytesIO(pix.tobytes("png"))).convert("RGB")


def ink_ratio(img: Image.Image, thresh: int = 200) -> float:
    g = ImageOps.grayscale(img)
    arr = np.asarray(g)
    return float((arr < thresh).mean())


def content_bbox(img: Image.Image, thresh: int = 200, pad: int = 12) -> tuple[int, int, int, int]:
    g = np.asarray(ImageOps.grayscale(img))
    mask = g < thresh
    # ignore outer 2% binder strip noise somewhat by requiring rows/cols with enough ink
    rows = mask.sum(axis=1)
    cols = mask.sum(axis=0)
    row_lim = max(3, int(0.002 * img.width))
    col_lim = max(3, int(0.002 * img.height))
    ys = np.where(rows > row_lim)[0]
    xs = np.where(cols > col_lim)[0]
    if len(xs) == 0 or len(ys) == 0:
        return (0, 0, img.width, img.height)
    x0, x1 = int(xs[0]), int(xs[-1])
    y0, y1 = int(ys[0]), int(ys[-1])
    x0 = max(0, x0 - pad)
    y0 = max(0, y0 - pad)
    x1 = min(img.width, x1 + pad)
    y1 = min(img.height, y1 + pad)
    return (x0, y0, x1, y1)


def clean_image(img: Image.Image) -> Image.Image:
    """Contrast boost, light denoise, trim margins; preserve text strokes."""
    img = ImageOps.autocontrast(img.convert("RGB"), cutoff=1)
    bbox = content_bbox(img)
    cropped = img.crop(bbox)
    g = ImageOps.grayscale(cropped)
    arr = np.asarray(g).astype(np.uint8)
    if cv2 is not None:
        _, bw = cv2.threshold(arr, 200, 255, cv2.THRESH_BINARY_INV)
        kernel = np.ones((2, 2), np.uint8)
        opened = cv2.morphologyEx(bw, cv2.MORPH_OPEN, kernel)
        speck = ((bw > 0) & (opened == 0))
        rgb = np.asarray(cropped).copy()
        rgb[speck] = 255
        cleaned = Image.fromarray(rgb)
    else:
        cleaned = cropped.filter(ImageFilter.MedianFilter(size=3))
    return cleaned


def deskew(img: Image.Image, max_angle: float = 4.0) -> tuple[Image.Image, float]:
    if cv2 is None:
        return img, 0.0
    g = np.asarray(ImageOps.grayscale(img))
    g = cv2.bitwise_not(g)
    thr = cv2.threshold(g, 0, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)[1]
    coords = np.column_stack(np.where(thr > 0))
    if coords.size < 500:
        return img, 0.0
    angle = cv2.minAreaRect(coords)[-1]
    if angle < -45:
        angle = -(90 + angle)
    else:
        angle = -angle
    if abs(angle) < 0.3 or abs(angle) > max_angle:
        return img, 0.0
    # rotate with expand
    rotated = img.rotate(angle, expand=True, fillcolor=(255, 255, 255))
    return rotated, float(angle)


def place_on_a4(img: Image.Image, landscape: bool = False) -> Image.Image:
    """Center content on an A4 canvas at ~150 DPI equivalent pixel size."""
    # 150 dpi A4 ~ 1240 x 1754
    if landscape:
        canvas_w, canvas_h = 1754, 1240
    else:
        canvas_w, canvas_h = 1240, 1754
    canvas = Image.new("RGB", (canvas_w, canvas_h), (255, 255, 255))
    # fit image into canvas with margin
    margin = 40
    max_w, max_h = canvas_w - 2 * margin, canvas_h - 2 * margin
    w, h = img.size
    scale = min(max_w / w, max_h / h, 1.0)
    nw, nh = max(1, int(w * scale)), max(1, int(h * scale))
    resized = img.resize((nw, nh), Image.Resampling.LANCZOS)
    x = (canvas_w - nw) // 2
    y = (canvas_h - nh) // 2
    canvas.paste(resized, (x, y))
    return canvas


def prep_for_ocr(img: Image.Image) -> Image.Image:
    """Autocontrast + mild sharpen — scanned pages are often washed out."""
    g = ImageOps.grayscale(img)
    g = ImageOps.autocontrast(g, cutoff=1)
    return g.convert("RGB")


def ocr_score(img: Image.Image) -> tuple[str, int]:
    im = prep_for_ocr(img)
    w, h = im.size
    small = im.resize((max(1, w // 2), max(1, h // 2)))
    text = pytesseract.image_to_string(small, config="--psm 6")
    score = sum(c.isalnum() for c in text)
    return text, score


def best_rotation_fast(
    img: Image.Image,
    *,
    prefer: list[int] | None = None,
    expect_two_up: bool = False,
) -> tuple[Image.Image, int, str, int]:
    """Try preferred rotations first; stop early on a strong hit."""
    order = list(prefer or [])
    for r in (0, 90, 180, 270):
        if r not in order:
            order.append(r)
    best = (img, 0, "", -1)
    for rot in order:
        im = img.rotate(-rot, expand=True, fillcolor=(255, 255, 255)) if rot else img
        # cheap ink/layout check before OCR
        two = looks_two_up(im) if expect_two_up else False
        if expect_two_up and im.width <= im.height:
            # skip OCR for portrait when we need landscape 2-up — unless nothing else works
            if rot not in order[-2:]:
                continue
        text, score = ocr_score(im)
        total = score + (int(score * 0.4) if two else 0)
        if total > best[3]:
            best = (im, rot, text, total)
        # early exit: solid OCR on expected layout
        if expect_two_up and two and score >= 60:
            break
        if not expect_two_up and score >= 80 and rot == (prefer[0] if prefer else 0):
            break
    return best[0], best[1], best[2], best[3]


def looks_two_up(img: Image.Image) -> bool:
    """Heuristic: landscape page with ink in both left and right halves."""
    w, h = img.size
    if w < h * 1.05:  # not landscape
        return False
    g = np.asarray(ImageOps.grayscale(img))
    mid = w // 2
    left = (g[:, :mid] < 200).mean()
    right = (g[:, mid:] < 200).mean()
    return left > 0.01 and right > 0.01


def split_two_up(img: Image.Image) -> tuple[Image.Image, Image.Image]:
    w, h = img.size
    mid = w // 2
    # small overlap trim at gutter
    gutter = max(4, w // 200)
    left = img.crop((0, 0, mid - gutter // 2, h))
    right = img.crop((mid + gutter // 2, 0, w, h))
    return left, right


def classify_text(text: str) -> dict:
    t = text.lower()
    out: dict = {"kind": "content", "chapter": None, "year": None, "paper": None, "school": None}

    if ink_like_blank(text) and len(re.findall(r"[A-Za-z]", text)) < 20:
        out["kind"] = "blank"
        return out

    if re.search(r"list of formulae|data and formulae|\bdata\b.*\bformulae\b|\bmf\s*2[67]\b", t, re.S):
        out["kind"] = "data"
    if "guardians of the" in t or "revision package" in t and "name" in t and "class" in t:
        out["kind"] = "cover"
    if "content" in t and "preface" in t and "equations" in t:
        out["kind"] = "cover"

    # Physics chapter headers — avoid TOC pages that list many chapters
    phys_hits = []
    for num, title in PHYS_CH.items():
        first = title.lower().split()[0]
        if re.search(rf"\b{num}\b[^\n]{{0,40}}{re.escape(first)}", t) or title.lower() in t:
            phys_hits.append(num)
    if len(phys_hits) >= 3:
        out["kind"] = "cover"
        out["chapter"] = None
    elif len(phys_hits) == 1:
        out["chapter"] = phys_hits[0]
    elif out["chapter"] is None:
        m = re.search(
            r"\b(1[0-9]|20|[1-9])\s*[-–:]?\s*(temperature|thermodynamic|electric fields|currents|circuits|"
            r"electromagnetic|quantum|nuclear|quantities|forces and moments|motion and forces|energy and fields|"
            r"projectile|collisions|circular|gravitational|oscillations|wave motion|superposition)",
            t,
        )
        if m:
            out["chapter"] = int(m.group(1))

    # Math chapter
    for num, title in MATH_CH.items():
        token = title.lower().split()[0]
        if re.search(rf"\b{num}[a-b]?\b[^\n]{{0,30}}{re.escape(token)}", t):
            out["chapter"] = num
            break

    # Year + paper
    m = re.search(r"(20\d{2})\s*paper\s*([12])", t)
    if m:
        out["year"] = int(m.group(1))
        out["paper"] = int(m.group(2))
    m2 = re.search(r"paper\s*([12]).{0,40}(20\d{2})", t, re.S)
    if m2 and out["year"] is None:
        out["paper"] = int(m2.group(1))
        out["year"] = int(m2.group(2))
    m3 = re.search(r"(20\d{2}).{0,60}year\s*6.{0,40}preliminary|preliminary examination.{0,40}(20\d{2})", t, re.S)
    if m3:
        out["year"] = int(next(g for g in m3.groups() if g))
        out["school"] = "RI"
    if "raffles institution" in t and "preliminary" in t:
        out["school"] = "RI"
    if re.search(r"9758/0([12])", t):
        out["paper"] = int(re.search(r"9758/0([12])", t).group(1))
    if re.search(r"october/november\s*(20\d{2})", t):
        out["year"] = int(re.search(r"october/november\s*(20\d{2})", t).group(1))

    return out


def ink_like_blank(text: str) -> bool:
    return sum(c.isalnum() for c in text) < 25


def normalize_sheet(
    img: Image.Image,
    *,
    force_rot: int | None = None,
    expect_two_up: bool,
    flags: list[Flag],
    source: str,
    src_page: int,
    prefer_rots: list[int] | None = None,
) -> list[tuple[Image.Image, str, str, int]]:
    """Return list of (image, half, ocr_text, rotation_used)."""
    if force_rot is not None:
        rotated = img.rotate(-force_rot, expand=True, fillcolor=(255, 255, 255)) if force_rot else img
        text, score = ocr_score(rotated)
        rot = force_rot
    else:
        candidates = prefer_rots or [0, 90, 180, 270]
        rotated, rot, text, score = best_rotation_fast(
            img, prefer=candidates, expect_two_up=expect_two_up
        )

    if score < 15 and ink_ratio(rotated) < 0.004:
        flags.append(Flag(source, src_page, "blank_or_unreadable", f"rot={rot} score={score}"))
        return [(place_on_a4(clean_image(rotated)), "", text, rot)]

    rotated, _angle = deskew(rotated)
    cleaned = clean_image(rotated)

    # Strong path for physics revision 2-up: require landscape + dual ink columns
    if expect_two_up:
        # If current result is portrait, explicitly try 90/270 even if OCR slightly preferred portrait
        if cleaned.height >= cleaned.width:
            for alt in (90, 270):
                cand = img.rotate(-alt, expand=True, fillcolor=(255, 255, 255))
                cand, _ = deskew(cand)
                cand = clean_image(cand)
                if looks_two_up(cand):
                    t2, s2 = ocr_score(cand)
                    # Accept if OCR is not drastically worse
                    if s2 >= max(20, score * 0.4):
                        cleaned, rot, text, score = cand, alt, t2, s2
                        break

        if looks_two_up(cleaned):
            left, right = split_two_up(cleaned)
            results = []
            for half, part in (("L", left), ("R", right)):
                part2, _ = deskew(part)
                part2 = clean_image(part2)
                part2, prot, ptext, pscore = best_rotation_fast(
                    part2, prefer=[0, 180, 90, 270], expect_two_up=False
                )
                if part2.width > part2.height * 1.05:
                    # prefer portrait for bound revision sheets
                    alt = part2.rotate(-90, expand=True, fillcolor=(255, 255, 255))
                    t_alt, s_alt = ocr_score(alt)
                    if s_alt >= pscore * 0.85:
                        part2, ptext, pscore = alt, t_alt, s_alt
                results.append((place_on_a4(part2, landscape=False), half, ptext or text, rot))
            return results
        else:
            flags.append(Flag(source, src_page, "two_up_not_detected", f"rot={rot} score={score} size={cleaned.size}"))

    landscape = cleaned.width > cleaned.height * 1.1
    return [(place_on_a4(cleaned, landscape=landscape), "", text, rot)]


def images_to_pdf(images: list[Image.Image], dest: Path) -> None:
    dest.parent.mkdir(parents=True, exist_ok=True)
    if not images:
        return
    rgb = [im.convert("RGB") for im in images]
    rgb[0].save(dest, save_all=True, append_images=rgb[1:], resolution=150.0)


def detect_force_rotation(sample_imgs: list[Image.Image]) -> int | None:
    votes: dict[int, int] = defaultdict(int)
    for img in sample_imgs:
        _, rot, _, score = best_rotation_fast(img, prefer=[0, 180, 90, 270])
        if score > 30:
            votes[rot] += 1
    if not votes:
        return None
    return max(votes.items(), key=lambda kv: kv[1])[0]


def process_physics_revision(pdf: Path, report: Report, flags: list[Flag], limit: int = 0) -> None:
    print(f"\n== Physics revision: {pdf.name}")
    doc = fitz.open(pdf)
    n = doc.page_count
    if limit > 0:
        n = min(n, limit)
    print(f"  pages={n}/{doc.page_count} (per-page orientation)")

    pages_out: list[PageOut] = []
    last_chapter: int | None = None
    recent_rots: list[int] = []
    for i in range(n):
        img = render_page(doc, i, dpi=170)
        prefer = [90, 270, 0, 180]  # physics revision sheets usually need 90° then split
        if recent_rots:
            mode = max(set(recent_rots[-8:]), key=recent_rots[-8:].count)
            prefer = [mode] + [r for r in prefer if r != mode]
        sheets = normalize_sheet(
            img,
            force_rot=None,
            expect_two_up=True,
            flags=flags,
            source=pdf.name,
            src_page=i + 1,
            prefer_rots=prefer,
        )
        for half_i, (im, half, pretext, rot_used) in enumerate(sheets):
            recent_rots.append(rot_used)
            # OCR header band for classification
            band = im.crop((0, 0, im.width, max(80, im.height // 3)))
            text, score = ocr_score(band)
            if score < 50:
                text2, score2 = ocr_score(im)
                if score2 > score:
                    text, score = text2, score2
            if pretext and len(pretext) > len(text):
                text = pretext
            # Explicit chapter header patterns on upright A5 sheets
            m_ch = re.search(
                r"(?:^|\n)\s*(1[0-9]|20|[1-9])\s*\n\s*(Temperature|Thermodynamic|Electric Fields|Currents|Circuits|"
                r"Electromagnetic|Quantum|Nuclear|Quantities|Forces|Motion|Energy|Projectile|Collisions|"
                r"Circular|Gravitational|Oscillations|Wave|Superposition)",
                text,
                re.I,
            )
            meta = classify_text(text)
            if m_ch and meta["kind"] == "content":
                meta["chapter"] = int(m_ch.group(1))
            # Don't inherit chapter onto data/cover pages
            if meta["kind"] == "content" and meta["chapter"] is None and last_chapter:
                meta["chapter"] = last_chapter
            if meta["kind"] == "content" and meta["chapter"]:
                last_chapter = meta["chapter"]
            if meta["kind"] == "blank" or ink_ratio(im) < 0.003:
                meta["kind"] = "blank"
                flags.append(Flag(pdf.name, i + 1, "blank_page", f"half={half}"))
            po = PageOut(
                image=im,
                source=pdf.name,
                src_page=i + 1,
                half=half,
                text=text,
                kind=meta["kind"],
                chapter=meta["chapter"],
            )
            pages_out.append(po)
        if (i + 1) % 20 == 0:
            print(f"  ... {i+1}/{n}")

    doc.close()

    # Partition
    data_pages = [p for p in pages_out if p.kind == "data"]
    # also treat early formula sheets: pages with high "permeability"/"planck" hits
    for p in pages_out:
        tl = p.text.lower()
        if p.kind == "content" and ("planck" in tl or "permeability of free space" in tl or "list of formulae" in tl):
            p.kind = "data"
            data_pages.append(p)

    cover = [p for p in pages_out if p.kind == "cover"]
    content = [p for p in pages_out if p.kind in {"content", "unknown"} and p.kind != "blank"]
    # re-filter content excluding those reclassified as data
    content = [p for p in pages_out if p.kind == "content"]
    blanks = [p for p in pages_out if p.kind == "blank"]

    out_root = RAW / "H2 physics" / "base syllabus" / "revision packages"
    out_root.mkdir(parents=True, exist_ok=True)

    # Data booklet
    if data_pages:
        dest = out_root / "Data and Formulae Booklet.pdf"
        # de-dup if multiple packages contribute — append with source suffix if exists
        if dest.exists():
            dest = out_root / f"Data and Formulae Booklet - {pdf.stem[:40]}.pdf"
        images_to_pdf([p.image for p in data_pages], dest)
        report.outputs.append(str(dest.relative_to(REPO)))
        print(f"  wrote {dest.name} ({len(data_pages)} pages)")
    else:
        flags.append(Flag(pdf.name, 0, "missing_data_booklet", "No data/formulae pages detected"))

    # Group by chapter
    by_ch: dict[int, list[PageOut]] = defaultdict(list)
    unassigned: list[PageOut] = []
    for p in content:
        if p.chapter and p.chapter in PHYS_CH:
            by_ch[p.chapter].append(p)
        else:
            unassigned.append(p)

    for ch, plist in sorted(by_ch.items()):
        title = PHYS_CH[ch]
        dest = out_root / f"Chap {ch} {title} Revision Package.pdf"
        images_to_pdf([p.image for p in plist], dest)
        report.outputs.append(str(dest.relative_to(REPO)))
        print(f"  wrote {dest.name} ({len(plist)} pages)")

    if unassigned:
        dest = out_root / f"_unassigned from {pdf.stem[:50]}.pdf"
        images_to_pdf([p.image for p in unassigned], dest)
        report.outputs.append(str(dest.relative_to(REPO)))
        flags.append(
            Flag(pdf.name, 0, "unassigned_pages", f"{len(unassigned)} content pages without chapter id → {dest.name}")
        )
        print(f"  FLAG unassigned={len(unassigned)}")

    if cover:
        dest = out_root / f"Cover - {pdf.stem[:50]}.pdf"
        images_to_pdf([p.image for p in cover], dest)
        report.outputs.append(str(dest.relative_to(REPO)))

    report.sources[pdf.name] = {
        "pages": n,
        "out_pages": len(pages_out),
        "chapters": sorted(by_ch.keys()),
        "data_pages": len(data_pages),
        "blank_pages": len(blanks),
        "unassigned": len(unassigned),
    }


def process_math_exam_bundle(pdf: Path, report: Report, flags: list[Flag], *, kind: str, limit: int = 0) -> None:
    """kind: tys | prelim"""
    print(f"\n== Math {kind}: {pdf.name}")
    doc = fitz.open(pdf)
    n = doc.page_count
    if limit > 0:
        n = min(n, limit)
    samples = [render_page(doc, i, dpi=120) for i in range(min(4, doc.page_count))]
    force = detect_force_rotation(samples)
    print(f"  pages={n}/{doc.page_count} force_rot={force}")

    pages: list[PageOut] = []
    cur_year: int | None = None
    cur_paper: int | None = None

    for i in range(n):
        img = render_page(doc, i, dpi=170)
        sheets = normalize_sheet(
            img,
            force_rot=force,
            expect_two_up=False,
            flags=flags,
            source=pdf.name,
            src_page=i + 1,
        )
        for im, half, pretext, _rot in sheets:
            # footer + header OCR
            head = im.crop((0, 0, im.width, im.height // 5))
            foot = im.crop((0, im.height * 4 // 5, im.width, im.height))
            t1, s1 = ocr_score(head)
            t2, s2 = ocr_score(foot)
            text = t1 + "\n" + t2
            if s1 + s2 < 40:
                text_full, _ = ocr_score(im)
                text = text_full
            meta = classify_text(text)
            if meta["year"]:
                cur_year = meta["year"]
            if meta["paper"]:
                cur_paper = meta["paper"]
            # carry forward
            year = meta["year"] or cur_year
            paper = meta["paper"] or cur_paper
            if ink_ratio(im) < 0.003:
                meta["kind"] = "blank"
            pages.append(
                PageOut(
                    image=im,
                    source=pdf.name,
                    src_page=i + 1,
                    half=half,
                    text=text,
                    kind=meta["kind"],
                    year=year,
                    paper=paper,
                    school=meta.get("school") or ("RI" if kind == "prelim" else None),
                )
            )
        if (i + 1) % 25 == 0:
            print(f"  ... {i+1}/{n}")
    doc.close()

    # Split into segments when year/paper changes on a title-like page
    segments: list[tuple[int | None, int | None, list[PageOut]]] = []
    buf: list[PageOut] = []
    seg_y, seg_p = None, None
    for p in pages:
        if p.kind == "blank":
            continue
        # new segment if year/paper both known and differ from segment start after we already have pages
        if buf and p.year and p.paper and (seg_y, seg_p) != (None, None):
            if (p.year, p.paper) != (seg_y, seg_p):
                # only split when this page looks like a new cover (has PAPER / 9758)
                if re.search(r"paper\s*[12]|9758/0[12]|preliminary examination", p.text.lower()):
                    segments.append((seg_y, seg_p, buf))
                    buf = []
                    seg_y, seg_p = p.year, p.paper
        if not buf:
            seg_y, seg_p = p.year, p.paper
        else:
            if p.year and seg_y is None:
                seg_y = p.year
            if p.paper and seg_p is None:
                seg_p = p.paper
        buf.append(p)
    if buf:
        segments.append((seg_y, seg_p, buf))

    if kind == "tys":
        out_dir = RAW / "H2 math" / "TYS QP"
    else:
        out_dir = RAW / "H2 math" / "prelim QP"
    out_dir.mkdir(parents=True, exist_ok=True)

    wrote = 0
    for year, paper, plist in segments:
        if not year or not paper:
            dest = out_dir.parent / "misc" if False else WORK / "math_unassigned"
            dest.mkdir(parents=True, exist_ok=True)
            path = dest / f"_unassigned_{pdf.stem}_{wrote}.pdf"
            images_to_pdf([p.image for p in plist], path)
            flags.append(Flag(pdf.name, plist[0].src_page, "unassigned_exam_segment", f"pages={len(plist)} → {path.name}"))
            report.outputs.append(str(path.relative_to(REPO)))
            wrote += 1
            continue
        if kind == "tys":
            name = f"{year} P{paper} A-level H2 math.pdf"
        else:
            name = f"{year} RI P{paper} A-level H2 math.pdf"
        dest = out_dir / name
        if dest.exists():
            # keep existing digital copy; write scan beside with suffix
            dest = out_dir / f"{year} RI P{paper} A-level H2 math SCAN.pdf" if kind == "prelim" else out_dir / f"{year} P{paper} A-level H2 math SCAN.pdf"
            flags.append(Flag(pdf.name, plist[0].src_page, "dest_exists", f"wrote scan as {dest.name}"))
        images_to_pdf([p.image for p in plist], dest)
        report.outputs.append(str(dest.relative_to(REPO)))
        print(f"  wrote {dest.name} ({len(plist)} pages)")
        wrote += 1

    report.sources[pdf.name] = {"pages": n, "segments": wrote, "kind": kind}


def process_math_revision(pdf: Path, report: Report, flags: list[Flag], limit: int = 0) -> None:
    print(f"\n== Math revision: {pdf.name}")
    doc = fitz.open(pdf)
    n = doc.page_count
    if limit > 0:
        n = min(n, limit)
    samples = [render_page(doc, i, dpi=120) for i in range(min(4, doc.page_count))]
    force = detect_force_rotation(samples)
    print(f"  pages={n}/{doc.page_count} force_rot={force}")

    pages: list[PageOut] = []
    last_ch: int | None = None
    for i in range(n):
        img = render_page(doc, i, dpi=170)
        sheets = normalize_sheet(
            img,
            force_rot=force if i > 0 else None,
            expect_two_up=False,
            flags=flags,
            source=pdf.name,
            src_page=i + 1,
        )
        for im, half, _, _rot in sheets:
            head = im.crop((0, 0, im.width, im.height // 3))
            text, score = ocr_score(head)
            if score < 40:
                text, _ = ocr_score(im)
            meta = classify_text(text)
            if meta["kind"] == "content" and meta["chapter"] is None:
                meta["chapter"] = last_ch
            if meta["chapter"]:
                last_ch = meta["chapter"]
            if ink_ratio(im) < 0.003:
                meta["kind"] = "blank"
            # preface / syllabus checklist → data-like support docs
            tl = text.lower()
            if "list of formulae" in tl or "mf27" in tl or "mf26" in tl:
                meta["kind"] = "data"
            if "syllabus" in tl and "checklist" in tl:
                meta["kind"] = "data"
            if meta.get("kind") == "cover" or ("content" in tl and "preface" in tl):
                meta["kind"] = "cover"
            pages.append(
                PageOut(
                    image=im,
                    source=pdf.name,
                    src_page=i + 1,
                    half=half,
                    text=text,
                    kind=meta["kind"],
                    chapter=meta["chapter"],
                )
            )
        if (i + 1) % 20 == 0:
            print(f"  ... {i+1}/{n}")
    doc.close()

    out_root = RAW / "H2 math" / "revision packages"
    out_root.mkdir(parents=True, exist_ok=True)

    data = [p for p in pages if p.kind == "data"]
    cover = [p for p in pages if p.kind == "cover"]
    content = [p for p in pages if p.kind == "content"]

    if data:
        dest = out_root / "Data Booklet MF27 and Syllabus Checklist.pdf"
        images_to_pdf([p.image for p in data], dest)
        report.outputs.append(str(dest.relative_to(REPO)))
        print(f"  wrote {dest.name} ({len(data)} pages)")
    else:
        flags.append(Flag(pdf.name, 0, "missing_data_booklet", "MF/syllabus pages not detected"))

    if cover:
        dest = out_root / "Cover and Contents.pdf"
        images_to_pdf([p.image for p in cover], dest)
        report.outputs.append(str(dest.relative_to(REPO)))

    by_ch: dict[int, list[PageOut]] = defaultdict(list)
    unassigned = []
    for p in content:
        if p.chapter in MATH_CH:
            by_ch[p.chapter].append(p)
        else:
            unassigned.append(p)
    for ch, plist in sorted(by_ch.items()):
        dest = out_root / f"Chap {ch} {MATH_CH[ch]} Revision Package.pdf"
        images_to_pdf([p.image for p in plist], dest)
        report.outputs.append(str(dest.relative_to(REPO)))
        print(f"  wrote {dest.name} ({len(plist)} pages)")
    if unassigned:
        dest = out_root / "_unassigned math revision pages.pdf"
        images_to_pdf([p.image for p in unassigned], dest)
        flags.append(Flag(pdf.name, 0, "unassigned_pages", f"{len(unassigned)} pages"))
        report.outputs.append(str(dest.relative_to(REPO)))

    report.sources[pdf.name] = {
        "pages": n,
        "chapters": sorted(by_ch.keys()),
        "data_pages": len(data),
        "unassigned": len(unassigned),
    }


def archive_sources(paths: list[Path]) -> None:
    arch = RAW / "_incoming_scans_processed"
    arch.mkdir(parents=True, exist_ok=True)
    for p in paths:
        dest = arch / p.name
        if p.exists():
            shutil.move(str(p), str(dest))
            print(f"archived {p.name} → _incoming_scans_processed/")


def write_flags(flags: list[Flag]) -> None:
    lines = [
        "# Scan processing flags",
        "",
        f"Generated: {datetime.now(timezone.utc).isoformat()}",
        "",
        "| Source | Page | Issue | Detail |",
        "|---|---:|---|---|",
    ]
    for f in flags:
        detail = f.detail.replace("|", "\\|")
        lines.append(f"| `{f.source}` | {f.page} | {f.issue} | {detail} |")
    if not flags:
        lines.append("| — | — | none | All pages classified |")
    FLAGS_PATH.write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--skip-archive", action="store_true")
    ap.add_argument("--only", choices=["physics", "math", "all"], default="all")
    ap.add_argument("--limit", type=int, default=0, help="Process only first N pages per PDF (smoke test)")
    args = ap.parse_args()

    ensure_dirs()
    report = Report(started=datetime.now(timezone.utc).isoformat())
    flags: list[Flag] = []

    phys = [
        RAW / "H2 physics" / "physics revision package 1 (flipped 180deg).pdf",
        RAW / "H2 physics" / "physics revision package 2 (flipped 180deg).pdf",
        RAW / "H2 physics" / "physics revision package 3 first half.pdf",
        RAW / "H2 physics" / "physics revision package 3 second half.pdf",
    ]
    math_files = [
        (RAW / "H2 math" / "math A lvl 2016-2020.pdf", "tys"),
        (RAW / "H2 math" / "math A lvl 2021-2025.pdf", "tys"),
        (RAW / "H2 math" / "math prelim RI 2018-2025.pdf", "prelim"),
        (RAW / "H2 math" / "math revision booklet T3.pdf", "revision"),
    ]

    try:
        if args.only in {"physics", "all"}:
            for p in phys:
                if not p.exists():
                    flags.append(Flag(p.name, 0, "missing_source", str(p)))
                    continue
                process_physics_revision(p, report, flags, limit=args.limit)

        if args.only in {"math", "all"}:
            for p, kind in math_files:
                if not p.exists():
                    flags.append(Flag(p.name, 0, "missing_source", str(p)))
                    continue
                if kind == "revision":
                    process_math_revision(p, report, flags, limit=args.limit)
                else:
                    process_math_exam_bundle(p, report, flags, kind=kind, limit=args.limit)

        if not args.skip_archive and not args.limit:
            to_arch = [p for p in phys if p.exists()]
            to_arch += [p for p, _ in math_files if p.exists()]
            if report.outputs:
                archive_sources(to_arch)

    except Exception as exc:
        flags.append(Flag("_pipeline", 0, "fatal", f"{exc}"))
        traceback.print_exc()
        write_flags(flags)
        report.finished = datetime.now(timezone.utc).isoformat()
        report.flags = [asdict(f) for f in flags]
        REPORT_PATH.write_text(json.dumps(asdict(report), indent=2), encoding="utf-8")
        return 1

    write_flags(flags)
    report.finished = datetime.now(timezone.utc).isoformat()
    report.flags = [asdict(f) for f in flags]
    REPORT_PATH.write_text(json.dumps(asdict(report), indent=2), encoding="utf-8")
    print(f"\nFlags: {FLAGS_PATH}")
    print(f"Report: {REPORT_PATH}")
    print(f"Outputs: {len(report.outputs)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
