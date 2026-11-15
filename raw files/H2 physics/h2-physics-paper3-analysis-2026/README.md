# H2 Physics (9478) Paper 3 analysis, November 2026

A data pack for the 2026 A-level H2 Physics Paper 3: what is likely to come up, given what Paper 2 tested, and what each topic usually asks. It is analysis only: it has no question lists and no exam questions.

## Files

- `paper3-analysis.md`: the full report (method, Paper 2 as sat, topic outlook, Section B, mechanics, patterns, what is robust, effort rule, question types inside each topic).
- `paper3-analysis.json`: every number in one file, for scripts and AI workflows. Key fields:
  - `topics[]`: per topic `headline` (the rounded, checked bands) and `computed` (the raw counts and chances behind them).
  - `section_b`: lead chances, the most likely pair, coverage, the A-level history.
  - `within_topic_question_types`: per topic, every 9478 question type with its share over all sources (`share`), the share after removing what the 2026 Paper 2 tested (`share_2026_paper3_view`), marks and shares per source, and flags.
  - `paper2_2026`, `mechanics`, `structure_and_patterns`, `robust_and_fragile`, `effort_rule`, `method`.
  - `raw.pairs`: per sitting (A-level 2016-2025, 16 schools 2026), marks per topic in Paper 2 and Paper 3, to recompute any chance.
- `topics.csv`, `question-types.csv`, `section-b-history.csv`, `pairs.csv`: the same data as flat tables.

## Definitions

- Topic codes: MEAS = Measurement, FORCES = Forces and moments (equilibrium, Hooke's law), MOTION = Kinematics, Newton's laws, momentum and mass flow, ENERGY = Work, energy and power, PROJ = Projectile motion (with air resistance), COLL = Collisions and impulse, CIRC = Circular motion, GRAV = Gravitational fields, OSC = Oscillations, WAVEM = Wave motion, SUPER = Superposition, THERM = Thermal physics (ideal gases and thermodynamics), EFLD = Electric fields (with capacitance), CURR = Currents (with a.c.), CIRCUITS = D.c. circuits (with capacitors and RC), EMFOR = Electromagnetic forces, EMIND = Electromagnetic induction, QUANT = Quantum physics, NUCL = Nuclear physics; MECH = the one general mechanics question.
- "In Paper 3 at all": 4 or more marks on the topic anywhere in Paper 3.
- "Whole Section A question": the topic leads (has the most marks in) a Section A question of 5 or more marks. The headline band runs from a stricter independent count (`whole_section_a_question_checker_strict`) up to this one (`whole_section_a_question_lead_rule`).
- "Leads a Section B option": the topic leads an option and has 8 or more of its 20 marks.
- Chances are conditioned on the topic's 2026 Paper 2 status and blend A-level (0.6) with the 2026 school pairs (0.4).

## Read this before you use it

- Papers 2 and 3 are one pool. Judge how common a topic is over both papers; do not argue "rare in Paper 3" for a topic that may just have sat in Paper 2.
- Use the `headline` bands for decisions; they take in the checks. The `computed` values are the raw inputs.
- The fragile parts are listed in `robust_and_fragile`: mainly mechanics, thermal, currents and the exact Section B pair.
- 2026 is the first 9478 sitting; the A-level years are the 9749 syllabus (2016: 9646). New 9478 content (capacitors and RC, capacitance, wavefunctions) is weighted from the 2026 school papers.
- Version 2026-11-13, made after Paper 2.
