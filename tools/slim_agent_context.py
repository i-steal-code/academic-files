#!/usr/bin/env python3
"""Slim high-token, low-signal corpora so agents are not drowned in bulk OCR dumps.

Targets already-converted GP periodicals / infopacks / long guides under
``converted packages/H1 GP/``. Full text remains regenerable from ``raw files/``
via ``convert_gp_package.py --full-corpus``.

Also reports other common local junk (does not delete unless --purge-junk).
"""

from __future__ import annotations

import argparse
import json
import re
import shutil
import sys
from datetime import datetime, timezone
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
CONV_GP = REPO / "converted packages" / "H1 GP"

# Bulk factual / multi-essay dumps — keep a title index, not the full OCR body.
BULK_NAME_RE = re.compile(
    r"(?i)("
    r"KS\s*Bull|Kaleidoscope|REHEARSE|GPB\s*Issue|Infopack|"
    r"ips-working-paper|Awfully\s*GP|A for GP|"
    r"Singapore and sustainable development|"
    r"our-sg-arts-plan|Case Studies for Effectiveness"
    r")"
)

# Keep curated packages under essay resources (not topic-pack corpora).
KEEP_FULL_RE = re.compile(
    r"(?i)("
    r"^essay\s*-|^model essay|"
    r"prelim essay questions|band descriptors|"
    r"AQ examples condensed|Modern World Essays|Essay Critique|"
    r"GP Revision|Extra Outlines|Essay Keywords|"
    r"Assignment|Reader Set|\(S\) Updated Essays"
    r")"
)

HEADING_RE = re.compile(r"^(#{1,6}\s+\S.*|\d+\.\s+\S.{8,120})$")
QUESTION_RE = re.compile(
    r"(?i)(^|\n)\s*(how far|to what extent|do you agree|discuss|is it|should |"
    r"consider the|evaluate|assess|why should|in what ways|"
    r"[\"'\u2018\u2019\u201c\u201d].{10,160}\?)"
)
TITLEISH_RE = re.compile(
    r"(?i)^\s*(.{10,160}\?|contents?|culture\s*&\s*the\s*arts|"
    r"science\s*(and|&)\s*tech|politics|environment|media|education|"
    r"global|singapore|economics?)\s*$"
)


def is_bulk_package(name: str, *, rel_parts: tuple[str, ...] | None = None) -> bool:
    """True for periodicals/infopacks and all ``topics + case studies`` packs.

    Curated model essays / question lists under essay resources stay full-text
    (see KEEP_FULL_RE). Topic packs are case-study corpora — index only.
    """
    if KEEP_FULL_RE.search(name):
        return False
    if BULK_NAME_RE.search(name):
        return True
    if rel_parts and "topics + case studies" in rel_parts:
        return True
    return False


_ESSAY_TITLE_RE = re.compile(
    r"(?i)(how far|to what extent|do you agree|discuss|is this|is it |"
    r"should we|consider the|evaluate|assess|will technology|"
    r"has technology|why should|in what ways|how important|"
    r"how true|do young|is conflict|is sustainable)"
)


def extract_index_lines(text: str, *, limit: int = 80) -> list[str]:
    """Prefer essay-title lines; fall back to headings / sparse ? lines."""
    primary: list[str] = []
    secondary: list[str] = []
    seen: set[str] = set()

    def add(raw: str, bucket: list[str]) -> None:
        s = re.sub(r"\s+", " ", raw).strip(" -\t•·")
        s = s.replace("\u0000", "")
        # Normalise common mojibake quotes for readability
        for a, b in (
            ("\u2018", "'"),
            ("\u2019", "'"),
            ("\u201c", '"'),
            ("\u201d", '"'),
            ("\ufffd", ""),
        ):
            s = s.replace(a, b)
        if len(s) < 12 or len(s) > 160:
            return
        key = s.lower()
        if key in seen:
            return
        if re.fullmatch(r"[\d\W]+", s):
            return
        # Mid-paragraph rhetorical questions: keep only if title-shaped
        words = s.split()
        if len(words) > 28 and not s.lstrip().startswith(('"', "'")):
            return
        # Drop OCR fragments that are clearly not titles
        if s[0].islower() and not s.startswith(("how ", "to what", "is ", "do ", "will ")):
            return
        if len(words) < 6 and not s.rstrip().endswith("?"):
            return
        seen.add(key)
        bucket.append(s)

    for line in text.splitlines():
        stripped = line.strip()
        if not stripped:
            continue
        if HEADING_RE.match(stripped) or TITLEISH_RE.match(stripped):
            add(stripped, primary if len(stripped) < 80 else secondary)
        elif stripped.endswith("?") and _ESSAY_TITLE_RE.search(stripped):
            add(stripped, primary)
        elif stripped.endswith("?") and (
            stripped.lstrip().startswith(('"', "'", "\u201c", "\u2018"))
            or stripped[:1].isupper()
        ):
            add(stripped, secondary)

    out = primary + [x for x in secondary if x not in primary]
    if len(out) < 8:
        for m in QUESTION_RE.finditer(text):
            snippet = text[m.start() : m.start() + 200]
            first = snippet.split("\n", 1)[0]
            add(first, out)
            if len(out) >= limit:
                break

    return out[:limit]


