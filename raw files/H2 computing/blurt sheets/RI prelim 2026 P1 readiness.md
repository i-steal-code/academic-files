# RI Computing Prelim 2026 — Paper 1 readiness sheet
# theory taper · memory / understanding · not code drills
# method: blurt → re-teach → dialogue → tick only when cold

Paper shape (RI): 3h / 100 / answer all · mega-bundled DB opener · decision tables · OOP diagram · ADT Big-O pick · recursion+stack · applied networks · PDPA on the scenario

How to use this sheet
- Each line is a must-have skill. Tick only when you can do it without notes.
- Primary modes: blurting (blank page), re-teaching (out loud / to someone), dialogue (Q&A, "why not X?").
- Do not open the next gate until the current gate's pass line is true.
- Code/practice is optional polish only after Gate 4 — this paper rewards explanation craft.

Taper rule
- Early gates = bankable RI marks.
- Later gates = distinction / cascade marks.
- If tired: only re-blurt Gate 1 + Gate 4 stems. Nothing new.

---

## Gate 0 — survival floor
Pass when: no blank section on a past RI paper skim.

### Blurt (blank page)
- [ ] OOP: draw one inheritance diagram (super + 2–3 children + 1 method each)
- [ ] OOP one-liners: encapsulation / inheritance / polymorphism
- [ ] DB: from one messy table → PK, simple ER (1:M and M:N), 3NF table list
- [ ] Recursion: features of recursion + what the call stack holds after 2 calls
- [ ] Networks: client-server OR DNS OR packet-switching (purpose + 1 +/−)

### Re-teach / dialogue
- [ ] Explain to yourself why JOINs do not "undo" 3NF
- [ ] Explain why a recursive call needs a base case (stack / non-termination)
- [ ] Dialogue: "Is polymorphism the same as inheritance?" — answer no, and why

Gate 0 pass: ☐

---

## Gate 1 — RI mega-opener (highest mark density)
Pass when: finish a RI Q1-style opener in ≤25 min, no blank parts.

This is the RI signature: ER + 3NF + SQL + NoSQL + PDPA in one stem.

### Blurt
- [ ] ER: entities, relationships, 1:M and M:N (M:N → bridge table)
- [ ] Table defs: every PK underlined / labelled; every FK named as referencing which table
- [ ] 3NF: spot transitive / partial dependency and fix it in words + tables
- [ ] SQL SELECT + JOIN (parameter idea: never invent column names not in the stem)
- [ ] SQL UPDATE or INSERT (RI likes these more than TYS)
- [ ] SQL aggregate if asked: GROUP BY + HAVING vs WHERE (aggregates → HAVING)
- [ ] NoSQL: 3 scenario-tied reasons (flexible schema / nested docs / scale-out) — not buzzwords
- [ ] PDPA: 2 concrete org actions on the stem's data (collect less / purpose limit / access control / vendor sharing)

### Re-teach / dialogue
- [ ] Re-teach the whole opener as a story: "company has X problem → we model → we query → we justify NoSQL → we protect people"
- [ ] Dialogue: "Why not put everything in one NoSQL document?" — when relational still wins
- [ ] Dialogue: "Does PDPA mean 'don't store personal data'?" — correct the misconception

### RI-specific traps
- [ ] NoSQL reasons must not contradict the ER you just drew
- [ ] PDPA names who does what with which field in the stem
- [ ] Bridge table for M:N is not optional fluff — missing it costs ER + 3NF together

Gate 1 pass: ☐

---

## Gate 2 — easy craft marks (DT / validation / backup)
Pass when: each item ≤8 min, definitions don't wobble.

### Blurt
- [ ] Decision table: full table from rules → simplify (merge rows) → pseudocode if asked
- [ ] Validation vs verification (one clear contrast + one method each)
- [ ] Test data: normal / abnormal / extreme — one example each for a given rule
- [ ] Check digit purpose (detect transcription errors) — Mod-11 / weighted if asked
- [ ] Backup vs archive (purpose contrast + one consequence of no backup)
- [ ] Encoding short block if it appears: ASCII vs Unicode / bin↔hex one conversion

