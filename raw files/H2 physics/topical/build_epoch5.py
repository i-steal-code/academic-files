"""Physics Epoch 5: P1 (MCQ) diagnostic marathon covering every chapter and syllabus concept.

Sources are MCQs NOT in the four P1 dress rehearsals (2026 VJC, HCI, DHS, EJC):
2026 NYJC P1, RI P1 2021-2023 (and 2025 for one item), RI 2025 TP MCQ, RI 2023 CT and 2024 TP Section A.
Concepts no source MCQ covers get an original question (GAP items).

Output: topical/Epoch 5/Epoch 5 Questions.pdf, Epoch 5 Answer Scheme.pdf.
Question PDF carries item numbers only; sources and concepts appear on the answer scheme only.
Run: python "raw files/H2 physics/topical/build_epoch5.py"
"""
import re
import sys
from pathlib import Path

import pymupdf

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT / "tools"))
from _epoch_lib import content_extent, open_doc, page_band  # noqa: E402

PH = "raw files/H2 physics/exam papers/"
OUT = ROOT / "raw files/H2 physics/topical/Epoch 5"

QP = {
    "NYJC26": ("prelim QP/2026 NYJC P1 prelim H2 physics.pdf", 30, "2026 NYJC P1"),
    "RI21": ("prelim QP/2021 RI P1 prelim H2 physics.pdf", 30, "2021 RI P1"),
    "RI22": ("prelim QP/2022 RI P1 prelim H2 physics.pdf", 30, "2022 RI P1"),
    "RI23": ("prelim QP/2023 RI P1 prelim H2 physics.pdf", 30, "2023 RI P1"),
    "RI25": ("prelim QP/2025 RI P1 prelim H2 physics.pdf", 30, "2025 RI P1 (sat Sep)"),
    "RITP25": ("misc/RI TP QP/2025 TP MCQ A-level H2 physics.pdf", 30, "2025 RI TP MCQ"),
    "RICT23": ("misc/RI TP QP/2023 CT Sect A A-level H2 physics.pdf", 15, "2023 RI CT Sect A"),
    "RITP24": ("misc/RI TP QP/2024 TP Sect A A-level H2 physics.pdf", 30, "2024 RI TP Sect A"),
}
ANS = {
    "NYJC26": "prelim ANS/2026 NYJC P1 prelim H2 physics.pdf",
    "RI21": "prelim ANS/2021 RI P1 prelim H2 physics.pdf",
    "RI22": "prelim ANS/2022 RI P1 prelim H2 physics.pdf",
    "RI23": "prelim ANS/2023 RI P1 prelim H2 physics.pdf",
    "RI25": "prelim ANS/2025 RI P1 prelim H2 physics.pdf",
    "RITP25": "misc/RI TP ANS/2025 TP A-level H2 physics.pdf",
    "RICT23": "misc/RI TP ANS/2023 CT A-level H2 physics.pdf",
    "RITP24": "misc/RI TP ANS/2024 TP Sect A A-level H2 physics.pdf",
}

