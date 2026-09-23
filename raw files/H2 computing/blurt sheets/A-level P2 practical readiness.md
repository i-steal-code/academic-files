# A-level Computing 9569 — Paper 2 practical readiness sheet

# practical return · muscle memory + wiring · not theory dumps

# method: monkeytype (epoch 3) → mega-chain part (closed-book) → checkpoint PASS → re-teach traps → tick only when cold

Paper shape (A-level P2): timed practical · multi-task ladder · files/validation · OOP · S&S/ADT · sqlite · web (HTML/Flask) · niche hedges (mongo/sockets) possible in final syllabus year

RI prelim P2 is harder/bundled — use as stretch mock. Pass mark for this sheet = TYS A-level task fluency.

How to use this sheet

- Each line is a must-have *runnable* skill. Tick only when you can write it from memory and the **checkpoint prints PASS**.
- Primary modes:
  - **Monkeytype** — epoch-3 cold blocks (comments = lesson); one block per paste
  - **Mega-chain part** — closed-book cell in `P2 CHAIN A/B/C`; no boilerplate open. For B/C: do not open `_archive/*answers*` until marking; run bottom checkpoints only after attempting.
  - **Re-teach** — narrate what each line does (out loud)
  - **Dialogue** — "why not X?" / name-wiring checks
- Do not open the next **chain part** until the current checkpoint is PASS.
- Theory blurt sheets stay separate. Here, explanations support *code*, not paper-1 essays.

Boilerplate anchors (your voice — open only when marking)

- `S&S.ipynb` · `ADT.ipynb` · `DB.ipynb` · `WEB DEV.ipynb` · `POOP.ipynb` · `SOCKETS.ipynb`
- Live practice: `P2 CHAIN A - attendance.ipynb` · `P2 CHAIN B - library.ipynb` · `P2 CHAIN C - directory.ipynb`
- Chain A still has in-notebook checkpoints + keys. **B/C (and future packs):** checkpoints encapsulated at notebook bottom; answers only in `_archive/P2 CHAIN B|C - answers.ipynb`
- Archive (do not peek for fresh reps): `_archive/2026-09 SS-ADT PRACTICE`, `_archive/2026-09 WEB-SQL PRACTICE`
- Do not leave practice DBs/JSON lying around (`chain_a.db`, `library_out.json`, mongo `chain_c_db`) after a session — close DB Browser and delete/drop when done
- Typing: `monkeytype drills.txt` (epoch 3) + `monkeytype drills epoch3 source.py`
- Session log: `practical session log.md` (thin — not a code dump)

Taper rule

- Early gates = bankable P2 marks (files, sqlite, OOP, core ADT/S&S).
- Later gates = web wiring + niche hedges.
- If tired: only redo **A2–A3** (sqlite) or **B2** (LL delete) or **B4** (binary/insertion). Nothing new.

After prelim results

- Only three allowed edits: which gate leaked · extend Phase on that gate · one niche gets a second slot.
- No new master-sheet chapters from practical fails.

---



## Gate 0 — practical floor (rusty return)

Pass when: Chain **B1** (OOP) and Chain **A2** smoke (db open + seed) both checkpoint PASS once.

### Monkeytype (optional warm)

- [ ] Epoch-3: R1 recursion *or* A1 node *or* D1 db open *or* F1 flask imports



### Mega-chain

- [ ] **B1** — Resource / DigitalResource + `stock`
- [ ] **A1** — validate dirty CSVs (or at least narrate the rules cold)



### Re-teach / dialogue

- [ ] Why `(value,)` needs the comma
- [ ] Why child must not read parent `__attrs` directly
- [ ] Dialogue: "What breaks if you skip `row_factory`?"



### Your known traps

- [ ] No f-string SQL splicing
- [ ] No mutable default `Node()` in `__init__`

Gate 0 pass: ☐

---



## Gate 1 — sqlite bank (highest P2 density)

Pass when: **A2 + A3** checkpoint PASS cold (schema/seed + JOIN/HAVING/never-attended/CRUD).

### Monkeytype

- [ ] Epoch-3 D1–D3 blocks



### Mega-chain

- [ ] **A2** — `chain_a.db` Member + Attendance seed from cleaned rows
- [ ] **A3** — INNER JOIN · GROUP BY/HAVING · LEFT JOIN never-attended · parameterised CRUD



### Re-teach / dialogue

- [ ] Re-teach: WHERE vs HAVING in one sentence each
- [ ] Dialogue: "INNER vs LEFT — who disappears?"
- [ ] Dialogue: "Why GROUP BY house not only name?"

Gate 1 pass: ☐

---



## Gate 2 — S&S rigidity (corrected forms)

Pass when: **B4** checkpoint PASS (sorted keys + recursive binary). Monkeytype S3 partition if quicksort path chosen.

### Monkeytype first

- [ ] S1 BinarySearch recursive (+ iterative notes)
- [ ] S2 InsertionSort
- [ ] S3 partition + quickSort (if not using insertion in B4)
- [ ] S4 merge / mergeSort (stretch — not forced in chains)



### Mega-chain

- [ ] **B4** — extract keys → sort → BinarySearch hit + miss



### Re-teach / dialogue

- [ ] Narrate binary window shrink on a 5-element list
- [ ] Narrate why partition's **final** swap matters
- [ ] Dialogue: "What goes wrong if recursive binary uses `middle` not `middle+1`?"

Gate 2 pass: ☐

---



## Gate 3 — ADT rigidity

Pass when: **B2 + B3** checkpoint PASS (LL head-delete + HashTable + BST traversals).

### Monkeytype

- [ ] A2 linked list core
- [ ] A4 HashTable init / insert / search



### Mega-chain

- [ ] **B2** — LinkedList insert_end / search / delete head
- [ ] **B3** — HashTable separate chaining + BST in/pre/post-order



