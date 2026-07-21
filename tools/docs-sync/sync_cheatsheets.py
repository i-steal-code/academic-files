#!/usr/bin/env python3
"""Pull multi-tab Google Docs cheatsheets into raw + markdown mirrors.

Auth: set GOOGLE_SERVICE_ACCOUNT_JSON to the full service-account JSON string
(or a path to a JSON key file). Share each Doc with the SA email as Viewer.

Registry: tools/docs-sync/cheatsheets.json
"""

from __future__ import annotations

import argparse
import json
import os
import re
import sys
import urllib.request
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

SCOPES = [
    "https://www.googleapis.com/auth/documents.readonly",
    "https://www.googleapis.com/auth/drive.readonly",
]

PLACEHOLDER_IDS = {"", "REPLACE_WITH_GOOGLE_DOC_ID"}


def repo_root() -> Path:
    return Path(__file__).resolve().parent.parent.parent


def load_registry(path: Path) -> list[dict[str, str]]:
    data = json.loads(path.read_text(encoding="utf-8"))
    return list(data.get("cheatsheets") or [])


def load_credentials():
    from google.oauth2 import service_account

    raw = os.environ.get("GOOGLE_SERVICE_ACCOUNT_JSON", "").strip()
    if not raw:
        raise SystemExit(
            "GOOGLE_SERVICE_ACCOUNT_JSON is not set "
            "(paste full JSON key, or a path to the key file)."
        )
    if raw.startswith("{"):
        info = json.loads(raw)
    else:
        key_path = Path(raw)
        if not key_path.is_file():
            raise SystemExit(f"Service account key file not found: {key_path}")
        info = json.loads(key_path.read_text(encoding="utf-8"))
    return service_account.Credentials.from_service_account_info(info, scopes=SCOPES)


def build_docs_service(creds):
    from googleapiclient.discovery import build

    return build("docs", "v1", credentials=creds, cache_discovery=False)


def slugify(title: str) -> str:
    s = title.strip().lower()
    s = re.sub(r"[^\w\s-]", "", s, flags=re.UNICODE)
    s = re.sub(r"[-\s]+", "-", s).strip("-")
    return s or "untitled"


def flatten_tabs(tabs: list[dict[str, Any]] | None, prefix: str = "") -> list[dict[str, Any]]:
    """Return flat list of {tabId, title, slug, documentTab} including child tabs."""
    out: list[dict[str, Any]] = []
    for tab in tabs or []:
        props = tab.get("tabProperties") or {}
        title = props.get("title") or "Untitled"
        tab_id = props.get("tabId") or ""
        slug_base = slugify(title)
        slug = f"{prefix}{slug_base}" if not prefix else f"{prefix}__{slug_base}"
        doc_tab = tab.get("documentTab")
        if tab_id and doc_tab is not None:
            out.append(
                {
                    "tabId": tab_id,
                    "title": title,
                    "slug": slug,
                    "documentTab": doc_tab,
                }
            )
        children = tab.get("childTabs") or []
        if children:
            out.extend(flatten_tabs(children, prefix=slug))
    return out


def read_paragraph_elements(elements: list[dict[str, Any]] | None) -> str:
    texts: list[str] = []
    for el in elements or []:
        text_run = el.get("textRun")
        if text_run and "content" in text_run:
            texts.append(text_run["content"])
    return "".join(texts)


def named_style_to_heading(named: str | None) -> int | None:
    if not named:
        return None
    m = re.match(r"HEADING_(\d)", named)
    if m:
        return int(m.group(1))
    if named == "TITLE":
        return 1
    if named == "SUBTITLE":
        return 2
    return None


def table_to_markdown(table: dict[str, Any]) -> str:
    rows_md: list[list[str]] = []
    for row in table.get("tableRows") or []:
        cells: list[str] = []
        for cell in row.get("tableCells") or []:
            cell_bits: list[str] = []
            for content in cell.get("content") or []:
                para = content.get("paragraph")
                if para:
                    cell_bits.append(read_paragraph_elements(para.get("elements")).strip())
            cells.append(" ".join(x for x in cell_bits if x).replace("|", "\\|") or " ")
        if cells:
            rows_md.append(cells)
    if not rows_md:
        return ""
    width = max(len(r) for r in rows_md)
    normalized = [r + [" "] * (width - len(r)) for r in rows_md]
    header = normalized[0]
    lines = [
        "| " + " | ".join(header) + " |",
        "| " + " | ".join("---" for _ in header) + " |",
    ]
    for row in normalized[1:]:
        lines.append("| " + " | ".join(row) + " |")
    return "\n".join(lines)


