from __future__ import annotations

from _frameviz_core import Edge, FrameModel, Node, render_and_emit


FRAME = FrameModel(
    doc_id="02_chomsky_hierarchy",
    doc_title="Chomsky Hierarchy",
    purpose="Visualize containment chain, recognizer intuition, and expressivity-versus-proof-cost tradeoff.",
    nodes=[
        Node("T3", "Type-3 Regular", "class"),
        Node("T2", "Type-2 Context-Free", "class"),
        Node("T1", "Type-1 Context-Sensitive", "class"),
        Node("T0", "Type-0 Unrestricted", "class"),
        Node("FA", "Finite Automaton", "machine"),
        Node("PDA", "Pushdown Automaton", "machine"),
        Node("LBA", "Linear-Bounded Automaton", "machine"),
        Node("TM", "Turing Machine", "machine"),
        Node("EXP", "Expressivity", "measure"),
        Node("BUR", "Verification Burden", "measure"),
    ],
    edges=[
        Edge("T3", "T2", "subset of"),
        Edge("T2", "T1", "subset of"),
        Edge("T1", "T0", "subset of"),
        Edge("T3", "FA", "recognized by"),
        Edge("T2", "PDA", "recognized by"),
        Edge("T1", "LBA", "recognized by"),
        Edge("T0", "TM", "recognized by"),
        Edge("T3", "EXP", "lower"),
        Edge("T0", "EXP", "higher"),
        Edge("EXP", "BUR", "typically increases"),
    ],
    notes=[
        "Containment is strict as a modeling heuristic unless proven otherwise.",
        "Higher power usually raises parsing and verification costs.",
    ],
)


if __name__ == "__main__":
    render_and_emit(FRAME, __file__)
