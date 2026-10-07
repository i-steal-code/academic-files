# Final taper reading plan — Tuesday 6 October

This is optional recall after `FINAL TAPER rewrite.ipynb`, not another practice session. Read only; do not repair or rerun old notebooks. **Maximum 30 minutes. Stop by 15:00.**

## Core reread — 20 minutes

1. **`Boilerplates/ADT.ipynb` — 6 min**
   - Linked-list head, traversal, delete/miss stopping conditions.
   - BST insert and traversal order.
   - Read the hash-table comparison note only. The notebook implements separate chaining; today's rewrite is the source for linear probing.

2. **`Boilerplates/S&S.ipynb` — 5 min**
   - Bubble sort: compare current with next; equal-key tie-break uses both records.
   - Recursive binary search: miss/base condition before the next invalid range.
   - Merge sort: inclusive/exclusive slice boundaries and leftovers.

3. **`Boilerplates/DB.ipynb` — 5 min**
   - The exam loop: connect → DROP/CREATE → parameterised INSERT → SELECT/UPDATE → commit → close.
   - `sqlite3.Row`, extracting `row["field"]`, JOIN conditions, aggregates and `GROUP BY`.

4. **`Boilerplates/POOP.ipynb` — 4 min**
   - `with open(...)` for read/write.
   - Private attributes, getters/setters, child `super().__init__(...)`, overridden methods.

## Optional reread — 10 minutes only if fresh

5. **`Boilerplates/WEB DEV.ipynb` — 6 min**
   - File writer, one Flask+SQLite route, `request.form`, parameterised query, `render_template`.
   - Confirm the route, form field, SQL parameter, template variable and `row[...]` names agree.

6. **`Boilerplates/TAPER drill.ipynb` — 4 min**
   - Read the task statements and checkpoint conditions only.
   - Do not copy the old attempt cells; use them only to recall empty, first, last and missing cases.

## Do not read today

- `SOCKETS.ipynb`
- Mongo sections
- Chains A–D or LINK end-to-end
- Archived attempts or answer notebooks
- Any new paper

Finish by reading the **stuck rule**, **contract check**, and **Wednesday timeline** in `A-level P2 practical readiness.md` once.
