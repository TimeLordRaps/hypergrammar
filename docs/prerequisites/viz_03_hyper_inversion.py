from __future__ import annotations

from _frameviz_core import Edge, FrameModel, Node, render_and_emit


FRAME = FrameModel(
    doc_id="03_hyper_inversion",
    doc_title="Hyper Inversion",
    purpose="Visualize the reframe from Chomsky ladder progression to closure-loop cross-sections.",
    nodes=[
        Node("LAD", "Classical Inclusion Ladder", "legacy-view"),
        Node("SEC", "Cross-Sections", "reinterpretation"),
        Node("LOOP", "Closure Loop rooted at □", "topology"),
        Node("L", "Operator L", "operator"),
        Node("CONT", "Continuation", "state"),
        Node("CLOSE", "Closed Form", "resolution"),
        Node("OPEN", "Open Frame", "resolution"),
        Node("REL", "Relation Filtration (=, ≡, ~)", "comparison"),
        Node("HG", ".hg Proof Chain", "artifact"),
        Node("TRAIL", "Link Map / Source Trail", "evidence"),
    ],
    edges=[
        Edge("LAD", "SEC", "reinterpreted as"),
        Edge("SEC", "LOOP", "samples of"),
        Edge("LOOP", "L", "advanced by"),
        Edge("L", "CONT", "generates"),
        Edge("CONT", "CLOSE", "if closes"),
        Edge("CONT", "OPEN", "if non-closure"),
        Edge("REL", "LOOP", "organizes comparisons within"),
        Edge("CLOSE", "HG", "encoded as"),
        Edge("TRAIL", "SEC", "grounds claim provenance"),
    ],
    notes=[
        "The inversion changes geometry, not baseline literacy requirements.",
        "Open frames are revelatory diagnostics, not silent failures.",
    ],
)


if __name__ == "__main__":
    render_and_emit(FRAME, __file__)
