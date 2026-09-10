"""Similarity-coordinate reconstruction from the paper's equation (3.2)."""

from __future__ import annotations

from dataclasses import asdict, dataclass
from math import isfinite


@dataclass(frozen=True)
class SimilarityCoordinates:
    tau: float
    z: float
    radius: float
    h: float
    q: float
    eta: float
    capital_x: float
    equation_residual: float
    iterations: int

    def as_dict(self) -> dict[str, float | int]:
        return asdict(self)


def reconstruct_similarity_coordinates(
    tau: float,
    z: float,
    radius: float,
    h: float,
    tolerance: float = 1e-13,
    max_iterations: int = 200,
) -> SimilarityCoordinates:
    """Solve ``q - z^2 q^(2h) = tau`` by a fail-closed bisection."""
    _validate_inputs(tau, z, radius, h, tolerance, max_iterations)

    def equation(q: float) -> float:
        return q - z * z * q ** (2.0 * h) - tau

    q, iterations = _bisect_q(equation, tau, tolerance, max_iterations)
    eta = z / q ** (0.5 - h)
    capital_x = radius * radius / (2.0 * q)
    return SimilarityCoordinates(
        tau=tau,
        z=z,
        radius=radius,
        h=h,
        q=q,
        eta=eta,
        capital_x=capital_x,
        equation_residual=equation(q),
        iterations=iterations,
    )


def _validate_inputs(
    tau: float, z: float, radius: float, h: float, tolerance: float, max_iterations: int
) -> None:
    _validate_geometry(tau, z, radius)
    _validate_solver_parameters(h, tolerance, max_iterations)


def _validate_geometry(tau: float, z: float, radius: float) -> None:
    if not (isfinite(tau) and tau > 0):
        raise ValueError("tau must be finite and positive")
    if not (isfinite(z) and isfinite(radius)):
        raise ValueError("z and radius must be finite")
    if radius < 0:
        raise ValueError("radius must be non-negative")


def _validate_solver_parameters(h: float, tolerance: float, max_iterations: int) -> None:
    if not (isfinite(h) and 0 < h < 0.01):
        raise ValueError("h must satisfy 0 < h < 1/100")
    if not (isfinite(tolerance) and tolerance > 0):
        raise ValueError("tolerance must be finite and positive")
    if max_iterations <= 0:
        raise ValueError("max_iterations must be positive")


def _bisect_q(equation, tau: float, tolerance: float, max_iterations: int) -> tuple[float, int]:
    lower = tau
    upper = max(1.0, 2.0 * tau)
    while equation(upper) <= 0:
        upper *= 2.0
        if not isfinite(upper):
            raise ArithmeticError("failed to bracket similarity coordinate q")

    iterations = 0
    for iteration in range(1, max_iterations + 1):
        iterations = iteration
        midpoint = 0.5 * (lower + upper)
        value = equation(midpoint)
        if abs(value) <= tolerance or upper - lower <= tolerance * max(1.0, midpoint):
            q = midpoint
            break
        if value > 0:
            upper = midpoint
        else:
            lower = midpoint
    else:
        raise ArithmeticError("similarity-coordinate solve did not converge")
    return q, iterations
