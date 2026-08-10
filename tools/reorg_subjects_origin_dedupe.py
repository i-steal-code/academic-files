#!/usr/bin/env python3
"""Normalize subject folders: origin bookkeeping, bitwise dedupe, near-dupe audit.

Writes tools/_scan_work/DUPLICATE_AUDIT.md and a JSON log of actions.
Does NOT convert packages — run convert_one.ps1 afterwards.
"""

from __future__ import annotations

import hashlib
import json
import re
import shutil
from collections import defaultdict
from dataclasses import asdict, dataclass
from datetime import datetime, timezone
from pathlib import Path

try:
    import fitz
except ImportError:  # pragma: no cover
    fitz = None  # type: ignore

REPO = Path(__file__).resolve().parent.parent
RAW = REPO / "raw files"
WORK = REPO / "tools" / "_scan_work"
AUDIT_MD = WORK / "DUPLICATE_AUDIT.md"
AUDIT_JSON = WORK / "reorg_origin_dedupe_log.json"


@dataclass
class Action:
    kind: str
    src: str
    dst: str | None = None
    note: str | None = None


ACTIONS: list[Action] = []
NEAR: list[dict] = []


def rel(p: Path) -> str:
    try:
        return p.resolve().relative_to(REPO.resolve()).as_posix()
    except ValueError:
        return str(p)


def ensure_dir(p: Path) -> None:
    p.mkdir(parents=True, exist_ok=True)


def sha256(path: Path, chunk: int = 1024 * 1024) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        while True:
            b = f.read(chunk)
            if not b:
                break
            h.update(b)
    return h.hexdigest()


def move_to(src: Path, dst: Path, *, note: str | None = None) -> None:
    ensure_dir(dst.parent)
    if dst.exists():
        if src.resolve() == dst.resolve():
            return
        if sha256(src) == sha256(dst):
            src.unlink()
            ACTIONS.append(Action("delete_bitwise_dup_after_move_collision", rel(src), rel(dst), note))
            return
        # collision with different bytes → audit
        audit_dir = dst.parent / "_audit_near_dupes"
        ensure_dir(audit_dir)
        alt = audit_dir / src.name
        if alt.exists():
            alt = audit_dir / f"{src.stem}__incoming{src.suffix}"
        shutil.move(str(src), str(alt))
        ACTIONS.append(Action("move_collision_to_audit", rel(src), rel(alt), note))
        NEAR.append(
            {
                "reason": "destination_exists_different_bytes",
                "kept": rel(dst),
                "incoming": rel(alt),
                "note": note,
            }
        )
        return
    shutil.move(str(src), str(dst))
    ACTIONS.append(Action("move", rel(src), rel(dst), note))


def copy_note(msg: str) -> None:
    ACTIONS.append(Action("note", msg))


def page_count(path: Path) -> int | None:
    if fitz is None or path.suffix.lower() != ".pdf":
        return None
    try:
        doc = fitz.open(path)
        n = doc.page_count
        doc.close()
        return n
    except Exception:  # noqa: BLE001
        return None


def prefer_pdf(a: Path, b: Path) -> Path:
    """Heuristic: more pages wins; then larger file; else a."""
    pa, pb = page_count(a), page_count(b)
    if pa is not None and pb is not None and pa != pb:
        return a if pa > pb else b
    sa, sb = a.stat().st_size, b.stat().st_size
    if sa != sb:
        return a if sa > sb else b
    return a


# ---------------------------------------------------------------------------
# Origin + normalize per subject
# ---------------------------------------------------------------------------


