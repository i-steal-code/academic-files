# Transition-day checklist (Cursor → Claude Code memory)

Do not run the full batch until you are ready to switch day-to-day agents.

## 1. Refresh the local archive

```powershell
cd "C:\Users\debig\OneDrive\Desktop\github repository\academic-files"
.\.venv-convert\Scripts\python.exe tools\export_cursor_memory.py --all
.\.venv-convert\Scripts\python.exe tools\export_cursor_memory.py --audit-only
```

Expect: one summary per primary transcript UUID, full `canvases/` mirror, updated `INDEX.md` / `POINTER.md` / `PILOT_AUDIT.json`.

## 2. Spot-check

- Open `ops/cursor-memory/INDEX.md` — every chat has a title and link.
- Open 2–3 `summaries/*.md` — agenda matches memory; decisions still make sense.
- Confirm canvases you care about (`math-readiness`, `physics-readiness`, …) are under `ops/cursor-memory/canvases/`.
- For any `_No substantial text reply_` under a plan-implement turn, use `POINTER.md` → raw JSONL or the preceding planning section.

## 3. Portability pack (committed)

Separate from the gitignored archive:

- [ ] `CLAUDE.md` (or `AGENTS.md`) with README bookkeeping + locked sits + GP coherence + convert commands
- [ ] `~/.claude/CLAUDE.md` with personal Cursor User Rules (commits, tone)
- [ ] `.claude/rules/` mirrors of `.cursor/rules/` (`paths:` for jupyter)

## 4. Dual-run

Keep `.cursor/rules/` until Claude Code sessions file/convert/audit correctly without opening Cursor chats.