# (source, question, concept shown on the answer scheme). Part A = Ch 1-11, Part B = Ch 12-20.
PART_A = [
    ("NYJC26", 1, "Ch 1 · derived units in base units (1a–c)"),
    ("RI22", 2, "Ch 1 · homogeneity of an equation (1d)"),
    ("GAP", 1, "Ch 1 · reasonable estimates (1e)"),
    ("GAP", 2, "Ch 1 · random vs systematic error, zero error (1f)"),
    ("NYJC26", 2, "Ch 1 · combining uncertainties (1g)"),
    ("RI23", 1, "Ch 1 · resolving a vector into components (1h–j)"),
    ("RI21", 6, "Ch 2 · upthrust and spring force in equilibrium (2b, c)"),
    ("RI21", 5, "Ch 2 · principle of moments (2d, g)"),
    ("NYJC26", 4, "Ch 2 · conditions for equilibrium; couples (2e, h)"),
    ("RI23", 4, "Ch 2 · three-force equilibrium: hinge force (2i)"),
    ("RI21", 2, "Ch 3 · from a v–t graph to an s–t graph (3b, c)"),
    ("NYJC26", 5, "Ch 3 · v–t graph of a bouncing ball (3b, c, e)"),
    ("RI23", 7, "Ch 3 · Newton's second law, connected bodies (3h, i)"),
    ("NYJC26", 6, "Ch 3 · force = rate of change of momentum (3g, h)"),
    ("RI21", 7, "Ch 4 · work done and efficiency (4b, c)"),
    ("NYJC26", 7, "Ch 4 · work done as the area under F–s (4c)"),
    ("RI22", 9, "Ch 4 · kinetic energy gained from a force (4e)"),
    ("NYJC26", 8, "Ch 5 · horizontal projection (5b)"),
    ("RI23", 2, "Ch 5 · comparing projectile paths (5b)"),
    ("RI22", 8, "Ch 5 · Ep and Ek during projectile motion (5c, d)"),
    ("RI23", 3, "Ch 5 · motion with a speed-dependent resistive force (5e)"),
    ("RI21", 4, "Ch 6 · impulse = area under F–t (6a)"),
    ("NYJC26", 9, "Ch 6 · conservation of momentum; collision force (6b, c)"),
    ("GAP", 3, "Ch 6 · elastic collision: relative speeds (6d, e)"),
    ("RI21", 9, "Ch 7 · angular velocity, centripetal acceleration (7a–e)"),
    ("RI23", 8, "Ch 7 · vertical circle: tension (7f)"),
    ("RI23", 10, "Ch 8 · gravitational potential: work from infinity (8e, f)"),
    ("RI23", 9, "Ch 8 · field and potential between two masses (8c, h)"),
    ("GAP", 4, "Ch 8 · escape speed (8i)"),
    ("NYJC26", 11, "Ch 8 · circular orbits: radius, period, energy (8j)"),
    ("NYJC26", 12, "Ch 8 · geostationary orbits (8k)"),
    ("RI21", 13, "Ch 9 · a = −ω²x: maximum acceleration (9d, e)"),
    ("RI23", 11, "Ch 9 · s.h.m. graphs (9g)"),
    ("NYJC26", 13, "Ch 9 · s.h.m. kinetic energy against time (9h)"),
    ("RITP25", 1, "Ch 9 · KE : PE in s.h.m. (9f, h)"),
    ("RITP25", 3, "Ch 9 · damping (9i, k)"),
    ("RITP25", 2, "Ch 9 · resonance (9j, l)"),
    ("NYJC26", 14, "Ch 10 · longitudinal wave: particle displacements (10a, e)"),
    ("RITP24", 7, "Ch 10 · phase difference and distance (10b–d)"),
    ("RI21", 17, "Ch 10 · intensity ∝ A², inverse square (10g, h)"),
    ("RI22", 18, "Ch 10 · polarisation, Malus' law (10i, j)"),
    ("RI23", 14, "Ch 11 · stationary wave on a string (11b, c)"),
    ("RITP24", 9, "Ch 11 · stationary sound wave with a reflector (11b–d)"),
    ("NYJC26", 15, "Ch 11 · two-source interference (11e–g)"),
    ("RI21", 18, "Ch 11 · double slit (11h)"),
    ("RI21", 19, "Ch 11 · diffraction grating: number of maxima (11i)"),
    ("GAP", 5, "Ch 11 · single-slit diffraction (11k, l)"),
    ("NYJC26", 16, "Ch 11 · Rayleigh criterion (11m)"),
]
PART_B = [
    ("RI22", 13, "Ch 12 · equation of state with mass and moles (12c, d)"),
    ("NYJC26", 17, "Ch 12 · kinetic theory assumptions (12e)"),
    ("RI22", 14, "Ch 12 · mean KE ∝ T; r.m.s. speed (12g)"),
    ("RI22", 15, "Ch 13 · specific heat capacity, mixing (13g)"),
    ("GAP", 6, "Ch 13 · thermal equilibrium; zeroth law (13c, e)"),
    ("NYJC26", 18, "Ch 13 · p–V cycle and the first law (13d, f)"),
    ("RITP24", 13, "Ch 13 · compression in an insulated container (13f)"),
    ("RI23", 17, "Ch 13 · first law for a kettle (13f)"),
    ("NYJC26", 20, "Ch 14 · Coulomb's law (14a)"),
    ("NYJC26", 19, "Ch 14 · potential by superposition; work by the field (14c–e)"),
    ("RI21", 20, "Ch 14 · field lines and equipotentials (14f)"),
    ("RI22", 21, "Ch 14 · charge accelerated in a uniform field (14g–i)"),
    ("RI23", 19, "Ch 14 · oil drop between plates (14h)"),
    ("RI23", 20, "Ch 15 · I = nAvq (15b)"),
    ("RI21", 22, "Ch 15 · e.m.f. and p.d. by energy (15c, e)"),
    ("RI21", 28, "Ch 15 · a.c. mean power (15f–i)"),
    ("RI25", 26, "Ch 15 · diodes and rectification (15j); you sat this paper in September"),
    ("NYJC26", 22, "Ch 16 · fault finding in a series circuit (16b, c)"),
    ("RITP25", 17, "Ch 16 · thermistor in a circuit (16e, f)"),
    ("RICT23", 4, "Ch 16 · internal resistance; maximum power (16g)"),
    ("RI23", 22, "Ch 16 · two e.m.f.s: p.d. between points (16j)"),
    ("RI22", 23, "Ch 16 · voltmeter readings as a resistance changes (16j)"),
    ("NYJC26", 23, "Ch 16 · capacitors in series and parallel (16k)"),
    ("GAP", 7, "Ch 16 · RC discharge (16l)"),
    ("NYJC26", 24, "Ch 17 · B from two wires (17b, c)"),
    ("RI21", 25, "Ch 17 · current balance, F = BIL (17f–h)"),
    ("RI23", 23, "Ch 17 · forces between parallel wires (17i)"),
    ("RITP25", 22, "Ch 17 · r = mv/Bq (17j, k)"),
    ("RICT23", 6, "Ch 17 · electron path in a magnetic field (17l)"),
    ("GAP", 8, "Ch 17 · velocity selector (17m)"),
    ("RI21", 27, "Ch 18 · change in flux linkage (18a–c)"),
    ("RITP25", 23, "Ch 18 · Lenz's law: concentric loops (18d, e)"),
    ("RI23", 24, "Ch 18 · e.m.f. in a moving rod (18e)"),
    ("NYJC26", 25, "Ch 18 · eddy currents (18f)"),
    ("NYJC26", 26, "Ch 18 · transformer and transmission loss (18g)"),
    ("RI21", 30, "Ch 19 · photoelectric emission rate (19a)"),
    ("RI22", 28, "Ch 19 · energy levels and visible photons (19b)"),
    ("NYJC26", 27, "Ch 19 · photon momentum, radiation pressure (19c)"),
    ("RI23", 27, "Ch 19 · de Broglie wavelength (19d, e)"),
    ("NYJC26", 28, "Ch 19 · wavefunction: the electron cloud (19f, g)"),
    ("RITP25", 27, "Ch 19 · uncertainty principle (19h)"),
    ("GAP", 9, "Ch 19 · infinite square well (19i)"),
    ("RITP25", 28, "Ch 20 · Rutherford scattering (20a)"),
    ("RI23", 30, "Ch 20 · random nature of decay (20d, e)"),
    ("RI22", 30, "Ch 20 · background count and half-life (20f, j)"),
    ("RITP25", 30, "Ch 20 · properties and uses of radiation (20g, l)"),
    ("NYJC26", 29, "Ch 20 · decay law and half-life (20h–k)"),
    ("RITP24", 29, "Ch 20 · α-decay: kinetic energy split (20m)"),
    ("NYJC26", 30, "Ch 20 · binding energy per nucleon, fission (20n, o)"),
]

