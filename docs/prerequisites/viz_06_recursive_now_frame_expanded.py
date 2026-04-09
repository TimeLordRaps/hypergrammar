from __future__ import annotations

from _frameviz_core import Edge, FrameModel, Node, render_and_emit


FRAME = FrameModel(
    doc_id="06_recursive_now_frame_expanded",
    doc_title="Expanded Recursive Now-Frame",
    purpose="Visualize expanded corrective architecture with Hyperkähler consistency and branch-aware parity filtering.",
    nodes=[
        Node("NX", "Expanded Now-Frame N", "state"),
        Node("HK", "HyperKähler Triplet Surrogate K", "state-component"),
        Node("CUR", "Curvature-Like Pressure", "derived-quantity"),
        Node("RTF", "Ricci Trace-Free Projection", "operator-detail"),
        Node("PF", "Planck-Scale Parity Filter", "operator"),
        Node("SUB", "Sub-Planck Recursive Meta-Mix", "branch"),
        Node("SUP", "Super-Planck Stable Projection", "branch"),
        Node("COR", "Corrective Loop Φ", "operator"),
        Node("RES", "Residual Bundle", "diagnostic"),
        Node("REP", "Fixed-Point Report", "artifact"),
    ],
    edges=[
        Edge("NX", "HK", "contains"),
        Edge("COR", "CUR", "computes"),
        Edge("CUR", "RTF", "projected to"),
        Edge("COR", "PF", "routes relation updates through"),
        Edge("PF", "SUB", "if D_ij < l_P"),
        Edge("PF", "SUP", "if D_ij >= l_P"),
        Edge("COR", "RES", "aggregates"),
        Edge("HK", "RES", "contributes compatibility error"),
        Edge("RES", "REP", "exported by"),
        Edge("COR", "NX", "updates"),
    ],
    notes=[
        "This visualization highlights the dual-branch parity logic as a first-class architectural split.",
        "Residuals are interpreted as closure health signals for the active frame.",
    ],
)


if __name__ == "__main__":
    render_and_emit(FRAME, __file__)
