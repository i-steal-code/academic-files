"""
Compare same-year RI prelim vs A-level H2 Math topic footprints.
Produces hedged alignment metrics — treat as descriptive, not predictive certainty.
"""

from __future__ import annotations

import json
import re
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
OUT = REPO / "tools" / "_scan_work" / "prelim_vs_alevel_alignment.json"

# Coarse pillars used for overlap (in-syllabus for revised 9758 where noted)
PILLARS = [
    "Inequalities",
    "Functions",
    "Graphing",
    "AP_GP_Sequences",
    "Recurrence",
    "Complex",
    "Vectors",
    "Planes",
    "Diff_AoD",
    "Maclaurin",
    "Integration",
    "AoI",
    "DE",
    "Parametric",
    "PnC",
    "Probability",
    "Binomial_DRV",
    "Normal",
    "Sampling_CLT",
    "HT",
    "Corr_Reg",
]

# OUT for 2026 revised syllabus — track but exclude from "in-syllabus overlap"
OUT_PILLARS = ["Method_of_Differences", "Poisson", "Normal_approx_binomial", "Polar_DeMoivre"]

PATTERNS: dict[str, list[str]] = {
    "Inequalities": [r"inequalit", r"solve.*(≤|≥|<|>)"],
    "Functions": [r"composite function", r"inverse function", r"\bfunction f\b", r"domain and range", r"f\^-1"],
    "Graphing": [r"sketch.*(graph|curve)", r"asymptote", r"transform.*(graph|curve)"],
    "AP_GP_Sequences": [
        r"arithmetic (progression|series)",
        r"geometric (progression|series)",
        r"common (difference|ratio)",
        r"sum to infinity",
    ],
    "Recurrence": [r"recurrence", r"u_\{?n\+1\}|u_{n\+1}|u\s*n\+1"],
    "Complex": [r"complex (number|root)", r"\bArgand\b", r"\bz\s*=", r"imaginary part|real part"],
    "Vectors": [r"\bvector", r"scalar product|vector product|position vector"],
    "Planes": [r"\bplane\b", r"cartesian equation of", r"equation of (the )?plane"],
    "Diff_AoD": [r"rate of change", r"stationary point", r"\bdy/dx\b", r"differentiate"],
    "Maclaurin": [r"Maclaurin", r"series expansion", r"sufficiently small"],
    "Integration": [r"\bintegrat", r"by parts|partial fraction"],
    "AoI": [r"volume.*(rotat|revolution|solid)", r"exact area", r"area.*(region|bounded)"],
    "DE": [r"differential equation"],
    "Parametric": [r"parametric equation"],
    "PnC": [r"how many (different )?(ways|arrangements)", r"permutation|combination", r"in a (circle|row)"],
    "Probability": [r"conditional probabilit", r"independent events", r"P\([A-Z]\|[A-Z]\)", r"tree diagram"],
    "Binomial_DRV": [r"binomial", r"X\s*~\s*B\(", r"discrete random variable", r"E\(X\)", r"Var\(X\)"],
    "Normal": [r"normal distribution", r"X\s*~\s*N\(", r"linear combination"],
    "Sampling_CLT": [r"Central Limit", r"unbiased estimate", r"sample mean"],
    "HT": [r"hypothesis", r"null hypothesis|H_0|H₀", r"critical region", r"p-value|level of significance"],
    "Corr_Reg": [
        r"product moment|correlation coefficient",
        r"scatter diagram",
        r"least squares|regression line",
        r"linearisation|transformation",
    ],
    "Method_of_Differences": [r"method of differences"],
    "Poisson": [r"\bPoisson\b"],
    "Normal_approx_binomial": [r"normal approximation|approximate.*binomial|binomial.*normal approx"],
    "Polar_DeMoivre": [r"\bpolar form\b", r"De Moivre|Demoivre"],
}


def load(path: Path) -> str:
    if not path.exists() or path.stat().st_size == 0:
        return ""
    return path.read_text(encoding="utf-8", errors="replace")


def tag(text: str) -> dict[str, bool]:
    return {
        k: any(re.search(p, text, re.I) for p in pats)
        for k, pats in PATTERNS.items()
    }


def first_existing(paths: list[Path]) -> tuple[str, Path | None]:
    for p in paths:
        t = load(p)
        if len(t) > 300:
            return t, p
    return "", None


