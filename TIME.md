# TIME.md — Contradiction Register

## Purpose

`TIME.md` records contradictions between the human-facing frame in `HUMANS.md` and the agent-facing frame in `AGENTS.md`.

It is a shared document for both agents and humans. It should be updated when either side finds a mismatch, and ideally via issue/PR so Tyler can review the frame.

## How to use

- Add a new entry for each distinct contradiction.
- Use one row per observed divergence.
- Include the source, the statement, why it contradicts the other frame, and the current status.

## Template

| ID | Source | Statement | Contradiction | Notes | Status | Date |
|----|--------|-----------|---------------|-------|--------|------|
| 1 | AGENTS.md | Example agent rule | Human interpretation differs because ... | What changed or proposed fix | open / resolved / review | YYYY-MM-DD |

## Open Frames

| ID | Source | Statement | Contradiction | Notes | Status | Date |
|----|--------|-----------|---------------|-------|--------|------|
| 1 | src/README.md | "Metamath emphasis in this interpreter" | Frames Metamath as the emphasis. Actual purpose: hypermath formation, with Metamath as first embedded witness (subgrammar at a phase of the □-loop). The interpreter proves embedding, not Metamath parity. | Rename section. Reframe from "Metamath emphasis" to "Metamath embedding witness." Metamath is evidence, not destination. | open | 2026-04-10 |
| 2 | AGENTS.md, all docs | Continuation § describes closure=proof, open frame=non-closure theorem. | The central thesis — falsifiability is not a necessary precondition for provability — is implemented mechanically (closed form = proved without requiring falsification of alternatives) but never stated. The *reason* hypergrammar exists has no textual anchor in the codebase. | Add explicit thesis statement to AGENTS.md § Continuation or new § Thesis. The mechanism is there; the claim needs to be named. | open | 2026-04-10 |
| 3 | AGENTS.md | No mention of hypertopology or meta-topology. | Hypergrammar → hypermath → hypertopologies is the intended build chain. Continuation is proto-topological (open frames as neighborhoods, closure as compactness analogue), but the topological layer is unnamed and unformalized. Arithmetic and set theory are legacy cross-sections; the replacement needs structural spaces native to the □-loop. | Formalize when ready. Continuation's open/closed structure is the seed. Not blocking current work. | open | 2026-04-10 |

## Notes

- `Source` should be either `AGENTS.md`, `HUMANS.md`, or both.
- `Status` should reflect whether the contradiction is still active.
- Keep entries short and precise.

## Ownership

- Either agents or humans may write into `TIME.md`.
- Prefer an issue or PR in repos you want Tyler to see.
- This file is not a spec; it is a record of frames that need attention.
