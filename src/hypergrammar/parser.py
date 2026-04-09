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
_METAMATH_REFERENCE_LABEL_KINDS = {"$a", "$p", "$f", "$e"}
_METAMATH_HYPOTHESIS_LABEL_KINDS = {"$f", "$e"}
_METAMATH_METADATA_SAMPLE_LIMIT = 25


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


def _metamath_line_range_url(source_blob_url: str, line_range: tuple[int, int] | None) -> str | None:
    if line_range is None:
        return None

    start, end = line_range
    if start == end:
        return f"{source_blob_url}#L{start}"
    return f"{source_blob_url}#L{start}-L{end}"


def _split_compressed_proof_tokens(proof_tokens: list[str]) -> dict[str, Any] | None:
    if not proof_tokens or proof_tokens[0] != "(":
        return None

    close_index = -1
    for idx in range(1, len(proof_tokens)):
        if proof_tokens[idx] == ")":
            close_index = idx
            break

    if close_index == -1:
        return {
            "well_formed": False,
            "reason": "missing_closing_paren_in_compressed_segment",
            "referenced_labels": [],
            "payload_tokens": [],
        }

    referenced_labels = [str(token) for token in proof_tokens[1:close_index]]
    payload_tokens = [str(token) for token in proof_tokens[close_index + 1 :]]
    payload_missing = len(payload_tokens) == 0
    payload_has_parens = any("(" in token or ")" in token for token in payload_tokens)

    well_formed = not payload_missing and not payload_has_parens
    reason: str | None = None
    if payload_missing:
        reason = "compressed_segment_missing_payload"
    elif payload_has_parens:
        reason = "compressed_payload_contains_parenthesis_tokens"

    return {
        "well_formed": well_formed,
        "reason": reason,
        "referenced_labels": referenced_labels,
        "payload_tokens": payload_tokens,
    }


def _decode_compressed_payload(payload_tokens: list[str]) -> dict[str, Any]:
    operations: list[dict[str, Any]] = []
    errors: list[str] = []
    invalid_characters: list[str] = []
    accumulator = 0
    position = 0

    for token in payload_tokens:
        for char in token:
            position += 1
            if "U" <= char <= "Y":
                accumulator = accumulator * 5 + (ord(char) - ord("U") + 1)
                continue

            if "A" <= char <= "T":
                index = accumulator * 20 + (ord(char) - ord("A") + 1)
                accumulator = 0
                operations.append(
                    {
                        "op": "index",
                        "index": index,
                        "symbol": char,
                        "position": position,
                    }
                )
                continue

            if char == "Z":
                if accumulator != 0:
                    errors.append("dangling_base5_prefix_before_save_marker")
                    accumulator = 0
                operations.append(
                    {
                        "op": "save",
                        "symbol": char,
                        "position": position,
                    }
                )
                continue

            if char == "?":
                if accumulator != 0:
                    errors.append("dangling_base5_prefix_before_placeholder")
                    accumulator = 0
                operations.append(
                    {
                        "op": "placeholder",
                        "symbol": char,
                        "position": position,
                    }
                )
                continue

            invalid_characters.append(char)
            errors.append(f"invalid_payload_character:{char}")
            accumulator = 0

    if accumulator != 0:
        errors.append("dangling_base5_prefix_at_end")

    index_operations = [op for op in operations if op.get("op") == "index"]
    save_operations = [op for op in operations if op.get("op") == "save"]
    placeholder_operations = [op for op in operations if op.get("op") == "placeholder"]

    return {
        "operations": operations,
        "decoded_indices": [int(op["index"]) for op in index_operations],
        "decoded_index_count": len(index_operations),
        "save_marker_count": len(save_operations),
        "placeholder_count": len(placeholder_operations),
        "invalid_characters": invalid_characters,
        "error_count": len(errors),
        "errors": errors,
        "well_formed": len(errors) == 0,
    }


def _extract_proof_reference_labels(proof_tokens: list[str]) -> dict[str, Any]:
    if not proof_tokens:
        return {
            "proof_form": "missing",
            "well_formed": False,
            "reference_source": "none",
            "referenced_labels": [],
            "placeholder_reference_count": 0,
            "reason": "empty_proof_segment",
        }

    compressed_parts = _split_compressed_proof_tokens(proof_tokens)
    if compressed_parts is not None:
        result: dict[str, Any] = {
            "proof_form": "compressed",
            "well_formed": bool(compressed_parts.get("well_formed", False)),
            "reference_source": "compressed_label_list",
            "referenced_labels": [
                str(token) for token in compressed_parts.get("referenced_labels", [])
            ],
            "placeholder_reference_count": 0,
            "compressed_payload_token_count": len(compressed_parts.get("payload_tokens", [])),
        }

        reason = compressed_parts.get("reason")
        if isinstance(reason, str) and reason:
            result["reason"] = reason

        return result

    raw_refs = [str(token) for token in proof_tokens]
    placeholder_count = sum(1 for token in raw_refs if token == "?")
    referenced_labels = [token for token in raw_refs if token != "?"]
    return {
        "proof_form": "uncompressed",
        "well_formed": True,
        "reference_source": "uncompressed_sequence",
        "referenced_labels": referenced_labels,
        "placeholder_reference_count": placeholder_count,
    }


