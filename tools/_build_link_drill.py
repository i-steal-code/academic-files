#!/usr/bin/env python3
"""A-level-shaped link drill. Adapted behaviour from prelim mark lines, not a prelim resit."""

from __future__ import annotations

import uuid
from pathlib import Path

import nbformat
from nbformat.v4 import new_code_cell, new_markdown_cell, new_notebook

ROOT = Path("computing practical/computing practical all boilerplates")
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
    print(f"wrote {path.name} ({len(cells)} cells)")


def build() -> None:
    cells = [
        md(
            """
# LINK drill — finish the chain (A-level shape)

This is not a resit of any prelim. The behaviours are the ones that drop marks on an A-level task ladder: a subtask is unfinished until its test has run, the empty/miss/first case is part of the answer, the next part must use the previous return, and every name is copied from this stem.

**Shape (TYS 2020–2025, not the 2026 warehouse/workshop mix):** file in → ordered records → search whose index is consumed by the next function → linked structure with an empty-list case → one web page that shows a result.

**Rules**
- Do not open `P2 CHAIN A/B/C/D` or their answers.
- Checkpoints are at the bottom. Answers are only in `_archive/LINK drill - answers.ipynb`.
- A part is done when you have executed it and the printed result is in this notebook.
- Before coding each part, copy the identifiers below into your cell. Do not rename them.

Data: `LINK_BAYS.csv`. L4 has no HTML files. You write `templates/link/desk.html` and `templates/link/lane.html` from the L4 stem.
"""
        ),
        md(
            """
---
## L1 — load and reject (file task)

`LoadBays("LINK_BAYS.csv")` returns two lists:

- `clean`: `(code, vessel, berth, tonnes:int)` 
- `rejected`: one short reason string per bad row

A row is clean only when `code` and `vessel` are non-empty and `tonnes` is an integer.

**Test you must run and leave visible:** print `len(clean)`, `len(rejected)`, and `clean[0]`.

Keep the name `clean`.
"""
        ),
        code(
            '''
# L1 — YOUR ATTEMPT
# identifiers: LoadBays, clean, rejected

clean = []
rejected = []
'''
        ),
        md(
            """
---
## L2 — order, then search, then use the index

Sort `clean` into `ordered` by `code` ascending, then `vessel` ascending. Any correct sort is fine. Do not call Python's `sorted` or `list.sort`.

`FindFirst(ordered, code)` returns the index of the **first** row with that code, or `-1`. The window must shrink. A miss must return `-1` rather than loop.

`ListVessels(ordered, code)` must call `FindFirst`. From that index, collect vessels while the code matches. If `FindFirst` returns `-1`, return `[]`. Do not scan from index 0.

**Test you must run:** 
- `FindFirst(ordered, "B07")` and `FindFirst(ordered, "Z99")`
- `print(ListVessels(ordered, "B07"))`
- `print(ListVessels(ordered, "Z99"))`
"""
        ),
        code(
            '''
# L2 — YOUR ATTEMPT
# identifiers: ordered, FindFirst, ListVessels

ordered = []
'''
        ),
        md(
            """
---
## L3 — insert into an empty chain, then in front

`Call(ref, vessel)` stores private `ref` and `vessel`, with `getRef`, `getVessel`, `getNext`, `setNext`.

`Lane` starts empty (`getFirst` is `None`). `AddCall(new_call)` inserts by ascending `ref`:

- empty lane: the new call becomes first
- smaller than first: it becomes the new first, and the old first follows it
- duplicate `ref`: print `Duplicate ref` and insert nothing
- otherwise: insert between two calls, or at the end

`Brief()` walks with `getNext` and returns a list of `(ref, vessel)`.

Keep the object in `bay_lane` so it does not clash with the later route function.

**Test you must run, in this order:** add ref `30` to an empty lane, add `10` (must become first), add `20`, add `10` again, then `print(bay_lane.Brief())`.
"""
        ),
        code(
            '''
# L3 — YOUR ATTEMPT
# identifiers: Call, Lane, bay_lane

bay_lane = None
'''
        ),
        md(
            """
---
## L4 — routes, and both pages written from this stem

Create the two files yourself. The names below are the whole specification.

`templates/link/desk.html`
- a heading
- the message in `error` when that variable is set
- a form that POSTs to the `desk` route
- one text field named `berth_code`, and a submit control

`templates/link/lane.html`
- a heading that shows `berth_code`
- one line per item in `rows`: the vessel and the berth
- a visible empty result when `rows` has no items
- a link back to the `desk` route

Routes:

- `desk` on `/`, GET and POST. POST reads `request.form` key `berth_code`. If it is non-empty, **return** `redirect(url_for("lane", berth_code=...))`. Otherwise show `desk.html` with `error`.
- `lane` on `/lane/<berth_code>`. From `ordered`, keep rows whose berth equals that code. `render_template("link/lane.html", rows=..., berth_code=...)`.
- Do not reuse route or field names from an older Flask task.
- `app.run` is not required for the checkpoint.

**Test you must run:** print the rows your `lane` filter keeps for berth `"1"`. The checkpoint then POSTs `berth_code` `1` and reads the lane page.
"""
        ),
        code(
            '''
# L4 — YOUR ATTEMPT
# identifiers: app, desk, lane_rows
from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)
lane_rows = []
'''
        ),
        md(
            """
---
# Checkpoints

Run after the attempts. A FAIL here means that part has no evidence yet.
"""
        ),
        code(
            '''
# CHECKPOINTS — LINK
PARTS = ("L1", "L2", "L3", "L4")


def _check_l1():
    if len(clean) != 7:
        return False, f"clean has {len(clean)}, expected 7"
    if len(rejected) < 2:
        return False, "rejected rows missing"
    if clean[0][0] == "" or not isinstance(clean[0][3], int):
        return False, "first clean row is not (code, vessel, berth, int tonnes)"
    return True, "ok"


def _check_l2():
    if FindFirst(ordered, "Z99") != -1:
        return False, "miss must return -1"
    idx = FindFirst(ordered, "B07")
    if idx < 0 or ordered[idx][0] != "B07":
        return False, "FindFirst did not land on B07"
    if idx > 0 and ordered[idx - 1][0] == "B07":
        return False, "FindFirst must return the first B07, not a later one"
    got = ListVessels(ordered, "B07")
    if got != ["Amber", "Coral", "Delta"]:
        return False, f"ListVessels(B07) is {got}"
    if ListVessels(ordered, "Z99") != []:
        return False, "missing code must return an empty list"
    return True, "ok"


def _check_l3():
    brief = bay_lane.Brief()
    refs = [r for r, _ in brief]
    if refs != [10, 20, 30]:
        return False, f"Brief refs {refs}; empty-lane and insert-before-first are required"
    if any(v == "" for _, v in brief):
        return False, "vessel missing"
    return True, "ok"


def _check_l4():
    if not lane_rows or any(str(r[2]) != "1" for r in lane_rows):
        return False, "lane_rows must be the berth 1 rows from ordered"
    client = app.test_client()
    posted = client.post("/", data={"berth_code": "1"})
    if posted.status_code not in (301, 302):
        return False, f"POST desk returned {posted.status_code}; berth_code must redirect"
    loc = posted.headers.get("Location", "")
    if "/lane/1" not in loc:
        return False, f"redirect went to {loc}"
    page = client.get("/lane/1")
    if page.status_code != 200 or b"Amber" not in page.data:
        return False, "lane did not render the berth 1 rows"
    return True, "ok"


_CHECKS = {"L1": _check_l1, "L2": _check_l2, "L3": _check_l3, "L4": _check_l4}
for part in PARTS:
    try:
        ok, detail = _CHECKS[part]()
    except Exception as e:
        ok, detail = False, str(e)
    print(f"{part}: {'PASS' if ok else 'FAIL — ' + detail}")
'''
        ),
    ]
    write_nb(ROOT / "LINK drill.ipynb", cells)
    _answers()


