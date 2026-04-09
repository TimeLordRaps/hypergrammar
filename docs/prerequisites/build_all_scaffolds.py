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
]


def main() -> None:
    base = Path(__file__).resolve().parent
    for script in SCAFFOLD_SCRIPTS:
        path = base / script
        print(f"\n==> running {path.name}")
        runpy.run_path(str(path), run_name="__main__")


if __name__ == "__main__":
    main()
