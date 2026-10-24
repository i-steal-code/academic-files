"""Build the Epoch 1 topical plan (from the readiness ratings) and its question / answer PDFs."""
import glob
import html
import json
import re
import sys
from pathlib import Path

from _epoch_lib import RAW, ROOT, WORK, auto_regions, has_text, load_overrides, region_key

CANVAS_DATA = Path.home() / ".cursor/projects/c-Users-debig-OneDrive-Desktop-github-repository-academic-files/canvases/math-readiness.canvas.data.json"
REGEN_DIR = ROOT / "converted packages/H2 math/topical/Regenerated solutions"

TOPIC_IDS = {
    "fnd": "Foundations", "vec": "Vectors", "eqn": "Equations and Inequalities", "fun": "Functions",
    "cpx": "Complex Numbers", "dif": "Differentiation Techniques", "aod": "Applications of Differentiation",
    "seq": "Sequences and Series", "mac": "Maclaurin and Binomial Series", "gra": "Graphs and Transformations",
    "int": "Integration Techniques", "aoi": "Applications of Integration", "de": "Differential Equations",
    "pnc": "Permutations and Combinations", "prb": "Probability", "drv": "Discrete Random Variables",
    "bin": "Binomial Distribution", "nor": "Normal Distribution", "sam": "Sampling and Estimation",
    "hyp": "Hypothesis Testing", "reg": "Correlation and Linear Regression",
}

BLOCKS = [
    ("Differentiation base", ["dif", "aod", "mac"]),
    ("Graphs", ["gra"]),
    ("Vectors", ["vec"]),
    ("Statistics I: normal, sampling, testing, regression", ["nor", "sam", "hyp", "reg"]),
    ("Integration chain", ["int", "aoi", "de"]),
    ("Sequences and series", ["seq"]),
    ("Statistics II: counting and distributions", ["pnc", "prb", "drv", "bin"]),
    ("Algebra: complex numbers, functions, equations", ["cpx", "fun", "eqn", "fnd"]),
]

CONFIRM_N = 3
FIXED_SWAPS = {
    ("Graphs and Transformations", 11): {"ref": "C8B Lect Notes · Example 4", "note": "Revision Order cites C7A Example 4, which is a sequences example; the curve-transformation example C8B Example 4 is used instead."},
}
SKIP_NOTES = {}


def load_ratings():
    return json.loads(CANVAS_DATA.read_text(encoding="utf-8"))["ratings"]


def load_core():
    ro = json.loads((WORK / "revision_order_topical.json").read_text(encoding="utf-8"))
    ex = {}
    for f in glob.glob(str(WORK / "topical_extract_G*.json")):
        for e in json.loads(Path(f).read_text(encoding="utf-8")):
            ex[(e["topic"], e["tier"], int(e["n"]))] = e
    for i in ro:
        i["extract"] = ex.get((i["topic"], i["tier"], i["n"]), {})
    return ro


def load_picks():
    picks = []
    for f in sorted(glob.glob(str(WORK / "epoch1_picks_X*.json"))):
        picks += json.loads(Path(f).read_text(encoding="utf-8"))
    return picks


def raw_rel(p: Path) -> str:
    return str(p.relative_to(ROOT)).replace("\\", "/")


QP_FROM_ANS = {"A-Level 2024 P1 Q11"}


