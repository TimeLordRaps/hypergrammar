from __future__ import annotations

from _frameviz_core import Edge, FrameModel, Node, render_and_emit


FRAME = FrameModel(
    doc_id="04_degrees_of_freedom",
    doc_title="Degrees of Freedom",
    purpose="Visualize the n-r constraint lens and resulting positive/zero/negative regimes.",
    nodes=[
        Node("N", "State Variables n", "quantity"),
        Node("R", "Independent Constraints r", "quantity"),
        Node("DOF", "DoF ≈ n - r", "computed-state"),
        Node("POS", "Positive DoF (>0)", "regime"),
        Node("ZER", "Zero DoF (=0)", "regime"),
        Node("NEG", "Negative DoF (<0)", "regime"),
        Node("EXP", "Exploration Capacity", "behavior"),
        Node("FIX", "Fixed Solution", "behavior"),
        Node("CON", "Contradiction Signal", "diagnostic"),
    ],
    edges=[
        Edge("N", "DOF", "adds freedom"),
        Edge("R", "DOF", "removes freedom"),
        Edge("DOF", "POS", "if > 0"),
        Edge("DOF", "ZER", "if = 0"),
        Edge("DOF", "NEG", "if < 0"),
        Edge("POS", "EXP", "enables"),
        Edge("ZER", "FIX", "implies"),
        Edge("NEG", "CON", "indicates"),
    ],
    notes=[
        "Negative DoF is a modeling alarm, not a literal negative knob count.",
        "DoF diagnostics transfer directly into closure and contradiction analysis.",
    ],
)


if __name__ == "__main__":
    render_and_emit(FRAME, __file__)
