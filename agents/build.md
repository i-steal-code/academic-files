# Build agent

## Primary function

Design and maintain **workspace infrastructure**: how the academic library is laid out, converted, ignored, audited, and handed between tools/agents. This role owns conventions and plumbing, not subject teaching content.

**In scope:** `README.md` library policy, `raw files/` / `converted packages/` / `origin/` / `unfiled/` rules, `tools/*`, `ops/*`, `.gitignore` / `.claudeignore` / `.cursorignore`, root `AGENTS.md`, `agents/*` protocol, Cursor↔Claude portability, convert/slim/audit scripts.

**Out of scope:** Writing or rewriting GP/math/physics/computing syllabus substance, marking scripts, or essay arguments — hand those to the matching subject role file.

## Rules & habits

- Prefer small decision-bearing files; never walk bulk OCR, page rasters, or sample datasets into context (see root `AGENTS.md`).
- GP bulk corpora (periodicals, infopacks, all `topics + case studies`) stay **index-only** in converted packages unless the user asks for `--full-corpus`.
- Science `converted packages/` are local analysis artifacts (gitignored); raw PDFs stay canonical.
- `raw files/unfiled/` is a gitignored inbox; file into subject trees before convert.
- Bitwise duplicates die; born-digital / text-layer editions beat scans.
- Locked 8881 P2 sits: never remix into practice banks (`.cursor/rules/gp-8881-locked-sits.mdc`).
- Chat is disposable; **this file** is the permanent log. Append session entries; do not rely on transcript length.
- Stay in infrastructure jurisdiction; do not silently become the computing/GP/math/physics content agent.

## Patterns

- Conversion: `tools/convert_gp_package.py` (GP markdown; default index for bulk), `tools/convert_one.ps1` / science hybrid packages.
- Context hygiene: `tools/slim_agent_context.py` (+ `--purge-junk`).
- Cursor memory pilot/batch: `tools/export_cursor_memory.py`; checklist `ops/TRANSITION_DAY.md`.
- Repo audit: `tools/audit_repo.py`.

## Session log

### 2026-11-04 — GP archive freeze (infra touch)

- **Decided:** GP practice workflow ended in place (no folder move). Root `AGENTS.md` no longer opens GP arsenal/planning/scripts by default. Always-on lock rule covers full season archive, not only the gold sit list.
- **Touched:** `AGENTS.md`, `.cursor/rules/gp-8881-locked-sits.mdc`, `README.md` (GP section); content banners owned by GP role under `raw files/H1 GP/`
- **Next:** None for GP from build.

### 2026-11-01 — Generalisable agent-workspace kit

- **Decided:** Ship a copy-paste kit at `templates/agent-workspace-kit/` so non-academic projects can unpack the same disposable-chat / permanent-role-log infrastructure (generic `build` + renameable `domain`, ignores, `CLAUDE.md`, `unpack.ps1`). Academic subject roles stay only in this repo’s `agents/`.
- **Touched:** `templates/agent-workspace-kit/**`, `agents/README.md`, `agents/build.md`, root `AGENTS.md`
- **Next:** When starting a new project, run `templates/agent-workspace-kit/unpack.ps1 -Destination <path>` and customise roles there.

### 2026-11-01 — Role-log protocol + agent context declutter

- **Decided:** Each role keeps `agents/<role>.md` as permanent thumbdrive; chats stay disposable. Always-on rule: `.cursor/rules/agent-role-logs.mdc`. Build role = workspace infrastructure only.
- **Decided (context hygiene):** Slim GP periodicals/infopacks/`topics + case studies` converted `content.md` to title indexes (~7 MB + ~4.5 MB → ~60 KB + ~115 KB class of savings). Add `.claudeignore` / `.cursorignore`, root `AGENTS.md` open-by-default map. Purge `_tmp_exec.txt`, Gemini humour chat JSON, clear `tools/_scan_work/`.
- **Decided (portability, prior):** High-value Cursor export = condensed summaries + canvases only; pilot in `ops/cursor-memory/`; full `--all` deferred to transition day (`ops/TRANSITION_DAY.md`).
- **Touched:** `agents/README.md`, `agents/build.md`, `.cursor/rules/agent-role-logs.mdc`, `AGENTS.md`, `README.md`, `tools/slim_agent_context.py`, `tools/convert_gp_package.py`, ignore files.
- **Next:** On Claude transition day run `export_cursor_memory.py --all` per checklist; optionally mirror build habits into `CLAUDE.md` without duplicating subject content.

### 2026-11-04 — GP image-PDF OCR (logged at season close)

- **Decided:** Image-only GP PDFs must not write an empty `content.md`. `tools/convert_gp_package.py` tries the text layer first (`pdf_text_only`), then full-page PyMuPDF OCR at 150 DPI (`pdf_ocr_tesseract`, tessdata via `fitz.get_tessdata()` or `C:\Program Files\Tesseract-OCR\tessdata`). Empty extract raises. Validate fails if `content.md` is under 40 characters. This recovered 2025 A-level P1 QP, P2 QP, P2 insert, and `AQ examples condensed.pdf`. `Set 6 MS [Routines].docx` converted via MarkItDown once forced. GP stays markdown-only (no page rasters).
- **Decided:** README H1 GP section no longer lists missing P1 prelims or pre-2024 RI/HCI P2 as collection holes. P2 mesh and the lock list are the inventory. Optional keys only: 2024 A-level P2 ANS, Specimen ANS, 2025 A-level AQ scheme.
- **Touched:** `tools/convert_gp_package.py`, `README.md`, `converted packages/H1 GP/exam papers/TYS */2025 *`, `converted packages/H1 GP/essay resources/AQ examples condensed/`, `converted packages/H1 GP/scripts/2024 NJC prelim/`.
- **Next:** None for GP. If `--validate` is run and `2025 TJC P2 prelim` insert is locked by OneDrive, that single miss is a file lock, not a missing package. Do not reopen subject practice from this role.
