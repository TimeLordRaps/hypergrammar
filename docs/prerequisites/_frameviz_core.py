from __future__ import annotations

from dataclasses import asdict, dataclass
import json
from pathlib import Path
from typing import Sequence


@dataclass(frozen=True)
class Node:
    key: str
    label: str
    kind: str = "concept"


@dataclass(frozen=True)
class Edge:
    source: str
    target: str
    relation: str


@dataclass(frozen=True)
class FrameModel:
    doc_id: str
    doc_title: str
    purpose: str
    nodes: Sequence[Node]
    edges: Sequence[Edge]
    notes: Sequence[str]


def _escape_mermaid(value: str) -> str:
    return value.replace('"', "'")


def to_mermaid(frame: FrameModel) -> str:
    lines = ["flowchart TD"]

    for node in frame.nodes:
        label = _escape_mermaid(node.label)
        lines.append(f"  {node.key}[\"{label}\"]")

    for edge in frame.edges:
        relation = _escape_mermaid(edge.relation)
        lines.append(f"  {edge.source} -- \"{relation}\" --> {edge.target}")

    return "\n".join(lines) + "\n"


def to_ascii(frame: FrameModel) -> str:
    node_label = {node.key: node.label for node in frame.nodes}

    lines = [
        f"{frame.doc_title} [{frame.doc_id}]",
        f"Purpose: {frame.purpose}",
        "",
        "Nodes:",
    ]

    for node in frame.nodes:
        lines.append(f"- {node.key}: {node.label} ({node.kind})")

    lines.append("")
    lines.append("Relations:")

    for edge in frame.edges:
        src = node_label.get(edge.source, edge.source)
        dst = node_label.get(edge.target, edge.target)
        lines.append(f"- {src} --[{edge.relation}]--> {dst}")

    if frame.notes:
        lines.append("")
        lines.append("Notes:")
        for note in frame.notes:
            lines.append(f"- {note}")

    return "\n".join(lines) + "\n"


def to_json_document(frame: FrameModel) -> dict:
    return {
        "doc_id": frame.doc_id,
        "doc_title": frame.doc_title,
        "purpose": frame.purpose,
        "nodes": [asdict(node) for node in frame.nodes],
        "edges": [asdict(edge) for edge in frame.edges],
        "notes": list(frame.notes),
    }


def emit_visualization(frame: FrameModel, script_file: str) -> dict:
    script_path = Path(script_file).resolve()
    base_dir = script_path.parent
    out_dir = base_dir / "visualizations" / frame.doc_id
    out_dir.mkdir(parents=True, exist_ok=True)

    mermaid_path = out_dir / f"{frame.doc_id}_frame.mmd"
    ascii_path = out_dir / f"{frame.doc_id}_frame.txt"
    json_path = out_dir / f"{frame.doc_id}_frame.json"

    mermaid_path.write_text(to_mermaid(frame), encoding="utf-8")
    ascii_path.write_text(to_ascii(frame), encoding="utf-8")
    json_path.write_text(
        json.dumps(to_json_document(frame), indent=2, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )

    return {
        "mermaid": str(mermaid_path),
        "ascii": str(ascii_path),
        "json": str(json_path),
    }


def render_and_emit(frame: FrameModel, script_file: str) -> None:
    outputs = emit_visualization(frame, script_file)
    print(f"[frameviz] {frame.doc_id}: generated visualization artifacts")
    print(f"  - Mermaid: {outputs['mermaid']}")
    print(f"  - ASCII:   {outputs['ascii']}")
    print(f"  - JSON:    {outputs['json']}")
