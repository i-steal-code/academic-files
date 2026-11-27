# Computing agent

## Primary function

**Bookkeeper** for H2 computing. Both papers are over (P2 practical 2026-10-07, P1 theory 2026-11-11), and the subject was archived on 2026-11-11 at Debig's request. This role keeps the computing library record accurate. It does not run practice or build new study material.

**In scope:** filing a new computing document into `raw files/H2 computing/**` by the `README.md` naming rules; re-running the existing converter for it; keeping the README computing inventory in step; answering from the frozen tree under `raw files/H2 computing/**` and `computing practical/`; refusing new blurts, papers, marking or practicals unless the user explicitly reopens computing.

**Out of scope:** Active practice of any kind; new tools or changes to library-wide conventions (ask the user); other subjects.

## Rules & habits

- **Archived 2026-11-11.** Read `raw files/H2 computing/ARCHIVED.md` and this file first. Default reply to practice requests: computing is closed; reopen only if the user explicitly asks. Do not delete or reorganise the frozen tree.
- Read this file at session start; append decisions under `## Session log` before the chat dies.
- Prefer converted package `content.md` for a **named** paper when text search helps; open `resource files/` and raw PDF when the task is a practical or fidelity matters.
- Do not ingest wholesale: `restaurants.json`, large Route/Stop CSVs, WAREHOUSE dumps — open the fixture the current question needs only (see root `AGENTS.md` / `.claudeignore`).
- Keep practical working copies under `computing practical/` aligned with the canonical package under `raw files/H2 computing/` when both exist; say which tree you edited.
- Chat is disposable; permanent computing conventions and progress live here.
- Plan by finished goals per day, never hours (Debig's rule).

## Patterns

- Layout (from library README): S1–S4 under `base syllabus/`; TYS/prelim P1 as PDF; P2 as package folder + `resource files/`; other schools under `Past Exam Papers from Other Schools/`; timed practice under `misc/`; imports under `origin/`.
- Blurt / readiness: `raw files/H2 computing/blurt sheets/`.

## Session log

### 2026-11-17 — Role becomes bookkeeper

- **Decided:** Library-wide: every role is a bookkeeper for its field. Computing role may file new computing documents and run the converter; still no practice. Focus-lock rule removed (P3 over). The garbled 2025 P1 package noted below was fixed on 2026-11-10 (hand-transcribed). Build role is now private (gitignored); older entries that mention it are history.
- **Next:** None unless the user reopens computing.

### 2026-11-01 — Role file established

- **Decided:** Computing agent owns all computing content jurisdiction; infrastructure changes go to `agents/build.md`.
- **Touched:** `agents/computing.md` (created).
- **Next:** First content session should log current prelim/practical focus and any naming fixes under this log.

### 2026-11-07 — Final theory run-in

- **Decided:** Remaining paper is theory, Wed 11 Nov. P2 practical is done (Debig: went very well, similar to the 2025 timed sit). RI prelim P1 on 15 Sep scored 68/100; main losses were the BST question and the ethics question. No theory touched since. Prelim paper is not in the repo.
- **Decided:** Plan by goals, not hours, brokered with physics via Jarvis. Final plan below supersedes the earlier topic order.
- **Gap found:** `RI prelim 2026 P1 readiness.md` has no ethics item. Source: S3G chapter section 6 and its A-level questions (2023 Q8, 2025 Q7, SP Q7).
- **Touched:** `agents/computing.md`.
- **Context:** The 68/100 predates the practical bootcamp (about 12 days before the 7 Oct paper, triggered by 25/100 on the prelim practical), so it understates current ADT, OOP and SQL knowledge. Do not treat it as today's level.
- **Decided:** Tonight is diagnose then JIT: blurt each topic, teach only what fails. Bootcamp-covered topics get a written-explanation check. Theory-only topics (ethics, PDPA, NoSQL reasons, networks, decision tables, validation, Big-O reasoning) are where JIT teaching is expected.
- **Final plan (Debig approved, relayed by Jarvis):**
  - Sat 7, night: diagnose first, teach only what fails. Ethics, networks and database theory (PDPA, NoSQL reasons) finished. Overflow to Tue: BST with ADT and recursion, OOP, SQL, as quick written checks.
  - Sun 8: none.
  - Mon 9: worst gap re-blurted cold once.
  - Tue 10: main day. One past paper blurted and marked, every gap re-blurted cold; last block recall only, normal bedtime. If tight, cut the paper to its long-answer questions and keep every re-blurt.
  - Wed 11: computing theory paper.
- **Next:** Record tonight's gap list here.

### 2026-11-10 — Cheatsheet skim (Tue, main day)

- **Source:** Google Doc "H2 computing cheatsheet" (Drive id `1xmA_SngyT9we4VEMKRUbA4NIx6JhwQJwPc9w-T1rS3U`). The text export drops images, so diagram-only parts (BST delete cases, class/ER diagrams, linked-list advantages list) could not be checked.
- **Real gaps (Debig confirmed):** Network security (heading only; DoS, firewall, digital signature, authentication appear in A-level P1 2021–2024) — Debig writing it. Test data section absent. Search and sort definitions — Debig rewriting.
- **Not gaps (images, invisible to the text export):** code of ethics areas table, check digit algorithm, most small gaps. Decision table already says 2^n; the export lost the superscript. Sorts/Big-O and BST detail live in practical notes and memory.
- **Lesson:** a Drive text export of this doc is not a full read; ask which parts are images before calling a section empty.
- **Possibly wrong as written (text-only check):** denary→hex uses remainders; check digit catches transcription/transposition, not missing data; child cannot reach parent private members; quadratic probing offsets are i², not index^n; IPv4 example uses colons and 225.
- **Converted 2025 P1 A-level package is garbled** (vertical OCR text); use the raw PDF. Flag to build agent.
- **Next:** blurt order today: network security → ethics/PDPA → decision table → sorts and BST → DB theory.
- **Done:** Debig wrote the network security section. Claude rewrote the S1B & C search and sort body text (tab `t.0`) from `computing practical/Boilerplates/S&S.ipynb`: linear, insertion, bubble, binary (recursive and iterative), mergesort, quicksort partition and conquer, plus an "Exam terms" paragraph (in-place, stable, divide and conquer). Headings, both images and the "Quicksorts tested…" line untouched. No complexity table added (already an image).
- **Done (Morals):** PDPA section now has the S3G lecture material (purpose, DPO role, 4 obligations as bullets, consequences, exam tip); Debig's original one-liner kept. Social issues plan replaced by a full essay (intro, 5 body paragraphs covering social, civic, digital divide, economic, legal/ethical; conclusion; P1 usage line), written with hub `artefacts/systems/world-model.md` reasoning (conditional claims, mechanism, who pays, binding rules). Facts used: POFMA 2019, SkillsFuture, Platform Workers Act 2024, SingHealth 2018 breach (~1.5M patients, PDPC fines). The only open Morals comment ("fact check and paraphrase; dumped from gemini") is addressed but must be resolved by hand: the connector cannot resolve comments. The "missing iterative binary search" comment (S1B & C) is also addressed.
- **Trace diagram = recursion trace tree, and it is tested:** 2024 A-level P1 Q2(a) [4] (S(n) = S(n-1) - 3, base 12; then features of recursion, stack for S(2), S(0) overflow, iterative rewrite) and 2025 ASRJC prelim [3]. Section written in the cheatsheet under S1A "Trace diagram"; the "this is not even filled out" comment there is addressed (resolve by hand). Flowcharts also appear (2024 Q1(a) [4]) and have no cheatsheet section.
- **Contention sweep (all 17 comments now resolved):** remaining text issues: digital signature says verification is "same process as asymmetric encryption" (wrong: sender's public key verifies); polymorphism example invents a `data_struct` parent of list/set; "an object is a data type"; quadratic probing `index^n`; Unicode "2^32 chars"; 1:1 "removed in 3NF"; no circular-queue full/empty test. Missing: test data, flowchart symbols. Empty: Exam highlights.
- **Sweep fixes done:** Debig fixed digital signature, object definition, quadratic probing and the 1:1 note; polymorphism example stays (deliberate analogy, not a claim about Python). Claude fixed Unicode code-point count, added circular queue full/empty paragraph, and added a Flowchart section (HEADING_3, before S1B & C) from S1A lecture notes. Test data left for Debig: source is S2A Programming Elements chapter section 5 (5.4 test cases, 5.5 test plan).
- **Debig wrote the test data section.** Claude cut "Iteration and recursion" (S2A & B) down to the S2A chapter section 6 content: features, comparison table (memory, speed, stack overflow, debugging, code size, use cases) and call stack/unwinding. This also removed the wrong claim that iteration uses more stack space. Headings kept; about 1,900 characters became about 1,100.
- **Blurt 1, network security (marked against the cheatsheet section).** Strong: malware types, DoS/DDoS, IDS/IPS, encryption keys, the full digital signature process, auth/MFA, firewall limits (b) 3/3. Gaps to re-blurt cold: CIA triad (all three blank); spyware missing; firewall payload filter and its purpose (rule-based monitoring of incoming/outgoing traffic); digital signature guarantees (authenticity, non-repudiation); (a) about 3/4, because it never said that only the company holds its private key, so a match proves the contract came from the company; symmetric key-distribution weakness. Wording fix: firewalls *can't inspect the contents* of encrypted packets; they can still filter them by IP, port and protocol.
- **Blurt 2, ethics/PDPA: weakest topic so far, which matches the prelim loss.** Code of ethics: recalled about 1 of the 8 areas (S3G section 6 table), no professional bodies named. DPO role wrong (said "reports to the committee"; it's the Commission, PDPC, and the DPO oversees compliance). The 4 obligations were not listed (purpose limitation never appeared), and consequences were blank. (a) 2023 Q8 [5]: about 2/5. It had the safety-over-deadline point, but no named area applied (public interest, integrity/disclosure), no other side, and the "overstated competence" argument is misapplied: the fault was *found* in testing. (b) PDPA tuition centre [3]: 3/3 (consent, protection, retention). JIT taught: the 8 areas grouped as self, others and society, plus the 4-step "discuss" structure. Re-blurt cold tonight.
- **Diagnosis across blurts 1–2:** understanding is ahead of labels. Debig can work out obligations or processes from context (PDPA (b) 3/3, digital signature process perfect) but can't recall named lists cold (CIA, the 3 signature guarantees, 4 PDPA obligations, 8 ethics areas). Re-blurts should drill the **names**, one keyword per item.
- **Blurt 3, decision tables:** quadrants, 2^n with derivation, and advantage/disadvantage correct. Full table (a) 3/3. Gaps: limited vs extended entry wrong (it is Y/N/X entries vs free values/statements, not "removes impossible cases"); impossible rules (asterisk, then omitted) and the completeness check missing. Simplification (b) about 1/3: dashes put in action rows, and rules overlap (dash expansion sums to 14, not 8). Taught: each column is one complete rule; merge only columns with identical actions that differ in one condition; check by counting 2^(dashes) per column = 2^n.
- **Blurt 4, sorts/BST:** sort mechanics, complexities, stability and in-place all solid; BST property, insert, search, traversal definitions and O(log n)/O(n) solid. Gaps: **BST delete cases wrong** (believed the root is a special case and that with 2 children the right child moves up; correct is leaf / one child (child replaces it) / two children (in-order successor = min of right subtree, or predecessor, replaces the value, then that node is removed). Debig spotted the contradiction himself in (c)). **Traversal execution:** pre-order put 35 before 40, and post-order was wrong (started with root 50) even though the definitions were right. Binary search recursive space is O(log n) stack frames holding bounds, not copied sub-arrays. Quicksort needs O(log n) avg / O(n) worst recursion stack, not "no extra memory"; the worst-case pivot is the smallest/largest *value*, not the first/last *position*. Exam: (a) 3/3, (b) about 0/2, (c) correct result, case unnamed, (d) 2/2.
- **Blurt 5, DB theory:** keys, 1:1/1:M, 2NF/3NF purpose and SQL-vs-NoSQL reasoning fine; 3NF decomposition (b) **4/4**. Gaps: partial and transitive definitions **swapped**, so (a) 0/2 even though the decomposition was right (same pattern: understanding ahead of labels); 1NF described as "unique records" instead of atomic cells; M:M junction table not stated; NoSQL types (only document recalled); referencing blank; ACID (only atomicity). (c) NoSQL correct; the stronger phrase is "flexible schema: each document can have its own fields".
- **Ran past midnight into exam day,** so the past paper was dropped to protect sleep (the plan cuts the paper before the re-blurts). All gaps went into `raw files/H2 computing/blurt sheets/A-level P1 final re-blurt.md` (prompts, then answers) for one cold pass on the morning of 11 Nov.
- **Paper is in the afternoon (Debig, 11 Nov).** The morning now has these goals: (1) one cold pass of the re-blurt sheet; (2) the long-answer questions of one unseen P1, blurted and marked, with Claude setting the paper when Debig checks in; (3) the last block before leaving is recall only, with no new material. Sleep first.
- **Code of ethics memory hook (Debig's request, 11 Nov):** added under the ethics image in Morals → Code of ethics: an intro line plus 8 bullets, one Facebook/Zuckerberg case per area (bold area name, then the story, then the rule), ordered self, others, society. Cases: Winklevoss (settled, framed as an accusation), "move fast and break things", 2019 FTC $5B, the 2012 emotional-contagion feed experiment, Cambridge Analytica (up to 87M), Facemash (Harvard board charges), Haugen 2021, the 2018 UN Myanmar report. Mostly company actions under him as CEO; the doc says so.
- **Morning re-blurt (11 Nov):** fixed: signature guarantees, 5 malware types, PDPA obligation names, BST delete (in-order successor), partial/transitive concept, referencing, ACID, limited vs extended entry. Still missing (failed twice): CIA integrity, firewall payload/definition, 3 ethics areas (Professional Conduct, Confidentiality & Privacy, CPD) and the bodies, "discuss" other side + judgement, impossible rules, traversal execution (falls back to in-order on lower subtrees), dependency arrow notation, 1NF definition, M:M junction table, wide-column. These are added at the top of the re-blurt sheet as the last-block list. Next: OOP label sweep, then long-answer questions from an unseen P1.
- **OOP label sweep (11 Nov):** solid on class/object/instantiation, constructor, inheritance, overloading vs overriding, class diagram boxes and +/-. Fixes: encapsulation = *bundling* attributes and methods + restricting direct access, and its benefit is protecting data from invalid/accidental change (validation in setters), not "stopping bad actors"; polymorphism needs "same method call, different behaviour depending on the object's class"; inheritance arrow has a hollow triangle head at the parent. Abstraction is not in the S2 notes, so skip it. Next: long-answer questions from one unseen P1; asked Debig which papers are unseen.
- **Pre-exam gap review (11 Nov, paper 2pm):** Debig is solving the A-level P1s on his own from here. The OOP fixes were added to the last-block list. Never tested this run-in: ADTs theory (hash collisions, linked list pros/cons, stack/queue uses), validation/verification checks, networks/web (protocols, client-server, HTTP/S), data representation and check digits, data protection methods and VCS, SQL statements. The papers act as the test for these.
- **Open in network security (now fixed by Debig):** the digital signature text never says which key: sender encrypts the digest with the sender's private key, and the receiver decrypts with the sender's public key. That pairing is the mark point.

### 2026-11-11 — P1 done; archive and pack up

- **Outcome:** P1 theory sat on 11 Nov at 2pm. Debig: it went well, and the difficulty was as expected from solving the 2024 and 2025 A-level P1s. P2 practical (7 Oct) had also gone well.
- **Decided:** Debig asked to archive computing for good. Frozen in place with no tree move, following the GP precedent. Added `raw files/H2 computing/ARCHIVED.md`. This role is now archive steward only. Root `AGENTS.md`, `agents/README.md` and `README.md` now mark computing as archived, and computing blurt sheets are no longer open by default.
- **Touched:** `raw files/H2 computing/ARCHIVED.md`, `agents/computing.md`, `AGENTS.md`, `agents/README.md`, `README.md`.
- **Next:** None unless the user explicitly reopens computing. Point Debig to physics (P3 on 17 Nov).
