from __future__ import annotations

from typing import Any

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
        self._validate_source_trail_accountability(spec, result)
        self._validate_metamath_hardening(spec, result)

        result.metrics.setdefault("rule_count", len(spec.rules))
        result.metrics.setdefault("chain_length", len(spec.derivation_chain))
        source_trail = spec.metadata.get("source_trail") if isinstance(spec.metadata, dict) else None
        if source_trail is not None:
            result.metrics.setdefault("source_trail", source_trail)
        reasoning = spec.metadata.get("reasoning") if isinstance(spec.metadata, dict) else None
        if reasoning is not None:
            result.metrics.setdefault("reasoning", reasoning)
        metamath_constraints = (
            spec.metadata.get("metamath_constraints") if isinstance(spec.metadata, dict) else None
        )
        if metamath_constraints is not None:
            result.metrics.setdefault("metamath_constraints", metamath_constraints)
        result.checks.setdefault("has_rules", len(spec.rules) > 0)

        return result

    def _validate_source_trail_accountability(
        self,
        spec: HypergrammarSpec,
        result: ValidationResult,
    ) -> None:
        if not isinstance(spec.metadata, dict):
            return

        source_trail = spec.metadata.get("source_trail")
        if source_trail is None:
            return

        if not isinstance(source_trail, dict):
            result.add_issue(
                IssueSeverity.ERROR,
                "source_trail.invalid",
                "metadata.source_trail must be a dictionary when present.",
            )
            return

        required_links = (
            "source_url",
            "source_blob_url",
            "source_history_url",
            "slice_file",
            "parser_file",
        )
        missing = [key for key in required_links if not source_trail.get(key)]
        if missing:
            result.add_issue(
                IssueSeverity.WARNING,
                "source_trail.missing_links",
                "Source-trail metadata is missing one or more accountability links.",
                missing=missing,
            )

        line_range = source_trail.get("line_range")
        line_range_url = source_trail.get("source_blob_line_url")
        if line_range and not line_range_url:
            result.add_issue(
                IssueSeverity.WARNING,
                "source_trail.line_range_link_missing",
                "line_range is present but source_blob_line_url is missing.",
            )

        reasoning = spec.metadata.get("reasoning")
        if reasoning is None:
            result.add_issue(
                IssueSeverity.WARNING,
                "reasoning.missing",
                "metadata.reasoning is missing; reason-point accountability is partial.",
            )
            return

        if not isinstance(reasoning, dict):
            result.add_issue(
                IssueSeverity.ERROR,
                "reasoning.invalid",
                "metadata.reasoning must be a dictionary when present.",
            )
            return

        linked_steps = self._count_reason_steps_with_references(reasoning)
        result.metrics.setdefault("source_trail_linked_reason_steps", linked_steps)
        if linked_steps == 0:
            result.add_issue(
                IssueSeverity.WARNING,
                "reasoning.no_references",
                "No reasoning steps include hyperlink/path references.",
            )

    def _validate_metamath_hardening(self, spec: HypergrammarSpec, result: ValidationResult) -> None:
        if not isinstance(spec.metadata, dict):
            return

        hardening = spec.metadata.get("metamath_constraints")
        if hardening is None:
            return

        if not isinstance(hardening, dict):
            result.add_issue(
                IssueSeverity.ERROR,
                "metamath_constraints.invalid",
                "metadata.metamath_constraints must be a dictionary when present.",
            )
            return

        source_trail = spec.metadata.get("source_trail")
        statement_counts: dict[str, Any] = {}
        if isinstance(source_trail, dict):
            raw_counts = source_trail.get("statement_counts")
            if isinstance(raw_counts, dict):
                statement_counts = raw_counts

        theorem_count_observed = self._safe_int(statement_counts.get("$p"))
        dv_count_observed = self._safe_int(statement_counts.get("$d"))

        proof_ok = True
        proof_segments = hardening.get("proof_segments")
        compressed_count_observed = 0
        if proof_segments is None and theorem_count_observed > 0:
            proof_ok = False
            result.add_issue(
                IssueSeverity.WARNING,
                "metamath.proof_segments.missing",
                "Theorem statements were observed but proof segment analysis is missing.",
                theorem_count=theorem_count_observed,
            )
        elif proof_segments is not None:
            if not isinstance(proof_segments, dict):
                proof_ok = False
                result.add_issue(
                    IssueSeverity.ERROR,
                    "metamath.proof_segments.invalid",
                    "metamath_constraints.proof_segments must be a dictionary.",
                )
            else:
                theorem_count = self._safe_int(proof_segments.get("theorem_count"))
                equals_count = self._safe_int(proof_segments.get("with_equals_segment_count"))
                compressed_count_observed = self._safe_int(proof_segments.get("compressed_count"))
                malformed_count = self._safe_int(proof_segments.get("malformed_count"))
                empty_proof_count = self._safe_int(proof_segments.get("empty_proof_count"))

                if theorem_count > equals_count:
                    proof_ok = False
                    result.add_issue(
                        IssueSeverity.ERROR,
                        "metamath.proof_segments.equals_mismatch",
                        "Some theorem statements are missing `$=` proof segments.",
                        theorem_count=theorem_count,
                        with_equals_segment_count=equals_count,
                    )

                if malformed_count > 0:
                    proof_ok = False
                    result.add_issue(
                        IssueSeverity.ERROR,
                        "metamath.proof_segments.malformed",
                        "Malformed theorem proof segments detected.",
                        malformed_count=malformed_count,
                        malformed_samples=proof_segments.get("malformed_samples", [])[:10],
                    )

                if empty_proof_count > 0:
                    proof_ok = False
                    result.add_issue(
                        IssueSeverity.ERROR,
                        "metamath.proof_segments.empty",
                        "One or more theorem proof segments are empty.",
                        empty_proof_count=empty_proof_count,
                    )

        dv_ok = True
        dv_discipline = hardening.get("disjoint_variable_discipline")
        if dv_discipline is None and dv_count_observed > 0:
            dv_ok = False
            result.add_issue(
                IssueSeverity.WARNING,
                "metamath.dv_discipline.missing",
                "`$d` statements were observed but disjoint-variable analysis is missing.",
                disjoint_statement_count=dv_count_observed,
            )
        elif dv_discipline is not None:
            if not isinstance(dv_discipline, dict):
                dv_ok = False
                result.add_issue(
                    IssueSeverity.ERROR,
                    "metamath.dv_discipline.invalid",
                    "metamath_constraints.disjoint_variable_discipline must be a dictionary.",
                )
            else:
                invalid_count = self._safe_int(dv_discipline.get("invalid_count"))
                undeclared_variable_count = self._safe_int(
                    dv_discipline.get("undeclared_variable_count")
                )
                redeclared_pair_count = self._safe_int(dv_discipline.get("redeclared_pair_count"))

                if invalid_count > 0:
                    dv_ok = False
                    result.add_issue(
                        IssueSeverity.ERROR,
                        "metamath.dv_discipline.invalid_declarations",
                        "Invalid disjoint-variable declarations detected.",
                        invalid_count=invalid_count,
                        invalid_samples=dv_discipline.get("invalid_samples", [])[:10],
                    )

                if undeclared_variable_count > 0:
                    dv_ok = False
                    result.add_issue(
                        IssueSeverity.ERROR,
                        "metamath.dv_discipline.undeclared_variables",
                        "Disjoint-variable declarations reference undeclared variables.",
                        undeclared_variable_count=undeclared_variable_count,
                        undeclared_variables=dv_discipline.get("undeclared_variables", [])[:20],
                    )

                if redeclared_pair_count > 0:
                    result.add_issue(
                        IssueSeverity.WARNING,
                        "metamath.dv_discipline.redeclared_pairs",
                        "Some disjoint-variable pairs are redeclared in multiple `$d` statements.",
                        redeclared_pair_count=redeclared_pair_count,
                        redeclared_pairs=dv_discipline.get("redeclared_pairs", [])[:20],
                    )

        linkage_ok = True
        theorem_linkage = hardening.get("theorem_linkage")
        if theorem_linkage is None and theorem_count_observed > 0:
            linkage_ok = False
            result.add_issue(
                IssueSeverity.WARNING,
                "metamath.theorem_linkage.missing",
                "Theorem statements were observed but theorem-linkage analysis is missing.",
                theorem_count=theorem_count_observed,
            )
        elif theorem_linkage is not None:
            if not isinstance(theorem_linkage, dict):
                linkage_ok = False
                result.add_issue(
                    IssueSeverity.ERROR,
                    "metamath.theorem_linkage.invalid",
                    "metamath_constraints.theorem_linkage must be a dictionary.",
                )
            else:
                linkage_theorem_count = self._safe_int(theorem_linkage.get("theorem_count"))
                reference_count = self._safe_int(theorem_linkage.get("reference_count"))
                resolved_reference_count = self._safe_int(
                    theorem_linkage.get("resolved_reference_count")
                )
                unresolved_reference_count = self._safe_int(
                    theorem_linkage.get("unresolved_reference_count")
                )
                placeholder_reference_count = self._safe_int(
                    theorem_linkage.get("placeholder_reference_count")
                )

                if theorem_count_observed > 0 and linkage_theorem_count != theorem_count_observed:
                    linkage_ok = False
                    result.add_issue(
                        IssueSeverity.WARNING,
                        "metamath.theorem_linkage.theorem_count_mismatch",
                        "Theorem count in linkage analysis does not match observed `$p` count.",
                        observed_theorem_count=theorem_count_observed,
                        linkage_theorem_count=linkage_theorem_count,
                    )

                if unresolved_reference_count > 0:
                    linkage_ok = False
                    result.add_issue(
                        IssueSeverity.ERROR,
                        "metamath.theorem_linkage.unresolved_references",
                        "Some theorem proof-label references are not available in `$a/$p/$f/$e` scope.",
                        unresolved_reference_count=unresolved_reference_count,
                        unresolved_labels=theorem_linkage.get("unresolved_labels", [])[:20],
                        unresolved_samples=theorem_linkage.get("unresolved_samples", [])[:10],
                    )

                if placeholder_reference_count > 0:
                    linkage_ok = False
                    result.add_issue(
                        IssueSeverity.WARNING,
                        "metamath.theorem_linkage.placeholders",
                        "Theorem proofs contain placeholder references (`?`); linkage is incomplete.",
                        placeholder_reference_count=placeholder_reference_count,
                    )

                if reference_count < (resolved_reference_count + unresolved_reference_count):
                    linkage_ok = False
                    result.add_issue(
                        IssueSeverity.WARNING,
                        "metamath.theorem_linkage.count_mismatch",
                        "Theorem linkage counts are internally inconsistent.",
                        reference_count=reference_count,
                        resolved_reference_count=resolved_reference_count,
                        unresolved_reference_count=unresolved_reference_count,
                    )

        payload_ok = True
        compressed_payload_decoding = hardening.get("compressed_payload_decoding")
        if compressed_payload_decoding is None and compressed_count_observed > 0:
            payload_ok = False
            result.add_issue(
                IssueSeverity.WARNING,
                "metamath.payload_decoding.missing",
                "Compressed theorem proofs were observed but payload decoding analysis is missing.",
                compressed_theorem_count=compressed_count_observed,
            )
        elif compressed_payload_decoding is not None:
            if not isinstance(compressed_payload_decoding, dict):
                payload_ok = False
                result.add_issue(
                    IssueSeverity.ERROR,
                    "metamath.payload_decoding.invalid",
                    "metamath_constraints.compressed_payload_decoding must be a dictionary.",
                )
            else:
                invalid_payload_count = self._safe_int(
                    compressed_payload_decoding.get("invalid_payload_count")
                )
                malformed_payload_count = self._safe_int(
                    compressed_payload_decoding.get("malformed_payload_count")
                )
                out_of_range_index_count = self._safe_int(
                    compressed_payload_decoding.get("out_of_range_index_count")
                )
                unresolved_label_list_reference_count = self._safe_int(
                    compressed_payload_decoding.get("unresolved_label_list_reference_count")
                )
                save_without_prior_step_count = self._safe_int(
                    compressed_payload_decoding.get("save_without_prior_step_count")
                )
                placeholder_reference_count = self._safe_int(
                    compressed_payload_decoding.get("placeholder_reference_count")
                )

                if invalid_payload_count > 0:
                    payload_ok = False
                    result.add_issue(
                        IssueSeverity.ERROR,
                        "metamath.payload_decoding.invalid_payloads",
                        "One or more compressed proof payloads failed decoding/expansion checks.",
                        invalid_payload_count=invalid_payload_count,
                        invalid_samples=compressed_payload_decoding.get("invalid_samples", [])[:10],
                    )

                if malformed_payload_count > 0:
                    payload_ok = False
                    result.add_issue(
                        IssueSeverity.ERROR,
                        "metamath.payload_decoding.malformed",
                        "Malformed compressed payload symbol streams were detected.",
                        malformed_payload_count=malformed_payload_count,
                    )

                if out_of_range_index_count > 0:
                    payload_ok = False
                    result.add_issue(
                        IssueSeverity.ERROR,
                        "metamath.payload_decoding.index_out_of_range",
                        "Decoded compressed payload indices exceed expansion bounds.",
                        out_of_range_index_count=out_of_range_index_count,
                    )

                if unresolved_label_list_reference_count > 0:
                    payload_ok = False
                    result.add_issue(
                        IssueSeverity.ERROR,
                        "metamath.payload_decoding.unresolved_label_list",
                        "Compressed proof label-list references include unavailable labels.",
                        unresolved_label_list_reference_count=unresolved_label_list_reference_count,
                    )

                if save_without_prior_step_count > 0:
                    payload_ok = False
                    result.add_issue(
                        IssueSeverity.ERROR,
                        "metamath.payload_decoding.save_without_step",
                        "Compressed payload uses `Z` save markers before any decodable step.",
                        save_without_prior_step_count=save_without_prior_step_count,
                    )

                if placeholder_reference_count > 0:
                    payload_ok = False
                    result.add_issue(
                        IssueSeverity.WARNING,
                        "metamath.payload_decoding.placeholders",
                        "Compressed payload includes placeholder markers (`?`); decoding is incomplete.",
                        placeholder_reference_count=placeholder_reference_count,
                    )

        stack_ok = True
        stack_execution = hardening.get("stack_execution")
        if stack_execution is None and theorem_count_observed > 0:
            stack_ok = False
            result.add_issue(
                IssueSeverity.WARNING,
                "metamath.stack_execution.missing",
                "Theorem statements were observed but stack-level proof execution analysis is missing.",
                theorem_count=theorem_count_observed,
            )
        elif stack_execution is not None:
            if not isinstance(stack_execution, dict):
                stack_ok = False
                result.add_issue(
                    IssueSeverity.ERROR,
                    "metamath.stack_execution.invalid",
                    "metamath_constraints.stack_execution must be a dictionary.",
                )
            else:
                invalid_theorem_count = self._safe_int(stack_execution.get("invalid_theorem_count"))
                unknown_label_count = self._safe_int(stack_execution.get("unknown_label_count"))
                stack_underflow_count = self._safe_int(stack_execution.get("stack_underflow_count"))
                substitution_conflict_count = self._safe_int(
                    stack_execution.get("substitution_conflict_count")
                )
                floating_type_mismatch_count = self._safe_int(
                    stack_execution.get("floating_type_mismatch_count")
                )
                essential_hypothesis_mismatch_count = self._safe_int(
                    stack_execution.get("essential_hypothesis_mismatch_count")
                )
                saved_reference_out_of_range_count = self._safe_int(
                    stack_execution.get("saved_reference_out_of_range_count")
                )
                placeholder_operation_count = self._safe_int(
                    stack_execution.get("placeholder_operation_count")
                )
                decode_error_count = self._safe_int(stack_execution.get("decode_error_count"))
                final_stack_shape_mismatch_count = self._safe_int(
                    stack_execution.get("final_stack_shape_mismatch_count")
                )
                final_result_mismatch_count = self._safe_int(
                    stack_execution.get("final_result_mismatch_count")
                )

                if invalid_theorem_count > 0:
                    stack_ok = False
                    result.add_issue(
                        IssueSeverity.ERROR,
                        "metamath.stack_execution.invalid_theorems",
                        "One or more theorem proofs failed stack-level execution checks.",
                        invalid_theorem_count=invalid_theorem_count,
                        invalid_samples=stack_execution.get("invalid_samples", [])[:10],
                    )

                if unknown_label_count > 0:
                    stack_ok = False
                    result.add_issue(
                        IssueSeverity.ERROR,
                        "metamath.stack_execution.unknown_labels",
                        "Proof execution referenced unknown labels.",
                        unknown_label_count=unknown_label_count,
                    )

                if stack_underflow_count > 0:
                    stack_ok = False
                    result.add_issue(
                        IssueSeverity.ERROR,
                        "metamath.stack_execution.stack_underflow",
                        "Proof execution encountered stack underflow when applying assertions.",
                        stack_underflow_count=stack_underflow_count,
                    )

                if substitution_conflict_count > 0:
                    stack_ok = False
                    result.add_issue(
                        IssueSeverity.ERROR,
                        "metamath.stack_execution.substitution_conflict",
                        "Substitution assignments conflicted during assertion application.",
                        substitution_conflict_count=substitution_conflict_count,
                    )

                if floating_type_mismatch_count > 0:
                    stack_ok = False
                    result.add_issue(
                        IssueSeverity.ERROR,
                        "metamath.stack_execution.floating_type_mismatch",
                        "Floating-hypothesis typecode checks failed during stack execution.",
                        floating_type_mismatch_count=floating_type_mismatch_count,
                    )

                if essential_hypothesis_mismatch_count > 0:
                    stack_ok = False
                    result.add_issue(
                        IssueSeverity.ERROR,
                        "metamath.stack_execution.essential_hypothesis_mismatch",
                        "Essential-hypothesis result-shape checks failed after substitution.",
                        essential_hypothesis_mismatch_count=essential_hypothesis_mismatch_count,
                    )

                if saved_reference_out_of_range_count > 0:
                    stack_ok = False
                    result.add_issue(
                        IssueSeverity.ERROR,
                        "metamath.stack_execution.saved_reference_out_of_range",
                        "Compressed proof execution referenced saved subproof indices out of range.",
                        saved_reference_out_of_range_count=saved_reference_out_of_range_count,
                    )

                if decode_error_count > 0:
                    stack_ok = False
                    result.add_issue(
                        IssueSeverity.ERROR,
                        "metamath.stack_execution.decode_errors",
                        "Compressed payload decoding produced errors during stack execution.",
                        decode_error_count=decode_error_count,
                    )

                if placeholder_operation_count > 0:
                    stack_ok = False
                    result.add_issue(
                        IssueSeverity.WARNING,
                        "metamath.stack_execution.placeholders",
                        "Proof execution includes placeholder operations (`?`), so verification is incomplete.",
                        placeholder_operation_count=placeholder_operation_count,
                    )

                if final_stack_shape_mismatch_count > 0:
                    stack_ok = False
                    result.add_issue(
                        IssueSeverity.ERROR,
                        "metamath.stack_execution.final_stack_shape",
                        "Final stack shape is invalid for one or more theorem proofs.",
                        final_stack_shape_mismatch_count=final_stack_shape_mismatch_count,
                    )

                if final_result_mismatch_count > 0:
                    stack_ok = False
                    result.add_issue(
                        IssueSeverity.ERROR,
                        "metamath.stack_execution.final_result_mismatch",
                        "Final proof result does not match theorem statement body for one or more theorems.",
                        final_result_mismatch_count=final_result_mismatch_count,
                    )

        result.checks["metamath_proof_segments"] = proof_ok
        result.checks["metamath_disjoint_discipline"] = dv_ok
        result.checks["metamath_theorem_linkage"] = linkage_ok
        result.checks["metamath_compressed_payload_decoding"] = payload_ok
        result.checks["metamath_stack_execution"] = stack_ok

    def _safe_int(self, value: Any) -> int:
        if isinstance(value, bool):
            return int(value)
        if isinstance(value, int):
            return value
        if isinstance(value, float):
            return int(value)
        if isinstance(value, str) and value.isdigit():
            return int(value)
        return 0

    def _count_reason_steps_with_references(self, reasoning: dict[str, Any]) -> int:
        linked_steps = 0
        for value in reasoning.values():
            if self._contains_reference(value):
                linked_steps += 1
        return linked_steps

    def _contains_reference(self, value: Any) -> bool:
        if isinstance(value, str):
            return (
                value.startswith("http://")
                or value.startswith("https://")
                or value.startswith("src/")
                or value.startswith("./")
            )
        if isinstance(value, dict):
            return any(self._contains_reference(item) for item in value.values())
        if isinstance(value, list):
            return any(self._contains_reference(item) for item in value)
        return False

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
            if not any(
                "RULE" in token.upper()
                or token.startswith("<rule")
                or token in {"$c", "$v", "$d", "$f", "$e", "$a", "$p", "${", "$}"}
                for token in rhs_tokens
            ):
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
