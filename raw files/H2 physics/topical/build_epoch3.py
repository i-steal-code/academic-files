"""Build Physics Epoch 3: exam-style papers on the user's weaker topics, weighted by the Paper 3 analysis.

Goal (user, 14 Nov): the highest attainable mark on every highly weighted topic, with enough hedging on the rest
that leaks are kept to a minimum. Section B option choice is drilled separately, so there is no choice here.

- Paper 1 (2 h): the weak, highly weighted topics: electric fields and capacitance, circuits and RC, gravitation,
  EM forces, nuclear.
- Paper 2 (2 h): a second pass at the high-weight topics, one long E-and-B question, and the likely hedges
  (oscillations, mechanics, superposition, quantum).
- Paper 3 (about 50 min): the remaining hedges (wave motion, thermal leftovers, measurement, impulse, line spectra).

Question documents look like an exam paper: each header carries only the question number and the item code.
Topic, source and method notes are on the answer scheme and in the plan only (rule: no hints on question documents).
Questions are in mixed topic order.

Source: unseen 2026 prelim P3 questions, including HCI and EJC (released for mining, 14 Nov). NJC P3 stays whole.
Seen sets (NYJC, ACJC, RVHS, RI), MI (9749 format) and every question used in Epoch 2 are excluded.

Run:  .venv-convert/Scripts/python.exe -I "raw files/H2 physics/topical/build_epoch3.py"
"""
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT / "tools"))
sys.path.insert(0, str(Path(__file__).resolve().parent))
sys.stdout.reconfigure(encoding="utf-8")

import pymupdf  # noqa: E402
from _epoch_compose import (MARGIN_BOT, MARGIN_TOP, PAGE_H, USABLE_W, Layout, add_footers, compact,  # noqa: E402
                            regions_for)
from _epoch_lib import HEADER_RE, load_overrides, open_doc, question_starts, next_start  # noqa: E402
from build_epoch2 import analysis, readiness  # noqa: E402

PHYS = "raw files/H2 physics"
OUT = ROOT / PHYS / "topical" / "Epoch 3"
QP = PHYS + "/exam papers/prelim QP/2026 {s} P3 prelim H2 physics.pdf"
ANS = PHYS + "/exam papers/prelim ANS/2026 {s} P3 prelim H2 physics.pdf"
MIN_PER_MARK = 1.6

BLOCKED = {"NYJC", "ACJC", "RVHS", "RI", "MI", "NJC"}  # seen, 9749 format, or kept whole
USED_EPOCH2 = {("TJC", 6), ("SAJC", 6), ("YIJC", 3), ("JPJC", 3), ("DHS", 5), ("VJC", 7), ("YIJC", 6), ("ASRJC", 4),
               ("VJC", 6), ("JPJC", 9), ("DHS", 7), ("TMJC", 8)}

# Topic code -> (chapter for the lowball, label). Codes follow the analysis where it has one.
TOPIC = {
    "EFLD": (14, "Electric fields and capacitance"), "CIRCUITS": (16, "D.c. circuits, capacitors and RC"),
    "GRAV": (8, "Gravitational fields"), "EMFOR": (17, "EM forces"), "NUCL": (20, "Nuclear physics"),
    "OSC": (9, "Oscillations"), "SUPER": (11, "Superposition (not gratings)"), "QUANT": (19, "Quantum (not the box)"),
    "WAVEM": (10, "Wave motion"), "THERM": (12, "Thermal leftovers"), "MEAS": (1, "Measurement"),
    "MECH-C": (6, "Mechanics: collisions and impulse"), "MECH-P": (5, "Mechanics: projectile motion"),
}

