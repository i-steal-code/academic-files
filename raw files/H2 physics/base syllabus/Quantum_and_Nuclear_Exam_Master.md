# H2 Physics — Quantum & Nuclear Exam Master Sheet

**Chapters:** 19 Quantum Physics · 20 Nuclear Physics (9478)
**Use:** formulae, decision rules, exam pointers. For diagrams and full derivations, open the lecture-note sections cited in §8.

> Notation note: `ψ²` in tables means the probability density `|ψ|²`.

---

## Contents

1. [Constants, units & conventions](#1-constants-units--conventions)
2. [Chapter 19 — Quantum Physics](#2-chapter-19--quantum-physics)
3. [Chapter 20 — Nuclear Physics](#3-chapter-20--nuclear-physics)
4. [Mechanics carried into nuclear questions](#4-mechanics-carried-into-nuclear-questions)
5. [Cross-topic links & common traps](#5-cross-topic-links--common-traps)
6. [Exam decision tables](#6-exam-decision-tables)
7. [Beyond-syllabus context](#7-beyond-syllabus-context)
8. [Lecture notes map](#8-lecture-notes-map)

---



## 1. Constants, units & conventions



### 1.1 Constants (Data booklet)


| Quantity                     | Value                     |
| ---------------------------- | ------------------------- |
| Elementary charge            | `e = 1.60 × 10⁻¹⁹ C`      |
| Planck constant              | `h = 6.63 × 10⁻³⁴ J s`    |
| Speed of light               | `c = 3.00 × 10⁸ m s⁻¹`    |
| Electron mass                | `mₑ = 9.11 × 10⁻³¹ kg`    |
| Avogadro constant            | `N_A = 6.02 × 10²³ mol⁻¹` |
| Unified atomic mass constant | `u = 1.66 × 10⁻²⁷ kg`     |


**The periodic table is NOT provided in Physics.** Only the Data and Formulae booklet. Any nuclide or molar mass you need will be stated in the question.

### 1.2 The unified atomic mass unit `u`

`1 u` is defined as **one twelfth of the mass of a carbon-12 atom**. It is *not* the mass of a nucleon.


| Particle | Mass / u |
| -------- | -------- |
| Proton   | 1.00728  |
| Neutron  | 1.00866  |
| Electron | 0.000549 |


**Two conversions, two purposes:**

```text
mass in kg   = (mass in u) × 1.66 × 10⁻²⁷      ← use with E = Δmc² in joules
energy       = (mass in u) × 931 MeV           ← use for MeV answers (faster)
```

**Critical precision rule.** Mass defect is a *small difference between large numbers*. Never round `mₚ ≈ mₙ ≈ 1 u` — the defect collapses to zero. Keep every decimal place until after the subtraction.

**Atomic vs nuclear mass.** Atomic masses include the electrons. Either convention works if applied consistently on both sides of an equation (electron masses then largely cancel); **mixing them in one calculation gives a wrong defect.**

### 1.3 Atomic mass of an element

```text
m = M / N_A       (M = molar mass in kg mol⁻¹)
m = A_r × u       (equivalent route)
```

Convert molar mass to **kg mol⁻¹** before dividing. Also feeds number density: `n = ρN_A / M`.

### 1.4 Energy units


| Unit         | Relation                |
| ------------ | ----------------------- |
| Electronvolt | `1 eV = 1.60 × 10⁻¹⁹ J` |
| MeV          | `1 MeV = 10⁶ eV`        |


- Energy levels and photons are usually quoted in **eV**; nuclear energies in **MeV**.
- Charge `q` through PD `V` gains `KE = qV`. For an electron this means `KE in eV = V in volts` numerically.
- Convert eV → J **before** using `½mv²` or `E = p²/(2m)` in SI.



### 1.5 Radioactivity units


| Unit              | Measures                                             |
| ----------------- | ---------------------------------------------------- |
| Becquerel (Bq)    | Activity: one decay per second — the examinable unit |
| Curie (Ci)        | Legacy unit; `1 Ci = 3.7 × 10¹⁰ Bq`                  |
| Counts per second | What a **detector** reads                            |
| Gray (Gy)         | Absorbed dose, J kg⁻¹ — beyond syllabus              |
| Sievert (Sv)      | Dose weighted for biological harm — beyond syllabus  |


**Count rate ≠ activity.** A detector intercepts only a fraction of emissions (solid angle, efficiency, absorption) and also picks up background. Count rate is *proportional* to activity, so the decay law still applies to it — but the number is smaller than the true Bq.

---



## 2. Chapter 19 — Quantum Physics



### 2.1 Photoelectric effect

**Evidence:** existence of a threshold frequency `f₀` supports the **particle** nature of EM radiation. Interference and diffraction support the **wave** nature.


| Formula           | Meaning                              |
| ----------------- | ------------------------------------ |
| `E = hf = hc/λ`   | Photon energy                        |
| `hf = Φ + KE_max` | Einstein photoelectric equation      |
| `Φ = hf₀`         | Work function                        |
| `KE_max = eVₛ`    | Stopping potential `Vₛ`              |
| `p = E/c = h/λ`   | Photon momentum (photon is massless) |


**Pointers**

- Intensity ↑ → more photons per second → photocurrent ↑. It does **not** raise `KE_max`.
- Frequency ↑ → `KE_max` ↑. Below `f₀` → no emission at any intensity.
- One photon is absorbed by one electron — that all-or-nothing rule is the whole point.

---



### 2.2 Wave–particle duality


| Object           | Wave evidence                                      | Particle evidence                       |
| ---------------- | -------------------------------------------------- | --------------------------------------- |
| EM radiation     | Interference, diffraction                          | Photoelectric effect, photon counting   |
| Matter (e⁻ etc.) | Electron diffraction, single-particle interference | Tracks, collisions, discrete detections |


**de Broglie**

```text
λ = h/p = h/(mv)      (non-relativistic)
```

**The only valid chain**

```
KE → v = √(2·KE/m) → p = mv → λ = h/p
```

**Do not** go `m → mc² → v`. Rest energy is not kinetic energy; mass alone never fixes a speed.

### 2.3 Nuance of duality (for explain questions)

A photon is not "a marble sometimes, a ripple other times." It is one quantum object whose **propagation** shows wave character (superposition, `λ`, interference) and whose **interactions** are particle-like (discrete `E = hf`, localised detection).

- Single-photon double slit: pattern builds one click at a time — wave statistics, particle detections.
- Classical E/B waves emerge when **many** photons occupy the same mode. It is not "photons plus a separate wave travelling together."
- Complementarity: more path information → less interference. Not a contradiction, a trade-off.

**Photons do not physically oscillate.** What oscillates is the electromagnetic **field**; a photon is a quantum of that field.

**EM waves as waves.** Since E and B oscillate perpendicular to the travel direction, EM waves are **transverse** (hence polarisable), obey **superposition**, and can form **standing waves** with nodes and antinodes (e.g. microwaves between transmitter and reflector). Energy and photons **propagate** in the travel direction — there is no row of stationary photons.

---



### 2.4 Wavefunction ψ


| Idea                | Statement                                       |
| ------------------- | ----------------------------------------------- |
| State of a particle | Wavefunction `ψ(x)`                             |
| Probability density | `ψ²` (shorthand for the squared magnitude of ψ) |
| Probability in `dx` | `P = ψ² dx`                                     |
| Normalisation       | `∫ ψ² dx = 1` over all space                    |


**Normalisation examples**

- Constant `ψ = A` on `0 ≤ x ≤ L`, zero elsewhere → `A = 1/√L`.
- Infinite well: `ψₙ(x) = √(2/L)·sin(nπx/L)`, `n = 1, 2, 3, …`

**Amplitude vs well width.** Peak of `ψ²` scales as `1/L`. Shrink `L` and the same total probability of 1 is squeezed into a narrower region, so the density rises.

**Superposition** of wavefunctions gives standing-wave solutions in a box and single-particle interference.

---



### 2.5 Infinite square well (particle in a box)

**Why "well":** potential energy is lower inside a limited region, so the particle is trapped — a trough in the PE graph.
**Why "infinite":** walls are impenetrable, so `ψ = 0` at and beyond the walls. An idealisation of a real (finite) trap that makes the boundary conditions clean.

```text
V = ∞          V = ∞
      |  V = 0  |
      0         L
```

**Standing-wave fit and energies**

```text
L = nλₙ/2   ⇒   λₙ = 2L/n,   pₙ = nh/(2L)
Eₙ = n²h²/(8mL²),   n = 1, 2, 3, …
```


| Symbol | Meaning                                                           |
| ------ | ----------------------------------------------------------------- |
| `n`    | Quantum number (`n = 1` is ground state)                          |
| `m`    | Particle mass                                                     |
| `L`    | **Width of the well** — the limit on where the particle can exist |


**Pointers**

- `E₁ > 0` always: zero-point energy. Confined does **not** mean zero energy.
- `E ∝ n²`, `E ∝ 1/L²`, `E ∝ 1/m`.
- `L` is **not** a wavelength. Rearrange for it if needed: `L = nh/√(8mEₙ)`.
- Quantum dots: smaller dot → larger `ΔE` → shorter `λ` emitted → colour shifts blue.

---



### 2.6 Atomic energy levels & line spectra

```text
hf = hc/λ = |E_upper − E_lower|
```


| Spectrum       | Process                                                                   |
| -------------- | ------------------------------------------------------------------------- |
| **Emission**   | Electron falls; photon of exactly `ΔE` is emitted. Arrows point **down**. |
| **Absorption** | Electron jumps up; those frequencies removed from continuous light.       |


**Hydrogen**

```text
Eₙ = −13.6/n² eV
```

**Why levels are negative.** The zero is set at `E = 0` for a **free electron at infinity**. Bound states lie below it, so energy must be *added* to escape. Total energy is negative because the negative electric PE outweighs the positive KE.

**When is energy positive?**


| Scale                                        | Positive energy means                                                    |
| -------------------------------------------- | ------------------------------------------------------------------------ |
| Hydrogen scale (`E∞ = 0`)                    | Free electron with leftover KE — the **continuum**, not a discrete level |
| Ground state set to 0 (e.g. sodium diagrams) | Ordinary **bound** excited states; just a shifted zero                   |
| Infinite well                                | Always positive; different model, different zero                         |


**Ionisation** is the limit `n → ∞`, at `E = 0`. Ionisation energy from level `n` is `|Eₙ|`; from the ground state it is `|E₁|`.

**Finding** `n`

```text
Eₙ = E₁/n²                    ⇒  n = √(E₁/Eₙ) = √(IE/|Eₙ|)
Ground → n by photon hf:  hf = IE(1 − 1/n²)   ⇒  n = √(IE/(IE − hf))
```

IE and `E₁` alone fix only the scale of the ladder — not a particular `n`.

**Counting lines**

- Emission lines possible among `k` populated levels: `kC2` (e.g. 5 levels → 10 lines).
- Absorption lines from a ground-state sample of `k` levels: `k − 1` (only upward from level 1).
- Shortest wavelength ↔ largest `ΔE` (e.g. top level → ground).

**Cascade logic (worked pattern).** Bombarding electrons of energy `E` populate every level with excitation energy `≤ E`. If levels 2 and 3 are reachable but 4 is not, the emission lines are `3→1`, `3→2`, `2→1` — three lines, because an atom in level 3 may descend either directly or via level 2.

**Why atoms sit in different states.** Excitation and decay are discrete random events, so a sample is a *population* spread across levels — mostly ground state, some excited. That mixture is why several emission lines appear at once.

**Fine structure / D-lines.** A "level" may actually be two very close levels. Sodium's level 2 is a pair, giving the yellow doublet at 589.0 nm and 589.6 nm, both decaying to the **ground state**. Their separation follows from `ΔE = hc(1/λ₁ − 1/λ₂) ≈ 3.4 × 10⁻²² J`.

**Not a diffraction grating.** A grating *sorts* wavelengths that already exist; energy levels *determine which wavelengths exist at all*.

---



### 2.7 Photon vs electron excitation (high-yield contrast)


|                  | Photon                                               | Bombarding electron                                              |
| ---------------- | ---------------------------------------------------- | ---------------------------------------------------------------- |
| Bound-state jump | Energy must **match** `ΔE` exactly                   | Needs **at least** `ΔE`; may reach any affordable level          |
| Surplus energy   | No such thing — absorbed whole or not at all         | Retained as KE of the **incoming** electron after the collision  |
| Ionisation       | Possible if `hf ≥ IE`; freed electron gets `hf − IE` | Possible if `KE ≥ IE`; surplus shared by the departing particles |


**Worked contrast (hydrogen, from ground):** gaps are 10.20 eV (`1→2`) and 12.09 eV (`1→3`).

- **11.40 eV photon** → matches nothing → **no transition**.
- **11.40 eV electron** → excites `1→2` and keeps 1.20 eV of KE.

**Where surplus does *not* go:** a bound electron cannot sit between levels holding spare KE. Bound energies are fixed; surplus stays with the projectile, or with a freed electron after ionisation.

**Excitation and further ionisation get easier higher up.** Levels crowd together near `E = 0`, so a high-`n` electron is weakly bound. But lifting an electron from the ground state all the way up is still expensive.

---



### 2.8 Heisenberg uncertainty principle

```text
Δx · Δp ≳ h
```

(Some texts use `ℏ` or `h/(4π)` — follow the version given in the question.)

**Why it is inherent, not experimental clumsiness.** Momentum ties to wavelength via `p = h/λ`. A sharp momentum needs a single pure wavelength — an endlessly extended wave, so position is undefined. A sharp position needs a narrow packet, which requires superposing many wavelengths, so momentum spreads. The two demands conflict; the trade-off is a property of the state.

**Exam uses**

1. Confinement estimate: `Δx ≈ L` ⇒ `Δp ≳ h/L` ⇒ `KE_min ≈ (Δp)²/(2m)`.
2. Explains why `E₁ ≠ 0` in a well — a confined particle cannot have exactly zero momentum.
3. Comparisons: for a given energy, `Δp ∝ √m`, so a proton's uncertainty ratio to an electron's is `√(mₚ/mₑ) ≈ 42.8`.
4. Order-of-magnitude only.

---



### 2.9 Quantum formula card

```text
E = hf = hc/λ
hf = Φ + KE_max;   Φ = hf₀;   KE_max = eVₛ
p_photon = h/λ = E/c;   λ_deBroglie = h/p
Eₙ = n²h²/(8mL²)   [box];   Eₙ = −13.6/n² eV   [H atom]
hf = |ΔE|;   ∫ψ² dx = 1;   Δx·Δp ≳ h
```

**Deriving** `E` **vs** `n` **— two different models**

```text
Bohr H atom:  Coulomb = centripetal, mvr = nh/2π
              ⇒ rₙ ∝ n²,  E = −ke²/(2r)  ⇒  Eₙ ∝ −1/n²

Infinite well: λₙ = 2L/n ⇒ pₙ = nh/2L ⇒ E = p²/2m ⇒ Eₙ ∝ +n²
```

---



## 3. Chapter 20 — Nuclear Physics



### 3.1 Nuclear atom & nuclides


| Symbol      | Meaning                             |
| ----------- | ----------------------------------- |
| `A`         | Nucleon number = protons + neutrons |
| `Z`         | Proton number                       |
| `N = A − Z` | Neutron number                      |
| `ᴬ_Z X`     | Nuclide notation                    |
| Isotopes    | Same `Z`, different `N`             |


**Rutherford α-scattering**


| Observation                                             | Conclusion                                                                                            |
| ------------------------------------------------------- | ----------------------------------------------------------------------------------------------------- |
| Most α pass with little deflection                      | Atom is mostly **empty space**                                                                        |
| A tiny fraction deflected > 90°, a few nearly backwards | Charge and nearly all mass concentrated in a **very small, dense, positive nucleus** (~10⁻¹⁴–10⁻¹⁵ m) |


**"Small but massive" — what it means.** The nucleus is ~10⁻¹⁵ m across versus ~10⁻¹⁰ m for the atom, so its volume is ~10¹⁵ times smaller, yet it holds over 99.9% of the mass (an electron is ~1/1836 of a proton). Nuclear density is ~10¹⁷ kg m⁻³ and roughly the same for all nuclei — which is why `R = r₀A^(1/3)`, i.e. volume ∝ A. A thinly spread positive charge (plum pudding) could never turn a fast α-particle back.

---



### 3.2 Radioactivity — nature & radiations

- **Spontaneous:** probability of decay is unaffected by temperature, pressure or chemical state.
- **Random:** impossible to predict which nucleus decays or when, though every nucleus has the same decay probability per unit time. This is what produces **fluctuating count rates**.


| Radiation | Identity                           | Ionising  | Penetration           | In E/B field               |
| --------- | ---------------------------------- | --------- | --------------------- | -------------------------- |
| **α**     | He nucleus `⁴₂He`                  | Strongest | Stopped by paper/skin | Deflected (heavy, +2e)     |
| **β⁻**    | Electron                           | Medium    | Few mm of aluminium   | Deflected more (light, −e) |
| **β⁺**    | **Positron** `e⁺` — *not a proton* | Medium    | Similar to β⁻         | Opposite sense to β⁻       |
| **γ**     | **Photon** (EM quantum)            | Weakest   | Needs lead/concrete   | Undeflected                |


**Background radiation.** Present with no source in the room:

- Cosmic rays
- Rocks and soil — uranium/thorium chains; **radon gas** is usually the largest single contributor
- Building materials
- Food and the body itself (K-40, C-14)
- Minor man-made sources

Consequence for graphs: `measured rate = source rate + background`, so the curve **flattens at the background level** instead of decaying to zero. **Subtract background from every reading before** fitting the decay law or taking logs.

**Half-life definition trap.** Defining half-life as "time for the number of nuclei in the box to halve" is wrong — the daughter nuclei stay in the box, so the total nuclei count is unchanged. Correct: the time for the number of **undecayed nuclei** (or activity, or corrected count rate) to fall to half its initial value.

---



### 3.3 Decay law toolkit

```text
A = λN
x = x₀·e^(−λt)
λ = ln 2 / t½
```


| Symbol | Meaning                                               |
| ------ | ----------------------------------------------------- |
| `A`    | Activity in Bq                                        |
| `λ`    | Decay constant                                        |
| `N`    | Number of undecayed nuclei                            |
| `t½`   | Half-life                                             |
| `x`    | `N`, activity, or **background-corrected** count rate |


**Techniques**

1. `t½ → λ = ln2/t½` → substitute into the exponential.
2. Or count half-lives: `n = t/t½` ⇒ `x = x₀/2ⁿ`.
3. From a graph: draw a **line of best fit** (random fluctuation), correct for background, read two points, then `t½ = −t·ln2 / ln(x/x₀)`.

---



### 3.4 Nuclear equations & conservation

Conserve in every process: **nucleon number** `A`, **charge** `Z`, and **mass–energy**.

```text
¹⁴₇N + ⁴₂He → ¹⁷₈O + ¹₁H
ᴬ_Z X → ᴬ_(Z+1) Y + ⁰₋₁e + ν̄        (β⁻ decay)
```

**Neutrino evidence.** β particles emerge with a **continuous** spread of kinetic energies up to a maximum. Energy and momentum conservation therefore require a second, undetected, neutral, near-massless particle — the (anti)neutrino.

---



### 3.5 Mass defect & binding energy

```text
Δm = Zmₚ + (A − Z)mₙ − m_nucleus
BE = Δm·c²
BE per nucleon = BE/A
```

- **BE** = energy needed to separate the nucleus into free nucleons = energy released when they bind.
- Higher `BE/A` → more stable.

**What mass defect is not.** It is not mass carried away by escaping fragments. It is the difference between a **bound nucleus** and its **free nucleons**, and it exists whether or not anything decays.

**Reaction Q-value** (related but distinct bookkeeping):

```text
Q = (m_reactants − m_products)·c²        Q > 0 ⇒ energy released
```

---



### 3.6 BE/A curve — fission & fusion

`BE/A` rises steeply for light nuclei, **peaks near ⁵⁶Fe** (~8.5 MeV), then falls slowly for heavy nuclei.


| Process     | Releases energy when                               |
| ----------- | -------------------------------------------------- |
| **Fusion**  | Light nuclei combine → products nearer the Fe peak |
| **Fission** | Heavy nuclei split → fragments nearer the Fe peak  |


**Trap:** "splitting always costs energy, fusing always releases it" is **false**. Energy is released whenever the products have **greater total binding energy** — i.e. whenever you move *toward* the iron peak. Splitting a light nucleus, or fusing beyond iron, would cost energy.

---



### 3.7 Applications & hazards (qualitative)

Argue from two properties:

1. **Half-life** — short for medical tracers (dose ends quickly); long for dating and durable sources.
2. **Penetration and ionisation** — α is most damaging if ingested or inhaled but stopped externally by skin; γ needs thick shielding; β is intermediate.

---



### 3.8 Nuclear formula card

```text
A = λN;   x = x₀e^(−λt);   λ = ln2/t½
Δm = Zmₚ + (A−Z)mₙ − m_nucleus;   BE = Δmc²
1 u = 1.66 × 10⁻²⁷ kg  ↔  931 MeV
Q = (Δm_reaction)c²;   E = mc²
R = r₀A^(1/3)   (constant nuclear density)
```

**Checklist for every nuclear question**

```text
1. Balance A and Z
2. Subtract background if working with count rates
3. A = λN ; λ = ln2/t½ ; exponential or ÷2ⁿ
4. Δm → BE or Q, via 931 MeV/u (keep full precision!)
5. α/β/γ properties if asked
6. BE/A argument: fuse light, fission heavy
```

---



## 4. Mechanics carried into nuclear questions

Nuclear papers reuse earlier chapters without warning. The recurring ones:

### 4.1 Elastic collisions (Chadwick-type neutron mass problems)

Two tools, both from Dynamics:

```text
Momentum:   mₙuₙ = mₙvₙ + mv
Elastic:    uₙ = v − vₙ        (relative approach = relative separation)
```

- "**Maximum** recoil speed" is the phrase that licenses treating the collision as **head-on / 1D**. No vectors needed.
- Keep `vₙ` **signed** (rightward positive). The algebra then returns the correct direction automatically: `vₙ = (mₙ − m)uₙ/(mₙ + m)`, which is negative (rebound) only when the target is heavier than the neutron.
- Applying both equations to two different targets and eliminating `uₙ` gives `mₙ = (m₁v₁ − m₂v₂)/(v₂ − v₁)`.



### 4.2 Momentum conservation in emission

γ emission recoils the nucleus: `p_nucleus = p_photon = h/λ = E/c`, so `v = E/(mc)`. Direction is opposite the photon.

### 4.3 Energy from a PD, then a field

Standard cross-chapter chain: `½mv² = qV` → `v` → then either `λ = h/p` (quantum) or `r = mv/(Bq)` (magnetic deflection).

---



## 5. Cross-topic links & common traps


| Trap                                              | Correction                                                                           |
| ------------------------------------------------- | ------------------------------------------------------------------------------------ |
| Mass alone gives de Broglie `λ`                   | Need `p` or KE first; never `mc² → v`                                                |
| Confined ⇒ zero energy                            | Infinite well has `E₁ > 0` (zero-point energy)                                       |
| `L` is a wavelength                               | `L` is the well **width**; `λₙ = 2L/n`                                               |
| Photon with more than enough energy still excites | Bound jumps need an **exact** match; electrons only need "at least"                  |
| Bound electron holds surplus KE                   | Bound energies are fixed; surplus stays with the projectile                          |
| Energy levels positive by default                 | Negative on the `E∞ = 0` scale; positive only in continuum or a shifted-zero diagram |
| Spectra are an atomic diffraction grating         | Analogy only; lines come from `ΔE` between levels                                    |
| Intensity raises `KE_max`                         | Intensity raises photocurrent only                                                   |
| `u` equals a nucleon mass                         | `u` is 1/12 of a C-12 **atom**; `mₚ = 1.00728 u`, `mₙ = 1.00866 u`                   |
| Rounding nucleon masses to 1 u                    | Destroys the mass defect — keep full precision                                       |
| Mixing atomic and nuclear masses                  | Pick one convention and use it on both sides                                         |
| β⁺ is a proton                                    | β⁺ is a **positron**                                                                 |
| γ is a mystery particle                           | γ is a **photon**                                                                    |
| Mass defect = escaped fragments                   | Mass defect = bound nucleus vs free nucleons                                         |
| Fission always consumes energy                    | Heavy-nucleus fission **releases** energy                                            |
| Forgetting background                             | Always correct count rate before fitting                                             |
| Count rate = activity                             | Proportional only; detector sees a fraction                                          |
| Expecting a periodic table                        | Not provided in Physics                                                              |


---



## 6. Exam decision tables



### Quantum


| You see…                                     | Use…                                                |
| -------------------------------------------- | --------------------------------------------------- |
| Threshold, stopping potential, work function | Photoelectric equations                             |
| "Wavelength of an electron"                  | `λ = h/p`, via KE first                             |
| Probability, normalisation                   | `ψ²`, `∫ψ² dx = 1`                                  |
| Particle in a box, quantum dot               | `Eₙ = n²h²/(8mL²)`                                  |
| Level diagram, spectral line                 | `hf = ΔE` (take the magnitude)                      |
| Emission vs absorption                       | Down = emit; up = absorb                            |
| Photon of odd energy hits atom               | Exact match or nothing                              |
| Electron bombardment                         | Any level with `ΔE ≤ KE`; count cascade lines       |
| Number of possible lines                     | `kC2` emission; `k − 1` absorption from ground      |
| Find `n`                                     | `n = √(IE ÷ Eₙ magnitude)` or `n = √(IE/(IE − hf))` |
| Confinement / minimum energy estimate        | Heisenberg with `KE ≈ p²/(2m)`                      |




### Nuclear


| You see…                              | Use…                                                    |
| ------------------------------------- | ------------------------------------------------------- |
| Rutherford scattering results         | Small, dense, positive nucleus; mostly empty atom       |
| Count rate vs time graph              | Line of best fit, subtract background, then exponential |
| Half-life, activity, `N`              | `A = λN`, `λ = ln2/t½`                                  |
| Missing particle in an equation       | Balance `A` and `Z`                                     |
| Continuous β energy spectrum          | (Anti)neutrino                                          |
| Masses of nucleus and nucleons        | `Δm`, then `BE = Δmc²` via 931 MeV/u                    |
| Energy released in a reaction         | `Q` from mass difference                                |
| Why fusion or fission releases energy | `BE/A` curve, movement toward Fe                        |
| Neutron beams, recoil speeds          | Momentum + elastic collision relations                  |
| Nucleus size or density               | `R = r₀A^(1/3)`                                         |


---



## 7. Beyond-syllabus context

Useful for intuition and Paper 3 application-style stems; not required knowledge.

- **Reactor waste reuse.** Spent fuel is ~95% uranium; reprocessing (PUREX) recovers uranium and plutonium for MOX fuel. Fast reactors can fission long-lived actinides. Individual isotopes are harvested for medicine and industry (Co-60 sterilisation, Tc-99m imaging, Pu-238 for spacecraft).
- **Radioisotope thermoelectric generators.** Decay heat → electricity via the Seebeck effect. ~5–8% efficient but no moving parts, hence deep-space missions.
- **Heat-to-electricity limits.** Any heat engine is capped by `η = 1 − T_C/T_H`. Reactors make heat; the electricity still comes from a steam cycle, so improvements mean better cycles, not beating Carnot.
- **Quantum dots in displays.** Smaller dot → larger `ΔE` → bluer emission; the basis of QLED colour conversion.

---



## 8. Lecture notes map


| Topic                                       | Open        |
| ------------------------------------------- | ----------- |
| Photoelectric effect                        | Ch 19 §19.1 |
| Duality, de Broglie                         | Ch 19 §19.2 |
| Wavefunction, normalisation, well solutions | Ch 19 §19.3 |
| Energy levels, emission/absorption spectra  | Ch 19 §19.4 |
| Heisenberg                                  | Ch 19 §19.5 |
| Rutherford, nuclides, isotopes              | Ch 20 §20.1 |
| Decay, α/β/γ, activity, half-life           | Ch 20 §20.2 |
| Nuclear equations, neutrino                 | Ch 20 §20.3 |
| Mass defect, BE, BE/A, fission and fusion   | Ch 20 §20.4 |


---



## One-line spines

- **Quantum:** energy and matter come in quanta with wave character; `ψ²` gives probability; confinement forces discrete `Eₙ`; atoms reveal their level ladder through `hf = ΔE`.
- **Nuclear:** a tiny, extremely dense nucleus; decay is spontaneous and random with exponential statistics; conserve `A`, `Z` and mass–energy; `BE = Δmc²`; move toward the iron peak to release energy.

---

*End of master sheet. Pair with tutorial drills; use timed papers for speed.*