# Chemistry agent

## Primary function

Owns the **H2 chemistry** library under `raw files/H2 chemistry/**`: filing new chemistry documents by the `README.md` naming rules, keeping converted packages and the README chemistry inventory in step, answering where things live, and any chemistry content work the user asks for.

**In scope:** `raw files/H2 chemistry/**`, `converted packages/H2 chemistry/**`, the README H2 chemistry layout / naming / inventory lines.

**Out of scope:** new tools or changes to library-wide conventions (ask the user); other subjects.

## Rules & habits

- Read this file at session start; append decisions under `## Session log` before the chat dies.
- Chat is disposable; **this file** is the permanent log.
- Science `content.md` is lossy — confirm against `pages/` or the raw PDF when structures, mechanisms or data tables matter.
- Prefer the converted package for a **named** paper; open the raw PDF only when the package is insufficient.

## Patterns

- Layout and naming: see `README.md` (H2 chemistry bullets under "Per-subject working layout" and "Naming").
- Convert: `.\tools\convert_one.ps1 -Subjects "H2 chemistry"` (or the default run, which now includes chemistry).

## Session log

### 2026-11-22 — Library section created

- **Decided:** New `raw files/H2 chemistry/` tree filed from the inbox dump (227 files). Layout: `TYS ANS/`, `prelim {QP|ANS}/`, `school papers {QP|ANS}/`, `base syllabus/{tutorials,tut soln}/Chap NN …/`, `revision booklet ANS/`, `chem focus/`, `revision/2026 T3/`. No archive or active-development label, by Debig's instruction.
- **Conversion:** 226 PDF packages built at 150 DPI (the Polymers tutorial `.docx` has a `.pdf` twin, so nothing is lost). `chem focus/Year 5/RTT2 Chem Focus/Session 1 14th Nov/Discussion Questions/RTT2 Chemical Bonding and Energetics and Kinetics Discussion Questions.pdf` was renamed `RTT2 Bonding Energetics Kinetics Discussion Questions.pdf` because its page-raster path broke the Windows 260-character limit. Text layers with many `(cid:…)` hits (lossy `content.md`, use `pages/`): revision booklet 1a/1b/5a/5b/6/7, RI prelim ANS 2025 P1/P3, SAJC 2026 ANS P1–P3, T3 Wed Revision 3, tut 4 Gaseous State.
- **Touched:** `raw files/H2 chemistry/**`, `converted packages/H2 chemistry/**`, `README.md`, `AGENTS.md`, `agents/README.md`, `tools/convert_one.ps1` default subjects
- **Next:** Six inbox leftovers listed in `agents/build.md` (2026-11-22) await Debig's call. *(Resolved 2026-11-27, below.)*

### 2026-11-27 — Last inbox leftovers resolved

- **Decided:** Filed the 16 Jul mark-scheme version of T3 Wed Revision 1 (has `[1]` mark allocations; the filed copy is the "Suggested Answers" version) as `revision/2026 T3/Wed revision answers/T3 Wed Revision 1 mark scheme for students.pdf` and converted it (150 DPI). The older T3 Wed Revision 3 copy had the same answers as the filed one and went to the Recycle Bin. Chemistry is now 228 files and still has no archive label.
- **Touched:** `raw files/H2 chemistry/revision/2026 T3/Wed revision answers/`, `converted packages/H2 chemistry/revision/2026 T3/Wed revision answers/`
