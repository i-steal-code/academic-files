#!/usr/bin/env python3
"""Markdown-only conversion packages for H1 GP under converted packages/.

Mirrors raw path layout. Prefer .docx over .pdf when both exist for the same stem.
No page rasters (GP is text-first per README conversion policy).
"""

from __future__ import annotations

import argparse
import hashlib
import json
import shutil
import sys
import traceback
from datetime import datetime, timezone
from pathlib import Path

try:
    import fitz  # PyMuPDF
except ImportError:  # pragma: no cover
    fitz = None  # type: ignore[assignment]

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

SUPPORTED = {".docx", ".pdf", ".md"}  # legacy .doc: convert to .docx first (Word); markitdown cannot read .doc
# Skip pathological scans (e.g. 2020 KS Bull Issue 1.pdf ~102MB, also gitignored)
MAX_BYTES = 40 * 1024 * 1024


def sha256_file(path: Path, chunk_size: int = 1 << 20) -> str:
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


def package_dir_for(src: Path, raw_root: Path, out_root: Path) -> Path:
    rel = src.resolve().relative_to(raw_root.resolve())
    return out_root / rel.parent / src.stem


def load_manifest(path: Path) -> dict | None:
    if not path.is_file():
        return None
    try:
        return json.loads(path.read_text(encoding="utf-8-sig"))
    except (OSError, json.JSONDecodeError):
        return None


def prefer_docx(files: list[Path]) -> list[Path]:
    """If stem has both docx and pdf (or doc), keep docx/doc and drop pdf."""
    by_key: dict[tuple[str, str], list[Path]] = {}
    for f in files:
        key = (f.parent.as_posix().lower(), f.stem.lower())
        by_key.setdefault(key, []).append(f)

    out: list[Path] = []
    for group in by_key.values():
        docs = [p for p in group if p.suffix.lower() in {".docx", ".doc"}]
        pdfs = [p for p in group if p.suffix.lower() == ".pdf"]
        mds = [p for p in group if p.suffix.lower() == ".md"]
        if docs:
            # Prefer .docx over .doc
            docx = [p for p in docs if p.suffix.lower() == ".docx"]
            out.extend(docx if docx else docs)
        elif pdfs:
            out.extend(pdfs)
        else:
            out.extend(mds)
    return sorted(out, key=lambda p: p.as_posix().lower())


PDF_EXTRACT_MODE = "pdf_text_only"


def extract_pdf_text_only(src: Path) -> str:
    """Extract printable text from a PDF; images and image metadata are skipped."""
    if fitz is None:
        raise RuntimeError("pymupdf is required for PDF conversion. pip install -r tools/requirements-convert.txt")
    parts: list[str] = []
    with fitz.open(src) as doc:
        for page in doc:
            text = page.get_text("text").strip()
            if text:
                parts.append(text)
    return "\n\n".join(parts).strip()


def read_markdown_source(src: Path) -> str:
    return src.read_text(encoding="utf-8", errors="replace").strip()


def convert_one(
    src: Path,
    *,
    repo_root: Path,
    raw_root: Path,
    out_root: Path,
    md_converter: MarkItDown,
    force: bool,
) -> str:
    pkg = package_dir_for(src, raw_root, out_root)
    manifest_path = pkg / "manifest.json"
    source_rel = rel_to(src, repo_root)
    digest = sha256_file(src)
    ext = src.suffix.lower()

    existing = load_manifest(manifest_path)
    extract_mode = PDF_EXTRACT_MODE if ext == ".pdf" else None
    if (
        not force
        and existing
        and existing.get("source_sha256") == digest
        and (pkg / "content.md").is_file()
        and (ext != ".pdf" or existing.get("extract_mode") == extract_mode)
    ):
        return "skipped"

    pkg.mkdir(parents=True, exist_ok=True)
    if ext == ".md":
        md_text = read_markdown_source(src)
    elif ext == ".pdf":
        md_text = extract_pdf_text_only(src)
    else:
        result = md_converter.convert(str(src))
        md_text = (result.text_content or "").strip()
    if not md_text:
        md_text = ""
    (pkg / "content.md").write_text(md_text + ("\n" if md_text else ""), encoding="utf-8")

    quality_warn: list[str] = []
    if len(md_text) < 40:
        quality_warn.append("empty_or_tiny_md")

    manifest = {
        "source_relpath": source_rel,
        "source_sha256": digest,
        "source_ext": ext,
        "kind": "gp-markdown",
        "markitdown_version": MARKITDOWN_VERSION,
        "converted_at": datetime.now(timezone.utc).isoformat(),
        "quality": {"chars": len(md_text), "warn": quality_warn},
    }
    if extract_mode:
        manifest["extract_mode"] = extract_mode
    manifest_path.write_text(json.dumps(manifest, indent=2) + "\n", encoding="utf-8")

    if quality_warn:
        print(f"  WARN {source_rel}: {', '.join(quality_warn)}")
    return "converted"