# (paper, topic, school, question, answer-side note). Order within a paper is the printed order (topics mixed).
ITEMS = [
    (1, "GRAV", "HCI", 2, "Geostationary orbit, then an elliptical orbit: Δφ, ΔE_K and why the design is hard."),
    (1, "CIRCUITS", "CJC", 2, "Energy from a Q–V graph; six capacitors in parallel; RC timing of a reset."),
    (1, "EMFOR", "ASRJC", 5, "Current balance (moments give B), then an electron's circular path: sketch and r = mv/Bq."),
    (1, "EFLD", "CJC", 1, "Field lines of two unequal spheres; E from the gradient of a V–x graph."),
    (1, "CIRCUITS", "DHS", 1, "Thermistor in a series circuit: currents, R, energy left in the battery, effect of a change."),
    (1, "NUCL", "HCI", 8, "BE per nucleon curve: why fission releases energy; mass from BE; energy released."),
    (1, "EFLD", "YIJC", 5, "E between plates, minimum launch speed, effect of doubling d; then a capacitor."),
    (1, "GRAV", "EJC", 5, "g equals free-fall acceleration; Earth's mass; surface potential and why it is negative."),
    (1, "CIRCUITS", "HCI", 5, "Battery with resistors switched in parallel: random vs systematic effects, 1/I against R."),
    (2, "MECH-C", "SAJC", 2, "Two trolleys: acceleration during the collision, then the final velocity of A."),
    (2, "OSC", "HCI", 3, "Needle in s.h.m.: ω, maximum acceleration, contact force at the extremes, sketch."),
    (2, "CIRCUITS", "JPJC", 5, "Internal resistance and energy; minimum resistance from an I–V graph (V/I, not gradient)."),
    (2, "GRAV", "SAJC", 3, "E_P = −2E_K for an orbit; total energy from a φ–r graph; two spheres."),
    (2, "QUANT", "HCI", 7, "Photoelectric evidence for photons; electron microscope and a 140 nm virus; solar sail."),
    (2, "NUCL", "EJC", 7, "β decay equation, conserved quantities, mass defect and BE per nucleon."),
    (2, "MECH-P", "YIJC", 2, "Package dropped from a drone: time, range, does the hiker catch it."),
    (2, "SUPER", "EJC", 6, "Principle of superposition; stationary wave in a tube; frequency from node spacing."),
    (2, "EMFOR", "EJC", 8, "Long question: particle between plates, then a magnetic field: the cyclotron (E and B together)."),
    (3, "MEAS", "ASRJC", 1, "Derived units; a constant's units from a homogeneous equation; uncertainty."),
    (3, "MECH-C", "TMJC", 3, "Impulse from an F–t graph, p–t sketch, then a wall collision and conservation of momentum."),
    (3, "THERM", "EJC", 3, "Specific heat capacity and latent heat: water poured onto ice, final state."),
    (3, "WAVEM", "EJC", 4, "Intensity from a point source (inverse square), amplitude; polarisation and Malus's law."),
    (3, "QUANT", "CJC", 5, "Line spectra as evidence for discrete levels; a transition wavelength and its region."),
]
PAPER_NAME = {1: "Paper 1", 2: "Paper 2", 3: "Paper 3 (hedges)"}

# Defects in the source papers, found in the page-by-page check. "q" notes are corrections of data only (never a
# method hint) and print under the question header; "a" notes print under the answer header.
ERRATA = {
    ("YIJC", 5): {"q": "Correction to the printed figure: in Fig. 5.1, plate A is at −4.5 V, as the text of (b) says."},
    ("TMJC", 3): {"a": "Source defects. The row labelled (b)(i) answers (c)(i), and its '6.0 s' means 6.0 ms. The (c)(ii) "
                       "sketch is incomplete: p rises from 1.0 N s with increasing gradient to 1.8 N s at 2.0 ms, is a "
                       "straight line to 3.4 N s at 4.0 ms, then rises with decreasing gradient to level off at "
                       "4.2 N s at 6.0 ms."},
    ("CJC", 2): {"a": "Source typo in (a)(i): ½CV² = ½(100 × 10⁻¹²)(2.5)² = 3.125 × 10⁻¹⁰ J = 3.13 × 10⁻¹⁰ J."},
}


def marks_of(school, q):
    p = QP.format(s=school)
    st = question_starts(p)
    d = open_doc(p)
    p0, y0 = st[q]
    p1, y1 = next_start(st, q, d)
    txt = ""
    for pg in range(p0, p1 + 1):
        r = d[pg].rect
        txt += d[pg].get_text(clip=pymupdf.Rect(0, y0 if pg == p0 else 0, r.width, y1 if pg == p1 else r.height))
    parts = sum(int(m) for m in re.findall(r"\[(\d{1,2})\]", txt))
    stated = re.findall(r"\[Total:?\s*(\d+)", txt)
    return parts, (int(stated[-1]) if stated else None)


