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

5. **Metamath hardening checks** (when Metamath constraint metadata is present)
   - theorem proof-segment structure around `$=` (compressed/uncompressed segment well-formedness)
   - disjoint-variable (`$d`) declaration discipline (declared vars, minimum arity, duplicate handling)
   - theorem-level proof-label linkage to available `$a/$p/$f/$e` labels in scope
   - compressed-proof payload decoding checks for label-index expansion semantics
   - stack-level proof-step execution checks (substitution + final result-shape validation)

## Run

From repo root:

- `PYTHONPATH=src E:/real_repos/hyper-grammar/.venv/bin/python.exe -m hypergrammar.cli src/hypergrammar/examples/grammar.json --pretty`
- `PYTHONPATH=src E:/real_repos/hyper-grammar/.venv/bin/python.exe -m hypergrammar.cli src/hypergrammar/examples/metagrammar.json --pretty`
- `PYTHONPATH=src E:/real_repos/hyper-grammar/.venv/bin/python.exe -m hypergrammar.cli src/hypergrammar/examples/metametagrammar.json --pretty`
- `PYTHONPATH=src E:/real_repos/hyper-grammar/.venv/bin/python.exe -m hypergrammar.cli src/hypergrammar/examples/metamath_metagrammar.json --pretty`
- `PYTHONPATH=src E:/real_repos/hyper-grammar/.venv/bin/python.exe src/hypergrammar/examples/build_metamath_slice_schema.py`
- `PYTHONPATH=src E:/real_repos/hyper-grammar/.venv/bin/python.exe -m hypergrammar.cli src/hypergrammar/examples/source_trail/setmm_slice_360_470.mm --pretty`
- `PYTHONPATH=src E:/real_repos/hyper-grammar/.venv/bin/python.exe -m hypergrammar.cli src/hypergrammar/examples/source_trail/setmm_extended_propositional.mm --pretty`

Exit code is `0` when valid, `1` when errors are present.

## Metamath emphasis in this interpreter

This interpreter supports two complementary Metamath tracks:

1. **Modeled Metamath metagrammar**
   - Input: [`./hypergrammar/examples/metamath_metagrammar.json`](./hypergrammar/examples/metamath_metagrammar.json)
   - Purpose: hand-authored schema-level representation of core Metamath statement families.
   - Emphasis: fast structural compatibility checks at the family/type level.

2. **Real-source Metamath slice parse**
   - Input: [`./hypergrammar/examples/source_trail/setmm_slice_360_470.mm`](./hypergrammar/examples/source_trail/setmm_slice_360_470.mm)
   - Parser output: [`./hypergrammar/examples/metamath_setmm_slice_parsed.json`](./hypergrammar/examples/metamath_setmm_slice_parsed.json)
   - Emphasis: source-traceable hardening checks driven by extracted statements from `set.mm`.

For Metamath-specific claims in this repo, treat the **real-source path** as the stronger evidence surface.

## Real-source Metamath slice parse (implemented)

This repository now parses a real Metamath source slice directly (`.mm`) into the interpreter schema.

### Source-trail hyperlink accountability

