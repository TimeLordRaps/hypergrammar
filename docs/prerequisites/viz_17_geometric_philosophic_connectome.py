from __future__ import annotations

from _frameviz_core import Edge, FrameModel, Node, render_and_emit


FRAME = FrameModel(
    doc_id="17_geometric_philosophic_connectome",
    doc_title="The Geometric-Philosophic Connectome",
    purpose="Visualize the quadfecta square: 4 corners, 4 edges, 2 diagonals, center = □, recursive isomorphism, VSM mapping.",
    nodes=[
        Node("GEO", "Geometry (base-geometric)", "chapter"),
        Node("PHIL", "Philosophy (base-philosophic)", "chapter"),
        Node("MGEO", "Meta-Geometry (expansion)", "chapter"),
        Node("MPHIL", "Meta-Philosophy (expansion)", "chapter"),
        Node("CENTER", "Center = □ (fixed point)", "criterion"),
        Node("DIAG1", "Diagonal: Geo↔Meta-Phil (Kant)", "concept"),
        Node("DIAG2", "Diagonal: Phil↔Meta-Geo (Gödel)", "concept"),
        Node("RISO", "Recursive Isomorphism (180° rotation)", "concept"),
        Node("VSM5", "VSM System 5 = □", "concept"),
    ],
    edges=[
        Edge("GEO", "PHIL", "Edge 1: Geometric Philosophy"),
        Edge("PHIL", "GEO", "Edge 2: Philosophical Geometry"),
        Edge("MGEO", "MPHIL", "Edge 3: Meta-Geometric Philosophy"),
        Edge("MPHIL", "MGEO", "Edge 4: Meta-Philosophical Geometry"),
        Edge("GEO", "MGEO", "meta-leveling: geometry → meta-geometry"),
        Edge("PHIL", "MPHIL", "meta-leveling: philosophy → meta-philosophy"),
        Edge("GEO", "MPHIL", "Diagonal 1: synthetic a priori (Kant)"),
        Edge("PHIL", "MGEO", "Diagonal 2: structural content (Gödel)"),
        Edge("DIAG1", "CENTER", "diagonals intersect at □"),
        Edge("DIAG2", "CENTER", "diagonals intersect at □"),
        Edge("RISO", "CENTER", "rotation generates structure from fixed point"),
        Edge("CENTER", "VSM5", "center = System 5 = identity/policy"),
    ],
    notes=[
        "First irreducibly 2-dimensional structure in the prerequisites.",
        "180° rotation: Geo↔Meta-Phil, Phil↔Meta-Geo. This IS ax-loop: L(L(x)) ~ x.",
        "Physical frame: two systems + mapping = recursive isomorphism.",
        "Abstract frame: one system + rotation = self-isomorphism.",
        "Both frames are ~-related but not = or ≡-related.",
    ],
)


if __name__ == "__main__":
    render_and_emit(FRAME, __file__)
