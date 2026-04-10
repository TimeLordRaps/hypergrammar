# TIME.md — Open Frame & Contradiction Register

## Purpose

`TIME.md` records open frames and contradictions discovered by humans or agents.

- **Contradictions** are divergences between `HUMANS.md` and `AGENTS.md` (or between either and the code).
- **Open frames** are unstated, unformalized, or unnamed structure that the codebase mechanically implements but never textually anchors.

It is a shared document for both agents and humans. It should be updated when either side finds a mismatch or an unformalized structure, and ideally via issue/PR so Tyler can review the frame.

## How to use

- Add a new entry for each distinct open frame or contradiction.
- Use one row per observed divergence or unformalized structure.
- Include the source, the statement, why it is an open frame or contradiction, and the current status.

## Template

| ID | Source | Statement | Contradiction | Notes | Status | Date |
|----|--------|-----------|---------------|-------|--------|------|
| 1 | AGENTS.md | Example agent rule | Human interpretation differs because ... | What changed or proposed fix | open / resolved / review | YYYY-MM-DD |

## Open Frames

| ID | Source | Statement | Contradiction | Notes | Status | Date |
|----|--------|-----------|---------------|-------|--------|------|
| 1 | src/README.md | "Metamath emphasis in this interpreter" | Frames Metamath as the emphasis. Actual purpose: hypermath formation, with Metamath as first embedded witness (subgrammar at a phase of the □-loop). The interpreter proves embedding, not Metamath parity. | Renamed section to "Metamath as first embedding witness." Reframed from emphasis to evidence. | resolved | 2026-04-10 |
| 2 | AGENTS.md, all docs | Continuation § describes closure=proof, open frame=non-closure theorem. | The central thesis — falsifiability is not a necessary precondition for provability — is implemented mechanically (closed form = proved without requiring falsification of alternatives) but never stated. The *reason* hypergrammar exists has no textual anchor in the codebase. | Add explicit thesis statement to AGENTS.md § Continuation or new § Thesis. The mechanism is there; the claim needs to be named. | open | 2026-04-10 |
| 3 | AGENTS.md | No mention of hypertopology or meta-topology. | Hypergrammar → hypermath → hypertopologies is the intended build chain. Continuation is proto-topological (open frames as neighborhoods, closure as compactness analogue), but the topological layer is unnamed and unformalized. Arithmetic and set theory are legacy cross-sections; the replacement needs structural spaces native to the □-loop. | Formalize when ready. Continuation's open/closed structure is the seed. Not blocking current work. | open | 2026-04-10 |
| 4 | HUMANS.md | "≡ (congruence) — same structure and depth, possibly built by different paths." | Ch20 and AGENTS.md corrected ≡ to depth-free: "Same outcome regardless of derivation depth or path." HUMANS.md carried the old depth-dependent definition. Also fixed in Ch18 topology. | Fixed: HUMANS.md ≡ now reads "same outcome regardless of derivation depth or path." Ch18 updated. | resolved | 2026-04-10 |
| 5 | HUMANS.md | Relations section says "These go from strictest to loosest" and lists =, ≡, ~ in that order. | HUMANS.md presented = first (implying primacy) while AGENTS.md establishes ~ as primary. A reader of HUMANS.md alone would not know = is derived. | Fixed: reordered to ~ first, added dependence statement. Now reads "most foundational to most derived." | resolved | 2026-04-10 |
| 6 | relations.py, constraints.py | `relation_congruent` defined in relations.py but never imported or called by constraints.py. | ≡ (congruence) is one of three core relations in AGENTS.md, but the constraint engine only uses `relation_equal` and `relation_similar`. Congruence has no runtime witness in the interpreter. The relation exists in code but is dead — never exercised. | Either wire ≡ into constraint checks where it belongs, or document why only ~ and = suffice at this stage. | open | 2026-04-10 |
| 7 | AGENTS.md, HUMANS.md, docs | `.hg` file format defined in AGENTS.md § File Format and HUMANS.md § How to read a derivation. | No `.hg` files exist anywhere in the repository. The native file format of the system has zero examples. The parser supports `.hg` but there is nothing to parse. | Create at least one canonical `.hg` example demonstrating a closed-form derivation. | open | 2026-04-10 |
| 8 | viz_20_meta_closure.py | Node "HIER" labeled "Dichrome Hierarchy: L/□ → Geo/Phil → Domain"; edges labeled "topological level in hierarchy" and "pre-topological level in hierarchy." | AGENTS.md § The Hypergrammar says "There are no levels." The viz uses "hierarchy" and "level" language for dichrome relationships. Similarly, viz_17 uses "meta-leveling" edge labels. The dichrome relationship may be a rotation or phase, not a hierarchy. | Rename/relabel to avoid "hierarchy"/"level" unless the dichrome structure is intentionally hierarchical (which would need an AGENTS.md amendment). | open | 2026-04-10 |

## Notes

- `Source` should be either `AGENTS.md`, `HUMANS.md`, a source file, or both.
- `Status` should reflect whether the open frame or contradiction is still active.
- Keep entries short and precise.

## Ownership

- Either agents or humans may write into `TIME.md`.
- Prefer an issue or PR in repos you want Tyler to see.
- This file is not a spec; it is a record of frames that need attention.
