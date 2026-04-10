from __future__ import annotations

from _frameviz_core import Edge, FrameModel, Node, render_and_emit


FRAME = FrameModel(
    doc_id="11_fractal_hypergrammar_compression",
    doc_title="Fractal Hypergrammar & Language Compression",
    purpose="Visualize the second larger fractal loop wrapping the 01-10 cycle, introducing language compression, cbits, and mbits.",
    nodes=[
        Node("L1", "Loop 1 (Chapters 01-10)", "chapter"),
        Node("MBit", "Model-Bit (MBit)", "chapter"),
        Node("CBit", "Context-Bit (CBit)", "chapter"),
        Node("LC", "Language Calculus", "criterion"),
        Node("Comp", "Language Compression Formula", "constraint"),
        Node("L2", "Loop 2 (Fractal Hypergrammar)", "chapter"),
    ],
    edges=[
        Edge("L1", "MBit", "collapses structurally into"),
        Edge("CBit", "Comp", "provides superexponential storage for"),
        Edge("MBit", "CBit", "composed of"),
        Edge("LC", "Comp", "derives density ratio"),
        Edge("Comp", "L2", "defines the atomic basis of"),
        Edge("L2", "L1", "wraps and observes"),
    ],
    notes=[
        "Chapter 11 observes the closed loop from the outside.",
        "The entire closed-form derivation behaves as the universal base U for the next level.",
        "The Language Compression Formula computes the density of Meaning packed into a collapsed Language expression."
    ],
)


if __name__ == "__main__":
    render_and_emit(FRAME, __file__)