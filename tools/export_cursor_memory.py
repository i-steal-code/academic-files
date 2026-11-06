#!/usr/bin/env python3
"""
Export high-value Cursor memory into a local, gitignored archive for Claude Code.

Pilot / batch modes:
  python tools/export_cursor_memory.py --pilot
  python tools/export_cursor_memory.py --all
  python tools/export_cursor_memory.py --audit-only

What is packaged (high-value only):
  - condensed chat summaries (user queries + substantial assistant text)
  - canvases (.tsx + .data.json; no node_modules)
  - INDEX.md + POINTER.md

Raw JSONL is NOT copied by default (size + PII). Use --link-raw to record absolute paths.
"""

from __future__ import annotations

import argparse
import json
import re
import shutil
import sys
from dataclasses import dataclass, field
from datetime import datetime, timezone
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
DEFAULT_OUT = REPO / "ops" / "cursor-memory"
PROJECT_SLUG = "c-Users-debig-OneDrive-Desktop-github-repository-academic-files"
CURSOR_PROJECT = Path.home() / ".cursor" / "projects" / PROJECT_SLUG
TRANSCRIPTS = CURSOR_PROJECT / "agent-transcripts"
CANVASES = CURSOR_PROJECT / "canvases"
LOCALAPPDATA = Path(
    __import__("os").environ.get(
        "LOCALAPPDATA",
        str(Path.home() / "AppData" / "Local"),
    )
)
AGENT_STORES_ROOT = LOCALAPPDATA / "Cursor" / "AgentStores" / "cursor_agent_stores"

USER_QUERY_RE = re.compile(r"<user_query>\s*(.*?)\s*</user_query>", re.S | re.I)
TIMESTAMP_RE = re.compile(r"<timestamp>\s*(.*?)\s*</timestamp>", re.S | re.I)
NOISE_USER_PREFIXES = (
    "Perform any necessary follow-up",
    "Briefly inform the user about the task result",
    "The following task has finished",
)


@dataclass
class Turn:
    role: str
    text: str
    timestamp: str | None = None


@dataclass
class ChatExport:
    uuid: str
    path: Path
    bytes: int
    lines: int
    user_queries: list[str] = field(default_factory=list)
    assistant_finals: list[str] = field(default_factory=list)
    first_ts: str | None = None
    last_ts: str | None = None
    title: str = ""


def extract_text_blocks(message: object) -> list[str]:
    if not isinstance(message, dict):
        return []
    content = message.get("content")
    if isinstance(content, str):
        return [content] if content.strip() else []
    if not isinstance(content, list):
        return []
    out: list[str] = []
    for block in content:
        if isinstance(block, dict) and block.get("type") == "text":
            t = block.get("text") or ""
            if t.strip():
                out.append(t)
    return out


def parse_user_payload(raw: str) -> tuple[str | None, str]:
    ts = None
    m_ts = TIMESTAMP_RE.search(raw)
    if m_ts:
        ts = m_ts.group(1).strip()
    m_q = USER_QUERY_RE.search(raw)
    if m_q:
        return ts, m_q.group(1).strip()
    # system notifications / bare text
    cleaned = TIMESTAMP_RE.sub("", raw).strip()
    return ts, cleaned


def is_noise_user(text: str) -> bool:
    t = text.strip()
    if not t:
        return True
    return any(t.startswith(p) for p in NOISE_USER_PREFIXES)


def compact_assistant(text: str, limit: int = 1200) -> str:
    t = text.strip()
    # Drop leading planning fluff lines that are only tool narration if short
    if len(t) <= limit:
        return t
    # Keep head + tail so conclusions survive
    head, tail = 700, 400
    return t[:head].rstrip() + "\n\n[…]\n\n" + t[-tail:].lstrip()


def load_chat(jsonl: Path) -> ChatExport:
    uid = jsonl.parent.name
    exp = ChatExport(uuid=uid, path=jsonl, bytes=jsonl.stat().st_size, lines=0)
    # pairs: list of [user_text, last_assistant_text]
    pairs: list[list[str]] = []
    with jsonl.open(encoding="utf-8", errors="replace") as fh:
        for line in fh:
            exp.lines += 1
            line = line.strip()
            if not line:
                continue
            try:
                obj = json.loads(line)
            except json.JSONDecodeError:
                continue
            role = obj.get("role")
            texts = extract_text_blocks(obj.get("message") or {})
            if not texts:
                continue
            raw = "\n".join(texts)
            if role == "user":
                ts, body = parse_user_payload(raw)
                if ts:
                    exp.first_ts = exp.first_ts or ts
                    exp.last_ts = ts
                if is_noise_user(body):
                    continue
                pairs.append([body, ""])
            elif role == "assistant" and pairs:
                body = raw.strip()
                if len(body) >= 40:
                    pairs[-1][1] = body  # keep last substantial reply for this user turn
    exp.user_queries = [p[0] for p in pairs]
    exp.assistant_finals = [p[1] for p in pairs]
    if exp.user_queries:
        first = re.sub(r"\s+", " ", exp.user_queries[0]).strip()
        exp.title = first[:80] + ("…" if len(first) > 80 else "")
    else:
        exp.title = "(no user queries)"
    return exp


