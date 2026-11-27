"""Build Physics Epoch 2 (v2): P3 prep in two blocks, from the Paper 3 analysis and the readiness page.

Block 1 is a 2-hour question marathon of Section A questions: one standard question for every topic the analysis
gives about a 1-in-3 or better chance of a whole Section A question (its effort rule, step 1: "floor first").
Block 2 is Section B practice in 30-minute chunks: nuclear and oscillations to full depth plus one electricity area
(effort rule, step 3), then further options by marks at risk.

Inputs, read live:
- h2-physics-paper3-analysis-2026/topics.csv: expected Section A marks and the chance a topic leads a Section B option.
- work/physics-readiness.html: each chapter's lowball (evaluated with node), so topical and taper evidence counts.

Scores:
- Block 1 order: expected Section A marks x (1 - lowball): Section A marks at risk.
- Block 2 order after the core three: chance it leads an option x 20 x (1 - lowball).

Source: unseen 2026 prelim P3 questions. Seen sets (NYJC, ACJC, RVHS, RI) and MI (a 9749-format paper, which the
analysis leaves out) are excluded. RESERVED sets stay whole for timed P3 runs.

Run:  .venv-convert/Scripts/python.exe -I "raw files/H2 physics/topical/build_epoch2.py" [--block 2]
"""
import csv
import json
import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT / "tools"))
sys.stdout.reconfigure(encoding="utf-8")

import pymupdf  # noqa: E402
from _epoch_compose import Layout, add_footers, regions_for  # noqa: E402
from _epoch_lib import load_overrides, open_doc, question_starts, next_start  # noqa: E402

PHYS = "raw files/H2 physics"
OUT = ROOT / PHYS / "topical" / "Epoch 2"
READINESS = ROOT / PHYS / "work" / "physics-readiness.html"
TOPICS = ROOT / PHYS / "h2-physics-paper3-analysis-2026" / "topics.csv"
QP = PHYS + "/exam papers/prelim QP/2026 {s} P3 prelim H2 physics.pdf"
ANS = PHYS + "/exam papers/prelim ANS/2026 {s} P3 prelim H2 physics.pdf"
MIN_PER_MARK = 1.6  # P3 rate: 120 min / 75 marks
CHUNK_MIN = 30      # Block 2: one Section B option per chunk

SEEN = {"NYJC", "ACJC", "RVHS", "RI"}
EXCLUDED = {"MI"}                 # 9749-format paper, left out by the analysis
RESERVED = {"HCI", "EJC", "NJC"}  # whole unseen P3s for timed runs

# Analysis topic code -> (chapter whose lowball stands for it, label)
TOPIC = {
    "CIRCUITS": (16, "D.c. circuits, capacitors and RC"),
    "OSC": (9, "Oscillations"),
    "GRAV": (8, "Gravitational fields"),
    "NUCL": (20, "Nuclear physics"),
    "EMFOR": (17, "EM forces: charged particles in E and B"),
    "EFLD": (14, "Electric fields and capacitance"),
    "CURR": (15, "Currents and a.c."),
    "MECH": (2, "General mechanics: forces and moments"),
}
MECH_EXPECTED = 7.0  # the analysis gives "about 7 (5-9)" for the one general mechanics question

