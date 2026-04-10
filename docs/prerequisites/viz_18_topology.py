from __future__ import annotations

from _frameviz_core import Edge, FrameModel, Node, render_and_emit


FRAME = FrameModel(
    doc_id="18_topology",
    doc_title="Topology",
    purpose="Visualize base topology: open-set axioms, homeomorphism, invariants, the hierarchy Set⊃Topology⊃...⊃Geometry, and the ~-relation as topological.",
    nodes=[
        Node("L17", "Ch17 Connectome (Closed)", "chapter"),
        Node("OPEN", "Open Sets (3 axioms)", "concept"),
        Node("CONT", "Continuity (preimage of open is open)", "concept"),
        Node("HOMEO", "Homeomorphism (topological equivalence)", "concept"),
        Node("INV", "Invariants: genus, π₁, χ, dimension", "criterion"),
        Node("HIER", "Set ⊃ Topology ⊃ Differential ⊃ Metric ⊃ Geometry", "concept"),
        Node("SIM", "Similarity ~ = Topological Relation", "concept"),
        Node("CLASS", "Classification: closed/open/oscillating", "concept"),
    ],
    edges=[
        Edge("L17", "OPEN", "connectome structure needs topological axioms stated"),
        Edge("OPEN", "CONT", "open sets define which maps preserve nearness"),
        Edge("CONT", "HOMEO", "continuous bijection with continuous inverse"),
        Edge("HOMEO", "INV", "invariants distinguish non-homeomorphic spaces"),
        Edge("HIER", "SIM", "topology = coarsest layer; ~ is the topological relation"),
        Edge("SIM", "INV", "~ preserves topological invariants"),
        Edge("INV", "CLASS", "derivation types classified by topological type"),
        Edge("CLASS", "L17", "closed form = loop, open frame = curve, paradox = orbit"),
    ],
    notes=[
        "Base formalism for meta-topologies (Ch19). Must be stated before generalized.",
        "Topology is more primitive than geometry: every geometry determines a topology, not vice versa.",
        "The filtration = ⊂ ≡ ⊂ ~ recapitulates Set⊃...⊃Geometry in reverse.",
        "Classification of surfaces by genus parallels classification of derivations by closure type.",
    ],
)


if __name__ == "__main__":
    render_and_emit(FRAME, __file__)
