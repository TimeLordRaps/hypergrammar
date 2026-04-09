from __future__ import annotations

import argparse
import json

from .interpreter import HypergrammarInterpreter


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="hypergrammar-interpreter",
        description=(
            "Validate grammar/metagrammar/metametagrammar specs against "
            "hypergrammar constraints."
        ),
    )
    parser.add_argument(
        "spec",
        help="Path to a specification file (.json, .hg, or .mm)",
    )
    parser.add_argument(
        "--pretty",
        action="store_true",
        help="Pretty-print JSON output",
    )
    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)

    interpreter = HypergrammarInterpreter()
    result = interpreter.evaluate_source(args.spec)

    if args.pretty:
        print(json.dumps(result.to_dict(), indent=2, ensure_ascii=False))
    else:
        print(json.dumps(result.to_dict(), ensure_ascii=False))

    return 0 if result.is_valid else 1


if __name__ == "__main__":
    raise SystemExit(main())
