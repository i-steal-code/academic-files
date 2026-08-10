#!/usr/bin/env python3
"""Markdown-only conversion packages for H1 GP under converted packages/.

Mirrors raw path layout. Prefer .docx over .pdf when both exist for the same stem.
No page rasters (GP is text-first per README conversion policy).
"""

from __future__ import annotations

import argparse
import hashlib
import json
import sys
import traceback
from datetime import datetime, timezone
from pathlib import Path

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

SUPPORTED = {".docx", ".pdf"}  # legacy .doc: convert to .docx first (Word); markitdown cannot read .doc
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
        return json.loads(path.read_text(encoding="utf-8"))
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
        if docs:
            # Prefer .docx over .doc
            docx = [p for p in docs if p.suffix.lower() == ".docx"]
            out.extend(docx if docx else docs)
        else:
            out.extend(pdfs)
    return sorted(out, key=lambda p: p.as_posix().lower())


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

    existing = load_manifest(manifest_path)
    if (
        not force
        and existing
        and existing.get("source_sha256") == digest
        and (pkg / "content.md").is_file()
    ):
        return "skipped"

    pkg.mkdir(parents=True, exist_ok=True)
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
        "source_ext": src.suffix.lower(),
        "kind": "gp-markdown",
        "markitdown_version": MARKITDOWN_VERSION,
        "converted_at": datetime.now(timezone.utc).isoformat(),
        "quality": {"chars": len(md_text), "warn": quality_warn},
    }
    manifest_path.write_text(json.dumps(manifest, indent=2) + "\n", encoding="utf-8")

    if quality_warn:
        print(f"  WARN {source_rel}: {', '.join(quality_warn)}")
    return "converted"


SKIP_DIR_PARTS = {"origin", "_audit_near_dupes", "_incoming_arranged"}


def iter_sources(gp_root: Path) -> list[Path]:
    def keep(p: Path) -> bool:
        if not p.is_file() or p.suffix.lower() not in SUPPORTED:
            return False
        parts = set(p.relative_to(gp_root).parts)
        if parts & SKIP_DIR_PARTS:
            return False
        return True

    candidates = [p for p in gp_root.rglob("*") if keep(p)]
    files = [p for p in candidates if p.stat().st_size <= MAX_BYTES]
    for p in candidates:
        if p.stat().st_size > MAX_BYTES:
            print(f"SKIP oversized ({p.stat().st_size / 1e6:.1f} MB): {p.name}")
    return prefer_docx(files)


def main(argv: list[str] | None = None) -> int:
    repo_default = Path(__file__).resolve().parent.parent
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--repo", type=Path, default=repo_default)
    ap.add_argument("--force", action="store_true")
    ap.add_argument("--limit", type=int, default=0)
    args = ap.parse_args(argv)

    repo_root = args.repo.resolve()
    raw_root = (repo_root / "raw files").resolve()
    gp_root = raw_root / "H1 GP"
    out_root = (repo_root / "converted packages").resolve()

    if not gp_root.is_dir():
        print(f"Missing {gp_root}", file=sys.stderr)
        return 1

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
    return 1 if counts["failed"] else 0


if __name__ == "__main__":
    raise SystemExit(main())
