from __future__ import annotations

from _hyperstructure_scaffold_core import build_and_emit

if __name__ == "__main__":
    build_and_emit(
        chapter_id="18_topology",
        chapter_title="Topology",
        chapter_number=18,
        previous_chapter_id="17_geometric_philosophic_connectome",
        constraints=[
            "topology = properties preserved under continuous deformation (no tearing, no gluing)",
            "three axioms: empty/whole open, arbitrary unions open, finite intersections open",
            "homeomorphism = topological equivalence; invariants = genus, π₁, χ, dimension",
            "hierarchy: Set ⊃ Topology ⊃ Differential ⊃ Metric ⊃ Geometry",
            "similarity ~ is the topological relation: neighborhoods, not distances",
        ],
        notes=[
            "Base formalism for meta-topologies (Ch19). Must precede, not follow.",
            "Topology was implicitly present from Ch01: the loop □→L(□)→L(L(□))~□ is topological.",
            "The filtration = ⊂ ≡ ⊂ ~ recapitulates Set⊃Topology⊃...⊃Geometry in reverse.",
            "Classification of surfaces: genus determines closed orientable surface type.",
            "Classification of derivations: closed (loop), open (curve), oscillating (paradox).",
        ],
        script_file=__file__,
    )
