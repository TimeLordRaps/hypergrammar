from __future__ import annotations

import importlib
import json
from pathlib import Path
import sys

REPO_ROOT = Path(__file__).resolve().parents[3]
SRC_ROOT = REPO_ROOT / "src"


SOURCE_MM = Path("src/hypergrammar/examples/source_trail/setmm_slice_360_470.mm")
OUT_JSON = Path("src/hypergrammar/examples/metamath_setmm_slice_parsed.json")


def _load_spec(source: Path):
    if str(SRC_ROOT) not in sys.path:
        sys.path.insert(0, str(SRC_ROOT))
    parser_mod = importlib.import_module("hypergrammar.parser")
    return parser_mod.load_spec(source)


def spec_to_dict(spec) -> dict:
    return {
        "name": spec.name,
        "layer": spec.layer.value,
        "target_layer": spec.target_layer.value if spec.target_layer else None,
        "universe_symbol": spec.universe_symbol,
        "ground_symbol": spec.ground_symbol,
        "closure_operator": spec.closure_operator,
        "terminals": list(spec.terminals),
        "nonterminals": list(spec.nonterminals),
        "rules": [
            {
                "lhs": rule.lhs,
                "rhs": list(rule.rhs),
                "raw": rule.raw,
            }
            for rule in spec.rules
        ],
        "derivation_chain": list(spec.derivation_chain),
        "metadata": spec.metadata,
    }


def main() -> None:
    source_path = REPO_ROOT / SOURCE_MM
    out_path = REPO_ROOT / OUT_JSON

    if not source_path.exists():
        raise FileNotFoundError(f"Metamath source slice not found: {source_path}")

    spec = _load_spec(SOURCE_MM)
    payload = spec_to_dict(spec)
    out_path.write_text(json.dumps(payload, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")

    print("[metamath-schema] built parsed schema from real source slice")
    print(f"  - source: {SOURCE_MM}")
    print(f"  - output: {OUT_JSON}")
    print(f"  - rules: {len(spec.rules)}")


if __name__ == "__main__":
    main()