def organize_math() -> None:
    subj = RAW / "H2 math"
    origin = subj / "origin"
    ensure_dir(origin)

    for name in (
        "math A lvl 2016-2020.pdf",
        "math A lvl 2021-2025.pdf",
        "math prelim RI 2018-2025.pdf",
        "math revision booklet T3.pdf",
    ):
        src = subj / name
        if src.is_file():
            move_to(src, origin / name, note="original import bundle")

    # Revision Paper_* solutions → prelim ANS (2018–2020 new; 2021 near-dupe flag)
    ans = subj / "prelim ANS"
    ensure_dir(ans)
    for src in sorted(subj.glob("Revision Paper_*.pdf")):
        m = re.match(r"Revision Paper_(\d{4}) RI Prelim (P[12]) \(Soln\)\.pdf$", src.name)
        if not m:
            NEAR.append({"reason": "unparsed_revision_paper_name", "path": rel(src)})
            continue
        year, paper = m.group(1), m.group(2)
        dst = ans / f"{year} RI {paper} A-level H2 math.pdf"
        if not dst.exists():
            move_to(src, dst, note="file Revision Paper soln into prelim ANS")
        else:
            if sha256(src) == sha256(dst):
                src.unlink()
                ACTIONS.append(Action("delete_bitwise_dup", rel(src), rel(dst), "revision vs prelim ANS"))
            else:
                audit = subj / "_audit_near_dupes"
                ensure_dir(audit)
                dest = audit / src.name
                shutil.move(str(src), str(dest))
                ACTIONS.append(Action("flag_near_dupe", rel(src), rel(dest)))
                NEAR.append(
                    {
                        "reason": "revision_soln_vs_prelim_ANS_different_bytes",
                        "a": rel(dst),
                        "b": rel(dest),
                        "pages_a": page_count(dst),
                        "pages_b": page_count(dest),
                        "bytes_a": dst.stat().st_size,
                        "bytes_b": dest.stat().st_size,
                        "prefer_heuristic": rel(prefer_pdf(dst, dest)),
                    }
                )


def organize_physics() -> None:
    subj = RAW / "H2 physics"
    origin = subj / "origin"
    ensure_dir(origin)
    exam = subj / "exam papers"
    qp = exam / "prelim QP"
    ans = exam / "prelim ANS"
    ensure_dir(qp)
    ensure_dir(ans)

    for name in (
        "physics revision package 1 (flipped 180deg).pdf",
        "physics revision package 2 (flipped 180deg).pdf",
        "physics revision package 3 first half.pdf",
        "physics revision package 3 second half.pdf",
    ):
        src = subj / name
        if src.is_file():
            move_to(src, origin / name, note="original revision scan bundle")

    # desktop.ini noise
    ini = subj / "desktop.ini"
    if ini.is_file():
        ini.unlink()
        ACTIONS.append(Action("delete", rel(ini), None, "noise"))

    # Map loose RI prelims at subject root into exam papers
    mappings: list[tuple[str, Path]] = []
    root_pdfs = [p for p in subj.glob("*.pdf")]
    for src in root_pdfs:
        n = src.name
        dst: Path | None = None
        # 2021
        m = re.match(r"2021 RI Prelims H2 Phy Paper (\d) (QP|Soln)\.pdf$", n)
        if m:
            paper, kind = m.group(1), m.group(2)
            folder = qp if kind == "QP" else ans
            dst = folder / f"2021 RI P{paper} A-level H2 physics.pdf"
        m = re.match(r"2022 RI Prelims H2 Phy Paper (\d) (QP|Soln)\.pdf$", n)
        if m:
            paper, kind = m.group(1), m.group(2)
            folder = qp if kind == "QP" else ans
            dst = folder / f"2022 RI P{paper} A-level H2 physics.pdf"
        m = re.match(r"2022 RI Prelims H2 Phy Paper 3 Sect ([AB]) QP\.pdf$", n)
        if m:
            sect = m.group(1)
            dst = qp / f"2022 RI P3{sect} A-level H2 physics.pdf"
        # 2023 (messy spacing)
        m = re.match(
            r"2023 RI\s+H2 Physics Prelims\s+P(\d)(?: Section ([AB]))? (Questions|Answers)\.pdf$",
            n,
        )
        if m:
            paper, sect, kind = m.group(1), m.group(2), m.group(3)
            folder = qp if kind == "Questions" else ans
            label = f"P{paper}{sect}" if sect else f"P{paper}"
            dst = folder / f"2023 RI {label} A-level H2 physics.pdf"
        # 2025
        m = re.match(
            r"2025 RI H2 Physics Prelims P(\d)(?: Section ([AB]))? (Questions|Answers)\.pdf$",
            n,
        )
        if m:
            paper, sect, kind = m.group(1), m.group(2), m.group(3)
            folder = qp if kind == "Questions" else ans
            label = f"P{paper}{sect}" if sect else f"P{paper}"
            dst = folder / f"2025 RI {label} A-level H2 physics.pdf"

        if dst is not None:
            mappings.append((n, dst))
            move_to(src, dst, note="file loose RI prelim")
        else:
            # leftover root pdfs → origin/unsorted
            move_to(src, origin / "unsorted_root" / n, note="unmapped root pdf")

    # Physics revision chapter twins: keep higher page-count name without suffix;
    # move the other into _audit_near_dupes (not bitwise identical).
    rev = subj / "base syllabus" / "revision packages"
    audit = rev / "_audit_near_dupes"
    if rev.is_dir():
        for long in sorted(rev.glob("* - physics revision package.pdf")):
            short_name = long.name.replace(" - physics revision package.pdf", ".pdf")
            short = rev / short_name
            if not short.exists():
                # rename long → short
                move_to(long, short, note="normalize revision package name")
                continue
            if sha256(long) == sha256(short):
                long.unlink()
                ACTIONS.append(Action("delete_bitwise_dup", rel(long), rel(short)))
                continue
            keep = prefer_pdf(short, long)
            drop = long if keep == short else short
            # If we prefer long content, replace short with long content under short name
            if keep == long:
                ensure_dir(audit)
                # park current short, promote long → short
                parked = audit / f"displaced__{short.name}"
                shutil.move(str(short), str(parked))
                shutil.move(str(long), str(short))
                ACTIONS.append(Action("promote_long_over_short", rel(long), rel(short)))
                NEAR.append(
                    {
                        "reason": "physics_revision_twin_promoted_long",
                        "kept": rel(short),
                        "parked": rel(parked),
                        "pages_kept": page_count(short),
                        "pages_parked": page_count(parked),
                    }
                )
            else:
                ensure_dir(audit)
                dest = audit / long.name
                shutil.move(str(long), str(dest))
                ACTIONS.append(Action("park_lower_fidelity_twin", rel(long), rel(dest)))
                NEAR.append(
                    {
                        "reason": "physics_revision_twin_parked_long",
                        "kept": rel(short),
                        "parked": rel(dest),
                        "pages_kept": page_count(short),
                        "pages_parked": page_count(dest),
                        "note": "kept higher page-count / larger short-named package; audit parked twin",
                    }
                )

        # Multiple data booklets / unassigned → audit (user chooses)
        data_files = sorted(rev.glob("Data and Formulae Booklet*.pdf")) + sorted(
            rev.glob("_unassigned*.pdf")
        )
        if len(data_files) > 1:
            ensure_dir(audit)
            for p in data_files:
                NEAR.append(
                    {
                        "reason": "multiple_data_booklet_or_unassigned",
                        "path": rel(p),
                        "pages": page_count(p),
                        "bytes": p.stat().st_size,
                    }
                )


