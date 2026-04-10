# hyper-grammar

**hyper-grammar** is a docs-first, self-verifying symbolic library project.

The repository is organized so that conceptual foundations are readable first, executable artifacts are inspectable second, and validation outputs are reproducible from source trails.

## Docs-first ideal

This repository is intentionally built as **theory -> scaffold -> execution -> validation**:

1. Learn the conceptual progression in `docs/prerequisites/`.
2. Inspect generated scaffolds and visualizations to see each layer operationalized.
3. Run the interpreter in `src/` against canonical examples and real Metamath slices.
4. Verify claims via machine-readable metadata and source-trail links.

If you only read one file first, start here:

- [`docs/prerequisites/00_learning_path.md`](docs/prerequisites/00_learning_path.md)

## Repository map

- [`docs/prerequisites/`](docs/prerequisites/) — docs-first curriculum (chapters `00`–`21`), scaffolds, and visualizers.
- [`src/`](src/) — executable interpreter package and examples.
- [`src/README.md`](src/README.md) — detailed interpreter + Metamath validation behavior.
- [`AGENTS.md`](AGENTS.md) — agent-facing behavior and conceptual contract.
- [`HUMANS.md`](HUMANS.md) — human-facing companion document.
- [`TIME.md`](TIME.md) — open frame & contradiction register.

## Reading path

- [`00_learning_path.md`](docs/prerequisites/00_learning_path.md)
- [`01_grammar_fundamentals.md`](docs/prerequisites/01_grammar_fundamentals.md)
- [`02_chomsky_hierarchy.md`](docs/prerequisites/02_chomsky_hierarchy.md)
- [`03_hyper_inversion.md`](docs/prerequisites/03_hyper_inversion.md)
- [`04_degrees_of_freedom.md`](docs/prerequisites/04_degrees_of_freedom.md)
- [`05_recursive_now_frame.md`](docs/prerequisites/05_recursive_now_frame.md)
- [`06_recursive_now_frame_expanded.md`](docs/prerequisites/06_recursive_now_frame_expanded.md)
- [`07_transframe_ontology.md`](docs/prerequisites/07_transframe_ontology.md)
- [`08_corrective_time_syntropy.md`](docs/prerequisites/08_corrective_time_syntropy.md)
- [`09_mensaclaused_metaretrocausality.md`](docs/prerequisites/09_mensaclaused_metaretrocausality.md)
- [`10_necessity_constraint_form.md`](docs/prerequisites/10_necessity_constraint_form.md)
- [`11_fractal_hypergrammar_compression.md`](docs/prerequisites/11_fractal_hypergrammar_compression.md)
- [`12_consolidative_recurrence.md`](docs/prerequisites/12_consolidative_recurrence.md)
- [`13_geometry.md`](docs/prerequisites/13_geometry.md)
- [`14_meta_geometry.md`](docs/prerequisites/14_meta_geometry.md)
- [`15_philosophy.md`](docs/prerequisites/15_philosophy.md)
- [`16_meta_philosophy.md`](docs/prerequisites/16_meta_philosophy.md)
- [`17_geometric_philosophic_connectome.md`](docs/prerequisites/17_geometric_philosophic_connectome.md)
- [`18_topology.md`](docs/prerequisites/18_topology.md)
- [`19_meta_topologies.md`](docs/prerequisites/19_meta_topologies.md)
- [`20_meta_closure.md`](docs/prerequisites/20_meta_closure.md)
- [`21_hypertopologies.md`](docs/prerequisites/21_hypertopologies.md)

## Interpreter and validation

The interpreter currently validates grammar/metagrammar/metametagrammar specs and includes a hardened Metamath pathway:

- proof-segment structure checks
- disjoint-variable discipline checks
- theorem-label linkage checks
- compressed payload label-index expansion checks
- stack-level proof-step execution checks (substitution + final result-shape)

See full operational details in [`src/README.md`](src/README.md).

## Publication posture

This repo is meant to be consumable publicly:

- conceptual docs are first-class artifacts,
- executable checks are explicit and reproducible,
- source-trail accountability is embedded in generated metadata.

That combination is the baseline publication contract for hyper-grammar.
