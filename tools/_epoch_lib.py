"""Shared helpers for building topical epoch packs: source resolution and question region detection."""
import json
import re
from functools import lru_cache
from pathlib import Path

import pymupdf

ROOT = Path(__file__).resolve().parents[1]
RAW = ROOT / "raw files" / "H2 math"
WORK = ROOT / "tools" / "_scan_work"

NUM_RE = re.compile(r"^\s*(?:Q(?:n|uestion)?\.?\s*)?(\d{1,2})\s*(?:[.)]\s*)?(?:\(|\[|[A-Za-z]|$)")
HEADER_RE = re.compile(
    r"(turn over|page \d+|\d+\s*(of|/)\s*\d+|9758|©|raffles|junior college|institution|preliminary|"
    r"prelim|answer all|blank page|for examiner|\[\s*turn|end of paper|continued)",
    re.I,
)


@lru_cache(maxsize=None)
def open_doc(path: str):
    return pymupdf.open(str(ROOT / path))


def has_text(path: str) -> bool:
    d = open_doc(path)
    return sum(len(d[i].get_text()) for i in range(min(len(d), 4))) > 200


OCR_CACHE = WORK / "_ocr_cache"


def ocr_page(path: str, pno: int):
    """Windows OCR lines for a scanned page as [(x0_frac, y0_frac, y1_frac, text)], cached on disk."""
    import hashlib

    OCR_CACHE.mkdir(exist_ok=True)
    key = hashlib.md5(f"{path}|{pno}".encode()).hexdigest()
    f = OCR_CACHE / f"{key}.json"
    if f.exists():
        return json.loads(f.read_text(encoding="utf-8"))
    import winocr
    from PIL import Image

    pix = open_doc(path)[pno].get_pixmap(dpi=150)
    img = Image.frombytes("RGB", (pix.width, pix.height), pix.samples)
    res = winocr.recognize_pil_sync(img, "en")
    lines = []
    for ln in res["lines"]:
        ws = ln["words"]
        r0 = ws[0]["bounding_rect"]
        y1 = max(w["bounding_rect"]["y"] + w["bounding_rect"]["height"] for w in ws)
        lines.append((r0["x"] / pix.width, r0["y"] / pix.height, y1 / pix.height, ln["text"]))
    f.write_text(json.dumps(lines), encoding="utf-8")
    return lines


@lru_cache(maxsize=None)
def ink_rows(path: str, pno: int):
    """Per-row ink flags (top to bottom) of a page rendered at 50 dpi."""
    pix = open_doc(path)[pno].get_pixmap(dpi=50, colorspace=pymupdf.csGRAY)
    w, h = pix.width, pix.height
    s = pix.samples
    rows = []
    for y in range(h):
        row = s[y * w + int(0.04 * w): y * w + int(0.96 * w)]
        rows.append(any(v < 175 for v in row))
    return rows


def ink_extent(path: str, pno: int, y0: float, y1: float):
    page = open_doc(path)[pno]
    H = page.rect.height
    rows = ink_rows(path, pno)
    n = len(rows)
    a, b = int(y0 / H * n), min(n, int(y1 / H * n) + 1)
    hits = [i for i in range(a, b) if rows[i]]
    if not hits:
        return None
    return max(y0, hits[0] / n * H - 4), min(y1, (hits[-1] + 1) / n * H + 4)


@lru_cache(maxsize=None)
def candidates(path: str):
    if not has_text(path):
        out = []
        for pno in range(len(open_doc(path))):
            W = open_doc(path)[pno].rect.width
            H = open_doc(path)[pno].rect.height
            for x0, y0, _, text in ocr_page(path, pno):
                if x0 > 0.12 or y0 > 0.93 or y0 < 0.03:
                    continue
                head = text.strip().split(" ")[0]
                if len(head) <= 2:
                    head = head.translate(str.maketrans("IlO|o", "11010"))
                    text = head + text.strip()[len(head):]
                m = re.match(r"^\s*(\d{1,2})\s*$", text) or re.match(r"^\s*(\d{1,2})\s+\S", text)
                if m and 1 <= int(m.group(1)) <= 25:
                    out.append((pno, round(y0 * H, 1), int(m.group(1)), round(x0 * W, 1)))
        out.sort()
        return out
    d = open_doc(path)
    out = []
    for pno, page in enumerate(d):
        W = page.rect.width
        for b in page.get_text("dict")["blocks"]:
            for ln in b.get("lines", []):
                spans = [s for s in ln["spans"] if s["text"].strip()]
                if not spans:
                    continue
                text = "".join(s["text"] for s in spans).strip()
                x0 = spans[0]["bbox"][0]
                if x0 > 0.22 * W:
                    continue
                m = NUM_RE.match(text)
                if m and 1 <= int(m.group(1)) <= 25:
                    out.append((pno, round(ln["bbox"][1], 1), int(m.group(1)), round(x0, 1)))
    out.sort()
    return out