def _analyze_metamath_proof_segments(statements: list[dict[str, Any]]) -> dict[str, Any]:
    theorem_statements = [stmt for stmt in statements if stmt.get("kind") == "$p"]

    compressed_count = 0
    uncompressed_count = 0
    missing_count = 0
    malformed_count = 0
    empty_proof_count = 0
    samples: list[dict[str, Any]] = []
    malformed_samples: list[dict[str, Any]] = []

    for stmt in theorem_statements:
        label = str(stmt.get("label") or "") or None
        assertion_tokens = [str(token) for token in stmt.get("body", [])]
        proof_tokens = [str(token) for token in stmt.get("proof", [])]

        proof_analysis = _extract_proof_reference_labels(proof_tokens)
        proof_form = str(proof_analysis.get("proof_form", "missing"))
        well_formed = bool(proof_analysis.get("well_formed", False))
        referenced_labels = [
            str(token).strip()
            for token in proof_analysis.get("referenced_labels", [])
            if str(token).strip()
        ]
        placeholder_reference_count = int(proof_analysis.get("placeholder_reference_count", 0))

        entry: dict[str, Any] = {
            "label": label,
            "assertion_token_count": len(assertion_tokens),
            "proof_token_count": len(proof_tokens),
            "has_equals_segment": True,
            "proof_form": proof_form,
            "well_formed": well_formed,
            "reference_source": str(proof_analysis.get("reference_source", "unknown")),
            "referenced_labels": referenced_labels,
            "referenced_labels_count": len(referenced_labels),
            "placeholder_reference_count": placeholder_reference_count,
        }

        if proof_form == "missing":
            missing_count += 1
            empty_proof_count += 1
        elif proof_form == "compressed":
            compressed_count += 1
            if "compressed_payload_token_count" in proof_analysis:
                entry["compressed_payload_token_count"] = int(
                    proof_analysis["compressed_payload_token_count"]
                )
        elif proof_form == "uncompressed":
            uncompressed_count += 1

        reason = proof_analysis.get("reason")
        if isinstance(reason, str) and reason:
            entry["reason"] = reason

        if not well_formed:
            malformed_count += 1
            if reason == "compressed_segment_missing_payload":
                empty_proof_count += 1

        if len(samples) < _METAMATH_METADATA_SAMPLE_LIMIT:
            samples.append(entry)
        if not well_formed and len(malformed_samples) < _METAMATH_METADATA_SAMPLE_LIMIT:
            malformed_samples.append(entry)

    theorem_count = len(theorem_statements)
    return {
        "theorem_count": theorem_count,
        "with_equals_segment_count": theorem_count,
        "compressed_count": compressed_count,
        "uncompressed_count": uncompressed_count,
        "missing_count": missing_count,
        "malformed_count": malformed_count,
        "empty_proof_count": empty_proof_count,
        "all_well_formed": malformed_count == 0,
        "samples": samples,
        "malformed_samples": malformed_samples,
    }


def _analyze_theorem_label_linkage(statements: list[dict[str, Any]]) -> dict[str, Any]:
    scoped_labels: dict[str, str] = {}
    labels_by_kind: dict[str, int] = {kind: 0 for kind in sorted(_METAMATH_REFERENCE_LABEL_KINDS)}

    theorem_count = 0
    reference_count = 0
    resolved_reference_count = 0
    unresolved_reference_count = 0
    placeholder_reference_count = 0
    unresolved_labels: set[str] = set()

    samples: list[dict[str, Any]] = []
    unresolved_samples: list[dict[str, Any]] = []

    for stmt in statements:
        kind = str(stmt.get("kind"))
        label_raw = stmt.get("label")
        label = str(label_raw).strip() if isinstance(label_raw, str) else ""

        if kind == "$p":
            theorem_count += 1
            proof_tokens = [str(token) for token in stmt.get("proof", [])]
            proof_analysis = _extract_proof_reference_labels(proof_tokens)

            referenced_labels = [
                str(token).strip()
                for token in proof_analysis.get("referenced_labels", [])
                if str(token).strip()
            ]
            referenced_labels_unique = list(dict.fromkeys(referenced_labels))
            resolved_refs = [token for token in referenced_labels_unique if token in scoped_labels]
            unresolved_refs = [token for token in referenced_labels_unique if token not in scoped_labels]

            resolved_kind_counts: dict[str, int] = {}
            for token in resolved_refs:
                token_kind = scoped_labels[token]
                resolved_kind_counts[token_kind] = resolved_kind_counts.get(token_kind, 0) + 1

            ref_count = len(referenced_labels_unique)
            unresolved_count = len(unresolved_refs)
            placeholder_count = int(proof_analysis.get("placeholder_reference_count", 0))

            reference_count += ref_count
            resolved_reference_count += len(resolved_refs)
            unresolved_reference_count += unresolved_count
            placeholder_reference_count += placeholder_count
            unresolved_labels.update(unresolved_refs)

            entry: dict[str, Any] = {
                "label": label or None,
                "proof_form": str(proof_analysis.get("proof_form", "unknown")),
                "well_formed": bool(proof_analysis.get("well_formed", False)),
                "reference_source": str(proof_analysis.get("reference_source", "unknown")),
                "in_scope_label_count": len(scoped_labels),
                "referenced_labels": referenced_labels_unique,
                "resolved_references": resolved_refs,
                "unresolved_references": unresolved_refs,
                "resolved_reference_kinds": resolved_kind_counts,
                "reference_count": ref_count,
                "unresolved_reference_count": unresolved_count,
                "placeholder_reference_count": placeholder_count,
            }

            if "reason" in proof_analysis:
                entry["reason"] = str(proof_analysis["reason"])

            if len(samples) < _METAMATH_METADATA_SAMPLE_LIMIT:
                samples.append(entry)
            if unresolved_refs and len(unresolved_samples) < _METAMATH_METADATA_SAMPLE_LIMIT:
                unresolved_samples.append(entry)

        if label and kind in _METAMATH_REFERENCE_LABEL_KINDS and label not in scoped_labels:
            scoped_labels[label] = kind
            labels_by_kind[kind] = labels_by_kind.get(kind, 0) + 1

    label_scope_sample = [
        {"label": scoped_label, "kind": scoped_kind}
        for scoped_label, scoped_kind in list(scoped_labels.items())[:_METAMATH_METADATA_SAMPLE_LIMIT]
    ]

    return {
        "theorem_count": theorem_count,
        "available_label_count": len(scoped_labels),
        "available_labels_by_kind": labels_by_kind,
        "reference_count": reference_count,
        "resolved_reference_count": resolved_reference_count,
        "unresolved_reference_count": unresolved_reference_count,
        "placeholder_reference_count": placeholder_reference_count,
        "all_resolved": unresolved_reference_count == 0,
        "unresolved_labels": sorted(unresolved_labels)[:_METAMATH_METADATA_SAMPLE_LIMIT],
        "label_scope_sample": label_scope_sample,
        "samples": samples,
        "unresolved_samples": unresolved_samples,
    }