def sources_for(ref: str):
    """(question source, solution source); each {'pdf', 'q'} or None."""
    m = re.match(r"A-Level (\d{4}) P(\d) Q(\d+)", ref)
    if m:
        y, p, q = m.groups()
        name = f"{y} P{p} A-level H2 math.pdf"
        s = {"pdf": raw_rel(RAW / "TYS ANS" / name), "q": int(q)}
        if ref in QP_FROM_ANS:
            return {**s, "manual": True, "qside": True}, s
        return {"pdf": raw_rel(RAW / "TYS QP" / name), "q": int(q)}, s
    m = re.match(r"RI Mock (\d{4}) P(\d) Q(\d+)", ref)
    if m:
        y, p, q = m.groups()
        s = {"pdf": raw_rel(RAW / "misc" / f"{y} RI P{p} mock Solns H2 math.pdf"), "q": int(q)}
        return ({**s, "manual": True, "qside": True}, s)
    m = re.match(r"([A-Z]+) Prelim (\d{4}) P(\d) Q(\d+)", ref)
    if m:
        sch, y, p, q = m.groups()
        name = f"{y} {sch} P{p} prelim H2 math.pdf"
        qp, ans = RAW / "prelim QP" / name, RAW / "prelim ANS" / name
        s = {"pdf": raw_rel(ans), "q": int(q)} if ans.exists() else None
        if qp.exists():
            qs = {"pdf": raw_rel(qp), "q": int(q)}
        elif s:
            qs = {**s, "manual": True, "qside": True}
        else:
            qs = None
        return qs, s
    m = re.match(r"(C\w+) Add Prac · Q(\d+)", ref)
    if m:
        ch, q = m.groups()
        base = RAW / "topical" / "Add Prac"
        qp, sp = base / f"{ch} Add Prac Qns.pdf", base / f"{ch} Add Prac Solns.pdf"
        return ({"pdf": raw_rel(qp), "q": int(q)} if qp.exists() else None,
                {"pdf": raw_rel(sp), "q": int(q)} if sp.exists() else None)
    m = re.match(r"(C\w+) Lect(?:ure)? Notes · (.+)", ref)
    if m:
        ch, ex = m.groups()
        sub = "statistics" if ch.startswith("CS") else "pure"
        pdf = RAW / "base syllabus" / sub / f"{ch} Lecture Notes.pdf"
        tag = re.sub(r"\s*lecture notes?$", "", ex, flags=re.I).strip()
        if tag.startswith("Section 3"):
            tag = "Section 3"
        s = {"pdf": raw_rel(pdf), "q": tag, "manual": True}
        prompt = OUT_DIR / "prompts" / f"{ch} Lecture Notes {tag}.md"
        return ({"regen": raw_rel(prompt)} if prompt.exists() else {**s, "qside": True}), dict(s)
    m = re.match(r"(Zeta|Lambda|Delta) Q(\d+) · (.+)", ref)
    if m:
        return None, None
    return None, None


def t3_sources(item):
    e = item.get("extract") or {}
    qpath, spath = e.get("questionPath"), e.get("solutionPath")
    if not qpath:
        return None, None
    def pkg(p):
        p = Path(p)
        return p.parent.parent.name if p.parent.name == "pages" else p.parent.name

    stem = pkg(qpath)
    sstem = pkg(spath) if spath else stem.replace("Qns", "Solns")
    q = int(re.match(r"\w+ Q(\d+)", item["ref"]).group(1))
    base = RAW / "topical" / "T3 SR set"
    return ({"pdf": raw_rel(base / f"{stem}.pdf"), "q": q}, {"pdf": raw_rel(base / f"{sstem}.pdf"), "q": q})


def regen_source(ref: str):
    f = REGEN_DIR / f"{ref}.md"
    return {"regen": raw_rel(f)} if f.exists() else None


