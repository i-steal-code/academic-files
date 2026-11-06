# ops

Local operator tooling for agent portability. Not part of the academic corpus.

## `cursor-memory/` (gitignored)

High-value Cursor export for Claude Code:

| Path | Role |
| --- | --- |
| `INDEX.md` | Catalog of condensed chats + canvases |
| `POINTER.md` | Absolute paths to live Cursor transcript/canvas dirs |
| `summaries/<uuid>.md` | Agenda + condensed assistant answers |
| `canvases/` | `.canvas.tsx` + `.data.json` (no runtime) |
| `PILOT_AUDIT.json` | Compression / cue-hit metrics from last export |

### Pilot

```powershell
.\.venv-convert\Scripts\python.exe tools\export_cursor_memory.py --pilot
.\.venv-convert\Scripts\python.exe tools\export_cursor_memory.py --audit-only
```

### Transition-day batch

```powershell
.\.venv-convert\Scripts\python.exe tools\export_cursor_memory.py --all
```

Raw JSONL is not copied (size + sensitive exam discussion). Deep lookup uses `POINTER.md`.

### Pilot results (2026-11-01)

| Metric | Value |
| --- | --- |
| Chats | 2 (`7472f035…` filing/transition, `990da5f5…` math topical) |
| Raw JSONL | 2.3 MB |
| Summaries | 105 KB (~22× smaller) |
| Cue recovery | Both chats retained filing/convert/prelim/canvas keywords |
| Canvases | 11 files (all current project canvases; no `node_modules`) |

**What worked:** user agendas intact; final answers recoverable for naming rules, `unfiled/`, model-essay filing, Add Prac / mock Solns moves, conversion policy.

**Known gap:** “Implement the plan…” turns are often tool-only in JSONL (`_No substantial text reply_`). On transition day, use the previous planning section or raw JSONL via `POINTER.md`.

Full batch size today: **13** primary transcripts (~8.5 MB raw). Checklist: `ops/TRANSITION_DAY.md`.