GAP = {
    1: ("Which value is closest to the kinetic energy of an adult sprinting at top speed?",
        ["20 J", "200 J", "2 kJ", "20 kJ"], "C",
        "Mass about 70 kg, speed about 8–10 m s⁻¹: ½ × 70 × 9² ≈ 2.8 × 10³ J, so about 2 kJ."),
    2: ("A micrometer screw gauge has a zero error of +0.02 mm that a student does not correct. "
        "The student takes ten readings of the diameter of a wire and calculates their mean. Which statement is correct?",
        ["The zero error is a random error, and averaging the ten readings removes it.",
         "The zero error is a systematic error. It makes the mean less accurate but does not reduce the precision of the readings.",
         "The zero error is a systematic error. It reduces the precision of the readings but not the accuracy of the mean.",
         "The zero error is a random error. It reduces the accuracy of the mean but not the precision of the readings."], "B",
        "A zero error shifts every reading by the same amount in the same direction: systematic. "
        "Averaging cannot remove it. The readings stay as close together as before (precision unchanged) but are all off the true value (accuracy lost)."),
    3: ("Sphere P of mass 2.0 kg moves to the right at 5.0 m s⁻¹. It collides head-on with sphere Q of mass 1.0 kg, "
        "which moves to the left at 1.0 m s⁻¹. The collision is perfectly elastic. What is the velocity of Q after the collision?",
        ["3.0 m s⁻¹ to the right", "5.0 m s⁻¹ to the right", "7.0 m s⁻¹ to the right", "9.0 m s⁻¹ to the right"], "C",
        "Momentum (right positive): 2.0(5.0) + 1.0(−1.0) = 9.0 = 2.0v_P + 1.0v_Q. Elastic: relative speed of approach 6.0 = "
        "relative speed of separation, so v_Q − v_P = 6.0. Solving: v_P = 1.0 m s⁻¹, v_Q = 7.0 m s⁻¹ to the right. "
        "Check KE: 25.5 J before and after."),
    4: ("The escape speed from the surface of planet X is v. Planet Y has the same density as X and twice its radius. "
        "What is the escape speed from the surface of Y?",
        ["v", "√2 v", "2v", "2√2 v"], "C",
        "½mv² = GMm/R gives v = √(2GM/R). Same density: M ∝ R³, so M/R ∝ R² and v ∝ R. Twice the radius: 2v."),
    5: ("Light of wavelength 600 nm is incident normally on a single slit of width 0.12 mm. "
        "A screen is 2.0 m from the slit. What is the width of the central bright fringe on the screen?",
        ["5.0 mm", "10 mm", "20 mm", "40 mm"], "C",
        "First minima at b sin θ = λ: sin θ = 600 × 10⁻⁹ / 0.12 × 10⁻³ = 5.0 × 10⁻³. Each minimum is 2.0 × 5.0 × 10⁻³ = 10 mm "
        "from the centre, so the central maximum is 20 mm wide (10 mm is the slip twin: half the width)."),
    6: ("Body P is in thermal equilibrium with body Q. Body Q is in thermal equilibrium with body R. "
        "The three bodies are of different materials and masses. Which statement must be true?",
        ["P and R have the same internal energy.",
         "P and R are at the same temperature.",
         "There is a net transfer of energy from P to R when they are placed in thermal contact.",
         "P, Q and R have the same heat capacity."], "B",
        "Zeroth law: P and R are each in thermal equilibrium with Q, so they are in thermal equilibrium with each other, "
        "which means the same temperature. With no temperature difference there is no net energy transfer. "
        "Internal energy and heat capacity depend on mass and material, so they need not be equal."),
    7: ("A capacitor of capacitance 470 μF is charged to 12 V and then discharged through a resistor of resistance 10 kΩ. "
        "What is the potential difference across the capacitor 4.7 s after the discharge starts?",
        ["1.6 V", "4.4 V", "6.0 V", "7.6 V"], "B",
        "τ = RC = 10 × 10³ × 470 × 10⁻⁶ = 4.7 s, so t = τ and V = 12e⁻¹ = 4.4 V. "
        "7.6 V is 12(1 − e⁻¹), the charging curve; 1.6 V is 12e⁻²."),
    8: ("Positive ions enter a region where a uniform electric field of strength 2.0 × 10⁴ V m⁻¹ and a uniform magnetic field "
        "of flux density 0.050 T are perpendicular to each other and to the ions' velocity. Ions of one speed pass through undeflected. "
        "Which row gives that speed, and what happens to an ion moving at twice that speed?",
        ["1.0 × 10³ m s⁻¹; deflected in the direction of the electric force",
         "1.0 × 10³ m s⁻¹; deflected in the direction of the magnetic force",
         "4.0 × 10⁵ m s⁻¹; deflected in the direction of the electric force",
         "4.0 × 10⁵ m s⁻¹; deflected in the direction of the magnetic force"], "D",
        "Undeflected when qE = Bqv, so v = E/B = 2.0 × 10⁴ / 0.050 = 4.0 × 10⁵ m s⁻¹ (1.0 × 10³ is E × B). "
        "At twice the speed Bqv > qE, so the magnetic force wins."),
    9: ("An electron is confined in a one-dimensional infinite square well of width L. Its wavefunction is the standing-wave "
        "solution with n = 3. Which row gives the electron's de Broglie wavelength and the number of points between the walls "
        "where the probability of finding the electron is zero?",
        ["2L/3; 2", "2L/3; 3", "3L/2; 2", "L/3; 2"], "A",
        "n half-wavelengths fit the well: 3(λ/2) = L, so λ = 2L/3. The n = 3 standing wave has nodes at the walls and two "
        "between them, at L/3 and 2L/3, where |ψ|² = 0."),
}

