# Role agents

Chat context is disposable. Each **role** keeps a durable markdown file that the next agent in that role reads and updates. Treat the chat as RAM; treat `agents/<role>.md` as the thumbdrive.

## Roles

H1 GP, H2 computing, H2 math and H2 physics are **archived** (physics re-froze 2026-11-27 after P1); their roles are **bookkeepers** for their own field: each files new documents by the `README.md` naming rules, keeps converted packages and the README inventory in step, answers where things live, and logs here. None of these roles runs practice or builds new tools unless the user explicitly asks.

| Role file | Covers |
| --- | --- |
| [`chemistry.md`](chemistry.md) | H2 chemistry — `raw files/H2 chemistry/` |
| [`computing.md`](computing.md) | H2 computing — `raw files/H2 computing/ARCHIVED.md` |
| [`gp.md`](gp.md) | H1 GP — `raw files/H1 GP/ARCHIVED.md` |
| [`math.md`](math.md) | H2 math — `raw files/H2 math/ARCHIVED.md` |
| [`physics.md`](physics.md) | H2 physics — `raw files/H2 physics/ARCHIVED.md` |

Library-wide conventions (layers, naming, conversion) live in the root `README.md`.

Add a new role by copying [`_role.template.md`](_role.template.md) and linking it in this table.

**Portable kit for other repos:** [`templates/agent-workspace-kit/`](../templates/agent-workspace-kit/) — see `UNPACK.md` / `unpack.ps1`.

## Permanent-log protocol

1. **Start:** open `agents/<role>.md` for the role you are acting as.
2. **Work:** prefer that file + high-signal paths in root `AGENTS.md` over replaying long chats or bulk corpora.
3. **Log:** after decisions that future holders need, append under `## Session log` using:

```markdown
### YYYY-MM-DD — short title

- **Decided:** …
- **Touched:** `path` …
- **Next:** …
```

4. **Habits / rules:** when a pattern should stick across sessions, add it under `## Rules & habits` in that role file (not only in the chat).
5. **Never** use the role file as a paste bin for OCR dumps, full transcripts, or page rasters. Point at paths instead.

## Relation to other docs

| Doc | Job |
| --- | --- |
| Root `AGENTS.md` | What any agent may open by default (corpus hygiene) |
| `agents/<role>.md` | Who this agent is, and what this role has already decided |
| `.cursor/rules/` | Always-on hard constraints (locked sits, writing coherence, this protocol) |
| `ops/cursor-memory/` | Optional export of old Cursor chats; not a substitute for role logs |
