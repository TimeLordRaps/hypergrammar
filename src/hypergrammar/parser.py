from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from .models import GrammarLayer, HypergrammarSpec, Rule


def _ordered_unique(items: list[str]) -> tuple[str, ...]:
    seen: set[str] = set()
    output: list[str] = []
    for item in items:
        normalized = item.strip()
        if not normalized:
            continue
        if normalized in seen:
            continue
        seen.add(normalized)
        output.append(normalized)
    return tuple(output)


def _parse_rule(raw: dict[str, Any] | str) -> Rule:
    if isinstance(raw, str):
        if "->" not in raw:
            raise ValueError(f"Rule string must include '->': {raw}")
        lhs, rhs = raw.split("->", 1)
        rhs_tokens = rhs.strip().split()
        return Rule(lhs=lhs.strip(), rhs=tuple(rhs_tokens), raw=raw)

    if not isinstance(raw, dict):
        raise TypeError(f"Unsupported rule format: {type(raw)!r}")

    lhs = str(raw.get("lhs", "")).strip()
    if not lhs:
        raise ValueError("Rule dictionary is missing a non-empty 'lhs'")

    rhs_value = raw.get("rhs", [])
    if isinstance(rhs_value, str):
        rhs_tokens = rhs_value.split()
    elif isinstance(rhs_value, list):
        rhs_tokens = [str(token).strip() for token in rhs_value if str(token).strip()]
    else:
        raise TypeError("Rule 'rhs' must be either a string or a list of strings")

    return Rule(lhs=lhs, rhs=tuple(rhs_tokens), raw=raw.get("raw"))


def parse_spec(data: dict[str, Any], *, name_hint: str = "") -> HypergrammarSpec:
    if "layer" not in data:
        raise ValueError("Specification must include 'layer'")

    layer = GrammarLayer.from_value(str(data["layer"]))
    target_layer_raw = data.get("target_layer")
    target_layer = (
        GrammarLayer.from_value(str(target_layer_raw)) if target_layer_raw is not None else None
    )

    rules_raw = data.get("rules", [])
    if not isinstance(rules_raw, list):
        raise TypeError("Specification field 'rules' must be a list")

    rules = tuple(_parse_rule(rule) for rule in rules_raw)

    derivation_chain_raw = data.get("derivation_chain", [])
    if not isinstance(derivation_chain_raw, list):
        raise TypeError("Specification field 'derivation_chain' must be a list")

    metadata = data.get("metadata", {})
    if not isinstance(metadata, dict):
        raise TypeError("Specification field 'metadata' must be a dictionary")

    return HypergrammarSpec(
        name=str(data.get("name") or name_hint or "unnamed_spec"),
        layer=layer,
        universe_symbol=str(data.get("universe_symbol", "U")),
        ground_symbol=str(data.get("ground_symbol", "$")),
        closure_operator=str(data.get("closure_operator", "L")),
        terminals=_ordered_unique([str(t) for t in data.get("terminals", [])]),
        nonterminals=_ordered_unique([str(t) for t in data.get("nonterminals", [])]),
        rules=rules,
        derivation_chain=tuple(str(term).strip() for term in derivation_chain_raw if str(term).strip()),
        target_layer=target_layer,
        metadata=metadata,
    )


def _load_hg(path: Path) -> HypergrammarSpec:
    chain: list[str] = []
    for raw_line in path.read_text(encoding="utf-8").splitlines():
        line = raw_line.split("--", 1)[0].strip()
        if not line:
            continue
        chain.append(line)

    return HypergrammarSpec(
        name=path.stem,
        layer=GrammarLayer.GRAMMAR,
        derivation_chain=tuple(chain),
    )


def load_spec(source: str | Path | dict[str, Any] | HypergrammarSpec) -> HypergrammarSpec:
    if isinstance(source, HypergrammarSpec):
        return source

    if isinstance(source, dict):
        return parse_spec(source)

    path = Path(source)
    if not path.exists():
        raise FileNotFoundError(f"Specification file not found: {path}")

    if path.suffix.lower() == ".hg":
        return _load_hg(path)

    if path.suffix.lower() == ".json":
        payload = json.loads(path.read_text(encoding="utf-8"))
        if not isinstance(payload, dict):
            raise TypeError("JSON spec must be an object at top level")
        return parse_spec(payload, name_hint=path.stem)

    raise ValueError(
        f"Unsupported specification extension '{path.suffix}'. Use .json or .hg"
    )
