from __future__ import annotations

import json
from pathlib import Path
import re
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


_METAMATH_LABELLED = {"$f", "$e", "$a", "$p"}
_METAMATH_UNLABELLED = {"$c", "$v", "$d"}


def _tokenize_metamath(text: str) -> list[str]:
    raw_tokens = text.split()
    tokens: list[str] = []
    in_comment = False

    for token in raw_tokens:
        if in_comment:
            if token == "$)":
                in_comment = False
            continue

        if token == "$(":
            in_comment = True
            continue

        tokens.append(token)

    return tokens


def _parse_metamath_statements(tokens: list[str]) -> list[dict[str, Any]]:
    statements: list[dict[str, Any]] = []
    i = 0
    n = len(tokens)

    while i < n:
        token = tokens[i]

        if token in {"${", "$}"}:
            statements.append({"kind": token, "label": None, "body": [], "proof": []})
            i += 1
            continue

        if token in _METAMATH_UNLABELLED:
            kind = token
            i += 1
            body: list[str] = []
            while i < n and tokens[i] != "$.":
                body.append(tokens[i])
                i += 1

            if i >= n:
                raise ValueError(f"Unterminated Metamath statement starting with {kind}")

            i += 1
            statements.append({"kind": kind, "label": None, "body": body, "proof": []})
            continue

        if i + 1 < n and tokens[i + 1] in _METAMATH_LABELLED:
            label = token
            kind = tokens[i + 1]
            i += 2
            body: list[str] = []
            proof: list[str] = []

            if kind == "$p":
                while i < n and tokens[i] != "$=":
                    body.append(tokens[i])
                    i += 1
                if i >= n:
                    raise ValueError(f"Unterminated theorem statement for label {label}")
                i += 1
                while i < n and tokens[i] != "$.":
                    proof.append(tokens[i])
                    i += 1
                if i >= n:
                    raise ValueError(f"Unterminated theorem proof for label {label}")
            else:
                while i < n and tokens[i] != "$.":
                    body.append(tokens[i])
                    i += 1
                if i >= n:
                    raise ValueError(f"Unterminated statement for label {label}")

            i += 1
            statements.append({"kind": kind, "label": label, "body": body, "proof": proof})
            continue

        i += 1

    return statements


def _metamath_line_range_from_path(path: Path) -> tuple[int, int] | None:
    match = re.search(r"(\d+)_(\d+)", path.stem)
    if not match:
        return None
    return int(match.group(1)), int(match.group(2))


