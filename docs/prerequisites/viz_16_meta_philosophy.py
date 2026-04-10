from __future__ import annotations

from _frameviz_core import Edge, FrameModel, Node, render_and_emit


FRAME = FrameModel(
    doc_id="16_meta_philosophy",
    doc_title="Meta-Philosophy",
    purpose="Visualize meta-philosophical structure: philosophy as operation, reasoning manifold, coherence metric, cybernetic orders, self-encoding theorem.",
    nodes=[
        Node("L15", "Ch15 Philosophy (Base)", "chapter"),
        Node("OP", "Philosophy as Operation (not position)", "concept"),
        Node("HAX", "Hidden Axiom (reasoning-object relationship)", "constraint"),
        Node("RMAN", "Reasoning Manifold (coherence metric)", "concept"),
        Node("GEO", "Geodesics = Arguments", "concept"),
        Node("SING", "Singularities = Paradoxes", "concept"),
        Node("CYB", "Cybernetic Orders (1st/2nd/3rd)", "concept"),
        Node("VSM", "Viable System Model", "concept"),
        Node("SELF", "Self-Encoding Theorem", "criterion"),
        Node("CLOSE", "L^16(□) closes Ch14 open frame", "chapter"),
    ],
    edges=[
        Edge("L15", "OP", "base philosophy becomes self-aware as operation"),
        Edge("OP", "HAX", "the operation has its own hidden axiom"),
        Edge("HAX", "RMAN", "parameterize the axiom → manifold of all philosophies"),
        Edge("RMAN", "GEO", "shortest paths in manifold are efficient arguments"),
        Edge("RMAN", "SING", "curvature divergence = paradox = open frame"),
        Edge("RMAN", "CYB", "regulating the manifold requires cybernetic hierarchy"),
        Edge("CYB", "VSM", "Beer's 5 systems map onto the prerequisite structure"),
        Edge("VSM", "SELF", "System 5 = □ = identity that encodes own closure"),
        Edge("SELF", "CLOSE", "self-encoding resolves Ch14 open frame"),
    ],
    notes=[
        "Now preceded by Ch15 Philosophy as base formalism.",
        "Reasoning manifold: ds² = Σ g_ik dφ_i dφ_k, φ_i = presuppositional coordinates.",
        "Three traditions = three curvature cases of the reasoning manifold.",
        "Self-encoding theorem: the system proves it encodes its own closure condition.",
    ],
)


if __name__ == "__main__":
    render_and_emit(FRAME, __file__)