- Upstream source (raw): [set.mm raw](https://raw.githubusercontent.com/metamath/set.mm/develop/set.mm)
- Upstream source (raw via GitHub): [set.mm raw (refs/heads/develop)](https://github.com/metamath/set.mm/raw/refs/heads/develop/set.mm)
- Upstream source (browse): [set.mm on GitHub](https://github.com/metamath/set.mm/blob/develop/set.mm)
- Upstream source (line-anchored slice): [set.mm lines 360-470](https://github.com/metamath/set.mm/blob/develop/set.mm#L360-L470)
- Upstream source history: [set.mm commit history](https://github.com/metamath/set.mm/commits/develop/set.mm)
- Latest observed upstream commit (this accountability pass): [e4c0fea](https://github.com/metamath/set.mm/commit/e4c0fea5b90d4d807e6f588a064025cec1d3adbb)
- Captured slice: [`./hypergrammar/examples/source_trail/setmm_slice_360_470.mm`](./hypergrammar/examples/source_trail/setmm_slice_360_470.mm)
- Parser path: [`./hypergrammar/parser.py`](./hypergrammar/parser.py)
- Constraint path: [`./hypergrammar/constraints.py`](./hypergrammar/constraints.py)
- Schema builder: [`./hypergrammar/examples/build_metamath_slice_schema.py`](./hypergrammar/examples/build_metamath_slice_schema.py)
- Generated parsed schema: [`./hypergrammar/examples/metamath_setmm_slice_parsed.json`](./hypergrammar/examples/metamath_setmm_slice_parsed.json)

Reasoning chain is encoded in parsed schema metadata under:

- `metadata.source_trail`
- `metadata.reasoning`
- `metadata.metamath_constraints`

### Reason-point evidence map

- Claim: the parsed schema comes from a real upstream slice window.
   - Evidence: [set.mm lines 360-470](https://github.com/metamath/set.mm/blob/develop/set.mm#L360-L470) -> [`setmm_slice_360_470.mm`](./hypergrammar/examples/source_trail/setmm_slice_360_470.mm) -> [`metamath_setmm_slice_parsed.json`](./hypergrammar/examples/metamath_setmm_slice_parsed.json)
- Claim: extraction logic is inspectable and reproducible.
   - Evidence: [`parser.py`](./hypergrammar/parser.py) (`_tokenize_metamath`, `_parse_metamath_statements`) and [`build_metamath_slice_schema.py`](./hypergrammar/examples/build_metamath_slice_schema.py)
- Claim: theorem linkage is checked against in-scope Metamath labels.
   - Evidence: `metadata.metamath_constraints.theorem_linkage` links theorem proof references to available `$a/$p/$f/$e` labels and reports unresolved references.
- Claim: compressed proof payloads are decoded and validated against expansion-table semantics.
   - Evidence: `metadata.metamath_constraints.compressed_payload_decoding` decodes compressed payload symbols and checks index bounds against expanded mandatory-hypothesis + label-list tables.
- Claim: proof execution is checked at stack level, not just index/linkage level.
   - Evidence: `metadata.metamath_constraints.stack_execution` executes proof steps, validates floating/essential substitution behavior, and checks final theorem result shape.
- Claim: validation output carries the full accountability + hardening trail.
   - Evidence: run CLI on the `.mm` slice (command above) and inspect `metrics.source_trail`, `metrics.reasoning`, and `metrics.metamath_constraints`.

### Metamath hardening output map

When real-source metadata is present, CLI checks include:

- `metamath_proof_segments`
- `metamath_disjoint_discipline`
- `metamath_theorem_linkage`
- `metamath_compressed_payload_decoding`
- `metamath_stack_execution`

And detailed diagnostics are emitted under:

- `metrics.metamath_constraints.proof_segments`
- `metrics.metamath_constraints.disjoint_variable_discipline`
- `metrics.metamath_constraints.theorem_linkage`
- `metrics.metamath_constraints.compressed_payload_decoding`
- `metrics.metamath_constraints.stack_execution`

## Metamath trial (current result)

The bundled modeled spec [`src/hypergrammar/examples/metamath_metagrammar.json`](./hypergrammar/examples/metamath_metagrammar.json) and the real-source parsed schema [`src/hypergrammar/examples/metamath_setmm_slice_parsed.json`](./hypergrammar/examples/metamath_setmm_slice_parsed.json) both represent core Metamath statement families (`$c`, `$v`, `$f`, `$e`, `$a`, `$p`, `$d`, block delimiters, comments) as a metagrammar targeting grammar.

With the current closure chain input, the real-source slice validates successfully under hypergrammar constraints, including proof segments, disjoint-variable discipline, theorem-linkage, payload decoding, and stack-level execution checks.

### What that means about Metamath specifically

For this interpreter and this trial input, "Metamath validates" means:

1. A Metamath-style **database schema** can be represented as a metagrammar in this model.
2. The represented statement families are structurally compatible with current hypergrammar checks:
   - layer compatibility (`metagrammar -> grammar`),
   - rule-symbol domain coherence,
   - closure/axiom checks on the supplied derivation chain,
   - Metamath hardening checks for `$=` proof segments, `$d` discipline, theorem-label linkage, compressed payload label-index expansion semantics, and stack-level proof-step execution.
3. At this scope, Metamath appears as an embeddable external formal system at the **syntax/schema level**.

### What this does **not** mean yet

This does **not** currently prove that:

- all Metamath databases (e.g., full `set.mm`) satisfy hypergrammar,
- all Metamath proof objects are semantically equivalent to hypergrammar closure proofs,
- Metamath's complete proof-checking semantics have been rederived in hypergrammar.

So the current result is a **positive structural compatibility witness**, not a total semantic equivalence claim.

### Empirical hardening progress

- **Disjoint-variable restriction enforcement during substitution** — DONE. Stack-level proof execution now collects `$d` pairs into scopes, computes mandatory DV pairs for each assertion, and checks that substitution images have disjoint variable sets. Violation count is tracked and reported through the constraint engine.
- **Compressed-subproof execution semantics** — VERIFIED. Save (Z) and recall operations follow Metamath verifier behavior: Z copies the current stack top into the saved-subproof list, and recall pushes a copy from saved subproofs back onto the stack. Index computation (`index - len(expanded_label_table) - 1`) is correct.
- **Larger theorem/hypothesis families** — DONE. Extended test slice (`setmm_extended_propositional.mm`) exercises multi-step uncompressed proofs (a1i: 9 steps), DV-restricted assertions (dvel/dvth with `$d x y`), syntax builders (wn, wi), and all four propositional axioms (ax-mp, ax-1, ax-2, ax-3).

### Remaining hardening targets

- Extend test coverage to theorems with compressed proofs that use save/recall (Z) operations.
- Validate against larger `set.mm` slices covering predicate calculus (quantifiers, `$d` between set and wff variables).
- Cross-check with an independent Metamath verifier (e.g., mmverify.py) on the same slices.
