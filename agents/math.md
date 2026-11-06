# Math agent

## Primary function

Full jurisdiction over **H2 math** content and practice: topical sets, TYS/prelims, revision order, readiness artifacts. Infrastructure changes belong to the build agent.

**In scope:** `raw files/H2 math/**`, math canvases/readiness notes tied to math work, syllabus-cut marking on questions.

**Out of scope:** Repo-wide convert policy; other subjects’ substance.

## Rules & habits

- Read this file first; append session decisions here.
- Science `content.md` is lossy — confirm against `pages/` or raw PDF when equations matter.
- Chat disposable; this file permanent.

## Session log

### 2026-11-03 — Epoch 2 rebuild (pipeline + E1 hyp)

- **Decided:** Rebuilt Epoch 2: dropped all pure Normal and Sampling items. Hyp block = all Epoch 1 hyp questions (4 extras + 4 cores incl. CS5 Q3 sub) plus pipeline P1–P4 (AL 2024 P2 Q8, Zeta Q7, NJC 2026 P2 Q12, CS5 Q12). Other topic blocks unchanged. NJC/EJC still no official schemes in corpus.
- **Touched:** `tools/_build_epoch2.py`, `converted packages/H2 math/topical/Epoch 2/` (Questions, Answer Scheme, plan).
- **Next:** Drill pipeline hyp block hardest; Binomial and Corr & Reg standalone.

### 2026-11-03 — P1 spots locked on P2 board

- **Decided:** Locked Pure P1 spots: Complex, AOD, DE, AOI, calculus techniques (Diff + Int), Graphs. Unspotted Pure = open-notes night-before hedge only. Section B order: Normal → Sampling → Hypothesis Testing as one pipeline; Binomial and Corr & Reg as separate large pillars (topic-alone trivial; Corr & Reg must not merge with distribution drills).
- **Touched:** `canvases/math-p2-readiness.canvas.tsx` + `.data.json`.
- **Next:** Drill Epoch 2 along that stats order; spotted Pure under timed Sec A work.

### 2026-11-03 — Epoch 2 Paper 2 / stats pack

- **Decided:** Built Epoch 2 as a Paper-2 Section B pack (28 questions): remaining Revision Order stats cores not printed in Epoch 1, plus selected stretches for GC-heavy and explanation-heavy multi-distribution edges. Did not reprint Epoch 1 items (finish unticked E1 stats cores — especially P&C L2 and hyp — from those PDFs). Dropped thin Pure P2A top-up (NJC Maclaurin schemes missing). RI 2021 P2 Q stems use Revision Order worksheets (scanned QP has no OCR). EJC 2026 P2 Q11 kept as the flagship Normal+Binomial+grades chain; answer side notes no official scheme in corpus.
- **Touched:** `tools/_build_epoch2.py`, regenerated `tools/_scan_work/revision_order_topical.json`, `converted packages/H2 math/topical/Epoch 2/` (Questions + Answer Scheme + plan + worksheets).
- **Next:** Drill along locked P1 spots + Normal→Sampling→Hyp pipeline.

### 2026-11-03 — Post-P1 Paper 2 readiness canvas

- **Decided:** After Paper 1, spun a separate P2 board from the readiness seed: Section B (stats, 60) is the live checklist with ratings + Epoch 1 core items; Section A (pure, 40) keeps full P2A weights but focuses via user-toggled P1 spots plus a notes field until the Paper 1 autopsy arrives. Inherited pre-P1 ratings (Normal L4; P&C still L2; most other stats cores unticked). Interim Pure watch defaults to Level ≤2 / unfinished core (Functions still the clearest Sec A leak).
- **Touched:** `canvases/math-p2-readiness.canvas.tsx` (managed Cursor canvases path); seed `p2_ready_seed.json` in temp.
- **Next:** When P1 spot details arrive, mark Pure topics on the board (or paste autopsy notes) and lock the Sec A drill list; keep stats order P&C → remaining unticked cores by weight.

### 2026-11-02 — Replace 2024–2025 TYS ANS

- **Decided:** Filed new A-level H2 math P1/P2 solutions from `unfiled/` into `raw files/H2 math/TYS ANS/` as `YYYY PX A-level H2 math.pdf`, replacing the prior working copies. Rebuilt the four converted packages. Deleted the parked superseded copies (not RI-aligned mark schemes).
- **Touched:** `TYS ANS/2024–2025 P1–P2`, `converted packages/H2 math/TYS ANS/2024–2025…`
- **Next:** None for this replace.

### 2026-11-01 — Role file established

- **Decided:** Math content role separated from build infrastructure.
- **Touched:** `agents/math.md` (created).
- **Next:** Log current topical/prelim focus on first math session.

### 2026-11-01 — Pre-Paper 1 Epoch 1 review and theory-solve paper selection

- **Decided:** Reviewed student's pre-P1 Epoch 1 completion state (`math-readiness.canvas.data.json`): P1 brutal readiness rose from 35.1/100 to 76.4/100 (overall 86.4/200 to 148.7/200). Vectors (11/11 core, L4), Graphs (11/11 core, L3), Calculus/DE/Sequences core blocks all completed. Remaining P1 vulnerabilities flagged: Functions still at L2 (0/7 core done), Complex Numbers rated L3 on only 1/8 core done, and Equations/Inequalities & Foundations at L3 with 0 core check-set items ticked. Selected 4 unseen P1 papers with full QP+ANS in the corpus for pre-exam theory-solving: A-Level 2025 P1, A-Level 2023 P1 (with 2026 syllabus cuts noted), HCI Prelim 2025 P1, and A-Level 2022 P1 (or RVHS Prelim 2026 P1 + 2025 TJC/NYJC ANS).
- **Touched:** `agents/math.md`.
- **Next:** After Paper 1, pivot immediately to Paper 2 Section A/B gaps (Functions for P2A, Permutations & Combinations still at L2, and unticked Statistics core items).
