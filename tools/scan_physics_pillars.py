#!/usr/bin/env python3
"""Rough pillar-weightage scan over the H2 physics corpus.

Signals:
  1. Syllabus breadth: lecture-note pages per chapter
  2. Working depth:    tutorial-solution pages per chapter
  3. Exam presence:    keyword hits in TYS answer papers + RI TP/CT papers
"""

from __future__ import annotations

import json
import re
import sys
from collections import defaultdict
from pathlib import Path

import fitz

ROOT = Path(r"c:\Users\debig\OneDrive\Desktop\github repository\academic-files")
PHYS = ROOT / "raw files" / "H2 physics"
BASE = PHYS / "base syllabus"
EXAM = PHYS / "exam papers"

# Chapter -> pillar
PILLAR_OF_CHAPTER = {
    1: "Classical mechanics",
    2: "Classical mechanics",
    3: "Classical mechanics",
    4: "Classical mechanics",
    5: "Classical mechanics",
    6: "Classical mechanics",
    7: "Classical mechanics",
    8: "Classical mechanics",
    9: "Wave phenomena",   # oscillations
    10: "Wave phenomena",
    11: "Wave phenomena",
    12: "Thermodynamics",
    13: "Thermodynamics",
    14: "Electrical physics",
    15: "Electrical physics",
    16: "Electrical physics",
    17: "Electrical physics",
    18: "Electrical physics",
    19: "Modern physics",
    20: "Modern physics",
}

PILLARS = [
    "Classical mechanics",
    "Wave phenomena",
    "Thermodynamics",
    "Electrical physics",
    "Modern physics",
]

# Distinctive keywords (lowercased, regex-escaped literals)
KEYWORDS: dict[str, list[str]] = {
    "Classical mechanics": [
        "momentum", "impulse", "newton", "friction", "projectile", "collision",
        "elastic collision", "centripetal", "angular velocity", "torque",
        "moment of", "equilibrium", "gravitational field", "orbit", "satellite",
        "escape", "kepler", "free fall", "acceleration", "terminal velocity",
        "work done", "kinetic energy", "potential energy", "power", "lever",
        "centre of mass", "drag",
    ],
    "Wave phenomena": [
        "wavelength", "amplitude", "frequency of the wave", "oscillat",
        "simple harmonic", "s.h.m", "damping", "resonance", "phase difference",
        "superposition", "interference", "diffraction", "double slit",
        "diffraction grating", "stationary wave", "standing wave", "node",
        "antinode", "doppler", "intensity", "polaris", "path difference",
        "transverse", "longitudinal",
    ],
    "Thermodynamics": [
        "temperature", "thermal", "ideal gas", "internal energy", "specific heat",
        "latent heat", "kelvin", "isothermal", "adiabatic", "first law of thermo",
        "boltzmann", "mole", "kinetic theory", "root mean square speed",
        "heat capacity", "thermometer", "melting", "boiling",
    ],
    "Electrical physics": [
        "resistance", "resistivity", "current", "voltage", "potential difference",
        "e.m.f", "emf", "capacitor", "capacitance", "circuit", "resistor",
        "kirchhoff", "potentiometer", "electric field", "coulomb",
        "magnetic flux", "magnetic field", "solenoid", "induced", "faraday",
        "lenz", "transformer", "alternating current", "ohm", "charge",
    ],
    "Modern physics": [
        "photon", "photoelectric", "work function", "threshold frequency",
        "de broglie", "wavefunction", "wave function", "quantum", "tunnel",
        "uncertainty principle", "energy level", "line spectr", "electronvolt",
        "nucleus", "nuclide", "isotope", "radioactive", "half-life", "half life",
        "decay constant", "binding energy", "mass defect", "fission", "fusion",
        "alpha particle", "beta", "gamma ray", "becquerel",
    ],
}


def page_counts(folder: Path) -> dict[int, int]:
    out: dict[int, int] = {}
    for pdf in folder.glob("*.pdf"):
        m = re.search(r"Chap (\d+)", pdf.name)
        if not m:
            continue
        doc = fitz.open(pdf)
        out[int(m.group(1))] = doc.page_count
        doc.close()
    return out


def extract_text(pdf: Path) -> str:
    doc = fitz.open(pdf)
    txt = "".join(page.get_text() for page in doc)
    doc.close()
    return txt.lower()


def score_text(txt: str) -> dict[str, int]:
    scores: dict[str, int] = {}
    for pillar, words in KEYWORDS.items():
        total = 0
        for w in words:
            total += len(re.findall(re.escape(w), txt))
        scores[pillar] = total
    return scores


def main() -> None:
    notes = page_counts(BASE / "lect notes")
    tuts = page_counts(BASE / "tut soln")

    by_pillar = defaultdict(lambda: {"chapters": [], "note_pages": 0, "tut_pages": 0})
    for ch, pillar in PILLAR_OF_CHAPTER.items():
        by_pillar[pillar]["chapters"].append(ch)
        by_pillar[pillar]["note_pages"] += notes.get(ch, 0)
        by_pillar[pillar]["tut_pages"] += tuts.get(ch, 0)

    # Exam keyword scoring
    exam_sets = {
        "TYS ANS (2016-2024)": sorted((EXAM / "TYS ANS").glob("*.pdf")),
        "RI TP/CT QP": sorted((EXAM / "misc" / "RI TP QP").glob("*.pdf")),
        "RI TP/CT ANS": sorted((EXAM / "misc" / "RI TP ANS").glob("*.pdf")),
    }

    exam_scores: dict[str, dict[str, int]] = {}
    per_paper: dict[str, dict[str, int]] = {}
    for label, pdfs in exam_sets.items():
        agg = dict.fromkeys(PILLARS, 0)
        for pdf in pdfs:
            txt = extract_text(pdf)
            s = score_text(txt)
            per_paper[f"{label} :: {pdf.stem}"] = s
            for k, v in s.items():
                agg[k] += v
        exam_scores[label] = agg

    result = {
        "chapters": {
            str(ch): {
                "pillar": PILLAR_OF_CHAPTER[ch],
                "note_pages": notes.get(ch, 0),
                "tut_pages": tuts.get(ch, 0),
            }
            for ch in sorted(PILLAR_OF_CHAPTER)
        },
        "by_pillar": {k: dict(v) for k, v in by_pillar.items()},
        "exam_keyword_scores": exam_scores,
        "per_paper": per_paper,
    }

    out = ROOT / "tools" / "_physics_pillar_scan.json"
    out.write_text(json.dumps(result, indent=2), encoding="utf-8")

    # Console summary (ascii-safe)
    def pct(d: dict[str, int]) -> dict[str, float]:
        tot = sum(d.values()) or 1
        return {k: round(100 * v / tot, 1) for k, v in d.items()}

    print("PILLAR | chapters | note pg | tut pg | tut/note")
    for p in PILLARS:
        b = by_pillar[p]
        ratio = b["tut_pages"] / b["note_pages"] if b["note_pages"] else 0
        print(
            f"{p:20s} | {len(b['chapters']):2d} | {b['note_pages']:4d} | "
            f"{b['tut_pages']:3d} | {ratio:.2f}"
        )

    print("\nNote-page share %:", pct({p: by_pillar[p]["note_pages"] for p in PILLARS}))
    print("Tut-page share  %:", pct({p: by_pillar[p]["tut_pages"] for p in PILLARS}))
    for label, sc in exam_scores.items():
        print(f"{label} keyword share %:", pct(sc))
    print(f"\nJSON: {out}")


if __name__ == "__main__":
    sys.exit(main())
