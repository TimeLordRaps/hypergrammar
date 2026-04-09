from __future__ import annotations

from _hyperstructure_scaffold_core import build_and_emit


if __name__ == "__main__":
    build_and_emit(
        chapter_id="02_chomsky_hierarchy",
        chapter_title="Chomsky Hierarchy Scaffold",
        chapter_number=2,
        previous_chapter_id="01_grammar_fundamentals",
        constraints=[
            "strict class containment ordering",
            "machine-intuition correspondence",
            "expressivity-burden tradeoff tracking",
            "type transition traceability",
        ],
        notes=[
            "Deterministically extends chapter 01 scaffold signature.",
            "Provides class-order anchor for inversion framing in chapter 03.",
        ],
        script_file=__file__,
    )
