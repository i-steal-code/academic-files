"""Compose epoch question / answer PDFs from cropped source regions."""
import hashlib
import html
import json
import re
import subprocess
from pathlib import Path

import pymupdf

from _epoch_lib import ROOT, WORK, auto_regions, content_extent, has_text, load_overrides, open_doc, region_key

CHROME = r"C:\Program Files\Google\Chrome\Application\chrome.exe"
FONT = r"C:\Windows\Fonts\segoeui.ttf"
FONT_B = r"C:\Windows\Fonts\segoeuib.ttf"
PAGE_W, PAGE_H = 595.0, 842.0
MARGIN_X, MARGIN_TOP, MARGIN_BOT = 34.0, 34.0, 40.0
USABLE_W = PAGE_W - 2 * MARGIN_X
HTML_CACHE = WORK / "_html_pdf"

KATEX = """
<link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/katex@0.16.9/dist/katex.min.css">
<script defer src="https://cdn.jsdelivr.net/npm/katex@0.16.9/dist/katex.min.js"></script>
<script defer src="https://cdn.jsdelivr.net/npm/katex@0.16.9/dist/contrib/auto-render.min.js"
 onload="renderMathInElement(document.body,{delimiters:[{left:'$$',right:'$$',display:true},{left:'$',right:'$',display:false}],throwOnError:false});"></script>
"""

BASE_CSS = """
@page { size: A4; margin: 16mm 15mm 16mm 15mm; }
body { font-family: 'Segoe UI', Arial, sans-serif; font-size: 10.5pt; line-height: 1.45; color: #111; }
h1 { font-size: 17pt; margin: 0 0 6pt; } h2 { font-size: 13pt; margin: 14pt 0 4pt; border-bottom: 1px solid #ccc; }
h3 { font-size: 11.5pt; margin: 10pt 0 3pt; }
table { border-collapse: collapse; width: 100%; margin: 6pt 0; font-size: 9.5pt; }
th, td { border: 1px solid #bbb; padding: 3pt 5pt; vertical-align: top; text-align: left; }
th { background: #f0f0f0; } blockquote { margin: 6pt 0; padding: 4pt 8pt; background: #f6f6f6; border-left: 3px solid #999; }
code { font-size: 9pt; } .small { font-size: 9pt; color: #444; } .pb { page-break-before: always; }
"""


def html_to_pdf(body_html: str, name: str, extra_css: str = "") -> Path:
    HTML_CACHE.mkdir(exist_ok=True)
    doc = f"<!doctype html><html><head><meta charset='utf-8'>{KATEX}<style>{BASE_CSS}{extra_css}</style></head><body>{body_html}</body></html>"
    h = hashlib.md5(doc.encode("utf-8")).hexdigest()[:10]
    out = HTML_CACHE / f"{name}-{h}.pdf"
    if out.exists():
        return out
    src = HTML_CACHE / f"{name}-{h}.html"
    src.write_text(doc, encoding="utf-8")
    subprocess.run([CHROME, "--headless=new", "--disable-gpu", "--no-pdf-header-footer", "--virtual-time-budget=20000",
                    f"--print-to-pdf={out}", src.as_uri()], check=True, capture_output=True, timeout=180)
    return out


def md_to_html(md_text: str) -> str:
    import markdown

    stash = []

    def keep(m):
        stash.append(m.group(0))
        return f"\x00{len(stash) - 1}\x00"

    t = re.sub(r"\$\$.+?\$\$", keep, md_text, flags=re.S)
    t = re.sub(r"(?<!\\)\$[^$\n]+?\$", keep, t)
    out = markdown.markdown(t, extensions=["tables", "sane_lists"])
    return re.sub(r"\x00(\d+)\x00", lambda m: html.escape(stash[int(m.group(1))], quote=False), out)


def regen_pdf(md_rel: str) -> Path:
    md = (ROOT / md_rel).read_text(encoding="utf-8")
    return html_to_pdf(md_to_html(md), "regen-" + re.sub(r"\W+", "_", Path(md_rel).stem))


def overrides_regions(src, ov):
    key = region_key(src["pdf"], src["q"]) + ("|question" if src.get("qside") else "")
    o = ov.get(key)
    if not o:
        return None
    d = open_doc(src["pdf"])
    out = []
    for r in o["regions"]:
        p = r["page"] - 1
        H = d[p].rect.height
        out.append((p, r["top"] * H, r["bottom"] * H))
    return out


