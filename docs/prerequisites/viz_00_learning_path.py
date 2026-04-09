from __future__ import annotations

from _frameviz_core import Edge, FrameModel, Node, render_and_emit


FRAME = FrameModel(
    doc_id="00_learning_path",
    doc_title="Hyper-Grammar Prerequisites Learning Path",
    purpose="Show chapter dependency order and closure return from chapter 10 back to chapter 01.",
    nodes=[
        Node("P00", "Prerequisites Directory", "container"),
        Node("P01", "01 Grammar Fundamentals", "chapter"),
        Node("P02", "02 Chomsky Hierarchy", "chapter"),
        Node("P03", "03 Hyper Inversion", "chapter"),
        Node("P04", "04 Degrees of Freedom", "chapter"),
        Node("P05", "05 Recursive Now-Frame", "chapter"),
        Node("P06", "06 Expanded Recursive Now-Frame", "chapter"),
        Node("P07", "07 Transframe Ontology", "chapter"),
        Node("P08", "08 Corrective Time Syntropy", "chapter"),
        Node("P09", "09 Mensaclaused Metaretrocausality", "chapter"),
        Node("P10", "10 Necessity Constraint Form", "chapter"),
        Node("P11", "AGENTS/HUMANS/TIME Governance", "reference"),
    ],
    edges=[
        Edge("P00", "P01", "contains"),
        Edge("P00", "P02", "contains"),
        Edge("P00", "P03", "contains"),
        Edge("P00", "P04", "contains"),
        Edge("P00", "P05", "contains"),
        Edge("P00", "P06", "contains"),
        Edge("P00", "P07", "contains"),
        Edge("P00", "P08", "contains"),
        Edge("P00", "P09", "contains"),
        Edge("P00", "P10", "contains"),
        Edge("P01", "P02", "prerequisite for"),
        Edge("P02", "P03", "prerequisite for"),
        Edge("P03", "P04", "prerequisite for"),
        Edge("P04", "P05", "prerequisite for"),
        Edge("P05", "P06", "prerequisite for"),
        Edge("P06", "P07", "prerequisite for"),
        Edge("P07", "P08", "prerequisite for"),
        Edge("P08", "P09", "prerequisite for"),
        Edge("P09", "P10", "computably defines"),
        Edge("P10", "P01", "presupposes (closure return)"),
        Edge("P11", "P03", "formal anchor"),
        Edge("P11", "P10", "closure language anchor"),
        Edge("P11", "P09", "contradiction logging context"),
    ],
    notes=[
        "Dependency chain becomes a closure cycle with 09→10→01.",
        "Chapter 10 is late in computable order and prior in logical grounding.",
        "Governance docs remain source-of-truth for contradictions and refinements.",
    ],
)


if __name__ == "__main__":
    render_and_emit(FRAME, __file__)
