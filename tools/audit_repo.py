#!/usr/bin/env python3
"""Audit converted packages vs raw sources; check in-repo path references.

Reports:
  - orphan packages (no raw source)
  - missing packages (raw exists, no package)
  - stale manifests (sha mismatch)
  - incomplete science packages (missing content.md / pages / page count)
  - broken relative links and backtick path refs in markdown/README/tools docs

Does not modify files unless --fix-gp / --prune-orphans is passed.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import shutil
import sys
from collections import defaultdict
from datetime import datetime, timezone
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
RAW = REPO / "raw files"
CONV = REPO / "converted packages"

SKIP_DIR_PARTS = {
    "origin",
    "_audit_near_dupes",
    "_incoming_arranged",
    "tuition material",
}
# Converted by policy only when explicitly requested (convert_one.ps1 -SkipMisc default)
POLICY_SKIP_DIR_NAMES = {"misc"}
POLICY_SKIP_PATH_SUBSTR = (
    "/practical worksheets",
    "\\practical worksheets",
)
SCIENCE_SUBJECTS = {"H2 math", "H2 physics", "H2 computing"}
GP_SUBJECT = "H1 GP"
SCIENCE_EXTS = {".pdf"}
GP_EXTS = {".pdf", ".docx", ".md"}
MAX_GP_BYTES = 40 * 1024 * 1024

MD_LINK_RE = re.compile(r"\[([^\]]*)\]\(([^)]+)\)")
BACKTICK_PATH_RE = re.compile(
    r"`((?:raw files|converted packages|tools|computing practical)/[^`\n]+)`"
)


def sha256_file(path: Path, chunk_size: int = 1 << 20) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        while True:
            chunk = f.read(chunk_size)
            if not chunk:
                break
            h.update(chunk)
    return h.hexdigest()


def should_skip(path: Path, root: Path) -> bool:
    parts = set(path.relative_to(root).parts)
    return bool(parts & SKIP_DIR_PARTS)


def package_dir_for(src: Path) -> Path:
    rel = src.resolve().relative_to(RAW.resolve())
    return CONV / rel.parent / src.stem


def prefer_docx(files: list[Path]) -> list[Path]:
    by_key: dict[tuple[str, str], list[Path]] = defaultdict(list)
    for f in files:
        key = (f.parent.as_posix().lower(), f.stem.lower())
        by_key[key].append(f)
    out: list[Path] = []
    for group in by_key.values():
        docs = [p for p in group if p.suffix.lower() in {".docx", ".doc"}]
        pdfs = [p for p in group if p.suffix.lower() == ".pdf"]
        mds = [p for p in group if p.suffix.lower() == ".md"]
        if docs:
            docx = [p for p in docs if p.suffix.lower() == ".docx"]
            out.extend(docx if docx else docs)
        elif pdfs:
            out.extend(pdfs)
        else:
            out.extend(mds)
    return out


def iter_science_sources() -> list[Path]:
    files: list[Path] = []
    for subj in SCIENCE_SUBJECTS:
        root = RAW / subj
        if not root.is_dir():
            continue
        for p in root.rglob("*.pdf"):
            if should_skip(p, root):
                continue
            files.append(p)
    return sorted(files, key=lambda p: p.as_posix().lower())


def iter_gp_sources(*, include_oversized: bool = False) -> list[Path]:
    root = RAW / GP_SUBJECT
    if not root.is_dir():
        return []
    cands = [
        p
        for p in root.rglob("*")
        if p.is_file() and p.suffix.lower() in GP_EXTS and not should_skip(p, root)
    ]
    if not include_oversized:
        cands = [p for p in cands if p.stat().st_size <= MAX_GP_BYTES]
    return sorted(prefer_docx(cands), key=lambda p: p.as_posix().lower())


def load_manifest(path: Path) -> dict | None:
    if not path.is_file():
        return None
    try:
        # utf-8-sig strips BOM written by some PowerShell JSON dumps
        return json.loads(path.read_text(encoding="utf-8-sig"))
    except (OSError, json.JSONDecodeError):
        return None


def is_policy_skipped(src: Path) -> bool:
    """misc/ and practical-worksheet dumps are optional (SkipMisc default)."""
    try:
        rel = "/" + src.relative_to(RAW).as_posix().lower() + "/"
        parts = {p.lower() for p in src.relative_to(RAW).parts}
    except ValueError:
        return False
    if parts & {p.lower() for p in POLICY_SKIP_DIR_NAMES}:
        return True
    for sub in POLICY_SKIP_PATH_SUBSTR:
        needle = sub.replace("\\", "/").lower()
        if needle in rel:
            return True
    return False


def audit_packages() -> dict:
    science_all = iter_science_sources()
    science = [p for p in science_all if not is_policy_skipped(p)]
    science_skipped = [p for p in science_all if is_policy_skipped(p)]
    gp = iter_gp_sources(include_oversized=True)
    gp_convert = iter_gp_sources(include_oversized=False)
    expected = {package_dir_for(p).resolve() for p in science + gp}
    convert_expected = {package_dir_for(p).resolve() for p in science + gp_convert}

    issues: dict[str, list] = defaultdict(list)
    ok_packages = 0

    # Orphans (packages whose raw source is gone — including policy-skipped raw still OK)
    expected_including_skipped = {
        package_dir_for(p).resolve() for p in science_all + gp
    }
    if CONV.is_dir():
        for manifest in CONV.rglob("manifest.json"):
            pkg = manifest.parent.resolve()
            if pkg not in expected_including_skipped:
                issues["orphan_packages"].append(
                    pkg.relative_to(REPO).as_posix()
                )

    # Missing / stale / incomplete (policy-required sources only)
    for src in science + gp_convert:
        pkg = package_dir_for(src)
        rel_src = src.relative_to(REPO).as_posix()
        rel_pkg = pkg.relative_to(REPO).as_posix()
        content = pkg / "content.md"
        manifest_path = pkg / "manifest.json"
        if not content.is_file() or not manifest_path.is_file():
            issues["missing_packages"].append(rel_src)
            continue
        man = load_manifest(manifest_path)
        if not man:
            issues["bad_manifest"].append(rel_pkg)
            continue
        digest = sha256_file(src)
        if man.get("source_sha256") != digest:
            issues["stale_sha"].append(
                {
                    "source": rel_src,
                    "package": rel_pkg,
                    "manifest_sha": man.get("source_sha256"),
                }
            )
        expected_rel = src.relative_to(REPO).as_posix()
        # Normalize path separators in manifests
        man_path = (man.get("source_relpath") or "").replace("\\", "/")
        if man_path and man_path != expected_rel:
            issues["path_mismatch"].append(
                {"source": rel_src, "manifest_path": man.get("source_relpath")}
            )

        subj = src.relative_to(RAW).parts[0] if src.is_relative_to(RAW) else ""
        if subj in SCIENCE_SUBJECTS:
            pages_dir = pkg / "pages"
            page_count = man.get("page_count")
            if page_count is None:
                page_count = man.get("pages") or man.get("quality", {}).get("pages")
            pngs = sorted(pages_dir.glob("page-*.png")) if pages_dir.is_dir() else []
            if not pages_dir.is_dir() or not pngs:
                issues["science_missing_pages"].append(rel_pkg)
            elif page_count and int(page_count) != len(pngs):
                issues["science_page_count_mismatch"].append(
                    {
                        "package": rel_pkg,
                        "manifest_pages": page_count,
                        "png_count": len(pngs),
                    }
                )
        ok_packages += 1

    return {
        "science_sources_required": len(science),
        "science_sources_policy_skipped": len(science_skipped),
        "gp_sources": len(gp),
        "gp_convert_sources": len(gp_convert),
        "ok_packages_checked": ok_packages,
        "expected_packages": len(convert_expected),
        "policy_skipped_examples": [
            p.relative_to(REPO).as_posix() for p in science_skipped[:8]
        ],
        "issues": {k: v for k, v in issues.items() if v},
        "issue_counts": {k: len(v) for k, v in issues.items() if v},
    }


def resolve_link(base_file: Path, target: str) -> Path | None:
    t = target.strip()
    if not t or t.startswith(("http://", "https://", "mailto:", "#")):
        return None
    # strip anchors / titles
    t = t.split()[0].strip("<>\"'")
    t = t.split("#")[0]
    if not t:
        return None
    # URL-decode light
    t = t.replace("%20", " ")
    cand = (base_file.parent / t).resolve()
    try:
        cand.relative_to(REPO.resolve())
    except ValueError:
        # allow absolute-from-repo style
        cand2 = (REPO / t).resolve()
        try:
            cand2.relative_to(REPO.resolve())
            return cand2
        except ValueError:
            return cand
    return cand


def audit_links() -> dict:
    broken: list[dict] = []
    checked = 0
    roots = [
        REPO / "README.md",
        REPO / "tools",
        REPO / "raw files" / "H1 GP",
        REPO / "raw files" / "H2 physics" / "revision packages" / "README.md",
        REPO / "raw files" / "H2 physics" / "blurt sheets",
        REPO / "raw files" / "H2 computing" / "blurt sheets",
    ]
    files: list[Path] = []
    for r in roots:
        if r.is_file() and r.suffix.lower() == ".md":
            files.append(r)
        elif r.is_dir():
            files.extend(p for p in r.rglob("*.md") if p.is_file())
            files.extend(p for p in r.rglob("*.py") if p.is_file() and "origin" not in p.parts)

    # Also check tool path mentions that look like concrete files
    for path in files:
        try:
            text = path.read_text(encoding="utf-8", errors="replace")
        except OSError:
            continue
        # markdown links
        for m in MD_LINK_RE.finditer(text):
            target = m.group(2)
            resolved = resolve_link(path, target)
            if resolved is None:
                continue
            checked += 1
            if not resolved.exists():
                broken.append(
                    {
                        "file": path.relative_to(REPO).as_posix(),
                        "kind": "md_link",
                        "target": target,
                        "resolved": str(resolved),
                    }
                )
        # backtick paths from repo root
        for m in BACKTICK_PATH_RE.finditer(text):
            target = m.group(1).rstrip("/")
            # skip globs / ellipsis
            if "*" in target or "…" in target or "..." in target:
                continue
            # skip directory-only mentions that are known roots
            checked += 1
            cand = (REPO / target).resolve()
            if not cand.exists():
                # allow stem references like tools/foo.py when documented as module
                broken.append(
                    {
                        "file": path.relative_to(REPO).as_posix(),
                        "kind": "backtick_path",
                        "target": target,
                    }
                )

    # Essay arsenal cross-refs like `01`, `05 - Paper 1 house model.md`, `06`, `07`
    arsenal = REPO / "raw files" / "H1 GP" / "essay arsenal"
    if arsenal.is_dir():
        present = {p.name for p in arsenal.glob("*.md")}
        stems = {p.stem for p in arsenal.glob("*.md")}
        # numbered refs
        for md in arsenal.glob("*.md"):
            text = md.read_text(encoding="utf-8", errors="replace")
            for m in re.finditer(r"`(\d{2}(?:\s*-\s*[^`]+)?\.md|\d{2})`", text):
                ref = m.group(1)
                checked += 1
                if ref.endswith(".md"):
                    if ref not in present:
                        broken.append(
                            {
                                "file": md.relative_to(REPO).as_posix(),
                                "kind": "arsenal_ref",
                                "target": ref,
                            }
                        )
                else:
                    # bare number like 01, 06
                    if not any(s.startswith(ref) for s in stems):
                        broken.append(
                            {
                                "file": md.relative_to(REPO).as_posix(),
                                "kind": "arsenal_ref",
                                "target": ref,
                            }
                        )

    # Concrete tool scripts referenced in README
    for tool in [
        "tools/reorg_subjects_origin_dedupe.py",
        "tools/convert_gp_package.py",
        "tools/convert_one.ps1",
        "tools/rebuild_physics_revision_packages.py",
        "tools/resplit_math_ri_prelims.py",
        "tools/reorg_gp_tuition.py",
        "tools/convert_science_package.py",
        "tools/requirements-convert.txt",
    ]:
        checked += 1
        if not (REPO / tool).is_file():
            broken.append({"file": "README.md", "kind": "tool_path", "target": tool})

    return {"checked": checked, "broken": broken, "broken_count": len(broken)}


def prune_orphans(orphans: list[str]) -> int:
    n = 0
    for rel in orphans:
        pkg = REPO / rel
        if pkg.is_dir():
            shutil.rmtree(pkg, ignore_errors=True)
            n += 1
            print(f"PRUNED {rel}")
    return n


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--json-out", type=Path, default=None)
    ap.add_argument("--prune-orphans", action="store_true")
    args = ap.parse_args()

    print("Auditing converted packages…")
    pkg = audit_packages()
    print(
        f"  science_required={pkg['science_sources_required']} "
        f"science_skipped={pkg['science_sources_policy_skipped']} "
        f"gp={pkg['gp_sources']} "
        f"(convertible={pkg['gp_convert_sources']}) "
        f"checked={pkg['ok_packages_checked']}"
    )
    for k, n in sorted(pkg["issue_counts"].items()):
        print(f"  ISSUE {k}: {n}")

    print("Auditing in-repo links…")
    links = audit_links()
    print(f"  checked={links['checked']} broken={links['broken_count']}")
    for b in links["broken"][:40]:
        print(f"  BROKEN {b['kind']}: {b.get('target')}  (from {b['file']})")
    if links["broken_count"] > 40:
        print(f"  ... and {links['broken_count'] - 40} more")

    if args.prune_orphans:
        orphans = pkg["issues"].get("orphan_packages", [])
        prune_orphans(orphans)

    report = {
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "packages": pkg,
        "links": links,
    }
    out = args.json_out or (REPO / "tools" / "_scan_work" / "repo_audit_report.json")
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
    print(f"Wrote {out.relative_to(REPO)}")

    # Non-zero if serious issues remain after optional prune
    serious = 0
    for key in (
        "missing_packages",
        "stale_sha",
        "path_mismatch",
        "science_page_count_mismatch",
        "bad_manifest",
    ):
        serious += pkg["issue_counts"].get(key, 0)
    if not args.prune_orphans:
        serious += pkg["issue_counts"].get("orphan_packages", 0)
    serious += links["broken_count"]
    return 1 if serious else 0


if __name__ == "__main__":
    raise SystemExit(main())
