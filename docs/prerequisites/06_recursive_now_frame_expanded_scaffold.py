from __future__ import annotations

from dataclasses import dataclass
from typing import List, Tuple

import numpy as np


@dataclass
class Body:
    """Local many-body state in the active Now-Frame."""

    name: str
    state: np.ndarray  # shape: (d,)


@dataclass
class HyperKahlerTriplet:
    """Surrogate Hyperkähler triplet (I, J, K style structures)."""

    j1: np.ndarray
    j2: np.ndarray
    j3: np.ndarray


@dataclass
class RecursiveNowFrame:
    """
    Expanded Recursive Now-Frame state.

    - bodies: present-state many-body set (now-only ontology)
    - holo: holographic all-to-all connectivity matrix
    - trace: enfolded residue of prior potentials (no explicit history tape)
    - hk: Hyperkähler-surrogate structure state
    """

    bodies: List[Body]
    holo: np.ndarray  # (n, n)
    trace: np.ndarray  # (d,)
    hk: HyperKahlerTriplet
    planck_scale: float = 1.616255e-35
    tolerance: float = 1e-9


def _random_skew(dim: int, rng: np.random.Generator) -> np.ndarray:
    m = rng.normal(size=(dim, dim))
    return 0.5 * (m - m.T)


def initialize_frame(
    bodies: List[Body],
    seed: int = 11,
    planck_scale: float = 1.616255e-35,
) -> RecursiveNowFrame:
    if len(bodies) < 2:
        raise ValueError("Need at least two bodies for many-body holographic coupling")

    dims = {b.state.shape for b in bodies}
    if len(dims) != 1:
        raise ValueError("All body states must have identical dimensionality")

    d = next(iter(dims))[0]
    n = len(bodies)

    holo = np.ones((n, n), dtype=np.float64)
    np.fill_diagonal(holo, 1.0)

    trace = np.mean(np.stack([b.state for b in bodies], axis=0), axis=0)

    rng = np.random.default_rng(seed)
    hk = HyperKahlerTriplet(
        j1=_random_skew(d, rng),
        j2=_random_skew(d, rng),
        j3=_random_skew(d, rng),
    )

    return RecursiveNowFrame(
        bodies=bodies,
        holo=holo,
        trace=trace,
        hk=hk,
        planck_scale=planck_scale,
    )


def _states(frame: RecursiveNowFrame) -> np.ndarray:
    return np.stack([b.state for b in frame.bodies], axis=0)


def _distance_matrix(frame: RecursiveNowFrame) -> np.ndarray:
    s = _states(frame)
    diff = s[:, None, :] - s[None, :, :]
    return np.linalg.norm(diff, axis=-1)


def _recursive_meta_mix(relation: np.ndarray, depth: int) -> np.ndarray:
    if depth <= 0:
        return relation

    mixed = relation @ relation.T + relation
    max_abs = float(np.max(np.abs(mixed)))
    if max_abs > 1.0:
        mixed = mixed / max_abs

    return _recursive_meta_mix(mixed, depth=depth - 1)


def planck_scale_parity_filter(
    frame: RecursiveNowFrame,
    relation: np.ndarray,
    recursive_depth: int = 3,
) -> np.ndarray:
    """
    Planck-Scale Parity Filter:
    - below Planck scale: recursively meta-connected transform
    - above Planck scale: flat/stable observational projection
    """
    dmat = _distance_matrix(frame)
    sub_planck = (dmat < frame.planck_scale).astype(np.float64)
    super_planck = 1.0 - sub_planck

    recursive_branch = _recursive_meta_mix(relation, depth=recursive_depth)
    flat_branch = 0.5 * (relation + relation.T)

    filtered = sub_planck * recursive_branch + super_planck * flat_branch

    # enforce all-to-all coupling floor (off-diagonal)
    filtered = 0.5 * (filtered + filtered.T)
    off_diag = ~np.eye(filtered.shape[0], dtype=bool)
    filtered[off_diag] += 1e-6
    np.fill_diagonal(filtered, 1.0)

    # bounded magnitude for stability
    filtered = np.tanh(filtered)
    np.fill_diagonal(filtered, 1.0)

    return filtered


def _ricci_trace_free(metric_like: np.ndarray) -> np.ndarray:
    n = metric_like.shape[0]
    scalar = np.trace(metric_like) / max(n, 1)
    return metric_like - scalar * np.eye(n)


def _project_skew(m: np.ndarray) -> np.ndarray:
    return 0.5 * (m - m.T)


def hyperkahler_consistency_residual(hk: HyperKahlerTriplet) -> float:
    """
    Surrogate quaternionic consistency residual.
    Lower is better.
    """
    r12 = np.linalg.norm(hk.j1 @ hk.j2 - hk.j3, ord="fro")
    r23 = np.linalg.norm(hk.j2 @ hk.j3 - hk.j1, ord="fro")
    r31 = np.linalg.norm(hk.j3 @ hk.j1 - hk.j2, ord="fro")
    return float(r12 + r23 + r31)


