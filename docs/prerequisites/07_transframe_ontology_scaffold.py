from __future__ import annotations

from _hyperstructure_scaffold_core import build_and_emit


if __name__ == "__main__":
    build_and_emit(
        chapter_id="07_transframe_ontology",
        chapter_title="Transframe Ontology Scaffold",
        chapter_number=7,
        previous_chapter_id="06_recursive_now_frame_expanded",
        constraints=[
            "now-frame accessibility boundary",
            "global transframe movement requirement",
            "recursive self-embedding admissibility",
            "non-local interpolation restriction",
        ],
        notes=[
            "Deterministically links from chapter 06 via signature inheritance.",
            "Sets ontology manifold for chapter 08 corrective-time scaffolding.",
        ],
        script_file=__file__,
    )
