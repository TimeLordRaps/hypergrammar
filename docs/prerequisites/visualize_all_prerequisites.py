from __future__ import annotations

from pathlib import Path
import runpy


SCRIPTS = [
    "viz_00_learning_path.py",
    "viz_01_grammar_fundamentals.py",
    "viz_02_chomsky_hierarchy.py",
    "viz_03_hyper_inversion.py",
    "viz_04_degrees_of_freedom.py",
    "viz_05_recursive_now_frame.py",
    "viz_06_recursive_now_frame_expanded.py",
    "viz_07_transframe_ontology.py",
    "viz_08_corrective_time_syntropy.py",
    "viz_09_mensaclaused_metaretrocausality.py",
    "viz_10_necessity_constraint_form.py",
]


def main() -> None:
    base = Path(__file__).resolve().parent
    for script in SCRIPTS:
        script_path = base / script
        print(f"\n==> running {script_path.name}")
        runpy.run_path(str(script_path), run_name="__main__")


if __name__ == "__main__":
    main()