# Block 1: (topic, school, question, what it tests, analysis question types it hits)
BLOCK1 = [
    ("CIRCUITS", "TJC", 6, "Q = CV and ½CV², then recharging a flashgun capacitor: tangent and τ from the V–t curve.", "CCT-T20, T19; ELF-T19"),
    ("CIRCUITS", "SAJC", 6, "Terminal p.d. below the e.m.f., then four capacitors with a supply and a flash-tube: combine first.", "CCT-T09, T17, T18"),
    ("GRAV", "YIJC", 3, "φ–r sketch, why φ is negative, planet mass from the φ graph, then rotation.", "GRV-T08, T07, T16"),
    ("EFLD", "DHS", 5, "V–x graph of two charges: signs from its shape, E from the gradient, electron launched (energy).", "ELF-T09, T08"),
    ("NUCL", "VJC", 7, "Random vs spontaneous; energy released from BE per nucleon; activity from power.", "NUC-T06, T21, T10"),
    ("EMFOR", "YIJC", 6, "Electron in B (r = mv/Bq), add E to pass undeflected (v = E/B), then a positron.", "EMF-T14, T20, T12"),
    ("CURR", "VJC", 6, "Transformer de-icer: mean power, r.m.s. current, P–t and charge–t sketches.", "CUR-T14, T11"),
    ("MECH", "JPJC", 3, "Hinged uniform bar at 30°: moments about the hinge, then the hinge force by resolving.", "FOR-T11"),
    ("OSC", "ASRJC", 4, "Ball on a curved track: show s.h.m. from a = (g/r)x, half-period from r, then damping.", "OSC-T03, T04, T18"),
]
# Block 2: (topic, school, question, what it tests). The first CORE items follow the effort rule, the rest go by score.
BLOCK2_CORE = [
    ("NUCL", "JPJC", 9, "α-decay recoil: momentum equation, V/v ratio, Q-value from masses in u."),
    ("OSC", "DHS", 7, "Mass on a spring: define s.h.m., velocity from the x–t graph, a and v directions, energy (21 marks)."),
    ("EMFOR", "TMJC", 8, "Mass spectrometer: velocity selector (why undeflected, which plate is higher, v = E/B), then r = mv/Bq."),
]
BLOCK2_MORE = [
    ("CIRCUITS", "TMJC", 7, "Potential along a uniform wire, R from ρ, D, L and m; NTC thermistor; charging a 2.0 F capacitor (sketch and time)."),
    ("GRAV", "CJC", 8, "Why the Moon doesn't fall in; weight at pole vs equator; Earth–Moon distance and the null point."),
    ("NUCL", "YIJC", 9, "Nuclear density and what it says about the atom; fission; energy released from BE per nucleon."),
    ("EFLD", "JPJC", 8, "Field of force, V–x of two spheres, electron approaching; capacitor in a flash circuit."),
    ("OSC", "SAJC", 8, "Define s.h.m.; the tide as s.h.m. (earliest time a tanker clears); then a wire in a magnetic field."),
]


def readiness():
    """Evaluate the readiness page's model with node; return {ch: {w, low, ...}}."""
    html = READINESS.read_text(encoding="utf-8")
    js = re.findall(r"<script>(.*?)</script>", html, re.S)[-1]
    stub = ("const els={};const document={getElementById:id=>(els[id]??={textContent:'',innerHTML:'',"
            "setAttribute(){},addEventListener(){},querySelectorAll(){return []}}),querySelectorAll(){return []},"
            "addEventListener(){}};const window={addEventListener(){}};")
    tail = "\nconsole.log(JSON.stringify(CH.map(c=>({ch:c.ch,t:c.t,w:c.w,low:lowFrac(c)}))));"
    r = subprocess.run(["node"], input=stub + js + tail, capture_output=True, text=True, encoding="utf-8", check=True)  # stdin: the script is too long for a Windows command line
    return {c["ch"]: c for c in json.loads(r.stdout.strip().splitlines()[-1])}


def analysis():
    """topics.csv -> {code: (expected Section A marks, chance it leads a Section B option)}."""
    out = {}
    with open(TOPICS, encoding="utf-8") as f:
        for row in csv.DictReader(f):
            exp = float(row["exp_marks_central"]) if row["exp_marks_central"] else MECH_EXPECTED
            pb = float(row["p_leads_section_b"]) if row["p_leads_section_b"] else 0.175
            out[row["code"]] = (exp, pb)
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
    rd, an = readiness(), analysis()
    risk_a = {k: an[k][0] * (1 - rd[ch]["low"]) for k, (ch, _) in TOPIC.items()}
    risk_b = {k: an[k][1] * 20 * (1 - rd[ch]["low"]) for k, (ch, _) in TOPIC.items()}

    def item(block, k, s, q, why, types=""):
        assert s not in SEEN | EXCLUDED | RESERVED, f"{s} is seen, excluded or reserved"
        mk = marks_of(s, q)
        ch, name = TOPIC[k]
        return {"block": block, "key": k, "ch": ch, "topic": name, "ref": f"{s} 2026 P3 Q{q}", "marks": mk,
                "mins": round(mk * MIN_PER_MARK) if block == 1 else CHUNK_MIN, "why": why, "types": types,
                "qsrc": {"pdf": QP.format(s=s), "q": q}, "ssrc": {"pdf": ANS.format(s=s), "q": q}}

    b1 = sorted(BLOCK1, key=lambda x: -risk_a[x[0]])
    b2_more = sorted(BLOCK2_MORE, key=lambda x: -risk_b[x[0]])
    items = [item(1, *x) for x in b1]
    items += [dict(item(2, *x), core=True) for x in BLOCK2_CORE]
    items += [dict(item(2, *x), core=False) for x in b2_more]
    clock = 0
    for i, e in enumerate(items, 1):
        e["id"] = f"E2-{i:02d}"
        if e["block"] == 1:
            clock += e["mins"]
            e["by"] = f"{clock // 60}:{clock % 60:02d}"
    return rd, an, risk_a, risk_b, items


