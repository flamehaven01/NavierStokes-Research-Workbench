"""Shared field and vector types for the mathematical kernel."""

from __future__ import annotations

from collections.abc import Callable

Point3 = tuple[float, float, float]
Vector3 = tuple[float, float, float]
VelocityField = Callable[[Point3, float], Vector3]
ScalarField = Callable[[Point3, float], float]
ForceField = VelocityField


def add(*vectors: Vector3) -> Vector3:
    """Add three-dimensional vectors componentwise."""
    return (
        sum(vector[0] for vector in vectors),
        sum(vector[1] for vector in vectors),
        sum(vector[2] for vector in vectors),
    )


def scale(factor: float, vector: Vector3) -> Vector3:
    """Multiply a vector by a scalar."""
    return factor * vector[0], factor * vector[1], factor * vector[2]


def infinity_norm(vector: Vector3) -> float:
    """Return the componentwise infinity norm."""
    return max(abs(value) for value in vector)
