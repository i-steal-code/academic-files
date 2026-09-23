#!/usr/bin/env python3
"""Build the three P2 mega-chain practice notebooks (nbformat-valid)."""

from __future__ import annotations

import uuid
from pathlib import Path

import nbformat
from nbformat.v4 import new_code_cell, new_markdown_cell, new_notebook

ROOT = Path("computing practical/computing practical all boilerplates")


def cid() -> str:
    return uuid.uuid4().hex[:8]


def md(source: str):
    return new_markdown_cell(source=source.strip("\n") + "\n", id=cid())


def code(source: str):
    # Outer quotes for callers should be ''' so cell body may contain """
    return new_code_cell(source=source.strip("\n") + "\n", id=cid(), execution_count=None, outputs=[])


def write_nb(path: Path, cells: list) -> None:
    nb = new_notebook(
        cells=cells,
        metadata={
            "kernelspec": {
                "display_name": "Python 3",
                "language": "python",
                "name": "python3",
            }
        },
    )
    path.write_text(nbformat.writes(nb), encoding="utf-8", newline="\n")
    print(f"wrote {path.name} ({len(cells)} cells)")


def build_chain_a() -> None:
    cells = [
        md(
            """
# P2 CHAIN A — club attendance (validate → sqlite → queries → Flask)

Closed-book mega-question. Reference voice: `DB.ipynb`, `WEB DEV.ipynb`. **Do not open them.**

**Rules**
- One kernel; run parts in order.
- Do **not** scroll to **Answer keys** until that part's checkpoint prints `PASS` (or you are marking).
- Later parts need earlier artifacts (`clean_members`, `clean_attendance`, `chain_a.db`).
- Templates live in `templates/chain_a/` — form `name=` and `url_for(...)` targets are **not** the usual latecoming ones.

**Data:** `MEMBERS.csv`, `ATTENDANCE.csv` in this folder (deliberately dirty rows included).

Suggested session: A1+A2 one day; A3 next; A4 when sqlite is cold.
"""
        ),
        md(
            """
---
## Part A1 — load + validate (12 min)

Read both CSVs. Skip header rows. Build:

- `clean_members`: list of `(member_id:int, name:str, house:str, year:int)`
- `clean_attendance`: list of `(date:str, member_id:int, session:str)`
- `rejected`: list of short reason strings for every rejected row

**Member rules:** `member_id` must parse as `int`; `name` non-empty; `house` non-empty; `year` in `{5, 6}`.

**Attendance rules:** `date` non-empty; `member_id` parses as `int`; `session` non-empty.

Do **not** require FK membership yet. Use explicit `if` checks — no bare `try/except` as your only validation.
"""
        ),
        code(
            '''
# Part A1 — YOUR ATTEMPT
import csv

clean_members = []
clean_attendance = []
rejected = []

# write from memory
'''
        ),
        code(
            '''
# CHECKPOINT A1 — run after your attempt (not the answer key)
ok = True
msgs = []
if len(clean_members) != 15:
    ok = False
    msgs.append(f"clean_members expected 15, got {len(clean_members)}")
if len(clean_attendance) != 33:
    ok = False
    msgs.append(f"clean_attendance expected 33, got {len(clean_attendance)}")
if len(rejected) < 3:
    ok = False
    msgs.append(f"rejected expected at least 3, got {len(rejected)}")
ids = {m[0] for m in clean_members}
if 1013 in ids or 1014 in ids:
    ok = False
    msgs.append("bad member ids leaked into clean_members")
print("PASS" if ok else "FAIL: " + "; ".join(msgs))
'''
        ),
        md(
            """
---
## Part A2 — schema + seed (12 min)

Connect to **`chain_a.db`**. Set `row_factory = sqlite3.Row`. DROP then CREATE:

- `Member(member_id INTEGER PRIMARY KEY, name TEXT, house TEXT, year INTEGER)`
- `Attendance(date TEXT, member_id INTEGER, session TEXT, PRIMARY KEY(date, member_id), FOREIGN KEY(member_id) REFERENCES Member(member_id))`

Seed from `clean_members` / `clean_attendance` with `?` placeholders and `INSERT OR IGNORE`. `commit()`.

**Check target:** 15 members; attendance rows whose `member_id` exists in Member.
"""
        ),
        code(
            '''
# Part A2 — YOUR ATTEMPT
import sqlite3

# write from memory — use clean_members / clean_attendance from A1
'''
        ),
        code(
            '''
# CHECKPOINT A2
import sqlite3
conn = sqlite3.connect("chain_a.db")
conn.row_factory = sqlite3.Row
cur = conn.cursor()
ok = True
msgs = []
try:
    n_m = cur.execute("SELECT COUNT(*) AS c FROM Member").fetchone()["c"]
    n_a = cur.execute("SELECT COUNT(*) AS c FROM Attendance").fetchone()["c"]
    if n_m != 15:
        ok = False
        msgs.append(f"Member count {n_m} != 15")
    if n_a < 30:
        ok = False
        msgs.append(f"Attendance count {n_a} looks too low")
    row = cur.execute("SELECT name FROM Member WHERE member_id = ?", (1001,)).fetchone()
    if row is None or row["name"] != "Ada Tan":
        ok = False
        msgs.append("row_factory / seed smoke failed for 1001")
except Exception as e:
    ok = False
    msgs.append(str(e))
conn.close()
print("PASS" if ok else "FAIL: " + "; ".join(msgs))
'''
        ),
        md(
            """
---
## Part A3 — query bank (15 min)

Using `chain_a.db`, write parameterised queries (wildcards in the **tuple**):

1. **JOIN hit list:** members in house `East` who attended a `Training` session — print `name`, `date`, `session`.
2. **HAVING:** houses with `COUNT(*)` of attendance rows `>= 5` — print `house`, total.
3. **Never-attended:** members with **no** Attendance row (`LEFT OUTER JOIN` + `IS NULL`) in house `West` — print names.
4. One **UPDATE** then **DELETE** on a throwaway row you `INSERT` first (parameterised); `commit`.

Remember: aggregates belong in `HAVING`, not `WHERE`.
"""
        ),
        code(
            '''
# Part A3 — YOUR ATTEMPT
import sqlite3
conn = sqlite3.connect("chain_a.db")
conn.row_factory = sqlite3.Row
cur = conn.cursor()

# 1 JOIN
# 2 HAVING
# 3 never-attended
# 4 CRUD smoke

conn.close()
'''
        ),
        code(
            '''
# CHECKPOINT A3
import sqlite3
conn = sqlite3.connect("chain_a.db")
conn.row_factory = sqlite3.Row
cur = conn.cursor()
ok = True
msgs = []
east_train = cur.execute(
    "SELECT Member.name, Attendance.date, Attendance.session "
    "FROM Member INNER JOIN Attendance ON Member.member_id = Attendance.member_id "
    "WHERE Member.house = ? AND Attendance.session = ?",
    ("East", "Training"),
).fetchall()
if len(east_train) < 1:
    ok = False
    msgs.append("JOIN East/Training returned nothing — DB empty or wrong schema?")
hav = cur.execute(
    "SELECT Member.house, COUNT(*) AS total "
    "FROM Member INNER JOIN Attendance ON Member.member_id = Attendance.member_id "
    "GROUP BY Member.house HAVING COUNT(*) >= 5"
).fetchall()
if len(hav) < 1:
    ok = False
    msgs.append("HAVING query returned no groups")
never = cur.execute(
    "SELECT Member.name FROM Member LEFT OUTER JOIN Attendance "
    "ON Member.member_id = Attendance.member_id "
    "WHERE Attendance.member_id IS NULL AND Member.house = ?",
    ("West",),
).fetchall()
_ = never
conn.close()
print("PASS" if ok else "FAIL: " + "; ".join(msgs))
'''
        ),
        md(
            """
---
## Part A4 — Flask wiring (20 min)

Build a Flask app that uses **`chain_a.db`** and templates under `templates/chain_a/`:

| Route | Function name | Template | Behaviour |
|-------|---------------|----------|-----------|
| `/` GET+POST | `portal` | `chain_a/portal.html` | POST reads `session_type` + `member_name`; validate with explicit `if`; **return** `redirect(url_for("hits", ...))` |
| `/hits/<session_type>/<member_name>` | `hits` | `chain_a/hits.html` | JOIN query; `LIKE` on name with wildcards in tuple; pass `rows`, `session_type`, `member_name` |
| `/log` GET+POST | `log_absence` | `chain_a/log.html` | form keys `mid`, `when`, `sess`; INSERT parameterised; redirect to `portal` |

Also: `get_db()`, `row_factory`, `if __name__ == "__main__": app.run(port=5001)` (5001 avoids clashing with WEB DEV on 5000).

Stop other Flask apps first. Checkpoint is structural only — also self-check by starting the app.
"""
        ),
        code(
            '''
# Part A4 — YOUR ATTEMPT
from flask import Flask, render_template, request, redirect, url_for
import sqlite3

app = Flask(__name__)

# get_db, portal, hits, log_absence, __main__
'''
        ),
        code(
            '''
# CHECKPOINT A4 — structural (does not start the server)
ok = True
msgs = []
needed = ["app", "get_db", "portal", "hits", "log_absence"]
g = globals()
for name in needed:
    if name not in g:
        ok = False
        msgs.append(f"missing {name}")
if "app" in g:
    rules = {rule.rule: rule.endpoint for rule in app.url_map.iter_rules() if rule.endpoint != "static"}
    expect = {"/": "portal", "/log": "log_absence"}
    for path, ep in expect.items():
        if rules.get(path) != ep:
            ok = False
            msgs.append(f"route {path} expected endpoint {ep}, got {rules.get(path)}")
    if "hits" not in rules.values():
        ok = False
        msgs.append("hits endpoint not registered")
print("PASS" if ok else "FAIL: " + "; ".join(msgs))
print("Manual: run app on 5001 and POST a search + log one absence.")
'''
        ),
        md("---\n# Answer keys — scroll only after checkpoints (or when marking)\n\n## Answer — Part A1"),
        code(
            '''
# Answer — Part A1
import csv

clean_members = []
clean_attendance = []
rejected = []

with open("MEMBERS.csv", encoding="utf-8") as f:
    reader = csv.reader(f)
    next(reader)
    for row in reader:
        if len(row) < 4:
            rejected.append("member: short row")
            continue
        mid_s, name, house, year_s = row[0].strip(), row[1].strip(), row[2].strip(), row[3].strip()
        if not mid_s.isdigit():
            rejected.append(f"member: bad id {mid_s!r}")
            continue
        if name == "" or house == "":
            rejected.append(f"member: empty name/house id={mid_s}")
            continue
        if not year_s.isdigit() or int(year_s) not in (5, 6):
            rejected.append(f"member: bad year {year_s!r}")
            continue
        clean_members.append((int(mid_s), name, house, int(year_s)))

with open("ATTENDANCE.csv", encoding="utf-8") as f:
    reader = csv.reader(f)
    next(reader)
    for row in reader:
        if len(row) < 3:
            rejected.append("attendance: short row")
            continue
        date, mid_s, session = row[0].strip(), row[1].strip(), row[2].strip()
        if date == "":
            rejected.append("attendance: empty date")
            continue
        if not mid_s.isdigit():
            rejected.append(f"attendance: bad id {mid_s!r}")
            continue
        if session == "":
            rejected.append("attendance: empty session")
            continue
        clean_attendance.append((date, int(mid_s), session))

print(len(clean_members), len(clean_attendance), len(rejected))
# traps: next(reader) for header; year domain {5,6}; empty checks before int()
'''
        ),
        md("## Answer — Part A2"),
        code(
            '''
# Answer — Part A2
import sqlite3

conn = sqlite3.connect("chain_a.db")
conn.row_factory = sqlite3.Row
cur = conn.cursor()

cur.execute("DROP TABLE IF EXISTS Attendance")
cur.execute("DROP TABLE IF EXISTS Member")
cur.execute(
    "CREATE TABLE Member("
    "member_id INTEGER PRIMARY KEY, name TEXT, house TEXT, year INTEGER)"
)
cur.execute(
    "CREATE TABLE Attendance("
    "date TEXT, member_id INTEGER, session TEXT, "
    "PRIMARY KEY(date, member_id), "
    "FOREIGN KEY(member_id) REFERENCES Member(member_id))"
)

for mid, name, house, year in clean_members:
    cur.execute(
        "INSERT OR IGNORE INTO Member(member_id, name, house, year) VALUES (?,?,?,?)",
        (mid, name, house, year),
    )
for date, mid, session in clean_attendance:
    cur.execute(
        "INSERT OR IGNORE INTO Attendance(date, member_id, session) VALUES (?,?,?)",
        (date, mid, session),
    )
conn.commit()
print(cur.execute("SELECT COUNT(*) AS c FROM Member").fetchone()["c"])
print(cur.execute("SELECT COUNT(*) AS c FROM Attendance").fetchone()["c"])
conn.close()
# traps: DROP child before parent; ? placeholders; commit
'''
        ),
        md("## Answer — Part A3"),
        code(
            '''
# Answer — Part A3
import sqlite3
conn = sqlite3.connect("chain_a.db")
conn.row_factory = sqlite3.Row
cur = conn.cursor()

cur.execute(
    "SELECT Member.name, Attendance.date, Attendance.session "
    "FROM Member INNER JOIN Attendance ON Member.member_id = Attendance.member_id "
    "WHERE Member.house = ? AND Attendance.session = ? ORDER BY Attendance.date",
    ("East", "Training"),
)
for row in cur.fetchall():
    print(row["name"], row["date"], row["session"])

cur.execute(
    "SELECT Member.house, COUNT(*) AS total "
    "FROM Member INNER JOIN Attendance ON Member.member_id = Attendance.member_id "
    "GROUP BY Member.house HAVING COUNT(*) >= 5"
)
for row in cur.fetchall():
    print(row["house"], row["total"])

cur.execute(
    "SELECT Member.name FROM Member LEFT OUTER JOIN Attendance "
    "ON Member.member_id = Attendance.member_id "
    "WHERE Attendance.member_id IS NULL AND Member.house = ?",
    ("West",),
)
for row in cur.fetchall():
    print(row["name"])

cur.execute(
    "INSERT OR IGNORE INTO Attendance(date, member_id, session) VALUES (?,?,?)",
    ("2099-01-01", 1001, "Training"),
)
cur.execute(
    "UPDATE Attendance SET session = ? WHERE date = ? AND member_id = ?",
    ("Match", "2099-01-01", 1001),
)
cur.execute(
    "DELETE FROM Attendance WHERE date = ? AND member_id = ?",
    ("2099-01-01", 1001),
)
conn.commit()
conn.close()
# traps: HAVING not WHERE for COUNT; trailing comma on 1-tuples
'''
        ),
        md("## Answer — Part A4"),
        code(
            '''
# Answer — Part A4
from flask import Flask, render_template, request, redirect, url_for
import sqlite3

app = Flask(__name__)

def get_db():
    conn = sqlite3.connect("chain_a.db")
    conn.row_factory = sqlite3.Row
    return conn

@app.route("/", methods=["GET", "POST"])
def portal():
    error = None
    if request.method == "POST":
        session_type = request.form.get("session_type", "").strip()
        member_name = request.form.get("member_name", "").strip()
        if session_type and member_name:
            return redirect(url_for("hits", session_type=session_type, member_name=member_name))
        error = "Please fill in all fields"
    return render_template("chain_a/portal.html", error=error)

@app.route("/hits/<session_type>/<member_name>")
def hits(session_type, member_name):
    conn = get_db()
    cur = conn.cursor()
    cur.execute(
        "SELECT Member.name, Member.house, Attendance.date, Attendance.session "
        "FROM Member INNER JOIN Attendance ON Member.member_id = Attendance.member_id "
        "WHERE Attendance.session = ? AND Member.name LIKE ? ORDER BY Attendance.date",
        (session_type, f"%{member_name}%"),
    )
    rows = cur.fetchall()
    conn.close()
    return render_template(
        "chain_a/hits.html",
        rows=rows,
        session_type=session_type,
        member_name=member_name,
    )

@app.route("/log", methods=["GET", "POST"])
def log_absence():
    error = None
    if request.method == "POST":
        mid = request.form.get("mid", "").strip()
        when = request.form.get("when", "").strip()
        sess = request.form.get("sess", "").strip()
        if not (mid and when and sess):
            error = "Please fill in all fields"
        else:
            conn = get_db()
            cur = conn.cursor()
            cur.execute(
                "INSERT OR IGNORE INTO Attendance(date, member_id, session) VALUES (?,?,?)",
                (when, mid, sess),
            )
            conn.commit()
            conn.close()
            return redirect(url_for("portal"))
    return render_template("chain_a/log.html", error=error)

if __name__ == "__main__":
    app.run(port=5001)
# traps: MUST return redirect; form keys match template; url_for endpoint == def name
'''
        ),
    ]
    write_nb(ROOT / "P2 CHAIN A - attendance.ipynb", cells)