def doc_rel(d) -> str:
    return str(Path(d.name).resolve().relative_to(ROOT)).replace("\\", "/")


def compact(regs, min_blank=20.0, keep=6.0):
    """Split clips at blank horizontal bands taller than min_blank points, dropping the blank part."""
    from _epoch_lib import ink_rows

    out = []
    for d, p, clip in regs:
        rows = ink_rows(doc_rel(d), p)
        n, H = len(rows), d[p].rect.height
        a, b = int(clip.y0 / H * n), min(n, int(clip.y1 / H * n) + 1)
        seg_start, blank_run = clip.y0, 0
        last_ink = None
        for i in range(a, b):
            if rows[i]:
                if blank_run * H / n >= min_blank and last_ink is not None:
                    cut_top = last_ink + keep
                    out.append((d, p, pymupdf.Rect(clip.x0, seg_start, clip.x1, min(cut_top, clip.y1))))
                    seg_start = max(clip.y0, i / n * H - keep)
                blank_run = 0
                last_ink = (i + 1) / n * H
            else:
                blank_run += 1
        end = min(clip.y1, (last_ink + keep) if last_ink else clip.y1)
        if end - seg_start > 4:
            out.append((d, p, pymupdf.Rect(clip.x0, seg_start, clip.x1, end)))
    return out


def blank_split_y(d, p, clip):
    """A y inside clip near its middle that falls on a blank row."""
    from _epoch_lib import ink_rows

    rows = ink_rows(doc_rel(d), p)
    n, H = len(rows), d[p].rect.height
    mid = int((clip.y0 + clip.y1) / 2 / H * n)
    for off in range(0, n):
        for i in (mid - off, mid + off):
            if clip.y0 / H * n < i < clip.y1 / H * n and 0 <= i < n and not rows[i]:
                return (i + 0.5) / n * H
    return (clip.y0 + clip.y1) / 2


def blank_row_above(d, p, y_limit, y_min):
    """Lowest y <= y_limit (and > y_min) sitting in a run of at least 2 blank rows, else None."""
    from _epoch_lib import ink_rows

    rows = ink_rows(doc_rel(d), p)
    n, H = len(rows), d[p].rect.height
    i = min(n - 2, int(y_limit / H * n))
    while i / n * H > y_min:
        if not rows[i] and not rows[i - 1]:
            return (i - 0.5) / n * H
        i -= 1
    return None


def regions_for(src, ov):
    """[(doc, pno, clip Rect)] for a source, or [] if unavailable. Override regions are used exactly as given."""
    regs = _regions_for(src, ov)
    if src and "pdf" in src and overrides_regions(src, ov) is not None:
        return regs
    return compact(regs)


def _regions_for(src, ov):
    if not src:
        return []
    if "regen" in src:
        pdf = regen_pdf(src["regen"])
        d = pymupdf.open(str(pdf))
        rel = str(pdf.relative_to(ROOT)).replace("\\", "/")
        out = []
        for p in range(len(d)):
            ext = content_extent(rel, p, 0, d[p].rect.height)
            if ext:
                out.append((open_doc(rel), p, pymupdf.Rect(0, ext[0], d[p].rect.width, ext[1])))
        return out
    if not (ROOT / src["pdf"]).exists():
        return []
    regs = overrides_regions(src, ov)
    if regs is None and not src.get("manual"):
        regs = auto_regions(src["pdf"], src["q"])
    if not regs and src.get("pages") and not src.get("manual"):
        from _epoch_lib import hinted_regions

        regs = hinted_regions(src["pdf"], src["q"], src["pages"])
    if not regs:
        return []
    d = open_doc(src["pdf"])
    out = []
    for p, y0, y1 in regs:
        W = d[p].rect.width
        out.append((d, p, pymupdf.Rect(0.03 * W, y0, 0.97 * W, y1)))
    return out


