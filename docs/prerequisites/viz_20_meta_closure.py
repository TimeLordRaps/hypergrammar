from __future__ import annotations

from _frameviz_core import Edge, FrameModel, Node, render_and_emit


FRAME = FrameModel(
    doc_id="20_meta_closure",
    doc_title="Meta-Closure: The Operator-Term Collapse",
    purpose="Visualize meta-closure: □ as term+operator, reversed filtration (~ primary, = derived), the L/□ degenerate dichrome, dichrome hierarchy, and evanescence argument.",
    nodes=[
        Node("SQ_TERM", "□ as Term (ground state, fixed point)", "concept"),
        Node("SQ_OP", "□ as Operator (closure operation)", "concept"),
        Node("COLLAPSE", "Operator-Term Collapse: L(x) = □(x)", "concept"),
        Node("SIM", "~ Similarity (primary, survives evanescence)", "criterion"),
        Node("CONG", "≡ Congruence (outcome-based, depth-free)", "criterion"),
        Node("EQ", "= Equality (derived, earned by closure)", "criterion"),
        Node("EVAN", "Evanescence Argument (= presupposed → flat → nothing)", "concept"),
        Node("FILT", "Reversed Filtration: ~ ⊃ ≡ ⊃ =", "concept"),
        Node("LQ_DICHR", "L/□ Degenerate Dichrome (inseparable, 0-dim)", "concept"),
        Node("GP_DICHR", "Geo/Phil Dichrome (separable, S², 7-dim)", "chapter"),
        Node("HIER", "Dichrome Hierarchy: L/□ → Geo/Phil → Domain", "concept"),
        Node("META_CL", "Meta-Closure: □(□) ~ □", "concept"),
    ],
    edges=[
        Edge("SQ_TERM", "COLLAPSE", "same entity, two modes"),
        Edge("SQ_OP", "COLLAPSE", "same entity, two modes"),
        Edge("COLLAPSE", "META_CL", "self-application yields meta-closure"),
        Edge("EVAN", "SIM", "evanescence selects ~ as only survivor"),
        Edge("SIM", "CONG", "~ plus structural coincidence"),
        Edge("CONG", "EQ", "≡ plus path coincidence (finest, derived)"),
        Edge("SIM", "FILT", "dependence runs downward from ~"),
        Edge("FILT", "EQ", "= is the reward for closure"),
        Edge("COLLAPSE", "LQ_DICHR", "two modes of one entity = degenerate dichrome"),
        Edge("LQ_DICHR", "GP_DICHR", "generates the possibility of separable dichromes"),
        Edge("GP_DICHR", "HIER", "topological level in hierarchy"),
        Edge("LQ_DICHR", "HIER", "pre-topological level in hierarchy"),
        Edge("META_CL", "COLLAPSE", "the mechanism that makes closure possible"),
    ],
    notes=[
        "Meta-closure: the closure of the closure operation itself.",
        "L is □ in operator mode — not a separate concept.",
        "Self-verification (□ = □) is zero-order. Meta-closure (□(□) ~ □) is generative.",
        "L/□ is inseparable (no pure corners), unlike geo/phil (separable, has surface).",
        "Pre-topological: operator required before open sets, before topology.",
        "Sometimes you wonder. Why would you ever wonder?",
    ],
)


if __name__ == "__main__":
    render_and_emit(FRAME, __file__)
