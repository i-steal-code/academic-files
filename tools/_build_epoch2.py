"""Build Epoch 2: Paper 2 / Statistics-focused topical pack from remaining cores + edge-case stretches."""
from __future__ import annotations

import html
import json
import re
import sys
from pathlib import Path

from _epoch_lib import RAW, ROOT, WORK, auto_regions, has_text, load_overrides, region_key
from _build_epoch1 import (
    CONFIRM_N,
    DEFAULT_MARKS,
    KIND_LABEL,
    MIN_PER_MARK,
    SEV_H,
    SEV_R,
    TOPIC_IDS,
    item_marks,
    marks_str,
    regen_source,
    sources_for,
    t3_sources,
)

CANVAS_DATA = (
    Path.home()
    / ".cursor/projects/c-Users-debig-OneDrive-Desktop-github-repository-academic-files/canvases/math-readiness.canvas.data.json"
)
OUT_DIR = ROOT / "converted packages/H2 math/topical/Epoch 2"
REGEN_DIR = ROOT / "converted packages/H2 math/topical/Regenerated solutions"

# Paper-2 order: counting → discrete/binomial → Normal→Sampling→Hyp pipeline → Corr & Reg alone
BLOCKS = [
    ("Statistics I: counting and probability", ["pnc", "prb"]),
    ("Statistics II: discrete and binomial", ["drv", "bin"]),
    ("Statistics III: Normal → Sampling → Hyp pipeline", ["hyp"]),
    ("Statistics IV: correlation and regression (standalone)", ["reg"]),
]

# Scanned QP with no OCR candidates — use Revision Order worksheets for the question side
WORKSHEET_Q = {
    "RI Prelim 2021 P2 Q8",
    "RI Prelim 2021 P2 Q9",
    "RI Prelim 2021 P2 Q10",
}

# Stretch refs for non-hyp topics (nor/sam dropped — conquered; not pure-normal drills)
STRETCH_KEYS = {
    "pnc": [
        "A-Level 2016 P2 Q7",
        "TJC Prelim 2026 P2 Q7",
        "CS1A Add Prac · Q16",
    ],
    "prb": [
        "A-Level 2018 P2 Q7",
        "NJC Prelim 2025 P2 Q9",
    ],
    "drv": [
        "RI Prelim 2025 P2 Q5",
        "RI Prelim 2021 P2 Q10",
    ],
    "bin": [
        "EJC Prelim 2026 P2 Q11",
        "RI Prelim 2021 P2 Q9",
        "Zeta Q2",
    ],
    "reg": [
        "A-Level 2020 P2 Q7",
        "TJC Prelim 2026 P2 Q9",
    ],
}

# Full Epoch 1 Hypothesis Testing list (extras + cores), reprinted into Epoch 2
E1_HYP = [
    {"kind": "extra", "ref": "CS5 Add Prac · Q5", "n": 1, "marks": "8"},
    {"kind": "extra", "ref": "CS5 Add Prac · Q2", "n": 2, "marks": "7"},
    {"kind": "extra", "ref": "CS5 Add Prac · Q8", "n": 3, "marks": "12"},
    {"kind": "extra", "ref": "CS5 Add Prac · Q11", "n": 4, "marks": "5"},
    {"kind": "core", "ref": "CS5 Add Prac · Q3", "n": 1, "marks": "9",
     "note": "Epoch 1 core 1 substitute (replaces A-Level 2019 P2 Q9 — scan incomplete)"},
    {"kind": "core", "ref": "A-Level 2020 P2 Q10", "n": 2, "marks": "13",
     "note": "From Epoch 1 — pipeline hybrid"},
    {"kind": "core", "ref": "A-Level 2018 P2 Q5", "n": 3, "marks": "7",
     "note": "From Epoch 1 — pipeline hybrid"},
    {"kind": "core", "ref": "DHS Prelim 2026 P2 Q10", "n": 4, "marks": "12",
     "note": "From Epoch 1 — pipeline hybrid"},
]

