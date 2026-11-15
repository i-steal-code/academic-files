# Agent context map

Prefer small, decision-bearing files. Do **not** walk bulk OCR dumps, page rasters, or sample datasets into context.

## Focus lock (until the Physics P3 paper ends, 2026-11-17)

Debig set this on 2026-11-07 so he can study; it overrides the rest of this file. Physics works normally to the agreed study plan. Computing's paper was on 2026-11-11 and the subject is now archived. Every other role does no work and replies in one line that points Debig back to studying. Full rule: `../hub/AGENTS.md`.

## Role agents (permanent thumbdrive)

Chats are disposable. Each role keeps durable state in `agents/<role>.md` (function, rules, habits, session log). Protocol: `agents/README.md`. Always-on rule: `.cursor/rules/agent-role-logs.mdc`.

| Role | File | Job |
| --- | --- | --- |
| Build | `agents/build.md` | Workspace infrastructure |
| Computing | `agents/computing.md` | H2 computing **archived**: freeze steward only (`raw files/H2 computing/ARCHIVED.md`) |
| GP | `agents/gp.md` | H1 GP **archived** — freeze steward only (`raw files/H1 GP/ARCHIVED.md`) |
| Math | `agents/math.md` | H2 math content |
| Physics | `agents/physics.md` | H2 physics content |

At session start, read your role file. Before the chat ends, append decisions there so the next holder is not stuck replaying a long transcript.

**Other projects:** unpack `templates/agent-workspace-kit/` (see that folder’s `UNPACK.md`).

## Open by default (high signal)

| Path | Why |
| --- | --- |
| `agents/<role>.md` | Your role’s permanent context |
| `README.md` | Library layers, naming, conversion policy |
| `.cursor/rules/` | Role-log protocol; GP archive/lock rule; writing coherence |
| `raw files/*/blurt sheets/` | Active revision notes (math / physics; computing's are archived) |

## Open only when the task names them

- A specific paper under `converted packages/…/<stem>/content.md` (or its raw PDF)
- One chapter tutorial / lect notes package
- Any `raw files/H1 GP/**` path — **season archived**; open only if the user explicitly asks about GP
- Any `raw files/H2 computing/**` or `computing practical/**` path — **archived 2026-11-11**; open only if the user explicitly asks about computing

## Never load wholesale

- Entire H1 GP tree as “default context” (archived — see `raw files/H1 GP/ARCHIVED.md`)
- KS Bull / Kaleidoscope / REHEARSE / Infopacks / IPS papers / long GP guides / **all** `topics + case studies` packs — **index-only** under `converted packages/` (`corpus_mode: index`). Titles only; raw PDF/DOCX for deep read. Rebuild full dump only with `python tools/convert_gp_package.py --full-corpus --force`.
- `converted packages/**/pages/` rasters
- `tools/_scan_work/`, `ops/cursor-memory/`, `origin/`, `unfiled/`
- `restaurants.json`, large CSVs, warehouse fixtures

## Hygiene tools

```powershell
python tools\slim_agent_context.py              # re-index bulk GP corpora
python tools\slim_agent_context.py --purge-junk # clear temp / chat-export dumps
```
