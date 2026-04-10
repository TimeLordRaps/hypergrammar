from __future__ import annotations

import re


TOKEN_PATTERN = re.compile(r"[A-Za-z0-9_$]+")


def normalize_term(term: str) -> str:
    return "".join(term.split())


def tokenize_term(term: str) -> set[str]:
    return set(TOKEN_PATTERN.findall(term))


def relation_equal(left: str, right: str) -> bool:
    return normalize_term(left) == normalize_term(right)


def _balanced_parentheses(text: str) -> bool:
    depth = 0
    for char in text:
        if char == "(":
            depth += 1
        elif char == ")":
            depth -= 1
            if depth < 0:
                return False
    return depth == 0


def unwrap_loop(term: str, operator: str = "L") -> tuple[int, str]:
    current = normalize_term(term)
    depth = 0
    marker = f"{operator}("

    while current.startswith(marker) and current.endswith(")"):
        inner = current[len(marker) : -1]
        if not _balanced_parentheses(inner):
            break
        current = inner
        depth += 1

    return depth, current


def relation_congruent(left: str, right: str, operator: str = "L") -> bool:
    """Structural identity: same outcome regardless of derivation depth or path.
    Per AGENTS.md corrected filtration (Ch20), ≡ is depth-free."""
    _, left_base = unwrap_loop(left, operator)
    _, right_base = unwrap_loop(right, operator)
    return normalize_term(left_base) == normalize_term(right_base)


def relation_similar(left: str, right: str, operator: str = "L") -> bool:
    """Primary relation: non-empty overlap of continuation capacity.
    Per AGENTS.md corrected filtration (Ch20), ~ is foundational. Survives evanescence."""
    left_tokens = tokenize_term(left)
    right_tokens = tokenize_term(right)

    if left_tokens & right_tokens:
        return True

    # Fall through to base-form comparison (continuation overlap via shared base).
    _, left_base = unwrap_loop(left, operator)
    _, right_base = unwrap_loop(right, operator)

    return normalize_term(left_base) == normalize_term(right_base)