def _new_metamath_scope() -> dict[str, Any]:
    return {
        "v": set(),
        "f": [],
        "e": [],
        "labels": {},
    }


def _active_scope_snapshot(scope_stack: list[dict[str, Any]]) -> dict[str, Any]:
    active_vars: set[str] = set()
    active_f_entries: list[dict[str, Any]] = []
    active_e_entries: list[dict[str, Any]] = []
    active_labels: dict[str, str] = {}

    for scope in scope_stack:
        active_vars.update(str(token) for token in scope.get("v", set()))
        active_f_entries.extend(scope.get("f", []))
        active_e_entries.extend(scope.get("e", []))
        labels = scope.get("labels", {})
        for label, kind in labels.items():
            active_labels[str(label)] = str(kind)

    return {
        "v": active_vars,
        "f_entries": active_f_entries,
        "e_entries": active_e_entries,
        "labels": active_labels,
    }


def _build_mandatory_hypothesis_labels(
    theorem_body_tokens: list[str],
    active_snapshot: dict[str, Any],
) -> list[str]:
    active_vars = set(str(token) for token in active_snapshot.get("v", set()))
    active_f_entries = [entry for entry in active_snapshot.get("f_entries", []) if isinstance(entry, dict)]
    active_e_entries = [entry for entry in active_snapshot.get("e_entries", []) if isinstance(entry, dict)]

    used_tokens = set(str(token) for token in theorem_body_tokens)
    for entry in active_e_entries:
        used_tokens.update(str(token) for token in entry.get("body", []))
    used_vars = {token for token in used_tokens if token in active_vars}

    mandatory_f_labels: list[str] = []
    seen_vars: set[str] = set()
    for entry in active_f_entries:
        label = str(entry.get("label") or "").strip()
        var = str(entry.get("var") or "").strip()
        if not label or not var:
            continue
        if var in used_vars and var not in seen_vars:
            mandatory_f_labels.append(label)
            seen_vars.add(var)

    mandatory_e_labels: list[str] = []
    for entry in active_e_entries:
        label = str(entry.get("label") or "").strip()
        if label:
            mandatory_e_labels.append(label)

    return mandatory_f_labels + mandatory_e_labels


