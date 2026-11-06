# Role agents

Chat context is disposable. Each **role** keeps a durable markdown file that the next agent in that role reads and updates. Treat the chat as RAM; treat `agents/<role>.md` as the thumbdrive.

## Roles

| Role file | Primary function |
| --- | --- |
| [`build.md`](build.md) | Workspace infrastructure: library layout, conversion, ignore/slim hygiene, agent portability, tooling under `tools/` / `ops/`, repo conventions |
| [`computing.md`](computing.md) | H2 computing content and practice: syllabus notes, papers, practicals, blurt sheets, computing-specific marking and drills |
| [`gp.md`](gp.md) | H1 GP **archived** (season closed): freeze steward only — see `raw files/H1 GP/ARCHIVED.md` |
| [`math.md`](math.md) | H2 math content and practice: topical sets, prelims/TYS, readiness canvases, syllabus cuts |
| [`physics.md`](physics.md) | H2 physics content and practice: chapters, revision packages, prelims, blurt sheets |

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
