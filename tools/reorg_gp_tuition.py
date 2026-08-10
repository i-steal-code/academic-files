#!/usr/bin/env python3
"""Unpack raw files/H1 GP/tuition material into the normalised GP folder tree.

- Content-hash dedupe within tuition (prefer cleanest filename)
- Drop tuition copies that already exist elsewhere under H1 GP
- Classify remaining files into exam papers / notes / essay resources /
  topics + case studies / misc
"""

from __future__ import annotations

import argparse
import hashlib
import re
import shutil
import sys
from collections import defaultdict
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
GP = REPO / "raw files" / "H1 GP"
TUITION = GP / "tuition material"

SUFFIX_JUNK = re.compile(
    r"(?:\s*\(\d+\))?(?:\s+\d+)?(?=\.[^.]+$)",
    re.IGNORECASE,
)


def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        while True:
            chunk = f.read(1 << 20)
            if not chunk:
                break
            h.update(chunk)
    return h.hexdigest()


def name_score(name: str) -> tuple:
    """Lower is better — prefer cleanest duplicate filename."""
    stem = Path(name).stem
    penalty = 0
    if re.search(r"\(\d+\)$", stem):
        penalty += 10
    if re.search(r"\s+\d+$", stem):
        penalty += 5
    if stem.endswith(" ") or "  " in stem:
        penalty += 3
    # Prefer shorter, cleaner names
    return (penalty, len(name), name.lower())


def clean_stem(name: str) -> str:
    """Strip Windows copy suffixes like (1) only — keep years in parentheses."""
    stem = Path(name).stem
    stem = re.sub(r"\s*\([1-9]\)$", "", stem)
    stem = re.sub(r"\s+", " ", stem).strip(" ._")
    return stem


