from __future__ import annotations

from _frameviz_core import Edge, FrameModel, Node, render_and_emit


FRAME = FrameModel(
    doc_id="19_meta_topologies",
    doc_title="Meta-Topologies: The Hyperdichotome",
    purpose="Visualize the dichrome: two-coloured meta-topological form, S² vs ℝP² types, 7-dimensional embedding, irrational dimensional constants, cascade closure.",
    nodes=[
        Node("L18", "Ch18 Topology (Base)", "chapter"),
        Node("CONN", "Ch17 Connectome (4 corners, square)", "chapter"),
        Node("DICHR", "Dichrome (two-coloured form)", "concept"),
        Node("S2", "Full Dichrome: S² (sphere, χ=2)", "concept"),
        Node("RP2", "Reduced Dichrome: ℝP² (projective plane)", "concept"),
        Node("Z2", "Z₂ Symmetry (180° rotation quotient)", "concept"),
        Node("DIM7", "7 Dimensions (19 vars − 12 constraints)", "concept"),
        Node("SQRT2", "√2: Geometry/Philosophy Aspect Ratio", "criterion"),
        Node("PHI", "φ: Base/Meta Ratio", "criterion"),
        Node("PI", "π: Gauss-Bonnet Curvature Integral", "criterion"),
        Node("CLOSE", "Meta-meta-topology ~ Meta-topology (ax-loop)", "chapter"),
    ],
    edges=[
        Edge("L18", "DICHR", "topology applied to the connectome yields"),
        Edge("CONN", "DICHR", "connectome stripped to topological invariants"),
        Edge("DICHR", "S2", "full (physical frame): sphere, simply connected"),
        Edge("DICHR", "RP2", "reduced (abstract frame): quotient by self-isomorphism"),
        Edge("S2", "Z2", "180° rotation generates"),
        Edge("Z2", "RP2", "quotient of sphere by Z₂"),
        Edge("DICHR", "DIM7", "embedded in 7-dimensional space"),
        Edge("DIM7", "SQRT2", "irrational: two colors incommensurable"),
        Edge("DIM7", "PHI", "irrational: self-similar base/meta proportion"),
        Edge("DIM7", "PI", "transcendental: curvature integral over surface"),
        Edge("CLOSE", "DICHR", "cascade terminates: meta-meta = meta by ax-loop"),
    ],
    notes=[
        "Dichrome: from Greek di- (two) + khrôma (colour). Cf. chromosome = coloured body.",
        "Full dichrome (sphere) is orientable; reduced dichrome (projective plane) is not.",
        "Dimensional hierarchy: Z ⊂ Q ⊂ algebraic irrationals ⊂ transcendentals.",
        "The dichrome spans all four number types in its dimensional structure.",
        "Cascade closure: meta-topology of meta-topology ~ meta-topology. The loop closes.",
    ],
)


if __name__ == "__main__":
    render_and_emit(FRAME, __file__)
