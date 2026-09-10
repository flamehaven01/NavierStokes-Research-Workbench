from __future__ import annotations

from fractions import Fraction
from math import exp, sqrt

import pytest

from nsrw.math_kernel.concentration import ConcentrationParameters
from nsrw.math_kernel.leading_field import (
    LeadingProfiles,
    cartesian_velocity,
    evaluate_leading_state,
    pressure_field,
    toy_pure_swirl_profiles,
)

PARAMETERS = ConcentrationParameters(Fraction(1, 200))


def test_toy_profile_evaluates_source_shaped_leading_field() -> None:
    profiles = toy_pure_swirl_profiles()
    tau = 0.2
    capital_x = 0.5
    radius = sqrt(2 * tau * capital_x)
    state = evaluate_leading_state(profiles, PARAMETERS, radius, 0.0, 1 - tau)
    assert state.coordinates.q == pytest.approx(tau)
    assert state.coordinates.capital_x == pytest.approx(capital_x)
    expected_e = sqrt(2 * capital_x) * exp(-capital_x)
    assert state.azimuthal_velocity == pytest.approx(
        tau ** -float(PARAMETERS.amplitude_exponent) * expected_e
    )
    assert state.radial_velocity == 0.0
    assert state.axial_velocity == 0.0
    assert state.as_dict()["coordinates"]["eta"] == pytest.approx(0.0)
    assert profiles.authority == "MANUFACTURED_DIAGNOSTIC_NOT_SOURCE_PROFILE"


def test_axis_requires_zero_radial_flux() -> None:
    profiles = toy_pure_swirl_profiles()
    state = evaluate_leading_state(profiles, PARAMETERS, 0.0, 0.0, 0.8)
    assert state.radial_velocity == 0.0
    assert state.azimuthal_velocity == 0.0

    invalid = LeadingProfiles(
        profiles.azimuthal,
        profiles.axial,
        lambda _x, _eta: 1.0,
        profiles.pressure,
        "invalid-axis",
        "TEST_MUTATION",
    )
    with pytest.raises(ValueError, match="vanish on the axis"):
        evaluate_leading_state(invalid, PARAMETERS, 0.0, 0.0, 0.8)


def test_cartesian_velocity_converts_cylindrical_basis() -> None:
    velocity = cartesian_velocity(toy_pure_swirl_profiles(), PARAMETERS)
    at_positive_x = velocity((0.4, 0.0, 0.0), 0.8)
    at_positive_y = velocity((0.0, 0.4, 0.0), 0.8)
    assert at_positive_x[0] == pytest.approx(0.0)
    assert at_positive_x[1] > 0
    assert at_positive_y[0] == pytest.approx(-at_positive_x[1])
    assert at_positive_y[1] == pytest.approx(0.0, abs=1e-12)
    assert velocity((0.0, 0.0, 0.0), 0.8) == pytest.approx((0.0, 0.0, 0.0))


def test_pressure_field_matches_leading_state() -> None:
    profiles = toy_pure_swirl_profiles()
    pressure = pressure_field(profiles, PARAMETERS)
    point = (0.4, 0.0, 0.0)
    state = evaluate_leading_state(profiles, PARAMETERS, 0.4, 0.0, 0.8)
    assert pressure(point, 0.8) == pytest.approx(state.pressure)


@pytest.mark.parametrize("radius", [-0.1, float("inf")])
def test_leading_state_rejects_bad_radius(radius: float) -> None:
    with pytest.raises(ValueError, match="radius"):
        evaluate_leading_state(toy_pure_swirl_profiles(), PARAMETERS, radius, 0.0, 0.8)


def test_leading_state_rejects_singular_or_later_time() -> None:
    with pytest.raises(ValueError, match="tau"):
        evaluate_leading_state(toy_pure_swirl_profiles(), PARAMETERS, 0.2, 0.0, 1.0)
