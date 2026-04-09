# Hyper Inversion: From Chomsky Ladder to Closure Loop

This page explains how `hyper-grammar` reinterprets classical hierarchy thinking.

It does **not** erase the value of classical grammar theory; it changes the organizing geometry from a one-way ladder to a closure-oriented loop.

## Start from the classical baseline

Before inversion, review:

- [`01_grammar_fundamentals.md`](./01_grammar_fundamentals.md)
  - [What is a formal grammar?](./01_grammar_fundamentals.md#what-is-a-formal-grammar)
  - [Production rules and derivations](./01_grammar_fundamentals.md#production-rules-and-derivations)
  - [Parse trees and ambiguity](./01_grammar_fundamentals.md#parse-trees-and-ambiguity)
- [`02_chomsky_hierarchy.md`](./02_chomsky_hierarchy.md)
  - [The hierarchy at a glance](./02_chomsky_hierarchy.md#the-hierarchy-at-a-glance)
  - [Type-2 context-free grammars](./02_chomsky_hierarchy.md#type-2-context-free-grammars)
  - [Inclusion chain and what it means](./02_chomsky_hierarchy.md#inclusion-chain-and-what-it-means)

## Hyper-grammar source of truth

For the formal definitions used below, see:

- [Concepts](../../AGENTS.md#concepts)
- [Axioms](../../AGENTS.md#axioms)
- [Continuation](../../AGENTS.md#continuation)
- [The Hypergrammar (not Chomsky)](../../AGENTS.md#the-hypergrammar-not-chomsky)
- [File Format](../../AGENTS.md#file-format)

## The inversion in one sentence

Classically, grammar classes are viewed as an expressivity ladder; in hyper-grammar, those views are treated as **cross-sections of a closure process** rooted at `□` and operated by `L`.

See the formal loop statement in [The Hypergrammar (not Chomsky)](../../AGENTS.md#the-hypergrammar-not-chomsky).

## Mapping table: classical view to hyper inversion

| Classical frame | Hyper inversion framing | Primary links |
|---|---|---|
| Inclusion ladder ($\text{Type-3} \subset \text{Type-2} \subset \text{Type-1} \subset \text{Type-0}$) | Observational slices at different phases of one loop | [Hierarchy baseline](./02_chomsky_hierarchy.md#the-hierarchy-at-a-glance), [Hypergrammar loop](../../AGENTS.md#the-hypergrammar-not-chomsky) |
| Derivation as rewrite progression | Continuation as frame-in-progress that either closes or reveals non-closure | [Derivations](./01_grammar_fundamentals.md#production-rules-and-derivations), [Continuation](../../AGENTS.md#continuation) |
| Accept/reject as terminal parsing outcome | Closed form vs open frame (verification geometry) | [Parse/ambiguity](./01_grammar_fundamentals.md#parse-trees-and-ambiguity), [Continuation](../../AGENTS.md#continuation) |
| Expressivity increase up hierarchy | Relation filtration and closure behavior around fixed point (`=`, `≡`, `~`) | [Concepts](../../AGENTS.md#concepts), [Axioms](../../AGENTS.md#axioms) |
| Grammar file as syntax artifact | `.hg` file as replayable proof-chain with closure condition | [File format](../../AGENTS.md#file-format) |

## Why sibling repos matter to this inversion

The sibling lineage provides context for **structural** versus **behavioral** framing:

- `symbolic-satisfaction`
  - [README](https://github.com/TimeLordRaps/symbolic-satisfaction/blob/main/README.md)
  - [APROLOGOS](https://github.com/TimeLordRaps/symbolic-satisfaction/blob/main/APROLOGOS.md)
  - [FRAME](https://github.com/TimeLordRaps/symbolic-satisfaction/blob/main/FRAME.md)
  - [REDEFINITIONS](https://github.com/TimeLordRaps/symbolic-satisfaction/blob/main/REDEFINITIONS.md)
- `symbolic-satisfaction-1`
  - [README](https://github.com/TimeLordRaps/symbolic-satisfaction-1/blob/main/README.md)
  - [SAFETY_BRIEF](https://github.com/TimeLordRaps/symbolic-satisfaction-1/blob/main/SAFETY_BRIEF.md)
- `satisfaction-suffices`
  - [README](https://github.com/TimeLordRaps/satisfaction-suffices/blob/main/README.md)
  - [docs/index](https://github.com/TimeLordRaps/satisfaction-suffices/blob/main/docs/index.md)

These are useful for prerequisite readers because they show the same recurring move: move from preference-level guidance to structure-level guarantees.

## Terminology collision guardrails

### “Frame” is overloaded across projects

- In `symbolic-satisfaction`, [FRAME.md](https://github.com/TimeLordRaps/symbolic-satisfaction/blob/main/FRAME.md) treats frame in a structural-existence sense (`E ≠ 0` framing language).
- In `hyper-grammar`, [Continuation](../../AGENTS.md#continuation) uses frame for an unclosed derivation state.

When writing or teaching, name which frame is meant each time.

### Similarity symbol alignment

- `symbolic-satisfaction-1` uses `~` in its own continuation/universality framing (see [README](https://github.com/TimeLordRaps/symbolic-satisfaction-1/blob/main/README.md) and [SAFETY_BRIEF](https://github.com/TimeLordRaps/symbolic-satisfaction-1/blob/main/SAFETY_BRIEF.md)).
- `hyper-grammar` defines `~` in [Concepts](../../AGENTS.md#concepts) as non-empty overlap of continuation capacity.

They are adjacent ideas, but not automatically identical definitions; preserve local definitions when switching contexts.

## Link Map / Source Trail

Each claim below includes direct trace links.

1. **Classical hierarchy statement**
   - Source: [Hierarchy at a glance](./02_chomsky_hierarchy.md#the-hierarchy-at-a-glance)
2. **Hyper loop reinterpretation claim**
   - Source: [The Hypergrammar (not Chomsky)](../../AGENTS.md#the-hypergrammar-not-chomsky)
3. **Continuation-based verification framing**
   - Sources: [Derivations](./01_grammar_fundamentals.md#production-rules-and-derivations), [Continuation](../../AGENTS.md#continuation)
4. **Relation filtration reference (`= ⊂ ≡ ⊂ ~`)**
   - Source: [Concepts](../../AGENTS.md#concepts)
5. **Closed vs open behavior interpretation**
   - Source: [Continuation](../../AGENTS.md#continuation)
6. **Proof-chain file semantics (`.hg`)**
   - Source: [File Format](../../AGENTS.md#file-format)
7. **Structural-vs-behavioral lineage context**
   - Sources: [symbolic-satisfaction README](https://github.com/TimeLordRaps/symbolic-satisfaction/blob/main/README.md), [symbolic-satisfaction-1 SAFETY_BRIEF](https://github.com/TimeLordRaps/symbolic-satisfaction-1/blob/main/SAFETY_BRIEF.md), [satisfaction-suffices docs/index](https://github.com/TimeLordRaps/satisfaction-suffices/blob/main/docs/index.md)

## Practical reading sequence

1. Review classical definitions in [`01_grammar_fundamentals.md`](./01_grammar_fundamentals.md).
2. Read the hierarchy in [`02_chomsky_hierarchy.md`](./02_chomsky_hierarchy.md).
3. Read [Concepts](../../AGENTS.md#concepts), [Axioms](../../AGENTS.md#axioms), and [Continuation](../../AGENTS.md#continuation).
4. Return to this inversion page and follow each link in the Link Map / Source Trail.

## Deterministic scaffold

- Script: [`03_hyper_inversion_scaffold.py`](./03_hyper_inversion_scaffold.py)
- Artifact target: `./scaffolds/03_hyper_inversion/`

If any mismatch between this page and [`../../AGENTS.md`](../../AGENTS.md) is found, log it in [`../../TIME.md`](../../TIME.md).