def build_chain_b() -> None:
    """Practice notebook: attempts only. Checkpoints encapsulated at bottom. No answer keys."""
    cells = [
        md(
            """
# P2 CHAIN B — library inventory (OOP → ADT → S&S → JSON)

Closed-book mega-question. Reference voice: `POOP.ipynb`, `ADT.ipynb`, `S&S.ipynb`. **Do not open them.**

**Rules**
- Parts depend on earlier objects in the same kernel (`stock` → linked list → hash/BST → sorted keys → JSON).
- Use double-underscore privates + getters; child must not read parent `__attrs` directly.
- **Checkpoints** are encapsulated at the **bottom** of this notebook — run them only after you finish a part (or the whole chain). Do not treat them as a writing guide.
- **No answer keys in this notebook.** Mark against boilerplates / archive answers only after attempting.

**Domain:** library resources — print books and digital resources.
"""
        ),
        md(
            """
---
## Part B1 — OOP hierarchy (12 min)

Implement:

- `Resource(resource_id, title)` with private `__resource_id`, `__title`, getters, `set_title`, and `describe()` → `Resource {id}: {title}`
- `DigitalResource(resource_id, title, filesize_mb)` inheriting from `Resource`: call `super().__init__`, store private `__filesize_mb` as `int`, override `describe()` using **getters** for parent fields → `Digital Resource {id}: {title} ({n} MB)`

Build `stock`: a Python list of at least 6 mixed Resource / DigitalResource instances. Print each `.describe()`.
"""
        ),
        code(
            '''
# Part B1 — YOUR ATTEMPT

stock = []
# classes + populate stock
'''
        ),
        md(
            """
---
## Part B2 — LinkedList of resource IDs (15 min)

`Node` (data + right link, getters/setters) and `LinkedList` with `__start`, `is_empty`, `insert_end`, `search` (Node or None), `delete` (**including head case**).

Insert every `resource_id` from `stock` via `insert_end` into `catalogue = LinkedList()`.

Then: `delete` the **first** id you inserted (head), `search` a mid id (found), `search(-1)` → None, `delete` a missing id (no crash).
"""
        ),
        code(
            '''
# Part B2 — YOUR ATTEMPT

catalogue = None  # LinkedList()
# Node, LinkedList, drive from stock
'''
        ),
        md(
            """
---
## Part B3 — HashTable + BST report (15 min)

1. `HashTable(N)` separate chaining: `self.__arr = [LinkedList() for _ in range(N)]` — never `[LinkedList()] * N`. Methods: `hash_function`, `insert`, `search` (bool). Insert all ids currently in `catalogue`.
2. `TreeNode` + `BST` with `insert` (`<=` left, `>` right) and `in_order` / `pre_order` / `post_order` each taking a **node**. Insert same ids. Print in-order.

Use `N = 7`. Keep `ht` and `bst` in the kernel. Prefer a `walk_ids()` helper or equivalent on the list.
"""
        ),
        code(
            '''
# Part B3 — YOUR ATTEMPT

ht = None
bst = None
# HashTable, TreeNode, BST + load from catalogue
'''
        ),
        md(
            """
---
## Part B4 — sort + binary search on extracted keys (12 min)

Build `keys` (list of ints) from the catalogue.

1. **Insertion sort** *or* `partition` + `quickSort` (final pivot↔rightmark swap). Sort a **copy** into `sorted_keys`.
2. Recursive `BinarySearch(Arr, FindValue, Low, High)` — `Low > High` → `-1`; recurse with `middle ± 1` and **return** the call.

Demo: search existing id and missing id on `sorted_keys`.
"""
        ),
        code(
            '''
# Part B4 — YOUR ATTEMPT

keys = []
sorted_keys = []
# extract, sort, BinarySearch demos
'''
        ),
        md(
            """
---
## Part B5 — JSON round-trip (8 min)

Build a JSON-serialisable list of dicts from `stock`, e.g.
`{"id": ..., "title": ..., "kind": "print"|"digital", "filesize_mb": ...|null}`.

- `save_catalogue(filename, data)` — `json.dump`, utf-8
- `load_catalogue(filename)` — `json.load`

Write `library_out.json`, load it back, assert same length.

When finished practising, delete `library_out.json` so it does not linger as a trail.
"""
        ),
        code(
            '''
# Part B5 — YOUR ATTEMPT
import json

# save_catalogue / load_catalogue / round-trip
'''
        ),
        md(
            """
---
# Checkpoints (encapsulated)

Run **after** attempting. Edit `PARTS` below to choose what to mark. These cells are not a guide while writing.
"""
        ),
        code(
            '''
# CHECKPOINTS — Chain B (run after attempts)
# Set which parts to mark, then run this cell once.

PARTS = ("B1", "B2", "B3", "B4", "B5")  # e.g. ("B1", "B2") while still climbing


def _rid(obj):
    if hasattr(obj, "get_resource_id"):
        return obj.get_resource_id()
    return obj.get_id()


def _check_b1():
    g = globals()
    if "Resource" not in g or "DigitalResource" not in g:
        return False, "missing class"
    r = Resource(1, "Alpha")
    d = DigitalResource(2, "Beta", "12")
    if "Resource 1: Alpha" not in r.describe():
        return False, f"Resource.describe odd: {r.describe()!r}"
    if "Digital Resource 2: Beta" not in d.describe() or "12" not in d.describe():
        return False, f"DigitalResource.describe odd: {d.describe()!r}"
    if not isinstance(d, Resource):
        return False, "DigitalResource should be subclass of Resource"
    if len(stock) < 6:
        return False, f"stock length {len(stock)} < 6"
    return True, "ok"


def _check_b2():
    first_id = _rid(stock[0])
    mid_id = _rid(stock[2])
    if catalogue is None or catalogue.is_empty():
        return False, "catalogue empty/missing"
    if catalogue.search(first_id) is not None:
        return False, "head id still present after required delete"
    if catalogue.search(mid_id) is None:
        return False, "mid id missing — insert_end/search broken?"
    if catalogue.search(-1) is not None:
        return False, "search(-1) should be None"
    return True, "ok"


def _check_b3():
    mid_id = _rid(stock[2])
    if ht is None or bst is None:
        return False, "ht or bst missing"
    if not ht.search(mid_id):
        return False, "hash search failed for mid id"
    if hasattr(bst, "in_order") and hasattr(bst, "get_root"):
        bst.in_order(bst.get_root())
    return True, "ok"


def _check_b4():
    if sorted_keys != sorted(sorted_keys):
        return False, "sorted_keys not sorted"
    if len(sorted_keys) < 5:
        return False, "too few keys"
    target = sorted_keys[len(sorted_keys) // 2]
    idx = BinarySearch(sorted_keys, target, 0, len(sorted_keys) - 1)
    if idx < 0 or sorted_keys[idx] != target:
        return False, "BinarySearch miss on existing value"
    if BinarySearch(sorted_keys, -999, 0, len(sorted_keys) - 1) != -1:
        return False, "BinarySearch should return -1 for absent"
    return True, "ok"


def _check_b5():
    from pathlib import Path
    import json
    p = Path("library_out.json")
    if not p.exists():
        return False, "library_out.json missing"
    data = json.loads(p.read_text(encoding="utf-8"))
    if len(data) != len(stock):
        return False, f"json len {len(data)} != stock {len(stock)}"
    if not isinstance(data[0], dict) or "id" not in data[0]:
        return False, "records should be dicts with id"
    return True, "ok"


_CHECKS = {
    "B1": _check_b1,
    "B2": _check_b2,
    "B3": _check_b3,
    "B4": _check_b4,
    "B5": _check_b5,
}

for part in PARTS:
    try:
        ok, detail = _CHECKS[part]()
    except Exception as e:
        ok, detail = False, str(e)
    print(f"{part}: {'PASS' if ok else 'FAIL — ' + detail}")
'''
        ),
    ]
    write_nb(ROOT / "P2 CHAIN B - library.ipynb", cells)
    _write_chain_b_answers_archive()