# Pipeline P1–P4 (cancerous multiparts / critical-region gym)
HYP_PIPELINE = [
    {"kind": "stretch", "ref": "A-Level 2024 P2 Q8", "n": 6, "marks": "8",
     "note": "Pipeline P1: unbiased estimates → min α given rejection → n=10 insufficient"},
    {"kind": "stretch", "ref": "Zeta Q7 · Statistics", "n": 7, "marks": "12",
     "note": "Pipeline P2: unbiased → directional test → significance wording → normality? → critical set known σ"},
    {"kind": "stretch", "ref": "NJC Prelim 2026 P2 Q12", "n": 8, "marks": "12",
     "note": "Pipeline P3: unbiased → test → 1-tail vs 2-tail from rejection → non-normal find set of n"},
    {"kind": "stretch", "ref": "CS5 Add Prac · Q12", "n": 5, "marks": "8",
     "note": "Pipeline P4: symbolic critical regions (known σ), both tails"},
]

ALLOW_NO_SOLN = {"EJC Prelim 2026 P2 Q11", "NJC Prelim 2026 P2 Q12"}


def load_ratings():
    return json.loads(CANVAS_DATA.read_text(encoding="utf-8"))["ratings"]


def load_core():
    return json.loads((WORK / "revision_order_topical.json").read_text(encoding="utf-8"))


def e1_ref_set():
    plan = (ROOT / "converted packages/H2 math/topical/Epoch 1/Epoch 1 plan.md").read_text(encoding="utf-8")
    out = set()
    for line in plan.splitlines():
        if not line.startswith("- E1-"):
            continue
        body = line.split(": ", 1)[1]
        body = re.sub(r" \(replaces .+?\)$", "", body)
        body = re.sub(r"\. Regenerated solution\.$", ".", body)
        body = body.rstrip(".").strip()
        out.add(body)
        out.add(re.sub(r" \[\d+[^\]]*\]$", "", body))
        m = re.search(r"replaces (.+?)\)", line)
        if m:
            out.add(m.group(1).strip())
            out.add(re.sub(r" \[\d+[^\]]*\]$", "", m.group(1).strip()))
    return out


def ref_base(ref: str) -> str:
    return re.sub(r" \[\d+[^\]]*\]$", "", ref).strip()


def paper_key(ref: str) -> str | None:
    """Stable id for A-level / prelim / mock papers: 'A-Level 2019 P2 Q9' or 'RI Prelim 2021 P2 Q8'."""
    m = re.match(r"^(A-Level \d{4} P\d Q\d+)", ref)
    if m:
        return m.group(1)
    m = re.match(r"^((?:[A-Z]+ Prelim|RI Mock) \d{4} P\d Q\d+)", ref)
    if m:
        return m.group(1)
    return None


def in_e1(ref: str, e1: set[str]) -> bool:
    base = ref_base(ref)
    if ref in e1 or base in e1:
        return True
    if base.startswith("CS4 Lecture Notes") and any("CS4 Lecture Notes" in r for r in e1):
        return True
    # Add Prac / Lect Notes: exact base only (already checked)
    # Paper refs: match on full school/year/paper/qn, never prefix (Q1 vs Q11; Zeta Q7 calc vs stats)
    pk = paper_key(base)
    if pk:
        return any(paper_key(r) == pk for r in e1)
    return False


def t3_stats_sources(item):
    """Resolve Zeta/Lambda/Delta Statistics questions from raw T3 PDFs (no extract JSON needed)."""
    m = re.match(r"(Zeta|Lambda|Delta) Q(\d+)", item["ref"])
    if not m:
        return None, None
    st, q = m.group(1), int(m.group(2))
    base = RAW / "topical" / "T3 SR set"
    # Prefer Statistics-named files; fall back to any matching set stem
    qn = next(base.glob(f"2026 {st} *Statistics* Qns.pdf"), None) or next(base.glob(f"2026 {st} *Qns.pdf"), None)
    sn = next(base.glob(f"2026 {st} *Statistics* Solns.pdf"), None) or next(base.glob(f"2026 {st} *Solns.pdf"), None)

    def rel(p: Path | None):
        return None if p is None else str(p.relative_to(ROOT)).replace("\\", "/")

    qs = {"pdf": rel(qn), "q": q} if qn else None
    ss = {"pdf": rel(sn), "q": q} if sn else None
    return qs, ss


def worksheet_src(ref: str):
    """Prefer md worksheet rendered via regen pipeline (Chrome + KaTeX)."""
    base = paper_key(ref) or ref_base(ref)
    md = OUT_DIR / "worksheets" / f"{base}.md"
    if not md.exists():
        for p in (OUT_DIR / "worksheets").glob("*.md"):
            if p.stem == base or ref.startswith(p.stem):
                md = p
                break
    if not md.exists():
        return None
    return {"regen": str(md.relative_to(ROOT)).replace("\\", "/")}


