# Grammar Fundamentals

This document gives the general grammar background needed before reading the grammar type ladder and hypergrammar inversion notes.

## What is a grammar?

A **grammar** is a finite specification that generates a language.

A standard grammar is written as a 4-tuple:

- $G = (V, \Sigma, P, S)$
- $V$: nonterminal symbols
- $\Sigma$: terminal symbols
- $P$: production rules
- $S$: start symbol

A grammar does not list every sentence directly. It gives rule-based machinery for deriving sentences.

## Alphabet, strings, and languages

- **Alphabet**: a finite set of symbols, e.g. $\Sigma = \{a,b\}$.
- **String**: a finite sequence over an alphabet, e.g. `abba`.
- **Language**: a set of strings over an alphabet.

Example language:

- $L = \{ a^n b^n \mid n \geq 0 \}$
- Contains `""`, `ab`, `aabb`, `aaabbb`, ...

## Terminals and nonterminals

- **Terminals** are output symbols that appear in final strings.
- **Nonterminals** are placeholders used during derivation.

Example:

- Nonterminals: $\{S\}$
- Terminals: $\{a,b\}$
- Rule: $S \rightarrow aSb \mid \epsilon$

Here, `S` is replaced until only terminals remain.

## Production rules and derivations

A **production** rewrites one symbol pattern into another.

- Leftmost derivation: always expand the leftmost nonterminal first.
- Rightmost derivation: always expand the rightmost nonterminal first.

For grammar $S \rightarrow aSb \mid \epsilon$:

1. $S \Rightarrow aSb$
2. $\Rightarrow aaSbb$
3. $\Rightarrow aa\epsilon bb$
4. $\Rightarrow aabb$

So `aabb` is in the language.

## Parse trees and ambiguity

A **parse tree** records one derivation structure for a string.

A grammar is **ambiguous** if at least one string has two distinct parse trees.

Why this matters:

- Ambiguity complicates parsing and proof obligations.
- Unambiguous structure is often preferred in verification pipelines.

## Why grammars matter for verification

Grammars are useful because they turn language acceptance into structural questions:

- Can this string be generated?
- Which rule path generated it?
- Is the derivation unique?

This framing connects naturally to formal proof and model checking workflows.

## Deterministic scaffold

- Script: [`01_grammar_fundamentals_scaffold.py`](./01_grammar_fundamentals_scaffold.py)
- Artifact target: `./scaffolds/grammar_fundamentals/`

Closure note: after completing chapters 02 through 09, read
[`10_necessity_constraint_form.md`](./10_necessity_constraint_form.md)
to reinterpret chapter 01 as presupposed by the computed closure constraint.

Next step: read [`02_chomsky_hierarchy.md`](./02_chomsky_hierarchy.md).