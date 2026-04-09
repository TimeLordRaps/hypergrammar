from __future__ import annotations

from _frameviz_core import Edge, FrameModel, Node, render_and_emit


FRAME = FrameModel(
    doc_id="05_recursive_now_frame",
    doc_title="Recursive Now-Frame",
    purpose="Visualize present-only state evolution via corrective feedback, parity filtering, and unfolding.",
    nodes=[
        Node("NOW", "Now-Frame N", "state"),
        Node("B", "Many-Body Local States B", "state-component"),
        Node("H", "Holographic Coupling H", "state-component"),
        Node("T", "Enfolded Trace τ", "state-component"),
        Node("C", "Corrective Feedback C", "operator"),
        Node("RIC", "Ricci Trace-Free Projection", "operator-detail"),
        Node("PF", "Planck-Scale Parity Filter", "operator-detail"),
        Node("U", "Structural Update U", "operator"),
        Node("N2", "Next Now-Frame N'", "state"),
        Node("FP", "Fixed-Point Residual", "diagnostic"),
        Node("NF", "No Forecasting Rule", "constraint"),
    ],
    edges=[
        Edge("NOW", "B", "contains"),
        Edge("NOW", "H", "contains"),
        Edge("NOW", "T", "contains"),
        Edge("C", "RIC", "uses"),
        Edge("C", "PF", "uses"),
        Edge("C", "FP", "drives down"),
        Edge("C", "U", "feeds"),
        Edge("U", "N2", "produces"),
        Edge("T", "U", "constrains"),
        Edge("NF", "C", "governs"),
    ],
    notes=[
        "Past is represented as trace only; no timeline replay object exists.",
        "Future is unfolded through correction, not extrapolated from history windows.",
    ],
)


if __name__ == "__main__":
    render_and_emit(FRAME, __file__)