def fmt_low(rd, k):
    return f"{rd[TOPIC[k][0]]['low'] * 100:.0f}%"


def compose(items, side, rd, an, risk_a, risk_b):
    ov = load_overrides()
    doc = pymupdf.open()
    lay = Layout(doc)
    toc, problems = [], []
    b1 = [e for e in items if e["block"] == 1]
    b2 = [e for e in items if e["block"] == 2]
    lay.new_page()
    lay.banner("Physics Epoch 2: P3 prep from the Paper 3 analysis" + (" (answer scheme)" if side == "a" else ""), [
        "Built from the Paper 3 analysis (13 Nov) and your readiness page. Unseen 2026 prelim P3 questions only; "
        "HCI, EJC and NJC P3 are kept whole for timed runs.",
        *([f"Block 1, question marathon: {len(b1)} Section A questions, {sum(e['marks'] for e in b1)} marks, "
            f"about {sum(e['mins'] for e in b1)} min in one sitting. One question for every topic with about a "
            "1-in-3 or better chance of a whole Section A question."] if b1 else []),
        f"Block 2, Section B: {len(b2)} options of about 20 marks, {CHUNK_MIN} min each. The first three are the core "
        "(nuclear, oscillations, charged particles in E and B); do the rest by order as time allows.",
        "Report each as: question, marks out of total, marks lost to skill leaks.",
    ])
    if b1:
        lay.banner("Block 1 order: Section A marks at risk = expected marks × (1 − your lowball)", [
            f"{e['topic']}: expected {an[e['key']][0]:.1f} of 55, lowball {fmt_low(rd, e['key'])}, at risk "
            f"{risk_a[e['key']]:.1f}" for e in b1], fill=(0.95, 0.95, 0.90))
    lay.banner("Block 2 order after the core: chance it leads an option × 20 × (1 − your lowball)", [
        f"{'Core' if e['core'] else 'Next'}: {e['topic']} (leads an option {an[e['key']][1] * 100:.0f}%, "
        f"at risk {risk_b[e['key']]:.1f})" for e in b2], fill=(0.95, 0.95, 0.90))
    for block, sel, title in ((1, b1, "Block 1: 2-hour question marathon"),
                              (2, b2, f"Block 2: Section B in {CHUNK_MIN}-minute chunks")):
        if not sel:
            continue
        lay.new_page()
        toc.append([1, title, len(doc)])
        note = ("One sitting, no breaks. The clock column is when you should be done with each question; "
                "if you are more than 10 min behind, skip to the next question." if block == 1 else
                f"One option per chunk, {CHUNK_MIN} min hard stop. Read the whole option first (2 min), then write.")
        lay.banner(title, [note, ", ".join(f"{x['id']} {x['ref']}" for x in sel)])
        for e in sel:
            src = e["qsrc"] if side == "q" else e["ssrc"]
            regs = regions_for(src, ov)
            first_h = regs[0][2].height * min(1.0, 527 / regs[0][2].width) if regs else 40
            when = f"done by {e['by']}" if block == 1 else ("core" if e["core"] else "next")
            lay.item_header(e["id"], f"{e['topic']} · {e['ref']} [{e['marks']}] · {e['mins']} min · {when}",
                            # The method note is a spoiler: answer scheme only (user, 13 Nov).
                            (e["why"] + (f" ({e['types']})" if e["types"] else "")) if side == "a" else "", first_h)
            toc.append([2, f"{e['id']} {e['topic']} · {e['ref']}", len(doc)])
            if not regs:
                problems.append((e["id"], e["ref"], side))
                lay.note("Source region not found; open the source PDF: " + src["pdf"])
            for d, p, clip in regs:
                lay.place(d, p, clip)
            lay.gap(12)
    add_footers(doc, "Physics Epoch 2 " + ("questions" if side == "q" else "answer scheme"), 0)
    doc.set_toc([[1, "Contents", 1]] + toc)
    return doc, problems


