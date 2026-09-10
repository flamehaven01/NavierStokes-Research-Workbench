from __future__ import annotations

from fractions import Fraction

import pytest

from nsrw.math_kernel.manufactured import decaying_shear
from nsrw.math_kernel.operators import sample_residual
from nsrw.math_kernel.scaling import (
    ScalingLaw,
    periodic_scaling_certificate,
    viscosity_rescale_force,
    viscosity_rescale_pressure,
    viscosity_rescale_velocity,
    viscosity_scaling_certificate,
)


def test_viscosity_scaling_exact_exponents() -> None:
    certificate = viscosity_scaling_certificate()
    assert certificate.momentum_terms_match
    assert set(certificate.term_exponents.values()) == {Fraction(1, 2)}
    assert certificate.invariant_exponents["energy_squared"] == Fraction(5, 2)
    assert certificate.invariant_exponents["vorticity_linf"] == 0
    rendered = certificate.as_dict()
    assert rendered["term_exponents"]["force"] == "1/2"
    assert rendered["claim_status"] == "SUPPORTED"


def test_periodic_scaling_exact_exponents() -> None:
    certificate = periodic_scaling_certificate()
    assert certificate.momentum_terms_match
    assert set(certificate.term_exponents.values()) == {Fraction(3)}
    assert certificate.invariant_exponents["bkm_time_integral"] == 0
    assert certificate.as_dict()["invariant_exponents"]["energy_squared"] == "-1"


def test_wrong_force_exponent_breaks_covariance() -> None:
    wrong = ScalingLaw(
        velocity=Fraction(1, 2),
        space_argument=Fraction(-1, 2),
        time_argument=Fraction(0),
        pressure=Fraction(1),
        force=Fraction(3, 2),
        viscosity_coefficient=Fraction(1),
    ).certify("mutated", "test-only")
    assert not wrong.momentum_terms_match
    assert wrong.term_exponents["force"] == Fraction(3, 2)


def test_viscosity_rescaled_solution_has_small_residual() -> None:
    source_velocity, source_pressure, source_force = decaying_shear(1.0)
    viscosity = 0.36
    velocity = viscosity_rescale_velocity(source_velocity, viscosity)
    pressure = viscosity_rescale_pressure(source_pressure, viscosity)
    force = viscosity_rescale_force(source_force, viscosity)
    sample = sample_residual(velocity, pressure, force, viscosity, (0.1, 0.4, -0.2), 0.3)
    assert sample.residual_infinity_norm < 2e-7


def test_rescaled_fields_apply_paper_formula() -> None:
    def velocity(point: tuple[float, float, float], time: float) -> tuple[float, float, float]:
        return point[0], time, point[2]

    def pressure(point: tuple[float, float, float], time: float) -> float:
        return sum(point) + time

    transformed_velocity = viscosity_rescale_velocity(velocity, 4.0)
    transformed_pressure = viscosity_rescale_pressure(pressure, 4.0)
    transformed_force = viscosity_rescale_force(velocity, 4.0)
    assert transformed_velocity((2, 4, 6), 0.5) == pytest.approx((2, 1, 6))
    assert transformed_force((2, 4, 6), 0.5) == pytest.approx((2, 1, 6))
    assert transformed_pressure((2, 4, 6), 0.5) == pytest.approx(26.0)


@pytest.mark.parametrize("bad", [0.0, -1.0, float("inf"), float("nan")])
def test_rescaling_rejects_invalid_viscosity(bad: float) -> None:
    velocity, pressure, force = decaying_shear(1.0)
    with pytest.raises(ValueError, match="viscosity"):
        viscosity_rescale_velocity(velocity, bad)
    with pytest.raises(ValueError, match="viscosity"):
        viscosity_rescale_pressure(pressure, bad)
    with pytest.raises(ValueError, match="viscosity"):
        viscosity_rescale_force(force, bad)