def _write_chain_b_answers_archive() -> None:
    """Answers live only under _archive — not in the practice notebook."""
    archive = ROOT / "_archive"
    archive.mkdir(exist_ok=True)
    cells = [
        md("# P2 CHAIN B — answers (archive only)\n\nOpen only when marking. Not for cold practice."),
        md("## Answer — Part B1"),
        code(
            '''
# Answer — Part B1
class Resource:
    def __init__(self, resource_id, title):
        self.__resource_id = resource_id
        self.__title = title

    def get_resource_id(self):
        return self.__resource_id

    def get_title(self):
        return self.__title

    def set_title(self, title):
        self.__title = title

    def describe(self):
        return f"Resource {self.__resource_id}: {self.__title}"

class DigitalResource(Resource):
    def __init__(self, resource_id, title, filesize_mb):
        super().__init__(resource_id, title)
        self.__filesize_mb = int(filesize_mb)

    def get_filesize_mb(self):
        return self.__filesize_mb

    def describe(self):
        return (
            f"Digital Resource {self.get_resource_id()}: "
            f"{self.get_title()} ({self.__filesize_mb} MB)"
        )

stock = [
    Resource(101, "Discrete Maths"),
    DigitalResource(102, "Python Notes", 4),
    Resource(103, "Networks Primer"),
    DigitalResource(104, "SQL Lab Pack", 18),
    Resource(105, "Ethics Reader"),
    DigitalResource(106, "Flask Demo", 2),
    Resource(107, "Algorithms Sketch"),
]
for item in stock:
    print(item.describe())
'''
        ),
        md("## Answer — Part B2"),
        code(
            '''
# Answer — Part B2
class Node:
    def __init__(self, data=None):
        self.__data = data
        self.__right = None

    def get_data(self):
        return self.__data

    def set_data(self, data):
        self.__data = data

    def get_right(self):
        return self.__right

    def set_right(self, right):
        self.__right = right

class LinkedList:
    def __init__(self):
        self.__start = None

    def is_empty(self):
        return self.__start is None

    def insert_end(self, data):
        new = Node()
        new.set_data(data)
        if self.is_empty():
            self.__start = new
        else:
            current = self.__start
            while current.get_right() is not None:
                current = current.get_right()
            current.set_right(new)

    def search(self, data):
        current = self.__start
        while current is not None and current.get_data() != data:
            current = current.get_right()
        return current

    def delete(self, data):
        if self.is_empty():
            return
        if self.__start.get_data() == data:
            self.__start = self.__start.get_right()
            return
        previous = None
        current = self.__start
        while current is not None and current.get_data() != data:
            previous = current
            current = current.get_right()
        if current is None:
            return
        previous.set_right(current.get_right())

    def walk_ids(self):
        out = []
        current = self.__start
        while current is not None:
            out.append(current.get_data())
            current = current.get_right()
        return out

catalogue = LinkedList()
for item in stock:
    catalogue.insert_end(item.get_resource_id())
catalogue.delete(stock[0].get_resource_id())
print(catalogue.walk_ids())
'''
        ),
        md("## Answer — Part B3"),
        code(
            '''
# Answer — Part B3
class HashTable:
    def __init__(self, N):
        self.__n = N
        self.__arr = [LinkedList() for _ in range(N)]

    def hash_function(self, key):
        return key % self.__n

    def insert(self, key):
        bucket = self.__arr[self.hash_function(key)]
        if bucket.search(key) is None:
            bucket.insert_end(key)

    def search(self, key):
        return self.__arr[self.hash_function(key)].search(key) is not None

class TreeNode:
    def __init__(self, data):
        self.__data = data
        self.__left = None
        self.__right = None

    def get_data(self):
        return self.__data

    def get_left(self):
        return self.__left

    def set_left(self, node):
        self.__left = node

    def get_right(self):
        return self.__right

    def set_right(self, node):
        self.__right = node

class BST:
    def __init__(self):
        self.__root = None

    def get_root(self):
        return self.__root

    def insert(self, data):
        new = TreeNode(data)
        if self.__root is None:
            self.__root = new
            return
        current = self.__root
        while current:
            if data <= current.get_data():
                if current.get_left() is None:
                    current.set_left(new)
                    return
                current = current.get_left()
            else:
                if current.get_right() is None:
                    current.set_right(new)
                    return
                current = current.get_right()

    def in_order(self, node):
        if node is not None:
            self.in_order(node.get_left())
            print(node.get_data())
            self.in_order(node.get_right())

    def pre_order(self, node):
        if node is not None:
            print(node.get_data())
            self.pre_order(node.get_left())
            self.pre_order(node.get_right())

    def post_order(self, node):
        if node is not None:
            self.post_order(node.get_left())
            self.post_order(node.get_right())
            print(node.get_data())

ht = HashTable(7)
bst = BST()
for rid in catalogue.walk_ids():
    ht.insert(rid)
    bst.insert(rid)
bst.in_order(bst.get_root())
'''
        ),
        md("## Answer — Part B4"),
        code(
            '''
# Answer — Part B4
def InsertionSort(Arr):
    for i in range(1, len(Arr)):
        current = Arr[i]
        j = i - 1
        while j >= 0 and Arr[j] > current:
            Arr[j + 1] = Arr[j]
            j -= 1
        Arr[j + 1] = current
    return Arr

def BinarySearch(Arr, FindValue, Low, High):
    if Low > High:
        return -1
    middle = (Low + High) // 2
    if Arr[middle] == FindValue:
        return middle
    elif FindValue < Arr[middle]:
        return BinarySearch(Arr, FindValue, Low, middle - 1)
    else:
        return BinarySearch(Arr, FindValue, middle + 1, High)

keys = catalogue.walk_ids()
sorted_keys = InsertionSort(keys[:])
print(sorted_keys)
print(BinarySearch(sorted_keys, sorted_keys[0], 0, len(sorted_keys) - 1))
print(BinarySearch(sorted_keys, -999, 0, len(sorted_keys) - 1))
'''
        ),
        md("## Answer — Part B5"),
        code(
            '''
# Answer — Part B5
import json

def save_catalogue(filename, data):
    with open(filename, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)

def load_catalogue(filename):
    with open(filename, encoding="utf-8") as f:
        return json.load(f)

payload = []
for item in stock:
    if isinstance(item, DigitalResource):
        payload.append({
            "id": item.get_resource_id(),
            "title": item.get_title(),
            "kind": "digital",
            "filesize_mb": item.get_filesize_mb(),
        })
    else:
        payload.append({
            "id": item.get_resource_id(),
            "title": item.get_title(),
            "kind": "print",
            "filesize_mb": None,
        })

save_catalogue("library_out.json", payload)
print(load_catalogue("library_out.json")[0])
# delete library_out.json when done marking so it is not a trail
'''
        ),
    ]
    write_nb(archive / "P2 CHAIN B - answers.ipynb", cells)