def resolve_sources(item):
    ref = item["ref"]
    if ref.startswith(("Zeta", "Lambda", "Delta")):
        qs, ss = t3_stats_sources(item)
        if qs is None and ss is None:
            qs, ss = t3_sources(item)
    else:
        qs, ss = sources_for(ref)
    pk = paper_key(ref)
    if pk in WORKSHEET_Q:
        ws = worksheet_src(ref)
        if ws:
            qs = ws
    if ss is None or not item.get("hasSoln", True):
        ss = regen_source(ref_base(ref)) or regen_source(ref) or ss
    return qs, ss


def make_entry(item, kind: str, note: str = ""):
    ref = item["ref"]
    # synthesise minimal RO-shaped dict if needed
    ro_item = item if "hasSoln" in item or "found" in item else {
        "ref": ref,
        "n": item.get("n", 0),
        "marks": item.get("marks", ""),
        "hasSoln": not any(k in ref for k in ALLOW_NO_SOLN),
        "found": True,
        "notes": [],
        "tier": kind,
        "topic": item.get("topic", "Hypothesis Testing"),
    }
    qs, ss = resolve_sources(ro_item)
    if qs is None and ss is None:
        return None
    if ss is None and not any(k in ref for k in ALLOW_NO_SOLN):
        return None
    if ss is None and any(k in ref for k in ALLOW_NO_SOLN):
        short = re.sub(r"\s+", " ", ref_base(ref))
        ss = regen_source(short)
    notes = list(ro_item.get("notes") or [])
    if note:
        notes.append(note)
    if kind == "stretch" and "Pipeline" not in (note or ""):
        notes.append("Epoch 2 stretch")
    ref_clean = re.sub(r"(Section \d+):.*", r"\1", ref)
    ref_clean = re.sub(r"\s+lecture notes$", "", ref_clean, flags=re.I)
    return {
        "kind": kind,
        "ref": ref_clean,
        "coreN": item.get("n") or ro_item.get("n", 0),
        "marks": item.get("marks") or ro_item.get("marks", ""),
        "stem": "",
        "skip": "",
        "note": "; ".join(filter(None, notes)),
        "status": "",
        "qsrc": qs,
        "ssrc": ss,
        "tier": kind,
        "topic": ro_item.get("topic", "Hypothesis Testing"),
    }


def find_ro(items_src, ref_key: str):
    """Match on full ref stem (e.g. 'CS5 Add Prac · Q5'), never a bare chapter prefix."""
    key = ref_base(ref_key)
    exact = [i for i in items_src if ref_base(i["ref"]) == key]
    if exact:
        return exact[0]
    # Paper / Zeta: allow key as substring only when it includes the question number
    if re.search(r"Q\d+", key):
        hits = [i for i in items_src if key in i["ref"]]
        return hits[0] if hits else None
    return None


def build_hyp_entries(items_src):
    """Epoch 1 hyp list (all) + pipeline P1–P4."""
    entries = []
    for spec in E1_HYP + HYP_PIPELINE:
        key = ref_base(spec["ref"])
        ro = find_ro(items_src, key)
        if ro is None:
            ro = {
                "ref": spec["ref"],
                "n": spec["n"],
                "marks": spec["marks"],
                "hasSoln": not any(k in spec["ref"] for k in ALLOW_NO_SOLN),
                "found": True,
                "notes": [],
                "tier": spec["kind"],
                "topic": "Hypothesis Testing",
            }
        else:
            ro = dict(ro)
            ro["ref"] = spec["ref"]  # keep the intended Add Prac Q number
            ro["n"] = spec["n"]
            if spec.get("marks"):
                ro["marks"] = spec["marks"]
        e = make_entry(ro, spec["kind"], note=spec.get("note", ""))
        if e:
            # Force display ref from spec (RO match must not overwrite Q number)
            e["ref"] = spec["ref"]
            entries.append(e)
        else:
            print("WARN no source for hyp", spec["ref"])
    return entries


