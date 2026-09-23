#!/usr/bin/env python3
"""Convert monkeytype drills epoch3 source.py → monkeytype drills.txt.

Paste units = # ========== sections (R1, S1, …), not every blank-line gap.
Indent → literal \\t ; newlines → literal \\n.
"""

from pathlib import Path

SRC = Path("computing practical/computing practical all boilerplates/monkeytype drills epoch3 source.py")
OUT = Path("computing practical/computing practical all boilerplates/monkeytype drills.txt")

text = SRC.read_text(encoding="utf-8")
lines = text.split("\n")

# Drop file header until first section marker
sections: list[list[str]] = []
current: list[str] | None = None
for ln in lines:
    if ln.startswith("# =========="):
        if current is not None:
            sections.append(current)
        # keep a short human label as first comment line of the paste
        label = ln.strip("# ").strip("= ").strip()
        current = [f"# {label}"] if label else []
        continue
    if current is None:
        continue  # still in file header
    current.append(ln)
if current is not None:
    sections.append(current)


def indent_unit(block_lines: list[str]) -> int:
    for ln in block_lines:
        if not ln.strip() or ln.lstrip().startswith("#"):
            continue
        spaces = len(ln) - len(ln.lstrip(" "))
        if spaces and spaces % 4 == 2:
            return 2
    return 4


def convert_block(block_lines: list[str]) -> str:
    # trim leading/trailing blank lines
    while block_lines and block_lines[0].strip() == "":
        block_lines = block_lines[1:]
    while block_lines and block_lines[-1].strip() == "":
        block_lines = block_lines[:-1]
    if not block_lines:
        return ""
    unit = indent_unit(block_lines)
    converted = []
    for line in block_lines:
        if line.startswith("\t"):
            i = 0
            while i < len(line) and line[i] == "\t":
                i += 1
            converted.append(("\\t" * i) + line[i:])
            continue
        spaces = len(line) - len(line.lstrip(" "))
        content = line.lstrip(" ")
        converted.append(("\\t" * (spaces // unit)) + content)
    return "\\n".join(converted)


out_blocks = []
for sec in sections:
    body = convert_block(sec)
    if body:
        out_blocks.append(body)

header = (
    "EPOCH 3 — paste ONE section block. Literal \\t and \\n are control chars.\n"
    "Comments are the lesson (understanding > WPM). Readable: monkeytype drills epoch3 source.py\n"
    "Dropped: linear, bubble, iterative-as-separate, S&S Hash, crumb spam, flask-mongo.\n"
    "Order: R1 → S1-S4 → A1-A4 → P1 → D1-D3 → F1 → O1 → K1\n\n"
)

OUT.write_text(header + "\n\n".join(out_blocks) + "\n", encoding="utf-8", newline="\n")
print(f"wrote {len(out_blocks)} blocks to {OUT.name}")
for i, b in enumerate(out_blocks, 1):
    first = b.split("\\n", 1)[0][:72]
    print(f"  {i:02d}  {first}")