def _analyze_compressed_payload_decoding(statements: list[dict[str, Any]]) -> dict[str, Any]:
    scope_stack: list[dict[str, Any]] = [_new_metamath_scope()]

    theorem_count = 0
    compressed_theorem_count = 0
    invalid_payload_count = 0
    out_of_range_index_count = 0
    unresolved_label_list_reference_count = 0
    save_without_prior_step_count = 0
    placeholder_reference_count = 0
    malformed_payload_count = 0

    samples: list[dict[str, Any]] = []
    invalid_samples: list[dict[str, Any]] = []

    for stmt in statements:
        kind = str(stmt.get("kind"))
        label = str(stmt.get("label") or "").strip()
        body_tokens = [str(token) for token in stmt.get("body", [])]
        proof_tokens = [str(token) for token in stmt.get("proof", [])]

        if kind == "${":
            scope_stack.append(_new_metamath_scope())
            continue
        if kind == "$}":
            if len(scope_stack) > 1:
                scope_stack.pop()
            continue

        if kind == "$v":
            scope_stack[-1]["v"].update(body_tokens)
            continue

        if kind == "$f":
            if label:
                var = body_tokens[-1] if body_tokens else ""
                scope_stack[-1]["f"].append({"label": label, "var": var, "body": body_tokens})
                scope_stack[-1]["labels"][label] = "$f"
            continue

        if kind == "$e":
            if label:
                scope_stack[-1]["e"].append({"label": label, "body": body_tokens})
                scope_stack[-1]["labels"][label] = "$e"
            continue

        if kind == "$a":
            if label:
                scope_stack[-1]["labels"][label] = "$a"
            continue

        if kind == "$p":
            theorem_count += 1

            active_snapshot = _active_scope_snapshot(scope_stack)
            active_labels = {
                lbl: lbl_kind
                for lbl, lbl_kind in active_snapshot.get("labels", {}).items()
                if lbl_kind in _METAMATH_REFERENCE_LABEL_KINDS
            }

            compressed_parts = _split_compressed_proof_tokens(proof_tokens)
            if compressed_parts is not None:
                compressed_theorem_count += 1

                label_list = [
                    str(token).strip()
                    for token in compressed_parts.get("referenced_labels", [])
                    if str(token).strip()
                ]
                unresolved_label_list_refs = [
                    token for token in label_list if token not in active_labels
                ]
                unresolved_label_list_reference_count += len(unresolved_label_list_refs)

                mandatory_hyp_labels = _build_mandatory_hypothesis_labels(body_tokens, active_snapshot)
                expanded_labels = mandatory_hyp_labels + label_list
                expanded_label_count = len(expanded_labels)

                payload_tokens = [
                    str(token)
                    for token in compressed_parts.get("payload_tokens", [])
                    if str(token)
                ]
                payload_decode = _decode_compressed_payload(payload_tokens)

                out_of_range_indices: list[dict[str, Any]] = []
                save_without_prior_step = 0
                saved_steps = 0
                decoded_steps = 0
                for operation in payload_decode.get("operations", []):
                    op_kind = str(operation.get("op"))
                    if op_kind == "index":
                        decoded_steps += 1
                        index = int(operation.get("index", 0))
                        max_index = expanded_label_count + saved_steps
                        if index < 1 or index > max_index:
                            out_of_range_indices.append(
                                {
                                    "index": index,
                                    "max_index": max_index,
                                    "symbol": operation.get("symbol"),
                                    "position": operation.get("position"),
                                }
                            )
                    elif op_kind == "save":
                        if decoded_steps == 0:
                            save_without_prior_step += 1
                        else:
                            saved_steps += 1

                payload_well_formed = bool(compressed_parts.get("well_formed", False)) and bool(
                    payload_decode.get("well_formed", False)
                )
                malformed = not payload_well_formed
                if malformed:
                    malformed_payload_count += 1

                out_of_range_index_count += len(out_of_range_indices)
                save_without_prior_step_count += save_without_prior_step
                placeholder_count = int(payload_decode.get("placeholder_count", 0))
                placeholder_reference_count += placeholder_count

                valid = (
                    payload_well_formed
                    and len(unresolved_label_list_refs) == 0
                    and len(out_of_range_indices) == 0
                    and save_without_prior_step == 0
                    and placeholder_count == 0
                )
                if not valid:
                    invalid_payload_count += 1

                entry: dict[str, Any] = {
                    "label": label or None,
                    "compressed": True,
                    "valid": valid,
                    "payload_well_formed": payload_well_formed,
                    "expanded_label_count": expanded_label_count,
                    "mandatory_hypothesis_count": len(mandatory_hyp_labels),
                    "compressed_label_list_count": len(label_list),
                    "decoded_index_count": int(payload_decode.get("decoded_index_count", 0)),
                    "save_marker_count": int(payload_decode.get("save_marker_count", 0)),
                    "placeholder_reference_count": placeholder_count,
                    "unresolved_label_list_references": unresolved_label_list_refs,
                    "out_of_range_indices": out_of_range_indices,
                    "save_without_prior_step_count": save_without_prior_step,
                    "decode_errors": payload_decode.get("errors", []),
                }

                reason = compressed_parts.get("reason")
                if isinstance(reason, str) and reason:
                    entry["reason"] = reason

                if len(mandatory_hyp_labels) > 0:
                    entry["mandatory_hypothesis_sample"] = mandatory_hyp_labels[
                        :_METAMATH_METADATA_SAMPLE_LIMIT
                    ]
                if len(label_list) > 0:
                    entry["compressed_label_list_sample"] = label_list[
                        :_METAMATH_METADATA_SAMPLE_LIMIT
                    ]
                if len(expanded_labels) > 0:
                    entry["expanded_label_sample"] = expanded_labels[
                        :_METAMATH_METADATA_SAMPLE_LIMIT
                    ]

                if len(samples) < _METAMATH_METADATA_SAMPLE_LIMIT:
                    samples.append(entry)
                if not valid and len(invalid_samples) < _METAMATH_METADATA_SAMPLE_LIMIT:
                    invalid_samples.append(entry)

            if label:
                scope_stack[-1]["labels"][label] = "$p"
            continue

        # Other statement kinds do not affect this analysis directly.

    return {
        "theorem_count": theorem_count,
        "compressed_theorem_count": compressed_theorem_count,
        "invalid_payload_count": invalid_payload_count,
        "malformed_payload_count": malformed_payload_count,
        "out_of_range_index_count": out_of_range_index_count,
        "unresolved_label_list_reference_count": unresolved_label_list_reference_count,
        "save_without_prior_step_count": save_without_prior_step_count,
        "placeholder_reference_count": placeholder_reference_count,
        "all_valid": (
            compressed_theorem_count == 0
            or (
                invalid_payload_count == 0
                and malformed_payload_count == 0
                and out_of_range_index_count == 0
                and unresolved_label_list_reference_count == 0
                and save_without_prior_step_count == 0
                and placeholder_reference_count == 0
            )
        ),
        "samples": samples,
        "invalid_samples": invalid_samples,
    }


def _apply_substitution(tokens: list[str], substitution: dict[str, tuple[str, ...]]) -> list[str]:
    expanded: list[str] = []
    for token in tokens:
        if token in substitution:
            expanded.extend(substitution[token])
        else:
            expanded.append(token)
    return expanded


