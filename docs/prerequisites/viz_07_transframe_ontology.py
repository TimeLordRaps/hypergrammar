from __future__ import annotations

from _frameviz_core import Edge, FrameModel, Node, render_and_emit


FRAME = FrameModel(
    doc_id="07_transframe_ontology",
    doc_title="Transframe Ontology",
    purpose="Visualize accessibility boundaries and closure conditions required for transframe movement.",
    nodes=[
        Node("NOW", "Accessible Now-Frame F_now", "manifold"),
        Node("EXT", "Inaccessible Frame Coordinates F_ext", "manifold"),
        Node("U", "Universe State Operator U", "operator"),
        Node("R", "Recursive Self-Embedding R", "operator"),
        Node("CLS", "Closure Condition R(U) ≈ U", "criterion"),
        Node("MOV", "Transframe Movement", "capability"),
        Node("NLI", "No Local Interpolation", "constraint"),
        Node("APP", "Nearby but Incomplete Approximations", "context"),
    ],
    edges=[
        Edge("NOW", "EXT", "boundary of accessibility"),
        Edge("U", "R", "subject to"),
        Edge("R", "CLS", "evaluated by"),
        Edge("CLS", "MOV", "enables when satisfied"),
        Edge("NLI", "MOV", "restricts method"),
        Edge("APP", "MOV", "motivates refinement"),
    ],
    notes=[
        "Only now-frame content is directly accessible in the active perspective.",
        "Transframe movement is conditional and global, not local interpolation.",
    ],
)


if __name__ == "__main__":
    render_and_emit(FRAME, __file__)