def _load_metamath(path: Path) -> HypergrammarSpec:
    text = path.read_text(encoding="utf-8")
    tokens = _tokenize_metamath(text)
    statements = _parse_metamath_statements(tokens)

    kind_to_nonterminal = {
        "$c": "DECL_C",
        "$v": "DECL_V",
        "$d": "DV_D",
        "$f": "HYP_F",
        "$e": "HYP_E",
        "$a": "AX_A",
        "$p": "THM_P",
        "${": "BLOCK_OPEN",
        "$}": "BLOCK_CLOSE",
    }

    statement_counts: dict[str, int] = {}
    observed_nonterminals: list[str] = []
    observed_terminals: set[str] = {
        "LABEL",
        "SYMBOL_SEQ",
        "VAR_SEQ",
        "TYPECODE",
        "VAR",
        "EXPR",
        "PROOF",
        "$.",
        "$=",
        "${",
        "$}",
        "$",
        "U",
        "ε",
    }
    sample_labels: list[str] = []

    for stmt in statements:
        kind = str(stmt["kind"])
        statement_counts[kind] = statement_counts.get(kind, 0) + 1
        observed_terminals.add(kind)
        observed_terminals.update(str(token) for token in stmt["body"])
        observed_terminals.update(str(token) for token in stmt["proof"])

        nonterminal = kind_to_nonterminal.get(kind)
        if nonterminal and nonterminal not in observed_nonterminals:
            observed_nonterminals.append(nonterminal)

        label = stmt.get("label")
        if isinstance(label, str) and label and len(sample_labels) < 25:
            sample_labels.append(label)

    nonterminals: list[str] = ["DB", "STMT"]
    if "BLOCK_OPEN" in observed_nonterminals or "BLOCK_CLOSE" in observed_nonterminals:
        nonterminals.append("BLOCK")
    nonterminals.extend(observed_nonterminals)

    rules: list[Rule] = [
        Rule(lhs="DB", rhs=("STMT", "DB"), raw="DB -> STMT DB"),
        Rule(lhs="DB", rhs=("STMT",), raw="DB -> STMT"),
    ]

    if "BLOCK" in nonterminals:
        rules.append(Rule(lhs="BLOCK", rhs=("${", "STMT", "$}"), raw="BLOCK -> ${ STMT $}"))
        rules.append(Rule(lhs="STMT", rhs=("BLOCK",), raw="STMT -> BLOCK"))

    if "DECL_C" in nonterminals:
        rules.append(Rule(lhs="DECL_C", rhs=("LABEL", "$c", "SYMBOL_SEQ", "$.")))
        rules.append(Rule(lhs="STMT", rhs=("DECL_C",), raw="STMT -> DECL_C"))
    if "DECL_V" in nonterminals:
        rules.append(Rule(lhs="DECL_V", rhs=("LABEL", "$v", "VAR_SEQ", "$.")))
        rules.append(Rule(lhs="STMT", rhs=("DECL_V",), raw="STMT -> DECL_V"))
    if "DV_D" in nonterminals:
        rules.append(Rule(lhs="DV_D", rhs=("LABEL", "$d", "VAR_SEQ", "$.")))
        rules.append(Rule(lhs="STMT", rhs=("DV_D",), raw="STMT -> DV_D"))
    if "HYP_F" in nonterminals:
        rules.append(Rule(lhs="HYP_F", rhs=("LABEL", "$f", "TYPECODE", "VAR", "$.")))
        rules.append(Rule(lhs="STMT", rhs=("HYP_F",), raw="STMT -> HYP_F"))
    if "HYP_E" in nonterminals:
        rules.append(Rule(lhs="HYP_E", rhs=("LABEL", "$e", "EXPR", "$.")))
        rules.append(Rule(lhs="STMT", rhs=("HYP_E",), raw="STMT -> HYP_E"))
    if "AX_A" in nonterminals:
        rules.append(Rule(lhs="AX_A", rhs=("LABEL", "$a", "EXPR", "$.")))
        rules.append(Rule(lhs="STMT", rhs=("AX_A",), raw="STMT -> AX_A"))
    if "THM_P" in nonterminals:
        rules.append(Rule(lhs="THM_P", rhs=("LABEL", "$p", "EXPR", "$=", "PROOF", "$.")))
        rules.append(Rule(lhs="STMT", rhs=("THM_P",), raw="STMT -> THM_P"))

    line_range = _metamath_line_range_from_path(path)
    source_url = "https://raw.githubusercontent.com/metamath/set.mm/develop/set.mm"
    source_blob_url = "https://github.com/metamath/set.mm/blob/develop/set.mm"

    metadata: dict[str, Any] = {
        "source_trail": {
            "source_url": source_url,
            "source_blob_url": source_blob_url,
            "slice_file": str(path).replace("\\", "/"),
            "line_range": list(line_range) if line_range else None,
            "statement_counts": statement_counts,
            "sample_labels": sample_labels,
            "accountability": {
                "parse_mode": "real_metamath_slice",
                "comment_handling": "ignore tokens between $( and $)",
                "statement_extraction": "supports $c $v $d $f $e $a $p ${ $}",
            },
        },
        "reasoning": {
            "1_source": source_url,
            "2_slice": str(path).replace("\\", "/"),
            "3_parse": "tokenize -> strip comments -> extract statements",
            "4_schema": "emit metagrammar spec for hypergrammar constraints",
        },
    }

    return HypergrammarSpec(
        name=f"metamath_slice_{path.stem}",
        layer=GrammarLayer.METAGRAMMAR,
        target_layer=GrammarLayer.GRAMMAR,
        terminals=tuple(sorted(observed_terminals)),
        nonterminals=tuple(_ordered_unique(nonterminals)),
        rules=tuple(rules),
        derivation_chain=("$", "L($)", "L(L($))"),
        metadata=metadata,
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

    if path.suffix.lower() == ".mm":
        return _load_metamath(path)

    if path.suffix.lower() == ".json":
        payload = json.loads(path.read_text(encoding="utf-8"))
        if not isinstance(payload, dict):
            raise TypeError("JSON spec must be an object at top level")
        return parse_spec(payload, name_hint=path.stem)

    raise ValueError(
        f"Unsupported specification extension '{path.suffix}'. Use .json, .hg, or .mm"
    )
