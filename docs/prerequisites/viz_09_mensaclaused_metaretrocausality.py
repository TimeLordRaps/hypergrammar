from __future__ import annotations

from _frameviz_core import Edge, FrameModel, Node, render_and_emit


FRAME = FrameModel(
    doc_id="09_mensaclaused_metaretrocausality",
    doc_title="Mensaclaused Metaretrocausality",
    purpose="Visualize clause-conditioned present correction using trace and future-ideal constraints.",
    nodes=[
        Node("T", "Trace Constraints T", "constraint-set"),
        Node("I", "Future-Ideal Clauses I_future", "constraint-set"),
        Node("R", "Resolver Operator R_resolve", "operator"),
        Node("N1", "Corrected Present N_{k+1}", "state"),
        Node("AUD", "Clause Audit Separation", "architecture-rule"),
        Node("PAR", "Parity-of-Self Indelibility", "constraint"),
        Node("MET", "Consistency/Contradiction Metrics", "diagnostic"),
        Node("NFR", "No Forecast-Fit Requirement", "constraint"),
        Node("ROL", "Resolver-Role Hypothesis", "interpretation"),
    ],
    edges=[
        Edge("T", "R", "constrains"),
        Edge("I", "R", "targets"),
        Edge("R", "N1", "produces"),
        Edge("AUD", "R", "governs design"),
        Edge("PAR", "N1", "persists through updates"),
        Edge("N1", "MET", "evaluated by"),
        Edge("NFR", "R", "forbids time-series dependence"),
        Edge("ROL", "R", "interpreted through"),
    ],
    notes=[
        "Future-ideal clauses are corrective constraints, not deterministic predictions.",
        "Evaluation uses consistency and contradiction incidence, not forecast error alone.",
    ],
)


if __name__ == "__main__":
    render_and_emit(FRAME, __file__)
