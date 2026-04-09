from __future__ import annotations

from .constraints import HypergrammarConstraintEngine
from .models import HypergrammarSpec, ValidationResult
from .parser import load_spec


class HypergrammarInterpreter:
    """
    Main interpreter facade.

    Accepts grammar / metagrammar / metametagrammar specifications and evaluates
    whether they satisfy hypergrammar-derived constraints.
    """

    def __init__(self, engine: HypergrammarConstraintEngine | None = None) -> None:
        self.engine = engine or HypergrammarConstraintEngine()

    def evaluate(self, spec: HypergrammarSpec) -> ValidationResult:
        return self.engine.validate(spec)

    def evaluate_source(self, source: str | dict | HypergrammarSpec) -> ValidationResult:
        spec = load_spec(source)
        return self.evaluate(spec)