def _analyze_stack_level_proof_execution(statements: list[dict[str, Any]]) -> dict[str, Any]:
    scope_stack: list[dict[str, Any]] = [_new_metamath_scope()]
    definitions: dict[str, dict[str, Any]] = {}

    theorem_count = 0
    executed_theorem_count = 0
    invalid_theorem_count = 0

    unknown_label_count = 0
    stack_underflow_count = 0
    substitution_conflict_count = 0
    floating_type_mismatch_count = 0
    essential_hypothesis_mismatch_count = 0
    saved_reference_out_of_range_count = 0
    placeholder_operation_count = 0
    decode_error_count = 0
    final_stack_shape_mismatch_count = 0
    final_result_mismatch_count = 0

    samples: list[dict[str, Any]] = []
    invalid_samples: list[dict[str, Any]] = []

    for stmt in statements:
        kind = str(stmt.get("kind"))
        label = str(stmt.get("label") or "").strip()
        body_tokens = [str(token) for token in stmt.get("body", [])]
        proof_tokens = [str(token) for token in stmt.get("proof", [])]

        if kind == "${":
            scope_stack.append(_new_metamath_scope())
            continue
        if kind == "$}":
            if len(scope_stack) > 1:
                scope_stack.pop()
            continue

        if kind == "$v":
            scope_stack[-1]["v"].update(body_tokens)
            continue

        if kind == "$f":
            if label:
                definition = {
                    "kind": "$f",
                    "label": label,
                    "body": body_tokens,
                    "mandatory_hypotheses": [],
                }
                definitions[label] = definition
                scope_stack[-1]["f"].append({"label": label, "var": (body_tokens[-1] if body_tokens else "")})
                scope_stack[-1]["labels"][label] = "$f"
            continue

        if kind == "$e":
            if label:
                definition = {
                    "kind": "$e",
                    "label": label,
                    "body": body_tokens,
                    "mandatory_hypotheses": [],
                }
                definitions[label] = definition
                scope_stack[-1]["e"].append({"label": label, "body": body_tokens})
                scope_stack[-1]["labels"][label] = "$e"
            continue

        if kind in {"$a", "$p"}:
            active_snapshot = _active_scope_snapshot(scope_stack)
            mandatory_hypotheses = _build_mandatory_hypothesis_labels(body_tokens, active_snapshot)

            assertion_definition = {
                "kind": kind,
                "label": label,
                "body": body_tokens,
                "mandatory_hypotheses": mandatory_hypotheses,
            }

            if kind == "$p":
                theorem_count += 1

                stack: list[dict[str, Any]] = []
                saved_nodes: list[dict[str, Any]] = []
                last_step_node: dict[str, Any] | None = None
                theorem_errors: list[str] = []
                theorem_valid = True
                step_count = 0

                compressed_parts = _split_compressed_proof_tokens(proof_tokens)
                proof_form = "compressed" if compressed_parts is not None else "uncompressed"

                operations: list[dict[str, Any]] = []

                if compressed_parts is not None:
                    label_list = [
                        str(token).strip()
                        for token in compressed_parts.get("referenced_labels", [])
                        if str(token).strip()
                    ]
                    expanded_label_table = mandatory_hypotheses + label_list

                    if not bool(compressed_parts.get("well_formed", False)):
                        theorem_valid = False
                        theorem_errors.append(str(compressed_parts.get("reason") or "compressed_proof_not_well_formed"))

                    payload_tokens = [
                        str(token)
                        for token in compressed_parts.get("payload_tokens", [])
                        if str(token)
                    ]
                    payload_decode = _decode_compressed_payload(payload_tokens)
                    decode_errors = [str(err) for err in payload_decode.get("errors", [])]
                    if decode_errors:
                        theorem_valid = False
                        decode_error_count += len(decode_errors)
                        theorem_errors.extend(decode_errors)

                    for raw_op in payload_decode.get("operations", []):
                        op_kind = str(raw_op.get("op"))
                        if op_kind == "index":
                            index = int(raw_op.get("index", 0))
                            if index <= 0:
                                theorem_valid = False
                                theorem_errors.append("decoded_index_not_positive")
                                continue

                            if index <= len(expanded_label_table):
                                operations.append(
                                    {
                                        "op": "label",
                                        "label": expanded_label_table[index - 1],
                                        "index": index,
                                    }
                                )
                            else:
                                saved_idx = index - len(expanded_label_table) - 1
                                operations.append(
                                    {
                                        "op": "saved",
                                        "saved_index": saved_idx,
                                        "index": index,
                                    }
                                )
                        elif op_kind == "save":
                            operations.append({"op": "save"})
                        elif op_kind == "placeholder":
                            operations.append({"op": "placeholder"})
                else:
                    for token in proof_tokens:
                        stripped = str(token).strip()
                        if not stripped:
                            continue
                        if stripped == "?":
                            operations.append({"op": "placeholder"})
                        else:
                            operations.append({"op": "label", "label": stripped})

                def _push_label(label_name: str) -> None:
                    nonlocal theorem_valid
                    nonlocal unknown_label_count
                    nonlocal stack_underflow_count
                    nonlocal substitution_conflict_count
                    nonlocal floating_type_mismatch_count
                    nonlocal essential_hypothesis_mismatch_count

                    definition = definitions.get(label_name)
                    if definition is None:
                        unknown_label_count += 1
                        theorem_valid = False
                        theorem_errors.append(f"unknown_label:{label_name}")
                        return

                    definition_kind = str(definition.get("kind"))
                    if definition_kind in _METAMATH_HYPOTHESIS_LABEL_KINDS:
                        stack.append(
                            {
                                "expr": [str(token) for token in definition.get("body", [])],
                                "origin": label_name,
                                "kind": definition_kind,
                            }
                        )
                        return

                    if definition_kind in {"$a", "$p"}:
                        hypothesis_labels = [
                            str(token)
                            for token in definition.get("mandatory_hypotheses", [])
                            if str(token)
                        ]

                        if len(stack) < len(hypothesis_labels):
                            stack_underflow_count += 1
                            theorem_valid = False
                            theorem_errors.append(
                                f"stack_underflow:{label_name}:{len(hypothesis_labels)}"
                            )
                            return

                        popped_nodes = [stack.pop() for _ in hypothesis_labels][::-1]
                        substitution: dict[str, tuple[str, ...]] = {}

                        for hyp_label, node in zip(hypothesis_labels, popped_nodes):
                            hyp_definition = definitions.get(hyp_label)
                            if hyp_definition is None:
                                unknown_label_count += 1
                                theorem_valid = False
                                theorem_errors.append(f"unknown_hypothesis_label:{hyp_label}")
                                continue

                            hyp_kind = str(hyp_definition.get("kind"))
                            hyp_body = [str(token) for token in hyp_definition.get("body", [])]
                            node_expr = [str(token) for token in node.get("expr", [])]

                            if hyp_kind == "$f":
                                if len(hyp_body) < 2:
                                    theorem_valid = False
                                    theorem_errors.append(f"invalid_f_hypothesis_body:{hyp_label}")
                                    continue

                                expected_typecode = hyp_body[0]
                                variable_token = hyp_body[-1]

                                if not node_expr or node_expr[0] != expected_typecode:
                                    floating_type_mismatch_count += 1
                                    theorem_valid = False
                                    theorem_errors.append(
                                        f"floating_type_mismatch:{hyp_label}:{expected_typecode}"
                                    )
                                    continue

                                candidate = tuple(node_expr[1:])
                                if variable_token in substitution:
                                    if substitution[variable_token] != candidate:
                                        substitution_conflict_count += 1
                                        theorem_valid = False
                                        theorem_errors.append(
                                            f"substitution_conflict:{variable_token}"
                                        )
                                else:
                                    substitution[variable_token] = candidate
                                continue

                            if hyp_kind == "$e":
                                expected_expr = _apply_substitution(hyp_body, substitution)
                                if expected_expr != node_expr:
                                    essential_hypothesis_mismatch_count += 1
                                    theorem_valid = False
                                    theorem_errors.append(
                                        f"essential_hypothesis_mismatch:{hyp_label}"
                                    )
                                continue

                            theorem_valid = False
                            theorem_errors.append(f"invalid_hypothesis_kind:{hyp_kind}")

                        result_expr = _apply_substitution(
                            [str(token) for token in definition.get("body", [])],
                            substitution,
                        )
                        stack.append(
                            {
                                "expr": result_expr,
                                "origin": label_name,
                                "kind": definition_kind,
                            }
                        )
                        return

                    theorem_valid = False
                    theorem_errors.append(f"unsupported_definition_kind:{definition_kind}")

                for operation in operations:
                    op_kind = str(operation.get("op"))

                    if op_kind == "label":
                        label_name = str(operation.get("label") or "").strip()
                        if not label_name:
                            theorem_valid = False
                            theorem_errors.append("empty_label_reference")
                            continue
                        _push_label(label_name)
                        step_count += 1
                        if stack:
                            top = stack[-1]
                            last_step_node = {
                                "expr": [str(token) for token in top.get("expr", [])],
                                "origin": str(top.get("origin") or ""),
                                "kind": str(top.get("kind") or ""),
                            }
                        continue

                    if op_kind == "saved":
                        saved_index = int(operation.get("saved_index", -1))
                        if saved_index < 0 or saved_index >= len(saved_nodes):
                            saved_reference_out_of_range_count += 1
                            theorem_valid = False
                            theorem_errors.append(f"saved_reference_out_of_range:{saved_index}")
                            continue

                        saved_node = saved_nodes[saved_index]
                        stack.append(
                            {
                                "expr": [str(token) for token in saved_node.get("expr", [])],
                                "origin": str(saved_node.get("origin") or ""),
                                "kind": str(saved_node.get("kind") or ""),
                            }
                        )
                        step_count += 1
                        if stack:
                            top = stack[-1]
                            last_step_node = {
                                "expr": [str(token) for token in top.get("expr", [])],
                                "origin": str(top.get("origin") or ""),
                                "kind": str(top.get("kind") or ""),
                            }
                        continue

                    if op_kind == "save":
                        if last_step_node is None:
                            theorem_valid = False
                            theorem_errors.append("save_without_prior_step")
                        else:
                            saved_nodes.append(
                                {
                                    "expr": [str(token) for token in last_step_node.get("expr", [])],
                                    "origin": str(last_step_node.get("origin") or ""),
                                    "kind": str(last_step_node.get("kind") or ""),
                                }
                            )
                        continue

                    if op_kind == "placeholder":
                        placeholder_operation_count += 1
                        theorem_valid = False
                        theorem_errors.append("placeholder_operation")
                        continue

                    theorem_valid = False
                    theorem_errors.append(f"unsupported_operation:{op_kind}")

                expected_result = [str(token) for token in body_tokens]
                final_stack_size = len(stack)
                final_result_matches = final_stack_size == 1 and stack[0].get("expr", []) == expected_result

                if final_stack_size != 1:
                    final_stack_shape_mismatch_count += 1
                    theorem_valid = False
                    theorem_errors.append(f"final_stack_shape:{final_stack_size}")

                if not final_result_matches:
                    final_result_mismatch_count += 1
                    theorem_valid = False
                    theorem_errors.append("final_result_mismatch")

                theorem_sample: dict[str, Any] = {
                    "label": label or None,
                    "proof_form": proof_form,
                    "valid": theorem_valid,
                    "step_count": step_count,
                    "final_stack_size": final_stack_size,
                    "final_result_matches_theorem": final_result_matches,
                    "mandatory_hypothesis_count": len(mandatory_hypotheses),
                    "saved_subproof_count": len(saved_nodes),
                    "error_count": len(theorem_errors),
                    "errors": theorem_errors[:_METAMATH_METADATA_SAMPLE_LIMIT],
                }

                if final_stack_size > 0:
                    theorem_sample["final_result"] = [
                        str(token) for token in stack[-1].get("expr", [])
                    ]
                theorem_sample["expected_result"] = expected_result

                if len(samples) < _METAMATH_METADATA_SAMPLE_LIMIT:
                    samples.append(theorem_sample)
                if not theorem_valid and len(invalid_samples) < _METAMATH_METADATA_SAMPLE_LIMIT:
                    invalid_samples.append(theorem_sample)

                executed_theorem_count += 1
                if not theorem_valid:
                    invalid_theorem_count += 1

            if label:
                definitions[label] = assertion_definition
                scope_stack[-1]["labels"][label] = kind

            continue

    all_valid = (
        theorem_count == 0
        or (
            invalid_theorem_count == 0
            and unknown_label_count == 0
            and stack_underflow_count == 0
            and substitution_conflict_count == 0
            and floating_type_mismatch_count == 0
            and essential_hypothesis_mismatch_count == 0
            and saved_reference_out_of_range_count == 0
            and placeholder_operation_count == 0
            and decode_error_count == 0
            and final_stack_shape_mismatch_count == 0
            and final_result_mismatch_count == 0
        )
    )

    return {
        "theorem_count": theorem_count,
        "executed_theorem_count": executed_theorem_count,
        "invalid_theorem_count": invalid_theorem_count,
        "unknown_label_count": unknown_label_count,
        "stack_underflow_count": stack_underflow_count,
        "substitution_conflict_count": substitution_conflict_count,
        "floating_type_mismatch_count": floating_type_mismatch_count,
        "essential_hypothesis_mismatch_count": essential_hypothesis_mismatch_count,
        "saved_reference_out_of_range_count": saved_reference_out_of_range_count,
        "placeholder_operation_count": placeholder_operation_count,
        "decode_error_count": decode_error_count,
        "final_stack_shape_mismatch_count": final_stack_shape_mismatch_count,
        "final_result_mismatch_count": final_result_mismatch_count,
        "all_valid": all_valid,
        "samples": samples,
        "invalid_samples": invalid_samples,
    }


