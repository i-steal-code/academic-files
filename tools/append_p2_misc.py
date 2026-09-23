#!/usr/bin/env python3
"""Append agreed misc sections to existing P2 boilerplate notebooks."""

from __future__ import annotations

import json
import uuid
from pathlib import Path

BASE = Path(__file__).resolve().parents[1] / "computing practical" / "computing practical all boilerplates"


def md(text: str) -> dict:
    lines = text.strip("\n").split("\n")
    src = [ln + "\n" for ln in lines[:-1]] + ([lines[-1] + "\n"] if lines else [])
    return {
        "cell_type": "markdown",
        "id": uuid.uuid4().hex[:8],
        "metadata": {},
        "source": src,
    }


def code(text: str) -> dict:
    lines = text.strip("\n").split("\n")
    src = [ln + "\n" for ln in lines[:-1]] + ([lines[-1] + "\n"] if lines else [])
    return {
        "cell_type": "code",
        "id": uuid.uuid4().hex[:8],
        "metadata": {},
        "source": src,
        "outputs": [],
        "execution_count": None,
    }


def load(name: str) -> dict:
    return json.loads((BASE / name).read_text(encoding="utf-8"))


def save(name: str, nb: dict) -> None:
    path = BASE / name
    path.write_text(
        json.dumps(nb, indent=1, ensure_ascii=False) + "\n",
        encoding="utf-8",
        newline="\n",
    )


def set_source(cell: dict, text: str) -> None:
    lines = text.split("\n")
    cell["source"] = [ln + "\n" for ln in lines[:-1]] + (
        [lines[-1] + "\n"] if lines[-1] != "" or text.endswith("\n") else []
    )


def patch_adt() -> None:
    nb = load("ADT.ipynb")
    src = "".join(nb["cells"][6]["source"])
    if "def pre_order" not in src:
        old = """    def in_order(self, node):
        if node is not None:
            self.in_order(node.get_left())
            print(node.get_data())
            self.in_order(node.get_right())
"""
        new = """    def in_order(self, node):
        # left, visit, right → ascending
        if node is not None:
            self.in_order(node.get_left())
            print(node.get_data())
            self.in_order(node.get_right())

    def pre_order(self, node):
        # visit, left, right
        if node is not None:
            print(node.get_data())
            self.pre_order(node.get_left())
            self.pre_order(node.get_right())

    def post_order(self, node):
        # left, right, visit
        if node is not None:
            self.post_order(node.get_left())
            self.post_order(node.get_right())
            print(node.get_data())
"""
        if old not in src:
            raise SystemExit("ADT: in_order block not found")
        set_source(nb["cells"][6], src.replace(old, new))

    if not any(
        c["cell_type"] == "markdown" and "Misc — traversals" in "".join(c.get("source", []))
        for c in nb["cells"]
    ):
        nb["cells"].insert(
            7,
            md(
                """### Misc — traversals (adapt from in-order)

Same recursive shape; only the **visit** position changes:

| Order | Sequence |
|-------|----------|
| in-order | left → visit → right (sorted keys) |
| pre-order | visit → left → right |
| post-order | left → right → visit |

Call with `bst.in_order(bst.get_root())` (same for pre/post)."""
            ),
        )

    for c in nb["cells"]:
        s = "".join(c.get("source", []))
        if "Exam cheat-sheet" in s and "pre_order" not in s:
            s = s.replace(
                "in_order(node): left → root → right\n",
                "in_order(node): left → root → right\n"
                "pre_order: visit → left → right\n"
                "post_order: left → right → visit\n",
            )
            if "pre_order" not in s:
                s += "\npre_order / post_order: move the print (see misc traversals)\n"
            set_source(c, s)

    save("ADT.ipynb", nb)
    print("ADT ok")