### Re-teach / dialogue

- [ ] Why `while current is not None` not `while current.get_right()`
- [ ] Why `[LinkedList()] * N` shares one object
- [ ] Dialogue: "in_order without a node argument — why does it fail?"

Gate 3 pass: ☐

---



## Gate 4 — Flask / web wiring

Pass when: **A4** checkpoint PASS + manual search/log works on port 5001.

### Monkeytype

- [ ] F1 flask wiring block



### Mega-chain

- [ ] **A4** — `portal` / `hits` / `log_absence` with `templates/chain_a/` name pairs



### Re-teach / dialogue

- [ ] Scan every name pair out loud before running
- [ ] Dialogue: "What if redirect has no `return`?"
- [ ] Dialogue: "BuildError on url_for — what mismatched?"

Gate 4 pass: ☐

---



## Gate 5 — files / validation / programming elements

Pass when: **A1** + **B5** checkpoint PASS. Add mod-11 once from `POOP.ipynb` if the paper stem needs it.

### Mega-chain

- [ ] **A1** — load + validate; rejected list; clean tuples
- [ ] **B5** — JSON save/load round-trip `library_out.json`



### Re-teach / dialogue

- [ ] Check digit purpose: transcription errors (not "lossy transfer")
- [ ] Dialogue: "extreme vs abnormal test data — one example each"

Gate 5 pass: ☐

---



## Gate 6 — niche hedges (capped)

Pass when: **C2–C4** each cleared once under soft time — then stop. (Year-7 optionality; not red.)

### Mega-chain

- [ ] **C1** — Staff + Directory (needed before migrate)
- [ ] **C2** — mongo drop / insert_many / find projection / update_one filter-first
- [ ] **C3** — Flask over mongo (`desk` / `matches_view` / `hire`, port 5002)
- [ ] **C4** — `recv_line` + server/client spine comments (runnable bonus)



### Ban after one pass

- [ ] No second week living in mongo/sockets if Gates 1–4 are red

Gate 6 pass: ☐ (optional for distinction buffer)

---



## Gate 7 — full paper dress rehearsal

Pass when: 2× TYS P2 (prefer **2020–2022**) + 1× later year or RI P2 stretch, post-mortem = only rigidity leaks.

### Paper loop

- [ ] Timed paper A (2020–22 bias)
- [ ] Timed paper B (2020–22 bias)
- [ ] Contrast paper (2023–24 or RI)
- [ ] After each: list failed gate numbers only; redo that **chain part**; do not "redo whole syllabus"

Gate 7 pass: ☐

---



## Daily card (practical)



### Always-bank (every session)

- [ ] One **A2 or A3** query/seed fragment cold *or* checkpoint redo
- [ ] One **B2 or B4** fragment (LL delete *or* binary/insertion)
- [ ] Gate 4: narrate name-wiring for `portal`→`hits` (even without coding)



### Rotate (one per session)

- [ ] Monkeytype 1–2 epoch-3 cold blocks
- [ ] **A1** validation rules aloud
- [ ] **B3** in_order three-liner
- [ ] **C4** recv_line once if Gate 6 open



### Ban list until Gates 1–4 green

- [ ] New niche topics beyond Gate 6 cap
- [ ] Re-reading boilerplates without a chain-part attempt
- [ ] Opening `_archive/*answers*` (or Chain A keys) before checkpoint
- [ ] Leaving `chain_a.db` / `library_out.json` / mongo practice DBs open or undeleted after a session
- [ ] 34-minute full monkeytype dumps (epoch-1 style)
- [ ] Expanding master sheet instead of fixing a failed part

---



## Dialogue prompt bank (practical)

1. Write binary search recursive — now change it to iterative without looking.
2. Partition this array aloud; where is the pivot at the end?
3. Delete the head of a linked list — what line is mandatory?
4. Why does `[LinkedList()] * N` fail? Fix it.
5. WHERE vs HAVING — give one illegal and one legal query.
6. Trace form `member_name=` → `request.form` → `url_for("hits")` → route param.
7. What happens if `redirect` is not returned?
8. Child `describe` needs parent id/title — show the safe way.
9. LIKE search — show the parameter tuple with wildcards.
10. Never-attended list — why LEFT JOIN and why `IS NULL`?

---



## Session log protocol

After a cold session, append one entry in `practical session log.md` (not a full code paste):

1. **Chain + part** (e.g. A3)
2. **Checkpoint** PASS / FAIL
3. **Traps** — only real fails (one line each)
4. **Next** — same part if FAIL; else next dependent part + one always-bank item

Do not rewrite this readiness sheet after one bad day.

---



## Score map (how gates buy P2)


| Gates passed | What you have secured                         |
| ------------ | --------------------------------------------- |
| 0 only       | Can start a file; still blank on tasks        |
| 0–1          | sqlite bank — largest typical practical swing |
| 0–3          | Core algorithms + ADT — S1 practical covered  |
| 0–4          | Web tasks no longer free marks left behind    |
| 0–5          | Files/validation/JSON craft                   |
| 0–6          | Niche shock absorber (mongo/sockets)          |
| 0–7          | Exam pacing proven on full papers             |


Target for A-level: **Gates 0–4 green, Gate 5 mostly, Gate 6 once, Gate 7 started.**  
RI P2 mocks: same gates; expect bundling — do not move Gate 6 ahead of 1–4.

---



## Final week card (no new niches)

Chain parts only:

1. A2 + one A3 query (JOIN or HAVING)
2. B4 binary + insertion **or** S3 partition final swap
3. B2 LL delete including head
4. A4 narrate `portal`→`hits` name wiring (run if time)
5. A1 validation rules if weak

Then stop. Sleep beats one more mongo tutorial.