def build_plan():
    ratings = load_ratings()
    core = load_core()
    picks = load_picks()
    subs = {re.sub(r"\s*\[.*$", "", p["replaces"]).strip(): p for p in picks if p.get("role") == "substitute" and p.get("replaces")}
    extras = {}
    for p in picks:
        if p.get("role") == "extra":
            extras.setdefault(p["topic"], []).append(p)

    plan = []
    for bname, tids in BLOCKS:
        for tid in tids:
            topic = TOPIC_IDS[tid]
            level = ratings.get(tid, 0)
            mode = "full" if level <= 2 else "confirm"
            items = [i for i in core if i["topic"] == topic and i["tier"] == "core"]
            if mode == "confirm":
                items = items[:CONFIRM_N]
            entries = []
            for p in sorted(extras.get(topic, []), key=lambda x: x.get("order", 99)) if mode == "full" else []:
                entries.append({"kind": "extra", "ref": p["ref"], "marks": p.get("marks"), "stem": p.get("stem", ""),
                                "parts": p.get("parts", "all"), "why": p.get("why", ""),
                                "qsrc": {"pdf": p["qPdf"], "q": p["qNumber"], "pages": p.get("qPages")},
                                "ssrc": {"pdf": p["sPdf"], "q": p.get("sNumber", p["qNumber"]), "pages": p.get("sPages")}})
            for i in items:
                ref, note = i["ref"], ""
                swap = FIXED_SWAPS.get((topic, i["n"]))
                if swap:
                    ref, note = swap["ref"], swap["note"]
                sub = subs.get(i["ref"])
                ex = i.get("extract") or {}
                needs_sub = sub is not None
                if needs_sub:
                    entries.append({"kind": "substitute", "ref": sub["ref"], "marks": sub.get("marks"),
                                    "stem": sub.get("stem", ""), "parts": sub.get("parts", "all"),
                                    "why": sub.get("why", ""), "replaces": i["ref"], "coreN": i["n"],
                                    "qsrc": {"pdf": sub["qPdf"], "q": sub["qNumber"], "pages": sub.get("qPages")},
                                    "ssrc": {"pdf": sub["sPdf"], "q": sub.get("sNumber", sub["qNumber"]), "pages": sub.get("sPages")}})
                    continue
                if ref.startswith(("Zeta", "Lambda", "Delta")):
                    qs, ss = t3_sources(i)
                else:
                    qs, ss = sources_for(ref)
                if ss is None or not i.get("hasSoln", True):
                    ss = regen_source(i["ref"]) or ss
                if qs is None and ss is None:
                    continue
                ref = re.sub(r"(Section \d+):.*", r"\1", ref)
                ref = re.sub(r"\s+lecture notes$", "", ref)
                entries.append({"kind": "core", "ref": ref, "coreN": i["n"], "marks": i.get("marks", ""),
                                "stem": ex.get("stem", ""), "skip": "", "note": "; ".join(filter(None, [note] + (i.get("notes") or []))),
                                "status": ex.get("status", ""), "qsrc": qs, "ssrc": ss})
            plan.append({"block": bname, "tid": tid, "topic": topic, "level": level, "mode": mode, "items": entries})
    return plan


def region_report(plan):
    ov = load_overrides()
    rows = []
    for t in plan:
        for e in t["items"]:
            for side in ("qsrc", "ssrc"):
                src = e.get(side)
                if not src:
                    rows.append((t["topic"], e["ref"], side, "NO SOURCE", ""))
                    continue
                if "regen" in src:
                    rows.append((t["topic"], e["ref"], side, "regen", src["regen"]))
                    continue
                key = region_key(src["pdf"], src["q"])
                if key in ov:
                    rows.append((t["topic"], e["ref"], side, "override", key))
                    continue
                if src.get("manual") or not (ROOT / src["pdf"]).exists():
                    rows.append((t["topic"], e["ref"], side, "MANUAL" if (ROOT / src["pdf"]).exists() else "MISSING PDF", key))
                    continue
                r = auto_regions(src["pdf"], src["q"])
                tag = "auto" if has_text(src["pdf"]) else "ocr"
                rows.append((t["topic"], e["ref"], side, tag if r else "AUTO-FAIL", f"{key} {r}"))
    return rows


OUT_DIR = ROOT / "converted packages/H2 math/topical/Epoch 1"
KIND_LABEL = {"core": "Core", "extra": "Extra fundamental", "substitute": "Substitute"}


def number_items(plan):
    k = 0
    for t in plan:
        n_core = sum(1 for e in t["items"] if e["kind"] in ("core", "substitute"))
        n_extra = sum(1 for e in t["items"] if e["kind"] == "extra")
        xi = 0
        for e in t["items"]:
            k += 1
            e["id"] = f"E1-{k:03d}"
            if e["kind"] == "extra":
                xi += 1
                e["label"] = f"Extra fundamental {xi} of {n_extra}"
            elif e["kind"] == "substitute":
                e["label"] = f"Core {e['coreN']} (substitute)"
            else:
                e["label"] = f"Core {e['coreN']} of {n_core}" if t["mode"] == "full" else f"Core {e['coreN']} (check set)"
    return plan


def marks_str(m):
    if m in (None, ""):
        return ""
    m = str(m)
    return m if m.startswith("[") else f"[{m}]"