def build_plan():
    ratings = load_ratings()
    core = load_core()
    e1 = e1_ref_set()
    by_topic = {}
    for i in core:
        by_topic.setdefault(i["topic"], []).append(i)

    plan = []
    for bname, tids in BLOCKS:
        for tid in tids:
            topic = TOPIC_IDS[tid]
            level = ratings.get(tid, 0)
            items_src = by_topic.get(topic, [])
            entries = []

            if tid == "hyp":
                entries = build_hyp_entries(items_src)
            else:
                # Remaining cores not printed in Epoch 1
                for i in items_src:
                    if i["tier"] != "core":
                        continue
                    if in_e1(i["ref"], e1):
                        continue
                    if not i.get("found", True) and not i["ref"].startswith(("Zeta", "Lambda", "Delta")):
                        continue
                    e = make_entry(i, "core")
                    if e:
                        entries.append(e)

                for key in STRETCH_KEYS.get(tid, []):
                    hits = [i for i in items_src if i["tier"] == "stretch" and key in i["ref"]]
                    if not hits:
                        print("WARN missing stretch", tid, key)
                        continue
                    i = hits[0]
                    if in_e1(i["ref"], e1):
                        continue
                    e = make_entry(i, "stretch")
                    if e:
                        entries.append(e)
                    else:
                        print("WARN no source for stretch", i["ref"])

            if not entries:
                continue
            plan.append(
                {
                    "block": bname,
                    "tid": tid,
                    "topic": topic,
                    "level": level,
                    "mode": "epoch2",
                    "items": entries,
                }
            )
    return plan


def number_items(plan):
    k = 0
    for t in plan:
        n_extra = sum(1 for e in t["items"] if e["kind"] == "extra")
        xi = 0
        for e in t["items"]:
            k += 1
            e["id"] = f"E2-{k:03d}"
            if e["kind"] == "extra":
                xi += 1
                e["label"] = f"Extra fundamental {xi} of {n_extra}"
            elif e["kind"] == "stretch":
                e["label"] = f"Pipeline / stretch {e['coreN']}"
            else:
                e["label"] = f"Core {e['coreN']}"
    return plan


def header_lines(t, e, side):
    line1 = f"{t['topic']}  |  {e['label']}"
    bits = [e["ref"]]
    if marks_str(e.get("marks")):
        bits.append(marks_str(e.get("marks")))
    if e.get("note"):
        bits.append(e["note"])
    if side == "a":
        s = e.get("ssrc") or {}
        if not s:
            bits.append("NO OFFICIAL SCHEME in corpus — work then self-check numerically / ask for regen")
        elif "regen" in s:
            bits.append("REGENERATED worked solution (no official mark scheme in the corpus)")
        elif s.get("pdf"):
            bits.append("solution: " + Path(s["pdf"]).stem)
    return line1, "  ·  ".join(bits)


def compose_side(plan, side):
    from _epoch_compose import Layout, regions_for
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
        lay.banner(
            f"{t['topic']}  (confidence {t['level']}/4)",
            [
                f"{t['block']}. Epoch 2 Paper-2 pack. {len(t['items'])} questions: "
                + ", ".join(f"{e['id']} {e['ref']}" for e in t["items"])
            ],
        )
        for e in t["items"]:
            src = e.get("qsrc") if side == "q" else e.get("ssrc")
            regs = regions_for(src, ov) if src else []
            line1, line2 = header_lines(t, e, side)
            first_h = regs[0][2].height * min(1.0, 527 / regs[0][2].width) if regs else 40
            lay.item_header(e["id"], line1, line2, first_h)
            pages[e["id"]] = len(doc)
            toc.append([3, f"{e['id']} {e['ref']}", len(doc)])
            if not regs:
                problems.append((e["id"], e["ref"], side))
                lay.note("Source region not available yet. " + (e.get("stem") or e.get("note") or ""))
            for d, p, clip in regs:
                lay.place(d, p, clip)
            lay.gap(12)
    return doc, toc, pages, problems


def block_summary(plan):
    model_path = WORK / "math_readiness_model.json"
    if model_path.exists():
        model = {t["id"]: t for t in json.loads(model_path.read_text(encoding="utf-8"))["topics"]}
    else:
        model = {}
    out = []
    for bname, tids in BLOCKS:
        ts = [t for t in plan if t["block"] == bname]
        if not ts:
            continue
        n = sum(len(t["items"]) for t in ts)
        marks = sum(item_marks(e) for t in ts for e in t["items"])
        gain = 0.0
        for t in ts:
            mt = model.get(t["tid"])
            if not mt:
                continue
            w, nt, L = mt.get("p2b", mt.get("marksAvg", 0)), mt["nt"], t["level"]
            if t["tid"] in ("mac", "eqn"):
                w = mt.get("p2a", w)
            val = lambda l: w * ((1 - nt) * SEV_R[min(l, 4)] + nt * SEV_H[min(l, 4)])
            gain += val(4) - val(L)
        topics = ", ".join(f"{t['topic']} ({t['level']})" for t in ts)
        out.append({"block": bname, "topics": topics, "n": n, "hours": marks * MIN_PER_MARK / 60, "gain": gain})
    return out


