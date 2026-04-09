from __future__ import annotations

from _frameviz_core import Edge, FrameModel, Node, render_and_emit


FRAME = FrameModel(
    doc_id="10_necessity_constraint_form",
    doc_title="Necessity Constraint Form",
    purpose="Visualize dual status of chapter 10: computably extracted from 01–09 yet presupposing 01 as closure return.",
    nodes=[
        Node("C1", "Chapter 01", "chapter"),
        Node("C2", "Chapter 02", "chapter"),
        Node("C3", "Chapter 03", "chapter"),
        Node("C4", "Chapter 04", "chapter"),
        Node("C5", "Chapter 05", "chapter"),
        Node("C6", "Chapter 06", "chapter"),
        Node("C7", "Chapter 07", "chapter"),
        Node("C8", "Chapter 08", "chapter"),
        Node("C9", "Chapter 09", "chapter"),
        Node("C10", "Chapter 10 Necessity Constraint", "constraint"),
        Node("CLS", "System Closure", "criterion"),
    ],
    edges=[
        Edge("C1", "C2", "defines basis for"),
        Edge("C2", "C3", "enables"),
        Edge("C3", "C4", "enables"),
        Edge("C4", "C5", "constrains"),
        Edge("C5", "C6", "expands"),
        Edge("C6", "C7", "grounds"),
        Edge("C7", "C8", "feeds"),
        Edge("C8", "C9", "feeds"),
        Edge("C9", "C10", "computably defines"),
        Edge("C10", "C1", "presupposes"),
        Edge("C10", "CLS", "is defined as"),
        Edge("CLS", "C1", "re-enters system at"),
    ],
    notes=[
        "Chapter 10 is discovered after 01–09 are computably defined.",
        "Chapter 10 simultaneously acts as presupposed condition of chapter 01.",
        "Closure is the system-level necessity constraint.",
    ],
)


if __name__ == "__main__":
    render_and_emit(FRAME, __file__)
