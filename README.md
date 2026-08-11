# academic-files
File database for LLM qualitative analysis.

## Resource management overview

Each subject under `raw files/` has a **working tree** (canonical, named, LLM-facing) plus an **`origin/`** vault for original imports.

| Layer | Role |
|--------|------|
| Working folders (`TYS QP` / `TYS ANS`, `prelim QP` / `prelim ANS`, `revision packages`, `exam papers/…`, `base syllabus/…`, `misc/`) | Normalised filenames; what you study and convert |
| `origin/` | Untouched import bundles (combined scans, Y6 dumps, practical resource zips as received). Not converted |
| `converted packages/` | LLM indexes mirroring the working tree (not `origin/`) |

**Bookkeeping rules**

1. New dumps go into `origin/` first (or stay there after split).
2. Split / rename into the working tree with the naming scheme below.
3. Bitwise-identical duplicates are deleted; keep the canonical path.
4. Near-duplicates (same paper, different bytes) are resolved by hand — keep the higher-fidelity copy.
5. Converters skip `origin/` and (by default with `-SkipMisc`) archived `misc/` practice.

**Per-subject working layout**

- **H2 math:** `TYS QP|ANS`, `prelim QP|ANS`, `revision packages/`, `origin/` (A-level / prelim / revision scan bundles)
- **H2 physics:** `exam papers/{TYS,prelim} {QP|ANS}`, `exam papers/misc/` (TP/CT), `base syllabus/{lect notes,tutorials,tut soln}/`, `revision packages/Chap N …/Chap N Revision Package {1|2|3}.pdf` (+ data booklet), `origin/` (revision scan bundles)
- **H2 computing:** `TYS QP/`, `prelim QP/` — P1 is a single PDF; P2 is a **package** (`…P2…/` with the PDF + `resource files/`). Timed practice under `misc/`. Imports under `origin/`
- **H1 GP:** `exam papers/{TYS,prelim,promo} {ANS|QP|IN}`, plus `essay resources/`, `topics + case studies/`, `notes/`, `misc/`, `origin/`

Reorg / dedupe helper: `python tools/reorg_subjects_origin_dedupe.py`

## Conversion policy

- **H1 GP:** markdown-only packages under `converted packages/H1 GP/` (prefer `.docx` → md when both exist for the same stem; PDF only if no DOCX). Run `python tools/convert_gp_package.py`.
- **Cheatsheets / living notes:** keep as ordinary files under `notes/`. Prefer infrequent manual drops over live API sync. Experimental Google Docs hourly sync lives on archived branch `archive/google-integration`.
- **H2 math / physics / computing:** hybrid packages — raw PDF stays canonical; MarkItDown `content.md` is a lossy text index; `pages/page-NNN.png` preserves visual fidelity for equations/figures.
- Never treat science `content.md` as exam-accurate alone. Prefer md for search/chunking; open `pages/` or the raw PDF when math or diagrams matter.

how to deal with math content (syllabus):
some minor changes in qns, mark out portions of questions that are not tested in the 2026 H2 math syllabus.

### Science hybrid conversion

Requires **Python 3.10+** on PATH/`py` launcher (MarkItDown). The wrapper creates `.venv-convert` automatically.

```powershell
# setup + mass convert (math, physics, computing PDFs under raw files/)
.\tools\convert_one.ps1

# skip archived RI TP under exam papers/misc/ (and other misc/)
.\tools\convert_one.ps1 -SkipMisc

# force rebuild / smoke test
.\tools\convert_one.ps1 -Force
.\tools\convert_one.ps1 -Limit 2
```

Package layout (mirrors raw path, stem = package folder):

```text
converted packages/H2 math/TYS ANS/2016 P1 A-level H2 math/
  content.md
  pages/page-001.png
  manifest.json
```

`converted packages/` page rasters are gitignored (local analysis artifacts). Re-run the converter after adding PDFs.

Image-only scans (many math TYS/prelim QP + revision packages) often have empty `content.md`; fidelity for LLM vision is in `pages/` (those packages were rendered at **220 DPI**; born-digital PDFs stay at 150 DPI with usable markdown).

## Collection target