def plan_markdown(plan):
    rows = block_summary(plan)
    lines = [
        "# Epoch 2 plan",
        "",
        "Paper 2 Section B pack. **Pure Normal and Sampling drills are omitted** (conquered). "
        "The hyp block is the Normal → Sampling → Hypothesis Testing **pipeline**: all Epoch 1 hyp questions "
        "reprinted here, plus pipeline P1–P4 hybrids. Binomial and Corr & Reg stay as standalone pillars "
        "(Corr & Reg is never merged into distribution drills).",
        "",
        "| # | Block | Topics (rating) | Questions | Est. hours | Model marks if topics reach 4 (rough) |",
        "|---|---|---|---|---|---|",
    ]
    for i, r in enumerate(rows, 1):
        lines.append(f"| {i} | {r['block']} | {r['topics']} | {r['n']} | {r['hours']:.1f} | {r['gain']:.1f} |")
    tot_n = sum(r["n"] for r in rows)
    lines += [
        "",
        f"Total: {tot_n} questions, about {sum(r['hours'] for r in rows):.0f} hours at {MIN_PER_MARK} minutes per mark.",
        "",
        "## Pipeline map (Hypothesis Testing block)",
        "",
        "| Item | Role | What stacks |",
        "|---|---|---|",
        "| CS5 Q5, Q2, Q8, Q11 | E1 extras | Warm-up hyp technique |",
        "| CS5 Q3 | E1 core 1 (sub) | z-test stand-in for AL 2019 P2 Q9 |",
        "| AL 2020 P2 Q10 | E1 core 2 | Critical region (known σ) then large-n unbiased test |",
        "| AL 2018 P2 Q5 | E1 core 3 | Why n≥30; reverse-engineer variance from non-rejection |",
        "| DHS 2026 P2 Q10 | E1 core 4 | Unbiased → p-value → range of k → why n=12 fails |",
        "| AL 2024 P2 Q8 | Pipeline P1 | Unbiased → min α given rejection → n=10 insufficient |",
        "| Zeta Q7 | Pipeline P2 | Unbiased → test → significance wording → normality? → critical set |",
        "| NJC 2026 P2 Q12 | Pipeline P3 | Unbiased → test → 1-tail vs 2-tail → non-normal set of n (no scheme) |",
        "| CS5 Q12 | Pipeline P4 | Symbolic critical regions both ways |",
        "",
    ]
    for t in plan:
        lines.append(f"## {t['topic']} (rating {t['level']})")
        for e in t["items"]:
            sol = ""
            if not e.get("ssrc"):
                sol = " No official scheme in corpus."
            elif "regen" in (e.get("ssrc") or {}):
                sol = " Regenerated solution."
            lines.append(f"- {e['id']} {e['label']}: {e['ref']} {marks_str(e.get('marks'))}.{sol}")
        lines.append("")
    return "\n".join(lines)