def plan_md(items, rd, an, risk_a, risk_b):
    b1 = [e for e in items if e["block"] == 1]
    b2 = [e for e in items if e["block"] == 2]
    L = ["# Physics Epoch 2 plan (v2)", "",
         "P3 prep (Tue 17 Nov, 2 pm), rebuilt from the Paper 3 analysis "
         "(`h2-physics-paper3-analysis-2026/`) and the readiness page. Unseen 2026 prelim P3 questions; HCI, EJC and "
         "NJC P3 kept whole; MI left out (9749 format). Built by `build_epoch2.py`.", "",
         f"## Block 1: 2-hour question marathon ({sum(e['marks'] for e in b1)} marks, about "
         f"{sum(e['mins'] for e in b1)} min)", "",
         "One sitting. Order = Section A marks at risk (expected marks × (1 − lowball)).", "",
         "| ID | Topic | Question | Marks | Done by | Tests | Types | Mark |", "|---|---|---|---|---|---|---|---|"]
    L += [f"| {e['id']} | {e['topic']} | {e['ref']} | {e['marks']} | {e['by']} | {e['why']} | {e['types']} | |" for e in b1]
    L += ["", f"## Block 2: Section B, {CHUNK_MIN}-minute chunks", "",
          "Core first (effort rule: nuclear and oscillations to full depth plus one electricity area), then by "
          "chance it leads an option × 20 × (1 − lowball).", "",
          "| ID | Core | Topic | Question | Marks | Tests | Mark |", "|---|---|---|---|---|---|---|"]
    L += [f"| {e['id']} | {'yes' if e['core'] else ''} | {e['topic']} | {e['ref']} | {e['marks']} | {e['why']} | |" for e in b2]
    L += ["", "## Scores", "", "| Topic | Lowball | Expected Section A marks | At risk (A) | Leads option | At risk (B) |",
          "|---|---|---|---|---|---|"]
    L += [f"| {name} | {fmt_low(rd, k)} | {an[k][0]:.1f} | {risk_a[k]:.2f} | {an[k][1] * 100:.0f}% | {risk_b[k]:.2f} |"
          for k, (ch, name) in sorted(TOPIC.items(), key=lambda kv: -risk_a[kv[0]])]
    L += ["", "Report each as: question, marks out of total, marks lost to skill leaks. Results go into `TOPICAL` on "
          "the readiness page.", ""]
    return "\n".join(L)


def keep_marks(new, old):
    """Carry recorded marks (the last table cell of each item row) and trailing notes over a rebuild."""
    done = {m[1]: m[2] for m in re.finditer(r"^\| (E2-\d\d) \|.*\| ([^|]*\S[^|]*) \|$", old, re.M)}
    new = re.sub(r"^(\| (E2-\d\d) \|.*\|) \|$", lambda m: f"{m[1]} {done[m[2]]} |" if m[2] in done else m[0], new, flags=re.M)
    notes = [ln for ln in old.splitlines() if ln.startswith(("Block 1 done", "Block 2 done"))]
    return new + ("\n" + "\n".join(notes) + "\n" if notes else "")


if __name__ == "__main__":
    # --block 2 writes that block alone to its own PDFs and leaves the plan and the full PDFs untouched.
    only = int(sys.argv[sys.argv.index("--block") + 1]) if "--block" in sys.argv else None
    rd, an, risk_a, risk_b, items = build_plan()
    OUT.mkdir(parents=True, exist_ok=True)
    if only is None:
        plan_path = OUT / "Epoch 2 plan.md"
        plan_path.write_text(keep_marks(plan_md(items, rd, an, risk_a, risk_b),
                                        plan_path.read_text(encoding="utf-8") if plan_path.exists() else ""), encoding="utf-8")
    sel = [e for e in items if only is None or e["block"] == only]
    tag = f"Epoch 2 Block {only}" if only else "Epoch 2"
    for side, name in (("q", f"{tag} Questions.pdf"), ("a", f"{tag} Answer Scheme.pdf")):
        doc, prob = compose(sel, side, rd, an, risk_a, risk_b)
        doc.save(str(OUT / name), garbage=3, deflate=True)
        print(name, len(doc), "pages; missing regions:", prob)
    for k, (ch, name) in sorted(TOPIC.items(), key=lambda kv: -risk_a[kv[0]]):
        print(f"{name}: low {fmt_low(rd, k)}, A {an[k][0]:.1f} -> {risk_a[k]:.2f}, B {an[k][1]:.2f} -> {risk_b[k]:.2f}")
    for e in items:
        print(e["id"], e["block"], e["topic"], e["ref"], e["marks"], e["mins"], e.get("by", ""), e.get("core", ""))
