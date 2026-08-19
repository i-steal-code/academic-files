#!/usr/bin/env python3
"""Normalize newly imported H2 computing notes, references, and school papers."""

from __future__ import annotations

import hashlib
import shutil
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
COMP = REPO / "raw files" / "H2 computing"
BASE = COMP / "base syllabus"
OTHER = COMP / "Past Exam Papers from Other Schools"
PRELIM = COMP / "prelim QP"


def ensure(path: Path) -> Path:
    path.mkdir(parents=True, exist_ok=True)
    return path


def move(src: Path, dst: Path) -> None:
    if not src.exists():
        return
    ensure(dst.parent)
    if dst.exists():
        if src.is_file() and dst.is_file() and sha256(src) == sha256(dst):
            src.unlink()
            print(f"DEDUP {src.relative_to(REPO)}")
            return
        raise FileExistsError(f"destination exists: {dst}")
    shutil.move(str(src), str(dst))
    print(f"MOVE  {src.relative_to(REPO)} -> {dst.relative_to(REPO)}")


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def move_contents(src: Path, dst: Path) -> None:
    if not src.is_dir():
        return
    ensure(dst)
    for child in list(src.iterdir()):
        move(child, dst / child.name)
    try:
        src.rmdir()
    except PermissionError:
        # OneDrive can briefly lock emptied directories; harmless to leave empty.
        print(f"EMPTY (locked) {src.relative_to(REPO)}")


def normalize_theory() -> None:
    ensure(BASE)
    for name in (
        "S1 Algorithms and Data Structures",
        "S2 Programming",
        "S3 Data and Information",
        "S4 Computer Networks",
    ):
        move(COMP / name, BASE / name)

    renames = {
        BASE / "S1 Algorithms and Data Structures" / "S1A Algo Representation"
        / "2025 Chapter S1A Algo Rep (Student).pdf":
        BASE / "S1 Algorithms and Data Structures" / "S1A Algo Representation"
        / "2025 Chapter S1A Algo Representation.pdf",
        BASE / "S1 Algorithms and Data Structures" / "S1A Algo Representation"
        / "2025 Chapter S1A Algo Rep Tutorial (Student).pdf":
        BASE / "S1 Algorithms and Data Structures" / "S1A Algo Representation"
        / "2025 Chapter S1A Algo Representation Tutorial.pdf",
        BASE / "S3 Data and Information" / "S3A Data Representation"
        / "2025 Chapter S3A Data Representations Tutorial Solutions.pdf":
        BASE / "S3 Data and Information" / "S3A Data Representation"
        / "2025 Chapter S3A Data Representation Tutorial Solutions.pdf",
        BASE / "S3 Data and Information" / "S3D Python SQLite"
        / "2026 Chapter S3D Python Sqlite.pdf":
        BASE / "S3 Data and Information" / "S3D Python SQLite"
        / "2026 Chapter S3D Python SQLite.pdf",
        BASE / "S4 Computer Networks" / "S4F Networks" / "Tutorial Slides.pdf":
        BASE / "S4 Computer Networks" / "S4F Networks"
        / "2026 Chapter S4F Networks Tutorial Slides.pdf",
        BASE / "S4 Computer Networks" / "S4G Network Security" / "Tutorial Slides.pdf":
        BASE / "S4 Computer Networks" / "S4G Network Security"
        / "2026 Chapter S4G Network Security Tutorial Slides.pdf",
    }
    for src, dst in renames.items():
        move(src, dst)

    # Tuck loose programming/data assets into explicit resource folders.
    for chapter in ("S1G Hash Table", "S1H Binary Search Tree"):
        folder = BASE / "S1 Algorithms and Data Structures" / chapter
        resources = ensure(folder / "Programming Exercise Sample Codes")
        for file in list(folder.glob("*.py")):
            move(file, resources / file.name)

    sql = BASE / "S3 Data and Information" / "S3C Structured Query Language"
    resources = ensure(sql / "Resource Files")
    for suffix in ("*.csv", "*.db"):
        for file in list(sql.glob(suffix)):
            move(file, resources / file.name)


def normalize_references() -> None:
    refs = ensure(BASE / "reference documents")
    pseudo = COMP / "A lvls pseudocode documentation.pdf"
    quick = COMP / "Quick Reference Guide (for A-level exam) (1).pdf"
    move(pseudo, refs / "A-level pseudocode documentation.pdf")
    move(quick, refs / "Quick Reference Guide for A-level exam.pdf")

    duplicate = REPO / "computing practical" / "Quick Reference Guide (for A-level exam) (1).pdf"
    canonical = refs / "Quick Reference Guide for A-level exam.pdf"
    if duplicate.is_file() and canonical.is_file() and sha256(duplicate) == sha256(canonical):
        duplicate.unlink()
        print(f"DEDUP {duplicate.relative_to(REPO)}")


def p2_package(
    root: Path,
    stem: str,
    paper: Path,
    resources: Path | None = None,
    solutions: Path | None = None,
) -> None:
    package = ensure(root / stem)
    move(paper, package / f"{stem}.pdf")
    if resources and resources.is_dir():
        move_contents(resources, ensure(package / "resource files"))
    if solutions and solutions.is_dir():
        move_contents(solutions, ensure(package / "solutions"))


