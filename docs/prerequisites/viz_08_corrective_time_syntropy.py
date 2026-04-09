from __future__ import annotations

from _frameviz_core import Edge, FrameModel, Node, render_and_emit


FRAME = FrameModel(
    doc_id="08_corrective_time_syntropy",
    doc_title="Corrective Time Syntropy",
    purpose="Visualize corrective ordering where ideal clauses guide state updates under uncertainty.",
    nodes=[
        Node("NK", "Current Now-Frame N_k", "state"),
        Node("IK", "Ideal Clauses I_k", "constraint-set"),
        Node("C", "Corrective Operator C", "operator"),
        Node("N1", "Next State N_{k+1}", "state"),
        Node("RHO", "Residual Inconsistency ρ", "diagnostic"),
        Node("SYN", "Syntropic Ordering", "behavior"),
        Node("UNC", "Irreducible Uncertainty", "condition"),
        Node("PLAN", "Ideal-Attractor Planning", "strategy"),
        Node("TR", "History as Trace Constraints", "constraint"),
    ],
    edges=[
        Edge("NK", "C", "input"),
        Edge("IK", "C", "guides"),
        Edge("C", "N1", "produces"),
        Edge("NK", "RHO", "measured by"),
        Edge("N1", "RHO", "target non-increase"),
        Edge("RHO", "SYN", "supports when decreasing"),
        Edge("UNC", "PLAN", "requires"),
        Edge("PLAN", "IK", "defines"),
        Edge("TR", "C", "constrains without forecasting"),
    ],
    notes=[
        "Time is modeled as correction ordering, not deterministic future extrapolation.",
        "Planning remains valid via ideal attractors under uncertainty.",
    ],
)


if __name__ == "__main__":
    render_and_emit(FRAME, __file__)