@lru_cache(maxsize=None)
def question_starts(path: str, max_q: int = 25):
    """Sequentially locate question 1, 2, 3, ... at a consistent left margin."""
    cands = candidates(path)
    scanned = not has_text(path)
    tol = 24 if scanned else 14
    seeds = [c for c in cands if c[2] == 1][:6] or [c for c in cands if c[2] == 2][:3]
    best = {}
    for seed in seeds:
        margin = seed[3]
        pool = [c for c in cands if abs(c[3] - margin) <= tol]
        starts = {seed[2]: (seed[0], seed[1])}
        pos = (seed[0], seed[1])
        misses = 0
        for q in range(seed[2] + 1, max_q + 1):
            hit = next((c for c in pool if (c[0], c[1]) > pos and c[2] == q), None)
            if hit is None:
                misses += 1
                if misses > (2 if scanned else 0):
                    break
                continue
            misses = 0
            starts[q] = (hit[0], hit[1])
            pos = (hit[0], hit[1])
        if len(starts) > len(best):
            best = starts
    return best


def next_start(starts, q, doc):
    later = sorted(k for k in starts if k > q)
    if later:
        return starts[later[0]]
    return len(doc) - 1, doc[-1].rect.height * 0.935


def _norm(t: str) -> str:
    return re.sub(r"[\d\s|]+", "", t).lower()[:60]


@lru_cache(maxsize=None)
def running_texts(path: str):
    """Normalised texts of blocks repeated near the top or bottom of many pages (running headers/footers)."""
    d = open_doc(path)
    from collections import Counter

    cnt = Counter()
    for page in d:
        H = page.rect.height
        seen = set()
        for b in page.get_text("blocks"):
            if b[4].strip() and (b[3] < 0.16 * H or b[1] > 0.84 * H):
                k = _norm(b[4])
                if k and k not in seen:
                    seen.add(k)
                    cnt[k] += 1
    need = max(3, int(0.4 * len(d)))
    return {k for k, v in cnt.items() if v >= need}


@lru_cache(maxsize=None)
def page_band(path: str, pno: int):
    """(top, bottom) between running header and footer blocks on this page."""
    page = open_doc(path)[pno]
    H = page.rect.height
    run = running_texts(path)
    top, bot = 0.0, H
    for b in page.get_text("blocks"):
        if not b[4].strip():
            continue
        if _norm(b[4]) in run or HEADER_RE.search(b[4]) and (b[3] < 0.09 * H or b[1] > 0.91 * H):
            if b[3] < 0.16 * H:
                top = max(top, b[3] + 1)
            elif b[1] > 0.84 * H:
                bot = min(bot, b[1] - 1)
    for dr in page.get_drawings():
        r = dr["rect"]
        if r.height < 3 and r.width > 0.5 * page.rect.width:
            if top - 14 <= r.y0 <= top + 14 and r.y0 < 0.18 * H:
                top = max(top, r.y1 + 1)
            if bot - 14 <= r.y1 <= bot + 14 and r.y0 > 0.82 * H:
                bot = min(bot, r.y0 - 1)
    return top, bot


def body_bounds(path: str, pno: int):
    """Top and bottom of the page body, ignoring running headers and footers."""
    page = open_doc(path)[pno]
    H = page.rect.height
    ys = []
    for b in page.get_text("blocks"):
        x0, y0, x1, y1, text = b[0], b[1], b[2], b[3], b[4]
        if not text.strip():
            continue
        if (y1 < 0.09 * H or y0 > 0.91 * H) and (HEADER_RE.search(text) or len(text.strip()) < 6):
            continue
        ys.append((y0, y1))
    for dr in page.get_drawings():
        r = dr["rect"]
        if r.height < 0.85 * H and r.width < 0.95 * page.rect.width:
            ys.append((r.y0, r.y1))
    for img in page.get_image_info():
        r = pymupdf.Rect(img["bbox"])
        if r.height < 0.9 * H:
            ys.append((r.y0, r.y1))
    if not ys:
        return None
    return max(0.0, min(y for y, _ in ys) - 4), min(H, max(y for _, y in ys) + 4)


