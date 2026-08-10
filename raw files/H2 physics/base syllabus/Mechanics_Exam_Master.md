#  H2 Physics — Mechanics Exam Master Sheet

**Chapters:** 1 Quantities & Measurement · 2 Forces & Moments · 3 Motion & Forces · 4 Energy & Fields · 5 Projectile Motion · 6 Collisions · 7 Circular Motion · 8 Gravitational Fields (9478)

**Use:** formulae, examinable definitions, decision rules, Phase-1 tutorial triage. For diagrams and full derivations, open the lecture-note sections cited in §10.

> Notation note: in tables, avoid bare `|` inside code spans (breaks Markdown tables). Write `Δp/p` rather than fraction bars with pipes.

---

## Contents

1. [How to use this sheet (Phase 1 vs Phase 2)](#1-how-to-use-this-sheet-phase-1-vs-phase-2)
2. [Chapter 1 — Quantities & Measurement](#2-chapter-1--quantities--measurement)
3. [Chapter 2 — Forces & Moments](#3-chapter-2--forces--moments)
4. [Chapter 3 — Motion & Forces](#4-chapter-3--motion--forces)
5. [Chapter 4 — Energy & Fields](#5-chapter-4--energy--fields)
6. [Chapter 5 — Projectile Motion](#6-chapter-5--projectile-motion)
7. [Chapter 6 — Collisions](#7-chapter-6--collisions)
8. [Chapter 7 — Circular Motion](#8-chapter-7--circular-motion)
9. [Chapter 8 — Gravitational Fields](#9-chapter-8--gravitational-fields)
10. [Cross-topic links & common traps](#10-cross-topic-links--common-traps)
11. [Phase 1 tutorial triage (Ch 1–5)](#11-phase-1-tutorial-triage-ch-15)
12. [Lecture notes map](#12-lecture-notes-map)

---

## 1. How to use this sheet (Phase 1 vs Phase 2)


| Phase              | Chapters | Goal                                                                                                        |
| ------------------ | -------- | ----------------------------------------------------------------------------------------------------------- |
| **Phase 1 (now)**  | 1–5      | Cram core tools: units/uncertainty, statics, N2L, energy, projectiles. Skim low-value tutorial parts.       |
| **Phase 2 (next)** | 6–8      | Deep work. Difficulty and paper weight jump here: momentum/collisions, circular motion, gravitation/orbits. |


**Why Ch 6–8 get more time**

- They appear as **full structured questions**, not just MCQ fillers.
- They **reuse** Ch 1–5 constantly (resolve forces, energy, sign convention, `F = dp/dt`).
- Vertical circles and orbits combine **dynamics + energy** under one diagram — the classic A-level trap zone.

**Phase 1 rule of thumb:** if a Ch 1–5 question only drills a skill you already do cleanly (plain SUVAT, one-step Hooke, read-a-definition), skim the solution once. Spend the saved time on Ch 6–8 and on the **MUST / HIGH** items in §11.

---

## 2. Chapter 1 — Quantities & Measurement

### 2.1 Examinable definitions


| Term                     | Wording to write                                                                  |
| ------------------------ | --------------------------------------------------------------------------------- |
| **Base quantity**        | Most fundamental physical quantities used to define others                        |
| **Derived quantity**     | Formed by combining base quantities by products/quotients                         |
| **Homogeneous equation** | Every term has the same base units (necessary but not sufficient for correctness) |
| **Systematic error**     | All readings always above or always below the true value by a fixed amount        |
| **Random error**         | Readings scattered about the mean; equal chance of + or −                         |
| **Accuracy**             | Closeness of the mean to the true value (hit by systematic error)                 |
| **Precision**            | Agreement of repeated measurements (hit by random error)                          |
| **Resolution**           | Smallest graduation on the instrument scale                                       |
| **Scalar / vector**      | Magnitude only / magnitude and direction                                          |


Base quantities in syllabus: mass, length, time, current, temperature, amount of substance. (Candela not required.)

### 2.2 Uncertainty rules (memorise)

```text
Q = aX ± bY          →  ΔQ = |a|ΔX + |b|ΔY
Q = a X^m Y^n        →  ΔQ/Q = |m|ΔX/X + |n|ΔY/Y
```

- Absolute uncertainty: **1 s.f.**; quote the quantity to the **same decimal place**.
- Fractional/percentage uncertainty: **2 s.f.**
- Uncertainties **never cancel** — always add.
- For awkward functions (`cos θ`, etc.): use upper–lower bound: `ΔQ = (Q_max − Q_min)/2`.
- Always rearrange the subject **before** differentiating/propagating.

Least-s.f. / least-d.p. rules are a **quick alternative** for simple multiply/add; when the question asks for uncertainty analysis, use the fractional method.

### 2.3 Vectors

```text
F = √(Fx² + Fy²)      tan θ = Fy/Fx   (watch quadrant)
Δv = v − u            (vector subtraction — draw tip-to-tail)
```

Sign convention first. Obtuse angles: check components, do not blindly take the acute inverse-tan.

### 2.4 Lecture-note pointers

- Homogeneity pitfalls: LN §1.2
- Accuracy vs precision diagrams: LN §1.7
- Uncertainty worked examples: LN §1.8
- Vector addition/subtraction: LN §1.9

---

## 3. Chapter 2 — Forces & Moments

### 3.1 Force types (quick)


| Force                 | Direction / note                                           |
| --------------------- | ---------------------------------------------------------- |
| Weight `W = mg`       | Vertically down through **centre of gravity**              |
| Normal `N`            | Perpendicular to surface, away from it                     |
| Upthrust `U`          | Vertically up; = weight of fluid displaced                 |
| Friction `f`          | Parallel to surfaces; opposes relative (or tending) motion |
| Tension / compression | Along a string/rod; pull / push                            |
| Hooke `F = kx`        | Within limit of proportionality                            |


Friction coefficients `μ` and viscosity: **knowledge not required** (appendix only).

### 3.2 Definitions


| Term                     | Wording                                                                                                     |
| ------------------------ | ----------------------------------------------------------------------------------------------------------- |
| **Centre of gravity**    | Point at which the weight of the body appears to act                                                        |
| **Moment of a force**    | Product of the force and the **perpendicular distance** of its line of action from the axis: `τ = F × L`    |
| **Couple**               | Pair of equal and opposite forces whose lines of action do not coincide; tends to produce **rotation only** |
| **Torque of a couple**   | `Fd` (one force × perpendicular separation)                                                                 |
| **Principle of moments** | For equilibrium: sum of clockwise moments about any axis = sum of anticlockwise moments about the same axis |
| **Equilibrium**          | Resultant force = 0 **and** resultant moment about any axis = 0                                             |


Three coplanar forces in equilibrium: lines of action all parallel, **or** all concurrent.

### 3.3 Exam habits

1. Draw a clean **free-body diagram** first.
2. Take moments about a point that **eliminates an unknown** (usually the hinge).
3. Then resolve `ΣFx = 0`, `ΣFy = 0` for the remaining unknowns.
4. Toppling: contact force at far support → 0; line of weight passes through pivot edge.
5. Tension vs compression along a member: resolve **along** the member and see which way the ends are pulled/pushed.

### 3.4 Lecture-note pointers

- Force catalogue + Hooke graph: LN §2.1
- Moment / couple diagrams: LN §2.2
- Concurrent three-force argument: LN §2.3
- CG of lamina (plumbline): Appendix

---

## 4. Chapter 3 — Motion & Forces

### 4.1 Kinematics definitions


| Term                       | Definition                                                  |
| -------------------------- | ----------------------------------------------------------- |
| Distance                   | Total path length (scalar)                                  |
| Displacement               | Distance in a specified direction from a reference (vector) |
| Instantaneous speed        | `dx/dt`                                                     |
| Instantaneous velocity     | `ds/dt`                                                     |
| Instantaneous acceleration | `dv/dt`                                                     |
| Average speed / velocity   | `Δx/Δt` / `Δs/Δt`                                           |


### 4.2 Graph dictionary


| Graph | Gradient     | Area under |
| ----- | ------------ | ---------- |
| `s–t` | velocity     | —          |
| `v–t` | acceleration | `Δs`       |
| `a–t` | —            | `Δv`       |


Displacement curves must be **smooth** (no kinks) when velocity is continuous.

### 4.3 SUVAT (straight line, **constant** `a` only)

```text
v  = u + at
s  = ½(u + v)t
s  = ut + ½at²
v² = u² + 2as
```

Define the positive direction **before** substituting. Reject unphysical roots (negative time, etc.).

### 4.4 Momentum & Newton


| Term                | Wording                                                                                |
| ------------------- | -------------------------------------------------------------------------------------- |
| **Inertia**         | Reluctance to change motion                                                            |
| **Mass**            | Measure of inertia                                                                     |
| **Linear momentum** | `p = mv`                                                                               |
| **N1**              | Remains at rest or uniform straight-line motion unless a resultant external force acts |
| **N2**              | Rate of change of momentum ∝ resultant force, same direction: `F = dp/dt`              |
| **N3**              | If A exerts a force on B, B exerts an equal and opposite force on A                    |
| **1 N**             | Force that gives 1 kg an acceleration of 1 m s⁻²                                       |


**Action–reaction criteria:** same type of force; act on **different** bodies (so they do not cancel).

`N` and `W` on a standing person are **not** an N3 pair (same body; different force types).

### 4.5 Dynamics toolkit

```text
Constant mass:     F_net = ma
Mass flow / thrust: F = (dm/dt) Δv     (e.g. rocket / jet: ρAv²)
```

**Multi-body method**

1. System as a whole → eliminate internal forces → find `a`.
2. Isolate one body → find coupling force / tension.
3. Negative coupling force ⇒ compression (pushed together), not tension.

### 4.6 Lecture-note pointers

- Graph sets: LN §3.1
- SUVAT from `v–t`: LN §3.2
- N2 cases + thrust: LN §3.4
- Action–reaction vs N/W: LN Fig. 3.5–3.6

---

## 5. Chapter 4 — Energy & Fields

> Tutorial 4 is titled "Fields and Energy" but the **discussion questions are almost entirely mechanical energy/power**. Field depth for gravity sits in Ch 8; electric fields return in Ch 14.

### 5.1 Definitions


| Term                             | Wording                                                                                     |
| -------------------------------- | ------------------------------------------------------------------------------------------- |
| **Work (constant force)**        | Product of the force and the displacement **in the direction of the force**: `W = Fs cos θ` |
| **1 J**                          | Work done by 1 N through 1 m in the direction of the force                                  |
| **Field**                        | Region of space where an object with the right property experiences a force                 |
| **Gravitational field strength** | Gravitational force per unit mass: `g = F_G / m`                                            |
| **Electric field strength**      | Electric force per unit positive charge: `E = F_E / q`                                      |
| **Work by field ↔ PE**           | `W_field = −ΔU`                                                                             |
| **Conservation of energy**       | Energy cannot be created or destroyed; only transferred or transformed                      |
| **Power**                        | Rate of work done / energy transfer: `P = dW/dt`                                            |
| **Efficiency**                   | `η = (useful output / total input) × 100%`                                                  |


### 5.2 Core formulae

```text
Variable force (F ‖ s):   W = ∫ F ds = area under F–s graph
Kinetic energy:           E_K = ½ mv²
Hookean spring:           U_E = ½ kx² = ½ Fx     (within proportionality limit)
Uniform g near Earth:     ΔU = mg Δh             (zero of U is arbitrary)
Force from PE:            F = − dU/ds
Power (F ‖ v):            P = Fv
```

Beyond the proportionality limit: use **area under the F–x graph**, not blindly `½kx²`.

### 5.3 Energy bookkeeping

- Isolated: `E_i = E_f`
- Closed with external work: `E_i + W_ext = E_f` (`W` into system positive)
- Identify the **useful** output carefully for efficiency (ΔKE of vehicle? GPE of water?).
- `kWh` is **energy**, not power.

### 5.4 Lecture-note pointers

- Energy stores / pathways: LN §1.3
- Work sign & F–s area: LN §1.4
- KE derivation: LN §1.5
- Elastic PE: LN §1.6
- Fields intro + GPE: LN §1.7–1.8
- Power & efficiency: LN §1.11

---

## 6. Chapter 5 — Projectile Motion

### 6.1 Model (no air resistance)

```text
a_x = 0          a_y = −g   (up positive)
u_x = u cos θ    u_y = u sin θ
s_x = u_x t
s_y = u_y t − ½ g t²
v_x = u_x
v_y = u_y − g t
```

Horizontal and vertical motions are **independent**. Trajectory is a parabola:

```text
s_y = s_x tan θ − (g s_x²)/(2 u² cos² θ)
```

Level ground range / flight (derive once, then use):

```text
T = 2 u sin θ / g
R = u² sin 2θ / g          →  R_max at θ = 45°
```

Landing below / above launch: do **not** use the level-ground formulae. Solve the quadratic for `t` with the correct `s_y`.

### 6.2 Air resistance (qualitative — examinable)


| Feature           | Without drag       | With drag                          |
| ----------------- | ------------------ | ---------------------------------- |
| Trajectory        | Symmetric parabola | Asymmetric; shorter height & range |
| `a` on way up     | `g` down           | `a_up = g + F_air/m > g`           |
| At apex           | `a = g`            | Still `a = g` (v = 0 ⇒ drag = 0)   |
| `a` on way down   | `g`                | `a_down = g − F_air/m < g`         |
| Time up vs down   | Equal (level)      | Time up **shorter** than time down |
| Terminal velocity | —                  | `F_air = W`, `a = 0`, constant v   |


Energy with drag: work against drag → thermal; at terminal velocity, loss of GPE → thermal only.

### 6.3 Lecture-note pointers

- Independence of axes: LN §5.4
- GPE of projectile: LN §5.5
- Full air-resistance FBDs and graphs: LN §5.6
- Parabola proof: LN Appendix §5.7

---

## 7. Chapter 6 — Collisions

### 7.1 Impulse & momentum

```text
impulse = ⟨F_net⟩ Δt = ∫ F dt = Δp
```

Same `Δp`, larger `Δt` ⇒ smaller average force (seatbelts, crumple zones, airbags).

### 7.2 Definitions


| Term                              | Wording                                                                                                   |
| --------------------------------- | --------------------------------------------------------------------------------------------------------- |
| **Conservation of momentum**      | When bodies in a system interact, total momentum remains constant **provided no net external force acts** |
| **Closed system**                 | No resultant external force                                                                               |
| **Elastic (perfectly)**           | Momentum **and** total KE conserved (before vs after)                                                     |
| **Inelastic**                     | Momentum conserved; total KE **decreases**                                                                |
| **Completely inelastic**          | Bodies coalesce; common final velocity; maximum KE loss for given masses                                  |
| **Relative speeds (1-D elastic)** | Relative speed of approach = relative speed of separation: `u₁ − u₂ = v₂ − v₁` (signed)                   |


Coefficient of restitution: **not required**.

### 7.3 Decision table


| Collision type       | Equations to use                                        |
| -------------------- | ------------------------------------------------------- |
| Elastic 1-D          | COM + relative-speed rule **or** COM + KE               |
| Inelastic            | COM only (+ energy if asked how much KE lost)           |
| Completely inelastic | COM + `v₁ = v₂`                                         |
| Explosion / recoil   | COM (explosive impulse ≫ external impulses during `Δt`) |


Equal-mass head-on elastic, target at rest: **velocities exchange**.

Appendix special cases (useful shortcuts):

```text
m₁ ≪ m₂, u₂ = 0  →  v₁ ≈ −u₁,  v₂ ≈ 0
m₁ ≫ m₂, u₂ = 0  →  v₁ ≈  u₁,  v₂ ≈ 2u₁
```

### 7.4 Lecture-note pointers

- Impulse = area under F–t: LN §6.1
- COM from N3: LN §6.3
- Relative-speed derivation: LN Appendix §6.5
- Super-elastic / recoil / explosion: LN §6.4

---

## 8. Chapter 7 — Circular Motion

### 8.1 Definitions


| Term                     | Wording                                                                                             |
| ------------------------ | --------------------------------------------------------------------------------------------------- |
| **Period** `T`           | Time for one complete revolution                                                                    |
| **Frequency** `f`        | Number of revolutions per unit time; `f = 1/T`                                                      |
| **Radian**               | Angle subtended by arc length equal to the radius; `θ = s/r`                                        |
| **Angular velocity** `ω` | Rate of change of angular displacement: `ω = dθ/dt`                                                 |
| **Centripetal force**    | Radial component of the **resultant** force toward the centre — **not** a separate force on the FBD |


### 8.2 Kinematics & dynamics

```text
v = r ω
ω = 2π / T = 2π f
a = v²/r = ω² r = v ω          (toward centre)
F = m v²/r = m ω² r            (toward centre)
```

SUVAT does **not** apply to UCM (acceleration direction keeps changing). Work by pure centripetal force is **zero** (F ⊥ ds) ⇒ speed constant in UCM.

If the centripetal force is removed, the body leaves **tangentially**.

### 8.3 Standard setups


| Setup                                 | Key relations                                                        |
| ------------------------------------- | -------------------------------------------------------------------- |
| Ball on string, smooth table          | `T = mv²/r`, `N = mg`                                                |
| Conical pendulum                      | `T sin θ = mv²/r`, `T cos θ = mg` → `tan θ = v²/(rg)`, `r = L sin θ` |
| Banked road (ideal, no friction)      | `tan θ = v²/(rg)`                                                    |
| Flat bend                             | Friction supplies `mv²/r`; skid if demand > max friction             |
| Vertical circle (string/rod)          | Bottom: `T − mg` or `T + …` carefully; top often critical            |
| Loop-the-loop, just in contact at top | `N = 0` ⇒ `v_top = √(rg)`; then energy ⇒ `v_bottom,min = √(5gr)`     |


**Banked with friction:** `v > v_ideal` ⇒ friction **down** the bank; `v < v_ideal` ⇒ friction **up**.

**Vertical free motion** is usually **non-uniform**: tangential component of weight changes speed. Contact is lost first at the **top**.

### 8.4 Lecture-note pointers

- `a = v²/r` derivation: LN §7.3
- Horizontal examples (conical, bank, aircraft): LN §7.5
- Vertical / loop critical speeds: LN §7.6

---

## 9. Chapter 8 — Gravitational Fields

### 9.1 Definitions


| Term                                   | Wording                                                                                                 |
| -------------------------------------- | ------------------------------------------------------------------------------------------------------- |
| **Newton’s law of gravitation**        | Two point masses attract with a force ∝ product of masses and ∝ 1/(distance)²                           |
| **Gravitational field**                | Region where a mass experiences a gravitational force                                                   |
| **Gravitational field strength** `g`   | Force per unit mass at a point: `g = F/m`                                                               |
| **Gravitational potential energy** `U` | Work done by an **external** force bringing the mass from infinity to that point                        |
| **Gravitational potential** `φ`        | Work done **per unit mass** by an external force bringing a small test mass from infinity to that point |
| **Escape speed**                       | Minimum speed to escape to infinity (just reach infinity with zero speed)                               |
| **Geostationary satellite**            | Remains fixed in the sky as viewed from Earth                                                           |


Geostationary conditions: period = 24 h; west→east; equatorial plane.

### 9.2 Formulae (signs matter)

```text
F = GMm / r²                         (magnitude; always attractive)
g = GM / r²                          (toward M)
U = − GMm / r                        (infinity = 0; always negative for bound pairs)
φ = − GM / r
F = − dU/dr                          g = − dφ/dr
Near Earth, h ≪ R_E:  ΔU ≈ mgh
v_escape = √(2GM/R)
Orbit:  GMm/r² = mv²/r  ⇒  v = √(GM/r)
T² = (4π² / GM) r³                   (Kepler III)
Satellite:  E_K = GMm/(2r)
            E_P = −GMm/r
            E_T = −GMm/(2r)          (bound ⇒ E_T < 0)
```

**Non-negotiable:** negative signs on `U` and `φ` are **not** direction markers and **must not be omitted**.

Between two masses: `φ` adds as a **scalar**; `g` adds as a **vector**. Neutral point: `g = 0` = turning point of `φ–r`.

### 9.3 Graphs to recognise

- `g–r` for solid sphere: linear inside, `1/r²` outside
- `φ–r`: rises toward 0 as `r → ∞`; more negative nearer the mass
- Equipotentials denser where `|g|` is larger
- `φ–r` and `g–r` between two masses (Fig. 8.8 in LN)

### 9.4 Lecture-note pointers

- Definitions & `g = GM/r²`: LN §8.1–8.2
- `U`, `φ`, gradient relations: LN §8.3 (full ∫ derivation of `U` **not required**)
- Two-mass graphs: LN §8.4
- Escape: LN §8.5
- Apparent weight / equator: LN §8.6
- Orbits, energies, GEO: LN §8.7

---

## 10. Cross-topic links & common traps

### 10.1 Links that papers exploit


| From                       | Into                                                    |
| -------------------------- | ------------------------------------------------------- |
| Ch 1 vectors / uncertainty | Every later numeric & practical                         |
| Ch 2 moments / FBD         | Ch 3 multi-body, Ch 7 banking/lean                      |
| Ch 3 N2 + `F = dp/dt`      | Ch 6 impulse, Ch 7 centripetal, rockets                 |
| Ch 4 energy                | Ch 5 projectiles, Ch 6 KE loss, Ch 7 loops, Ch 8 orbits |
| Ch 5 independence of axes  | Ch 7 vertical circle components                         |
| Ch 6 COM                   | Nuclear α recoil (Ch 20), explosions                    |
| Ch 7 `v²/r`                | Ch 8 orbital speed / Kepler                             |


### 10.2 Trap list

1. Homogeneous equation ≠ correct equation.
2. Accuracy ≠ precision; averaging kills random, not systematic.
3. Moments: use **perpendicular** distance to the **line of action**.
4. `N` and `W` are not an N3 pair.
5. SUVAT only for **straight-line constant a** — never UCM.
6. Sign convention forgotten in projectiles / vertical throws.
7. Level-ground range formula used when landing height ≠ 0.
8. Drawing "centripetal force" as an extra arrow on the FBD.
9. Omitting the minus in `U = −GMm/r` or `φ = −GM/r`.
10. Mixing elastic PE zero (natural length) with a convenient GPE zero carelessly.
11. Using `½kx²` past the limit of proportionality.
12. Applying COM when a significant external force acts in that direction for a long time.

---

## 11. Phase 1 tutorial triage (Ch 1–5)

**Ratings**


| Tag       | Meaning                                             | Action                           |
| --------- | --------------------------------------------------- | -------------------------------- |
| **MUST**  | High exam yield or unique technique                 | Do fully, check against solution |
| **HIGH**  | Common paper skill; worth one clean pass            | Do, or re-do if rusty            |
| **MED**   | Useful once; diminishing returns if you already can | Skim method; spot-check answer   |
| **SKIP*** | Low incremental value for a time-crunched Phase 1   | Read solution in ≤2 min; move on |


SKIP means "don't invest problem-solving time now", not "never look". Definitions you cannot recite still need a 30-second glance.

---

### Chapter 1 — Quantities & Measurement (D1–D10, C1)


| Q   | Value | Why / what to extract                                    |
| --- | ----- | -------------------------------------------------------- |
| D1  | MED   | Base-unit isolation drill                                |
| D2  | HIGH  | Pressure/density units + fractional powers — standard    |
| D3  | HIGH  | Dimensional analysis + "**k cannot be found**" line      |
| D4  | MUST  | Least s.f. vs formal uncertainty; add/multiply rules     |
| D5  | SKIP  | Fermi estimates — fun, rare as full marks                |
| D6  | MUST  | Propagate `g = 4π²L/T²`; rearrange first                 |
| D7  | MUST  | Free-fall `g` + % unc. + systematic timing error         |
| D8  | MED   | 1-D `Δv` with signs                                      |
| D9  | MUST  | Vector `Δv` (cosine/sine rule) + obtuse-angle check      |
| D10 | HIGH  | Resolve 3 coplanar forces → resultant                    |
| C1  | SKIP  | Alternate unit systems / metrology — low paper frequency |


**Ch 1 time budget:** ~40% on D4, D6, D7, D9. Skim D5, C1.

---

### Chapter 2 — Forces & Moments (D1–D7, C1–C3)


| Q   | Value | Why / what to extract                                         |
| --- | ----- | ------------------------------------------------------------- |
| D1  | MED   | Upthrust vs weight lines of action (stability idea)           |
| D2  | HIGH  | Two-rope equilibrium; `tan θ` from dividing equations         |
| D3  | MUST  | Incline friction + normals by moments + **toppling** geometry |
| D4  | MUST  | Beam: moments about hinge → T → hinge resultant               |
| D5  | HIGH  | Tension argument along plank + moments + Hooke + resultant    |
| D6  | HIGH  | Composite CG; cutting at CG ≠ equal masses                    |
| D7  | MUST  | Inclined rod: resolve weight for moments + friction direction |
| C1  | MED   | Pin-jointed frame tension/compression (node method)           |
| C2  | MED   | Sphere wedged in inclines                                     |
| C3  | SKIP  | Harmonic overhang series / spreadsheet — olympiad flavour     |


**Ch 2 time budget:** D3, D4, D7 are non-negotiable. C3 is a time sink — skip.

---

### Chapter 3 — Motion & Forces (D1–D12, C1–C2)


| Q   | Value | Why / what to extract                                      |
| --- | ----- | ---------------------------------------------------------- |
| D1  | HIGH  | Consistent `s–t / v–t / a–t` sketches                      |
| D2  | MED   | Catch-up quadratic; reject negative root                   |
| D3  | HIGH  | Reaction delay + braking distance (two-stage)              |
| D4  | HIGH  | Upward release then fall; signed displacement              |
| D5  | HIGH  | Timing experiment for plate length + systematic errors     |
| D6  | MUST  | Linearise free-fall data (`t²` vs `s`, logs)               |
| D7  | HIGH  | Plumbline in accelerating frames (+ circular foreshadow)   |
| D8  | MUST  | Parachutist: system vs man → eliminate T                   |
| D9  | MUST  | Coupled vehicles: system → isolate → compression sign      |
| D10 | MUST  | Painter/crate: subtract N2L equations                      |
| D11 | HIGH  | Conceptual force scenarios (scale, mirror, bug, Atwood)    |
| D12 | MUST  | Thrust via `ρAv²` — feeds rockets / Ch 6 thinking          |
| C1  | HIGH  | Block on accelerating block (friction provides `a`)        |
| C2  | SKIP* | Wedge–block constraint derivation — heavy; Phase 2 if time |


Do C2 only if multi-body N2L already feels easy; otherwise defer.

**Ch 3 time budget:** D8–D10, D12 first. D1/D6 for graph/practical. Defer C2.

---

### Chapter 4 — Energy & Fields (D1–D10, C1–C2)


| Q   | Value | Why / what to extract                                                                                             |
| --- | ----- | ----------------------------------------------------------------------------------------------------------------- |
| D1  | SKIP  | Energy-store narrative language — read once                                                                       |
| D2  | MUST  | Work from F–x area → reconstruct E_K–x graph                                                                      |
| D3  | HIGH  | Spring → collision → pendulum; **needs Ch 6 elastic result** — do after a Ch 6 skim, or treat ball speed as given |
| D4  | HIGH  | Vertical spring: careful GPE zero                                                                                 |
| D5  | HIGH  | Connected trolley + falling mass, shared `v`                                                                      |
| D6  | MED   | Constant-speed tow; `P = Fv`                                                                                      |
| D7  | MUST  | Power on gradient — dual method (force route vs power route)                                                      |
| D8  | MUST  | Same as D7 with unit conversion trap (km h⁻¹)                                                                     |
| D9  | MED   | Waterwheel GPE / average power                                                                                    |
| D10 | HIGH  | Wind turbine: derive `½ ρ A v³` then blade length                                                                 |
| C1  | SKIP* | Variable-direction tension integral — calculus-heavy                                                              |
| C2  | SKIP* | `f = kv²` → cubic in `λ` — algebra contest, low frequency                                                         |


**Ch 4 time budget:** D2, D7, D8 essential. D10 if power questions worry you. Skip C1–C2 in Phase 1.

---

### Chapter 5 — Projectile Motion (D1–D8, C1–C2)


| Q   | Value | Why / what to extract                                              |
| --- | ----- | ------------------------------------------------------------------ |
| D1  | MUST  | Derive `T`, `t_H`, `R`; prove `θ = 45°` for max range              |
| D2  | MUST  | Landing below launch; **sign of** `v_y` for time                   |
| D3  | HIGH  | Aircraft bomb: choose downward +ve carefully                       |
| D4  | MUST  | Vertical throw with drag `kv`: `a > g`, a–t sketch, time asymmetry |
| D5  | HIGH  | Lunar data set: constant `v_x`, find g, energy, trajectories       |
| D6  | HIGH  | Skydiver v–t regions → a–t sketch                                  |
| D7  | MUST  | Qualitative `v_x`, `v_y` with vs without air resistance            |
| D8  | HIGH  | Gradient of v–t → `a`; test `F ∝ v` with ratios                    |
| C1  | MED   | Relative-velocity bombing — clever but niche                       |
| C2  | SKIP* | Inclined-plane optimum angle proof — defer to Phase 2              |


**Ch 5 time budget:** D1, D2, D4, D7 first (these feed exam explanations). D5/D8 for data skills. Skip C2 now.

---

### Phase 1 recommended order (tight timetable)

```text
Day block A — foundations
  Ch1: D4, D6, D7, D9
  Ch2: D3, D4, D7  (+ D2, D6 if statics shaky)

Day block B — dynamics
  Ch3: D1, D6, D8, D9, D10, D12  (+ D3, D4, D11)

Day block C — energy & projectiles
  Ch4: D2, D4, D5, D7, D8  (+ D10)
  Ch5: D1, D2, D4, D6, D7  (+ D5, D8)

Then move to Ch 6–8. Revisit SKIP items only if a past paper exposes a hole.
```

**Rough cut:** of ~57 main D/C questions in Ch 1–5, Phase 1 should fully work ~25–30 **MUST/HIGH** items and skim the rest. That is the intentional trade for Ch 6–8 depth.

---

## 12. Lecture notes map


| Chapter | File                                                             | Priority sections          |
| ------- | ---------------------------------------------------------------- | -------------------------- |
| 1       | `lect notes/Chap 1 Quantities and Measurement Lecture Notes.pdf` | §1.6–1.9                   |
| 2       | `lect notes/Chap 2 Forces and Moments Lecture Notes.pdf`         | §2.2–2.3                   |
| 3       | `lect notes/Chap 3 Motion and Forces Lecture Notes.pdf`          | §3.1–3.2, §3.4             |
| 4       | `lect notes/Chap 4 Energy and Fields Lecture Notes.pdf`          | §1.4–1.6, §1.8, §1.10–1.11 |
| 5       | `lect notes/Chap 5 Projectile Motion Lecture Notes.pdf`          | §5.4, §5.6                 |
| 6       | `lect notes/Chap 6 Collisions Lecture Notes.pdf`                 | §6.1, §6.3, Appendix       |
| 7       | `lect notes/Chap 7 Circular Motion Lecture Notes.pdf`            | §7.3, §7.5–7.6             |
| 8       | `lect notes/Chap 8 Gravitational Fields Lecture Notes.pdf`       | §8.2–8.3, §8.5, §8.7       |


Tutorial solutions live in `tut soln/Chap N … Tutorial Solutions.pdf`.

---

*Phase 1 focus: §§2–6 + §11. Phase 2: dig §§7–9 with full tutorial work on Ch 6–8.*