def write_summary(exp: ChatExport, out_dir: Path) -> Path:
    out_dir.mkdir(parents=True, exist_ok=True)
    path = out_dir / f"{exp.uuid}.md"
    lines: list[str] = []
    lines.append(f"# {exp.title}")
    lines.append("")
    lines.append(f"- **uuid:** `{exp.uuid}`")
    lines.append(f"- **source:** `{exp.path}`")
    lines.append(f"- **size:** {exp.bytes:,} bytes / {exp.lines} JSONL lines")
    lines.append(f"- **span:** {exp.first_ts or '?'} → {exp.last_ts or '?'}")
    lines.append(f"- **user turns kept:** {len(exp.user_queries)}")
    lines.append("")
    lines.append("## Agenda (user queries)")
    lines.append("")
    for i, q in enumerate(exp.user_queries, 1):
        one = re.sub(r"\s+", " ", q).strip()
        if len(one) > 240:
            one = one[:240] + "…"
        lines.append(f"{i}. {one}")
    lines.append("")
    lines.append("## Decisions / answers (condensed assistant text)")
    lines.append("")
    n = max(len(exp.user_queries), len(exp.assistant_finals))
    for i in range(n):
        q = exp.user_queries[i] if i < len(exp.user_queries) else ""
        a = exp.assistant_finals[i] if i < len(exp.assistant_finals) else ""
        if not q and not a:
            continue
        q1 = re.sub(r"\s+", " ", q).strip()[:160]
        lines.append(f"### {i+1}. {q1 or '(assistant)'}")
        lines.append("")
        if a:
            lines.append(compact_assistant(a))
        else:
            lines.append("_No substantial text reply captured (tool-only turn)._")
        lines.append("")
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")
    return path


def copy_canvases(dest: Path) -> list[str]:
    dest.mkdir(parents=True, exist_ok=True)
    copied: list[str] = []
    if not CANVASES.is_dir():
        return copied
    for p in sorted(CANVASES.iterdir()):
        if p.name in {"node_modules", "tsconfig.json"}:
            continue
        if p.suffix.lower() in {".tsx", ".json"} or p.name.endswith(".canvas.tsx"):
            if p.is_file():
                shutil.copy2(p, dest / p.name)
                copied.append(p.name)
    return copied


def write_pointer(out: Path) -> None:
    text = f"""# Cursor memory pointers (absolute, local)

These paths are outside the git worktree. Claude Code / agents should read
`ops/cursor-memory/` first; use the paths below only for deep lookup.

| Kind | Path |
| --- | --- |
| Agent transcripts (JSONL) | `{TRANSCRIPTS}` |
| Canvases (live Cursor copies) | `{CANVASES}` |
| AgentStores root | `{AGENT_STORES_ROOT}` |
| Workspace storage (SQLite) | `%APPDATA%\\\\Cursor\\\\User\\\\workspaceStorage\\\\` (opaque; low value) |

Generated: {datetime.now(timezone.utc).isoformat()}
"""
    (out / "POINTER.md").write_text(text, encoding="utf-8")


def write_index(out: Path, chats: list[ChatExport], canvases: list[str]) -> None:
    lines = [
        "# Cursor memory index (pilot / export)",
        "",
        f"Generated: {datetime.now(timezone.utc).isoformat()}",
        "",
        "## How to use",
        "",
        "1. Read this index for the chat you need.",
        "2. Open `summaries/<uuid>.md` for agenda + condensed answers.",
        "3. Open `canvases/` for analysis UIs (source only; no Cursor runtime).",
        "4. Use `POINTER.md` if you must open the raw JSONL.",
        "",
        "## Chats",
        "",
        "| UUID | Title | Span | Summary | Raw bytes |",
        "| --- | --- | --- | --- | ---: |",
    ]
    for c in chats:
        span = f"{(c.first_ts or '?')[:16]} → {(c.last_ts or '?')[:16]}"
        title = c.title.replace("|", "/")
        lines.append(
            f"| `{c.uuid[:8]}…` | {title} | {span} | [md](summaries/{c.uuid}.md) | {c.bytes:,} |"
        )
    lines += ["", "## Canvases", ""]
    if canvases:
        for name in canvases:
            lines.append(f"- `canvases/{name}`")
    else:
        lines.append("_None copied._")
    lines.append("")
    (out / "INDEX.md").write_text("\n".join(lines), encoding="utf-8")


def list_transcripts() -> list[Path]:
    if not TRANSCRIPTS.is_dir():
        return []
    files: list[Path] = []
    for d in sorted(TRANSCRIPTS.iterdir()):
        if not d.is_dir():
            continue
        # Prefer parent-named jsonl; skip nested subagent-only if parent exists
        main = d / f"{d.name}.jsonl"
        if main.is_file():
            files.append(main)
            continue
        jsonls = sorted(d.glob("*.jsonl"))
        if jsonls:
            # pick largest as primary
            files.append(max(jsonls, key=lambda p: p.stat().st_size))
    return files