class Layout:
    def __init__(self, doc):
        self.doc = doc
        self.page = None
        self.y = 0

    def new_page(self):
        self.page = self.doc.new_page(width=PAGE_W, height=PAGE_H)
        self.page.insert_font(fontname="seg", fontfile=FONT)
        self.page.insert_font(fontname="segb", fontfile=FONT_B)
        self.y = MARGIN_TOP
        return self.page

    def room(self):
        return PAGE_H - MARGIN_BOT - self.y if self.page else -1

    def text(self, x, y, s, size=9, bold=False, color=(0, 0, 0)):
        self.page.insert_text((x, y), s, fontname="segb" if bold else "seg", fontsize=size, color=color)

    def wrap(self, s, size, width):
        f = pymupdf.Font(fontfile=FONT)
        words, lines, cur = s.split(), [], ""
        for w in words:
            t = (cur + " " + w).strip()
            if f.text_length(t, fontsize=size) > width and cur:
                lines.append(cur)
                cur = w
            else:
                cur = t
        if cur:
            lines.append(cur)
        return lines

    def banner(self, title, lines, fill=(0.90, 0.93, 0.98)):
        body = [ln for s in lines for ln in self.wrap(s, 8.5, USABLE_W - 16)]
        h = 22 + 11.5 * len(body)
        if self.room() < h + 60:
            self.new_page()
        r = pymupdf.Rect(MARGIN_X, self.y, PAGE_W - MARGIN_X, self.y + h)
        self.page.draw_rect(r, color=None, fill=fill)
        self.text(MARGIN_X + 8, self.y + 15, title, size=11, bold=True)
        yy = self.y + 28
        for ln in body:
            self.text(MARGIN_X + 8, yy, ln, size=8.5, color=(0.2, 0.2, 0.2))
            yy += 11.5
        self.y += h + 8

    def item_header(self, ident, line1, line2, first_h):
        l2 = self.wrap(line2, 8, USABLE_W - 12) if line2 else []
        h = 17 + 10 * len(l2)
        if self.room() < h + min(first_h, 140) + 6:
            self.new_page()
        r = pymupdf.Rect(MARGIN_X, self.y, PAGE_W - MARGIN_X, self.y + h)
        self.page.draw_rect(r, color=(0.55, 0.55, 0.55), fill=(0.95, 0.95, 0.95), width=0.6)
        self.text(MARGIN_X + 6, self.y + 12, ident, size=9.5, bold=True)
        self.text(MARGIN_X + 62, self.y + 12, line1, size=9, bold=True, color=(0.15, 0.15, 0.15))
        yy = self.y + 23
        for ln in l2:
            self.text(MARGIN_X + 6, yy, ln, size=8, color=(0.3, 0.3, 0.3))
            yy += 10
        self.y += h + 4
        return self.page

    def place(self, src_doc, pno, clip):
        scale = min(1.0, USABLE_W / clip.width)
        h = clip.height * scale
        full = PAGE_H - MARGIN_TOP - MARGIN_BOT
        if h > full:
            mid = blank_split_y(src_doc, pno, clip)
            self.place(src_doc, pno, pymupdf.Rect(clip.x0, clip.y0, clip.x1, mid))
            self.place(src_doc, pno, pymupdf.Rect(clip.x0, mid, clip.x1, clip.y1))
            return
        if self.room() < h:
            if self.room() > 160 and h > 200:
                cut = blank_row_above(src_doc, pno, clip.y0 + (self.room() - 6) / scale, clip.y0 + 40)
                if cut:
                    self.place(src_doc, pno, pymupdf.Rect(clip.x0, clip.y0, clip.x1, cut))
                    self.place(src_doc, pno, pymupdf.Rect(clip.x0, cut, clip.x1, clip.y1))
                    return
            self.new_page()
        w = clip.width * scale
        target = pymupdf.Rect(MARGIN_X, self.y, MARGIN_X + w, self.y + h)
        self.page.show_pdf_page(target, src_doc, pno, clip=clip)
        self.y += h + 3

    def note(self, s):
        lines = self.wrap(s, 9, USABLE_W - 10)
        if self.room() < 12 * len(lines) + 8:
            self.new_page()
        for ln in lines:
            self.text(MARGIN_X + 5, self.y + 10, ln, size=9, color=(0.6, 0.1, 0.1))
            self.y += 12
        self.y += 4

    def gap(self, g=10):
        self.y += g


def add_footers(doc, label, offset):
    for i, page in enumerate(doc):
        page.insert_font(fontname="seg", fontfile=FONT)
        page.insert_text((MARGIN_X, PAGE_H - 18), label, fontname="seg", fontsize=7.5, color=(0.45, 0.45, 0.45))
        s = f"{i + 1 + offset}"
        page.insert_text((PAGE_W - MARGIN_X - 12, PAGE_H - 18), s, fontname="seg", fontsize=8, color=(0.3, 0.3, 0.3))