def front_matter(plan, qpages, apages, side, offset):
    from _epoch_compose import html_to_pdf

    summ = block_summary(plan)
    order_rows = "".join(
        f"<tr><td>{i}</td><td>{html.escape(r['block'])}</td><td>{html.escape(r['topics'])}</td><td>{r['n']}</td>"
        f"<td>{r['hours']:.1f}</td><td>{r['gain']:.1f}</td></tr>"
        for i, r in enumerate(summ, 1)
    )
    order_html = (
        "<h2>Order</h2><p>Epoch 2 is Paper 2 Section B: counting and probability, then discrete/binomial, "
        "then the Normal→Sampling→Hyp <b>pipeline</b> (all Epoch 1 hyp questions plus pipeline P1–P4), "
        "then Corr &amp; Reg alone. Pure Normal and Sampling drills are omitted.</p>"
        "<table><tr><th>#</th><th>Block</th><th>Topics (rating)</th><th>Qns</th><th>Hours</th><th>Rough model gain to 4</th></tr>"
        + order_rows
        + "</table><p class='small'>Hours assume 2.4 minutes per mark (exam pace plus marking).</p>"
    )
    title = "Epoch 2 topical pack: questions" if side == "q" else "Epoch 2 topical pack: answer scheme"
    rows = []
    for t in plan:
        rows.append(
            f"<tr><th colspan='5'>{html.escape(t['block'])}: {html.escape(t['topic'])} "
            f"(confidence {t['level']}/4)</th></tr>"
        )
        for e in t["items"]:
            rows.append(
                f"<tr><td>{e['id']}</td><td>{html.escape(e['label'])}</td><td>{html.escape(e['ref'])}</td>"
                f"<td>{html.escape(marks_str(e.get('marks')))}</td>"
                f"<td>{qpages[e['id']] + offset} / {apages.get(e['id'], qpages[e['id']]) + offset}</td></tr>"
            )
    intro = (
        "<p>Each question has the same ID in the question PDF and the answer PDF. Questions are cropped from the original papers.</p>"
        "<p><b>Epoch 2</b> drops pure Normal/Sampling drills. The hyp block reprints <b>all Epoch 1 hypothesis-testing "
        "questions</b> and adds pipeline P1–P4 hybrids (unbiased estimates, CLT/normality assumptions, critical regions, tests). "
        "Binomial and Corr &amp; Reg stay standalone.</p>"
        "<p>Where a question has no official mark scheme in the corpus, the answer side notes that explicitly.</p>"
    )
    body = (
        f"<h1>{title}</h1><p class='small'>H2 Mathematics 9758. Built for Paper 2 after Epoch 1 extras.</p>"
        f"{intro}{order_html}<h2>Contents</h2><table><tr><th>ID</th><th>Role</th><th>Source</th><th>Marks</th><th>Page (Q / A)</th></tr>"
        + "".join(rows)
        + "</table>"
    )
    css = (
        "table{font-size:8.3pt} td,th{padding:1.5pt 4pt} td:nth-child(1),td:nth-child(2),td:nth-child(4),td:nth-child(5)"
        "{white-space:nowrap} p{margin:4pt 0}"
    )
    return html_to_pdf(body, f"epoch2-front-{side}", css)


def build_pdfs(plan):
    import pymupdf
    from _epoch_compose import add_footers

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
    for side, body, front, toc, label in (
        ("q", qdoc, f_q, qtoc, "Epoch 2 questions"),
        ("a", adoc, f_a, atoc, "Epoch 2 answer scheme"),
    ):
        add_footers(body, label, len(front))
        out = pymupdf.open()
        out.insert_pdf(front)
        out.insert_pdf(body)
        out.set_toc([[1, "Contents", 1]] + [[lv, s, p + len(front)] for lv, s, p in toc])
        name = "Epoch 2 Questions.pdf" if side == "q" else "Epoch 2 Answer Scheme.pdf"
        out.save(str(OUT_DIR / name), garbage=3, deflate=True)
        results[side] = (name, len(out))
    return results, qprob, aprob


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
                    rows.append(
                        (
                            t["topic"],
                            e["ref"],
                            side,
                            "MANUAL" if (ROOT / src["pdf"]).exists() else "MISSING PDF",
                            key,
                        )
                    )
                    continue
                r = auto_regions(src["pdf"], src["q"])
                tag = "auto" if has_text(src["pdf"]) else "ocr"
                rows.append((t["topic"], e["ref"], side, tag if r else "AUTO-FAIL", f"{key} {r}"))
    return rows


if __name__ == "__main__":
    plan = number_items(build_plan())
    WORK.mkdir(parents=True, exist_ok=True)
    (WORK / "epoch2_plan.json").write_text(json.dumps(plan, indent=1, ensure_ascii=False), encoding="utf-8")
    n = sum(len(t["items"]) for t in plan)
    print("items", n)
    for t in plan:
        print(f"  {t['block'][:34]:34s} {t['topic'][:28]:28s} L{t['level']} {len(t['items'])}")
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    (OUT_DIR / "Epoch 2 plan.md").write_text(plan_markdown(plan), encoding="utf-8")
    if "--regions" in sys.argv:
        from collections import Counter

        rows = region_report(plan)
        print(Counter(r[3] for r in rows))
        for r in rows:
            if r[3] not in ("auto", "ocr", "regen", "override") or "-v" in sys.argv:
                print("  ", r[3], "|", r[0][:18], "|", r[1][:40], "|", r[2], "|", str(r[4])[:100])
    if "--pdf" in sys.argv:
        res, qp, ap = build_pdfs(plan)
        print(res)
        print("no question region:", qp)
        print("no solution region:", ap)