- Digitised TYS for all subjects (ANS + QP per paper)
- Past 5 years prelims (2021–2025) from RI and HCI for all subjects (ANS + QP per paper)
- Paper counts: math P1–2; physics P1–4 (RI prelims usually split P3 into P3A/P3B); computing P1–2 (P1 theory, P2 practical); GP P1–2 (P1 essay, P2 compre)
- ANS may appear as MS / SS / Soln(s) / Solutions in source filenames; stored under ANS folders

## Naming

- TYS: `YYYY PX A-level H2 {subject}.pdf` (physics TYS ANS currently year-bundled: `YYYY A-level H2 physics.pdf`)
- Prelims: `YYYY {RI|HCI} PX prelim H2 {subject}.pdf` (GP: `YYYY {RI|HCI} PX prelim H1 GP.pdf`) — use **prelim**, not `A-level`, so these are not confused with national papers
- Promo (GP extras): keep `YYYY {RI|HCI} PX A-level H1 GP.pdf` under `promo *` folders (folder already marks promo)
- Folder holds ANS vs QP (not repeated in filename); GP P2 also uses `prelim IN` / `promo IN` for comprehension inserts
- Computing P2 working units are folders: `YYYY [RI ]P2 prelim H2 computing/` (or TYS `… A-level …`) containing the PDF + `resource files/`
- GP essay models keep readable titles under `essay resources/` (`essay - {question}.pdf`); periodicals as `YYYY KS Bull Issue N.pdf`

## Missing documents

### H2 math

1. HCI prelim QP + ANS 2021–2022 (P1 + P2)
2. Optional: earlier HCI coverage beyond target window

**have:** TYS QP+ANS 2016–2025 P1–2; RI prelim QP 2018–2025; RI prelim ANS 2018–2025 (including Revision Paper solns for 2018–2021); HCI prelim QP+ANS 2023–2025; chapter revision packages + data booklet

### H2 physics

1. TYS QP 2016–2025 (all papers) — none present
2. TYS ANS 2025 — have year-bundled ANS 2016–2024 only (not yet split into P1–4)
3. RI prelim 2024 entire; RI P4 QP gaps where only ANS exists; HCI prelim QP+ANS 2021–2025
4. Optional: spot-check thin chapters (e.g. RP3 Currents is short in source)

**have:** TYS ANS year-bundles 2016–2024; RI prelim QP+ANS for 2021–2023 + 2025; RI TP/CT under `exam papers/misc/`; base syllabus lect notes + tut soln Chap 1–20; `revision packages/Chap N …/` each with **two** sets (`Chap N Revision Package 2` for Ch1–11 / `Chap N Revision Package 1` for Ch12–20, plus `Chap N Revision Package 3`), data booklet at folder root. Rebuild via `tools/rebuild_physics_revision_packages.py`. Originals in `origin/`.

### H2 computing

1. TYS ANS 2020–2025; prelim ANS; HCI prelims; RI prelim 2021–2022
2. Practical resource fidelity vs origin dumps if you re-import

**have:** TYS QP 2020–2025 (P1 PDF + P2 packages with resources); RI prelim QP 2023–2025 (same shape); timed practice under `misc/`; imports under `origin/`

### H1 GP

1. TYS entire (P1 essay + P2 compre, QP + ANS + P2 IN) — folders empty
2. P1 essay prelims RI + HCI 2021–2025 — none in prelim folders
3. P2 compre prelims: RI 2021–2023, 2025 split set (have 2024 RI QP+ANS+IN; 2025 RI only as FULL SET in misc); HCI 2021–2023 (have 2024–2025 HCI QP+ANS+IN)
4. Promo sets are extras: have RI Y5 Promo 2024–2025 QP+ANS+IN

**have:** normalised under `raw files/H1 GP/` as above. Tuition dump previously unpacked via `tools/reorg_gp_tuition.py`. Markdown mirrors: `python tools/convert_gp_package.py` (skips files >40MB, e.g. gitignored 2020 KS Bull Issue 1).

## Some thoughts

Due to the sheer volume of the A levels (230 marks for physics over 9.5h, 200 for math over 6h, 200 for computing over 6h — 700+ marks over ~24.5h), specialising in whole papers is not feasible for the sciences. Prefer topical mastery of hard/widely applicable topics, adaptation training, and exam strategy with high turnover and disciplined pacing.