def normalize_other_schools() -> None:
    # ACJC
    folder = OTHER / "2022 ACJC"
    move(folder / "2022 ACJC TA Paper 1 (QP).pdf", folder / "2022 ACJC TA P1 QP.pdf")
    move(folder / "2022 ACJC TA Suggested Solutions.pdf", folder / "2022 ACJC TA P1 ANS.pdf")

    # JPJC
    folder = OTHER / "2022 JPJC"
    move(folder / "2022 JPJC MYE P1 (QP).pdf", folder / "2022 JPJC MYE P1 QP.pdf")
    move(folder / "2022 JPJC MYE P1 (solution).pdf", folder / "2022 JPJC MYE P1 ANS.pdf")
    p2_package(
        folder,
        "2022 JPJC MYE P2",
        folder / "2022 JPJC MYE P2 (QP).pdf",
        folder / "Resource Files",
    )

    # RVHS
    folder = OTHER / "2022 RVHS"
    move(folder / "2022_JC2_CT3_P1_combined.pdf", folder / "2022 RVHS CT3 P1 QP.pdf")
    move(folder / "2022_JC2_CT3_P1_combined_sol.pdf", folder / "2022 RVHS CT3 P1 ANS.pdf")
    p2_package(
        folder,
        "2022 RVHS CT3 P2",
        folder / "2022_JC2_CT3_P2_combined.pdf",
        folder / "Resource Files",
        folder / "2022 JC2 CT3 P2 Solutions",
    )

    # VJC CT1 and CT2
    folder = OTHER / "2022 VJC"
    for assessment in ("CT1", "CT2"):
        src = folder / f"2022 VJC {assessment}"
        if not src.is_dir():
            continue
        move(src / f"2022 VJC {assessment} P1 (QP).pdf", src / f"2022 VJC {assessment} P1 QP.pdf")
        move(src / f"2022 VJC {assessment} P1 (MS).pdf", src / f"2022 VJC {assessment} P1 ANS.pdf")
        p2_package(
            src,
            f"2022 VJC {assessment} P2",
            src / f"2022 VJC {assessment} P2 (QP).pdf",
            src / "Resource Files",
            src / f"2022 VJC {assessment} P2 (sample code)",
        )
        ans = src / f"2022 VJC {assessment} P2 (MS).pdf"
        if ans.is_file():
            move(ans, src / f"2022 VJC {assessment} P2" / f"2022 VJC {assessment} P2 ANS.pdf")

    # YIJC
    folder = OTHER / "2022 YIJC"
    move(folder / "YIJC J2 MYE Paper 1.pdf", folder / "2022 YIJC MYE P1 QP.pdf")
    move(folder / "YIJC J2 MYE Paper 1 Solutions.pdf", folder / "2022 YIJC MYE P1 ANS.pdf")
    duplicate_q6 = folder / "thumb drive" / "Q6. Socket Programming Folder"
    canonical_q6 = folder / "thumb drive" / "Q6 Socket Programming Folder"
    if duplicate_q6.is_dir() and canonical_q6.is_dir():
        duplicate_files = sorted(
            (p.relative_to(duplicate_q6), sha256(p))
            for p in duplicate_q6.rglob("*") if p.is_file()
        )
        canonical_files = sorted(
            (p.relative_to(canonical_q6), sha256(p))
            for p in canonical_q6.rglob("*") if p.is_file()
        )
        if duplicate_files == canonical_files:
            try:
                shutil.rmtree(duplicate_q6)
                print(f"DEDUP {duplicate_q6.relative_to(REPO)}")
            except PermissionError:
                print(f"DEDUP contents; empty folder locked {duplicate_q6.relative_to(REPO)}")
    p2_package(
        folder,
        "2022 YIJC MYE P2",
        folder / "YIJC J2 MYE Paper 2.pdf",
        folder / "thumb drive",
        folder / "YIJC J2 MYE Paper 2 Solutions",
    )

    # HCI prelims belong with the existing canonical prelim QP collection.
    for year in (2023, 2024):
        folder = OTHER / f"{year} HCI"
        if not folder.is_dir():
            continue
        move(
            folder / f"{year} HCI Prelim Paper 1",
            PRELIM / f"{year} HCI P1 prelim H2 computing.pdf",
        )
        package = PRELIM / f"{year} HCI P2 prelim H2 computing"
        ensure(package)
        move(
            folder / f"{year} HCI Prelim Paper 2",
            package / f"{year} HCI P2 prelim H2 computing.pdf",
        )
        move_contents(folder / "Resource Files", ensure(package / "resource files"))
        if not any(folder.iterdir()):
            try:
                folder.rmdir()
            except PermissionError:
                print(f"EMPTY (locked) {folder.relative_to(REPO)}")

    # 2025 prelims retained under Other Schools, normalized to the same package shape.
    folder = OTHER / "2025 ASRJC"
    move(folder / "2025 ASRJC Prelim Theory P1", folder / "2025 ASRJC P1 prelim H2 computing.pdf")
    p2_package(
        folder,
        "2025 ASRJC P2 prelim H2 computing",
        folder / "2025 ASRJC Prelim Practical P2",
        folder / "Resource Files",
        folder / "Solutions for Practical",
    )

    folder = OTHER / "2025 NJC"
    p2_package(
        folder,
        "2025 NJC P2 prelim H2 computing",
        folder / "NJC Prelim 2025 Paper 2.pdf",
        folder / "Resource Files",
    )

    folder = OTHER / "2025 VJC"
    move(folder / "2025 VJC Prelim P1", folder / "2025 VJC P1 prelim H2 computing.pdf")
    p2_package(
        folder,
        "2025 VJC P2 prelim H2 computing",
        folder / "2025 VJC Prelim P2",
        folder / "Resource Files",
        folder / "Solutions for Practical",
    )


def main() -> int:
    normalize_theory()
    normalize_references()
    normalize_other_schools()
    print("Computing resources normalized.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
