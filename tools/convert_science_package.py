#!/usr/bin/env python3
"""Build hybrid science conversion packages: MarkItDown text + page PNGs + manifest.

Keeps raw PDFs as canonical sources. Sciences only (math / physics / computing).
GP should use a separate text-first markdown path.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import sys
import traceback
from datetime import datetime, timezone
from pathlib import Path
from typing import Iterable

try:
    import fitz  # PyMuPDF
except ImportError:  # pragma: no cover
    print("pymupdf is required. pip install -r tools/requirements-convert.txt", file=sys.stderr)
    raise

try:
    from markitdown import MarkItDown
except ImportError:  # pragma: no cover
    print("markitdown is required. pip install -r tools/requirements-convert.txt", file=sys.stderr)
    raise

try:
    import markitdown as _markitdown_mod

    MARKITDOWN_VERSION = getattr(_markitdown_mod, "__version__", "unknown")
except Exception:  # pragma: no cover
    MARKITDOWN_VERSION = "unknown"


DEFAULT_SUBJECTS = ("H2 math", "H2 physics", "H2 computing")
CID_RE = re.compile(r"\(cid:\d+\)")


def sha256_file(path: Path, chunk_size: int = 1024 * 1024) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        while True:
            chunk = f.read(chunk_size)
            if not chunk:
                break
            h.update(chunk)
    return h.hexdigest()


def rel_to(path: Path, base: Path) -> str:
    return path.resolve().relative_to(base.resolve()).as_posix()


def package_dir_for(pdf: Path, raw_root: Path, out_root: Path) -> Path:
    rel = pdf.resolve().relative_to(raw_root.resolve())
    return out_root / rel.parent / pdf.stem


def load_manifest(path: Path) -> dict | None:
    if not path.is_file():
        return None
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return None


def match_skip(pdf: Path, repo_root: Path, patterns: list[str]) -> bool:
    if not patterns:
        return False
    try:
        rel = pdf.resolve().relative_to(repo_root.resolve()).as_posix()
    except ValueError:
        rel = pdf.as_posix().replace("\\", "/")
    for pat in patterns:
        normalized = pat.replace("\\", "/")
        if Path(rel).match(normalized):
            return True
        # Common case from plan: **/misc/**
        if normalized in {"**/misc/**", "**/misc/*", "*/misc/*"}:
            if "/misc/" in f"/{rel}/":
                return True
        if normalized.endswith("/**") and normalized.startswith("**/"):
            mid = normalized[3:-3]
            if mid and f"/{mid}/" in f"/{rel}/":
                return True
    return False


def quality_flags(md_text: str) -> dict:
    cid_hits = len(CID_RE.findall(md_text))
    stripped = md_text.strip()
    empty_md = len(stripped) < 40
    warn: list[str] = []
    if cid_hits:
        warn.append(f"cid_hits={cid_hits}")
    if empty_md:
        warn.append("empty_or_tiny_md")
    return {"cid_hits": cid_hits, "empty_md": empty_md, "warn": warn}


def render_pages(pdf: Path, pages_dir: Path, dpi: int) -> int:
    pages_dir.mkdir(parents=True, exist_ok=True)
    # Clear stale pages when rebuilding
    for old in pages_dir.glob("page-*.png"):
        old.unlink()

    zoom = dpi / 72.0
    matrix = fitz.Matrix(zoom, zoom)
    doc = fitz.open(pdf)
    try:
        for i, page in enumerate(doc, start=1):
            pix = page.get_pixmap(matrix=matrix, alpha=False)
            out = pages_dir / f"page-{i:03d}.png"
            pix.save(out.as_posix())
        return doc.page_count
    finally:
        doc.close()


def convert_pdf(
    pdf: Path,
    *,
    repo_root: Path,
    raw_root: Path,
    out_root: Path,
    md_converter: MarkItDown,
    dpi: int,
    force: bool,
) -> str:
    """Returns status: skipped | converted | failed"""
    pkg = package_dir_for(pdf, raw_root, out_root)
    manifest_path = pkg / "manifest.json"
    source_rel = rel_to(pdf, repo_root)
    digest = sha256_file(pdf)

    existing = load_manifest(manifest_path)
    if (
        not force
        and existing
        and existing.get("source_sha256") == digest
        and existing.get("dpi") == dpi
        and (pkg / "content.md").is_file()
        and (pkg / "pages").is_dir()
    ):
        return "skipped"

    pkg.mkdir(parents=True, exist_ok=True)
    pages_dir = pkg / "pages"

    result = md_converter.convert_local(str(pdf))
    md_text = result.text_content or ""
    (pkg / "content.md").write_text(md_text, encoding="utf-8")

    page_count = render_pages(pdf, pages_dir, dpi)
    quality = quality_flags(md_text)

    manifest = {
        "source_relpath": source_rel,
        "source_sha256": digest,
        "page_count": page_count,
        "dpi": dpi,
        "markitdown_version": MARKITDOWN_VERSION,
        "converted_at": datetime.now(timezone.utc).isoformat(),
        "quality": quality,
    }
    manifest_path.write_text(json.dumps(manifest, indent=2) + "\n", encoding="utf-8")

    if quality["warn"]:
        print(f"  WARN {source_rel}: {', '.join(quality['warn'])}")
    return "converted"


def iter_pdfs(raw_root: Path, subjects: Iterable[str]) -> list[Path]:
    pdfs: list[Path] = []
    for subject in subjects:
        subject_dir = raw_root / subject
        if not subject_dir.is_dir():
            print(f"SKIP missing subject dir: {subject_dir}")
            continue
        pdfs.extend(sorted(subject_dir.rglob("*.pdf")))
    return pdfs


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    repo_default = Path(__file__).resolve().parent.parent
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--repo", type=Path, default=repo_default, help="Repository root")
    p.add_argument(
        "--root",
        type=Path,
        default=None,
        help="Raw files root (default: <repo>/raw files)",
    )
    p.add_argument(
        "--out",
        type=Path,
        default=None,
        help="Output root for packages (default: <repo>/converted packages)",
    )
    p.add_argument(
        "--subjects",
        type=str,
        default=",".join(DEFAULT_SUBJECTS),
        help="Comma-separated subject folder names under raw root",
    )
    p.add_argument(
        "--skip-glob",
        action="append",
        default=[],
        help="Glob relative to repo to skip (repeatable). Example: **/misc/**",
    )
    p.add_argument("--dpi", type=int, default=150, help="Page render DPI (default 150)")
    p.add_argument("--force", action="store_true", help="Rebuild even if SHA matches")
    p.add_argument(
        "--limit",
        type=int,
        default=0,
        help="Convert at most N PDFs (0 = no limit); useful for smoke tests",
    )
    return p.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv)
    repo_root = args.repo.resolve()
    raw_root = (args.root or (repo_root / "raw files")).resolve()
    out_root = (args.out or (repo_root / "converted packages")).resolve()
    subjects = [s.strip() for s in args.subjects.split(",") if s.strip()]
    skip_globs = args.skip_glob or []

    if not raw_root.is_dir():
        print(f"Raw root not found: {raw_root}", file=sys.stderr)
        return 1

    pdfs = iter_pdfs(raw_root, subjects)
    if skip_globs:
        pdfs = [p for p in pdfs if not match_skip(p, repo_root, skip_globs)]
    if args.limit > 0:
        pdfs = pdfs[: args.limit]

    print(f"Repo:      {repo_root}")
    print(f"Raw root:  {raw_root}")
    print(f"Out root:  {out_root}")
    print(f"Subjects:  {subjects}")
    print(f"PDFs:      {len(pdfs)}")
    print(f"DPI:       {args.dpi}")
    print(f"Skip:      {skip_globs or '(none)'}")

    md_converter = MarkItDown(enable_plugins=False)
    counts = {"converted": 0, "skipped": 0, "failed": 0}

    for i, pdf in enumerate(pdfs, start=1):
        rel = rel_to(pdf, repo_root)
        print(f"[{i}/{len(pdfs)}] {rel}")
        try:
            status = convert_pdf(
                pdf,
                repo_root=repo_root,
                raw_root=raw_root,
                out_root=out_root,
                md_converter=md_converter,
                dpi=args.dpi,
                force=args.force,
            )
            counts[status] += 1
            print(f"  -> {status}")
        except Exception as exc:  # noqa: BLE001 — batch must continue
            counts["failed"] += 1
            print(f"  -> failed: {exc}")
            traceback.print_exc()

    print(
        "Done: "
        f"converted={counts['converted']} "
        f"skipped={counts['skipped']} "
        f"failed={counts['failed']}"
    )
    return 1 if counts["failed"] else 0


if __name__ == "__main__":
    raise SystemExit(main())