A4 = pymupdf.paper_rect("a4")
M = 42
COLW = A4.width - 2 * M


def rel(k):
    return PH + QP[k][0]


def starts(path, n):
    """Sequential question-number starts (page, y, x, word bbox) at a consistent left margin."""
    d = open_doc(path)
    cands = []
    for pno, page in enumerate(d):
        W, H = page.rect.width, page.rect.height
        if pno == 0:
            continue
        for w in page.get_text("words"):
            x0, y0, x1, y1, t = w[:5]
            if x0 > 0.2 * W or y0 < 0.05 * H or y0 > 0.95 * H or not re.fullmatch(r"\d{1,2}\.?", t):
                continue
            q = int(t.rstrip("."))
            if 1 <= q <= n:
                cands.append((pno, y0, q, x0, pymupdf.Rect(x0, y0, x1, y1)))
    cands.sort(key=lambda c: (c[0], c[1]))
    best = {}
    for seed in [c for c in cands if c[2] == 1]:
        pool = [c for c in cands if abs(c[3] - seed[3]) <= 12]
        got, pos = {1: seed}, seed[:2]
        for q in range(2, n + 1):
            hit = next((c for c in pool if (c[0], c[1]) > pos and c[2] == q), None)
            if not hit:
                break
            got[q], pos = hit, hit[:2]
        if len(got) > len(best):
            best = got
    return best


