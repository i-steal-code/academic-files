"""Build the H2 Math readiness canvas from tagged A-level papers + the revision-order topical list."""
import json
import re
from collections import Counter, defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
WORK = ROOT / "tools" / "_scan_work"
TEMPLATE = ROOT / "tools" / "_math_readiness_template.tsx"
CANVAS = Path.home() / ".cursor" / "projects" / "c-Users-debig-OneDrive-Desktop-github-repository-academic-files" / "canvases" / "math-readiness.canvas.tsx"
WORKSHEET_DIR = "converted packages/H2 math/topical/Revision Order questions/"

TOPICS = [
    ("fnd", "Foundations", "Foundations", "Pure"),
    ("vec", "Vectors", "Vectors", "Pure"),
    ("eqn", "Equations and Inequalities", "Eqns & Ineq", "Pure"),
    ("fun", "Functions", "Functions", "Pure"),
    ("cpx", "Complex Numbers", "Complex", "Pure"),
    ("dif", "Differentiation Techniques", "Diff techniques", "Pure"),
    ("aod", "Applications of Differentiation", "App. of diff", "Pure"),
    ("seq", "Sequences and Series", "Seq & series", "Pure"),
    ("mac", "Maclaurin and Binomial Series", "Maclaurin", "Pure"),
    ("gra", "Graphs and Transformations", "Graphs", "Pure"),
    ("int", "Integration Techniques", "Integration", "Pure"),
    ("aoi", "Applications of Integration", "App. of int", "Pure"),
    ("de", "Differential Equations", "Diff eqns", "Pure"),
    ("pnc", "Permutations and Combinations", "P&C", "Statistics"),
    ("prb", "Probability", "Probability", "Statistics"),
    ("drv", "Discrete Random Variables", "DRV", "Statistics"),
    ("bin", "Binomial Distribution", "Binomial", "Statistics"),
    ("nor", "Normal Distribution", "Normal", "Statistics"),
    ("sam", "Sampling and Estimation", "Sampling", "Statistics"),
    ("hyp", "Hypothesis Testing", "Hyp. testing", "Statistics"),
    ("reg", "Correlation and Linear Regression", "Corr & reg", "Statistics"),
]
BY_NAME = {t[1]: t for t in TOPICS}
SHRINK_K = 20
PURE_TOTAL, STATS_TOTAL = 140, 60

# ---------- A-level tags ----------
tags = []
for f in sorted(WORK.glob("alevel_tag_P*_*.json")):
    tags += json.loads(f.read_text(encoding="utf-8"))
years = sorted({int(t["year"]) for t in tags})
papers = sorted({(int(t["year"]), int(t["paper"])) for t in tags})

unknown = Counter(t["topic"] for t in tags if t["topic"] not in BY_NAME)
if unknown:
    print("WARNING unknown topics:", unknown)

oos = sum(t["marks"] for t in tags if t.get("outOfSyllabus"))
ins = [t for t in tags if not t.get("outOfSyllabus") and t["topic"] in BY_NAME]


def section(t):
    if int(t["paper"]) == 1:
        return "p1"
    return "p2b" if BY_NAME[t["topic"]][3] == "Statistics" else "p2a"


# per year scaled marks (pure -> 140, stats -> 60) so removed parts do not shrink the paper
year_marks = {tid: [0.0] * len(years) for tid, *_ in TOPICS}
sec_marks = {tid: Counter() for tid, *_ in TOPICS}
for yi, y in enumerate(years):
    rows = [t for t in ins if int(t["year"]) == y]
    pure_sum = sum(t["marks"] for t in rows if BY_NAME[t["topic"]][3] == "Pure") or 1
    stat_sum = sum(t["marks"] for t in rows if BY_NAME[t["topic"]][3] == "Statistics") or 1
    for t in rows:
        tid = BY_NAME[t["topic"]][0]
        scale = PURE_TOTAL / pure_sum if BY_NAME[t["topic"]][3] == "Pure" else STATS_TOTAL / stat_sum
        year_marks[tid][yi] += t["marks"] * scale
        sec_marks[tid][section(t)] += t["marks"] * scale

nt_tot = sum(t["nonTrivialMarks"] for t in ins)
mk_tot = sum(t["marks"] for t in ins) or 1
nt_global = nt_tot / mk_tot