def build_plan():
    rd, an = readiness(), analysis()
    items, n = [], {}
    for paper, k, s, q, why in ITEMS:
        assert s not in BLOCKED and (s, q) not in USED_EPOCH2, f"{s} Q{q} is blocked or already used"
        mk, stated = marks_of(s, q)
        n[paper] = n.get(paper, 0) + 1
        ch, name = TOPIC[k]
        items.append({"paper": paper, "no": n[paper], "id": f"E3-{paper}{n[paper]:02d}", "key": k, "ch": ch,
                      "topic": name, "ref": f"{s} 2026 P3 Q{q}", "marks": mk, "stated": stated, "why": why,
                      "low": rd[ch]["low"], "exp": an.get(k, (None, None))[0],
                      "qsrc": {"pdf": QP.format(s=s), "q": q}, "ssrc": {"pdf": ANS.format(s=s), "q": q}})
    return items


# ---- Region repair (14 Nov, after a page-by-page check of the first build) --------------------------------------
# The shared auto-cropper is tuned for math papers. On these physics papers it (1) lost answer rows near page
# breaks, (2) kept whatever followed a question's [Total] line (BLANK PAGE, the Section B heading), (3) let a figure
# straddle an output page break, and (4) kept margin strips and page furniture. The functions below fix those.

def page_bounds(page, school, side):
    """Top and bottom of the usable body: below running headers, above running footers."""
    H = page.rect.height
    top, bot = 0.035 * H, 0.965 * H
    footers = []
    for b in page.get_text("blocks"):
        y0, y1, text = b[1], b[3], b[4].strip()
        if not text or (b[3] - b[1]) > 0.3 * H:  # rotated margin strips are tall: not a header
            continue
        # Running headers, footers and bare page numbers only. A short token such as "[B1]" near the foot of a
        # page is content: treating it as furniture cut the last line of an answer (CJC Q1).
        furniture = HEADER_RE.search(text) or re.fullmatch(r"[\d\s\-–]+", text)
        if y1 < 0.09 * H and furniture:
            top = max(top, y1 + 1)
        elif y0 > 0.91 * H and furniture:
            bot = min(bot, y0 - 1)
            footers.append((y0, y1))
    for img in page.get_image_info():  # a small logo sitting beside the footer text (TMJC crest)
        iy0, iy1 = img["bbox"][1], img["bbox"][3]
        if iy1 - iy0 < 0.08 * H and iy0 > 0.86 * H and any(iy0 < f1 + 12 and iy1 > f0 - 12 for f0, f1 in footers):
            bot = min(bot, iy0 - 1)
    if school == "HCI" and side == "q":  # corner hatching and page number sit above 7.5%, the footer below 92.5%
        top, bot = max(top, 0.075 * H), min(bot, 0.925 * H)
    return top, bot


def clean(regs, school, side, clamp_y=True):
    """Clamp regions to the page body and cut 'DO NOT WRITE IN THIS MARGIN' strips off the sides."""
    out = []
    for d, p, clip in regs:
        page = d[p]
        W = page.rect.width
        top, bot = page_bounds(page, school, side) if clamp_y else (clip.y0, clip.y1)
        x0, x1 = clip.x0, clip.x1
        for b in page.get_text("blocks"):
            if "THIS MARGIN" in b[4].upper() or "DO NOT WRITE" in b[4].upper():
                if b[2] < 0.5 * W:
                    x0 = max(x0, b[2] + 2)
                elif b[0] > 0.5 * W:
                    x1 = min(x1, b[0] - 2)
        for dr in page.get_drawings():  # the grey bar behind that strip is wider than its text
            r = dr["rect"]
            # Only a bar hugging the page edge counts: table rules and shaded mark columns are tall and thin too,
            # and clipping at those cut the marks column off some answer tables.
            if r.height > 0.5 * page.rect.height and r.width < 0.08 * W and dr.get("fill"):
                if r.x1 < 0.07 * W:
                    x0 = max(x0, r.x1 + 3)
                elif r.x0 > 0.93 * W:
                    x1 = min(x1, r.x0 - 3)
        y0, y1 = max(clip.y0, top), min(clip.y1, bot)
        if y1 - y0 > 6:
            out.append((d, p, pymupdf.Rect(x0, y0, x1, y1)))
    return out


def trim_total(regs):
    """Question side: end at this question's own [Total] line; drop a previous question's [Total] at the very top."""
    hits = [(i, r) for i, (d, p, clip) in enumerate(regs) for r in d[p].search_for("[Total", clip=clip)]
    if not hits:
        return regs
    regs = list(regs)
    i0, r0 = hits[0]
    if i0 == 0 and r0.y1 < regs[0][2].y0 + 45:  # leftover from the question before
        d, p, c = regs[0]
        regs[0] = (d, p, pymupdf.Rect(c.x0, r0.y1 + 2, c.x1, c.y1))
        hits = hits[1:]
    if not hits:
        return regs
    i, r = hits[-1]
    d, p, c = regs[i]
    return regs[:i] + [(d, p, pymupdf.Rect(c.x0, c.y0, c.x1, min(c.y1, r.y1 + 4)))]