def ans_starts(path, n):
    """Worked-solution starts: 'q' at the left margin with the answer letter beside it."""
    d = open_doc(path)
    cands = []
    for pno, page in enumerate(d):
        W = page.rect.width
        words = page.get_text("words")
        for w in words:
            x0, y0, x1, y1, t = w[:5]
            if x0 > 0.2 * W or not re.fullmatch(r"\d{1,2}", t):
                continue
            q = int(t)
            if not 1 <= q <= n:
                continue
            row = sorted((v for v in words if abs(v[1] - y0) < 4 and x1 < v[0] < x1 + 0.12 * W), key=lambda v: v[0])
            if row and re.fullmatch(r"[ABCD]", row[0][4]):
                cands.append((pno, y0, q, x0, row[0][4]))
    cands.sort(key=lambda c: (c[0], c[1]))
    best = {}
    for seed in [c for c in cands if c[2] == 1]:
        pool = [c for c in cands if abs(c[3] - seed[3]) <= 12]
        got, pos = {1: seed}, seed[:2]
        for q in range(2, n + 1):
            hit = next((c for c in pool if (c[0], c[1]) > pos and c[2] == q), None)
            if not hit:
                break
            got[q], pos = hit, hit[:2]
        if len(got) > len(best):
            best = got
    return best


def nyjc_answers():
    d = open_doc(PH + ANS["NYJC26"])
    out = []
    for pno, page in enumerate(d):
        for m in re.finditer(r"Ans\s*:?\s*([ABCD])\b", page.get_text()):
            out.append((m.group(1), pno))
    assert len(out) == 30, len(out)
    return {i + 1: v for i, v in enumerate(out)}


def pieces(path, p0, y0, p1, y1):
    """Clip rectangles for a region that may run over page breaks, trimmed to content."""
    d = open_doc(path)
    out = []
    for p in range(p0, p1 + 1):
        W = d[p].rect.width
        top, bot = page_band(path, p)
        a = y0 if p == p0 else top
        b = y1 if p == p1 else bot
        ext = content_extent(path, p, a, b)
        if ext and ext[1] - ext[0] > 6:
            out.append((p, pymupdf.Rect(0.04 * W, ext[0], 0.97 * W, ext[1])))
    return out


