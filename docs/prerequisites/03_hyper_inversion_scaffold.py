from __future__ import annotations

from _hyperstructure_scaffold_core import build_and_emit


if __name__ == "__main__":
    build_and_emit(
        chapter_id="03_hyper_inversion",
        chapter_title="Hyper Inversion Scaffold",
        chapter_number=3,
        previous_chapter_id="02_chomsky_hierarchy",
        constraints=[
            "ladder-to-loop reinterpretability",
            "continuation closure diagnostics",
            "relation filtration consistency (=, ≡, ~)",
            "source-trail hyperlink accountability",
        ],
        notes=[
            "Maps classical containment to loop cross-sections.",
            "Creates deterministic anchor for DoF diagnostics in chapter 04.",
        ],
        script_file=__file__,
    )