def answer_regions(pdf, q):
    """Answer side: everything from this question's start to the next one's, page by page, without body trimming."""
    st = question_starts(pdf)
    if q not in st:
        return []
    d = open_doc(pdf)
    (p0, y0), (p1, y1) = st[q], next_start(st, q, d)
    # A table heading row ('Qns | Answer | Marks') just above the first row is kept whole, not sliced through.
    # It must be a line made only of heading words, at least two of them ("Answer all the questions" is not one).
    lines = {}
    for w in d[p0].get_text("words"):
        if y0 - 30 < w[1] < y0 - 3:
            lines.setdefault(round(w[1] / 4), []).append(w)
    heads = [min(w[1] for w in ws) for ws in lines.values()
             if len(ws) >= 2 and all(TABLE_HEAD.fullmatch(w[4].strip()) for w in ws)]
    first_top = (min(heads) - 5) if heads else (y0 - 6)
    out = []
    for p in range(p0, p1 + 1):
        W, H = d[p].rect.width, d[p].rect.height
        top = first_top if p == p0 else 0.0
        bot = y1 - 2 if p == p1 else H
        if bot - top > 6:
            out.append((d, p, pymupdf.Rect(0.03 * W, top, 0.97 * W, bot)))
    return out


TABLE_HEAD = re.compile(r"\b(qns?|answers?|marks?|no\.?|solution|remarks?|question)\b", re.I)


def drop_slivers(regs):
    """Drop short pieces that hold only a repeated table heading row ('Qns | Answer | Marks') or nothing."""
    out = []
    for d, p, clip in regs:
        text = TABLE_HEAD.sub("", d[p].get_text(clip=clip))
        if clip.height < 34 and len(re.sub(r"[\W\d_]", "", text)) < 3:
            continue
        out.append((d, p, clip))
    return out


def scaled_h(clip):
    return clip.height * min(1.0, USABLE_W / clip.width) + 3


def groups_by_page(regs):
    """Consecutive pieces from the same source page: a figure and its labels stay in one group."""
    groups = []
    for r in regs:
        if groups and groups[-1][-1][0] is r[0] and groups[-1][-1][1] == r[1]:
            groups[-1].append(r)
        else:
            groups.append([r])
    return groups


def place_grouped(lay, groups, start=0):
    """Place groups; a group that fits on one page is never split across an output page break."""
    full = PAGE_H - MARGIN_TOP - MARGIN_BOT
    for g in groups[start:]:
        gh = sum(scaled_h(c) for *_, c in g)
        if gh <= full and lay.room() < gh:
            lay.new_page()
        for d, p, c in g:
            lay.place(d, p, c)


def hhmm(mins):
    return f"{mins // 60} h {mins % 60:02d} min" if mins >= 60 else f"{mins} min"