def question_regions(key, q, cache={}):
    path = rel(key)
    if key not in cache:
        cache[key] = starts(path, QP[key][1])
    st = cache[key]
    assert q in st, (key, q, sorted(st))
    p0, y0, _, _, num = st[q]
    if q + 1 in st:
        p1, y1 = st[q + 1][0], st[q + 1][1] - 6
    else:
        p1, y1 = p0, open_doc(path)[p0].rect.height
        end = [r for r in open_doc(path)[p0].search_for("End of Paper") if r.y0 > y0]
        if end:
            y1 = end[0].y0 - 4
    return path, pieces(path, p0, y0 - 6, p1, y1), (p0, num)


def solution_regions(key, q, cache={}):
    path = PH + ANS[key]
    if key not in cache:
        cache[key] = ans_starts(path, QP[key][1])
    st = cache[key]
    assert q in st, (key, q, sorted(st))
    p0, y0, _, _, letter = st[q]
    if q + 1 in st:
        p1, y1 = st[q + 1][0], st[q + 1][1] - 4
    else:  # last MCQ: stop at the next numbered answer (e.g. structured-question answers follow)
        page = open_doc(path)[p0]
        p1, y1 = p0, page.rect.height
        nxt = [w for w in page.get_text("words")
               if w[4] == str(q + 1) and w[0] < 0.2 * page.rect.width and w[1] > y0 + 4]
        if nxt:
            y1 = min(w[1] for w in nxt) - 4
    return path, pieces(path, p0, y0 - 4, p1, y1), letter


class Writer:
    def __init__(self, title):
        self.doc = pymupdf.open()
        self.title = title
        self.page = None
        self.y = 0

    def new_page(self):
        self.page = self.doc.new_page(width=A4.width, height=A4.height)
        self.y = M

    def need(self, h):
        if self.page is None or self.y + h > A4.height - M:
            self.new_page()

    def text(self, html, h_guess=400, css=""):
        self.need(40)
        r = pymupdf.Rect(M, self.y, M + COLW, A4.height - M)
        spare, _ = self.page.insert_htmlbox(r, html, css="* {font-family: sans-serif; font-size: 10.5pt;} " + css)
        if spare < 0:  # did not fit: new page and retry
            self.new_page()
            r = pymupdf.Rect(M, self.y, M + COLW, A4.height - M)
            spare, _ = self.page.insert_htmlbox(r, html, css="* {font-family: sans-serif; font-size: 10.5pt;} " + css)
        self.y = r.y1 - spare + 6

    def crop(self, path, pno, clip):
        s = min(1.0, COLW / clip.width)
        h = clip.height * s
        self.need(h + 4)
        tgt = pymupdf.Rect(M, self.y, M + clip.width * s, self.y + h)
        self.page.show_pdf_page(tgt, open_doc(path), pno, clip=clip)
        self.y += h + 4
        return tgt, s

    def footer(self):
        n = len(self.doc)
        for i, p in enumerate(self.doc):
            p.insert_text((M, A4.height - 22), f"{self.title} · page {i + 1} of {n}", fontsize=8,
                          fontname="helv", color=(0.4, 0.4, 0.4))


def place(w, path, pno, clip, hide=None):
    tgt, s = w.crop(path, pno, clip)
    if hide is not None and hide.intersects(clip):
        r = pymupdf.Rect(tgt.x0 + (hide.x0 - clip.x0) * s - 2, tgt.y0 + (hide.y0 - clip.y0) * s - 2,
                         tgt.x0 + (hide.x1 - clip.x0) * s + 2, tgt.y0 + (hide.y1 - clip.y0) * s + 2)
        w.page.draw_rect(r, color=None, fill=(1, 1, 1))


def first_height(regs):
    clip = regs[0][1]
    return min(A4.height - 2 * M - 30, clip.height * min(1.0, COLW / clip.width))


def gap_html(n, with_answer=False):
    q, opts, ans, sol = GAP[n]
    rows = "".join(f"<tr><td style='width:24px;vertical-align:top'><b>{L}</b></td><td style='width:480px'>{o}</td></tr>" for L, o in zip("ABCD", opts))
    html = f"<p>{q}</p><table style='width:100%'>{rows}</table>"
    if with_answer:
        html = f"<p><b>Worked solution:</b> {sol}</p>"
    return html