def _answers() -> None:
    cells = [
        md("# LINK drill — answers\n\nOpen only when marking."),
        md("## L1"),
        code(
            '''
import csv

def LoadBays(filename):
    clean, rejected = [], []
    with open(filename, encoding="utf-8") as f:
        reader = csv.reader(f)
        next(reader)
        for row in reader:
            if len(row) < 4:
                rejected.append("short row")
                continue
            code, vessel, berth, tonnes = [x.strip() for x in row]
            if code == "" or vessel == "":
                rejected.append("empty code or vessel")
                continue
            if not tonnes.lstrip("-").isdigit():
                rejected.append("tonnes not int")
                continue
            clean.append((code, vessel, berth, int(tonnes)))
    return clean, rejected

clean, rejected = LoadBays("LINK_BAYS.csv")
print(len(clean), len(rejected), clean[0])
'''
        ),
        md("## L2"),
        code(
            '''
def InsertionSort(records):
    arr = records[:]
    for i in range(1, len(arr)):
        current = arr[i]
        j = i - 1
        while j >= 0 and (arr[j][0], arr[j][1]) > (current[0], current[1]):
            arr[j + 1] = arr[j]
            j -= 1
        arr[j + 1] = current
    return arr

def FindFirst(records, code):
    low, high = 0, len(records) - 1
    found = -1
    while low <= high:
        middle = (low + high) // 2
        if records[middle][0] == code:
            found = middle
            high = middle - 1
        elif records[middle][0] < code:
            low = middle + 1
        else:
            high = middle - 1
    return found

def ListVessels(records, code):
    index = FindFirst(records, code)
    if index == -1:
        return []
    out = []
    while index < len(records) and records[index][0] == code:
        out.append(records[index][1])
        index += 1
    return out

ordered = InsertionSort(clean)
print(FindFirst(ordered, "B07"), FindFirst(ordered, "Z99"))
print(ListVessels(ordered, "B07"))
print(ListVessels(ordered, "Z99"))
'''
        ),
        md("## L3"),
        code(
            '''
class Call:
    def __init__(self, ref, vessel):
        self.__ref = ref
        self.__vessel = vessel
        self.__next = None

    def getRef(self):
        return self.__ref

    def getVessel(self):
        return self.__vessel

    def getNext(self):
        return self.__next

    def setNext(self, nxt):
        self.__next = nxt

class Lane:
    def __init__(self):
        self.__first = None

    def getFirst(self):
        return self.__first

    def AddCall(self, new_call):
        if self.__first is None:
            self.__first = new_call
            return True
        if new_call.getRef() == self.__first.getRef():
            print("Duplicate ref")
            return False
        if new_call.getRef() < self.__first.getRef():
            new_call.setNext(self.__first)
            self.__first = new_call
            return True
        current = self.__first
        while current.getNext() is not None and current.getNext().getRef() < new_call.getRef():
            current = current.getNext()
        nxt = current.getNext()
        if nxt is not None and nxt.getRef() == new_call.getRef():
            print("Duplicate ref")
            return False
        new_call.setNext(nxt)
        current.setNext(new_call)
        return True

    def Brief(self):
        out = []
        current = self.__first
        while current is not None:
            out.append((current.getRef(), current.getVessel()))
            current = current.getNext()
        return out

bay_lane = Lane()
bay_lane.AddCall(Call(30, "South Wind"))
bay_lane.AddCall(Call(10, "Amber"))
bay_lane.AddCall(Call(20, "Coral"))
bay_lane.AddCall(Call(10, "Amber"))
print(bay_lane.Brief())
'''
        ),
        md("## L4"),
        code(
            '''
from pathlib import Path
from flask import Flask, render_template, request, redirect, url_for

link_dir = Path("templates/link")
link_dir.mkdir(parents=True, exist_ok=True)
(link_dir / "desk.html").write_text(
    "<!doctype html><html><body><h1>bay desk</h1>"
    "{% if error %}<p>{{ error }}</p>{% endif %}"
    "<form method=\\"POST\\" action=\\"{{ url_for('desk') }}\\">"
    "<input type=\\"text\\" name=\\"berth_code\\">"
    "<input type=\\"submit\\" value=\\"open\\"></form></body></html>",
    encoding="utf-8",
)
(link_dir / "lane.html").write_text(
    "<!doctype html><html><body><h1>{{ berth_code }}</h1><ul>"
    "{% for row in rows %}<li>{{ row[1] }} — berth {{ row[2] }}</li>"
    "{% else %}<li>none</li>{% endfor %}</ul>"
    "<p><a href=\\"{{ url_for('desk') }}\\">back</a></p></body></html>",
    encoding="utf-8",
)

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def desk():
    error = None
    if request.method == "POST":
        berth_code = request.form.get("berth_code", "").strip()
        if berth_code:
            return redirect(url_for("lane", berth_code=berth_code))
        error = "Please fill in all fields"
    return render_template("link/desk.html", error=error)

@app.route("/lane/<berth_code>")
def lane(berth_code):
    rows = [row for row in ordered if str(row[2]) == str(berth_code)]
    return render_template("link/lane.html", rows=rows, berth_code=berth_code)

lane_rows = [row for row in ordered if str(row[2]) == "1"]
print(lane_rows)
'''
        ),
    ]
    write_nb(ARCHIVE / "LINK drill - answers.ipynb", cells)


if __name__ == "__main__":
    build()
