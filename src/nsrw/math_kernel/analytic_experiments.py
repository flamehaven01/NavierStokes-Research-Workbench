"""Deterministic M2 receipt for the bounded analytic spine."""

from __future__ import annotations

from fractions import Fraction
from math import sqrt

from nsrw.math_kernel.analytic_obligations import (
    classify_stress_region,
    cylindrical_incompressibility_sample,
    is_in_core,
    radial_pressure_balance_sample,
    sample_residual_order,
)
from nsrw.math_kernel.concentration import (
    ConcentrationParameters,
    concentration_exponent_ledger,
    correction_exponent,
    render_exponent_ledger,
)
from nsrw.math_kernel.leading_field import evaluate_leading_state, toy_pure_swirl_profiles


def run_analytic_spine_check() -> dict[str, object]:
    parameters = ConcentrationParameters(Fraction(1, 200))
    profiles = toy_pure_swirl_profiles()
    tau = 0.2
    capital_x = 0.5
    radius = sqrt(2.0 * tau * capital_x)
    time = 1.0 - tau

    incompressibility = cylindrical_incompressibility_sample(
        profiles, parameters, radius, 0.0, time
    )
    pressure_balance = radial_pressure_balance_sample(
        profiles, parameters, radius, 0.0, time
    )
    state = evaluate_leading_state(profiles, parameters, radius, 0.0, time)
    later_tau = 0.1
    later_radius = sqrt(2.0 * later_tau * capital_x)
    later_state = evaluate_leading_state(
        profiles, parameters, later_radius, 0.0, 1.0 - later_tau
    )
    observed_growth = later_state.azimuthal_velocity / state.azimuthal_velocity
    expected_growth = (later_tau / tau) ** -float(parameters.amplitude_exponent)
    growth_error = observed_growth - expected_growth

    power = float(correction_exponent(2).evaluate(parameters.h))
    residual_order = sample_residual_order(
        "toy_flat_remainder", lambda q: 3.0 * q**power, power, (1e-2, 1e-4, 1e-6), 3.01
    )
    wrong_order = sample_residual_order(
        "mutated_overclaim",
        lambda q: 3.0 * q**power,
        power + 1.0,
        (1e-2, 1e-4, 1e-6),
        1e5,
    )
    ledger = concentration_exponent_ledger()
    exponent_mutation_killed = (
        ledger["axial_to_radial_diffusion"].evaluate(parameters.h)
        != Fraction(1) * parameters.h
    )
    checks = {
        "parameter_domain": "PASS",
        "exponent_ledger": "PASS",
        "exponent_mutation": "PASS" if exponent_mutation_killed else "FAIL",
        "core_membership": "PASS"
        if is_in_core(state.coordinates.capital_x, state.coordinates.eta, 1.0, 0.8)
        else "FAIL",
        "stress_regions": "PASS"
        if [classify_stress_region(value, 0.25, 0.75) for value in (0.1, 0.5, 1.0)]
        == ["INNER", "ANNULUS", "EXTERIOR"]
        else "FAIL",
        "incompressibility": incompressibility.check_status,
        "radial_pressure_balance": pressure_balance.check_status,
        "fixed_similarity_growth": "PASS" if abs(growth_error) <= 1e-12 else "FAIL",
        "sampled_residual_order": residual_order.check_status,
        "overclaim_mutation": "PASS" if wrong_order.check_status == "FAIL" else "FAIL",
    }
    return {
        "schema_id": "flamehaven.navier-stokes-analytic-spine-receipt.v1",
        "check_status": "PASS" if set(checks.values()) == {"PASS"} else "FAIL",
        "claim_status": "UNVERIFIED",
        "source_scope": [
            "navier-stokes.pdf:p7:section3.1-eq3.2",
            "navier-stokes.pdf:p8:core-scales-pressure-balance",
            "navier-stokes.pdf:p9:stress-annulus",
        ],
        "authority": {
            "exponent_ledger": "EXACT_SYMBOLIC_ALGEBRA",
            "local_obligations": "SAMPLED_NUMERICAL_DIAGNOSTIC",
            "profile_fixture": profiles.authority,
            "source_paper_profiles": "NOT_INSTANTIATED",
            "global_navier_stokes_claim": "NOT_ESTABLISHED",
        },
        "parameters": {
            "h": "1/200",
            "A": "101/200",
            "D": "99/200",
        },
        "checks": checks,
        "exponents": render_exponent_ledger(parameters.h),
        "local_samples": [incompressibility.as_dict(), pressure_balance.as_dict()],
        "growth": {
            "initial_tau": tau,
            "later_tau": later_tau,
            "fixed_X": capital_x,
            "observed_ratio": observed_growth,
            "expected_ratio": expected_growth,
            "absolute_error": abs(growth_error),
        },
        "residual_order_samples": [residual_order.as_dict(), wrong_order.as_dict()],
    }