def gather_year(year: int) -> dict:
    # A-level: prefer ANS (QP often empty)
    a_p1, a_p1_src = first_existing(
        [
            REPO / "converted packages/H2 math/TYS ANS" / f"{year} P1 A-level H2 math/content.md",
            REPO / "converted packages/H2 math/TYS QP" / f"{year} P1 A-level H2 math/content.md",
        ]
    )
    a_p2, a_p2_src = first_existing(
        [
            REPO / "converted packages/H2 math/TYS ANS" / f"{year} P2 A-level H2 math/content.md",
            REPO / "converted packages/H2 math/TYS QP" / f"{year} P2 A-level H2 math/content.md",
        ]
    )
    # RI prelim
    r_p1, r_p1_src = first_existing(
        [
            REPO / "converted packages/H2 math/prelim QP" / f"{year} RI P1 prelim H2 math/content.md",
            REPO / "converted packages/H2 math/prelim ANS" / f"{year} RI P1 prelim H2 math/content.md",
        ]
    )
    r_p2, r_p2_src = first_existing(
        [
            REPO / "converted packages/H2 math/prelim QP" / f"{year} RI P2 prelim H2 math/content.md",
            REPO / "converted packages/H2 math/prelim ANS" / f"{year} RI P2 prelim H2 math/content.md",
        ]
    )

    a_text = a_p1 + "\n" + a_p2
    r_text = r_p1 + "\n" + r_p2
    if len(a_text) < 500 or len(r_text) < 500:
        return {
            "year": year,
            "usable": False,
            "reason": f"thin text a={len(a_text)} r={len(r_text)}",
        }

    a_tags = tag(a_text)
    r_tags = tag(r_text)

    a_set = {p for p in PILLARS if a_tags.get(p)}
    r_set = {p for p in PILLARS if r_tags.get(p)}
    inter = a_set & r_set
    union = a_set | r_set

    # prelim → A-level: of pillars on A-level, what fraction showed in prelim same year?
    recall = len(inter) / len(a_set) if a_set else 0.0
    # of pillars on prelim, what fraction also on A-level?
    precision = len(inter) / len(r_set) if r_set else 0.0
    jaccard = len(inter) / len(union) if union else 0.0

    a_only = sorted(a_set - r_set)
    r_only = sorted(r_set - a_set)

    out_a = [p for p in OUT_PILLARS if a_tags.get(p)]
    out_r = [p for p in OUT_PILLARS if r_tags.get(p)]

    return {
        "year": year,
        "usable": True,
        "sources": {
            "a_p1": str(a_p1_src) if a_p1_src else None,
            "a_p2": str(a_p2_src) if a_p2_src else None,
            "r_p1": str(r_p1_src) if r_p1_src else None,
            "r_p2": str(r_p2_src) if r_p2_src else None,
        },
        "a_pillars": sorted(a_set),
        "r_pillars": sorted(r_set),
        "intersection": sorted(inter),
        "a_only": a_only,
        "r_only": r_only,
        "metrics": {
            "recall_prelim_covers_alevel": round(100 * recall, 1),
            "precision_prelim_also_on_alevel": round(100 * precision, 1),
            "jaccard": round(100 * jaccard, 1),
            "n_a": len(a_set),
            "n_r": len(r_set),
            "n_inter": len(inter),
        },
        "out_topics": {"alevel": out_a, "ri": out_r},
    }


def pillar_hit_rates(years_data: list[dict]) -> dict:
    """How often each pillar appears on A-level vs RI across usable years."""
    usable = [y for y in years_data if y.get("usable")]
    n = len(usable) or 1
    a_counts = {p: 0 for p in PILLARS}
    r_counts = {p: 0 for p in PILLARS}
    both = {p: 0 for p in PILLARS}
    for y in usable:
        a = set(y["a_pillars"])
        r = set(y["r_pillars"])
        for p in PILLARS:
            if p in a:
                a_counts[p] += 1
            if p in r:
                r_counts[p] += 1
            if p in a and p in r:
                both[p] += 1
    rows = []
    for p in PILLARS:
        rows.append(
            {
                "pillar": p,
                "alevel_rate": round(100 * a_counts[p] / n, 1),
                "ri_rate": round(100 * r_counts[p] / n, 1),
                "same_year_both": round(100 * both[p] / n, 1),
                "a_hits": a_counts[p],
                "r_hits": r_counts[p],
                "both_hits": both[p],
                "n": n,
            }
        )
    rows.sort(key=lambda x: (-x["alevel_rate"], -x["same_year_both"], x["pillar"]))
    return {"n_years": n, "rows": rows}


