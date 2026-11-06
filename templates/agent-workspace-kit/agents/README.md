# Role agents

Chat context is disposable. Each **role** keeps a durable markdown file that the next agent in that role reads and updates. Treat the chat as RAM; treat `agents/<role>.md` as the thumbdrive.

## Roles

| Role file | Primary function |
| --- | --- |
| [`build.md`](build.md) | Repo / workspace infrastructure: layout, tooling, ignores, agent protocol, portability |
| [`domain.md`](domain.md) | _(Rename this file.)_ First product domain — replace with real jurisdiction |

Add a role: copy [`_role.template.md`](_role.template.md) → `agents/<name>.md`, fill the sections, link it in this table.

## Permanent-log protocol

1. **Start:** open `agents/<role>.md` for the role you are acting as.
2. **Work:** prefer that file + high-signal paths in root `AGENTS.md` over replaying long chats or bulk dumps.
3. **Log:** after decisions future holders need, append under `## Session log`:

```markdown
### YYYY-MM-DD — short title

- **Decided:** …
- **Touched:** `path` …
- **Next:** …
```

4. **Habits / rules:** when a pattern should stick across sessions, add it under `## Rules & habits` in that role file.
5. **Never** paste bin: no full transcripts, raw tool dumps, or bulk data. Point at paths instead.

## Relation to other docs

| Doc | Job |
| --- | --- |
| Root `AGENTS.md` | What any agent may open by default |
| `agents/<role>.md` | Who this agent is, and what this role already decided |
| `.cursor/rules/agent-role-logs.mdc` | Always-on: read role file, log, stay in lane |
| `CLAUDE.md` | Short Claude Code pointer to the same protocol |
