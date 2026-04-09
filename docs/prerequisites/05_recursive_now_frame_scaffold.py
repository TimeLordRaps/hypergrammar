from __future__ import annotations

from dataclasses import dataclass
from typing import List

import numpy as np


@dataclass
class Body:
    """Local body state in the current Now-Frame."""

    name: str
    state: np.ndarray  # shape: (d,)


@dataclass
class NowFrame:
    """
    Recursive Now-Frame state.

    - bodies: many-body local states (present only)
    - holo: holographic all-to-all coupling matrix (meta-connectivity)
    - trace: enfolded residue of prior potentials (not linear history)
    """

    bodies: List[Body]
    holo: np.ndarray  # shape: (n, n)
    trace: np.ndarray  # shape: (d,)
    planck_scale: float = 1.616255e-35
    tolerance: float = 1e-9


def initialize_now_frame(bodies: List[Body], planck_scale: float = 1.616255e-35) -> NowFrame:
    n = len(bodies)
    if n == 0:
        raise ValueError("NowFrame requires at least one body")

    dims = {b.state.shape for b in bodies}
    if len(dims) != 1:
        raise ValueError("All body states must share the same dimensionality")

    holo = np.ones((n, n), dtype=np.float64)
    np.fill_diagonal(holo, 1.0)

    trace = np.mean(np.stack([b.state for b in bodies], axis=0), axis=0)

    return NowFrame(bodies=bodies, holo=holo, trace=trace, planck_scale=planck_scale)


def _body_distance_matrix(frame: NowFrame) -> np.ndarray:
    states = np.stack([b.state for b in frame.bodies], axis=0)  # (n, d)
    diff = states[:, None, :] - states[None, :, :]
    return np.linalg.norm(diff, axis=-1)


def planck_scale_parity_filter(frame: NowFrame, relation: np.ndarray) -> np.ndarray:
    """
    Below Planck scale: recursive/meta-connected branch.
    Above Planck scale: flat/stable observational branch.
    """
    dmat = _body_distance_matrix(frame)

    sub_planck = (dmat < frame.planck_scale).astype(np.float64)
    super_planck = 1.0 - sub_planck

    # recursive branch (meta-connected amplification)
    recursive_branch = relation @ relation.T + relation

    # flat branch (stable symmetric observational projection)
    flat_branch = 0.5 * (relation + relation.T)

    filtered = sub_planck * recursive_branch + super_planck * flat_branch

    # Stabilize and keep all-to-all semantics finite
    max_abs = float(np.max(np.abs(filtered)))
    if max_abs > 1.0:
        filtered = filtered / max_abs

    filtered = 0.5 * (filtered + filtered.T)
    np.fill_diagonal(filtered, 1.0)
    return filtered


def _ricci_trace_free_projection(metric_like: np.ndarray) -> np.ndarray:
    """
    Hyperkähler-inspired Ricci-flat correction proxy:
    remove scalar trace component from curvature-like operator.
    """
    n = metric_like.shape[0]
    scalar_component = np.trace(metric_like) / max(n, 1)
    return metric_like - scalar_component * np.eye(n)


def corrective_feedback(
    frame: NowFrame,
    max_iters: int = 128,
    step: float = 0.05,
) -> NowFrame:
    """
    Fixed-point-seeking correction loop.

    Drives frame coupling toward structural self-consistency.
    No forecasting, no time-series fitting.
    """
    holo = frame.holo.copy()

    for _ in range(max_iters):
        curvature_like = holo @ holo.T - np.eye(holo.shape[0])
        ricci_tf = _ricci_trace_free_projection(curvature_like)

        candidate = holo - step * ricci_tf
        candidate = planck_scale_parity_filter(frame, candidate)

        residual = float(np.linalg.norm(candidate - holo, ord="fro"))
        holo = candidate

        if residual < frame.tolerance:
            break

    frame.holo = holo
    return frame


def enfold_trace(frame: NowFrame, blend: float = 0.5) -> np.ndarray:
    """
    Update current Trace as holographic enfoldment.
    Stores compressed structural residue, not explicit timeline memory.
    """
    present_mean = np.mean(np.stack([b.state for b in frame.bodies], axis=0), axis=0)
    frame.trace = blend * frame.trace + (1.0 - blend) * present_mean
    return frame.trace


def _structural_update(frame: NowFrame, blend: float = 0.5) -> None:
    """
    Move body states via present-frame structural consistency.
    No linear prediction from historical windows.
    """
    states = np.stack([b.state for b in frame.bodies], axis=0)  # (n, d)

    weighted = frame.holo @ states  # (n, d)
    norm = frame.holo.sum(axis=1, keepdims=True) + 1e-12
    target = weighted / norm

    updated = blend * states + (1.0 - blend) * target

    for i, body in enumerate(frame.bodies):
        body.state = updated[i]


def unfold(frame: NowFrame, depth: int) -> NowFrame:
    """
    Recursive transition to the next Now-Frame.

    The driver is self-consistency (corrective feedback),
    not extrapolation of a time series.
    """
    if depth <= 0:
        return frame

    frame = corrective_feedback(frame)
    enfold_trace(frame)
    _structural_update(frame)

    return unfold(frame, depth=depth - 1)


def fixed_point_residual(frame: NowFrame) -> float:
    """
    Diagnostic: how close the frame is to corrective fixed-point behavior.
    """
    clone = NowFrame(
        bodies=[Body(name=b.name, state=b.state.copy()) for b in frame.bodies],
        holo=frame.holo.copy(),
        trace=frame.trace.copy(),
        planck_scale=frame.planck_scale,
        tolerance=frame.tolerance,
    )

    corrected = corrective_feedback(clone, max_iters=64)
    return float(np.linalg.norm(corrected.holo - frame.holo, ord="fro"))


if __name__ == "__main__":
    # Example scaffold usage
    rng = np.random.default_rng(seed=7)
    bodies = [
        Body("A", rng.normal(size=(3,))),
        Body("B", rng.normal(size=(3,))),
        Body("C", rng.normal(size=(3,))),
    ]

    frame = initialize_now_frame(bodies)
    frame = unfold(frame, depth=10)

    print("Trace:", frame.trace)
    print("Fixed-point residual:", fixed_point_residual(frame))
