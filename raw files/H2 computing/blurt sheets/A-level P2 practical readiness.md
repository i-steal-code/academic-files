# A-level Computing 9569 — Paper 2 practical readiness

# method: finish a stem's own test → checkpoint → only then a full paper

**Now:** 2025 A-level P2 sat Mon 5 Oct in 3h under exam conditions. Building finished at 2h 25m, then 35 minutes of sweep, which found and fixed the linear-probing wrap in 4.3. About 90/100 (strict ~87), the best paper this cycle. The one real loss is `find_record`: it returns whatever is in the hash slot without checking the key, so searching for 475 printed `key: 175 | data: heavy`. No more papers. Taper to Wed 7 Oct, report 07:30, paper 08:00–11:00.

**Goal:** the highest mark on the day. On the day nobody marks your work before 11:00, so the last 30 minutes must find the errors as well as fix them.

---

## Score history

| Paper | Conditions | Mark |
|-------|-----------|------|
| 2026 RI TP | timed | 25 |
| 2024 HCI prelim | 3h | ~60 |
| 2021 A-level | timed, 10 min spare | ~77 (strict ~70) |
| 2022 A-level | 2h 30m first pass | ~60 |
| 2022 A-level | plus marked fixes, 2h 52m | ~83 |
| 2023 Task 2 only | 38 min, poor conditions | ~16–18 / ~25 |
| 2024 A-level | 3h 00m, no sweep | ~57 |
| 2024 A-level | plus evening fixes + `datetime` | ~72 |
| 2025 A-level | 2h 25m build + own sweep | ~90 (strict ~87) |

The range across the A-level papers is about 57 to 90. On papers where every task uses a familiar structure (2025: stack, inheritance, SQL join, hash table), you now finish with time to check. On papers with a step that looks new (2024: writing a file, adding days to a date), the stuck rule below decides the mark.

## What 2025 showed

| Task | Mark | Note |
|------|------|------|
| 1 Stack binary | 20 / 20 | `push` grows the list, `pop` returns the data with the pointer and `False` when empty, all three tests correct, including `46967` → `1011011101110111` |
| 2 Room game | ~37 / 38 | All four classes, `super()`, file → objects, both input loops, all 14 test inputs reach the Finish room. The door wording differs from the stem's example ("there is door in direction N" instead of "There is a door to the North"). |
| 3 Social DB | ~15 / 17 | Keys correct, four blocked comments correct. 3.3 is top-level code rather than the function the stem asks for. 3.2 shows no output for "Run your program". |
| 4 Hash table | ~16 / 19 | Initialise, hash, insert with wrap and full check, `read_data` with failure message: all correct. `find_record` does not probe and does not compare keys, and returns the whole record instead of the string. |
| Style | ~5 / 6 | |

The 4.6 output showed the mistake: you searched for 475 and it printed key 175. Item 2 of the contract check (write the expected output first) catches this in ten seconds. The sweep checked the code but not the printed output against what you asked for.

## Recurring leaks across the cycle

| Leak | Papers | The check that catches it |
|------|--------|---------------------------|
| A novel rule coded from memory instead of from the stem | HCI, 2021, 2022, 2024 Task 1 (2025 Task 1 was correct) | Copy each rule bullet as a `#` comment and code under it; hand-check one example |
| Output printed but never compared with what was asked | 2022 Caesar, 2024 4.4, 2025 4.6 | Write the expected output before running; compare the key or value you asked for |
| Happy path only | 2021 delete, 2023 queue wrap | Call the empty, missing and wrap cases once |
| Stuck on one unfamiliar step | 2024 3.4, 4.3 | Five-minute rule and fallback table |
| Stem asks for a function, code is top-level | 2024 1.4, 2025 3.3 | Tick "Write a function" bullets: there must be a `def` and a call |

## Raw timelines — 2024 vs 2025

### 2024 A-level · Sun 4 Oct · 13:40–16:40 · no sweep · ~57

Clock times are from the first dump on the day (later evening fixes overwrote some mtimes).