### Re-teach / dialogue
- [ ] Re-teach decision tables using a restaurant/member/discount scenario out loud
- [ ] Dialogue: "Is a check digit the same as data integrity?" — no; integrity is broader
- [ ] Dialogue: "Why keep backups off-site?" — one physical-risk sentence

Gate 2 pass: ☐

---

## Gate 3 — OOP modelling marks
Pass when: diagram + 4 explanations without re-reading notes.

### Blurt
- [ ] From a wordy scenario: identify superclass, subclasses, attributes, methods
- [ ] Instantiation: what an object is vs the class
- [ ] Encapsulation: private data + getters/setters; why hide
- [ ] Inheritance: is-a; what the child reuses / extends
- [ ] Polymorphism: same message, different behaviour; override example on your diagram
- [ ] Optional RI tail: test data for one numeric attribute on a child class

### Re-teach / dialogue
- [ ] Re-teach your diagram as if teaching a classmate who missed the lesson
- [ ] Dialogue: "Composition vs inheritance — when is has-a better?" (one example)
- [ ] Dialogue: "Can a child access parent `__private` directly?" — no; use getters / why

Gate 3 pass: ☐

---

## Gate 4 — S1 understanding marks (harder band)
Pass when: RI-style "pick DS by operation" + one BST/recursion stem without blanking stack.

Prefer blurting structures and trade-offs over writing full code.

### Blurt — ADT selection (RI favourite)
- [ ] Map operations → structure: add / exists / recent / sorted / FIFO
- [ ] List / array: when simple, when slow (search / middle insert)
- [ ] Stack: LIFO use cases (undo, call stack, postfix)
- [ ] Queue: FIFO; linear vs circular — one +/− each
- [ ] Hash: average O(1) search; collision idea; when hash is a bad fit (ordered traversal)
- [ ] BST: ordered search; unbalanced → chain → O(n)
- [ ] Linked list vs array: insert/delete vs random access

### Blurt — recursion / BST / sorts (explain, don't grind)
- [ ] Recursion: base case, self-call on smaller input, progress toward base
- [ ] Call stack: what is pushed/popped; overflow risk for deep/infinite recursion
- [ ] Rewrite idea: iterative ↔ recursive (describe steps; code optional)
- [ ] BST: insert rule; in-order = ascending; pre/post if asked
- [ ] Array BST / free list: only if you already know it — otherwise describe properties in words
- [ ] Merge sort: always O(n log n); needs extra space; stable idea
- [ ] Quick sort: average O(n log n); worst O(n²) on bad pivots / already sorted with bad pivot
- [ ] Insertion sort: good when nearly sorted / small n

### Re-teach / dialogue
- [ ] Re-teach: "Why binary search needs sorted input" and "why hash is not binary search"
- [ ] Dialogue: "For 'get most recent then oldest', why not BST?" → queue/stack reasoning
- [ ] Dialogue: "When does merge beat quick?" → worst-case guarantee / linked structures
- [ ] Dialogue: "Unbalanced BST — what went wrong and what is the cost?"

Gate 4 pass: ☐

---

## Gate 5 — applied networks (scenario-tied)
Pass when: answers fit the stem, not memorised dumps.

### Blurt
- [ ] URL parts you need: protocol, host/domain, path (document path)
- [ ] DNS: domain → IP (resolver path in one short chain)
- [ ] HTTP idea: request (method + path + headers + optional body) → response (page or redirect)
- [ ] Client-server: roles + 1 +/− for the scenario
- [ ] Native vs web app: 2 adv / 2 disadv tied to the stem
- [ ] Packet switching: why packetise; 2–3 header fields; router role
- [ ] MAC vs IP (if RI asks): local hardware id vs network routing address
- [ ] Optional RI extras: static vs dynamic IP; P2P +/−; firewall purpose + 1 limitation