topics_out = []
for tid, name, short, pillar in TOPICS:
    rows = [t for t in ins if t["topic"] == name]
    marks = sum(t["marks"] for t in rows)
    ntm = sum(t["nonTrivialMarks"] for t in rows)
    nt_raw = ntm / marks if marks else nt_global
    nt = (ntm + SHRINK_K * nt_global) / (marks + SHRINK_K)
    ym = year_marks[tid]
    avg = sum(ym) / len(years) if years else 0
    types = Counter()
    for t in rows:
        if t["nonTrivialMarks"] and t.get("ntType"):
            for k in re.split(r"[/,+ ]+", t["ntType"]):
                if k:
                    types[k.upper()] += t["nonTrivialMarks"]
    examples = [f'{t["year"]} P{t["paper"]} Q{t["q"]}{t.get("part","")}: {t["ntReason"]}'
                for t in sorted(rows, key=lambda r: -r["nonTrivialMarks"]) if t["nonTrivialMarks"] and t.get("ntReason")][:3]
    topics_out.append({
        "id": tid, "name": name, "short": short, "pillar": pillar,
        "weight": round(avg / 2, 2),
        "marksAvg": round(avg, 2),
        "p1": round(sec_marks[tid]["p1"] / len(years), 2) if years else 0,
        "p2a": round(sec_marks[tid]["p2a"] / len(years), 2) if years else 0,
        "p2b": round(sec_marks[tid]["p2b"] / len(years), 2) if years else 0,
        "yearsTested": sum(1 for v in ym if v > 0),
        "nYears": len(years),
        "minMarks": round(min(ym)) if ym else 0,
        "maxMarks": round(max(ym)) if ym else 0,
        "nt": round(nt, 4), "ntRaw": round(nt_raw, 4), "ntMarks": ntm, "totalMarks": marks,
        "ntTypes": dict(types), "ntExamples": examples,
    })

# ---------- topical items ----------
ro = json.loads((WORK / "revision_order_topical.json").read_text(encoding="utf-8"))
extract = {}
for f in sorted(WORK.glob("topical_extract_G*.json")):
    for e in json.loads(f.read_text(encoding="utf-8")):
        extract[(e["topic"], e["tier"], int(e["n"]), e["ref"])] = e

RESERVED = []
SPENT = [("RI", "2024", "2")]


def match(meta, rules):
    return any(meta.get("school") == s and meta.get("year") == y and (p is None or meta.get("paper") == p) for s, y, p in rules)


items_out = []
for i in ro:
    tid = BY_NAME[i["topic"]][0]
    e = extract.get((i["topic"], i["tier"], i["n"], i["ref"]))
    flags = []
    if i["kind"] == "prelim" and match(i["meta"], RESERVED):
        flags.append("reserved")
    if i["kind"] == "prelim" and match(i["meta"], SPENT):
        flags.append("spent")
    if any(n.startswith("Skip") for n in i["notes"]):
        flags.append("skip")
    if any(n.startswith("Printed") for n in i["notes"]):
        flags.append("check")
    no_qp = bool(e) and e.get("status") == "missing_doc" and i["found"]
    if not i["found"] or no_qp:
        status = "missing"
    elif e and e.get("status") in ("partial", "not_located"):
        status = "partial"
    elif not i["hasSoln"]:
        status = "noSoln"
    else:
        status = "ready"
    stem = (e or {}).get("stem") or ""
    if not stem:
        stem = "Source document not in the repository" if not i["found"] else "Question text not yet extracted"
    note = ""
    skip = [n for n in i["notes"] if n.startswith("Skip")]
    if skip:
        note = skip[0]
    if no_qp:
        note = "Question paper not in corpus; the summary is reconstructed from the worked solution."
    if i["ref"] == "C7A Lect Notes · Example 4" and i["topic"] == "Graphs and Transformations":
        note = "Cited example is a sequences question; the worksheet also includes C8B Example 4, the likely intended one."
    items_out.append({
        "key": f'{tid}-{i["tier"]}-{i["n"]}', "topicId": tid, "tier": i["tier"], "n": i["n"], "ref": i["ref"],
        "marks": i["marks"], "stem": stem, "status": status, "flags": flags, "note": note,
    })

# ---------- acquisition list ----------
acq = defaultdict(lambda: {"blocks": [], "core": False, "kind": "questions", "note": ""})
for i, o in zip(ro, items_out):
    label = f'{o["ref"]} ({i["topic"]}{", stretch" if i["tier"] == "stretch" else ""})'
    if i["found"] and o["status"] == "missing":
        m = i["meta"]
        doc = f'{m["school"]} Prelim {m["year"]} P{m["paper"]} question paper'
        note = "Only the worked solutions are in the corpus; the questions are not reprinted in them."
        kind = "questions"
    elif not i["found"]:
        if i["kind"] == "addprac":
            doc = f'RI {i["meta"]["chapter"]} Additional Practice (Qns + Solns)'
            note = "Same series as the C2A–C9C worksheets already in topical/T3 SR set."
            kind = "questions"
        elif i["kind"] == "mock":
            doc = f'RI Mock {i["meta"]["year"]} P{i["meta"]["paper"]}'
            note = "Revision order says this is on the hardcopy. Scan it into raw files/H2 math."
            kind = "hardcopy"
        else:
            doc, note, kind = i["ref"], "", "questions"
    elif not i["hasSoln"]:
        m = i["meta"]
        doc = f'{m["school"]} Prelim {m["year"]} P{m["paper"]} mark scheme'
        note = "Question paper is in the corpus; answers are not."
        kind = "solutions"
    else:
        continue
    a = acq[doc]
    a["blocks"].append(label)
    a["core"] = a["core"] or i["tier"] == "core"
    a["kind"], a["note"] = kind, note