def organize_computing() -> None:
    subj = RAW / "H2 computing"
    origin = subj / "origin"
    incoming = subj / "_incoming_arranged"
    if incoming.is_dir() and not origin.exists():
        incoming.rename(origin)
        ACTIONS.append(Action("rename", rel(incoming), rel(origin), "incoming → origin"))
    elif incoming.is_dir() and origin.exists():
        # merge
        for child in incoming.iterdir():
            move_to(child, origin / child.name, note="merge incoming into origin")
        incoming.rmdir()
        ACTIONS.append(Action("remove_empty", rel(incoming)))
    ensure_dir(origin)


def organize_gp() -> None:
    subj = RAW / "H1 GP"
    origin = subj / "origin"
    ensure_dir(origin)
    notes = subj / "notes"
    ensure_dir(notes)

    # Loose AQ MS at subject root → notes (working), copy originals marker into origin if needed
    for name in ("2025 AQ MS.docx", "AQ MS.docx", "Rules AQ MS.docx"):
        src = subj / name
        if not src.is_file():
            continue
        dst = notes / name
        if dst.exists():
            if sha256(src) == sha256(dst):
                src.unlink()
                ACTIONS.append(Action("delete_bitwise_dup", rel(src), rel(dst)))
            else:
                move_to(src, origin / "root_loose" / name, note="near-dupe of notes copy")
                NEAR.append(
                    {
                        "reason": "gp_root_vs_notes",
                        "a": rel(dst),
                        "b": rel(origin / "root_loose" / name),
                    }
                )
        else:
            move_to(src, dst, note="file root AQ MS into notes")


# ---------------------------------------------------------------------------
# Global bitwise dedupe within each subject (skip origin + audit)
# ---------------------------------------------------------------------------