def _pairwise_pairs(items: list[str]) -> list[tuple[str, str]]:
    pairs: list[tuple[str, str]] = []
    for i in range(len(items)):
        for j in range(i + 1, len(items)):
            left = items[i]
            right = items[j]
            if left <= right:
                pairs.append((left, right))
            else:
                pairs.append((right, left))
    return pairs


def _analyze_disjoint_variable_discipline(statements: list[dict[str, Any]]) -> dict[str, Any]:
    declared_vars: set[str] = set()
    for stmt in statements:
        kind = stmt.get("kind")
        body_tokens = [str(token) for token in stmt.get("body", [])]
        if kind == "$v":
            declared_vars.update(body_tokens)
            continue
        if kind == "$f" and body_tokens:
            declared_vars.add(body_tokens[-1])

    declarations = [stmt for stmt in statements if stmt.get("kind") == "$d"]
    pair_occurrences: dict[tuple[str, str], int] = {}
    undeclared_variables: set[str] = set()
    invalid_count = 0
    samples: list[dict[str, Any]] = []
    invalid_samples: list[dict[str, Any]] = []

    for stmt in declarations:
        raw_vars = [str(token) for token in stmt.get("body", [])]
        unique_vars = list(dict.fromkeys(raw_vars))
        counts: dict[str, int] = {}
        for var in raw_vars:
            counts[var] = counts.get(var, 0) + 1
        duplicates = sorted(var for var, count in counts.items() if count > 1)
        declaration_pairs = _pairwise_pairs(unique_vars)
        for pair in declaration_pairs:
            pair_occurrences[pair] = pair_occurrences.get(pair, 0) + 1

        undeclared = sorted(var for var in unique_vars if var not in declared_vars)
        undeclared_variables.update(undeclared)

        reasons: list[str] = []
        if len(unique_vars) < 2:
            reasons.append("requires_at_least_two_distinct_variables")
        if duplicates:
            reasons.append("duplicate_variables_in_single_declaration")
        if undeclared:
            reasons.append("uses_undeclared_variables")

        valid = len(reasons) == 0
        if not valid:
            invalid_count += 1

        entry: dict[str, Any] = {
            "label": stmt.get("label"),
            "variables": unique_vars,
            "pair_count": len(declaration_pairs),
            "valid": valid,
        }
        if duplicates:
            entry["duplicates"] = duplicates
        if undeclared:
            entry["undeclared"] = undeclared
        if reasons:
            entry["reasons"] = reasons

        if len(samples) < _METAMATH_METADATA_SAMPLE_LIMIT:
            samples.append(entry)
        if not valid and len(invalid_samples) < _METAMATH_METADATA_SAMPLE_LIMIT:
            invalid_samples.append(entry)

    redeclared_pairs = [
        [left, right]
        for (left, right), count in sorted(pair_occurrences.items())
        if count > 1
    ]

    return {
        "declaration_count": len(declarations),
        "declared_variable_count": len(declared_vars),
        "pair_count": len(pair_occurrences),
        "redeclared_pair_count": len(redeclared_pairs),
        "redeclared_pairs": redeclared_pairs[:_METAMATH_METADATA_SAMPLE_LIMIT],
        "undeclared_variable_count": len(undeclared_variables),
        "undeclared_variables": sorted(undeclared_variables)[:_METAMATH_METADATA_SAMPLE_LIMIT],
        "invalid_count": invalid_count,
        "all_valid": invalid_count == 0,
        "samples": samples,
        "invalid_samples": invalid_samples,
    }


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
    proof_segment_analysis = _analyze_metamath_proof_segments(statements)
    dv_discipline_analysis = _analyze_disjoint_variable_discipline(statements)
    theorem_linkage_analysis = _analyze_theorem_label_linkage(statements)
    compressed_payload_decoding_analysis = _analyze_compressed_payload_decoding(statements)
    stack_execution_analysis = _analyze_stack_level_proof_execution(statements)
    source_url = "https://raw.githubusercontent.com/metamath/set.mm/develop/set.mm"
    source_raw_github_url = "https://github.com/metamath/set.mm/raw/refs/heads/develop/set.mm"
    source_blob_url = "https://github.com/metamath/set.mm/blob/develop/set.mm"
    source_history_url = "https://github.com/metamath/set.mm/commits/develop/set.mm"
    source_blob_line_url = _metamath_line_range_url(source_blob_url, line_range)
    parser_file = "src/hypergrammar/parser.py"
    constraints_file = "src/hypergrammar/constraints.py"
    schema_builder = "src/hypergrammar/examples/build_metamath_slice_schema.py"
    schema_output = "src/hypergrammar/examples/metamath_setmm_slice_parsed.json"
    slice_file = str(path).replace("\\", "/")

    metadata: dict[str, Any] = {
        "source_trail": {
            "source_url": source_url,
            "source_raw_github_url": source_raw_github_url,
            "source_blob_url": source_blob_url,
            "source_blob_line_url": source_blob_line_url,
            "source_history_url": source_history_url,
            "source_branch": "develop",
            "slice_file": slice_file,
            "line_range": list(line_range) if line_range else None,
            "statement_counts": statement_counts,
            "sample_labels": sample_labels,
            "parser_file": parser_file,
            "schema_builder": schema_builder,
            "schema_output": schema_output,
            "accountability": {
                "parse_mode": "real_metamath_slice",
                "comment_handling": "ignore tokens between $( and $)",
                "statement_extraction": "supports $c $v $d $f $e $a $p ${ $}",
                "proof_segment_analysis": "extract theorem proof tokens after $= and classify compressed/uncompressed forms",
                "disjoint_variable_analysis": "extract $d declarations and validate declared-variable discipline",
                "theorem_linkage_analysis": "connect theorem proof-label references to in-scope $a/$p/$f/$e labels",
                "compressed_payload_decoding": "decode compressed payload symbols and validate label-index expansion bounds",
                "stack_execution_validation": "execute proof steps with substitution checks and theorem result-shape validation",
            },
        },
        "metamath_constraints": {
            "proof_segments": proof_segment_analysis,
            "disjoint_variable_discipline": dv_discipline_analysis,
            "theorem_linkage": theorem_linkage_analysis,
            "compressed_payload_decoding": compressed_payload_decoding_analysis,
            "stack_execution": stack_execution_analysis,
        },
        "reasoning": {
            "1_source_selection": {
                "claim": "The slice source is canonical set.mm on develop.",
                "raw_url": source_url,
                "raw_github_url": source_raw_github_url,
                "blob_url": source_blob_url,
                "line_range_url": source_blob_line_url,
                "history_url": source_history_url,
            },
            "2_slice_capture": {
                "claim": "A local slice artifact preserves the parsed source window.",
                "slice_file": slice_file,
                "line_range": list(line_range) if line_range else None,
            },
            "3_parser_accountability": {
                "claim": "Parsing process is traceable to tokenizer and statement extraction implementation.",
                "parser_file": parser_file,
                "tokenizer_symbol": "_tokenize_metamath",
                "statement_parser_symbol": "_parse_metamath_statements",
                "supports_kinds": "$c $v $d $f $e $a $p ${ $}",
            },
            "4_schema_projection": {
                "claim": "Extracted statements are projected into metagrammar schema consumed by constraints.",
                "schema_builder": schema_builder,
                "schema_output": schema_output,
                "target_layer": "grammar",
            },
            "5_metamath_hardening": {
                "claim": "Metamath-specific hardening checks evaluate proof-segment, disjoint-variable, theorem-linkage, compressed payload decoding, and stack-level execution discipline.",
                "constraints_file": constraints_file,
                "proof_segments": "metadata.metamath_constraints.proof_segments",
                "disjoint_variable_discipline": "metadata.metamath_constraints.disjoint_variable_discipline",
                "theorem_linkage": "metadata.metamath_constraints.theorem_linkage",
                "compressed_payload_decoding": "metadata.metamath_constraints.compressed_payload_decoding",
                "stack_execution": "metadata.metamath_constraints.stack_execution",
            },
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
