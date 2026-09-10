from __future__ import annotations

from fractions import Fraction

import pytest

from nsrw.math_kernel.analytic_obligations import (
    classify_stress_region,
    cylindrical_incompressibility_sample,
    is_in_core,
    radial_pressure_balance_sample,
    sample_residual_order,
)
from nsrw.math_kernel.concentration import ConcentrationParameters
from nsrw.math_kernel.leading_field import LeadingProfiles, toy_pure_swirl_profiles

PARAMETERS = ConcentrationParameters(Fraction(1, 200))
PROFILES = toy_pure_swirl_profiles()


def test_stress_region_classification() -> None:
    assert classify_stress_region(0.1, 0.25, 0.75) == "INNER"
    assert classify_stress_region(0.25, 0.25, 0.75) == "INNER"
    assert classify_stress_region(0.5, 0.25, 0.75) == "ANNULUS"
    assert classify_stress_region(0.75, 0.25, 0.75) == "EXTERIOR"


@pytest.mark.parametrize(
    "values",
    [(0.1, 0.0, 0.75), (0.1, 0.8, 0.75), (float("nan"), 0.25, 0.75)],
)
def test_stress_region_rejects_invalid_bounds(values: tuple[float, float, float]) -> None:
    with pytest.raises(ValueError):
        classify_stress_region(*values)


def test_core_membership_and_bounds() -> None:
    assert is_in_core(0.5, -0.4, 1.0, 0.8)
    assert not is_in_core(1.1, 0.0, 1.0, 0.8)
    assert not is_in_core(0.5, 0.9, 1.0, 0.8)
    with pytest.raises(ValueError, match="core bounds"):
        is_in_core(0.5, 0.0, 0.0, 0.8)


def test_toy_profile_local_obligations_pass() -> None:
    incompressibility = cylindrical_incompressibility_sample(
        PROFILES, PARAMETERS, 0.4, 0.0, 0.8
    )
    pressure = radial_pressure_balance_sample(PROFILES, PARAMETERS, 0.4, 0.0, 0.8)
    assert incompressibility.check_status == "PASS"
    assert incompressibility.value == pytest.approx(0.0)
    assert pressure.check_status == "PASS"
    assert abs(pressure.value) < pressure.tolerance
    assert pressure.as_dict()["evidence_class"] == "SAMPLED_NUMERICAL_DIAGNOSTIC"


def test_incompressibility_mutation_fails() -> None:
    mutated = LeadingProfiles(
        PROFILES.azimuthal,
        lambda _x, eta: eta,
        PROFILES.radial_flux,
        PROFILES.pressure,
        "mutated-axial",
        "TEST_MUTATION",
    )
    sample = cylindrical_incompressibility_sample(
        mutated, PARAMETERS, 0.4, 0.0, 0.8, tolerance=1e-5
    )
    assert sample.check_status == "FAIL"


def test_pressure_mutation_fails() -> None:
    mutated = LeadingProfiles(
        PROFILES.azimuthal,
        PROFILES.axial,
        PROFILES.radial_flux,
        lambda _x, _eta: 0.0,
        "mutated-pressure",
        "TEST_MUTATION",
    )
    sample = radial_pressure_balance_sample(
        mutated, PARAMETERS, 0.4, 0.0, 0.8, tolerance=1e-5
    )
    assert sample.check_status == "FAIL"


def test_residual_order_sample_distinguishes_supported_and_overclaimed_power() -> None:
    supported = sample_residual_order(
        "supported", lambda q: 2 * q**0.5, 0.5, (1e-2, 1e-4), 2.01
    )
    overclaimed = sample_residual_order(
        "overclaimed", lambda q: 2 * q**0.5, 1.5, (1e-2, 1e-4), 1e3
    )
    assert supported.check_status == "PASS"
    assert supported.maximum_normalized_value == pytest.approx(2.0)
    assert supported.as_dict()["sample_count"] == 2
    assert overclaimed.check_status == "FAIL"


@pytest.mark.parametrize(
    "kwargs",
    [
        {"q_samples": (), "claimed_power": 1.0, "bound": 1.0},
        {"q_samples": (0.0,), "claimed_power": 1.0, "bound": 1.0},
        {"q_samples": (0.1,), "claimed_power": float("inf"), "bound": 1.0},
        {"q_samples": (0.1,), "claimed_power": 1.0, "bound": 0.0},
        {
            "q_samples": (0.1,),
            "claimed_power": 1.0,
            "bound": 1.0,
            "derivative_multi_index": (-1, 0, 0),
        },
        {
            "q_samples": (0.1,),
            "claimed_power": 1.0,
            "bound": 1.0,
            "time_derivative_order": -1,
        },
    ],
)
def test_residual_order_rejects_invalid_contract(kwargs: dict[str, object]) -> None:
    with pytest.raises(ValueError):
        sample_residual_order("invalid", lambda q: q, **kwargs)  # type: ignore[arg-type]


@pytest.mark.parametrize(
    "call",
    [
        lambda: cylindrical_incompressibility_sample(PROFILES, PARAMETERS, 1e-6, 0, 0.8),
        lambda: cylindrical_incompressibility_sample(PROFILES, PARAMETERS, 0.4, 0, 1.0),
        lambda: radial_pressure_balance_sample(
            PROFILES, PARAMETERS, 0.4, 0, 0.8, tolerance=0
        ),
    ],
)
def test_local_obligations_reject_invalid_sampling(call) -> None:
    with pytest.raises(ValueError):
        call()
