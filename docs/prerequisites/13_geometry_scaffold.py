from __future__ import annotations

from _hyperstructure_scaffold_core import build_and_emit

if __name__ == "__main__":
    build_and_emit(
        chapter_id="13_geometry",
        chapter_title="Geometry",
        chapter_number=13,
        previous_chapter_id="12_consolidative_recurrence",
        constraints=[
            "Euclid five postulates: the parallel postulate is the hidden parameter",
            "Klein Erlangen Programme: geometry = transformation group",
            "Riemannian generalization: curvature as variable, not constant",
            "projective geometry: metric discarded, incidence and cross-ratio preserved",
            "filtration = ⊂ ≡ ⊂ ~ maps to geometric → projective resolution",
        ],
        notes=[
            "Base formalism for meta-geometry (Ch14). Must precede, not follow.",
            "Geometry was implicitly present since Ch01 (parse trees have spatial structure).",
            "Named explicitly here so meta-geometry can generalize it.",
            "The parallel postulate is parameter-shaped, not axiom-shaped — the crack through which meta-geometry enters.",
            "Erlangen link: L is the transformation group, = ≡ ~ are three invariant levels.",
        ],
        script_file=__file__,
    )
