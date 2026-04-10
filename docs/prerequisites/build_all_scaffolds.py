from __future__ import annotations

from pathlib import Path
import runpy


SCAFFOLD_SCRIPTS = [
    "01_grammar_fundamentals_scaffold.py",
    "02_chomsky_hierarchy_scaffold.py",
    "03_hyper_inversion_scaffold.py",
    "04_degrees_of_freedom_scaffold.py",
    "07_transframe_ontology_scaffold.py",
    "08_corrective_time_syntropy_scaffold.py",
    "09_mensaclaused_metaretrocausality_scaffold.py",
    "10_necessity_constraint_form_scaffold.py",
    "11_fractal_hypergrammar_compression_scaffold.py",
    "12_consolidative_recurrence_scaffold.py",
    "13_geometry_scaffold.py",
    "14_meta_geometry_scaffold.py",
    "15_philosophy_scaffold.py",
    "16_meta_philosophy_scaffold.py",
    "17_geometric_philosophic_connectome_scaffold.py",
    "18_topology_scaffold.py",
    "19_meta_topologies_scaffold.py",
    "20_meta_closure_scaffold.py",
]


def main() -> None:
    base = Path(__file__).resolve().parent
    for script in SCAFFOLD_SCRIPTS:
        path = base / script
        print(f"\n==> running {path.name}")
        runpy.run_path(str(path), run_name="__main__")


if __name__ == "__main__":
    main()