SKIP_DIR_PARTS = {"origin", "_audit_near_dupes", "_incoming_arranged"}


def iter_sources(gp_root: Path, *, include_oversized: bool = False) -> list[Path]:
    def keep(p: Path) -> bool:
        if not p.is_file() or p.suffix.lower() not in SUPPORTED:
            return False
        parts = set(p.relative_to(gp_root).parts)
        if parts & SKIP_DIR_PARTS:
            return False
        return True

    candidates = [p for p in gp_root.rglob("*") if keep(p)]
    if include_oversized:
        files = candidates
    else:
        files = [p for p in candidates if p.stat().st_size <= MAX_BYTES]
        for p in candidates:
            if p.stat().st_size > MAX_BYTES:
                print(f"SKIP oversized ({p.stat().st_size / 1e6:.1f} MB): {p.name}")
    return prefer_docx(files)


def expected_package_dirs(sources: list[Path], raw_root: Path, out_root: Path) -> set[Path]:
    return {package_dir_for(src, raw_root, out_root).resolve() for src in sources}


def _rmtree(path: Path) -> None:
    def onerror(func, p, exc_info):  # noqa: ANN001
        # Clear read-only files (common on Windows / OneDrive).
        import os
        import stat

        if not os.path.exists(p):
            return
        os.chmod(p, stat.S_IWRITE)
        func(p)

    shutil.rmtree(path, onexc=onerror)


def prune_orphans(
    *,
    gp_root: Path,
    raw_root: Path,
    out_root: Path,
    apply: bool,
) -> list[Path]:
    """Remove converted packages whose raw source no longer exists."""
    # Include oversized sources so we keep existing packages for local-only giants.
    sources = iter_sources(gp_root, include_oversized=True)
    expected = expected_package_dirs(sources, raw_root, out_root)
    orphans: list[Path] = []
    gp_out = out_root / "H1 GP"
    if not gp_out.is_dir():
        return orphans

    for manifest in gp_out.rglob("manifest.json"):
        pkg = manifest.parent.resolve()
        if pkg not in expected:
            orphans.append(pkg)

    orphans.sort(key=lambda p: p.as_posix().lower())
    for pkg in orphans:
        rel = pkg.relative_to(out_root.resolve())
        if apply:
            _rmtree(pkg)
            print(f"PRUNED {rel.as_posix()}")
        else:
            print(f"ORPHAN {rel.as_posix()}")
    return orphans


