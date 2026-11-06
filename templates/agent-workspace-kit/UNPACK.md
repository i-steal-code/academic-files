# Unpack: agent workspace kit

Copy this folder’s **contents** into the root of a new project (or merge file-by-file). Then customise roles for that product.

Chat = disposable RAM. `agents/<role>.md` = permanent thumbdrive.

## Layout after unpack

```text
<project-root>/
  AGENTS.md
  CLAUDE.md                          # optional; Claude Code entry
  .claudeignore
  .cursorignore
  .cursor/rules/agent-role-logs.mdc  # always-on protocol
  agents/
    README.md                        # protocol + role table
    _role.template.md                # copy to add a role
    build.md                         # infrastructure role (keep)
    domain.md                        # rename to your first domain role
```

## Steps

1. Copy everything under this kit into the target repo root (keep relative paths).
2. Edit `agents/README.md` — replace the example role table with your real roles.
3. Keep `agents/build.md` for repo plumbing; rewrite **In scope** paths for that project.
4. Rename `agents/domain.md` → e.g. `backend.md` / `product.md` / `editorial.md` and fill Primary function.
5. Update root `AGENTS.md` open-by-default / never-wholesale lists for *this* codebase’s token sinks.
6. Trim `.claudeignore` / `.cursorignore` to match (Node vs Python vs mono-repo).
7. First real session: act as **build**, append a session-log entry that records the unpack.

## One-liner (from this academic-files repo)

PowerShell — copy kit into another project root:

```powershell
$kit = "templates\agent-workspace-kit"
$dest = "D:\path\to\new-project"   # change me
Copy-Item "$kit\AGENTS.md","$kit\CLAUDE.md","$kit\.claudeignore","$kit\.cursorignore" $dest -Force
New-Item -ItemType Directory -Force "$dest\agents" | Out-Null
New-Item -ItemType Directory -Force "$dest\.cursor\rules" | Out-Null
Copy-Item "$kit\agents\*" "$dest\agents\" -Force
Copy-Item "$kit\.cursor\rules\*" "$dest\.cursor\rules\" -Force
# Do not copy UNPACK.md unless you want it in the target repo.
```

## Non-goals

- Not a framework, SDK, or shared global agents folder across products.
- Not a substitute for product docs — only agent jurisdiction + durable decisions.
- Subject/academic convert pipelines are **not** in this kit; add those only in repos that need them.