def main() -> None:
    years = list(range(2018, 2026))
    data = [gather_year(y) for y in years]
    usable = [d for d in data if d.get("usable")]

    recalls = [d["metrics"]["recall_prelim_covers_alevel"] for d in usable]
    precisions = [d["metrics"]["precision_prelim_also_on_alevel"] for d in usable]
    jaccards = [d["metrics"]["jaccard"] for d in usable]

    def mean(xs: list[float]) -> float:
        return round(sum(xs) / len(xs), 1) if xs else 0.0

    def median(xs: list[float]) -> float:
        if not xs:
            return 0.0
        s = sorted(xs)
        m = len(s) // 2
        return s[m] if len(s) % 2 else round((s[m - 1] + s[m]) / 2, 1)

    summary = {
        "n_usable_years": len(usable),
        "mean_recall": mean(recalls),
        "median_recall": median(recalls),
        "mean_precision": mean(precisions),
        "median_precision": median(precisions),
        "mean_jaccard": mean(jaccards),
        "median_jaccard": median(jaccards),
        "recall_min_max": [min(recalls), max(recalls)] if recalls else None,
        "interpretation": (
            "Recall = share of that year's A-level pillars also tagged in same-year RI prelim. "
            "Precision = share of RI prelim pillars that also appeared on that year's A-level. "
            "Keyword tagging on ANS/QP text is noisy; treat rates as coarse descriptive signals only."
        ),
    }

    pillar_rates = pillar_hit_rates(data)

    # Manual overlays from prior human coding (higher trust for recent years)
    # Used only to soft-correct narrative, stored separately
    manual_notes = {
        "2025_alevel_p2_pure": "Ineq, vectors, integration (from prior manual TYS coding)",
        "2025_ri_p2": "Ineq, Maclaurin, sequences, planes, full stats",
        "2024_alevel_p2": "Complex + triangle/area modelling",
        "2023_alevel_p2": "Ineq, Maclaurin, vectors, parametric",
        "method_limits": (
            "Same-year prelim vs A-level is not a causal forecast. "
            "Schools set prelims months earlier; national papers share a syllabus but not a blueprint. "
            "n≈7–8 usable years is too small for high-confidence prediction."
        ),
    }

    # Hedged 2026 base rates from A-level pillar rates only (ignore RI for prediction core)
    a_rows = pillar_rates["rows"]
    high = [r for r in a_rows if r["alevel_rate"] >= 70]
    mid = [r for r in a_rows if 40 <= r["alevel_rate"] < 70]
    low = [r for r in a_rows if 0 < r["alevel_rate"] < 40]
    never = [r for r in a_rows if r["alevel_rate"] == 0]

    result = {
        "description": "Same-year RI prelim vs A-level pillar overlap (keyword tags)",
        "caveats": [
            "Descriptive overlap only — not proof that prelims predict A-level.",
            "Tagging uses converted ANS/QP text; OCR and false positives/negatives inflate noise.",
            "Sample size ~8 matched years; intervals are wide; no statistical significance claimed for year-ahead forecasts.",
            "Revised 9758 (2026) removes Poisson, normal≈binomial, method of differences — older years overstate those.",
            "P1/P2 split differs by centre; pillar presence ≠ mark weight.",
        ],
        "summary": summary,
        "by_year": data,
        "pillar_rates": pillar_rates,
        "manual_notes": manual_notes,
        "alevel_base_rates_for_2026_hedge": {
            "high_ge_70": [{"pillar": r["pillar"], "rate": r["alevel_rate"]} for r in high],
            "mid_40_69": [{"pillar": r["pillar"], "rate": r["alevel_rate"]} for r in mid],
            "low_lt_40": [{"pillar": r["pillar"], "rate": r["alevel_rate"]} for r in low],
            "absent_in_sample": [r["pillar"] for r in never],
        },
    }

    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(result, indent=2), encoding="utf-8")
    print(f"Wrote {OUT}")
    print(json.dumps(summary, indent=2))
    print("\nBy year recall/precision/jaccard:")
    for d in usable:
        m = d["metrics"]
        print(
            f"  {d['year']}: recall {m['recall_prelim_covers_alevel']}%  "
            f"prec {m['precision_prelim_also_on_alevel']}%  jac {m['jaccard']}%  "
            f"(A {m['n_a']} / R {m['n_r']} / ∩ {m['n_inter']})"
        )


if __name__ == "__main__":
    main()