def slim_content(pkg: Path, *, dry_run: bool) -> tuple[int, int]:
    content = pkg / "content.md"
    if not content.is_file():
        return 0, 0
    before = content.stat().st_size
    text = content.read_text(encoding="utf-8", errors="replace")
    if text.lstrip().startswith("<!-- agent-corpus: index"):
        return before, before  # already slim

    index = extract_index_lines(text)
    raw_hint = ""
    man_path = pkg / "manifest.json"
    if man_path.is_file():
        try:
            man = json.loads(man_path.read_text(encoding="utf-8-sig"))
            raw_hint = man.get("source_relpath") or ""
        except (OSError, json.JSONDecodeError):
            pass
    if not raw_hint:
        # Best-effort mirror path under raw files
        try:
            rel = pkg.relative_to(CONV_GP)
            raw_hint = f"raw files/H1 GP/{rel.as_posix()}.*"
        except ValueError:
            raw_hint = "(see raw files/H1 GP mirror)"

    body_lines = [
        "<!-- agent-corpus: index — full OCR dump removed to protect context window -->",
        f"# Index: {pkg.name}",
        "",
        "This package is a **bulk periodical / infopack / long guide**.",
        "Agents must not load a full OCR dump into context.",
        f"- Raw source: `{raw_hint}`",
        "- Need full text for a named essay/topic: re-convert with "
        "`python tools/convert_gp_package.py --full-corpus` "
        "or open the raw PDF/DOCX for that stem only.",
        "",
        "## Titles / headings recovered from prior dump",
        "",
    ]
    if index:
        body_lines.extend(f"- {line}" for line in index)
    else:
        body_lines.append(
            "_No clean title list recovered. Open the raw file; do not re-dump into chat._"
        )
    body_lines.append("")
    new_text = "\n".join(body_lines)
    after = len(new_text.encode("utf-8"))

    if dry_run:
        return before, after

    content.write_text(new_text, encoding="utf-8")
    if man_path.is_file():
        try:
            man = json.loads(man_path.read_text(encoding="utf-8-sig"))
        except (OSError, json.JSONDecodeError):
            man = {}
        man["corpus_mode"] = "index"
        man["slimmed_at"] = datetime.now(timezone.utc).isoformat()
        man["quality"] = {
            "chars": len(new_text),
            "warn": ["slimmed_bulk_corpus"],
            "full_chars_before_slim": before,
        }
        man_path.write_text(json.dumps(man, indent=2) + "\n", encoding="utf-8")
    return before, after


def purge_junk(*, dry_run: bool) -> list[str]:
    notes: list[str] = []
    targets = [
        REPO / "_tmp_exec.txt",
        REPO / "raw files" / "H1 GP" / "misc" / "essay instance - Consider the value of humour.json",
    ]
    scan = REPO / "tools" / "_scan_work"
    for t in targets:
        if t.is_file():
            notes.append(f"delete file {t.relative_to(REPO)} ({t.stat().st_size // 1024} KB)")
            if not dry_run:
                t.unlink()
    if scan.is_dir():
        size = sum(p.stat().st_size for p in scan.rglob("*") if p.is_file())
        notes.append(f"clear dir tools/_scan_work/ ({size // 1024} KB)")
        if not dry_run:
            shutil.rmtree(scan, ignore_errors=True)
            scan.mkdir(parents=True, exist_ok=True)
            (scan / ".gitkeep").write_text("", encoding="utf-8")
    return notes


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--dry-run", action="store_true")
    ap.add_argument(
        "--purge-junk",
        action="store_true",
        help="Delete root temp dumps, Gemini chat JSON export, clear tools/_scan_work",
    )
    args = ap.parse_args()

    if not CONV_GP.is_dir():
        print("No local converted packages/H1 GP — nothing to slim.", file=sys.stderr)
        return 0

    total_before = total_after = 0
    n = 0
    for content in CONV_GP.rglob("content.md"):
        pkg = content.parent
        try:
            rel_parts = pkg.relative_to(CONV_GP).parts
        except ValueError:
            rel_parts = ()
        if not is_bulk_package(pkg.name, rel_parts=rel_parts):
            continue
        b, a = slim_content(pkg, dry_run=args.dry_run)
        if b == 0:
            continue
        n += 1
        total_before += b
        total_after += a
        flag = "already-slim" if b == a and content.read_text(encoding="utf-8", errors="replace").lstrip().startswith("<!-- agent-corpus") else "slim"
        # Re-read flag safely for dry-run
        if args.dry_run:
            flag = "would-slim"
        print(f"  {flag:12} {b // 1024:5} KB -> {a // 1024:4} KB  {pkg.relative_to(CONV_GP)}")

    print(
        f"\nBulk packages: {n}  "
        f"{total_before // 1024} KB -> {total_after // 1024} KB "
        f"(saved {max(0, total_before - total_after) // 1024} KB)"
    )

    if args.purge_junk:
        print("\nJunk:")
        for note in purge_junk(dry_run=args.dry_run):
            print(f"  {'would ' if args.dry_run else ''}{note}")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
