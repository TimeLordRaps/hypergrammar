# Chomsky Hierarchy

This document introduces the classical grammar hierarchy and its operational intuition.

## The hierarchy at a glance

The classical containment chain is:

$$
\text{Type-3} \subset \text{Type-2} \subset \text{Type-1} \subset \text{Type-0}
$$

Each step upward allows more expressive rule forms.

| Type | Name | Typical rule shape | Typical recognizer intuition |
|---|---|---|---|
| 3 | Regular | $A \rightarrow aB \mid a$ | Finite automaton |
| 2 | Context-Free | $A \rightarrow \alpha$ | Pushdown automaton |
| 1 | Context-Sensitive | $\alpha A \beta \rightarrow \alpha \gamma \beta$ with $|\gamma|\ge1$ | Linear-bounded automaton |
| 0 | Unrestricted | $\alpha \rightarrow \beta$ (mild constraints) | Turing machine |

## Type-3 regular grammars

Regular grammars capture patterns that do not need unbounded nested memory.

Example language:

- $L = (ab)^*$
- Strings: `""`, `ab`, `abab`, `ababab`, ...

A right-linear grammar can generate this with rules such as:

- $S \rightarrow aA \mid \epsilon$
- $A \rightarrow bS$

## Type-2 context-free grammars

Context-free grammars (CFGs) allow one nonterminal on the left side of each production.

Classic example:

- $L = \{ a^n b^n \mid n \ge 0 \}$

Grammar:

- $S \rightarrow aSb \mid \epsilon$

This needs stack-like memory; finite-state machinery alone is insufficient.

## Type-1 context-sensitive grammars

Context-sensitive grammars can enforce constraints that depend on surrounding symbols.

Intuition:

- Rewriting can depend on left/right context.
- String length is generally nondecreasing under production application.

These grammars capture some agreement/cross-dependency constraints not naturally represented as CFGs.

## Type-0 unrestricted grammars

Type-0 grammars are maximally general in the hierarchy.

- They can represent any recursively enumerable language.
- Their computational intuition aligns with Turing-complete rewriting systems.

Power increases, but reasoning complexity and verification burden also increase.

## Inclusion chain and what it means

Containment means every Type-3 language is also Type-2, every Type-2 also Type-1, and so on.

It does **not** mean every Type-1 language is Type-2, etc.

Why this matters:

- Higher expressivity can model richer structures.
- Lower expressivity can make parsing and proofs simpler.

## Why the hierarchy still matters

Even when modern systems are not written as textbook grammars, these classes still provide:

- A vocabulary for expressivity limits.
- A way to discuss what structural constraints can or cannot encode.
- A bridge from language theory to verification architecture.

Next step: read [`03_hyper_inversion.md`](./03_hyper_inversion.md) for the hyper-grammar reinterpretation.