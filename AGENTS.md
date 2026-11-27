# Agent context map

Prefer small, decision-bearing files. Do **not** walk bulk OCR dumps, page rasters, or sample datasets into context.

## Library archived (2026-11-27)

A-levels are over. H1 GP, H2 computing, H2 math and H2 physics are closed and kept as a frozen record; each subject folder has an `ARCHIVED.md` freeze notice. Agents for those subjects act as **bookkeepers**: file new documents by the `README.md` naming rules, keep converted packages and the README inventory in step, answer where things live, and log decisions. Do not run practice, set or mark work, or build new tools unless the user explicitly reopens a subject.

Physics was briefly reopened for the P1 paper (2026-11-17 → 2026-11-27) and re-froze when P1 ended. H2 chemistry is a library section with no archive or active-development label.

## Role agents (permanent thumbdrive)

Chats are disposable. Each role keeps durable state in `agents/<role>.md` (function, rules, habits, session log). Protocol: `agents/README.md`. Always-on rule: `.cursor/rules/agent-role-logs.mdc`.

| Role | File | Covers |
| --- | --- | --- |
| Chemistry | `agents/chemistry.md` | H2 chemistry library (`raw files/H2 chemistry/`) |
| Computing | `agents/computing.md` | H2 computing (`raw files/H2 computing/ARCHIVED.md`) |
| GP | `agents/gp.md` | H1 GP (`raw files/H1 GP/ARCHIVED.md`) |
| Math | `agents/math.md` | H2 math (`raw files/H2 math/ARCHIVED.md`) |
| Physics | `agents/physics.md` | H2 physics (`raw files/H2 physics/ARCHIVED.md`) |

At session start, read your role file. Before the chat ends, append decisions there so the next holder is not stuck replaying a long transcript.

**Other projects:** unpack `templates/agent-workspace-kit/` (see that folder’s `UNPACK.md`).

## Open by default (high signal)

| Path | Why |
| --- | --- |
| `agents/<role>.md` | Your role’s permanent context |
| `README.md` | Library layers, naming, conversion policy |
| `raw files/<subject>/ARCHIVED.md` | Freeze notice and where that subject's records live |
| `.cursor/rules/` | Role-log protocol; GP archive/lock rule; writing coherence |

## Open only when the task names them

- A specific paper under `converted packages/…/<stem>/content.md` (or its raw PDF)
- One chapter tutorial / lect notes package
- Any archived subject's `blurt sheets/`, `work/`, `scripts/` or practice files — frozen practice records
- Any `raw files/H1 GP/**` path — open only if the user explicitly asks about GP
- Any `raw files/H2 computing/**` or `computing practical/**` path — open only if the user explicitly asks about computing

## Never load wholesale

- Any whole subject tree as “default context”
- KS Bull / Kaleidoscope / REHEARSE / Infopacks / IPS papers / long GP guides / **all** `topics + case studies` packs — **index-only** under `converted packages/` (`corpus_mode: index`). Titles only; raw PDF/DOCX for deep read. Rebuild full dump only with `python tools/convert_gp_package.py --full-corpus --force`.
- `converted packages/**/pages/` rasters
- `tools/_scan_work/`, `ops/cursor-memory/`, `origin/`, `unfiled/`
- `restaurants.json`, large CSVs, warehouse fixtures

## Hygiene tools

```powershell
python tools\slim_agent_context.py              # re-index bulk GP corpora
python tools\slim_agent_context.py --purge-junk # clear temp / chat-export dumps
```
