# Degrees of Freedom (DoF)

This document explains what degrees of freedom are, how they work as a universal concept, and what positive, zero, and negative degrees of freedom mean in practice.

## What is a degree of freedom?

A **degree of freedom** is one independent way a system can vary while still obeying its rules.

If a system has more independent choices, it has more DoF. If rules/constraints remove choices, DoF decreases.

## Universal definition

Across domains, the same template applies:

1. Define the system's possible states.
2. Define the constraints that must hold.
3. Count how many independent state directions remain after constraints.

A common local model is:

$$
\text{DoF} \approx n - r
$$

- $n$: number of independent state variables.
- $r$: number of independent constraints.

This is a local linearized intuition. Real systems can be nonlinear, piecewise, or discrete, but the logic remains: **freedom = variation left after constraints**.

## How DoF works universally

The concept appears everywhere because every system has:

- A state space (what can vary), and
- A rule set (what must stay true).

Examples:

- **Mechanics**: position/orientation variables constrained by joints.
- **Optimization**: decision variables constrained by equations/inequalities.
- **Control systems**: actuator inputs constrained by dynamics/safety limits.
- **Formal languages/grammars**: derivation choices constrained by production rules.
- **Proof systems**: continuation paths constrained by axioms/inference rules.

Different field, same structure: more independent admissible variation means higher DoF.

## Positive degrees of freedom ($\text{DoF} > 0$)

Positive DoF means the system still has **choice space**.

- Multiple valid continuations exist.
- You can move/change without violating constraints.
- Exploration or adaptation is possible.

Example (equations):

- Variables: $x, y$ ($n=2$)
- Constraint: $x + y = 1$ ($r=1$)
- DoF: $2 - 1 = 1$

There is one independent parameter left, so infinitely many valid pairs remain.

## Zero degrees of freedom ($\text{DoF} = 0$)

Zero DoF means the system is **fully determined** (locally).

- No independent variation remains.
- You have a fixed solution (or a discrete finite set under nonlinearity/discreteness).
- Any change would violate at least one constraint.

Example (equations):

- Variables: $x, y$ ($n=2$)
- Constraints: $x+y=1$, $x-y=0$ ($r=2$, independent)
- DoF: $2 - 2 = 0$

Solution is fixed: $x=y=\frac{1}{2}$.

## Negative degrees of freedom ($\text{DoF} < 0$)

Negative DoF indicates an **overconstrained specification**.

Interpretation:

- More independent constraints than independent variables.
- Generic outcome: no admissible state exists.
- In practice this is a diagnostic signal for contradiction or model mismatch.

Example intuition:

- $n=2$ variables, $r=3$ independent hard constraints.
- $\text{DoF}= -1$.

This does not mean the system has "minus one physical knobs." It means your constraint set demands more independent conditions than the state space can satisfy.

## Quick domain comparison

| DoF sign | Meaning | Typical system behavior |
|---|---|---|
| Positive | Underdetermined / flexible | Many valid states or trajectories |
| Zero | Exactly determined | Fixed solution or rigid local behavior |
| Negative | Overdetermined | Inconsistency, infeasibility, contradiction signal |

## Connection to hyper-grammar terminology

In `hyper-grammar`, constraints appear as closure requirements over continuation structure (see [`../../AGENTS.md`](../../AGENTS.md)).

- Positive-like regime: multiple continuation paths still available.
- Zero-like regime: closure condition determines a specific resolved form.
- Negative-like regime: constraint set indicates non-closure/contradiction (open-frame revelation).

Related references:

- [Concepts](../../AGENTS.md#concepts)
- [Axioms](../../AGENTS.md#axioms)
- [Continuation](../../AGENTS.md#continuation)

## Practical checklist

When analyzing any system with DoF:

1. List state variables clearly.
2. Separate independent constraints from redundant ones.
3. Estimate local DoF ($n-r$) and verify with actual solvability.
4. Treat negative DoF as a model/debug signal, not a literal physical count.

Next step: read [`05_recursive_now_frame.md`](./05_recursive_now_frame.md) to apply DoF diagnostics to a recursive non-predictive modeling frame.