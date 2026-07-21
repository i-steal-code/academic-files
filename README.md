# academic-files
file database for LLM qualitative analysis

## conversion policy
- **H1 GP:** markdown-only (prefer `.docx` → md when both exist; PDF only if no DOCX). Text-heavy and converts cleanly.
- **Cheatsheets (Google Docs):** [experimental branch] source of truth stays in Google Docs (multi-tab). GitHub is a scheduled hourly mirror (see below). Exam papers and lecture PDFs remain manual file drops.
- **H2 math / physics / computing:** hybrid packages under `converted packages/` — raw PDF stays canonical; MarkItDown `content.md` is a lossy text index; `pages/page-NNN.png` preserves visual fidelity for equations/figures.
- Never treat science `content.md` as exam-accurate alone. Prefer md for search/chunking; open `pages/` or the raw PDF when math or diagrams matter.

how to deal with math content (syllabus):
some minor changes in qns, mark out portions of questions that are not tested in 2026 H2 math syllabus to take note of

### Google Docs cheatsheet sync
One-way Docs → GitHub. Each Doc tab becomes one raw `.docx` + one `.md` file.

**One-time setup**
1. GCP project → enable **Google Docs API** and **Google Drive API**.
2. Create a **service account** → download JSON key.
3. Share each cheatsheet Google Doc with the service account email as **Viewer**.
4. GitHub repo secret `GOOGLE_SERVICE_ACCOUNT_JSON` = full JSON key contents.
5. Set `document_id` in [`tools/docs-sync/cheatsheets.json`](tools/docs-sync/cheatsheets.json) (from the Doc URL).
6. Actions → **Sync Google Docs cheatsheets** → Run workflow (or wait for hourly cron).

**Local run**
```powershell
$env:GOOGLE_SERVICE_ACCOUNT_JSON = "C:\path\to\sa-key.json"
.\.venv-convert\Scripts\python.exe -m pip install -r tools\docs-sync\requirements.txt
.\.venv-convert\Scripts\python.exe tools\docs-sync\sync_cheatsheets.py --force
```

**Layout**
```text
raw files/H1 GP/notes/H1 GP cheatsheet/
  sync-meta.json
  tabs/{tab-slug}.docx
converted markdowns/H1 GP/cheatsheet/
  INDEX.md
  {tab-slug}.md
```

### science hybrid conversion
Requires **Python 3.10+** on PATH/`py` launcher (MarkItDown). The wrapper creates `.venv-convert` automatically.

```powershell
# setup + mass convert (math, physics, computing PDFs under raw files/)
.\tools\convert_one.ps1

# skip archived RI TP under exam papers/misc/
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

## collection target
- digitised TYS for all subjects (ANS + QP per paper)
- past 5 years prelims (2021-2025) from RI and HCI for all subjects (ANS + QP per paper)
- paper counts: math P1-2; physics P1-4 (RI prelims usually split P3 into P3A/P3B); computing P1-2 (P1 theory, P2 practical); GP P1-2 (P1 essay, P2 compre)
- ANS may appear as MS / SS / Soln(s) / Solutions in source filenames; stored under ANS folders

## naming
- TYS: `YYYY PX A-level H2 {subject}.pdf` (physics TYS ANS currently year-bundled: `YYYY A-level H2 physics.pdf`)
- prelims: `YYYY {RI|HCI} PX A-level H2 {subject}.pdf` (GP: `YYYY {RI|HCI} PX A-level H1 GP.pdf`)
- folder holds ANS vs QP (not repeated in filename); GP P2 also uses `prelim IN` / `promo IN` for comprehension inserts
- GP essay models keep readable titles under `essay resources/` (`essay - {question}.pdf`); periodicals as `YYYY KS Bull Issue N.pdf`

## missing documents
### H2 math
1. TYS QP 2016-2025 (P1 + P2) — ANS present for all
2. RI prelim QP 2021-2022 (P1 + P2) — ANS present
3. HCI prelim QP + ANS 2021-2022 (P1 + P2)

have: TYS ANS 2016-2025 P1-2; RI prelim ANS 2021-2025 P1-2; RI prelim QP 2023-2025 P1-2; HCI prelim QP+ANS 2023-2025 P1-2

### H2 physics
1. TYS QP 2016-2025 (all papers) — none present
2. TYS ANS 2025 — have year-bundled ANS 2016-2024 only (not yet split into P1-4)
3. RI prelim QP + ANS 2021-2025 entire (P1, P2, P3A, P3B, P4)
4. HCI prelim QP + ANS 2021-2025 entire (P1-4)

have: TYS ANS year-bundles 2016-2024; empty `prelim ANS`/`prelim QP` (school in filename, same as math); RI TP/CT archived under `exam papers/misc/`

### H2 computing
1. TYS 2020-2025 full sets (P1 theory + P2 practical, QP + ANS)
2. RI prelim QP + ANS 2021-2025 (P1-2)
3. HCI prelim QP + ANS 2021-2025 (P1-2)

have: empty `raw files/H2 computing`; some practical boilerplates/TPs under `computing practical/` (not normalised TYS/prelim sets)

### H1 GP
1. TYS entire (P1 essay + P2 compre, QP + ANS + P2 IN) — folders empty
2. P1 essay prelims RI + HCI 2021-2025 (QP + ANS) — none present
3. P2 compre prelims: RI 2021-2023, 2025 split set (have 2024 RI QP+ANS+IN; 2025 RI only as FULL SET in misc); HCI 2021-2023 (have 2024-2025 HCI QP+ANS+IN)
4. Promo sets are extras (not in core target): have RI Y5 Promo 2024-2025 QP+ANS+IN

have: normalised under `raw files/H1 GP/` — `exam papers/` (prelim/promo ANS|QP|IN + misc), `notes/`, `essay resources/` (KS Bull 2018–2025 + model essays), `topics + case studies/`, `misc/` (essay instance JSON)

## some thoughts
due to the sheer volume of the A levels (insane 230 marks for physics over 9.5h, 200 marks for math over 6h, 200 marks for computing over 6h) going for 700+ marks over the course of ~24.5h, it is simply not feasible to try and specialise in papers especially for the sciences.
instead, generalisation of skills would be needed; topical mastery of hard/widely applicable topics in the sciences, adaptation training (tackling tricky questions) and exam strategy. the sheer volume means that turnover rate needs to be high and pacing needs to be on-point.
