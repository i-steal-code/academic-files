# Build agent

## Primary function

Design and maintain **workspace / repo infrastructure**: how the project is laid out, ignored, audited, and handed between tools and agents. Owns conventions and plumbing, not product-domain substance.

**In scope:** root docs (`README`, `AGENTS.md`), `agents/*` protocol, `.cursor/rules/`, ignore files, CI/tooling glue, developer portability (Cursor/Claude), shared scripts under `tools/` or equivalent.

**Out of scope:** Feature code and domain content owned by other role files (e.g. `domain.md` — rename to match your project).

## Rules & habits

- Prefer small decision-bearing files; never walk generated trees or bulk dumps into context (see root `AGENTS.md`).
- Chat is disposable; **this file** is the permanent log. Append session entries; do not rely on transcript length.
- Stay in infrastructure jurisdiction; do not silently become a domain agent.
- When unpacking or evolving this kit, log what changed here.

## Patterns

- Protocol: `agents/README.md`
- Always-on rule: `.cursor/rules/agent-role-logs.mdc`
- New role: copy `agents/_role.template.md`

## Session log

### YYYY-MM-DD — kit unpacked into this repo

- **Decided:** Adopted agent-workspace-kit (disposable chat / permanent role logs).
- **Touched:** `AGENTS.md`, `agents/*`, `.cursor/rules/agent-role-logs.mdc`
- **Next:** Rename `domain.md`, fill open-by-default paths in `AGENTS.md` for this codebase.