def audit_export(out: Path, chats: list[ChatExport]) -> dict:
    """Measure compression and whether summaries still carry recoverable cues."""
    report: dict = {"chats": [], "totals": {}}
    raw_total = 0
    md_total = 0
    cue_hits = 0
    cues = (
        "FILED",
        "locked",
        "convert",
        "prelim",
        "unfiled",
        "CLAUDE",
        "naming",
        "digital",
        "canvas",
    )
    for c in chats:
        summary = out / "summaries" / f"{c.uuid}.md"
        md_bytes = summary.stat().st_size if summary.is_file() else 0
        raw_total += c.bytes
        md_total += md_bytes
        body = summary.read_text(encoding="utf-8", errors="replace") if summary.is_file() else ""
        hits = [k for k in cues if k.lower() in body.lower()]
        if hits:
            cue_hits += 1
        report["chats"].append(
            {
                "uuid": c.uuid,
                "raw_bytes": c.bytes,
                "summary_bytes": md_bytes,
                "compression": round(c.bytes / md_bytes, 1) if md_bytes else None,
                "user_queries": len(c.user_queries),
                "assistant_finals": len([a for a in c.assistant_finals if a.strip()]),
                "cue_hits": hits,
                "title": c.title,
            }
        )
    report["totals"] = {
        "chats": len(chats),
        "raw_bytes": raw_total,
        "summary_bytes": md_total,
        "compression": round(raw_total / md_total, 1) if md_total else None,
        "chats_with_cues": cue_hits,
        "canvases": len(list((out / "canvases").glob("*"))) if (out / "canvases").is_dir() else 0,
    }
    return report


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--out", type=Path, default=DEFAULT_OUT)
    ap.add_argument("--pilot", action="store_true", help="Export 2 representative chats + canvases")
    ap.add_argument("--all", action="store_true", help="Export every primary transcript + canvases")
    ap.add_argument("--uuids", nargs="*", default=[], help="Specific chat UUIDs")
    ap.add_argument("--audit-only", action="store_true", help="Audit existing export only")
    ap.add_argument("--limit", type=int, default=0)
    args = ap.parse_args(argv)

    out: Path = args.out
    if args.audit_only:
        if not (out / "INDEX.md").is_file():
            print(f"No export at {out}", file=sys.stderr)
            return 1
        # rebuild ChatExport stubs from summaries for audit
        chats: list[ChatExport] = []
        for p in sorted((out / "summaries").glob("*.md")):
            raw = next(TRANSCRIPTS.glob(f"{p.stem}/{p.stem}.jsonl"), None)
            if raw and raw.is_file():
                chats.append(load_chat(raw))
            else:
                chats.append(
                    ChatExport(
                        uuid=p.stem,
                        path=p,
                        bytes=0,
                        lines=0,
                        title=p.stem,
                    )
                )
        report = audit_export(out, chats)
        print(json.dumps(report, indent=2))
        return 0

    if not (args.pilot or args.all or args.uuids):
        print("Pass --pilot, --all, or --uuids", file=sys.stderr)
        return 2

    all_files = list_transcripts()
    by_uuid = {p.parent.name: p for p in all_files}

    if args.uuids:
        selected = [by_uuid[u] for u in args.uuids if u in by_uuid]
        missing = [u for u in args.uuids if u not in by_uuid]
        if missing:
            print(f"WARNING missing uuids: {missing}", file=sys.stderr)
    elif args.pilot:
        # Prefer: large library chat + mid topical chat (stable IDs from audit)
        preferred = [
            "7472f035-48da-46e8-92fe-d887aafbf47b",  # long filing / transition
            "990da5f5-e057-4ae8-8eed-6abf20409ccc",  # math topical
        ]
        selected = [by_uuid[u] for u in preferred if u in by_uuid]
        if len(selected) < 2:
            # fallback: two largest
            selected = sorted(all_files, key=lambda p: -p.stat().st_size)[:2]
    else:
        selected = all_files

    if args.limit > 0:
        selected = selected[: args.limit]

    if out.exists():
        # Pilot/all: refresh contents but keep directory
        for sub in ("summaries", "canvases"):
            d = out / sub
            if d.exists():
                shutil.rmtree(d)
    out.mkdir(parents=True, exist_ok=True)
    (out / "summaries").mkdir(parents=True, exist_ok=True)

    chats_out: list[ChatExport] = []
    for path in selected:
        exp = load_chat(path)
        write_summary(exp, out / "summaries")
        chats_out.append(exp)
        print(f"SUMMARY {exp.uuid[:8]}… queries={len(exp.user_queries)} -> summaries/{exp.uuid}.md")

    canvases = copy_canvases(out / "canvases")
    print(f"CANVASES {len(canvases)} files")
    write_pointer(out)
    write_index(out, chats_out, canvases)

    report = audit_export(out, chats_out)
    (out / "PILOT_AUDIT.json").write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
    print("WROTE", out / "INDEX.md")
    print("AUDIT totals", json.dumps(report["totals"]))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