def header_lines(t, e, side):
    line1 = f"{t['topic']}  |  {e['label']}"
    bits = [e["ref"]]
    if marks_str(e.get("marks")):
        bits.append(marks_str(e.get("marks")))
    if e.get("replaces"):
        bits.append(f"replaces {e['replaces']} (question paper not in the corpus)")
    if e.get("parts") and e["parts"] != "all":
        bits.append(f"do {e['parts']}")
    if e.get("skip"):
        bits.append(f"skip: {e['skip']}")
    if e.get("note"):
        bits.append(e["note"])
    if side == "a":
        s = e.get("ssrc") or {}
        if "regen" in s:
            bits.append("REGENERATED worked solution (no official mark scheme in the corpus)")
        elif s.get("pdf"):
            bits.append("solution: " + Path(s["pdf"]).stem)
    return line1, "  ·  ".join(bits)


def compose_side(plan, side):
    from _epoch_compose import Layout, add_footers, regions_for
    import pymupdf

    ov = load_overrides()
    doc = pymupdf.open()
    lay = Layout(doc)
    toc, pages, problems = [], {}, []
    last_block = None
    for t in plan:
        if t["block"] != last_block:
            last_block = t["block"]
            toc.append([1, t["block"], len(doc) + 1])
        lay.new_page()
        toc.append([2, t["topic"], len(doc)])
        mode = "full core list plus extra fundamentals" if t["mode"] == "full" else f"check set: first {len(t['items'])} core questions"
        lay.banner(f"{t['topic']}  (confidence {t['level']}/4)",
                   [f"{t['block']}. {mode}. {len(t['items'])} questions: " + ", ".join(f"{e['id']} {e['ref']}" for e in t["items"])])
        for e in t["items"]:
            src = e.get("qsrc") if side == "q" else e.get("ssrc")
            regs = regions_for(src, ov)
            line1, line2 = header_lines(t, e, side)
            first_h = regs[0][2].height * min(1.0, 527 / regs[0][2].width) if regs else 40
            lay.item_header(e["id"], line1, line2, first_h)
            pages[e["id"]] = len(doc)
            toc.append([3, f"{e['id']} {e['ref']}", len(doc)])
            if not regs:
                problems.append((e["id"], e["ref"], side))
                lay.note("Source region not available yet. " + (e.get("stem") or ""))
            for d, p, clip in regs:
                lay.place(d, p, clip)
            lay.gap(12)
    return doc, toc, pages, problems


SEV_R = [0, 0.1, 0.35, 0.8, 0.97]
SEV_H = [0, 0, 0.05, 0.25, 0.55]
MIN_PER_MARK = 2.4
DEFAULT_MARKS = 8


def item_marks(e):
    m = re.search(r"\[?(\d+)", str(e.get("marks") or ""))
    return int(m.group(1)) if m else DEFAULT_MARKS


def block_summary(plan):
    model = {t["id"]: t for t in json.loads((WORK / "math_readiness_model.json").read_text(encoding="utf-8"))["topics"]}
    out = []
    for bname, tids in BLOCKS:
        ts = [t for t in plan if t["block"] == bname]
        n = sum(len(t["items"]) for t in ts)
        marks = sum(item_marks(e) for t in ts for e in t["items"])
        gain = 0.0
        for t in ts:
            mt = model[t["tid"]]
            w, nt, L = mt["marksAvg"], mt["nt"], t["level"]
            val = lambda l: w * ((1 - nt) * SEV_R[l] + nt * SEV_H[l])
            gain += val(max(L, 3)) - val(L)
        topics = ", ".join(f"{t['topic']} ({t['level']})" for t in ts)
        out.append({"block": bname, "topics": topics, "n": n, "hours": marks * MIN_PER_MARK / 60, "gain": gain})
    return out


def plan_markdown(plan):
    rows = block_summary(plan)
    lines = ["# Epoch 1 plan", "",
             "Ratings come from the readiness sheet. Topics rated 1 or 2 get their full core list plus extra fundamentals; "
             "topics rated 3 get a check set of their first three core questions.", "",
             "| # | Block | Topics (rating) | Questions | Est. hours | Marks the model gains if every topic in the block reaches 3 |",
             "|---|---|---|---|---|---|"]
    for i, r in enumerate(rows, 1):
        lines.append(f"| {i} | {r['block']} | {r['topics']} | {r['n']} | {r['hours']:.1f} | {r['gain']:.1f} |")
    tot_n = sum(r["n"] for r in rows)
    lines += ["", f"Total: {tot_n} questions, about {sum(r['hours'] for r in rows):.0f} hours at {MIN_PER_MARK} minutes per mark "
              f"(attempt at exam pace plus marking), and {sum(r['gain'] for r in rows):.0f} model marks out of 200 available.", ""]
    for t in plan:
        lines.append(f"## {t['topic']} (rating {t['level']}, {'full list' if t['mode'] == 'full' else 'check set'})")
        for e in t["items"]:
            extra = f" (replaces {e['replaces']})" if e.get("replaces") else ""
            sol = " Regenerated solution." if "regen" in (e.get("ssrc") or {}) else ""
            lines.append(f"- {e['id']} {e['label']}: {e['ref']} {marks_str(e.get('marks'))}{extra}.{sol}")
        lines.append("")
    return "\n".join(lines)