def compose(sel, side, paper):
    ov = load_overrides()
    doc = pymupdf.open()
    lay = Layout(doc)
    toc, problems = [], []
    total = sum(e["marks"] for e in sel)
    mins = round(total * MIN_PER_MARK / 5) * 5
    lay.new_page()
    if side == "q":
        lay.banner(f"Physics Epoch 3 · {PAPER_NAME[paper]}", [
            f"{len(sel)} questions · {total} marks · {hhmm(mins)}. Answer all questions in one sitting.",
            "Record your finishing time. Report each question as: number, marks out of total, where the marks went.",
        ])
    else:
        lay.banner(f"Physics Epoch 3 · {PAPER_NAME[paper]} · answer scheme", [
            f"{len(sel)} questions · {total} marks · {hhmm(mins)}.",
            *[f"{e['no']}. {e['id']} · {e['topic']} · {e['ref']} [{e['marks']}]" for e in sel]])
    for e in sel:
        src = e["qsrc"] if side == "q" else e["ssrc"]
        school = e["ref"].split()[0]
        if side == "q":
            regs = trim_total(clean(regions_for(src, ov), school, side))
        else:
            regs = drop_slivers(compact(clean(answer_regions(src["pdf"], src["q"]), school, side)))
        groups = groups_by_page(regs)
        first_h = sum(scaled_h(c) for *_, c in groups[0]) if groups else 40
        full = PAGE_H - MARGIN_TOP - MARGIN_BOT
        if len(groups) > 1 and first_h < 120:  # a short opening block stays with the block that follows it
            both = first_h + sum(scaled_h(c) for *_, c in groups[1])
            if both + 50 <= full:
                groups[:2] = [groups[0] + groups[1]]
                first_h = both
        # Keep the header with its first block; never leave a header alone at the foot of a page.
        if lay.room() < (first_h if first_h + 50 <= full else 200) + 50:
            lay.new_page()
        if side == "q":
            lay.item_header(str(e["no"]), e["id"], "", first_h)  # exam style: number and code only
        else:
            lay.item_header(str(e["no"]), f"{e['id']} · {e['topic']} · {e['ref']} [{e['marks']}]", e["why"], first_h)
        toc.append([1, f"{e['no']} · {e['id']}" + ("" if side == "q" else f" · {e['ref']}"), len(doc)])
        if not regs:
            problems.append((e["id"], e["ref"], side))
            lay.note("Source region not found; open the source PDF: " + src["pdf"])
        erratum = ERRATA.get((school, src["q"]), {}).get(side)
        if erratum:
            lay.note(erratum)
        place_grouped(lay, groups)
        lay.gap(12)
    add_footers(doc, f"Physics Epoch 3 {PAPER_NAME[paper]} " + ("questions" if side == "q" else "answer scheme"), 0)
    doc.set_toc(toc)
    return doc, problems


def plan_md(items):
    L = ["# Physics Epoch 3 plan", "",
         "Exam-style papers on the weaker topics, weighted by the Paper 3 analysis (expected Section A marks) and the "
         "readiness page (chapter lowball). Question PDFs show only the number and code; this plan and the answer "
         "schemes carry the topics. Built by `build_epoch3.py`.", ""]
    for paper in (1, 2, 3):
        sel = [e for e in items if e["paper"] == paper]
        total = sum(e["marks"] for e in sel)
        L += [f"## {PAPER_NAME[paper]}: {total} marks, {hhmm(round(total * MIN_PER_MARK / 5) * 5)}", "",
              "| No. | Code | Topic | Question | Marks | Expected in Section A | Lowball | Mark |", "|---|---|---|---|---|---|---|---|"]
        L += [f"| {e['no']} | {e['id']} | {e['topic']} | {e['ref']} | {e['marks']} | "
              f"{'' if e['exp'] is None else format(e['exp'], '.1f')} | {e['low'] * 100:.0f}% | |" for e in sel]
        L.append("")
    return "\n".join(L)


def keep_marks(new, old):
    """Carry recorded marks (the last table cell of each item row) and trailing notes over a rebuild."""
    done = {m[1]: m[2] for m in re.finditer(r"^\| \d+ \| (E3-\d{3}) \|.*\| ([^|]*\S[^|]*) \|$", old, re.M)}
    new = re.sub(r"^(\| \d+ \| (E3-\d{3}) \|.*\|) \|$",
                 lambda m: f"{m[1]} {done[m[2]]} |" if m[2] in done else m[0], new, flags=re.M)
    notes = [ln for ln in old.splitlines() if ln.startswith("Paper ") and " done " in ln]
    return new + ("\n".join(notes) + "\n" if notes else "")


if __name__ == "__main__":
    items = build_plan()
    OUT.mkdir(parents=True, exist_ok=True)
    plan_path = OUT / "Epoch 3 plan.md"
    plan_path.write_text(keep_marks(plan_md(items), plan_path.read_text(encoding="utf-8") if plan_path.exists() else ""),
                         encoding="utf-8")
    for paper in (1, 2, 3):
        sel = [e for e in items if e["paper"] == paper]
        for side, tag in (("q", "Questions"), ("a", "Answer Scheme")):
            doc, prob = compose(sel, side, paper)
            name = f"Epoch 3 Paper {paper} {tag}.pdf"
            doc.save(str(OUT / name), garbage=3, deflate=True)
            print(name, len(doc), "pages; missing regions:", prob)
    for e in items:
        flag = "" if e["stated"] in (None, e["marks"]) else f"  <-- parts sum {e['marks']} but stated total {e['stated']}"
        print(e["id"], e["key"], e["ref"], e["marks"], flag)