def classify(name: str) -> tuple[str, str]:
    """Return (relative_dest_dir, suggested_filename)."""
    ext = Path(name).suffix.lower()
    stem = clean_stem(name)
    low = stem.lower()

    # --- Official A-Level / TYS ---
    if re.search(r"\b(a[\s-]?level|gce)\b", low) or re.match(r"202[45]\s+a\s*level", low):
        year_m = re.search(r"(20\d{2})", stem)
        year = year_m.group(1) if year_m else ""
        is_insert = "insert" in low or re.search(r"\bin\b", low) is not None
        if is_insert and "aq" not in low:
            return "exam papers/TYS IN", f"{year} P2 A-level H1 GP{ext}".strip()
        if any(k in low for k in ("ans booklet", "answer booklet")):
            return "exam papers/TYS ANS", f"{year} P2 A-level H1 GP{ext}".strip()
        if "paper 1" in low:
            return "exam papers/TYS QP", f"{year} P1 A-level H1 GP{ext}".strip()
        if "paper 2" in low and "qp" in low:
            return "exam papers/TYS QP", f"{year} P2 A-level H1 GP{ext}".strip()
        if re.search(r"paper\s*2$", low):
            # Unlabelled Paper 2 companion (not QP/IN/ANS) — keep in misc with clear name
            return "exam papers/misc", f"{year} P2 A-level H1 GP (unlabelled){ext}".strip()
        return "exam papers/misc", f"{stem}{ext}"

    # --- Named prelims (unknown school → misc unless clearly school) ---
    if "prelim" in low:
        year_m = re.search(r"(20\d{2})", stem)
        year = year_m.group(1) if year_m else ""
        if "insert" in low or re.search(r"\bin\b", low):
            return "exam papers/misc", f"{year} Prelim P2 IN A-level H1 GP{ext}".strip() if year else f"{stem}{ext}"
        if "p1" in low or "paper 1" in low:
            return "exam papers/misc", f"{year} Prelim P1 QP A-level H1 GP{ext}".strip() if year else f"{stem}{ext}"
        if "qp" in low or "p2" in low or "paper 2" in low:
            return "exam papers/misc", f"{year} Prelim P2 QP A-level H1 GP{ext}".strip() if year else f"{stem}{ext}"
        return "exam papers/misc", f"{stem}{ext}"

    # --- J1 MYE ---
    if "mye" in low:
        return "exam papers/misc", f"{stem}{ext}"

    # --- Essay models / critiques ---
    essay_markers = (
        "essay critique",
        "model essay",
        "extra outlines",
        "comparative essay",
        "updated essays",
        "(s1) how far",
        "(s2) the arts",
        "(s8) how far",
        "modern world essay",
    )
    if any(m in low for m in essay_markers) or re.match(r"\(s\d+\)", low):
        # Keep readable essay titles
        if low.startswith("(s") and "how far" in low or "arts do not" in low or "life expectancy" in low:
            q = re.sub(r"^\(s\d+\)\s*", "", stem, flags=re.I)
            return "essay resources", f"essay - {q}{ext}"
        return "essay resources", f"{stem}{ext}"

    # --- Skills / notes ---
    notes_markers = (
        "aq guide",
        "aq skills",
        "aq_faqs",
        "aq faqs",
        "aq intro",
        "aq marking",
        "aq sample",
        "paraphrasing",
        "punctuation",
        "minefields",
        "inner guide",
        "learning point",
        "developing and crafting insight",
        "adding qualifiers",
        "summary marking",
        "beyond dp2",
        "j2 essay thinking",
        "j2 aq review",
        "data collection model aq",
    )
    if any(m in low for m in notes_markers):
        return "notes", f"{stem}{ext}"

    # --- Practice compre / P2 sets → exam papers/misc ---
    p2_markers = (
        "comedy",
        "rules ",
        "rules qp",
        "rules in",
        "rules ms",
        "rules aq",
        "convenience",
        "meritocracy",
        "democracy",
        "deomcracy",  # typo in source
        "language in",
        "language qp",
        "language ms",
        "language aq",
        "millennial",
        "millenial",
        "complaining",
        "gender norms",
        "work-centred",
        "work-centered",
        "parental",
        "p2 qp",
        "p2 ms",
        "p2 art",
        "set 1",
        "set 3",
        "set 6",
        "set 7",
        "set meritocracy",
        "tm23",
        "8881 ",
    )
    # 8881* practice papers that aren't pure AQ skill sheets
    if any(m in low for m in p2_markers) or low.startswith("8881"):
        # AQ-only skill sheets already caught; remaining 8881 are practice papers
        if any(m in low for m in ("aq guide", "aq skills", "aq intro", "aq marking sample")):
            return "notes", f"{stem}{ext}"
        return "exam papers/misc", f"{stem}{ext}"

    # --- Topics / case studies / theme notes ---
    topic_markers = (
        "science & technology",
        "science and technology",
        "environment",
        "the arts",
        "media",
        "govt",
        "governance",
        "politics",
        "pol &",
        "ir ",
        "international",
        "ethics",
        "modern world",
        "modern societies",
        "culture & society",
        "culture and society",
        "security and conflict",
        "social inequalities",
        "theme ",
        "content consolidation",
        "singapore",
        "budget",
        "notable artworks",
        "case studies",
        "ips-working",
        "straits times",
        "our-sg-arts",
        "power player",
        "vi ai",
        "review mass media",
        "j2 revision",
        "j2 env",
        "sg values",
        "green paradox",
        "cognitive revolution",
        "predictive ai",
        "faultlines",
        "racial",
        "harmony",
    )
    if any(m in low for m in topic_markers):
        return "topics + case studies", f"{stem}{ext}"

    return "misc", f"{stem}{ext}"


