"""Evaluation of source-shaped leading fields in cylindrical coordinates."""

from __future__ import annotations

from collections.abc import Callable
from dataclasses import asdict, dataclass
from functools import partial
from math import atan2, cos, exp, isfinite, sin, sqrt

from nsrw.math_kernel.concentration import ConcentrationParameters
from nsrw.math_kernel.similarity import SimilarityCoordinates, reconstruct_similarity_coordinates
from nsrw.math_kernel.types import Point3, ScalarField, Vector3, VelocityField

Profile = Callable[[float, float], float]


def _constant_profile(value: float, _capital_x: float, _eta: float) -> float:
    return value


@dataclass(frozen=True)
class LeadingProfiles:
    azimuthal: Profile
    axial: Profile
    radial_flux: Profile
    pressure: Profile
    profile_id: str
    authority: str


@dataclass(frozen=True)
class LeadingFieldState:
    coordinates: SimilarityCoordinates
    radial_velocity: float
    azimuthal_velocity: float
    axial_velocity: float
    pressure: float

    def as_dict(self) -> dict[str, object]:
        return asdict(self)


def evaluate_leading_state(
    profiles: LeadingProfiles,
    parameters: ConcentrationParameters,
    radius: float,
    z: float,
    time: float,
) -> LeadingFieldState:
    if not (isfinite(radius) and radius >= 0):
        raise ValueError("radius must be finite and non-negative")
    tau = 1.0 - time
    coordinates = reconstruct_similarity_coordinates(
        tau, z, radius, float(parameters.h)
    )
    q = coordinates.q
    eta = coordinates.eta
    capital_x = coordinates.capital_x
    amplitude = q ** -float(parameters.amplitude_exponent)
    radial_flux = profiles.radial_flux(capital_x, eta)
    if radius == 0 and radial_flux != 0:
        raise ValueError("radial flux must vanish on the axis")
    radial_velocity = 0.0 if radius == 0 else radial_flux / radius
    return LeadingFieldState(
        coordinates=coordinates,
        radial_velocity=radial_velocity,
        azimuthal_velocity=amplitude * profiles.azimuthal(capital_x, eta),
        axial_velocity=amplitude * profiles.axial(capital_x, eta),
        pressure=q ** (-2.0 * float(parameters.amplitude_exponent))
        * profiles.pressure(capital_x, eta),
    )


def cartesian_velocity(
    profiles: LeadingProfiles, parameters: ConcentrationParameters
) -> VelocityField:
    def velocity(point: Point3, time: float) -> Vector3:
        x, y, z = point
        radius = sqrt(x * x + y * y)
        state = evaluate_leading_state(profiles, parameters, radius, z, time)
        if radius == 0:
            return 0.0, 0.0, state.axial_velocity
        angle = atan2(y, x)
        radial = state.radial_velocity
        azimuthal = state.azimuthal_velocity
        return (
            radial * cos(angle) - azimuthal * sin(angle),
            radial * sin(angle) + azimuthal * cos(angle),
            state.axial_velocity,
        )

    return velocity


def pressure_field(profiles: LeadingProfiles, parameters: ConcentrationParameters) -> ScalarField:
    def pressure(point: Point3, time: float) -> float:
        x, y, z = point
        return evaluate_leading_state(
            profiles, parameters, sqrt(x * x + y * y), z, time
        ).pressure

    return pressure


def toy_pure_swirl_profiles() -> LeadingProfiles:
    """Return a diagnostic fixture, not any profile asserted by the source paper."""

    def azimuthal(capital_x: float, _eta: float) -> float:
        return sqrt(2.0 * capital_x) * exp(-capital_x)

    def pressure(capital_x: float, _eta: float) -> float:
        return -0.5 * exp(-2.0 * capital_x)

    zero_profile = partial(_constant_profile, 0.0)
    return LeadingProfiles(
        azimuthal=azimuthal,
        axial=zero_profile,
        radial_flux=zero_profile,
        pressure=pressure,
        profile_id="toy-pure-swirl-v1",
        authority="MANUFACTURED_DIAGNOSTIC_NOT_SOURCE_PROFILE",
    )