| Clock | T+ | What the files show |
|-------|-----|---------------------|
| 13:40 | 0:00 | Start |
| 13:40–15:13 | 0:00–1:33 | No saved artifact. Reading + building without a checkpoint save. |
| 15:16 | 1:36 | `business.db` — Task 4 schema exists |
| 15:50 | 2:10 | `TASK1` saved — card game done |
| 16:35 | 2:55 | `TASK2` saved — number tree done (~45 min of clean work) |
| 16:39–16:40 | 2:59–3:00 | `TASK3` and `TASK4` saved incomplete: no `.html`, no `Villa_Booking` rows, 4.4 stub |

**Order inferred:** Task 4 schema early → Task 1 → Task 2 → Task 3 and Task 4.3/4.4 left for the last five minutes.

**Where the paper crashed:** the last ~25 minutes of the build window were still on Task 2. Tasks 3 and 4 never got a simple running version. The curveballs (write `.html`, add days to a date) were met by searching for the “right” API instead of a fallback, and there was no sweep because building ran to the bell.

### 2025 A-level · Mon 5 Oct · 3h · build stop at 2h 25m · ~90

Absolute start clock was not stated. From your timing: build done at 2h 25m, then 35 minutes of sweep. `database.db` at 20:16 and all notebooks batch-saved 22:38–22:39 put the sitting in the evening, ending near 22:40.

| T+ | What happened |
|----|----------------|
| 0:00 | Start |
| ~0:30–0:40 | `database.db` — Task 3 schema early (SQL banked while fresh) |
| 0:40–2:25 | Tasks 1, 2, 4 built; Task 2 game path completed with all 14 inputs |
| 2:25 | Last task finished. Sweep begins. |
| 2:25–3:00 | Own sweep. Found and fixed 4.3 wrap-around probing. Did not catch `find_record` returning the wrong key (175 instead of 475). |
| 3:00 | Notebooks saved. |

**Order inferred:** Task 3 early (banked), then the ADT/OOP tasks; hash table last; deliberate sweep.

**Where this paper held:** every task had a running simple version by 2h 25m. The sweep existed. One output-vs-input check was skipped.

## Side-by-side

| | 2024 (~57) | 2025 (~90) |
|---|---|---|
| Familiar structures | Tree, bubble, SQL create/load | Stack, inheritance, SQL join, hash insert |
| Curveballs | File write + date arithmetic | None of that kind; hash find needed probing |
| First artifact | 1h 36m | ~35 min |
| Two tasks with output | by ~2h 55m (Task1+2) | well before 2h 25m |
| Last 30–35 min | still building 3 and 4 | own sweep |
| Incomplete chains | 3.4, 4.3, 4.4 | none incomplete |
| Sweep finds | 0 (no sweep) | 1 of 2 real bugs |

## What went well in both

- **SQL create + load** lands early and holds when you touch it (2024 4.1/4.2, 2025 Task 3).
- **Array / tree / OOP structures you have drilled** finish with output once started (2024 Task 2; 2025 Tasks 1 and 2).
- **Execution counts stay low when the path is clear** (2025 Task 1: cells 1→2→3). High counts mark thrashing (2024 Task 4.3 cell ran to exec 22; 2025 Task 3.3 to exec 10).

## What crashed — and what would have changed it

**2024 failure mode: stuck without a simple version.**
- At **T+2:00** you already had Task 1 and Task 4 schema. Cap for Task 2 at that point should have been ~40–45 min (it took ~45 and scored ~20). Fine.
- At **T+2:30** Task 2 should have been force-saved. The remaining 30 minutes had to produce *something* for Task 3 and Task 4: `open(name+'.html','w')` with no edge cases, and date insert that ignores month rollover. That alone would have lifted the paper into the mid-60s/70s before any sweep.
- Searching for `distutils` / perfect `datetime` past **five minutes** was the decision that wiped Task 3.4 and 4.3–4.4.

**2025 near-miss: sweep checked code, not printed evidence.**
- Stopping build at 2h 25m was correct. The wrap fix in 4.3 proves the sweep can find logic bugs.
- What was missing: for 4.6, write “expect key 475 → law” before looking at the print. The print said key 175. That is a ten-second catch.

## Plan for Wednesday if 2026 has curveballs

You cannot remove curveballs. You can stop them from eating the dependent chain.

1. **Open (5 min).** Read all four tasks. Mark each as *bank* (SQL create/load, Flask join page, sorts, stack, class+file) or *curveball* (novel rules, unfamiliar library, new ADT variant). Write a time cap at 1.6 min/mark on each.