def _stabilize_hyperkahler(hk: HyperKahlerTriplet, step: float = 0.1) -> HyperKahlerTriplet:
    """
    Lightweight corrective update toward quaternionic compatibility.
    """
    j1 = _project_skew((1.0 - step) * hk.j1 + step * (hk.j2 @ hk.j3))
    j2 = _project_skew((1.0 - step) * hk.j2 + step * (hk.j3 @ hk.j1))
    j3 = _project_skew((1.0 - step) * hk.j3 + step * (hk.j1 @ hk.j2))
    return HyperKahlerTriplet(j1=j1, j2=j2, j3=j3)


def corrective_feedback(
    frame: RecursiveNowFrame,
    max_iters: int = 128,
    step: float = 0.04,
) -> Tuple[RecursiveNowFrame, float]:
    """
    Holomovement-inspired fixed-point correction loop.

    No linear forecasting: updates depend only on current structural consistency.
    """
    holo = frame.holo.copy()
    hk = frame.hk
    residual = float("inf")

    for _ in range(max_iters):
        curvature_like = holo @ holo.T - np.eye(holo.shape[0])
        ricci_tf = _ricci_trace_free(curvature_like)

        candidate_holo = holo - step * ricci_tf
        candidate_holo = planck_scale_parity_filter(frame, candidate_holo, recursive_depth=3)

        candidate_hk = _stabilize_hyperkahler(hk, step=0.08)

        holo_res = np.linalg.norm(candidate_holo - holo, ord="fro")
        hk_res = hyperkahler_consistency_residual(candidate_hk)
        residual = float(holo_res + hk_res)

        holo = candidate_holo
        hk = candidate_hk

        if residual < frame.tolerance:
            break

    frame.holo = holo
    frame.hk = hk
    return frame, residual


def enfold_trace(frame: RecursiveNowFrame, retain: float = 0.7) -> np.ndarray:
    """
    Past is represented only as enfolded trace in the present frame.
    """
    present_mean = np.mean(_states(frame), axis=0)
    spectral_hint = np.array([np.mean(frame.holo)], dtype=np.float64)

    # pad spectral hint to match state dimension
    spectral_vec = np.zeros_like(present_mean)
    spectral_vec[0] = spectral_hint[0]

    frame.trace = retain * frame.trace + (1.0 - retain) * (0.8 * present_mean + 0.2 * spectral_vec)
    return frame.trace


def _structural_update(frame: RecursiveNowFrame, mix: float = 0.55) -> None:
    """
    Present-state update via holographic consistency coupling.
    """
    s = _states(frame)
    weighted = frame.holo @ s
    norm = frame.holo.sum(axis=1, keepdims=True) + 1e-12
    target = weighted / norm

    updated = mix * s + (1.0 - mix) * target
    for i, b in enumerate(frame.bodies):
        b.state = updated[i]


def unfold(frame: RecursiveNowFrame, depth: int) -> RecursiveNowFrame:
    """
    Recursive transition to next Now-Frame.

    Future is unfolded by correction, not predicted from linear past windows.
    """
    if depth <= 0:
        return frame

    frame, _ = corrective_feedback(frame)
    enfold_trace(frame)
    _structural_update(frame)

    return unfold(frame, depth=depth - 1)


def fixed_point_report(frame: RecursiveNowFrame) -> dict:
    """Diagnostic summary for Indelible Correctiveness behavior."""
    clone = RecursiveNowFrame(
        bodies=[Body(name=b.name, state=b.state.copy()) for b in frame.bodies],
        holo=frame.holo.copy(),
        trace=frame.trace.copy(),
        hk=HyperKahlerTriplet(
            j1=frame.hk.j1.copy(),
            j2=frame.hk.j2.copy(),
            j3=frame.hk.j3.copy(),
        ),
        planck_scale=frame.planck_scale,
        tolerance=frame.tolerance,
    )

    corrected, residual = corrective_feedback(clone, max_iters=96)
    drift = float(np.linalg.norm(corrected.holo - frame.holo, ord="fro"))

    return {
        "correction_residual": residual,
        "hologram_drift": drift,
        "hk_residual": hyperkahler_consistency_residual(corrected.hk),
        "trace_norm": float(np.linalg.norm(corrected.trace)),
    }


if __name__ == "__main__":
    rng = np.random.default_rng(23)

    bodies = [
        Body("A", rng.normal(size=(4,))),
        Body("B", rng.normal(size=(4,))),
        Body("C", rng.normal(size=(4,))),
        Body("D", rng.normal(size=(4,))),
    ]

    frame = initialize_frame(bodies)
    frame = unfold(frame, depth=12)

    report = fixed_point_report(frame)
    print("Now-Frame trace:", frame.trace)
    print("Fixed-point report:", report)