def build():
    OUT.mkdir(parents=True, exist_ok=True)
    nyjc = nyjc_answers()
    items = [("A", i) for i in PART_A] + [("B", i) for i in PART_B]
    qw = Writer("Physics Epoch 5 · P1 diagnostic marathon · questions")
    aw = Writer("Physics Epoch 5 · answer scheme")
    key_rows = []
    part = None
    for n, (pt, (src, q, concept)) in enumerate(items, start=1):
        label = f"E5-{n:02d}"
        if pt != part:
            part = pt
            cnt = len(PART_A) if pt == "A" else len(PART_B)
            qw.new_page()
            qw.text(f"<h2>Part {pt}</h2><p>{cnt} questions. Target {2 * cnt} minutes (2 minutes per question, P1 pace). "
                    "Write your letter and S / E / G (sure, educated guess, guess) for each question on a separate sheet.</p>")
        if src == "GAP":
            qw.need(190)
            qw.text(f"<p><b>{label}</b></p>", css="p {margin:0}")
            qw.text(gap_html(q))
            letter, where = GAP[q][2], "Original question (no past MCQ covers this concept)"
        else:
            path, regs, (p0, num) = question_regions(src, q)
            assert regs, (src, q)
            qw.need(24 + first_height(regs))
            qw.text(f"<p><b>{label}</b></p>", css="p {margin:0}")
            for i, (p, clip) in enumerate(regs):
                place(qw, path, p, clip, hide=num if (i == 0 and p == p0) else None)
            where = f"{QP[src][2]} Q{q}"
            if src == "NYJC26":
                letter = nyjc[q][0]
            else:
                _, _, letter = solution_regions(src, q)
        qw.y += 10
        key_rows.append((label, letter, where, concept))
        # answer scheme entry
        if src not in ("GAP", "NYJC26"):
            aw.need(40 + first_height(solution_regions(src, q)[1]))
        else:
            aw.need(110)
        aw.text(f"<p><b>{label} · Answer {letter}</b> · {where}<br/><i>Tests:</i> {concept}</p>", css="p {margin:0}")
        if src == "GAP":
            aw.text(gap_html(q, with_answer=True))
        elif src == "NYJC26":
            aw.text(f"<p>Worked solution: 2026 NYJC P1 answer file (exam papers/prelim ANS), page {nyjc[q][1] + 1}.</p>")
        else:
            spath, sregs, _ = solution_regions(src, q)
            for p, clip in sregs:
                place(aw, spath, p, clip)
        aw.y += 12
    # answer key table at the front of the answer scheme
    key = pymupdf.open()
    kw = Writer("Physics Epoch 5 · answer scheme")
    kw.doc = key
    kw.new_page()
    half = len(PART_A)
    rows_a = "".join(f"<tr><td>{a}</td><td><b>{b}</b></td><td>{d}</td></tr>" for a, b, c, d in key_rows[:half])
    rows_b = "".join(f"<tr><td>{a}</td><td><b>{b}</b></td><td>{d}</td></tr>" for a, b, c, d in key_rows[half:])
    css = "td {font-size: 8.5pt; padding: 0 6px 0 0;} h2 {font-size: 13pt}"
    kw.text(f"<h2>Answer key · Part A</h2><table>{rows_a}</table>", css=css)
    kw.text(f"<h2>Answer key · Part B</h2><table>{rows_b}</table>", css=css)
    kw.doc.insert_pdf(aw.doc)
    kw.footer()
    qw.footer()
    qw.doc.save(OUT / "Epoch 5 Questions.pdf", garbage=3, deflate=True)
    kw.doc.save(OUT / "Epoch 5 Answer Scheme.pdf", garbage=3, deflate=True)
    print(f"{len(items)} items: Part A {len(PART_A)}, Part B {len(PART_B)}; "
          f"questions {len(qw.doc)} pages, answer scheme {len(kw.doc)} pages")
    print("key A:", "".join(r[1] for r in key_rows[:half]))
    print("key B:", "".join(r[1] for r in key_rows[half:]))


if __name__ == "__main__":
    build()
