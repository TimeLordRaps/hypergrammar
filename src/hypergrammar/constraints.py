from __future__ import annotations

from .models import (
    GrammarLayer,
    HypergrammarSpec,
    IssueSeverity,
    ValidationResult,
)
from .relations import relation_equal, relation_similar, unwrap_loop


EPSILON_ALIASES = {"ε", "epsilon", "EPS", "eps"}


class HypergrammarConstraintEngine:
    """
    Evaluates whether a grammar-like specification satisfies repository-level
    hypergrammar constraints derived from AGENTS.md axioms.
    """

    def validate(self, spec: HypergrammarSpec) -> ValidationResult:
        result = ValidationResult(spec_name=spec.name, layer=spec.layer)

        self._validate_basics(spec, result)
        self._validate_layer_target(spec, result)
        self._validate_rule_symbol_domain(spec, result)
        self._validate_axioms(spec, result)
        self._validate_closure(spec, result)

        result.metrics.setdefault("rule_count", len(spec.rules))
        result.metrics.setdefault("chain_length", len(spec.derivation_chain))
        result.checks.setdefault("has_rules", len(spec.rules) > 0)

        return result

    def _validate_basics(self, spec: HypergrammarSpec, result: ValidationResult) -> None:
        if not spec.name.strip():
            result.add_issue(
                IssueSeverity.ERROR,
                "spec.name.empty",
                "Specification name must not be empty.",
            )

        if not spec.closure_operator.strip():
            result.add_issue(
                IssueSeverity.ERROR,
                "spec.operator.empty",
                "Closure operator must not be empty.",
            )

        if not spec.rules and not spec.derivation_chain:
            result.add_issue(
                IssueSeverity.ERROR,
                "spec.empty",
                "Specification needs at least one rule or a derivation_chain.",
            )

        if not spec.derivation_chain:
            result.add_issue(
                IssueSeverity.WARNING,
                "chain.missing",
                "No derivation chain supplied; axiom and closure checks are partial.",
            )

    def _validate_layer_target(self, spec: HypergrammarSpec, result: ValidationResult) -> None:
        if spec.layer == GrammarLayer.GRAMMAR and spec.target_layer is not None:
            result.add_issue(
                IssueSeverity.WARNING,
                "layer.grammar.unexpected_target",
                "Grammar layer usually should not target another layer.",
                target_layer=spec.target_layer.value,
            )

        if spec.layer == GrammarLayer.METAGRAMMAR:
            if spec.target_layer != GrammarLayer.GRAMMAR:
                result.add_issue(
                    IssueSeverity.ERROR,
                    "layer.metagrammar.bad_target",
                    "Metagrammar must target 'grammar'.",
                    target_layer=(spec.target_layer.value if spec.target_layer else None),
                )

        if spec.layer == GrammarLayer.METAMETAGRAMMAR:
            if spec.target_layer != GrammarLayer.METAGRAMMAR:
                result.add_issue(
                    IssueSeverity.ERROR,
                    "layer.metametagrammar.bad_target",
                    "Metametagrammar must target 'metagrammar'.",
                    target_layer=(spec.target_layer.value if spec.target_layer else None),
                )

    def _validate_rule_symbol_domain(
        self,
        spec: HypergrammarSpec,
        result: ValidationResult,
    ) -> None:
        declared = set(spec.terminals) | set(spec.nonterminals)
        declared.add(spec.ground_symbol)
        declared.add(spec.universe_symbol)

        if spec.nonterminals:
            allowed_lhs = set(spec.nonterminals)
            for rule in spec.rules:
                if rule.lhs not in allowed_lhs:
                    result.add_issue(
                        IssueSeverity.ERROR,
                        "rule.lhs.unknown_nonterminal",
                        "Rule lhs is not declared as nonterminal.",
                        lhs=rule.lhs,
                    )

        for rule in spec.rules:
            for token in rule.rhs:
                if token in EPSILON_ALIASES:
                    continue
                if declared and token not in declared:
                    result.add_issue(
                        IssueSeverity.WARNING,
                        "rule.rhs.unknown_symbol",
                        "Rule rhs symbol not declared in terminals/nonterminals.",
                        lhs=rule.lhs,
                        token=token,
                    )

        rhs_tokens = {token for rule in spec.rules for token in rule.rhs}
        if spec.layer == GrammarLayer.METAGRAMMAR:
            if not any("RULE" in token.upper() or token.startswith("<rule") for token in rhs_tokens):
                result.add_issue(
                    IssueSeverity.WARNING,
                    "layer.metagrammar.no_rule_tokens",
                    "Metagrammar rules do not appear to reference rule-level tokens.",
                )

        if spec.layer == GrammarLayer.METAMETAGRAMMAR:
            if not any("META" in token.upper() or token.startswith("<meta") for token in rhs_tokens):
                result.add_issue(
                    IssueSeverity.WARNING,
                    "layer.metametagrammar.no_meta_tokens",
                    "Metametagrammar rules do not appear to reference meta-level tokens.",
                )

    def _validate_axioms(self, spec: HypergrammarSpec, result: ValidationResult) -> None:
        if not spec.derivation_chain:
            result.checks["ax_diff"] = False
            result.checks["ax_sim"] = False
            result.checks["ax_loop"] = False
            return

        closure_terms: list[str] = []
        max_depth = 0

        for term in spec.derivation_chain:
            depth, _ = unwrap_loop(term, spec.closure_operator)
            max_depth = max(max_depth, depth)
            if depth > 0:
                closure_terms.append(term)

        result.metrics["max_closure_depth"] = max_depth

        ax_diff_ok = True
        ax_sim_ok = True
        ax_loop_ok = True
        observed_loop_terms = 0

        for term in closure_terms:
            if relation_equal(term, spec.universe_symbol) or relation_equal(term, spec.ground_symbol):
                ax_diff_ok = False
                result.add_issue(
                    IssueSeverity.ERROR,
                    "axiom.ax_diff",
                    "ax-diff violated: closure term collapses to universe/ground.",
                    term=term,
                )

            if not (
                relation_similar(term, spec.universe_symbol, spec.closure_operator)
                or relation_similar(term, spec.ground_symbol, spec.closure_operator)
            ):
                ax_sim_ok = False
                result.add_issue(
                    IssueSeverity.ERROR,
                    "axiom.ax_sim",
                    "ax-sim violated: closure term is not similar to ground/universe.",
                    term=term,
                )

            depth, base = unwrap_loop(term, spec.closure_operator)
            if depth >= 2:
                observed_loop_terms += 1
                if not relation_similar(term, base, spec.closure_operator):
                    ax_loop_ok = False
                    result.add_issue(
                        IssueSeverity.ERROR,
                        "axiom.ax_loop",
                        "ax-loop violated: L(L(x)) is not similar to x.",
                        term=term,
                        base=base,
                    )

        if closure_terms and observed_loop_terms == 0:
            ax_loop_ok = False
            result.add_issue(
                IssueSeverity.WARNING,
                "axiom.ax_loop.unobserved",
                "No depth-2 closure term observed; ax-loop cannot be confirmed.",
            )

        result.checks["ax_diff"] = ax_diff_ok
        result.checks["ax_sim"] = ax_sim_ok
        result.checks["ax_loop"] = ax_loop_ok

    def _validate_closure(self, spec: HypergrammarSpec, result: ValidationResult) -> None:
        if len(spec.derivation_chain) < 2:
            result.checks["closed_form"] = False
            return

        first = spec.derivation_chain[0]
        last = spec.derivation_chain[-1]
        closed = relation_similar(last, first, spec.closure_operator)
        result.checks["closed_form"] = closed

        if not closed:
            result.add_issue(
                IssueSeverity.ERROR,
                "closure.open_frame",
                "Final derivation term is not similar to the first; open frame detected.",
                first=first,
                last=last,
            )
