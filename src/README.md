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

Exit code is `0` when valid, `1` when errors are present.
