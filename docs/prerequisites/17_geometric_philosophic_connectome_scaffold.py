from __future__ import annotations

from _hyperstructure_scaffold_core import build_and_emit

if __name__ == "__main__":
    build_and_emit(
        chapter_id="17_geometric_philosophic_connectome",
        chapter_title="The Geometric-Philosophic Connectome",
        chapter_number=17,
        previous_chapter_id="16_meta_philosophy",
        constraints=[
            "four corners: geometry, philosophy, meta-geometry, meta-philosophy",
            "four edges: directed reasoning relationships between adjacent corners",
            "two diagonals: Kant (geo↔meta-phil), Gödel (phil↔meta-geo)",
            "center = □: fixed point where all four corners are indistinguishable",
            "recursive isomorphism: 180° rotation generates the structure, ax-loop",
        ],
        notes=[
            "First irreducibly 2-dimensional structure in the prerequisites.",
            "VSM mapping: corners=System 1, edges=System 2, diagonals=System 3, meta-edge=System 4, center=System 5.",
            "Physical frame: recursive isomorphism (two systems, structural mapping).",
            "Abstract frame: self-isomorphism (one system, rotation).",
            "The two frames are ~-related but not =-related or ≡-related.",
        ],
        script_file=__file__,
    )