def build_chain_c() -> None:
    """Practice notebook: attempts only. Checkpoints encapsulated at bottom. No answer keys."""
    cells = [
        md(
            """
# P2 CHAIN C — staff directory (OOP → mongo → Flask → sockets)

Closed-book mega-question / niche hedge ladder. Reference voice: `POOP.ipynb`, `WEB DEV.ipynb` mongo misc, `SOCKETS.ipynb`.

**Requires** local MongoDB at `mongodb://localhost:27017/`. If mongo is down, still complete **C1** and **C4**; mark C2–C3 soft-fail in your session log.

**Rules**
- Dependency: C2 migrates objects from C1; C3 reads the mongo collection; C4 is the notify spine.
- Templates: `templates/chain_c/` — endpoints `desk`, `matches_view`, `hire`. Flask on port **5002**.
- **Checkpoints** are encapsulated at the **bottom** — run after attempting. Not a writing guide.
- **No answer keys in this notebook.** Archive answers only when marking.
- Prefer not to leave mongo collections / local junk lying around after a session (`chain_c_db.staff` can be dropped when done).
"""
        ),
        md(
            """
---
## Part C1 — in-memory staff collection (10 min)

`Staff(staff_id, surname, given, department)` with privates + getters + `as_dict()` for mongo.

`Directory`: `add(staff)`, `find_by_id(staff_id)`, `all_dicts()` → list of dicts.

Populate `roster = Directory()` with ≥5 staff. Print `all_dicts()`.
"""
        ),
        code(
            '''
# Part C1 — YOUR ATTEMPT

roster = None
'''
        ),
        md(
            """
---
## Part C2 — migrate to mongo (12 min)

`MongoClient("mongodb://localhost:27017/")`:

- DB `chain_c_db`, collection `staff`
- `drop()` for a repeatable run
- `insert_many(roster.all_dicts())`
- `find` with inclusion projection on `surname`, `department`
- `update_one` one staff department with `{"$set": {...}}` — **filter first**

Keep `coll` for C3.
"""
        ),
        code(
            '''
# Part C2 — YOUR ATTEMPT
from pymongo import MongoClient

coll = None
# migrate + update_one demo
'''
        ),
        md(
            """
---
## Part C3 — Flask over mongo (18 min)

Templates in `templates/chain_c/`:

| Route | Endpoint fn | Template | Notes |
|-------|-------------|----------|-------|
| `/` GET+POST | `desk` | `chain_c/desk.html` | form keys `dept_query`, `surname_query` → redirect |
| `/matches/<dept_query>/<surname_query>` | `matches_view` | `chain_c/matches.html` | mongo find; pass `people` |
| `/hire` GET+POST | `hire` | `chain_c/hire.html` | keys `sid`, `surname`, `given`, `department`; `insert_one`; redirect `desk` |

`get_mongo()` returns the `staff` collection. Port **5002**.
"""
        ),
        code(
            '''
# Part C3 — YOUR ATTEMPT
from flask import Flask, render_template, request, redirect, url_for
from pymongo import MongoClient

app = Flask(__name__)
# get_mongo, desk, matches_view, hire
'''
        ),
        md(
            """
---
## Part C4 — sockets notify spine (12 min)

1. `recv_line(sock)` loops `recv(1024)` until newline (or peer closed), decode utf-8, strip.
2. Comment the **server** spine: socket → bind → listen → accept → loop recv_line / sendall → close
   and **client** spine: connect → sendall `(line+"\\n").encode()` → recv → close.
3. Bonus: client sends `UPDATED <staff_id>`; server prints it.

Prefer `sendall`; always encode/decode utf-8.
"""
        ),
        code(
            '''
# Part C4 — YOUR ATTEMPT

def recv_line(sock):
    pass

# optional mini server/client below
'''
        ),
        md(
            """
---
# Checkpoints (encapsulated)

Run **after** attempting. Edit `PARTS` to choose what to mark.
"""
        ),
        code(
            '''
# CHECKPOINTS — Chain C (run after attempts)

PARTS = ("C1", "C2", "C3", "C4")


def _check_c1():
    if roster is None or len(roster.all_dicts()) < 5:
        return False, "roster needs >= 5 staff"
    d = roster.all_dicts()[0]
    for k in ("staff_id", "surname", "given", "department"):
        if k not in d:
            return False, f"as_dict missing {k}"
    return True, "ok"


def _check_c2():
    if coll is None:
        return False, "coll is None — mongo migrate not done"
    n = coll.count_documents({})
    if n < 5:
        return False, f"count {n} < 5"
    return True, "ok"


def _check_c3():
    for name in ("app", "get_mongo", "desk", "matches_view", "hire"):
        if name not in globals():
            return False, f"missing {name}"
    eps = {rule.endpoint for rule in app.url_map.iter_rules()}
    for ep in ("desk", "matches_view", "hire"):
        if ep not in eps:
            return False, f"endpoint {ep} not registered"
    return True, "ok (manual: app.run port 5002)"


def _check_c4():
    if "recv_line" not in globals() or not callable(recv_line):
        return False, "recv_line missing or not callable"
    return True, "ok"


_CHECKS = {"C1": _check_c1, "C2": _check_c2, "C3": _check_c3, "C4": _check_c4}

for part in PARTS:
    try:
        ok, detail = _CHECKS[part]()
    except Exception as e:
        ok, detail = False, str(e) + (" (is mongod running?)" if part == "C2" else "")
    print(f"{part}: {'PASS' if ok else 'FAIL — ' + detail}")
'''
        ),
    ]
    write_nb(ROOT / "P2 CHAIN C - directory.ipynb", cells)
    _write_chain_c_answers_archive()