### Re-teach / dialogue
- [ ] Re-teach a full "user types URL → page appears" walkthrough
- [ ] Dialogue: "Does the website run on the client?" — frontend executes in browser; backend on server
- [ ] Dialogue: "Is a switch the same as a router?" — MAC vs IP forwarding one-liner
- [ ] Dialogue: "GET vs POST — where does the form data live?" — URL/query vs body

Gate 5 pass: ☐

---

## Gate 6 — cascade / distinction marks
Pass when: after easy parts, you still finish the last explanation tails cleanly.

### Blurt / dialogue only
- [ ] NoSQL justification that stays consistent with your relational design
- [ ] PDPA paragraph: actor + action + data type + risk reduced
- [ ] Digital signature: create + verify; integrity (and authenticity if asked) — only if the paper asks
- [ ] Auth / MFA / DoS: one solid scenario answer each — depth over coverage
- [ ] Algorithm fault explanation: what goes wrong, why testing missed it, how to fix (words first)
- [ ] "Why this structure fails for operation X" — one crisp complexity sentence

Gate 6 pass: ☐

---

## Taper checklist (use as a daily card)

Only tick a row when blurted cold that day.

### Always-bank (do these every session)
- [ ] Gate 1 mega-opener story (ER → 3NF → SQL → NoSQL → PDPA)
- [ ] Gate 3 OOP diagram + 4 principles
- [ ] Gate 4 ADT picker (4 operations → 4 structures + why)

### Rotate (one per session)
- [ ] Decision table full → simplify
- [ ] Recursion + stack re-teach
- [ ] URL → DNS → HTTP response walkthrough
- [ ] Backup/archive OR validation/verification OR encoding

### Ban list until Gates 1 and 4 are green
- [ ] New niche topics (base-n puzzles, obscure protocol lists)
- [ ] Writing full Python ADT implementations "for confidence"
- [ ] Re-reading notes without blurting
- [ ] Opening HCI short-theory dumps as if they were RI mark layout

---

## Dialogue prompt bank (steal these)

Use with a friend, or alone out loud. Answer in full sentences.

1. Walk me through designing a ride-hail / clinic / warehouse DB from a messy table.
2. Why is M:N a trap, and what table fixes it?
3. Give three NoSQL reasons for this app — then argue when SQL is still better.
4. What must this company do under PDPA for phone numbers and payment data?
5. Draw the class diagram for robots / events / library items and explain polymorphism on it.
6. I need fast existence checks and also "most recent first" — pick structures and defend them.
7. Trace this recursive function and narrate the stack.
8. Why can merge sort's time be trusted more than quicksort's?
9. User enters a URL — narrate DNS, request, server, response (HTML vs redirect).
10. Is frontend "on the client" or "on the server"? Untangle hosting vs rendering.

---

## Past-paper gates (understanding checks, not grind)

Do as oral / written blurts, not timed code.

- [ ] RI 2023 P1 — Q1 DB + Q2 OOP/NoSQL/PDPA + one S1
- [ ] RI 2024 P1 — Q1 insurance mega-stem + DT + OOP events
- [ ] RI 2025 P1 — Q1 ride-hail mega-stem + Q2 ADT picker + Q3 robots OOP

After each: mark which gate failed. Re-blurt only that gate. Do not "do the whole paper again" until that gate is fixed.

---

## Score map (how gates buy marks on RI)

| Gates passed | What you have secured |
|--------------|------------------------|
| 0 only | Can sit the paper; still leak everywhere |
| 0–1 | Bank the mega-opener — RI's biggest single swing |
| 0–3 | Solid mid: opener + craft + OOP |
| 0–4 | Competitive: mid + S1 picker/recursion |
| 0–5 | Strong: networks no longer free marks left behind |
| 0–6 | Top-band explanations on cascade tails |

Target for prelim: **Gates 0–4 green, Gate 5 mostly green.** Gate 6 is polish.

---

## Final night card (no new content)

Blurt only:
1. One mega-opener story
2. One OOP diagram + four principles
3. Four operations → four ADTs
4. URL → page walkthrough
5. PDPA two actions on a made-up stem

Then stop. Sleep beats one more topic.
