#!/usr/bin/env python3
"""Build P2 CHAIN D — exam-rubric reds (B/C notebook conventions)."""

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
        metadata={
            "kernelspec": {
                "display_name": "Python 3",
                "language": "python",
                "name": "python3",
            }
        },
    )
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(nbformat.writes(nb), encoding="utf-8", newline="\n")
    print(f"wrote {path.relative_to(ROOT.parent.parent) if False else path.name} ({len(cells)} cells)")


def build_chain_d() -> None:
    cells = [
        md(
            """
# P2 CHAIN D — exam reds (wiring + ADT)

Closed-book. Marksheet lens: required behaviour + evidence — not elegance.

**Targets (from Chains A–C remake)**
1. Flask↔sqlite **name contracts** (`request.form` keys, `url_for` endpoints, `LIKE`, **return** redirect)
2. LinkedList of **ids** + **head delete**
3. HashTable + BST **built and used** + correct pre/in/post
4. Flask↔mongo same wiring discipline
5. **LAST sockets visit** — `recv_line` only; after this, do not practise sockets again (A-level P2 hit rate ≈ 0 in TYS; even RI TP is a thin slice)

**Rules**
- Checkpoints encapsulated at the **bottom**. No answer keys in this notebook (`_archive/P2 CHAIN D - answers.ipynb` when marking).
- New template names under `templates/chain_d/` — do **not** reuse Chain A/C key names from memory; open the HTML once to read `name=` / `url_for`.
- Port **5003** (sqlite Flask) and **5004** (mongo Flask).

**DB:** uses `chain_a.db` if present (from Chain A). If missing, run the SETUP cell once.
"""
        ),
        md(
            """
---
## SETUP — seed `chain_a.db` if needed (not a red; skip if A already seeded)

If checkpoint D1 cannot open a populated DB, run this once. Prefer your Chain A seed if it still works.
"""
        ),
        code(
            '''
# SETUP — run only if chain_a.db missing / empty
import csv, sqlite3, os
from pathlib import Path

if Path("chain_a.db").exists():
    conn = sqlite3.connect("chain_a.db")
    n = conn.execute("SELECT COUNT(*) FROM sqlite_master WHERE type='table'").fetchone()[0]
    conn.close()
    if n >= 2:
        print("chain_a.db already has tables — skip SETUP")
    else:
        print("re-seed needed — edit this cell or re-run Chain A2")
else:
    print("no chain_a.db — run Chain A1+A2 first, or paste a minimal seed here")
'''
        ),
        md(
            """
---
## Part D1 — Flask ↔ sqlite name wiring (15 min)  [Gate 4 red]

Templates: `templates/chain_d/front.html`, `show.html`, `record.html`.

| Route | Endpoint **def name** | Template | Form / params |
|-------|----------------------|----------|----------------|
| `/` GET+POST | `front` | `chain_d/front.html` | POST: `q_session`, `q_name` → **return** `redirect(url_for("show", ...))` |
| `/show/<q_session>/<q_name>` | `show` | `chain_d/show.html` | JOIN; `Member.name LIKE ?` with wildcards **in the tuple**; pass `rows`, `q_session`, `q_name` |
| `/record` GET+POST | `record` | `chain_d/record.html` | POST: `in_mid`, `in_date`, `in_session` → INSERT `?` → **return** `redirect(url_for("front"))` |

Also: `get_db()` + `row_factory`. `app.run(port=5003)`.

**Evidence:** structural checkpoint + one manual search + one insert.
"""
        ),
        code(
            '''
# Part D1 — YOUR ATTEMPT
from flask import Flask, render_template, request, redirect, url_for
import sqlite3

app = Flask(__name__)

# get_db, front, show, record, __main__ port 5003
'''
        ),
        md(
            """
---
## Part D2 — LinkedList of ids + head delete (12 min)  [Gate 3 red]

Build `Node` + `LinkedList` (`is_empty`, `insert_end`, `search` → Node/None, `delete` **including head**).

Driver (required evidence):
```text
ids = [10, 20, 30, 40, 50]
# insert_end each
# delete head (10)
# search(30) found; search(-1) is None; delete(-1) no crash
# walk remaining ids somehow (helper or prints)
```

Store **integers**, not objects. `is_empty` must mean “no nodes.”
"""
        ),
        code(
            '''
# Part D2 — YOUR ATTEMPT

ids = [10, 20, 30, 40, 50]
catalogue = None
# Node, LinkedList, drive as specified
'''
        ),
        md(
            """
---
## Part D3 — HashTable + BST from catalogue (12 min)  [Gate 3 red]

Depends on **D2** working.

1. `HashTable(7)` separate chaining with `[LinkedList() for _ in range(7)]`. `insert` / `search` → bool. Insert **every id still in catalogue** after the head delete.
2. `TreeNode` + `BST`: `insert` (`<=` left), `get_root`, `in_order` / `pre_order` / `post_order` each taking a **node**.  
   **pre/post must call themselves** on children (not `in_order`).
3. Print in-order. Keep `ht` and `bst` assigned (not left as `None`).
"""
        ),
        code(
            '''
# Part D3 — YOUR ATTEMPT

ht = None
bst = None
# HashTable, TreeNode, BST; load from catalogue; print in_order
'''
        ),
        md(
            """
---
## Part D4 — Flask ↔ mongo name wiring (15 min)  [Gate 6 web slice]

Requires mongod. Seed collection yourself in this part (or reuse `chain_c_db.staff` if still populated).

Templates: `templates/chain_d/lobby.html`, `listed.html`, `onboard.html`.

| Route | Endpoint | Template | Notes |
|-------|----------|----------|-------|
| `/` GET+POST | `lobby` | `chain_d/lobby.html` | form `f_dept`, `f_surname` → **return** redirect to `listed` |
| `/listed/<f_dept>/<f_surname>` | `listed` | `chain_d/listed.html` | `render_template("chain_d/listed.html", people=...)` — **not** `url_for` as template path |
| `/onboard` GET+POST | `onboard` | `chain_d/onboard.html` | methods include POST; form `f_sid`, `f_surname`, `f_given`, `f_dept`; `insert_one`; **return** `redirect(url_for("lobby"))` |

`get_mongo()` → staff collection. Port **5004**.

**Evidence:** endpoints registered + one find + one onboard if mongod up.
"""
        ),
        code(
            '''
# Part D4 — YOUR ATTEMPT
from flask import Flask, render_template, request, redirect, url_for
from pymongo import MongoClient

app_mongo = Flask("chain_d_mongo")

# get_mongo, lobby, listed, onboard, __main__ port 5004
# (use app_mongo so D1's app is not overwritten if same kernel)
'''
        ),
        md(
            """
---
## Part D5 — LAST sockets visit (5 min)  [then stop sockets]

Write `recv_line(sock)` only: loop `recv(1024)` until `b"\\n"` (or peer closed); decode utf-8; strip.

Comment server/client spines in one line each if you want — **do not** build a full game protocol.

After checkpoint: **sockets leave the practice rotation** (TYS P2 2020–2025: 0 hits in this repo; RI TP still a thin mark cluster).
"""
        ),
        code(
            '''
# Part D5 — YOUR ATTEMPT — last sockets practice

def recv_line(sock):
    pass
'''
        ),
        md(
            """
---
# Checkpoints (encapsulated)

Edit `PARTS`, then run. Not a writing guide.
"""
        ),
        code(
            '''
# CHECKPOINTS — Chain D

PARTS = ("D1", "D2", "D3", "D4", "D5")


def _check_d1():
    g = globals()
    for name in ("app", "get_db", "front", "show", "record"):
        if name not in g:
            return False, f"missing {name}"
    rules = {rule.rule: rule.endpoint for rule in app.url_map.iter_rules() if rule.endpoint != "static"}
    if rules.get("/") != "front" or rules.get("/record") != "record":
        return False, f"route map unexpected: {rules}"
    if "show" not in rules.values():
        return False, "show endpoint missing"
    return True, "ok (manual: port 5003 search + insert)"


def _check_d2():
    if catalogue is None:
        return False, "catalogue missing"
    if not catalogue.is_empty() and catalogue.search(10) is not None:
        # head 10 should be gone
        return False, "id 10 still present — head delete?"
    if catalogue.search(30) is None:
        return False, "30 missing"
    if catalogue.search(-1) is not None:
        return False, "search(-1) should be None"
    # is_empty semantics: empty list → True
    empty = type(catalogue)()
    if empty.is_empty() is not True:
        return False, "is_empty() wrong on empty list"
    return True, "ok"


def _check_d3():
    if ht is None or bst is None:
        return False, "ht or bst still None — not constructed"
    if not ht.search(30):
        return False, "hash miss on 30"
    if not hasattr(bst, "get_root") or bst.get_root() is None:
        return False, "bst root missing"
    # pre_order must not be an alias bug: call and ensure it runs
    bst.in_order(bst.get_root())
    return True, "ok"


def _check_d4():
    g = globals()
    app_m = g.get("app_mongo") or g.get("app")
    if app_m is None:
        return False, "app_mongo/app missing"
    for name in ("get_mongo", "lobby", "listed", "onboard"):
        if name not in g:
            return False, f"missing {name}"
    eps = {rule.endpoint for rule in app_m.url_map.iter_rules()}
    for ep in ("lobby", "listed", "onboard"):
        if ep not in eps:
            return False, f"endpoint {ep} not registered"
    return True, "ok (manual: port 5004 if mongod up)"


def _check_d5():
    import inspect
    if "recv_line" not in globals() or not callable(recv_line):
        return False, "recv_line missing"
    src = inspect.getsource(recv_line)
    if "pass" in src and "recv" not in src.replace("recv_line", ""):
        return False, "recv_line body still empty"
    if "recv" not in src:
        return False, "recv_line should call sock.recv"
    return True, "ok — sockets practice ends after this"


_CHECKS = {
    "D1": _check_d1,
    "D2": _check_d2,
    "D3": _check_d3,
    "D4": _check_d4,
    "D5": _check_d5,
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
    write_nb(ROOT / "P2 CHAIN D - reds.ipynb", cells)
    _write_chain_d_answers()


def _write_chain_d_answers() -> None:
    cells = [
        md("# P2 CHAIN D — answers (archive only)\n\nMarksheet-oriented reference. Open only when marking."),
        md("## Answer — D1"),
        code(
            '''
# Answer — D1
from flask import Flask, render_template, request, redirect, url_for
import sqlite3

app = Flask(__name__)

def get_db():
    conn = sqlite3.connect("chain_a.db")
    conn.row_factory = sqlite3.Row
    return conn

@app.route("/", methods=["GET", "POST"])
def front():
    error = None
    if request.method == "POST":
        q_session = request.form.get("q_session", "").strip()
        q_name = request.form.get("q_name", "").strip()
        if q_session and q_name:
            return redirect(url_for("show", q_session=q_session, q_name=q_name))
        error = "Please fill in all fields"
    return render_template("chain_d/front.html", error=error)

@app.route("/show/<q_session>/<q_name>")
def show(q_session, q_name):
    conn = get_db()
    cur = conn.cursor()
    cur.execute(
        "SELECT Member.name, Attendance.date, Attendance.session "
        "FROM Member INNER JOIN Attendance ON Member.member_id = Attendance.member_id "
        "WHERE Attendance.session = ? AND Member.name LIKE ? "
        "ORDER BY Attendance.date",
        (q_session, f"%{q_name}%"),
    )
    rows = cur.fetchall()
    conn.close()
    return render_template(
        "chain_d/show.html", rows=rows, q_session=q_session, q_name=q_name
    )

@app.route("/record", methods=["GET", "POST"])
def record():
    error = None
    if request.method == "POST":
        in_mid = request.form.get("in_mid", "").strip()
        in_date = request.form.get("in_date", "").strip()
        in_session = request.form.get("in_session", "").strip()
        if not (in_mid and in_date and in_session):
            error = "Please fill in all fields"
        else:
            conn = get_db()
            cur = conn.cursor()
            cur.execute(
                "INSERT OR IGNORE INTO Attendance(date, member_id, session) VALUES (?,?,?)",
                (in_date, in_mid, in_session),
            )
            conn.commit()
            conn.close()
            return redirect(url_for("front"))
    return render_template("chain_d/record.html", error=error)

if __name__ == "__main__":
    app.run(port=5003)
'''
        ),
        md("## Answer — D2"),
        code(
            '''
# Answer — D2
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

ids = [10, 20, 30, 40, 50]
catalogue = LinkedList()
for x in ids:
    catalogue.insert_end(x)
catalogue.delete(10)
print(catalogue.search(30) is not None, catalogue.search(-1), catalogue.walk_ids())
catalogue.delete(-1)
'''
        ),
        md("## Answer — D3"),
        code(
            '''
# Answer — D3
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
print(ht.search(30))
bst.in_order(bst.get_root())
'''
        ),
        md("## Answer — D4"),
        code(
            '''
# Answer — D4
from flask import Flask, render_template, request, redirect, url_for
from pymongo import MongoClient

app_mongo = Flask("chain_d_mongo")

def get_mongo():
    return MongoClient("mongodb://localhost:27017/")["chain_d_db"]["staff"]

# optional seed
_coll = get_mongo()
_coll.drop()
_coll.insert_many([
    {"staff_id": 1, "surname": "Tan", "given": "Mei", "department": "Maths"},
    {"staff_id": 2, "surname": "Lim", "given": "Wei", "department": "Computing"},
    {"staff_id": 3, "surname": "Ong", "given": "Siti", "department": "Science"},
])

@app_mongo.route("/", methods=["GET", "POST"])
def lobby():
    error = None
    if request.method == "POST":
        f_dept = request.form.get("f_dept", "").strip()
        f_surname = request.form.get("f_surname", "").strip()
        if f_dept and f_surname:
            return redirect(url_for("listed", f_dept=f_dept, f_surname=f_surname))
        error = "Please fill in all fields"
    return render_template("chain_d/lobby.html", error=error)

@app_mongo.route("/listed/<f_dept>/<f_surname>")
def listed(f_dept, f_surname):
    people = list(get_mongo().find(
        {"department": {"$regex": f_dept}, "surname": {"$regex": f_surname}},
        {"_id": 0},
    ))
    return render_template("chain_d/listed.html", people=people)

@app_mongo.route("/onboard", methods=["GET", "POST"])
def onboard():
    error = None
    if request.method == "POST":
        f_sid = request.form.get("f_sid", "").strip()
        f_surname = request.form.get("f_surname", "").strip()
        f_given = request.form.get("f_given", "").strip()
        f_dept = request.form.get("f_dept", "").strip()
        if not (f_sid and f_surname and f_given and f_dept):
            error = "Please fill in all fields"
        else:
            get_mongo().insert_one({
                "staff_id": int(f_sid),
                "surname": f_surname,
                "given": f_given,
                "department": f_dept,
            })
            return redirect(url_for("lobby"))
    return render_template("chain_d/onboard.html", error=error)

if __name__ == "__main__":
    app_mongo.run(port=5004)
'''
        ),
        md("## Answer — D5 (last sockets)"),
        code(
            '''
# Answer — D5
def recv_line(sock):
    data = b""
    while b"\\n" not in data:
        chunk = sock.recv(1024)
        if not chunk:
            break
        data += chunk
    return data.decode("utf-8").strip()
# server: socket → bind → listen → accept → recv_line / sendall → close
# client: socket → connect → sendall((line+"\\n").encode()) → recv → close
'''
        ),
    ]
    write_nb(ARCHIVE / "P2 CHAIN D - answers.ipynb", cells)


if __name__ == "__main__":
    build_chain_d()
