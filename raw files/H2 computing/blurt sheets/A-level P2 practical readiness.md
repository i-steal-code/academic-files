# A-level Computing 9569 — Paper 2 practical readiness

# method: finish a stem's own test → checkpoint → only then a full paper

**Now:** TAPER T1–T3 passed on 2026-10-02. Next is the 45-minute keep-warm (web, one JOIN, one parent/child), then the timed paper is 2021 A-level P2.

---

## What the exam actually does, in order

1. The stem names the function, the return, the test, and the file that must show the output.
2. The next subtask calls that function. It does not get a fresh hardcoded list.
3. The mark lines for "empty", "not found", and "first position" are separate from the happy path.
4. Web and class tasks pay the identifiers written in that paper, including the saved page.

A part that stops at a signature, a sketch, or a typo in the only test call scores the lines with no evidence. That is the 2026 result (25/100): Task 4 was carried far enough to run; Tasks 1.2–1.4 and 2.1–2.4 were not; Task 3 never became the `.py` and saved pages the stem asked for.

## What changes in practice

- A drill part is finished only when its test has been executed and the output is still in the notebook.
- Write the empty, miss, and first-item case before the middle case.
- Copy this stem's identifiers. Do not reuse names from the previous notebook.
- The next part must call the previous function. No stand-in data.
- Pillars stay the A-level ones: file, sort/search, ADT, SQL, one web page with a saved result. Prelim intensity means a dependent chain and strict cases, not a warehouse, maze, or socket task.
- Sockets stay closed. Mongo is not next.

## Open now — TAPER drill

Closed-book. One notebook, three parts. The checkpoint uses reversed data, the last index, an empty list, a head delete, a last-node delete, and a second database connection.

| Part | Behaviour | Done when |
|------|-----------|-----------|
| **T1** | Insertion sort ascending and bubble sort descending. Equal scores keep earlier order. Empty and one-item lists return themselves. | Checkpoint prints `T1: PASS`, and `batch` is still in its original order |
| **T2** | Add to an empty rack, in front of the first, and after the last. Duplicate prints `Duplicate`. Remove the first, the last, a missing number, and from an empty rack. | Checkpoint prints `T2: PASS` |
| **T3** | `MarkDone` changes one row and commits. `Cancel` deletes exactly two ids, with the column named on both sides of `OR`, and commits. | Checkpoint prints `T3: PASS` |

Notebook: `computing practical/Boilerplates/TAPER drill.ipynb`. Answers: `_archive/TAPER - answers.ipynb`.

T1 and T2 are the gate. T3 is in the same sitting because an uncommitted change and a bare `OR ?` have both already dropped marks. The next timed paper stays closed until all three print PASS.

### Keep warm — web, SQL reads, OOP

These are holding. They get a short closed-book pass after the taper, not a new chain and not a paper.

One 45-minute session, once, before the timed paper:

- **Web, 15 min.** From memory: one POST field, `return redirect`, one page you write yourself with a table row. Open `WEB DEV.ipynb` only after five minutes stuck.
- **SQL read, 10 min.** One `JOIN` with `?` placeholders, then print the rows. Schema design and Mongo stay closed.
- **OOP, 15 min.** A parent with a private field, a setter that rejects an empty value, and a child that reaches the parent through `super()` and a getter. Print the rejected value.

If one of those prints is wrong, fix that cell only. Do not open a new paper to revise it.

### After the taper is cold

Timed paper: **2021 A-level P2**. It is insertion sort, quicksort, a linked list with a subclass, then SQL and a saved page. That is the first real reading of distance from 70.

### Tired rule

T1 and its four prints only.

### Ban

Resitting 2026. Resitting 2024 HCI. Drilling the warehouse task. Sockets. A new mega-chain. Opening the answer notebook before the checkpoint. Sitting 2021 before T1–T3 PASS.

---

## Quick pointers

- Live: `TAPER drill.ipynb`
- History, not the next session: Chains A–D, LINK, 2024 HCI, the three untimed prelim tasks
- Voice refs when marking: `S&S` · `ADT` · `DB` · `WEB DEV` · `POOP`
- Typing: `monkeytype drills.txt` (epoch 3)
- Log: `practical session log.md`

---

## Banked

| Gate | Status | Note |
|------|--------|------|
| Web page, SQL read, basic class | holding | 2024 HCI: form, redirect, join, saved page, `TaskNode` |
| Quicksort on a real print | holding | brightness order on that paper |
| Insertion and bubble, last index | cleared | T1 PASS, 2026-10-02 |
| Linked-list head, last, empty | cleared | T2 PASS, 2026-10-02 |
| SQL UPDATE / DELETE + commit | cleared | T3 PASS, second connection saw both changes |
| sockets | closed | absent from TYS 2020–2025 |

**Target:** T1–T3 PASS, one keep-warm session, then 2021 A-level P2. Do not add topics from the 2026 pillar mix.