def structural_to_markdown(body_content: list[dict[str, Any]] | None) -> str:
    lines: list[str] = []

    for block in body_content or []:
        if "paragraph" in block:
            para = block["paragraph"]
            style = (para.get("paragraphStyle") or {}).get("namedStyleType")
            text = read_paragraph_elements(para.get("elements")).rstrip("\n")
            bullet = para.get("bullet")
            if bullet is not None:
                nest = int(bullet.get("nestingLevel") or 0)
                indent = "  " * nest
                lines.append(f"{indent}- {text.strip()}")
                continue
            level = named_style_to_heading(style)
            if level:
                lines.append(f"{'#' * level} {text.strip()}")
            elif text.strip():
                lines.append(text.strip())
            else:
                lines.append("")
        elif "table" in block:
            md = table_to_markdown(block["table"])
            if md:
                lines.append("")
                lines.append(md)
                lines.append("")
        elif "sectionBreak" in block:
            lines.append("")
        elif "tableOfContents" in block:
            continue

    # Collapse excessive blank lines
    out: list[str] = []
    blank = 0
    for line in lines:
        if line.strip() == "":
            blank += 1
            if blank <= 2:
                out.append("")
        else:
            blank = 0
            out.append(line)
    return "\n".join(out).strip() + "\n"


def export_tab_docx(creds, document_id: str, tab_id: str) -> bytes:
    import urllib.parse
    from google.auth.transport.requests import Request

    if not creds.valid:
        creds.refresh(Request())
    url = (
        f"https://docs.google.com/document/d/{document_id}/export"
        f"?format=docx&tab={urllib.parse.quote(tab_id)}"
    )
    req = urllib.request.Request(url, headers={"Authorization": f"Bearer {creds.token}"})
    with urllib.request.urlopen(req, timeout=120) as resp:
        data = resp.read()
    if not data or len(data) < 64:
        raise RuntimeError(f"Empty/short docx export for tab={tab_id}")
    if data[:2] != b"PK":
        raise RuntimeError(
            f"Docx export for tab={tab_id} did not return a ZIP/docx "
            f"(content-type may be HTML error). Check Doc sharing with the service account."
        )
    return data


def markdown_via_markitdown(docx_path: Path) -> str:
    from markitdown import MarkItDown

    md = MarkItDown(enable_plugins=False)
    result = md.convert_local(str(docx_path))
    return (result.text_content or "").strip() + "\n"


def write_index(md_dir: Path, tabs: list[dict[str, Any]], label: str) -> None:
    lines = [
        f"# {label}",
        "",
        "Synced from Google Docs (one file per tab).",
        "",
    ]
    for t in tabs:
        lines.append(f"- [{t['title']}](./{t['slug']}.md)")
    lines.append("")
    (md_dir / "INDEX.md").write_text("\n".join(lines), encoding="utf-8")


