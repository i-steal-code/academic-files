"""Build Physics Epoch 1: a short weakness pack from unseen 2026 prelim P2 questions.

Same architecture as the math epochs (tools/_epoch_lib.py and tools/_epoch_compose.py): source questions and
answers are cropped from the prelim PDFs and composed into a Questions PDF, an Answer Scheme PDF and a plan.

Priority comes from the readiness page: score = (4 - all-marks rating) x chapter weight, read live from
work/physics-readiness.html, so a rebuild follows the page. Weaknesses are chapters rated 2 or below, plus the
user's flagged weak links (superposition, nuclear, currents) and thin thermo understanding.

Pass 1 takes one question per weakness, in priority order. Pass 2 is a second question, if time allows.
Only unseen 2026 P2 sets are used, so the P3 papers stay whole for P3 practice.

Run:  .venv-convert/Scripts/python.exe -I "raw files/H2 physics/topical/build_epoch1.py"
"""
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT / "tools"))

import pymupdf  # noqa: E402
from _epoch_compose import Layout, add_footers, regions_for  # noqa: E402
from _epoch_lib import load_overrides, open_doc, question_starts, next_start  # noqa: E402

PHYS = "raw files/H2 physics"
OUT = ROOT / PHYS / "topical" / "Epoch 1"
READINESS = ROOT / PHYS / "work" / "physics-readiness.html"
QP = PHYS + "/exam papers/prelim QP/2026 {s} P2 prelim H2 physics.pdf"
ANS = PHYS + "/exam papers/prelim ANS/2026 {s} P2 prelim H2 physics.pdf"
MIN_PER_MARK = 1.6  # P2 rate: 120 min / 75 marks

FLAGGED = {11: "user-flagged weak link", 15: "user-flagged weak link", 20: "user-flagged weak link",
           13: "thin base understanding (user)"}

# chapter -> [(school, q, what it tests)]; first is Pass 1, second is Pass 2
PICKS = {
    16: [("YIJC", 5, "Capacitor discharging through a resistor. C and R from graph gradients (start from Q = CV); τ = RC; why the decay is exponential."),
         ("NJC", 6, "Uniform wire and NTC thermistor. Thermistor: n rises with T; write explanations as working.")],
    8: [("JPJC", 2, "Gravitational potential and the Earth. Potential is per unit mass, from infinity; ΔU = GMm(1/r₁ − 1/r₂)."),
        ("TJC", 4, "Binary stars of equal mass. Unseen set-up: draw it first; gravity uses the separation, the orbit uses the radius.")],
    18: [("TMJC", 6, "Flux definition and a circular coil. Flux linkage is NΦ; ε is the gradient of the NΦ–t graph."),
         ("SAJC", 6, "Small coil in a non-uniform field. Sketch NΦ–t first, then ε–t; Lenz for the direction.")],
    19: [("CJC", 6, "Electron in a one-dimensional box, |ψ|². L = nλ/2 → p = h/λ → E = p²/2m; |ψ|² is probability per unit length."),
         ("JPJC", 6, "Photon and threshold frequency. Photon: a quantum of EM radiation; threshold explained by one photon per electron.")],
    11: [("NJC", 5, "Microwave oven with a reflective casing. Reflection → stationary wave; nodes λ/2 apart (the Ch 11 (c) miss)."),
         ("JPJC", 4, "Double slit. Conditions for visible fringes; count both sides and the zero order.")],
    10: [("ASRJC", 4, "Longitudinal sound waves. Compression centres from the displacement graph; I ∝ A².")],
    20: [("NJC", 7, "U-235 fission with masses in u. Δm → kg → E = Δmc² in J → ÷ 1.60 × 10⁻¹⁹ → MeV."),
         ("DHS", 6, "Nuclear binding energy, strontium-90. Definition: energy to separate the nucleus completely into nucleons.")],
    13: [("ASRJC", 3, "First law with the direction of each energy change. ΔU = q + w signs; ΔU = (3/2)nRΔT.")],
    15: [("JPJC", 5, "r.m.s. by heating effect, then a square-wave current. r.m.s. is the root of the mean of I²; I₀ = √2 I_rms only for a sinusoid.")],
}


def chapters():
    """Chapter data from the readiness page: number, title, weight, all-marks rating."""
    txt = READINESS.read_text(encoding="utf-8")
    out = {}
    for line in txt.splitlines():
        m = re.search(r'\{ ch: (\d+),\s*t: "([^"]+)",.*?w: ([\d.]+),.*?sheet: (\d)', line)
        if not m:
            continue
        ch, title, w, sheet = int(m[1]), m[2], float(m[3]), int(m[4])
        tc = re.search(r"tc: (\d)", line)
        allr = re.search(r"all: (\d)", line)
        rating = int(allr[1]) if allr else int(tc[1]) if tc else sheet
        out[ch] = {"ch": ch, "title": title, "w": w, "rating": rating, "score": (4 - rating) * w}
    return out


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
    return sum(int(m) for m in re.findall(r"\[(\d{1,2})\]", txt))


def build_plan():
    chs = chapters()
    order = sorted(PICKS, key=lambda c: (-chs[c]["score"], c))
    items = []
    for pas in (0, 1):
        for c in order:
            if pas < len(PICKS[c]):
                s, q, why = PICKS[c][pas]
                mk = marks_of(s, q)
                items.append({
                    "pass": pas + 1, "ch": c, "topic": chs[c]["title"], "rating": chs[c]["rating"],
                    "score": chs[c]["score"], "flag": FLAGGED.get(c, ""), "ref": f"{s} 2026 P2 Q{q}",
                    "marks": mk, "mins": round(mk * MIN_PER_MARK), "why": why,
                    "qsrc": {"pdf": QP.format(s=s), "q": q}, "ssrc": {"pdf": ANS.format(s=s), "q": q},
                })
    for i, e in enumerate(items, 1):
        e["id"] = f"P1-{i:02d}"
    return order, chs, items


