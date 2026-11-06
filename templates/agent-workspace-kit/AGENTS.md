# Agent context map

Prefer small, decision-bearing files. Do **not** walk generated artifacts, vendor trees, or bulk dumps into context.

## Role agents (permanent thumbdrive)

Chats are disposable. Each role keeps durable state in `agents/<role>.md`. Protocol: `agents/README.md`. Always-on rule: `.cursor/rules/agent-role-logs.mdc`.

| Role | File | Job |
| --- | --- | --- |
| Build | `agents/build.md` | Workspace / repo infrastructure |
| Domain | `agents/domain.md` | _(rename)_ first product jurisdiction |

At session start, read your role file. Before the chat ends, append decisions there.

## Open by default (high signal)

| Path | Why |
| --- | --- |
| `agents/<role>.md` | Your role’s permanent context |
| `AGENTS.md` | This map |
| `.cursor/rules/` | Always-on constraints |
| _(add project docs)_ | README, ADRs, architecture notes |

## Open only when the task names them

- A specific source file or package under work
- One fixture, log, or screenshot required to fix a bug

## Never load wholesale

- `node_modules/`, `.venv/`, `dist/`, `build/`, `.next/`, coverage reports
- Lockfile blobs as “documentation”
- Large fixtures, snapshots, warehouse dumps, binary assets
- Secrets: `.env*`, credential JSON, private keys
- Full prior chat transcripts when `agents/<role>.md` already holds the decision

_Edit this section per project._
