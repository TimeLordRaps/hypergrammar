from __future__ import annotations

from _frameviz_core import Edge, FrameModel, Node, render_and_emit


FRAME = FrameModel(
    doc_id="13_geometry",
    doc_title="Geometry",
    purpose="Visualize the base geometry formalism: Euclid's axioms, the parallel postulate crack, non-Euclidean generalization, and the Erlangen Programme mapping to hypergrammar relations.",
    nodes=[
        Node("L12", "Ch12 Consolidative Recurrence (Closed)", "chapter"),
        Node("EUC", "Euclidean Geometry (curvature = 0)", "concept"),
        Node("PP", "Parallel Postulate (hidden parameter)", "constraint"),
        Node("HYP", "Hyperbolic Geometry (curvature < 0)", "concept"),
        Node("ELL", "Elliptic Geometry (curvature > 0)", "concept"),
        Node("RIEM", "Riemannian Manifold (curvature varies)", "concept"),
        Node("PROJ", "Projective Geometry (no metric)", "concept"),
        Node("ERL", "Erlangen Programme (geometry = group)", "concept"),
        Node("FILT", "Filtration = ⊂ ≡ ⊂ ~", "criterion"),
    ],
    edges=[
        Edge("L12", "EUC", "derivation space has flat geometry by default"),
        Edge("EUC", "PP", "distinguished by the parameter-shaped axiom"),
        Edge("PP", "HYP", "deny → infinitely many parallels"),
        Edge("PP", "ELL", "deny → no parallels"),
        Edge("HYP", "RIEM", "constant negative → variable curvature"),
        Edge("ELL", "RIEM", "constant positive → variable curvature"),
        Edge("EUC", "RIEM", "zero → variable curvature"),
        Edge("RIEM", "PROJ", "discard metric, retain incidence"),
        Edge("ERL", "FILT", "transformation group determines invariant level"),
        Edge("PROJ", "ERL", "Klein unification: all geometries as subgroups"),
    ],
    notes=[
        "Base formalism for meta-geometry (Ch14). Must be stated before it can be generalized.",
        "The parallel postulate is parameter-shaped, not axiom-shaped — this is the crack.",
        "Erlangen link: L is the transformation group; =, ≡, ~ are three invariant levels.",
        "Riemannian geometry makes curvature a variable — the key move Ch14 will generalize.",
    ],
)


if __name__ == "__main__":
    render_and_emit(FRAME, __file__)
