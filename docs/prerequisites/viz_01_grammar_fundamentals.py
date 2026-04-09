from __future__ import annotations

from _frameviz_core import Edge, FrameModel, Node, render_and_emit


FRAME = FrameModel(
    doc_id="01_grammar_fundamentals",
    doc_title="Grammar Fundamentals",
    purpose="Visualize how symbols and rules produce derivations, languages, and verification burden.",
    nodes=[
        Node("G", "Grammar G=(V,Σ,P,S)", "definition"),
        Node("V", "Nonterminals V", "symbol-set"),
        Node("S", "Start Symbol S", "symbol"),
        Node("SIG", "Alphabet Σ", "symbol-set"),
        Node("TERM", "Terminals", "symbol-set"),
        Node("PROD", "Productions P", "rule-set"),
        Node("DER", "Derivation", "process"),
        Node("TREE", "Parse Tree", "structure"),
        Node("AMB", "Ambiguity", "diagnostic"),
        Node("LANG", "Language L", "result"),
        Node("VER", "Verification Effort", "outcome"),
    ],
    edges=[
        Edge("G", "V", "contains"),
        Edge("G", "SIG", "contains"),
        Edge("G", "PROD", "contains"),
        Edge("G", "S", "contains"),
        Edge("SIG", "TERM", "supports terminal symbols"),
        Edge("V", "PROD", "rewritten by"),
        Edge("PROD", "DER", "drives"),
        Edge("S", "DER", "starting point"),
        Edge("DER", "TREE", "induces"),
        Edge("DER", "LANG", "generates members of"),
        Edge("TREE", "AMB", "may reveal"),
        Edge("AMB", "VER", "increases complexity of"),
    ],
    notes=[
        "Grammar is a finite generative machine, not an explicit sentence list.",
        "Ambiguity is structural, not merely stylistic.",
    ],
)


if __name__ == "__main__":
    render_and_emit(FRAME, __file__)