def unique_path(dest: Path) -> Path:
    if not dest.exists():
        return dest
    stem, suf = dest.stem, dest.suffix
    n = 2
    while True:
        cand = dest.with_name(f"{stem} ({n}){suf}")
        if not cand.exists():
            return cand
        n += 1


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--apply", action="store_true", help="Perform moves (default is dry-run)")
    ap.add_argument("--keep-tuition", action="store_true", help="Do not remove empty tuition folder")
    args = ap.parse_args()

    if not TUITION.is_dir():
        print(f"No tuition folder at {TUITION}", file=sys.stderr)
        return 1

    # Hash existing organised files
    existing_hash: dict[str, Path] = {}
    for p in GP.rglob("*"):
        if not p.is_file():
            continue
        if "tuition material" in p.parts:
            continue
        existing_hash[sha256_file(p)] = p

    # Group tuition by hash
    by_hash: dict[str, list[Path]] = defaultdict(list)
    for p in sorted(TUITION.iterdir()):
        if p.is_file():
            by_hash[sha256_file(p)].append(p)

    keepers: list[Path] = []
    dropped_dup: list[tuple[Path, Path]] = []
    dropped_overlap: list[tuple[Path, Path]] = []

    for h, paths in by_hash.items():
        best = sorted(paths, key=lambda p: name_score(p.name))[0]
        for other in paths:
            if other != best:
                dropped_dup.append((other, best))
        if h in existing_hash:
            dropped_overlap.append((best, existing_hash[h]))
            continue
        keepers.append(best)

    plan: list[tuple[Path, Path]] = []
    for src in sorted(keepers, key=lambda p: p.name.lower()):
        rel_dir, fname = classify(src.name)
        # Fix known typo in destination name
        fname = fname.replace("Deomcracy", "Democracy")
        dest = unique_path(GP / rel_dir / fname)
        # If classify produced same name collision across different hashes, unique_path handles it
        plan.append((src, dest))

    print(f"Tuition files: {sum(len(v) for v in by_hash.values())}")
    print(f"Unique hashes: {len(by_hash)}")
    print(f"Drop within-tuition dups: {len(dropped_dup)}")
    print(f"Drop overlap with existing: {len(dropped_overlap)}")
    print(f"Keep / move: {len(plan)}")
    print()

    buckets: dict[str, int] = defaultdict(int)
    for src, dest in plan:
        buckets[dest.parent.relative_to(GP).as_posix()] += 1
        print(f"MOVE  {src.name}")
        print(f"  ->  {dest.relative_to(GP).as_posix()}")
    print()
    print("Bucket counts:")
    for k in sorted(buckets):
        print(f"  {k}: {buckets[k]}")

    if dropped_dup:
        print("\nDuplicates dropped (keep first):")
        for other, best in dropped_dup[:40]:
            print(f"  DROP {other.name}  (= {best.name})")
        if len(dropped_dup) > 40:
            print(f"  ... +{len(dropped_dup) - 40} more")

    if dropped_overlap:
        print("\nAlready organised (drop tuition copy):")
        for src, ex in dropped_overlap:
            print(f"  DROP {src.name}  (= {ex.relative_to(GP).as_posix()})")

    if not args.apply:
        print("\nDry-run only. Re-run with --apply to execute.")
        return 0

    # Ensure dirs
    for _, dest in plan:
        dest.parent.mkdir(parents=True, exist_ok=True)

    # Delete dups first
    for other, _ in dropped_dup:
        other.unlink(missing_ok=True)
    for src, _ in dropped_overlap:
        src.unlink(missing_ok=True)

    for src, dest in plan:
        dest.parent.mkdir(parents=True, exist_ok=True)
        if src.resolve() == dest.resolve():
            continue
        if dest.exists():
            dest = unique_path(dest)
        shutil.move(str(src), str(dest))

    # Remove leftover tuition files (any missed) and folder
    leftovers = [p for p in TUITION.iterdir()] if TUITION.exists() else []
    for p in leftovers:
        if p.is_file():
            print(f"WARN leftover file: {p.name}", file=sys.stderr)
        elif p.is_dir() and not any(p.iterdir()):
            p.rmdir()

    if not args.keep_tuition and TUITION.exists():
        still = list(TUITION.iterdir())
        if not still:
            TUITION.rmdir()
            print("Removed empty tuition material/")
        else:
            print(f"Tuition folder still has {len(still)} entries; not removed.")

    print("Done.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
