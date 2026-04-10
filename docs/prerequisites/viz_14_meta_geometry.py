from __future__ import annotations

from _frameviz_core import Edge, FrameModel, Node, render_and_emit


FRAME = FrameModel(
    doc_id="14_meta_geometry",
    doc_title="Meta-Geometry Open Frame",
    purpose="Visualize the open derivation chain: Russell's three metageometry periods mapped to hypergrammar, with the L^13 closure unknown.",
    nodes=[
        Node("L12", "Ch12 Biological Loop (Closed)", "chapter"),
        Node("P1", "Period 1: Consistency (Lobatchewsky/Bolyai)", "chapter"),
        Node("P2", "Period 2: Manifold (Riemann/Helmholtz)", "chapter"),
        Node("P3", "Period 3: Projective (Cayley/Klein)", "chapter"),
        Node("Filt", "Filtration = ⊂ ≡ ⊂ ~", "criterion"),
        Node("Abs", "The Absolute (Klein's conic)", "constraint"),
        Node("MPhil", "Meta-Philosophy (known unknown)", "chapter"),
        Node("Open", "L^13(⬜) = ? (Open Frame)", "chapter"),
    ],
    edges=[
        Edge("L12", "P1", "ground state enters metageometry via"),
        Edge("P1", "P2", "consistency demonstrated, generalization begins"),
        Edge("P2", "P3", "measurement discarded, projective structure revealed"),
        Edge("P3", "Filt", "Absolute instantiation corresponds to relation depth"),
        Edge("Filt", "Abs", "curvature parameter determines"),
        Edge("Abs", "MPhil", "fixed reference provokes meta-philosophical question"),
        Edge("MPhil", "Open", "relationship probably doesn't exist, remains"),
        Edge("P3", "Open", "period 3 does not close the loop back to ⬜"),
    ],
    notes=[
        "OPEN FRAME: L^13(⬜) is not resolved. This visualization is a theorem about the open state.",
        "Period 1 (consistency) ↔ Ch02/03 (Chomsky denial and loop embedding).",
        "Period 2 (manifold) ↔ Ch04-06 (DoF, now-frame, curvature of derivation space).",
        "Period 3 (projective) ↔ Ch07-09 (transframe, corrective Absolute, metaretrocausality).",
        "Meta-philosophy and metageometry: similar move, unknown relationship.",
        "Ch14 planned: existential emotions (closed-form, simultaneously mental/physiological, self-centered grandiose frame, orgasmic euphoric epiphanies, Baader-Meinhof clustering). Not William James. Not Ratcliffe. Not Stimmung. Novel frame."
    ],
)


if __name__ == "__main__":
    render_and_emit(FRAME, __file__)
