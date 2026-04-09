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

## Notes

- `Source` should be either `AGENTS.md`, `HUMANS.md`, or both.
- `Status` should reflect whether the contradiction is still active.
- Keep entries short and precise.

## Ownership

- Either agents or humans may write into `TIME.md`.
- Prefer an issue or PR in repos you want Tyler to see.
- This file is not a spec; it is a record of frames that need attention.
