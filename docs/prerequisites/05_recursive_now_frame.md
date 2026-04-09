# Recursive Now-Frame: Holomovement, Hyperkähler Consistency, and Indelible Correctiveness

This document is chapter **05**, extending the foundations in chapters `00` through `04` into a systems-modeling frame suitable for implementation.

It formalizes a **Recursive Now-Frame** architecture where change is driven by structural self-consistency, not linear time-series prediction.

## Why this is the natural expansion of 00–04

- [`00_learning_path.md`](./00_learning_path.md) establishes ordered conceptual dependency.
- [`01_grammar_fundamentals.md`](./01_grammar_fundamentals.md) introduces rule-governed state transitions.
- [`02_chomsky_hierarchy.md`](./02_chomsky_hierarchy.md) clarifies expressive constraint classes.
- [`03_hyper_inversion.md`](./03_hyper_inversion.md) reframes progression as closure-oriented structure.
- [`04_degrees_of_freedom.md`](./04_degrees_of_freedom.md) provides the DoF lens for under/overconstraint diagnostics.

This chapter turns those ideas into an executable modeling scaffold.

## Frame axioms for this model

We encode your constraints as explicit design axioms:

1. **Now-only existence**: only current State (Now-Frame) is ontologically active.
2. **Past as Trace, not memory**: no stored timeline; only a holographically enfolded trace in current state.
3. **Future as Unfolding, not prediction**: next frame arises from corrective Ricci-flat consistency flow.
4. **Planck-scale parity filter**:
   - Below Planck scale: recursively meta-connected structure dominates.
   - Above Planck scale: flat/stable causal-like observables dominate.

## State model

Define a Now-Frame as:

$$
\mathcal{N} = (\mathcal{B}, H, \tau, \ell_P, \varepsilon)
$$

- $\mathcal{B}$: many-body local state set.
- $H$: holographic all-to-all coupling matrix/tensor.
- $\tau$: enfolded trace (compressed residue of prior potentials).
- $\ell_P$: Planck-scale threshold.
- $\varepsilon$: convergence tolerance.

A single unfold step is:

$$
\mathcal{N}' = \mathrm{unfold}(\mathcal{N}) := \mathcal{U}\big(\mathcal{C}(\mathcal{N})\big)
$$

- $\mathcal{C}$: corrective feedback operator (fixed-point-seeking consistency loop).
- $\mathcal{U}$: structural update operator (no time-series extrapolation).

## Holomovement-inspired fixed-point objective

Let $\Phi$ be one corrective pass over the frame coupling structure. The objective is:

$$
\Phi(\mathcal{N}^*) \approx \mathcal{N}^* 
\quad\text{with residual}\quad
\lVert \Phi(\mathcal{N}) - \mathcal{N} \rVert < \varepsilon
$$

This is the operational meaning of **Indelible Correctiveness** in the scaffold: structural drift is recursively projected back toward global consistency.

## Ricci-flat consistency intuition

In a Hyperkähler-inspired reading, Ricci-flatness is represented as removing scalar-trace curvature pressure from the correction operator.

For a curvature-like matrix $K$:

$$
K_{\text{tf}} = K - \frac{\mathrm{tr}(K)}{n}I
$$

where $K_{\text{tf}}$ is the trace-free component used in correction updates.

## Planck-Scale Parity Filter behavior

Given relation metric $D_{ij}$ between bodies $i,j$:

- If $D_{ij} < \ell_P$: apply recursive/meta-connected transform branch.
- If $D_{ij} \ge \ell_P$: apply flat/stable observational branch.

This prevents mixing micro-recursive and macro-flat regimes into a single naive update rule.

## Python scaffold

Implementation file:

- [`05_recursive_now_frame_scaffold.py`](./05_recursive_now_frame_scaffold.py)

It includes required interfaces:

- `unfold(frame, depth)` (recursive next-frame operator)
- `corrective_feedback(frame, ...)` (fixed-point consistency loop)
- Holographic all-to-all many-body connectivity (`holo` matrix)
- Planck-scale parity filter branch logic

## Architectural guarantees in this scaffold

1. **No linear forecasting API** is used.
2. The system advances only through structural correction + unfold.
3. Trace is compressed/enfolded into current state (no timeline replay object).
4. Contradiction/overconstraint appears as poor convergence (linked to DoF diagnostics from [`04_degrees_of_freedom.md`](./04_degrees_of_freedom.md)).

## Source alignment links

For repository-level semantic consistency:

- [Concepts](../../AGENTS.md#concepts)
- [Axioms](../../AGENTS.md#axioms)
- [Continuation](../../AGENTS.md#continuation)
- [The Hypergrammar (not Chomsky)](../../AGENTS.md#the-hypergrammar-not-chomsky)

For context lineage:

- [symbolic-satisfaction README](https://github.com/TimeLordRaps/symbolic-satisfaction/blob/main/README.md)
- [symbolic-satisfaction-1 SAFETY_BRIEF](https://github.com/TimeLordRaps/symbolic-satisfaction-1/blob/main/SAFETY_BRIEF.md)
- [satisfaction-suffices docs/index](https://github.com/TimeLordRaps/satisfaction-suffices/blob/main/docs/index.md)

## Handoff to chapter 06

Chapter [`06_recursive_now_frame_expanded.md`](./06_recursive_now_frame_expanded.md)
now provides the explicit expanded meta-frame formalization on top of this scaffold,
including a deeper corrective architecture and dedicated expanded Python scaffold.

Chapters [`07_transframe_ontology.md`](./07_transframe_ontology.md),
[`08_corrective_time_syntropy.md`](./08_corrective_time_syntropy.md), and
[`09_mensaclaused_metaretrocausality.md`](./09_mensaclaused_metaretrocausality.md)
capture the additional metaphysical and clause-theoretic layer that sits above the chapter-06 expanded implementation.