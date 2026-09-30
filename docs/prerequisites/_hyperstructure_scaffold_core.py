from __future__ import annotations

from dataclasses import asdict, dataclass
import hashlib
import json
from pathlib import Path
from typing import Any, Sequence


@dataclass(frozen=True)
class HyperNode:
    key: str
    label: str
    kind: str


@dataclass(frozen=True)
class HyperEdge:
    source: str
    target: str
    relation: str


@dataclass(frozen=True)
class HyperStructure:
    chapter_id: str
    chapter_title: str
    chapter_number: int
    previous_chapter_id: str | None
    previous_signature: str
    deterministic_seed: str
    constraints: Sequence[str]
    nodes: Sequence[HyperNode]
    edges: Sequence[HyperEdge]
    notes: Sequence[str]
    signature: str


def _canonical(obj: Any) -> str:
    return json.dumps(obj, sort_keys=True, separators=(",", ":"), ensure_ascii=False)


def _sha(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def _artifact_paths(base_dir: Path, chapter_id: str) -> tuple[Path, Path, Path]:
    out_dir = base_dir / "scaffolds" / chapter_id
    out_dir.mkdir(parents=True, exist_ok=True)
    return (
        out_dir / f"{chapter_id}_hyperstructure.json",
        out_dir / f"{chapter_id}_hyperstructure.txt",
        out_dir / f"{chapter_id}_hyperstructure.mmd",
    )


def _find_previous_signature(base_dir: Path, chapter_id: str) -> str | None:
    scaffold_json = (
        base_dir / "scaffolds" / chapter_id / f"{chapter_id}_hyperstructure.json"
    )
    if scaffold_json.exists():
        obj = json.loads(scaffold_json.read_text(encoding="utf-8"))
        sig = obj.get("signature")
        if isinstance(sig, str) and sig:
            return sig

    viz_json = (
        base_dir / "visualizations" / chapter_id / f"{chapter_id}_frame.json"
    )
    if viz_json.exists():
        payload = json.loads(viz_json.read_text(encoding="utf-8"))
        return _sha(_canonical(payload))

    return None


def _mermaid(nodes: Sequence[HyperNode], edges: Sequence[HyperEdge]) -> str:
    lines = ["flowchart TD"]
    for node in nodes:
        label = node.label.replace('"', "'")
        lines.append(f"  {node.key}[\"{label}\"]")
    for edge in edges:
        rel = edge.relation.replace('"', "'")
        lines.append(f"  {edge.source} -- \"{rel}\" --> {edge.target}")
    return "\n".join(lines) + "\n"


def _ascii(structure: HyperStructure) -> str:
    lines = [
        f"{structure.chapter_title} [{structure.chapter_id}]",
        f"Previous: {structure.previous_chapter_id or 'none'}",
        f"Previous signature: {structure.previous_signature}",
        f"Deterministic seed: {structure.deterministic_seed}",
        f"Signature: {structure.signature}",
        "",
        "Constraints:",
    ]
    lines.extend(f"- {c}" for c in structure.constraints)
    lines.append("")
    lines.append("Nodes:")
    lines.extend(f"- {n.key}: {n.label} ({n.kind})" for n in structure.nodes)
    lines.append("")
    lines.append("Edges:")
    lines.extend(
        f"- {e.source} --[{e.relation}]--> {e.target}" for e in structure.edges
    )
    if structure.notes:
        lines.append("")
        lines.append("Notes:")
        lines.extend(f"- {n}" for n in structure.notes)
    return "\n".join(lines) + "\n"


def build_hyperstructure(
    *,
    chapter_id: str,
    chapter_title: str,
    chapter_number: int,
    previous_chapter_id: str | None,
    constraints: Sequence[str],
    notes: Sequence[str],
    script_file: str,
) -> HyperStructure:
    base_dir = Path(script_file).resolve().parent

    previous_signature = "GENESIS"
    if previous_chapter_id:
        found = _find_previous_signature(base_dir, previous_chapter_id)
        if not found:
            raise FileNotFoundError(
                f"Could not resolve previous signature for '{previous_chapter_id}'. "
                "Run prerequisite visualizations and prior scaffolds first."
            )
        previous_signature = found

    deterministic_seed = _sha(
        _canonical(
            {
                "chapter_id": chapter_id,
                "chapter_number": chapter_number,
                "previous_signature": previous_signature,
                "constraints": list(constraints),
            }
        )
    )

    nodes = [
        HyperNode("H0", f"{chapter_id} hyperstructure", "chapter"),
        HyperNode("H1", f"deterministic seed {deterministic_seed[:12]}", "seed"),
        HyperNode("H2", f"inherits {previous_signature[:12]}", "link"),
        HyperNode("H3", "constraint manifold", "constraint"),
        HyperNode("H4", "future scaffold anchor", "anchor"),
    ]

    edges = [
        HyperEdge("H2", "H0", "grounds"),
        HyperEdge("H1", "H0", "deterministically instantiates"),
        HyperEdge("H0", "H3", "encodes"),
        HyperEdge("H3", "H4", "provides coherent links for"),
    ]

    payload = {
        "chapter_id": chapter_id,
        "chapter_title": chapter_title,
        "chapter_number": chapter_number,
        "previous_chapter_id": previous_chapter_id,
        "previous_signature": previous_signature,
        "deterministic_seed": deterministic_seed,
        "constraints": list(constraints),
        "nodes": [asdict(n) for n in nodes],
        "edges": [asdict(e) for e in edges],
        "notes": list(notes),
    }

    signature = _sha(_canonical(payload))

    return HyperStructure(
        chapter_id=chapter_id,
        chapter_title=chapter_title,
        chapter_number=chapter_number,
        previous_chapter_id=previous_chapter_id,
        previous_signature=previous_signature,
        deterministic_seed=deterministic_seed,
        constraints=constraints,
        nodes=nodes,
        edges=edges,
        notes=notes,
        signature=signature,
    )


def emit_hyperstructure(structure: HyperStructure, script_file: str) -> dict[str, str]:
    base_dir = Path(script_file).resolve().parent
    json_path, txt_path, mmd_path = _artifact_paths(base_dir, structure.chapter_id)

    payload = {
        "chapter_id": structure.chapter_id,
        "chapter_title": structure.chapter_title,
        "chapter_number": structure.chapter_number,
        "previous_chapter_id": structure.previous_chapter_id,
        "previous_signature": structure.previous_signature,
        "deterministic_seed": structure.deterministic_seed,
        "constraints": list(structure.constraints),
        "nodes": [asdict(n) for n in structure.nodes],
        "edges": [asdict(e) for e in structure.edges],
        "notes": list(structure.notes),
        "signature": structure.signature,
    }

    json_path.write_text(
        json.dumps(payload, indent=2, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )
    txt_path.write_text(_ascii(structure), encoding="utf-8")
    mmd_path.write_text(_mermaid(structure.nodes, structure.edges), encoding="utf-8")

    return {
        "json": str(json_path),
        "txt": str(txt_path),
        "mmd": str(mmd_path),
    }


def build_and_emit(
    *,
    chapter_id: str,
    chapter_title: str,
    chapter_number: int,
    previous_chapter_id: str | None,
    constraints: Sequence[str],
    notes: Sequence[str],
    script_file: str,
) -> None:
    structure = build_hyperstructure(
        chapter_id=chapter_id,
        chapter_title=chapter_title,
        chapter_number=chapter_number,
        previous_chapter_id=previous_chapter_id,
        constraints=constraints,
        notes=notes,
        script_file=script_file,
    )
    outputs = emit_hyperstructure(structure, script_file)

    print(f"[scaffold] {structure.chapter_id}: deterministic hyperstructure emitted")
    print(f"  - JSON: {outputs['json']}")
    print(f"  - TXT:  {outputs['txt']}")
    print(f"  - MMD:  {outputs['mmd']}")
    print(f"  - signature: {structure.signature}")
