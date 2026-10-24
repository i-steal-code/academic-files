import html
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "raw files" / "H2 math" / "topical" / "H2 Math Revision Order.html"
CP = ROOT / "converted packages" / "H2 math"
OUT = ROOT / "tools" / "_scan_work" / "revision_order_topical.json"

raw = SRC.read_text(encoding="utf-8", errors="replace")


def clean(s: str) -> str:
    s = re.sub(r"<[^>]+>", " ", s)
    s = html.unescape(s)
    s = s.replace("\u00a0", " ").replace("\ufffd", "·")
    return re.sub(r"\s+", " ", s).strip()


def md_len(p: Path) -> int:
    f = p / "content.md"
    return f.stat().st_size if f.exists() else -1


def resolve(ref: str):
    """Return (kind, candidate dirs in priority order, note)."""
    m = re.match(r"A-Level (\d{4}) P(\d) Q(\d+)", ref)
    if m:
        y, p, q = m.groups()
        name = f"{y} P{p} A-level H2 math"
        return "alevel", [CP / "TYS ANS" / name, CP / "TYS QP" / name], {"year": y, "paper": p, "q": q}
    m = re.match(r"RI Mock (\d{4}) P(\d) Q(\d+)", ref)
    if m:
        y, p, q = m.groups()
        return "mock", [CP / "misc" / f"{y} RI P{p} mock H2 math", CP / "misc" / f"{y} RI P{p} mock Solns H2 math"], {"year": y, "paper": p, "q": q}
    m = re.match(r"([A-Z]+) Prelim (\d{4}) P(\d) Q(\d+)", ref)
    if m:
        sch, y, p, q = m.groups()
        name = f"{y} {sch} P{p} prelim H2 math"
        return "prelim", [CP / "prelim QP" / name, CP / "prelim ANS" / name], {"school": sch, "year": y, "paper": p, "q": q}
    m = re.match(r"(C\w+) Add Prac · Q(\d+)", ref)
    if m:
        ch, q = m.groups()
        return "addprac", [CP / "topical" / "Add Prac" / f"{ch} Add Prac Qns", CP / "topical" / "Add Prac" / f"{ch} Add Prac Solns"], {"chapter": ch, "q": q}
    m = re.match(r"(C\w+) Lect(?:ure)? Notes · (.+)", ref)
    if m:
        ch, ex = m.groups()
        sub = "statistics" if ch.startswith("CS") else "pure"
        return "lectnotes", [CP / "base syllabus" / sub / f"{ch} Lecture Notes"], {"chapter": ch, "example": ex}
    m = re.match(r"(Zeta|Lambda|Delta) Q(\d+) · (.+)", ref)
    if m:
        st, q, chs = m.groups()
        return "t3set", [], {"set": st, "q": q, "chapters": chs}
    return "unknown", [], {}


T3_FILES = {
    "Calculus I": ["6a", "6b", "7c", "8a", "8b", "8ab"],
    "Calculus II": ["9a", "9b", "9c", "9abc"],
    "Complex Numbers Sequences and Series": ["5", "7a", "7b"],
    "Vectors II and III": ["2a", "2b", "2c"],
    "Statistics": ["cs", "s", "statistics"],
}


def t3_dirs(st: str, chapters: str):
    tags = [t.strip().lower() for t in chapters.split(",")]
    best = None
    for name, keys in T3_FILES.items():
        if any(t in keys for t in tags):
            best = name
            break
    if best is None and any(t.startswith("cs") for t in tags):
        best = "Statistics"
    if best is None:
        return []
    base = CP / "topical" / "T3 SR set"
    return [base / f"2026 {st} {best} Qns", base / f"2026 {st} {best} Solns"]


items = []
group = None
for sec in re.finditer(r'(<p class="grp">([^<]+)</p>)?<section class="topic" id="([^"]+)">(.*?)</section>', raw, re.S):
    if sec.group(2):
        group = clean(sec.group(2))
    tid = sec.group(3)
    body = sec.group(4)
    title = clean(re.search(r"<h3>(.*?)</h3>", body, re.S).group(1))
    core_html, _, stretch_html = body.partition("<details>")
    for tier, chunk in (("core", core_html), ("stretch", stretch_html)):
        for li in re.finditer(r'<li class="q">(.*?)</li>', chunk, re.S):
            frag = li.group(1)
            n = clean(re.search(r'<span class="n">(.*?)</span>', frag).group(1))
            ref = clean(re.search(r'class="ref">(.*?)</label>', frag, re.S).group(1))
            mk = re.search(r'<span class="mk">(.*?)</span>', frag, re.S)
            notes = [clean(x) for x in re.findall(r'<p class="nt[^"]*">(.*?)</p>', frag, re.S)]
            kind, dirs, meta = resolve(ref)
            if kind == "t3set":
                dirs = t3_dirs(meta["set"], meta["chapters"])
            avail = []
            for d in dirs:
                avail.append({"dir": str(d.relative_to(ROOT)), "exists": d.exists(), "md": md_len(d) if d.exists() else -1,
                              "pages": len(list((d / "pages").glob("*.png"))) if (d / "pages").exists() else 0})
            usable = [a for a in avail if a["exists"] and (a["md"] > 500 or a["pages"] > 0)]
            ok = lambda a: a["exists"] and (a["md"] > 500 or a["pages"] > 0)
            if kind in ("alevel", "lectnotes"):
                has_q = has_s = bool(usable)
            elif kind in ("prelim", "mock"):
                qp, ans = avail[0], avail[1]
                has_s = ok(ans)
                has_q = ok(qp) or has_s
            elif kind in ("addprac", "t3set") and len(avail) == 2:
                has_q, has_s = ok(avail[0]), ok(avail[1])
            else:
                has_q = has_s = False
            items.append({
                "hasQ": has_q, "hasSoln": has_s,
                "group": group, "topicId": tid, "topic": title, "tier": tier, "n": int(n), "ref": ref,
                "marks": clean(mk.group(1)) if mk else "", "notes": notes, "kind": kind, "meta": meta,
                "sources": avail, "found": bool(usable),
                "textSource": next((a["dir"] for a in usable if a["md"] > 500), None),
            })

OUT.write_text(json.dumps(items, indent=1, ensure_ascii=False), encoding="utf-8")

from collections import Counter, defaultdict
print("items", len(items), Counter(i["tier"] for i in items))
by = defaultdict(lambda: [0, 0, 0, 0])
for i in items:
    k = i["topic"]
    idx = 0 if i["tier"] == "core" else 2
    by[k][idx] += 1
    if not i["found"]:
        by[k][idx + 1] += 1
for k, v in by.items():
    print(f"{k:40s} core {v[0]:2d} missing {v[1]:2d} | stretch {v[2]:2d} missing {v[3]:2d}")
print("\nMISSING:")
for i in items:
    if not i["found"]:
        print(f"  [{i['tier']}] {i['topic']}: {i['ref']} ({i['kind']}) {i['marks']}")
print("\nNO TEXT (pages only):")
for i in items:
    if i["found"] and not i["textSource"]:
        print(f"  [{i['tier']}] {i['topic']}: {i['ref']}")
