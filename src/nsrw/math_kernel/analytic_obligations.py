"""Bounded analytic obligations for the concentrating leading-field interface."""

from __future__ import annotations

from collections.abc import Callable, Sequence
from dataclasses import dataclass
from math import isfinite

from nsrw.math_kernel.concentration import ConcentrationParameters
from nsrw.math_kernel.leading_field import LeadingProfiles, evaluate_leading_state


class SerializableSample:
    def as_dict(self) -> dict[str, object]:
        return dict(vars(self))


@dataclass(frozen=True)
class LocalObligationSample(SerializableSample):
    name: str
    value: float
    tolerance: float
    check_status: str
    evidence_class: str = "SAMPLED_NUMERICAL_DIAGNOSTIC"

@dataclass(frozen=True)
class ResidualOrderSample(SerializableSample):
    label: str
    claimed_power: float
    maximum_normalized_value: float
    bound: float
    sample_count: int
    derivative_multi_index: tuple[int, int, int]
    time_derivative_order: int
    check_status: str
    evidence_class: str = "FINITE_ASYMPTOTIC_SAMPLE_NOT_PROOF"

def classify_stress_region(capital_x: float, inner: float, outer: float) -> str:
    if not (isfinite(capital_x) and isfinite(inner) and isfinite(outer)):
        raise ValueError("stress-region inputs must be finite")
    if not 0 < inner < outer:
        raise ValueError("stress annulus must satisfy 0 < inner < outer")
    if capital_x <= inner:
        return "INNER"
    if capital_x < outer:
        return "ANNULUS"
    return "EXTERIOR"


def is_in_core(capital_x: float, eta: float, max_x: float, max_abs_eta: float) -> bool:
    if not (0 < max_x and 0 < max_abs_eta < 1):
        raise ValueError("core bounds require max_x > 0 and 0 < max_abs_eta < 1")
    return 0 <= capital_x <= max_x and abs(eta) <= max_abs_eta


def cylindrical_incompressibility_sample(
    profiles: LeadingProfiles,
    parameters: ConcentrationParameters,
    radius: float,
    z: float,
    time: float,
    step: float = 1e-5,
    tolerance: float = 1e-7,
) -> LocalObligationSample:
    _validate_local_sample(radius, time, step, tolerance)

    def radial_flux(sample_radius: float) -> float:
        state = evaluate_leading_state(profiles, parameters, sample_radius, z, time)
        return sample_radius * state.radial_velocity

    def axial_velocity(sample_z: float) -> float:
        return evaluate_leading_state(profiles, parameters, radius, sample_z, time).axial_velocity

    radial_term = (radial_flux(radius + step) - radial_flux(radius - step)) / (2 * step * radius)
    axial_term = (axial_velocity(z + step) - axial_velocity(z - step)) / (2 * step)
    value = radial_term + axial_term
    return _local_sample("cylindrical_incompressibility", value, tolerance)


def radial_pressure_balance_sample(
    profiles: LeadingProfiles,
    parameters: ConcentrationParameters,
    radius: float,
    z: float,
    time: float,
    step: float = 1e-5,
    tolerance: float = 1e-5,
) -> LocalObligationSample:
    _validate_local_sample(radius, time, step, tolerance)
    plus = evaluate_leading_state(profiles, parameters, radius + step, z, time).pressure
    minus = evaluate_leading_state(profiles, parameters, radius - step, z, time).pressure
    derivative = (plus - minus) / (2 * step)
    azimuthal = evaluate_leading_state(
        profiles, parameters, radius, z, time
    ).azimuthal_velocity
    value = derivative - azimuthal * azimuthal / radius
    return _local_sample("radial_pressure_balance", value, tolerance)


def sample_residual_order(
    label: str,
    value_at_q: Callable[[float], float],
    claimed_power: float,
    q_samples: Sequence[float],
    bound: float,
    derivative_multi_index: tuple[int, int, int] = (0, 0, 0),
    time_derivative_order: int = 0,
) -> ResidualOrderSample:
    if not q_samples or any(not isfinite(q) or q <= 0 for q in q_samples):
        raise ValueError("q samples must be finite and positive")
    if not isfinite(claimed_power) or not isfinite(bound) or bound <= 0:
        raise ValueError("claimed power and positive bound must be finite")
    if any(index < 0 for index in derivative_multi_index) or time_derivative_order < 0:
        raise ValueError("derivative orders must be non-negative")
    normalized = [abs(value_at_q(q)) / q**claimed_power for q in q_samples]
    maximum = max(normalized)
    return ResidualOrderSample(
        label=label,
        claimed_power=claimed_power,
        maximum_normalized_value=maximum,
        bound=bound,
        sample_count=len(q_samples),
        derivative_multi_index=derivative_multi_index,
        time_derivative_order=time_derivative_order,
        check_status="PASS" if maximum <= bound else "FAIL",
    )


def _validate_local_sample(radius: float, time: float, step: float, tolerance: float) -> None:
    if not (isfinite(radius) and radius > step > 0):
        raise ValueError("radius must be finite and greater than the positive step")
    if not (isfinite(time) and time + step < 1):
        raise ValueError("time must be finite and remain below the singular time")
    if not (isfinite(tolerance) and tolerance > 0):
        raise ValueError("tolerance must be finite and positive")


def _local_sample(name: str, value: float, tolerance: float) -> LocalObligationSample:
    return LocalObligationSample(
        name=name,
        value=value,
        tolerance=tolerance,
        check_status="PASS" if abs(value) <= tolerance else "FAIL",
    )