def compose(items, side, order, chs):
    ov = load_overrides()
    doc = pymupdf.open()
    lay = Layout(doc)
    toc, problems, last = [], [], None
    lay.new_page()
    p1 = [e for e in items if e["pass"] == 1]
    p2 = [e for e in items if e["pass"] == 2]
    lay.banner("Physics Epoch 1: weakness pack before P2" + (" (answer scheme)" if side == "a" else ""), [
        "Unseen 2026 prelim P2 questions only, so the P3 papers stay whole. Priority from the readiness page: "
        "(4 − all-marks rating) × chapter weight. Pass 1 is one question per weakness; Pass 2 is a second one if time allows.",
        f"Pass 1: {len(p1)} questions, {sum(e['marks'] for e in p1)} marks, about {sum(e['mins'] for e in p1)} min. "
        f"Pass 2: {len(p2)} questions, {sum(e['marks'] for e in p2)} marks, about {sum(e['mins'] for e in p2)} min. "
        f"Time each at {MIN_PER_MARK} min per mark; the 2-minute stall rule applies.",
        "Report each as: chapter, question, marks out of total, marks lost to skill leaks.",
    ])
    lay.banner("Priority order", [
        f"{i}. Ch {c} {chs[c]['title']}: rating {chs[c]['rating']}, weight {chs[c]['w']}, score {chs[c]['score']:.1f}"
        + (f" ({FLAGGED[c]})" if c in FLAGGED else "")
        for i, c in enumerate(order, 1)
    ], fill=(0.95, 0.95, 0.90))
    for e in items:
        block = "Pass 1: one question per weakness" if e["pass"] == 1 else "Pass 2: second question, if time"
        if block != last:
            last = block
            lay.new_page()
            toc.append([1, block, len(doc)])
            lay.banner(block, [", ".join(f"{x['id']} {x['ref']}" for x in items if x["pass"] == e["pass"])])
        src = e["qsrc"] if side == "q" else e["ssrc"]
        regs = regions_for(src, ov)
        first_h = regs[0][2].height * min(1.0, 527 / regs[0][2].width) if regs else 40
        lay.item_header(e["id"], f"Ch {e['ch']} {e['topic']} · {e['ref']} [{e['marks']}] · {e['mins']} min",
                        e["why"] if side == "a" else "", first_h)  # method note: answer scheme only (user, 13 Nov)
        toc.append([2, f"{e['id']} Ch {e['ch']} · {e['ref']}", len(doc)])
        if not regs:
            problems.append((e["id"], e["ref"], side))
            lay.note("Source region not found; open the source PDF: " + src["pdf"])
        for d, p, clip in regs:
            lay.place(d, p, clip)
        lay.gap(12)
    add_footers(doc, "Physics Epoch 1 " + ("questions" if side == "q" else "answer scheme"), 0)
    doc.set_toc([[1, "Contents", 1]] + toc)
    return doc, problems


def plan_md(order, chs, items):
    lines = ["# Physics Epoch 1 plan", "",
             "Weakness pack before P2 (Fri 13 Nov). Unseen 2026 prelim P2 questions only; P3 papers stay whole. "
             "Priority from the readiness page: (4 − all-marks rating) × chapter weight. "
             "Built by `build_epoch1.py` on the math epoch library.", "",
             "| # | Chapter | Rating | Weight | Score | Note |", "|---|---|---|---|---|---|"]
    for i, c in enumerate(order, 1):
        x = chs[c]
        lines.append(f"| {i} | Ch {c} {x['title']} | {x['rating']} | {x['w']} | {x['score']:.1f} | {FLAGGED.get(c, '')} |")
    for pas, name in ((1, "Pass 1: one question per weakness"), (2, "Pass 2: second question, if time")):
        sel = [e for e in items if e["pass"] == pas]
        lines += ["", f"## {name}", "",
                  f"{len(sel)} questions, {sum(e['marks'] for e in sel)} marks, about {sum(e['mins'] for e in sel)} min.", "",
                  "| ID | Chapter | Question | Marks | Min | Tests | Done |", "|---|---|---|---|---|---|---|"]
        for e in sel:
            lines.append(f"| {e['id']} | Ch {e['ch']} | {e['ref']} | {e['marks']} | {e['mins']} | {e['why']} | |")
    lines += ["", "Report each as: chapter, question, marks out of total, marks lost to skill leaks. "
              "Results go into `TOPICAL` on the readiness page.", ""]
    return "\n".join(lines)


if __name__ == "__main__":
    order, chs, items = build_plan()
    OUT.mkdir(parents=True, exist_ok=True)
    (OUT / "Epoch 1 plan.md").write_text(plan_md(order, chs, items), encoding="utf-8")
    for side, name in (("q", "Epoch 1 Questions.pdf"), ("a", "Epoch 1 Answer Scheme.pdf")):
        doc, prob = compose(items, side, order, chs)
        doc.save(str(OUT / name), garbage=3, deflate=True)
        print(name, len(doc), "pages; missing regions:", prob)
    for e in items:
        print(e["id"], e["pass"], f"Ch {e['ch']}", e["ref"], e["marks"], e["mins"])