for i, o in zip(ro, items_out):
    if o["status"] == "partial":
        e = extract.get((i["topic"], i["tier"], i["n"], i["ref"])) or {}
        m = re.match(r"A-Level (\d{4}) P(\d)", i["ref"])
        doc = f"A-level {m.group(1)} P{m.group(2)} complete scan" if m else f'{i["ref"]} clean copy'
        a = acq[doc]
        a["blocks"].append(f'{o["ref"]} ({i["topic"]}{", stretch" if i["tier"] == "stretch" else ""})')
        a["core"] = a["core"] or i["tier"] == "core"
        a["kind"] = "scan"
        a["note"] = (e.get("issues") or "Pages missing from the scanned copy.")[:220]

SCAN_GAPS = {
    "A-level 2019 P2 complete scan": "Printed pages 18–19 are missing (Q9(iii), Q10 stem, data table and part (i)).",
    "A-level 2022 P2 complete scan": "Printed pages 14–15 are missing (Q7); the 8-mark split used for weights is estimated.",
    "A-level 2024 P1 complete scan": "The question-paper scan has no Q11 pages; marks were read from the answer file.",
}
for doc, note in SCAN_GAPS.items():
    a = acq[doc]
    a["kind"] = "scan"
    a["note"] = note
    if not a["blocks"]:
        a["blocks"].append("Weight tagging only")

TIMED_GAPS = {
    "VJC Prelim 2026 P1 question paper": ("Final rehearsal 1 (about a week before Paper 1)",
                                          "Only the solutions booklet is in the corpus; it does not reprint the questions."),
    "ACJC Prelim 2026 P1 question paper": ("Timed set 2",
                                           "Only the solutions booklet is in the corpus; it does not reprint the questions."),
    "RVHS Prelim 2026 P1 + P2 mark schemes": ("Timed set 6",
                                              "Question papers are in the corpus; no solutions, so the set cannot be self-marked."),
}
for doc, (blocks, note) in TIMED_GAPS.items():
    acq[doc].update({"blocks": [blocks], "core": True, "kind": "timed", "note": note})

acquire_out = sorted(
    [{"doc": d, "kind": a["kind"], "priority": "core" if a["core"] else "stretch", "blocks": a["blocks"], "note": a["note"]}
     for d, a in acq.items()],
    key=lambda a: (a["priority"] != "core", a["kind"] == "solutions", -len(a["blocks"])),
)

data = {
    "topics": topics_out,
    "years": [str(y) for y in years],
    "yearMarks": {k: [round(v, 2) for v in vs] for k, vs in year_marks.items()},
    "items": items_out,
    "acquire": acquire_out,
    "meta": {"papers": len(papers), "taggedMarks": mk_tot, "oosMarks": oos, "ntGlobal": round(nt_global, 4),
             "shrinkK": SHRINK_K, "worksheetDir": WORKSHEET_DIR},
}

tpl = TEMPLATE.read_text(encoding="utf-8")
CANVAS.write_text(tpl.replace("__DATA__", json.dumps(data, ensure_ascii=False, indent=1)), encoding="utf-8")
(WORK / "math_readiness_model.json").write_text(json.dumps(data, ensure_ascii=False, indent=1), encoding="utf-8")

print(f"papers {len(papers)} years {years} in-syllabus marks {mk_tot} oos {oos} nt_global {nt_global:.3f}")
print(f"{'topic':34s} {'w%':>6s} {'avg':>6s} {'P1':>5s} {'P2A':>5s} {'P2B':>5s} {'yrs':>4s} {'ntRaw':>6s} {'nt':>6s}")
for t in sorted(topics_out, key=lambda t: -t["weight"]):
    print(f'{t["name"]:34s} {t["weight"]:6.2f} {t["marksAvg"]:6.1f} {t["p1"]:5.1f} {t["p2a"]:5.1f} {t["p2b"]:5.1f} {t["yearsTested"]:4d} {t["ntRaw"]:6.2f} {t["nt"]:6.2f}')
print("weight sum", round(sum(t["weight"] for t in topics_out), 2))
print("items", len(items_out), Counter(o["status"] for o in items_out))
print("acquire", len(acquire_out))
for a in acquire_out:
    print(" ", a["priority"], a["kind"], a["doc"], len(a["blocks"]))
