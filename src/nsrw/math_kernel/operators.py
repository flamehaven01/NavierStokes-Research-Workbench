"""Finite-difference differential operators and Navier--Stokes diagnostics.

These routines are numerical falsification aids. A small sampled residual is not a proof that
a field solves the PDE globally.
"""

from __future__ import annotations

from dataclasses import asdict, dataclass
from math import isfinite

from nsrw.math_kernel.types import (
    ForceField,
    Point3,
    ScalarField,
    Vector3,
    VelocityField,
    add,
    infinity_norm,
    scale,
)


def _validate_step(step: float, name: str) -> None:
    if not isfinite(step) or step <= 0:
        raise ValueError(f"{name} must be finite and positive")


def _shift(point: Point3, axis: int, amount: float) -> Point3:
    values = list(point)
    values[axis] += amount
    return values[0], values[1], values[2]


def _spatial_partial(
    field: VelocityField, point: Point3, time: float, axis: int, step: float
) -> Vector3:
    plus = field(_shift(point, axis, step), time)
    minus = field(_shift(point, axis, -step), time)
    return scale(0.5 / step, add(plus, scale(-1.0, minus)))


def _spatial_second(
    field: VelocityField, point: Point3, time: float, axis: int, step: float
) -> Vector3:
    plus = field(_shift(point, axis, step), time)
    center = field(point, time)
    minus = field(_shift(point, axis, -step), time)
    return scale(1.0 / (step * step), add(plus, scale(-2.0, center), minus))


def _time_partial(field: VelocityField, point: Point3, time: float, step: float) -> Vector3:
    plus = field(point, time + step)
    minus = field(point, time - step)
    return scale(0.5 / step, add(plus, scale(-1.0, minus)))


def jacobian(
    field: VelocityField, point: Point3, time: float, step: float = 1e-5
) -> tuple[Vector3, Vector3, Vector3]:
    """Return rows ``component`` by columns ``spatial axis``."""
    _validate_step(step, "step")
    columns = [_spatial_partial(field, point, time, axis, step) for axis in range(3)]
    return (
        (columns[0][0], columns[1][0], columns[2][0]),
        (columns[0][1], columns[1][1], columns[2][1]),
        (columns[0][2], columns[1][2], columns[2][2]),
    )


def divergence(field: VelocityField, point: Point3, time: float, step: float = 1e-5) -> float:
    matrix = jacobian(field, point, time, step)
    return sum(matrix[index][index] for index in range(3))


def curl(field: VelocityField, point: Point3, time: float, step: float = 1e-5) -> Vector3:
    matrix = jacobian(field, point, time, step)
    return (
        matrix[2][1] - matrix[1][2],
        matrix[0][2] - matrix[2][0],
        matrix[1][0] - matrix[0][1],
    )


def laplacian(
    field: VelocityField, point: Point3, time: float, step: float = 1e-4
) -> Vector3:
    _validate_step(step, "step")
    return add(*[_spatial_second(field, point, time, axis, step) for axis in range(3)])


def pressure_gradient(
    pressure: ScalarField, point: Point3, time: float, step: float = 1e-5
) -> Vector3:
    _validate_step(step, "step")
    values = []
    for axis in range(3):
        plus = pressure(_shift(point, axis, step), time)
        minus = pressure(_shift(point, axis, -step), time)
        values.append((plus - minus) / (2.0 * step))
    return values[0], values[1], values[2]


def convective_term(
    velocity: VelocityField, point: Point3, time: float, step: float = 1e-5
) -> Vector3:
    value = velocity(point, time)
    matrix = jacobian(velocity, point, time, step)
    return (
        sum(value[axis] * matrix[0][axis] for axis in range(3)),
        sum(value[axis] * matrix[1][axis] for axis in range(3)),
        sum(value[axis] * matrix[2][axis] for axis in range(3)),
    )


def navier_stokes_residual(
    velocity: VelocityField,
    pressure: ScalarField,
    force: ForceField,
    viscosity: float,
    point: Point3,
    time: float,
    spatial_step: float = 1e-4,
    time_step: float = 1e-5,
) -> Vector3:
    """Approximate ``u_t + (u·grad)u - nu*Delta(u) + grad(p) - f``."""
    if not isfinite(viscosity) or viscosity <= 0:
        raise ValueError("viscosity must be finite and positive")
    _validate_step(spatial_step, "spatial_step")
    _validate_step(time_step, "time_step")
    return add(
        _time_partial(velocity, point, time, time_step),
        convective_term(velocity, point, time, spatial_step),
        scale(-viscosity, laplacian(velocity, point, time, spatial_step)),
        pressure_gradient(pressure, point, time, spatial_step),
        scale(-1.0, force(point, time)),
    )


@dataclass(frozen=True)
class ResidualSample:
    """A local diagnostic sample with explicit non-proof authority."""

    point: Point3
    time: float
    viscosity: float
    residual: Vector3
    divergence: float
    residual_infinity_norm: float
    evidence_class: str = "NUMERICAL_DIAGNOSTIC"
    claim_status: str = "UNVERIFIED"

    def as_dict(self) -> dict[str, object]:
        return asdict(self)


def sample_residual(
    velocity: VelocityField,
    pressure: ScalarField,
    force: ForceField,
    viscosity: float,
    point: Point3,
    time: float,
    spatial_step: float = 1e-4,
    time_step: float = 1e-5,
) -> ResidualSample:
    residual = navier_stokes_residual(
        velocity,
        pressure,
        force,
        viscosity,
        point,
        time,
        spatial_step,
        time_step,
    )
    return ResidualSample(
        point=point,
        time=time,
        viscosity=viscosity,
        residual=residual,
        divergence=divergence(velocity, point, time, spatial_step),
        residual_infinity_norm=infinity_norm(residual),
    )
