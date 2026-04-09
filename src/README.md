# `src` — Hypergrammar Interpreter

This folder now contains the executable interpreter package that evaluates whether a grammar-layer specification fits hypergrammar constraints.

## Layout

- `hypergrammar/models.py` — typed models for layers, rules, specs, and validation results.
- `hypergrammar/parser.py` — loads `.json` / `.hg` specs into normalized `HypergrammarSpec` objects.
- `hypergrammar/relations.py` — symbolic relation primitives (`=`, `≡`, `~`) and loop-depth parsing.
- `hypergrammar/constraints.py` — constraint engine implementing axiom + closure checks.
- `hypergrammar/interpreter.py` — orchestration facade.
- `hypergrammar/cli.py` — command-line interface.
- `hypergrammar/examples/*.json` — canonical input examples.

## What it checks

1. **Layer compatibility**
   - grammar
   - metagrammar (must target grammar)
   - metametagrammar (must target metagrammar)

2. **Rule-domain consistency**
   - lhs in nonterminal set
   - rhs symbol declarations

3. **Hypergrammar axioms (computational approximation)**
   - `ax-diff`: closure term does not collapse to universe/ground
   - `ax-sim`: closure term stays similar to ground/universe
   - `ax-loop`: `L(L(x)) ~ x` checked when depth-2 terms exist

4. **Closed-form condition**
   - final derivation term must be similar to first term

## Run

From repo root:

- `PYTHONPATH=src E:/real_repos/hyper-grammar/.venv/bin/python.exe -m hypergrammar.cli src/hypergrammar/examples/grammar.json --pretty`
- `PYTHONPATH=src E:/real_repos/hyper-grammar/.venv/bin/python.exe -m hypergrammar.cli src/hypergrammar/examples/metagrammar.json --pretty`
- `PYTHONPATH=src E:/real_repos/hyper-grammar/.venv/bin/python.exe -m hypergrammar.cli src/hypergrammar/examples/metametagrammar.json --pretty`
- `PYTHONPATH=src E:/real_repos/hyper-grammar/.venv/bin/python.exe -m hypergrammar.cli src/hypergrammar/examples/metamath_metagrammar.json --pretty`

Exit code is `0` when valid, `1` when errors are present.

## Metamath trial (current result)

The bundled spec `src/hypergrammar/examples/metamath_metagrammar.json` models core Metamath statement families (`$c`, `$v`, `$f`, `$e`, `$a`, `$p`, `$d`, block delimiters, comments) as a metagrammar targeting grammar.

With the current closure chain input, it validates successfully under hypergrammar constraints.

### What that means about Metamath specifically

For this interpreter and this trial input, "Metamath validates" means:

1. A Metamath-style **database schema** can be represented as a metagrammar in this model.
2. The represented statement families are structurally compatible with current hypergrammar checks:
   - layer compatibility (`metagrammar -> grammar`),
   - rule-symbol domain coherence,
   - closure/axiom checks on the supplied derivation chain.
3. At this scope, Metamath appears as an embeddable external formal system at the **syntax/schema level**.

### What this does **not** mean yet

This does **not** currently prove that:

- all Metamath databases (e.g., full `set.mm`) satisfy hypergrammar,
- all Metamath proof objects are semantically equivalent to hypergrammar closure proofs,
- Metamath's complete proof-checking semantics have been rederived in hypergrammar.

So the current result is a **positive structural compatibility witness**, not a total semantic equivalence claim.

### Next empirical hardening steps

- Parse a real Metamath source slice into this schema (instead of hand-authored sample tokens).
- Add constraints for compressed proof object structure (`$=` segments) and disjoint-variable discipline.
- Validate larger theorem/hypothesis families with derivation chains generated from actual proof traces.