def _write_chain_c_answers_archive() -> None:
    archive = ROOT / "_archive"
    archive.mkdir(exist_ok=True)
    cells = [
        md("# P2 CHAIN C — answers (archive only)\n\nOpen only when marking."),
        md("## Answer — Part C1"),
        code(
            '''
# Answer — Part C1
class Staff:
    def __init__(self, staff_id, surname, given, department):
        self.__staff_id = staff_id
        self.__surname = surname
        self.__given = given
        self.__department = department

    def get_staff_id(self):
        return self.__staff_id

    def as_dict(self):
        return {
            "staff_id": self.__staff_id,
            "surname": self.__surname,
            "given": self.__given,
            "department": self.__department,
        }

class Directory:
    def __init__(self):
        self.__people = []

    def add(self, staff):
        self.__people.append(staff)

    def find_by_id(self, staff_id):
        for p in self.__people:
            if p.get_staff_id() == staff_id:
                return p
        return None

    def all_dicts(self):
        return [p.as_dict() for p in self.__people]

roster = Directory()
for row in [
    (201, "Tan", "Mei", "Maths"),
    (202, "Lim", "Wei", "Computing"),
    (203, "Ong", "Siti", "Science"),
    (204, "Koh", "Ben", "Computing"),
    (205, "Raj", "Asha", "Languages"),
    (206, "Ng", "Hugo", "Maths"),
]:
    roster.add(Staff(*row))
print(roster.all_dicts())
'''
        ),
        md("## Answer — Part C2"),
        code(
            '''
# Answer — Part C2
from pymongo import MongoClient

client = MongoClient("mongodb://localhost:27017/")
db = client["chain_c_db"]
coll = db["staff"]
coll.drop()
coll.insert_many(roster.all_dicts())
for doc in coll.find({}, {"surname": 1, "department": 1, "_id": 0}):
    print(doc)
coll.update_one({"staff_id": 202}, {"$set": {"department": "Computer Science"}})
print(coll.find_one({"staff_id": 202}, {"_id": 0}))
'''
        ),
        md("## Answer — Part C3"),
        code(
            '''
# Answer — Part C3
from flask import Flask, render_template, request, redirect, url_for
from pymongo import MongoClient

app = Flask(__name__)

def get_mongo():
    client = MongoClient("mongodb://localhost:27017/")
    return client["chain_c_db"]["staff"]

@app.route("/", methods=["GET", "POST"])
def desk():
    error = None
    if request.method == "POST":
        dept_query = request.form.get("dept_query", "").strip()
        surname_query = request.form.get("surname_query", "").strip()
        if dept_query and surname_query:
            return redirect(url_for(
                "matches_view",
                dept_query=dept_query,
                surname_query=surname_query,
            ))
        error = "Please fill in all fields"
    return render_template("chain_c/desk.html", error=error)

@app.route("/matches/<dept_query>/<surname_query>")
def matches_view(dept_query, surname_query):
    people = list(get_mongo().find(
        {
            "department": {"$regex": dept_query},
            "surname": {"$regex": surname_query},
        },
        {"_id": 0},
    ))
    return render_template("chain_c/matches.html", people=people)

@app.route("/hire", methods=["GET", "POST"])
def hire():
    error = None
    if request.method == "POST":
        sid = request.form.get("sid", "").strip()
        surname = request.form.get("surname", "").strip()
        given = request.form.get("given", "").strip()
        department = request.form.get("department", "").strip()
        if not (sid and surname and given and department):
            error = "Please fill in all fields"
        else:
            get_mongo().insert_one({
                "staff_id": int(sid),
                "surname": surname,
                "given": given,
                "department": department,
            })
            return redirect(url_for("desk"))
    return render_template("chain_c/hire.html", error=error, ok=None)

if __name__ == "__main__":
    app.run(port=5002)
'''
        ),
        md("## Answer — Part C4"),
        code(
            '''
# Answer — Part C4
def recv_line(sock):
    data = b""
    while b"\\n" not in data:
        chunk = sock.recv(1024)
        if not chunk:
            break
        data += chunk
    return data.decode("utf-8").strip()

# server / client spines as comments — see SOCKETS.ipynb voice
'''
        ),
    ]
    write_nb(archive / "P2 CHAIN C - answers.ipynb", cells)


if __name__ == "__main__":
    # Chain A is frozen (in-notebook checkpoints + keys). Rebuild B/C only.
    build_chain_b()
    build_chain_c()
    print("chains B/C written (A unchanged)")