def front_matter(plan, qpages, apages, side, offset):
    from _epoch_compose import html_to_pdf

    summ = block_summary(plan)
    order_rows = "".join(
        f"<tr><td>{i}</td><td>{html.escape(r['block'])}</td><td>{html.escape(r['topics'])}</td><td>{r['n']}</td>"
        f"<td>{r['hours']:.1f}</td><td>{r['gain']:.1f}</td></tr>" for i, r in enumerate(summ, 1))
    order_html = (
        "<h2>Order</h2><p>Differentiation goes first because Graphs, Maclaurin series and the integration chain all rely on it. "
        "After that the blocks run roughly in order of marks unlocked: Graphs (your only topic at 1) and Vectors (the heaviest topic). "
        "Two statistics blocks are interleaved so that Paper 2 Section B does not go cold during the long pure stretches.</p>"
        "<table><tr><th>#</th><th>Block</th><th>Topics (rating)</th><th>Qns</th><th>Hours</th><th>Model marks gained at rating 3</th></tr>"
        + order_rows + "</table><p class='small'>Hours assume 2.4 minutes per mark (exam pace plus marking). Marks gained use the "
        "readiness model's brutal weighting and count only weak topics moving up to 3; check-set topics already sit at 3.</p>")

    title = "Epoch 1 topical pack: questions" if side == "q" else "Epoch 1 topical pack: answer scheme"
    rows = []
    for t in plan:
        rows.append(f"<tr><th colspan='5'>{html.escape(t['block'])}: {html.escape(t['topic'])} "
                    f"(confidence {t['level']}/4, {'full list' if t['mode'] == 'full' else 'check set'})</th></tr>")
        for e in t["items"]:
            rows.append(f"<tr><td>{e['id']}</td><td>{html.escape(e['label'])}</td><td>{html.escape(e['ref'])}</td>"
                        f"<td>{html.escape(marks_str(e.get('marks')))}</td><td>{qpages[e['id']] + offset} / {apages[e['id']] + offset}</td></tr>")
    intro = (
        "<p>Each question has the same ID in the question PDF and the answer PDF. Questions are cropped from the original papers, "
        "so diagrams and mark allocations are as printed. Work in the order given: blocks run top to bottom, and within a topic "
        "the extra fundamentals come first, then the core list.</p>"
        "<p>Topics you rated 1 or 2 get their full core list plus extra fundamental questions. Topics you rated 3 get a check set of "
        "their first three core questions only; the rest of their core list waits for Epoch 2 unless the timed paper shows a leak.</p>"
        "<p>Where a core question's paper is not in the corpus, a question of the same type replaces it and is labelled <b>substitute</b>. "
        "Where a core question has no official mark scheme, the answer PDF contains a <b>regenerated</b> worked solution, checked "
        "numerically but not an official scheme.</p>"
    )
    body = (f"<h1>{title}</h1><p class='small'>H2 Mathematics 9758. Built from the readiness ratings and the Revision Order core lists.</p>"
            f"{intro}{order_html}<h2>Contents</h2><table><tr><th>ID</th><th>Role</th><th>Source</th><th>Marks</th><th>Page (Q / A)</th></tr>"
            + "".join(rows) + "</table>")
    css = ("table{font-size:8.3pt} td,th{padding:1.5pt 4pt} td:nth-child(1),td:nth-child(2),td:nth-child(4),td:nth-child(5)"
           "{white-space:nowrap} p{margin:4pt 0}")
    return html_to_pdf(body, f"epoch1-front-{side}", css)