SKIP_DIR_NAMES = {"origin", "_audit_near_dupes", "_incoming_arranged"}


def iter_files(subj: Path) -> list[Path]:
    out: list[Path] = []
    for p in subj.rglob("*"):
        if not p.is_file():
            continue
        parts = set(p.relative_to(subj).parts)
        if parts & SKIP_DIR_NAMES:
            continue
        if p.name.lower() == "desktop.ini":
            continue
        out.append(p)
    return out


def dedupe_subject(subj: Path) -> None:
    by_hash: dict[str, list[Path]] = defaultdict(list)
    for p in iter_files(subj):
        try:
            by_hash[sha256(p)].append(p)
        except OSError as exc:
            ACTIONS.append(Action("hash_fail", rel(p), None, str(exc)))

    for digest, paths in by_hash.items():
        if len(paths) < 2:
            continue
        # Prefer: under exam papers / TYS / prelim / revision without audit; shorter path; canonical name
        def score(p: Path) -> tuple:
            s = rel(p).lower()
            canon = 0
            if " - physics revision package" in s:
                canon += 50
            if "/_audit" in s:
                canon += 100
            # prefer standardised names
            if re.search(r"\d{4} .*(A-level)", p.name):
                canon -= 10
            return (canon, len(s), s)

        paths_sorted = sorted(paths, key=score)
        keep = paths_sorted[0]
        for dup in paths_sorted[1:]:
            dup.unlink()
            ACTIONS.append(
                Action(
                    "delete_bitwise_dup",
                    rel(dup),
                    rel(keep),
                    f"sha256={digest[:12]}…",
                )
            )


def find_near_dupes_by_stem(subj: Path) -> None:
    """Same stem across different folders / close size → flag if not already listed."""
    by_stem: dict[str, list[Path]] = defaultdict(list)
    for p in iter_files(subj):
        if p.suffix.lower() not in {".pdf", ".docx"}:
            continue
        by_stem[p.stem.lower()].append(p)
    for stem, paths in by_stem.items():
        if len(paths) < 2:
            continue
        # already handled if bitwise identical (would have been deleted)
        hashes = {sha256(p) for p in paths}
        if len(hashes) == 1:
            continue
        NEAR.append(
            {
                "reason": "same_stem_different_bytes",
                "subject": subj.name,
                "stem": stem,
                "paths": [
                    {
                        "path": rel(p),
                        "bytes": p.stat().st_size,
                        "pages": page_count(p) if p.suffix.lower() == ".pdf" else None,
                    }
                    for p in paths
                ],
            }
        )


def write_audit() -> None:
    ensure_dir(WORK)
    lines = [
        "# Duplicate / near-duplicate audit",
        "",
        f"Generated: {datetime.now(timezone.utc).isoformat()}",
        "",
        "Bitwise-identical duplicates were deleted (kept the preferred canonical path).",
        "Items below are **not** bit-identical — choose the higher-fidelity copy, then delete the other.",
        "",
    ]
    if not NEAR:
        lines.append("_No near-duplicates flagged._")
    else:
        for i, item in enumerate(NEAR, 1):
            lines.append(f"## {i}. {item.get('reason', 'flag')}")
            lines.append("```json")
            lines.append(json.dumps(item, indent=2))
            lines.append("```")
            lines.append("")

    AUDIT_MD.write_text("\n".join(lines) + "\n", encoding="utf-8")
    AUDIT_JSON.write_text(
        json.dumps(
            {
                "generated_at": datetime.now(timezone.utc).isoformat(),
                "actions": [asdict(a) for a in ACTIONS],
                "near_duplicates": NEAR,
            },
            indent=2,
        )
        + "\n",
        encoding="utf-8",
    )


def main() -> int:
    ensure_dir(WORK)
    organize_math()
    organize_physics()
    organize_computing()
    organize_gp()

    for name in ("H2 math", "H2 physics", "H2 computing", "H1 GP"):
        subj = RAW / name
        if subj.is_dir():
            dedupe_subject(subj)
            find_near_dupes_by_stem(subj)

    write_audit()
    print(f"Actions: {len(ACTIONS)}")
    print(f"Near-dupe flags: {len(NEAR)}")
    print(f"Audit: {AUDIT_MD}")
    print(f"Log:   {AUDIT_JSON}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
