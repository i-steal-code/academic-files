#!/usr/bin/env python3
"""Restructure tutorial WhatsApp images and build Chap 19/20 discussion Q PDFs."""

from __future__ import annotations

from pathlib import Path

from PIL import Image

ROOT = Path(__file__).resolve().parents[1]
TUT = ROOT / "raw files" / "H2 physics" / "base syllabus" / "tutorials"
SRC = TUT  # images currently flat in tutorials/
OUT19 = TUT / "images" / "chap19-quantum"
OUT20 = TUT / "images" / "chap20-nuclear"
PDF19 = TUT / "Chap 19 Quantum Physics Discussion Questions.pdf"
PDF20 = TUT / "Chap 20 Nuclear Physics Discussion Questions.pdf"

# Source filenames (as on disk)
F = {
    "p6_d1d2": "WhatsApp Image 2026-07-26 at 11.42.22 PM (1).jpeg",
    "p7_mixed": "WhatsApp Image 2026-07-26 at 11.42.22 PM.jpeg",
    "p8_d6d8": "WhatsApp Image 2026-07-26 at 11.42.23 PM (3).jpeg",
    "d8d9": "WhatsApp Image 2026-07-26 at 11.42.23 PM (2).jpeg",
    "d10d13": "WhatsApp Image 2026-07-26 at 11.42.23 PM (1).jpeg",
    "challenging": "WhatsApp Image 2026-07-26 at 11.42.23 PM.jpeg",
    "c4c6_ans": "WhatsApp Image 2026-07-26 at 11.42.24 PM (1).jpeg",
    "selfcheck": "WhatsApp Image 2026-07-26 at 11.42.24 PM.jpeg",
    "n_d1d3": "WhatsApp Image 2026-07-26 at 11.43.46 PM.jpeg",
    "n_d4d5": "WhatsApp Image 2026-07-26 at 11.43.47 PM (2).jpeg",
    "n_d6d8": "WhatsApp Image 2026-07-26 at 11.43.47 PM (1).jpeg",
    "n_d9_ans": "WhatsApp Image 2026-07-26 at 11.43.47 PM.jpeg",
}


def open_rgb(path: Path) -> Image.Image:
    img = Image.open(path)
    if img.mode != "RGB":
        img = img.convert("RGB")
    return img


def save_copy(src: Path, dest: Path) -> Path:
    dest.parent.mkdir(parents=True, exist_ok=True)
    img = open_rgb(src)
    dest = dest.with_suffix(".jpg")
    img.save(dest, "JPEG", quality=92, optimize=True)
    print(f"  {dest.relative_to(TUT)}")
    return dest


def crop_vertical(src: Path, dest: Path, y0: float, y1: float) -> Path:
    """Crop fraction of height [y0, y1) where 0=top, 1=bottom."""
    dest.parent.mkdir(parents=True, exist_ok=True)
    img = open_rgb(src)
    w, h = img.size
    box = (0, int(h * y0), w, int(h * y1))
    cropped = img.crop(box)
    dest = dest.with_suffix(".jpg")
    cropped.save(dest, "JPEG", quality=92, optimize=True)
    print(f"  CROP {dest.relative_to(TUT)}  [{y0:.2f}-{y1:.2f}]")
    return dest


def images_to_pdf(paths: list[Path], out_pdf: Path) -> None:
    pages = [open_rgb(p) for p in paths]
    if not pages:
        raise SystemExit(f"No pages for {out_pdf}")
    first, rest = pages[0], pages[1:]
    out_pdf.parent.mkdir(parents=True, exist_ok=True)
    first.save(out_pdf, "PDF", resolution=150.0, save_all=True, append_images=rest)
    print(f"PDF: {out_pdf.name} ({len(pages)} pages)")


def main() -> None:
    print("Restructuring discussion-question images by chapter/topic...")
    OUT19.mkdir(parents=True, exist_ok=True)
    OUT20.mkdir(parents=True, exist_ok=True)

    # --- Chapter 19 Quantum (discussion only) ---
    q19: list[Path] = []
    q19.append(
        save_copy(
            SRC / F["p6_d1d2"],
            OUT19 / "01_D1-D2_photoelectric_wave-particle",
        )
    )
    # Mixed page: bottom = Wavefunction D4-D5 (heading ~ mid page after nuclear D3)
    q19.append(
        crop_vertical(
            SRC / F["p7_mixed"],
            OUT19 / "02_D4-D5_wavefunction_infinite_well",
            0.45,
            1.0,
        )
    )
    q19.append(
        save_copy(
            SRC / F["p8_d6d8"],
            OUT19 / "03_D6-D8_standing_waves_quantum_dots_line_spectra",
        )
    )
    q19.append(
        save_copy(
            SRC / F["d8d9"],
            OUT19 / "04_D8cont-D9_line_spectra_sodium_levels",
        )
    )
    q19.append(
        save_copy(
            SRC / F["d10d13"],
            OUT19 / "05_D10-D13_hydrogen_spectrum_uncertainty",
        )
    )

    # --- Chapter 20 Nuclear (discussion only) ---
    q20: list[Path] = []
    q20.append(
        save_copy(
            SRC / F["n_d1d3"],
            OUT20 / "01_D1-D3_nuclear_atom_radioactivity",
        )
    )
    # Gamma emission D3 from quantum booklet — nuclear topic
    q20.append(
        crop_vertical(
            SRC / F["p7_mixed"],
            OUT20 / "02_D3_gamma_emission_recoil_from_quantum_booklet",
            0.0,
            0.46,
        )
    )
    q20.append(
        save_copy(
            SRC / F["n_d4d5"],
            OUT20 / "03_D4-D5_half_life_cobalt60",
        )
    )
    q20.append(
        save_copy(
            SRC / F["n_d6d8"],
            OUT20 / "04_D6-D8_dating_fusion_fission",
        )
    )
    q20.append(
        save_copy(
            SRC / F["n_d9_ans"],
            OUT20 / "05_D9_deuterium_fusion_plus_numerical_answers",
        )
    )

    # Archive non-discussion originals aside (challenging / answers / self-check)
    other = TUT / "images" / "_excluded_non_discussion"
    for key, label in [
        ("challenging", "chap19_challenging_C1-C3"),
        ("c4c6_ans", "chap19_challenging_C4-C6_and_numerical_answers"),
        ("selfcheck", "chap19_selfcheck_solutions"),
    ]:
        save_copy(SRC / F[key], other / label)

    print("\nBuilding PDFs...")
    images_to_pdf(q19, PDF19)
    images_to_pdf(q20, PDF20)
    print("Done.")


if __name__ == "__main__":
    main()