def sync_one(entry: dict[str, str], docs_service, creds, root: Path, force: bool) -> str:
    """Returns status: skipped_placeholder | skipped_unchanged | synced"""
    doc_id = (entry.get("document_id") or "").strip()
    label = entry.get("label") or doc_id
    raw_dir = root / entry["raw_dir"]
    md_dir = root / entry["md_dir"]
    tabs_dir = raw_dir / "tabs"
    meta_path = raw_dir / "sync-meta.json"

    if doc_id in PLACEHOLDER_IDS:
        print(f"SKIP {label}: document_id not set in cheatsheets.json")
        # Ensure folder scaffold exists
        tabs_dir.mkdir(parents=True, exist_ok=True)
        md_dir.mkdir(parents=True, exist_ok=True)
        if not meta_path.is_file():
            meta_path.write_text(
                json.dumps(
                    {
                        "document_id": doc_id,
                        "label": label,
                        "status": "awaiting_document_id",
                        "tabs": [],
                    },
                    indent=2,
                )
                + "\n",
                encoding="utf-8",
            )
        if not (md_dir / "INDEX.md").is_file():
            (md_dir / "INDEX.md").write_text(
                f"# {label}\n\n"
                "Awaiting `document_id` in `tools/docs-sync/cheatsheets.json` "
                "and a successful sync run.\n",
                encoding="utf-8",
            )
        return "skipped_placeholder"

    print(f"FETCH {label} ({doc_id})")
    doc = (
        docs_service.documents()
        .get(documentId=doc_id, includeTabsContent=True)
        .execute()
    )
    revision_id = doc.get("revisionId") or ""
    existing = {}
    if meta_path.is_file():
        try:
            existing = json.loads(meta_path.read_text(encoding="utf-8"))
        except json.JSONDecodeError:
            existing = {}

    if (
        not force
        and existing.get("revisionId") == revision_id
        and revision_id
        and tabs_dir.is_dir()
        and md_dir.is_dir()
    ):
        print(f"  unchanged revisionId={revision_id}")
        return "skipped_unchanged"

    flat = flatten_tabs(doc.get("tabs"))
    if not flat:
        # Single-tab legacy: synthesize from top-level body if tabs empty
        body = doc.get("body")
        if body:
            flat = [
                {
                    "tabId": "legacy",
                    "title": label,
                    "slug": slugify(label),
                    "documentTab": {"body": body},
                }
            ]
        else:
            raise RuntimeError(f"No tabs/body returned for {doc_id}")

    # Disambiguate duplicate slugs
    seen: dict[str, int] = {}
    for t in flat:
        base = t["slug"]
        n = seen.get(base, 0)
        seen[base] = n + 1
        if n:
            t["slug"] = f"{base}-{n + 1}"

    tabs_dir.mkdir(parents=True, exist_ok=True)
    md_dir.mkdir(parents=True, exist_ok=True)

    kept_docx: set[str] = set()
    kept_md: set[str] = set()

    for t in flat:
        slug = t["slug"]
        tab_id = t["tabId"]
        print(f"  tab: {t['title']!r} -> {slug}")

        docx_path = tabs_dir / f"{slug}.docx"
        if tab_id == "legacy":
            # No per-tab export; write a minimal placeholder note in meta only
            # Still produce markdown from structural body.
            md_text = structural_to_markdown((t["documentTab"].get("body") or {}).get("content"))
            if len(md_text.strip()) < 40:
                raise RuntimeError(f"Legacy tab markdown too short for {label}")
            md_path = md_dir / f"{slug}.md"
            md_path.write_text(
                f"---\ntitle: {t['title']}\nsource: google-docs\n---\n\n{md_text}",
                encoding="utf-8",
            )
            kept_md.add(md_path.name)
            continue

        data = export_tab_docx(creds, doc_id, tab_id)
        docx_path.write_bytes(data)
        kept_docx.add(docx_path.name)

        md_text = structural_to_markdown((t["documentTab"].get("body") or {}).get("content"))
        if len(md_text.strip()) < 40:
            print("    structural md thin; falling back to MarkItDown on docx")
            md_text = markdown_via_markitdown(docx_path)

        md_path = md_dir / f"{slug}.md"
        md_path.write_text(
            f"---\ntitle: {t['title']}\ntab_id: {tab_id}\nsource: google-docs\n---\n\n{md_text}",
            encoding="utf-8",
        )
        kept_md.add(md_path.name)

    # Orphan cleanup (keep underscore-prefixed archives such as _legacy-pre-sync.docx)
    for old in tabs_dir.glob("*.docx"):
        if old.name.startswith("_"):
            continue
        if old.name not in kept_docx:
            old.unlink()
            print(f"  removed orphan raw: {old.name}")
    for old in md_dir.glob("*.md"):
        if old.name == "INDEX.md":
            continue
        if old.name not in kept_md:
            old.unlink()
            print(f"  removed orphan md: {old.name}")

    write_index(md_dir, flat, label)
    meta = {
        "document_id": doc_id,
        "label": label,
        "revisionId": revision_id,
        "title": doc.get("title"),
        "synced_at": datetime.now(timezone.utc).isoformat(),
        "tabs": [{"tabId": t["tabId"], "title": t["title"], "slug": t["slug"]} for t in flat],
    }
    meta_path.write_text(json.dumps(meta, indent=2) + "\n", encoding="utf-8")
    return "synced"


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--registry",
        type=Path,
        default=Path(__file__).resolve().parent / "cheatsheets.json",
    )
    parser.add_argument("--repo", type=Path, default=None)
    parser.add_argument("--force", action="store_true")
    args = parser.parse_args(argv)

    root = (args.repo or repo_root()).resolve()
    entries = load_registry(args.registry.resolve())
    if not entries:
        print("No cheatsheets in registry.")
        return 0

    # If every entry is placeholder, scaffold only (no credentials required)
    if all((e.get("document_id") or "").strip() in PLACEHOLDER_IDS for e in entries):
        print("All document_ids are placeholders; writing folder scaffolds only.")
        for e in entries:
            sync_one(e, None, None, root, force=args.force)
        return 0

    creds = load_credentials()
    from google.auth.transport.requests import Request

    if not creds.valid:
        creds.refresh(Request())
    docs_service = build_docs_service(creds)

    counts = {
        "synced": 0,
        "skipped_unchanged": 0,
        "skipped_placeholder": 0,
        "failed": 0,
    }
    for entry in entries:
        label = entry.get("label") or entry.get("document_id")
        try:
            status = sync_one(entry, docs_service, creds, root, force=args.force)
            counts[status] = counts.get(status, 0) + 1
            print(f"-> {label}: {status}")
        except Exception as exc:  # noqa: BLE001
            counts["failed"] += 1
            print(f"-> {label}: failed: {exc}", file=sys.stderr)
            import traceback

            traceback.print_exc()

    print(
        "Done: "
        f"synced={counts['synced']} "
        f"unchanged={counts['skipped_unchanged']} "
        f"placeholder={counts['skipped_placeholder']} "
        f"failed={counts['failed']}"
    )
    return 1 if counts["failed"] else 0


if __name__ == "__main__":
    raise SystemExit(main())
