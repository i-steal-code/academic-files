#!/usr/bin/env python3
"""Short taper before the next timed paper. Last-index sorts, list edges, SQL changes."""

from __future__ import annotations

import uuid
from pathlib import Path

import nbformat
from nbformat.v4 import new_code_cell, new_markdown_cell, new_notebook

ROOT = Path("computing practical/Boilerplates")
ARCHIVE = ROOT / "_archive"


def cid() -> str:
    return uuid.uuid4().hex[:8]


def md(source: str):
    return new_markdown_cell(source=source.strip("\n") + "\n", id=cid())


def code(source: str):
    return new_code_cell(source=source.strip("\n") + "\n", id=cid(), execution_count=None, outputs=[])


def write_nb(path: Path, cells: list) -> None:
    nb = new_notebook(
        cells=cells,
        metadata={"kernelspec": {"display_name": "Python 3", "language": "python", "name": "python3"}},
    )
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(nbformat.writes(nb), encoding="utf-8", newline="\n")
    print("wrote", path.name, len(cells), "cells")


def build() -> None:
    cells = [
        md(
            """
# TAPER — last index, list edges, SQL changes

Closed-book. This is the gate before the next timed paper. A part is done when its test has been executed and the print is still in this notebook.

**Rules**
- Do not call `sorted` or `list.sort`.
- The empty case, the one-item case, and the last position are part of the answer.
- Checkpoints are at the bottom. Answers are only in `_archive/TAPER - answers.ipynb`.
- Copy the identifiers below. Do not reuse names from LINK, HCI, or the chains.
"""
        ),
        md(
            """
---
## T1 — insertion and bubble, including the last element

`batch` is the starting list. It is in reverse order, and `40` appears twice.

`InsertionSort(records)` returns a new list, sorted by score ascending. When two scores are equal, the record that appears earlier in `records` stays earlier. The input list must be unchanged.

`BubbleSort(records)` returns a new list, sorted by score descending, with the same rule for equal scores. The input list must be unchanged.

Both functions must return `[]` for an empty list and a one-item list unchanged.

**Test you must run and leave visible:**
- `print(InsertionSort(batch))`
- `print(BubbleSort(batch))`
- `print(InsertionSort([]))`
- `print(BubbleSort([("Z", 1)]))`
- `print(batch)` after both sorts, so the original order is still there
"""
        ),
        code(
            '''
# T1 — YOUR ATTEMPT
# identifiers: batch, InsertionSort, BubbleSort

batch = [("E", 10), ("D", 40), ("C", 20), ("B", 40), ("A", 5)]
'''
        ),
        md(
            """
---
## T2 — linked list edges, before the middle case

`Slip(num)` stores a private `num` and a private next slip. Provide `getNum`, `getNext`, `setNext`.

`Rack` starts empty.

`IsEmpty()` is `True` only when the rack has no slips.

`Add(num)` inserts in ascending order:

- empty rack: the new slip becomes first
- smaller than the first: it becomes the new first, and the old first follows it
- larger than every slip: it becomes the last slip
- duplicate `num`: print `Duplicate` and insert nothing
- otherwise: insert between two slips

`Remove(num)` returns `True` when a slip was removed and `False` when it was not:

- empty rack
- the first slip
- the last slip
- a number that is not in the rack

`Items()` walks with `getNext` and returns a list of numbers.

**Test you must run, in this order:** `Add` 30, 10, 40, 20, then 10 again. `Remove` 10, then 40, then 99. Print `Items()` after the adds and after each remove. Print `IsEmpty()` on a new empty rack.
"""
        ),
        code(
            '''
# T2 — YOUR ATTEMPT
# identifiers: Slip, Rack, bay

bay = None
'''
        ),
        md(
            """
---
## T3 — an UPDATE and a DELETE that a second connection can see

Use the file `taper_jobs.db`. Table:

`Job(job_id INTEGER PRIMARY KEY, status TEXT)`

Seed job ids `1, 2, 3, 4`, each with status `open`.

`MarkDone(conn, job_id)` sets that one job to `done` and commits. Every other job stays `open`.

`Cancel(conn, first_id, second_id)` deletes those two job ids and commits. Every other job stays. The condition must name the column for each placeholder.

`Remaining(conn)` returns the surviving job ids in ascending order.

**Test you must run:** seed, `MarkDone` on `2`, print every `(job_id, status)`, `Cancel` 1 and 3, print `Remaining`.
"""
        ),
        code(
            '''
# T3 — YOUR ATTEMPT
# identifiers: MarkDone, Cancel, Remaining
import sqlite3
'''
        ),
        md(
            """
---
# Checkpoints

Run after the attempts. A FAIL means that part has no evidence yet. The SQL checkpoint removes `taper_jobs.db` when it finishes.
"""
        ),
        code(
            '''
# CHECKPOINTS — TAPER
import os
import sqlite3

PARTS = ("T1", "T2", "T3")


def _check_t1():
    for fn in (InsertionSort, BubbleSort):
        src = fn.__code__.co_names
        if "sorted" in src or "sort" in src:
            return False, "sorted or list.sort is not allowed"
    original = [("E", 10), ("D", 40), ("C", 20), ("B", 40), ("A", 5)]
    got_i = InsertionSort(original)
    if original != [("E", 10), ("D", 40), ("C", 20), ("B", 40), ("A", 5)]:
        return False, "InsertionSort changed its input"
    if got_i != [("A", 5), ("E", 10), ("C", 20), ("D", 40), ("B", 40)]:
        return False, f"InsertionSort is {got_i}"
    got_b = BubbleSort(original)
    if got_b != [("D", 40), ("B", 40), ("C", 20), ("E", 10), ("A", 5)]:
        return False, f"BubbleSort is {got_b}"
    if InsertionSort([]) != [] or BubbleSort([]) != []:
        return False, "empty list must return []"
    if InsertionSort([("Z", 1)]) != [("Z", 1)] or BubbleSort([("Z", 1)]) != [("Z", 1)]:
        return False, "one-item list must come back unchanged"
    return True, "ok"


def _check_t2():
    rack = Rack()
    if rack.IsEmpty() is not True:
        return False, "empty rack must be empty"
    rack.Add(30)
    rack.Add(10)
    rack.Add(40)
    rack.Add(20)
    if rack.Items() != [10, 20, 30, 40]:
        return False, f"after adds, Items is {rack.Items()}"
    rack.Add(10)
    if rack.Items() != [10, 20, 30, 40]:
        return False, "duplicate was inserted"
    if rack.Remove(10) is not True or rack.Items() != [20, 30, 40]:
        return False, f"head remove left {rack.Items()}"
    if rack.Remove(40) is not True or rack.Items() != [20, 30]:
        return False, f"last remove left {rack.Items()}"
    if rack.Remove(99) is not False:
        return False, "missing number must return False"
    if Rack().Remove(1) is not False:
        return False, "remove on an empty rack must return False"
    if Rack().IsEmpty() is not True:
        return False, "a new rack must be empty"
    return True, "ok"


def _check_t3():
    path = "taper_jobs.db"
    if os.path.exists(path):
        os.remove(path)
    conn = sqlite3.connect(path)
    conn.execute("CREATE TABLE Job(job_id INTEGER PRIMARY KEY, status TEXT)")
    conn.executemany("INSERT INTO Job VALUES (?, ?)", [(1, "open"), (2, "open"), (3, "open"), (4, "open")])
    conn.commit()
    MarkDone(conn, 2)
    other = sqlite3.connect(path)
    rows = list(other.execute("SELECT job_id, status FROM Job ORDER BY job_id"))
    other.close()
    if rows != [(1, "open"), (2, "done"), (3, "open"), (4, "open")]:
        conn.close()
        return False, f"MarkDone visible rows are {rows}"
    Cancel(conn, 1, 3)
    check = sqlite3.connect(path)
    left = [r[0] for r in check.execute("SELECT job_id FROM Job ORDER BY job_id")]
    check.close()
    conn.close()
    os.remove(path)
    if left != [2, 4]:
        return False, f"Cancel left {left}"
    return True, "ok"


_CHECKS = {"T1": _check_t1, "T2": _check_t2, "T3": _check_t3}
for part in PARTS:
    try:
        ok, detail = _CHECKS[part]()
    except Exception as e:
        ok, detail = False, str(e)
    print(f"{part}: {'PASS' if ok else 'FAIL — ' + detail}")
'''
        ),
    ]
    write_nb(ROOT / "TAPER drill.ipynb", cells)
    _answers()


