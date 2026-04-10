from __future__ import annotations

from _hyperstructure_scaffold_core import build_and_emit

if __name__ == "__main__":
    build_and_emit(
        chapter_id="15_philosophy",
        chapter_title="Philosophy",
        chapter_number=15,
        previous_chapter_id="14_meta_geometry",
        constraints=[
            "philosophy = formal study of presuppositions",
            "three traditions: analytic (flat), continental (curved), eastern (projective/metric-free)",
            "argument = derivation chain; axioms = ground state; inference rules = L",
            "deduction/induction/abduction map to L-application/continuation/inverse-L",
            "paradoxes = open frames: oscillating derivation chains that do not close",
        ],
        notes=[
            "Base formalism for meta-philosophy (Ch16). Must precede, not follow.",
            "Philosophy was implicitly present since Ch01 (choosing axioms is philosophical).",
            "The three traditions parallel the three geometries: Euclidean/Riemannian/projective.",
            "Table: analytic=curvature 0, continental=curvature varies, eastern=no metric.",
            "The hidden parameter of philosophy: the reasoning-object relationship.",
        ],
        script_file=__file__,
    )