def content_extent(path: str, pno: int, y0: float, y1: float):
    """Shrink [y0, y1] to the content actually present on the page in that band."""
    page = open_doc(path)[pno]
    H = page.rect.height
    bt, bb = page_band(path, pno)
    y0, y1 = max(y0, bt), min(y1, bb)
    if y1 - y0 < 4:
        return None
    ys = []
    for b in page.get_text("blocks"):
        if not b[4].strip():
            continue
        if b[3] <= y0 or b[1] >= y1:
            continue
        if (b[3] < 0.09 * H or b[1] > 0.91 * H) and (HEADER_RE.search(b[4]) or len(b[4].strip()) < 6):
            continue
        ys.append((max(b[1], y0), min(b[3], y1)))
    for dr in page.get_drawings():
        r = dr["rect"]
        if r.y1 <= y0 or r.y0 >= y1 or r.height > 0.85 * H:
            continue
        ys.append((max(r.y0, y0), min(r.y1, y1)))
    for img in page.get_image_info():
        r = pymupdf.Rect(img["bbox"])
        if r.y1 <= y0 or r.y0 >= y1 or r.height > 0.9 * H:
            continue
        ys.append((max(r.y0, y0), min(r.y1, y1)))
    if not ys:
        return None
    return max(y0, min(a for a, _ in ys) - 3), min(y1, max(b for _, b in ys) + 3)


def auto_regions(path: str, q: int):
    """Regions [(pno, y0, y1)] covering question q, or None if it cannot be located."""
    if not has_text(path):
        return scanned_regions(path, q)
    starts = question_starts(path)
    if q not in starts:
        return None
    d = open_doc(path)
    p0, y0 = starts[q]
    p1, y1 = next_start(starts, q, d)
    regions = []
    for p in range(p0, p1 + 1):
        bb = body_bounds(path, p)
        if bb is None:
            continue
        top = y0 - 4 if p == p0 else bb[0]
        bot = y1 - 2 if p == p1 else bb[1]
        if bot - top < 8:
            continue
        ext = content_extent(path, p, top, bot)
        if ext and ext[1] - ext[0] > 6:
            regions.append((p, round(ext[0], 1), round(ext[1], 1)))
    return regions or None


def page_has_question_text(path: str, pno: int, f0: float, f1: float) -> bool:
    for _, y0, _, text in ocr_page(path, pno):
        t = text.strip()
        if not (f0 <= y0 <= f1):
            continue
        if re.fullmatch(r"[\d\s\[\]()IlO|]*", t) or re.search(r"turn over|blank page|continued", t, re.I):
            continue
        if len(t) >= 4:
            return True
    return False


def scanned_regions(path: str, q: int):
    starts = question_starts(path)
    if q not in starts:
        return None
    d = open_doc(path)
    p0, y0 = starts[q]
    p1, y1 = next_start(starts, q, d)
    regions = []
    for p in range(p0, p1 + 1):
        H = d[p].rect.height
        top = y0 - 6 if p == p0 else 0.055 * H
        bot = y1 - 4 if p == p1 else 0.95 * H
        if bot - top < 10:
            continue
        if p != p0 and not page_has_question_text(path, p, top / H, bot / H):
            continue
        ext = ink_extent(path, p, top, bot)
        if ext and ext[1] - ext[0] > 8:
            regions.append((p, round(ext[0], 1), round(ext[1], 1)))
    return regions or None


def hinted_regions(path: str, q: int, pages):
    """Fallback when sequential detection fails: find question q on the given 1-based pages."""
    d = open_doc(path)
    pg = sorted(p - 1 for p in pages if 1 <= p <= len(d))
    if not pg:
        return None
    cands = [c for c in candidates(path) if pg[0] <= c[0] <= pg[-1] + 1]
    start = next((c for c in cands if c[2] == q and c[0] in pg), None)
    if start:
        p0, y0 = start[0], start[1]
        nxt = next((c for c in cands if (c[0], c[1]) > (p0, y0) and c[2] > q and abs(c[3] - start[3]) <= 24), None)
    else:
        p0, y0, nxt = pg[0], 0.0, None
    p1, y1 = (nxt[0], nxt[1]) if nxt else (pg[-1], d[pg[-1]].rect.height)
    scanned = not has_text(path)
    regions = []
    for p in range(p0, p1 + 1):
        H = d[p].rect.height
        if scanned:
            top = y0 - 6 if p == p0 else 0.055 * H
            bot = y1 - 4 if (p == p1 and nxt) else 0.95 * H
            ext = ink_extent(path, p, top, bot)
        else:
            bb = body_bounds(path, p) or (0, H)
            top = y0 - 4 if (p == p0 and start) else bb[0]
            bot = y1 - 2 if (p == p1 and nxt) else bb[1]
            ext = content_extent(path, p, top, bot)
        if ext and ext[1] - ext[0] > 6:
            regions.append((p, round(ext[0], 1), round(ext[1], 1)))
    return regions or None


def load_overrides():
    out = {}
    for f in sorted(WORK.glob("epoch_regions_override*.json")):
        out.update(json.loads(f.read_text(encoding="utf-8")))
    return out


def region_key(path: str, q) -> str:
    return f"{path}#{q}"