2. **Order: bank → bank → curveball → remaining.** Do your two strongest familiar tasks first until each has saved output. In this cycle that has been SQL and whichever of sort/tree/OOP/stack looks closest to drill. Leave the curveball until you have ~90–100 minutes of banked output, or until its own cap — whichever comes first.

3. **Curveball rule (non-negotiable).**
   - Minute 0–5: try the obvious API / Quick Reference.
   - Minute 5: switch to the fallback table (`open`, month-length list or `date+timedelta`, `%`, etc.).
   - Ship a **simple version that runs** before polishing edge cases.
   - Write the next dependent subtask in full even if upstream data is thin.

4. **Hard gates on the clock.**
   - **09:30 (T+1:30):** at least two tasks with visible output.
   - **10:15 (T+2:15):** every task attempted; every dependent part at least stubbed with a call and a test.
   - **10:30 (T+2:30):** stop building. Sweep starts even if a curveball is ugly.

5. **Sweep script (10:30–10:55).** For each notebook: (a) tick stem bullets against `def`s; (b) for every printed result, say out loud the input and the expected value, then look; (c) check named files exist and size > 0; (d) one empty/miss/wrap call where the stem names that case.

**Strengths to play forward:** SQL schema+seed+join, OOP with `super()`, file→objects, stack/queue/hash *insert*, sorts, saving a page.  
**Weaknesses to contain, not “solve” mid-paper:** novel Task 1 rules (copy bullets as comments), unfamiliar stdlib (5-minute fallback), find/search after probe (compare the key you asked for with the key that printed).

That is the whole strategy: bank marks on known shapes first, force a running simple version on anything new by five minutes, and spend the last half hour reading outputs against inputs — the check that would have turned 2024 into a mid-70 and 2025 into the mid-90s.

## Fallbacks to know cold

| Stem asks | Fallback |
|-----------|----------|
| Write a file with a given extension | `with open(name + '.html', 'w') as f: f.write(text)` |
| Read the lines of a file into a list | `[line.strip() for line in open(fname)]` |
| Parse `'05-Jan'` | `day, mon = s.split('-')` and `int(day)`, or `datetime.datetime.strptime(s + '-2025', '%d-%b-%Y').date()` |
| Add `i` days to a date | `(start + datetime.timedelta(days=i)).strftime('%d-%b')` |
| Add days without `datetime` | month lengths `[31,28,31,30,31,30,31,31,30,31,30,31]`; add 1 to the day, and when it passes the month's length set it to 1 and add 1 to the month |
| Hash find with linear probing | start at the hash; while the slot is not empty and fewer than `s` slots checked, compare `int(slot[0]) == int(key)`; step `(index + 1) % s` |
| Leaf count of a full binary tree | `2 ** (levels - 1)`; total nodes `2 ** levels - 1` |
| Sort by two keys without built-ins | compare the first key; if equal, compare the second key of **both** items |

## Contract check — after every subtask, about one minute

1. Tick each bullet in the stem against a line of code. "Write a function" means a `def` and a call.
2. Run the paper's own worked examples and given test data. Write the expected output first, then compare it with what printed.
3. For each function whose return the stem names, print `repr(result)` and `type(result)` once.
4. For each method the driver does not call, call the head, missing, and empty case once. Leave those lines in.
5. Turn each data warning in the stem into one query for that row.
6. Traversals: in-order is sorted, pre-order starts with the root, post-order ends with the root.
7. Files the stem names (`.html`, `.txt`, `.db`): check that they exist and are not empty.

## Mon 5 Oct — done

- 2025 full paper (~90). No more full papers. Leave 2020 and 2023 unopened.
- Tonight: no corrections. Sleep now.

## Tuesday rewrite list — blank cell, closed book, about 60 minutes, each one run

1. **Hash find with probing:** rebuild the 2025 table from `records.txt`, then `find_record(475)` must return `'law'` and a missing key must return `False`.
2. **Date expansion and availability:** Dolphin, 8 Apr, 4 days must give `08-Apr … 11-Apr`, with `10-Apr` and `11-Apr` unavailable. Use `start + timedelta(days=i)` and compare against `[row['date'] for row in rows]`.
3. **File write:** write two `.html` files with `with open`, then check both sizes are above 0.
4. **Two-key bubble sort:** number, then `red, green, blue`. Test equal numbers in all three colours.
5. **Circular queue probe:** enqueue 4, dequeue 2, enqueue 2, print from `headPointer`.
6. **Linked-list delete:** head, missing (no crash), empty.

