from __future__ import annotations

import math

import pytest

from nsrw.math_kernel.manufactured import decaying_shear, forced_linear_shear, zero_force
from nsrw.math_kernel.operators import (
    curl,
    divergence,
    jacobian,
    laplacian,
    navier_stokes_residual,
    pressure_gradient,
    sample_residual,
)


def test_linear_vector_field_operators() -> None:
    def field(point: tuple[float, float, float], _time: float) -> tuple[float, float, float]:
        x, y, z = point
        return 2 * y, 3 * z, 4 * x

    point = (0.2, -0.4, 0.8)
    matrix = jacobian(field, point, 0.0)
    assert matrix[0] == pytest.approx((0, 2, 0))
    assert matrix[1] == pytest.approx((0, 0, 3))
    assert matrix[2] == pytest.approx((4, 0, 0))
    assert divergence(field, point, 0.0) == pytest.approx(0.0)
    assert curl(field, point, 0.0) == pytest.approx((-3.0, -4.0, -2.0))
    assert laplacian(field, point, 0.0) == pytest.approx((0.0, 0.0, 0.0), abs=1e-7)


def test_pressure_gradient() -> None:
    def pressure(point: tuple[float, float, float], _time: float) -> float:
        x, y, z = point
        return x * x + 2 * y - 3 * z

    assert pressure_gradient(pressure, (0.4, 0.2, -0.1), 0.0) == pytest.approx((0.8, 2, -3))


@pytest.mark.parametrize(
    ("viscosity", "point", "time"),
    [
        (0.7, (0.2, 0.7, -0.1), 0.4),
        (1.3, (-0.3, 0.8, 0.2), 0.6),
    ],
)
def test_decaying_shear_has_small_residual_and_zero_divergence(
    viscosity: float, point: tuple[float, float, float], time: float
) -> None:
    sample = sample_residual(*decaying_shear(viscosity), viscosity, point, time)
    assert sample.residual_infinity_norm < 2e-7
    assert sample.divergence == pytest.approx(0.0)
    assert sample.evidence_class == "NUMERICAL_DIAGNOSTIC"
    assert sample.claim_status == "UNVERIFIED"


def test_forced_shear_has_small_residual() -> None:
    sample = sample_residual(*forced_linear_shear(), 1.0, (0.1, 0.8, 0.2), 0.6)
    assert sample.residual_infinity_norm < 1e-8
    assert sample.as_dict()["claim_status"] == "UNVERIFIED"


def test_wrong_force_is_killed() -> None:
    velocity, pressure, _force = forced_linear_shear()
    residual = navier_stokes_residual(
        velocity, pressure, zero_force, 1.0, (0.1, 0.8, 0.2), 0.6
    )
    assert residual[0] == pytest.approx(0.8)


def test_divergence_detects_compressible_field() -> None:
    def compressible(point: tuple[float, float, float], _time: float) -> tuple[float, float, float]:
        x, y, z = point
        return x, y, z

    assert divergence(compressible, (0.2, 0.3, 0.4), 0.0) == pytest.approx(3.0)


@pytest.mark.parametrize("bad", [0.0, -1.0, math.inf, math.nan])
def test_residual_rejects_invalid_viscosity(bad: float) -> None:
    velocity, pressure, force = forced_linear_shear()
    with pytest.raises(ValueError, match="viscosity"):
        navier_stokes_residual(velocity, pressure, force, bad, (0, 0, 0), 0)


@pytest.mark.parametrize("bad", [0.0, -1.0, math.inf])
def test_operators_reject_invalid_step(bad: float) -> None:
    velocity, pressure, force = forced_linear_shear()
    with pytest.raises(ValueError, match="spatial_step"):
        navier_stokes_residual(
            velocity, pressure, force, 1.0, (0, 0, 0), 0, spatial_step=bad
        )