def build_pdfs(plan):
    import pymupdf

    OUT_DIR.mkdir(parents=True, exist_ok=True)
    qdoc, qtoc, qpages, qprob = compose_side(plan, "q")
    adoc, atoc, apages, aprob = compose_side(plan, "a")
    offset = 0
    for _ in range(3):
        f_q = pymupdf.open(str(front_matter(plan, qpages, apages, "q", offset)))
        if len(f_q) == offset:
            break
        offset = len(f_q)
    f_a = pymupdf.open(str(front_matter(plan, qpages, apages, "a", offset)))
    results = {}
    for side, body, front, toc, label in (("q", qdoc, f_q, qtoc, "Epoch 1 questions"),
                                           ("a", adoc, f_a, atoc, "Epoch 1 answer scheme")):
        from _epoch_compose import add_footers

        add_footers(body, label, len(front))
        out = pymupdf.open()
        out.insert_pdf(front)
        out.insert_pdf(body)
        out.set_toc([[1, "Contents", 1]] + [[lv, s, p + len(front)] for lv, s, p in toc])
        name = "Epoch 1 Questions.pdf" if side == "q" else "Epoch 1 Answer Scheme.pdf"
        out.save(str(OUT_DIR / name), garbage=3, deflate=True)
        results[side] = (name, len(out))
    return results, qprob, aprob


def previews(plan, only=None):
    """Stack each item's crops into a PNG for visual QA."""
    from _epoch_compose import regions_for
    from PIL import Image

    ov = load_overrides()
    pdir = WORK / "_crops"
    pdir.mkdir(exist_ok=True)
    index = []
    for t in plan:
        for e in t["items"]:
            if only and e["id"] not in only:
                continue
            for side, key in (("q", "qsrc"), ("a", "ssrc")):
                src = e.get(key)
                regs = regions_for(src, ov)
                imgs = []
                for d, p, clip in regs:
                    pix = d[p].get_pixmap(dpi=60, clip=clip)
                    imgs.append(Image.frombytes("RGB", (pix.width, pix.height), pix.samples))
                f = pdir / f"{e['id']}_{side}.png"
                if imgs:
                    W = max(i.width for i in imgs)
                    canvas = Image.new("RGB", (W, sum(i.height + 6 for i in imgs)), (255, 120, 120))
                    y = 0
                    for i in imgs:
                        canvas.paste(i, (0, y))
                        y += i.height + 6
                    canvas.save(f)
                index.append({"id": e["id"], "side": side, "topic": t["topic"], "ref": e["ref"], "png": str(f.relative_to(ROOT)) if imgs else None,
                              "pdf": (src or {}).get("pdf") or (src or {}).get("regen"), "q": (src or {}).get("q"),
                              "regions": [[p + 1, round(c.y0 / d[p].rect.height, 3), round(c.y1 / d[p].rect.height, 3)] for d, p, c in regs]})
    (WORK / "epoch1_crop_index.json").write_text(json.dumps(index, indent=1, ensure_ascii=False), encoding="utf-8")
    return index


if __name__ == "__main__":
    plan = number_items(build_plan())
    (WORK / "epoch1_plan.json").write_text(json.dumps(plan, indent=1, ensure_ascii=False), encoding="utf-8")
    n = sum(len(t["items"]) for t in plan)
    print("items", n)
    for t in plan:
        print(f"  {t['block'][:28]:28s} {t['topic'][:30]:30s} L{t['level']} {t['mode']:7s} {len(t['items'])}")
    if "--regions" in sys.argv:
        from collections import Counter
        rows = region_report(plan)
        print(Counter(r[3] for r in rows))
        for r in rows:
            if r[3] not in ("auto", "ocr", "regen", "override") or "-v" in sys.argv:
                print("  ", r[3], "|", r[0][:18], "|", r[1], "|", r[2], "|", r[4][:120])
    if "--preview" in sys.argv:
        idx = previews(plan)
        print("previews", len(idx), "missing", sum(1 for i in idx if not i["png"]))
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    (OUT_DIR / "Epoch 1 plan.md").write_text(plan_markdown(plan), encoding="utf-8")
    if "--pdf" in sys.argv:
        res, qp, ap = build_pdfs(plan)
        print(res)
        print("no question region:", qp)
        print("no solution region:", ap)