def validate_packages(
    *,
    gp_root: Path,
    raw_root: Path,
    out_root: Path,
    repo_root: Path,
) -> int:
    sources = iter_sources(gp_root, include_oversized=True)
    convert_sources = iter_sources(gp_root, include_oversized=False)
    expected = expected_package_dirs(sources, raw_root, out_root)
    convert_expected = expected_package_dirs(convert_sources, raw_root, out_root)
    errors: list[str] = []

    for src in convert_sources:
        pkg = package_dir_for(src, raw_root, out_root)
        content = pkg / "content.md"
        manifest_path = pkg / "manifest.json"
        rel = rel_to(src, repo_root)
        if not content.is_file():
            errors.append(f"missing content.md for {rel}")
            continue
        manifest = load_manifest(manifest_path)
        if not manifest:
            errors.append(f"missing manifest for {rel}")
            continue
        digest = sha256_file(src)
        if manifest.get("source_sha256") != digest:
            errors.append(f"stale manifest for {rel}")
        if manifest.get("source_relpath") != rel:
            errors.append(f"manifest path mismatch for {rel}")

    for manifest in (out_root / "H1 GP").rglob("manifest.json"):
        pkg = manifest.parent.resolve()
        if pkg not in expected:
            errors.append(f"orphan package {pkg.relative_to(out_root.resolve()).as_posix()}")

    for pkg in convert_expected:
        if not (pkg / "content.md").is_file():
            rel = pkg.relative_to(out_root.resolve()).as_posix()
            errors.append(f"missing package {rel}")

    print(
        f"validate: sources={len(sources)} "
        f"convert={len(convert_sources)} "
        f"packages={len(list((out_root / 'H1 GP').rglob('manifest.json'))) if (out_root / 'H1 GP').is_dir() else 0}"
    )
    if errors:
        print(f"FAIL ({len(errors)} issues):")
        for err in errors[:40]:
            print(f"  - {err}")
        if len(errors) > 40:
            print(f"  ... and {len(errors) - 40} more")
        return 1
    print("OK: raw and converted packages are in sync")
    return 0


def main(argv: list[str] | None = None) -> int:
    repo_default = Path(__file__).resolve().parent.parent
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--repo", type=Path, default=repo_default)
    ap.add_argument("--force", action="store_true")
    ap.add_argument("--limit", type=int, default=0)
    ap.add_argument("--prune", action="store_true", help="Remove converted packages with no raw source")
    ap.add_argument("--validate", action="store_true", help="Check raw/converted parity and exit")
    args = ap.parse_args(argv)

    repo_root = args.repo.resolve()
    raw_root = (repo_root / "raw files").resolve()
    gp_root = raw_root / "H1 GP"
    out_root = (repo_root / "converted packages").resolve()

    if not gp_root.is_dir():
        print(f"Missing {gp_root}", file=sys.stderr)
        return 1

    if args.validate:
        return validate_packages(
            gp_root=gp_root,
            raw_root=raw_root,
            out_root=out_root,
            repo_root=repo_root,
        )

    if args.prune:
        orphans = prune_orphans(
            gp_root=gp_root,
            raw_root=raw_root,
            out_root=out_root,
            apply=True,
        )
        print(f"Pruned {len(orphans)} orphan package(s)")

    sources = iter_sources(gp_root)
    if args.limit > 0:
        sources = sources[: args.limit]

    print(f"Repo:     {repo_root}")
    print(f"GP root:  {gp_root}")
    print(f"Out root: {out_root}")
    print(f"Sources:  {len(sources)} (docx preferred over pdf for same stem)")

    md_converter = MarkItDown(enable_plugins=False)
    counts = {"converted": 0, "skipped": 0, "failed": 0}

    for i, src in enumerate(sources, start=1):
        rel = rel_to(src, repo_root)
        print(f"[{i}/{len(sources)}] {rel}")
        try:
            status = convert_one(
                src,
                repo_root=repo_root,
                raw_root=raw_root,
                out_root=out_root,
                md_converter=md_converter,
                force=args.force,
            )
            counts[status] += 1
            print(f"  -> {status}")
        except Exception as exc:  # noqa: BLE001
            counts["failed"] += 1
            print(f"  -> failed: {exc}")
            traceback.print_exc()

    print(
        "Done: "
        f"converted={counts['converted']} "
        f"skipped={counts['skipped']} "
        f"failed={counts['failed']}"
    )
    rc = 1 if counts["failed"] else 0
    if rc == 0:
        rc = validate_packages(
            gp_root=gp_root,
            raw_root=raw_root,
            out_root=out_root,
            repo_root=repo_root,
        )
    return rc


if __name__ == "__main__":
    raise SystemExit(main())