def patch_ss() -> None:
    nb = load("S&S.ipynb")
    if any("Misc — recursion patterns" in "".join(c.get("source", [])) for c in nb["cells"]):
        print("S&S already patched")
        return

    idx = next(
        i
        for i, c in enumerate(nb["cells"])
        if "complexity-lookup" in "".join(c.get("source", []))
    )
    nb["cells"][idx:idx] = [
        md(
            """<a id="misc-recursion"></a>
### Misc — recursion patterns (important only)

Same rules: **base case** → **self-call on smaller input** → **return/combine**.
Binary / merge / quick already cover range-splitting. These are the short extras papers invent."""
        ),
        code(
            """def Fact(n):
    # base: 0! and 1! = 1
    if n <= 1:
        return 1
    return n * Fact(n - 1)

def Sum1toN(n):
    # base: sum up to 0 is 0
    if n <= 0:
        return 0
    return n + Sum1toN(n - 1)

def ReverseString(s):
    # base: empty or one char already reversed
    if len(s) <= 1:
        return s
    # last char + reverse of the prefix
    return s[-1] + ReverseString(s[:-1])
"""
        ),
    ]

    for c in nb["cells"]:
        s = "".join(c.get("source", []))
        if s.startswith("# Search") and "misc-recursion" not in s:
            s = s.replace(
                "3. [Complexity lookup](#complexity-lookup)\n4. [Test scaffold](#tests)",
                "3. [Misc recursion](#misc-recursion)\n"
                "4. [Complexity lookup](#complexity-lookup)\n"
                "5. [Test scaffold](#tests)",
            )
            set_source(c, s)

    save("S&S.ipynb", nb)
    print("S&S ok")


def patch_poop() -> None:
    nb = load("POOP.ipynb")
    if any("def load_json" in "".join(c.get("source", [])) for c in nb["cells"]):
        print("POOP already patched")
        return

    i = next(
        i
        for i, c in enumerate(nb["cells"])
        if "def load_products" in "".join(c.get("source", []))
    )
    nb["cells"][i + 1 : i + 1] = [
        md(
            """### Misc — JSON text files

Same idea as CSV load, different module. Exam pattern: open → `json.load` → use dict/list → maybe `json.dump` to save."""
        ),
        code(
            """import json

def load_json(filename):
    # returns a list or dict depending on the file
    with open(filename, encoding="utf-8") as f:
        return json.load(f)

def save_json(filename, data):
    with open(filename, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)

# example shape often seen: list of dicts
# records = load_json("items.json")
# for r in records:
#     print(r["id"], r["name"])
"""
        ),
    ]
    save("POOP.ipynb", nb)
    print("POOP ok")


def patch_web() -> None:
    nb = load("WEB DEV.ipynb")
    if any("get_mongo" in "".join(c.get("source", [])) for c in nb["cells"]):
        print("WEB DEV already patched")
        return

    # insert before cheat-sheet (last cell)
    nb["cells"][-1:-1] = [
        md(
            """<a id="flask-mongo"></a>
### Misc — one Flask + mongo route (hedge)

Only if the paper forces NoSQL + web. Keep **one** read route. Full pymongo apps are not the norm — wiring practice only."""
        ),
        code(
            """# optional hedge — needs local MongoDB. Do not prioritise over sqlite Flask.
# Paste under your existing app = Flask(__name__) / imports when practising.
from pymongo import MongoClient

def get_mongo():
    client = MongoClient("mongodb://localhost:27017/")
    return client["p2db"]["lates"]

@app.route("/mongo/<reason>")
def mongo_by_reason(reason):
    coll = get_mongo()
    # inclusion projection; _id excluded
    rows = list(coll.find(
        {"Reason": reason},
        {"_id": 0, "Student_ID": 1, "Date": 1, "Reason": 1},
    ))
    return render_template("results.html", results=rows, category=reason, name="mongo")
"""
        ),
    ]
    save("WEB DEV.ipynb", nb)
    print("WEB DEV ok")


def patch_sockets() -> None:
    nb = load("SOCKETS.ipynb")
    s0 = "".join(nb["cells"][0]["source"])
    if "Brush-up checklist" in s0:
        print("SOCKETS already patched")
        return

    extra = """

### Brush-up checklist (re-type, do not expand)
1. `recv_line` — loop until `\\n`
2. Server: `socket` → `bind` → `listen` → `accept` → loop `recv_line` / `sendall` → close
3. Client: `connect` → send line with `\\n` → recv → close
4. Always encode/decode (`utf-8`); one accepted client at a time is enough for P2
"""
    set_source(nb["cells"][0], s0.rstrip() + extra + "\n")
    save("SOCKETS.ipynb", nb)
    print("SOCKETS ok")


if __name__ == "__main__":
    patch_adt()
    patch_ss()
    patch_poop()
    patch_web()
    patch_sockets()