def _answers() -> None:
    cells = [
        md("# TAPER — answers\n\nOpen only when marking."),
        md("## T1"),
        code(
            '''
def InsertionSort(records):
    arr = [row for row in records]
    for i in range(1, len(arr)):
        current = arr[i]
        j = i - 1
        while j >= 0 and arr[j][1] > current[1]:
            arr[j + 1] = arr[j]
            j -= 1
        arr[j + 1] = current
    return arr

def BubbleSort(records):
    arr = [row for row in records]
    n = len(arr)
    for i in range(n - 1):
        for j in range(n - 1 - i):
            if arr[j][1] < arr[j + 1][1]:
                arr[j], arr[j + 1] = arr[j + 1], arr[j]
    return arr

batch = [("E", 10), ("D", 40), ("C", 20), ("B", 40), ("A", 5)]
print(InsertionSort(batch))
print(BubbleSort(batch))
print(InsertionSort([]))
print(BubbleSort([("Z", 1)]))
print(batch)
'''
        ),
        md("## T2"),
        code(
            '''
class Slip:
    def __init__(self, num):
        self.__num = num
        self.__next = None

    def getNum(self):
        return self.__num

    def getNext(self):
        return self.__next

    def setNext(self, nxt):
        self.__next = nxt

class Rack:
    def __init__(self):
        self.__first = None

    def IsEmpty(self):
        return self.__first is None

    def Add(self, num):
        new = Slip(num)
        if self.__first is None:
            self.__first = new
            return True
        if num == self.__first.getNum():
            print("Duplicate")
            return False
        if num < self.__first.getNum():
            new.setNext(self.__first)
            self.__first = new
            return True
        current = self.__first
        while current.getNext() is not None and current.getNext().getNum() < num:
            current = current.getNext()
        nxt = current.getNext()
        if nxt is not None and nxt.getNum() == num:
            print("Duplicate")
            return False
        new.setNext(nxt)
        current.setNext(new)
        return True

    def Remove(self, num):
        if self.__first is None:
            return False
        if self.__first.getNum() == num:
            self.__first = self.__first.getNext()
            return True
        current = self.__first
        while current.getNext() is not None and current.getNext().getNum() != num:
            current = current.getNext()
        nxt = current.getNext()
        if nxt is None:
            return False
        current.setNext(nxt.getNext())
        return True

    def Items(self):
        out = []
        current = self.__first
        while current is not None:
            out.append(current.getNum())
            current = current.getNext()
        return out

bay = Rack()
for n in (30, 10, 40, 20, 10):
    bay.Add(n)
    print(bay.Items())
print(bay.Remove(10), bay.Items())
print(bay.Remove(40), bay.Items())
print(bay.Remove(99), bay.Items())
print(Rack().IsEmpty())
'''
        ),
        md("## T3"),
        code(
            '''
import sqlite3

def MarkDone(conn, job_id):
    conn.execute(
        "UPDATE Job SET status = ? WHERE job_id = ?",
        ("done", job_id),
    )
    conn.commit()

def Cancel(conn, first_id, second_id):
    conn.execute(
        "DELETE FROM Job WHERE job_id = ? OR job_id = ?",
        (first_id, second_id),
    )
    conn.commit()

def Remaining(conn):
    rows = conn.execute("SELECT job_id FROM Job ORDER BY job_id")
    return [r[0] for r in rows]

conn = sqlite3.connect("taper_jobs.db")
conn.execute("DROP TABLE IF EXISTS Job")
conn.execute("CREATE TABLE Job(job_id INTEGER PRIMARY KEY, status TEXT)")
conn.executemany(
    "INSERT INTO Job VALUES (?, ?)",
    [(1, "open"), (2, "open"), (3, "open"), (4, "open")],
)
conn.commit()
MarkDone(conn, 2)
for row in conn.execute("SELECT job_id, status FROM Job ORDER BY job_id"):
    print(row)
Cancel(conn, 1, 3)
print(Remaining(conn))
conn.close()
'''
        ),
    ]
    write_nb(ARCHIVE / "TAPER - answers.ipynb", cells)


if __name__ == "__main__":
    build()