Stop at 60 minutes even if the list is unfinished. Do not open a paper.

## Tuesday 6 October

- 06:15 wake, to move your body clock towards an 08:00 start
- 13:30–14:30 rewrite list
- 14:30–14:45 read the stuck rule, the fallbacks, the contract check and the exam-room rules, once
- afternoon: walk, rest, normal meals
- 18:30 dinner
- 20:30 screens off; pack the student pass, an approved calculator, water, a jacket
- 21:45 lights out

## Wednesday 7 October

- 06:00 wake
- 06:15 breakfast you eat on normal days
- leave with the commute plus 15 minutes spare
- 07:30 report
- 07:30–08:00 no code. Rehearse the opening: read the whole paper, set each task's time cap, choose the fastest task first.
- 08:00–08:05 read every task, write down each cap at 1.6 minutes per mark
- 08:05 start the task you are fastest at; leave any task with an unfamiliar structure for last
- about 09:30 two tasks finished, each with its output
- 10:30 stop building. Every task has at least its simple version running.
- 10:30–10:55 own sweep: contract check on every subtask; read each printed output against the input you gave; run each notebook from top to bottom; check the saved pages, files and file names
- 10:55 save everything
- 11:00 end

## Exam-room rules

- Open Flask as `http://127.0.0.1:<port>/`. Typing `https` gives a 400 before your route runs.
- Name each file exactly as the stem says, before writing code in it.
- Run the contract check after each subtask.
- Five minutes per unfamiliar step, then use the fallback.
- Build the simple version first. Every dependent part must be able to run.
- When a task's cap is reached, save and move on. Come back in the sweep.

### Ban

New topics. Any full or timed paper before Wednesday. Prelim papers. Sockets. Mongo. Coding after 15:00 on Tuesday.

---

## Quick pointers

- Last paper: `computing practical/2025 P2 A-level H2 computing/output files`
- History: 2024, 2022, 2021 A-level; 2023 Task 2; Chains A–D, LINK, TAPER, 2024 HCI
- Voice refs when marking: `S&S` · `ADT` · `DB` · `WEB DEV` · `POOP`
- Log: `practical session log.md`

---

## Banked

| Gate | Status | Note |
|------|--------|------|
| Create tables with keys, load CSV files | holding | 2021, 2022, 2024, 2025 |
| SQL joins and filters | holding | 2021, 2022, 2025 (blocked-user comments) |
| Web page with saved result | holding | 2024 HCI, 2021, 2022 |
| Stack with top-of-stack pointer | holding | 2025 Task 1, full marks |
| OOP inheritance with `super()` and private attributes | holding | 2025 Task 2 |
| File rows → objects of the right class | holding | 2025 Task 2.2 |
| Input loop until valid | holding | 2025 door and answer loops; 2022 menu fixed |
| Hash table insert with linear probing and wrap | holding | 2025 4.3, fixed in your own sweep |
| Hash table find with probing and key compare | open | 2025 4.5: returns the hash slot without comparing keys |
| SQL from computed data (date expansion) | holding after fix | 2024 4.3: 242 rows |
| Availability check against expanded dates | open | 2024 4.4 |
| Writing an output file the stem names | holding after fix | 2024 `test.html`; check size above 0 |
| Bubble sort, merge sort, recursive binary search | holding | 2022 |
| Two-key sort | open | 2024 1.3 compares one item with itself |
| Array-of-nodes tree, BST traversals | holding | 2024 Task 2, 2022 Task 3 |
| Circular queue structure | open | 2023 Task 2 wraparound print |
| Linked-list delete | open | 2021 missing-value delete |
| Novel spec rule in Task 1 | improving | wrong on the first pass 2021–2024; 2025 Task 1 correct |
| sockets | closed | absent from TYS 2020–2025 |

**Target on Wednesday:** every task has its simple version running by 10:30, and the sweep compares every printed output with the input that produced it.
