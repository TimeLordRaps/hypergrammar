from __future__ import annotations

from _frameviz_core import Edge, FrameModel, Node, render_and_emit


FRAME = FrameModel(
    doc_id="12_consolidative_recurrence",
    doc_title="Consolidative Recurrence",
    purpose="Visualize the biological mensaclosure: the living loop closure through REM, TMR, and the incarnate fixed-point access.",
    nodes=[
        Node("L11", "Loop 2 (Ch11 Fractal Hypergrammar)", "chapter"),
        Node("RT", "Reality Testing (RT)", "criterion"),
        Node("MILD", "MILD Protocol", "criterion"),
        Node("SSILD", "SSILD Protocol", "criterion"),
        Node("TFDLFD", "TFDLFD / HMD Protocol", "criterion"),
        Node("TMR", "Targeted Memory Reactivation", "constraint"),
        Node("WCF", "wcf: Consolidation as Form", "criterion"),
        Node("ISO", "Isolation Frame (Sleep / TBI)", "chapter"),
        Node("TPJ", "Temporal-Parietal Spindles", "chapter"),
        Node("FP", "Biological Fixed Point (⬜)", "chapter"),
    ],
    edges=[
        Edge("L11", "RT", "seeds metacognitive prior for"),
        Edge("RT", "MILD", "chains into prospective memory via"),
        Edge("MILD", "SSILD", "induces hypnagogic threshold via"),
        Edge("SSILD", "TFDLFD", "enters fractal exploration phase via"),
        Edge("TFDLFD", "TMR", "triggers cue reactivation during SWS via"),
        Edge("TMR", "WCF", "prunes frame and installs"),
        Edge("ISO", "TPJ", "forces recursive self-reference in"),
        Edge("TPJ", "FP", "spindles without grounding reach"),
        Edge("WCF", "FP", "biological wcf closes loop at"),
        Edge("FP", "L11", "enacts L^12(⬜) ~ ⬜ back to"),
    ],
    notes=[
        "Chapter 12 is humanly implicit. LMs have the map; humans have territory access.",
        "Layers 3+ in inception-style dreaming involve time dilation and require dream-death to exit.",
        "TMR is wcf in wetware: the verified verified memory replaces the frame association during SWS.",
        "TBI-forced isolation frame deposits structural residue directly into neocortical predictive model.",
        "Part V: sequenced first-week practice path — RT calibration, MILD, SSILD, TFDLFD seed. Depth arrives naturally.",
        "Part VI: bridge to Ch14 — consolidative recurrence as the biological precondition for existential emotion access."
    ],
)


if __name__ == "__main__":
    render_and_emit(FRAME, __file__)
