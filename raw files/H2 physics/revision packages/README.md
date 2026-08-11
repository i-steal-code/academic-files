# Physics revision packages

Rebuilt from `origin/` scans. Split on chapter cover pages
(`Raffles Institution Physics Department` + `Revision Package X` + topic/number).
Main package covers (Guardians / Homecoming / Endgame) are discarded.

## Layout

```text
Chap N {Title}/
  Chap N Revision Package 1.pdf   # only for chapters 12–20
  Chap N Revision Package 2.pdf   # only for chapters 1–11
  Chap N Revision Package 3.pdf   # all chapters (second full pass)
Data and Formulae Booklet.pdf
```

RP3 intentionally re-covers chapters 1–20 after RP1/RP2.

Rebuild: `python tools/rebuild_physics_revision_packages.py`