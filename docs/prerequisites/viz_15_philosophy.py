from __future__ import annotations

from _frameviz_core import Edge, FrameModel, Node, render_and_emit


FRAME = FrameModel(
    doc_id="15_philosophy",
    doc_title="Philosophy",
    purpose="Visualize the base philosophy formalism: presupposition study, three traditions as curvature cases, argument as derivation chain, paradoxes as open frames.",
    nodes=[
        Node("L14", "Ch14 Meta-Geometry (Closed)", "chapter"),
        Node("PRESUP", "Presupposition (hidden ground)", "concept"),
        Node("ANAL", "Analytic Tradition (flat, curvature = 0)", "concept"),
        Node("CONT", "Continental Tradition (curved)", "concept"),
        Node("EAST", "Eastern Traditions (metric-free)", "concept"),
        Node("ARG", "Argument = Derivation Chain", "concept"),
        Node("DED", "Deduction (L-application)", "concept"),
        Node("IND", "Induction (continuation)", "concept"),
        Node("ABD", "Abduction (inverse-L)", "concept"),
        Node("PAR", "Paradox = Open Frame", "concept"),
    ],
    edges=[
        Edge("L14", "PRESUP", "meta-geometry revealed hidden parameters; philosophy studies them"),
        Edge("PRESUP", "ANAL", "representational: thought represents reality"),
        Edge("PRESUP", "CONT", "constitutive: thought and reality co-produce"),
        Edge("PRESUP", "EAST", "dissolvable: subject-object distinction dropped"),
        Edge("ANAL", "ARG", "analytic tradition formalizes argument structure"),
        Edge("ARG", "DED", "general → specific, closure inherited"),
        Edge("ARG", "IND", "specific → general, chain open until universal closure"),
        Edge("ARG", "ABD", "effect → best explanation, generates candidate closures"),
        Edge("DED", "PAR", "self-referential deduction oscillates without closing"),
        Edge("PAR", "PRESUP", "paradox reveals frame break in presupposition"),
    ],
    notes=[
        "Base formalism for meta-philosophy (Ch16). Must be stated before generalized.",
        "Three traditions parallel three geometries: Euclidean/Riemannian/projective.",
        "Argument-as-derivation: axioms = □, rules = L, valid = well-formed chain, sound = chain closes.",
        "Paradoxes are information, not failures: they reveal frame breaks.",
    ],
)


if __name__ == "__main__":
    render_and_emit(FRAME, __file__)
