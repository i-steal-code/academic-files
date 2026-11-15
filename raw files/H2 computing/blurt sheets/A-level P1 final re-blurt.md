# A-level P1 final re-blurt (11 Nov 2026)

Gaps from the 10 Nov blurts (network security, ethics/PDPA, decision tables, sorts/BST, database theory). Cover the answers, recall each prompt cold, then check. Most gaps are **names of list items**, not understanding: learn one keyword per item.

## Still missing after the morning pass (last recall block: these only)

- **CIA integrity** = no unauthorised *modification* (this is the same word as the signature's "not changed" guarantee).
- **Firewall:** "monitors and controls incoming and outgoing traffic against rules"; 4th filter = **payload**.
- **Ethics areas missed:** Professional Conduct (feed experiment), Confidentiality & Privacy (Cambridge Analytica), CPD (FTC $5B). Bodies: ACM, IEEE, SCS.
- **"Discuss":** you must give the **other side** and a **judgement with its condition**, not just what went wrong.
- **Impossible rules:** mark `*`, then remove the column.
- **Traversals:** the same rule applies at *every* node. Pre `50 30 20 40 35 70 60 80` (40 before its child 35). Post `20 35 40 30 60 80 70 50` (70 after both its children).
- **Dependency notation:** the PK is at the *start* of the arrow. Partial: `B → C` where the key is `(A, B)`. Transitive: `A → B → C` where A is the PK.
- **1NF** = each cell holds **one value**, no repeating groups (not "every record unique").
- **M:M** = a third **junction table** holding both FKs, which turns it into two 1:M.
- **NoSQL types:** key-value, document, **wide-column**, graph.
- **Encapsulation** = *bundling* attributes and methods in one class + restricting direct access; the benefit is protecting data from invalid changes (setters validate), not stopping hackers.
- **Polymorphism** = the same method call behaves differently depending on the object's class (overriding is how).
- **Class diagram:** the inheritance arrow goes from child to parent with a **hollow triangle** head; show types (`- Name : STRING`).

## Prompts

1. CIA: the three, one line each.
2. Digital signature: the 3 guarantees. Which step proves *who sent it*, and which proves *not changed*?
3. Firewall: definition (one line) and the 4 filters.
4. Malware: the 5 types.
5. Symmetric encryption: its main weakness.
6. Code of ethics: the 3 bodies and the 8 areas of conduct (in 3 groups).
7. PDPA: the 4 obligations, the DPO's role, consequences.
8. "Discuss" ethics answer: the 4-step structure.
9. Decision tables: limited vs extended entry; impossible rules; the completeness check.
10. BST delete: the 3 cases.
11. Pre-, in- and post-order of the tree `50 → 30, 70; 30 → 20, 40; 70 → 60, 80; 40 → 35, _`.
12. Partial vs transitive dependency (one line each); what 1NF actually requires.
13. How an M:M relationship is built.
14. NoSQL: the 4 types; what referencing is.
15. ACID in full.

## Answers

1. **Confidentiality** (no unauthorised access), **Integrity** (no unauthorised modification), **Availability** (stays usable for authorised users).
2. **Integrity, authenticity, non-repudiation.** If the sender's public key decrypts the signature correctly, only the sender's private key could have made it: *who sent it*. If the two digests match: *not changed*.
3. Monitors and controls incoming and outgoing traffic against a set of rules. Filters: **IP, port, protocol, payload**. It can't inspect the *contents* of encrypted packets, but it can still filter them by IP, port and protocol.
4. **Virus, worm, trojan, ransomware, spyware** (spyware secretly collects user data and sends it to a third party).
5. The shared key has to be sent securely first; if it's intercepted, all messages can be read.
6. **ACM, IEEE, SCS.** Self: Integrity & Honesty, Competence, Continuing Professional Development. Others: Professional Conduct, Confidentiality & Privacy, Respect for IP. Society: Public Interest & Social Responsibility, Responsible Use of Technology.
7. **Consent, Purpose limitation, Protection, Retention limitation.** DPO: oversees compliance, promotes awareness, handles complaints, identifies risks, liaises with the PDPC (Personal Data Protection **Commission**). Breaches lead to investigations, financial penalties, reputational damage, legal consequences and business disruption.
8. Name the area of conduct, then apply it to the stem, then give the other side, then a judgement and the condition it depends on. Aim at the right stakeholder (often the public, not just the client).
9. Limited entry: Y/N conditions, X actions. Extended entry: values or statements as entries. Impossible rules are marked `*`, then removed. Completeness check: each column covers 2^(number of dashes) cases, and the total must equal 2^n. Dashes only go in condition rows; every column is one complete rule.
10. **Leaf:** remove it. **One child:** the child replaces it. **Two children:** copy in the in-order successor (min of the right subtree) or the predecessor, then delete that node (always case 1 or 2). The root is not a special case.
11. Pre: `50 30 20 40 35 70 60 80`. In: `20 30 35 40 50 60 70 80`. Post: `20 35 40 30 60 80 70 50`. Dot method: left dot for pre, under for in, right for post; trace anticlockwise from the root's left side.
12. **P**artial = depends on **p**art of a composite key. **T**ransitive = depends on the key **t**hrough another non-key field (PK → B → C). 1NF: every cell atomic (one value), no repeating groups, and a primary key that makes every row unique.
13. A junction (link) table holding both foreign keys, usually as a composite primary key. This turns M:M into two 1:M relationships.
14. **Key-value, document, wide-column, graph.** Referencing stores another document's ID instead of nesting a copy of it (use it for large or frequently updated data).
15. **Atomicity, Consistency, Isolation, Durability.**
