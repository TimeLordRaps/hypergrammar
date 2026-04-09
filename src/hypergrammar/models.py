from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
from typing import Any


class GrammarLayer(str, Enum):
    GRAMMAR = "grammar"
    METAGRAMMAR = "metagrammar"
    METAMETAGRAMMAR = "metametagrammar"

    @classmethod
    def from_value(cls, value: str) -> "GrammarLayer":
        normalized = value.strip().lower()
        for item in cls:
            if item.value == normalized:
                return item
        allowed = ", ".join(layer.value for layer in cls)
        raise ValueError(f"Unknown layer '{value}'. Allowed values: {allowed}")


class IssueSeverity(str, Enum):
    INFO = "info"
    WARNING = "warning"
    ERROR = "error"


@dataclass(slots=True)
class Rule:
    lhs: str
    rhs: tuple[str, ...]
    raw: str | None = None


@dataclass(slots=True)
class HypergrammarSpec:
    name: str
    layer: GrammarLayer
    universe_symbol: str = "U"
    ground_symbol: str = "$"
    closure_operator: str = "L"
    terminals: tuple[str, ...] = ()
    nonterminals: tuple[str, ...] = ()
    rules: tuple[Rule, ...] = ()
    derivation_chain: tuple[str, ...] = ()
    target_layer: GrammarLayer | None = None
    metadata: dict[str, Any] = field(default_factory=dict)


@dataclass(slots=True)
class ValidationIssue:
    severity: IssueSeverity
    code: str
    message: str
    context: dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        return {
            "severity": self.severity.value,
            "code": self.code,
            "message": self.message,
            "context": self.context,
        }


@dataclass(slots=True)
class ValidationResult:
    spec_name: str
    layer: GrammarLayer
    checks: dict[str, bool] = field(default_factory=dict)
    metrics: dict[str, Any] = field(default_factory=dict)
    issues: list[ValidationIssue] = field(default_factory=list)

    def add_issue(
        self,
        severity: IssueSeverity,
        code: str,
        message: str,
        **context: Any,
    ) -> None:
        self.issues.append(
            ValidationIssue(
                severity=severity,
                code=code,
                message=message,
                context=context,
            )
        )

    @property
    def has_errors(self) -> bool:
        return any(issue.severity == IssueSeverity.ERROR for issue in self.issues)

    @property
    def is_valid(self) -> bool:
        return not self.has_errors

    def to_dict(self) -> dict[str, Any]:
        return {
            "spec_name": self.spec_name,
            "layer": self.layer.value,
            "is_valid": self.is_valid,
            "checks": self.checks,
            "metrics": self.metrics,
            "issues": [issue.to_dict() for issue in self.issues],
        }
