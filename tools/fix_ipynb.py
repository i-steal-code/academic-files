#!/usr/bin/env python3
"""Normalize and validate Jupyter notebooks (nbformat).

Fixes the recurring Paper-2 boilerplate failures:
  - stream outputs missing required \"name\" (usually stdout)
  - cells missing \"id\" (future hard error)

Usage:
  py -3 tools/fix_ipynb.py
  py -3 tools/fix_ipynb.py path/to/one.ipynb
  py -3 tools/fix_ipynb.py \"computing practical/computing practical all boilerplates\"

Exit code 0 = all valid after fix; 1 = validation still failing.
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

try:
    import nbformat
    from nbformat.validator import normalize, validate, NotebookValidationError
except ImportError:
    print("Install nbformat: py -3 -m pip install nbformat", file=sys.stderr)
    sys.exit(1)

DEFAULT_ROOTS = [
    Path("computing practical/computing practical all boilerplates"),
]


def iter_notebooks(paths: list[Path]) -> list[Path]:
    found: list[Path] = []
    for p in paths:
        if p.is_file() and p.suffix == ".ipynb":
            found.append(p)
        elif p.is_dir():
            found.extend(sorted(p.rglob("*.ipynb")))
    # skip checkpoints
    return [p for p in found if ".ipynb_checkpoints" not in p.parts]


def fix_stream_names(nb) -> int:
    n = 0
    for cell in nb.cells:
        if cell.get("cell_type") != "code":
            continue
        for out in cell.get("outputs", []):
            if out.get("output_type") == "stream" and "name" not in out:
                out["name"] = "stdout"
                n += 1
    return n


def fix_notebook(path: Path) -> tuple[bool, str]:
    with path.open(encoding="utf-8") as f:
        nb = nbformat.read(f, as_version=4)

    streams = fix_stream_names(nb)
    _, nb = normalize(nb)

    try:
        validate(nb)
    except NotebookValidationError as e:
        return False, f"FAIL {path}: {e}"

    with path.open("w", encoding="utf-8", newline="\n") as f:
        nbformat.write(nb, f)

    extra = f" (stream name fixes: {streams})" if streams else ""
    return True, f"OK   {path}{extra}"


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument(
        "paths",
        nargs="*",
        type=Path,
        help="Notebook files or directories (default: computing practical boilerplates)",
    )
    args = ap.parse_args()
    roots = args.paths or DEFAULT_ROOTS
    notebooks = iter_notebooks(roots)
    if not notebooks:
        print("No notebooks found.", file=sys.stderr)
        return 1

    ok = True
    for nb_path in notebooks:
        success, msg = fix_notebook(nb_path)
        print(msg)
        ok = ok and success
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
