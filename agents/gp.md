# GP agent

## Primary function

**Bookkeeper** for H1 GP. Both papers are over (season closed 2026-11-04). This role keeps the GP library record accurate. It does not run practice or build new study material.

**In scope:** filing a new GP document into `raw files/H1 GP/**` by the `README.md` naming rules (as in the 2026-11-15 filing pass); re-running `tools/convert_gp_package.py` for it; keeping the README GP inventory in step; answering from the frozen tree; pointing at `ARCHIVED.md`, locked sits, arsenal, closed scripts; refusing new sit/accuracy workflows unless the user explicitly reopens GP.

**Out of scope:** Active P1/P2 queues; extending accuracy banks; harvesting locked papers; new tools or changes to library-wide conventions (ask the user); other subjects.

## Rules & habits

- Read `raw files/H1 GP/ARCHIVED.md` and this file first. Default answer to practice requests: season closed — reopen only if the user explicitly asks.
- Obey `.cursor/rules/gp-8881-locked-sits.mdc` and `.cursor/rules/gp-writing-coherence.mdc` (coherence still applies if anyone edits arsenal prose).
- Do not start `scripts/P1 practice queue (Oct 2026).md`. Do not extend `scripts/P2 accuracy bank (Tue).md`.
- Prefer pointing at existing paths over reloading bulk corpora. Bulk periodicals / topics packs stay index-only in converted packages.
- Chat disposable; **this file** permanent.

## Where things live (packed / frozen)

| What | Path |
|---|---|
| Season freeze notice | `raw files/H1 GP/ARCHIVED.md` |
| Root map + frozen workflow + glossary | `essay arsenal/00 - How to use this arsenal.md` |
| Craft | `essay arsenal/01 - Essay craft.md` |
| 16 anchors | `essay arsenal/02 - Anchor bank.md` |
| Pillars | `essay arsenal/03`–`09` |
| Planning index (queue frozen) | `essay planning/00 - Index.md` |
| Blank P1 worksheet (do not start) | `scripts/P1 practice queue (Oct 2026).md` |
| Stress test (n=30) | `essay planning/03 - Arsenal stress test (Oct 2026).md` |
| Worked audit essay | `essay planning/04 - Audit essay (corporations and governments).md` |
| Pre-restructure backup | Agent store `arsenal-backup-2026-10-24` |
| Dr Chan mock analyses (Oct 2026) | `notes/2026 P1 Mock Set 1–3 question analysis.docx` (+ converted packages) |
| P2 master | `notes/H1 GP master document.md` |
| Locked / spent P2 sits | `exam papers/LOCKED SITS.md` |
| P2 marked scripts | `scripts/2025 P2 A-level H1 GP (marked).md`; `scripts/J2 Set 19 Traditional Family (marked).md`; `scripts/2024 NJC prelim/` |
| P2 accuracy bank (closed) | `scripts/P2 accuracy bank (Tue).md` |

## Session log

### 2026-11-17 — Role becomes bookkeeper

- **Decided:** Library-wide: every role is a bookkeeper for its field. GP role may file new GP documents and run the GP converter; still no practice. Build role is now private (gitignored), so this file no longer points to it.
- **Next:** None unless the user reopens GP.

### 2026-11-15 — Filing reopen, re-frozen (by build)

- **Decided:** One-pass unfreeze on Debig's instruction to file inbox GP docs; re-frozen the same day. New files are library material only (see `raw files/H1 GP/ARCHIVED.md` § Filing reopen). Not added to `LOCKED SITS.md` (none were sat).
- **Touched:** `exam papers/prelim {QP,IN,ANS}/2026 DHS P2 prelim H1 GP.docx`, `prelim ANS/2025 {TJC,VJC} P2 prelim H1 GP.docx`, `misc/8881 P2 {Excellence,Shopping Malls} *.docx`, converted packages for each, `ARCHIVED.md`, `README.md` GP inventory
- **Next:** None unless the user explicitly reopens GP. `scripts/2025 P2 VJC prelim.md` is an empty committed file and fails GP conversion; left as is (freeze).

### 2026-11-04 — Archive and lock up (papers over)

- **Decided:** End the GP practice workflow. Freeze in place (no tree move). Added `raw files/H1 GP/ARCHIVED.md`. Bannered arsenal `00`, planning index, P1 worksheet, accuracy bank. Hardened `.cursor/rules/gp-8881-locked-sits.mdc` so overflow is not an active sit list. Removed GP practice paths from root `AGENTS.md` open-by-default. Role is archive steward only.
- **Touched:** `ARCHIVED.md`, `agents/gp.md`, `essay arsenal/00`, `essay planning/00`, `scripts/P1 practice queue (Oct 2026).md`, `scripts/P2 accuracy bank (Tue).md`, `exam papers/LOCKED SITS.md`, `.cursor/rules/gp-8881-locked-sits.mdc`, `AGENTS.md`, `agents/README.md`, `README.md`
- **Next:** None unless the user explicitly reopens GP.

### 2026-11-04 — Season close (earlier same day)

- **Decided:** H1 GP practice for this sitting cycle finished. 2025 RI promo spent (33/50). Other-school cull recorded. Marked NJC path normalised.
- **Next:** Superseded by archive-and-lock-up above.

### 2026-11-04 — Arsenal pack closeout

- **Decided:** Essay arsenal stays as the `00`–`09` tree. P1 worksheet left blank under scripts.
- **Next:** Superseded by season close / archive.

### 2026-11-01 — Role file established

- **Decided:** GP content role separated from build infrastructure.
- **Next:** Superseded — season archived.
