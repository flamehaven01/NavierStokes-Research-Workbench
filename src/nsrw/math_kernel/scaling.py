"""Exact scaling exponents and field transformations from the source paper."""

from __future__ import annotations

from dataclasses import dataclass
from fractions import Fraction
from math import isfinite, sqrt

from nsrw.math_kernel.types import ForceField, Point3, ScalarField, VelocityField, scale


def _fraction_text(value: Fraction) -> str:
    return str(value.numerator) if value.denominator == 1 else f"{value.numerator}/{value.denominator}"


@dataclass(frozen=True)
class ScalingCertificate:
    name: str
    source_locator: str
    term_exponents: dict[str, Fraction]
    invariant_exponents: dict[str, Fraction]
    evidence_class: str = "EXACT_EXPONENT_ALGEBRA"
    claim_status: str = "SUPPORTED"

    @property
    def momentum_terms_match(self) -> bool:
        return len(set(self.term_exponents.values())) == 1

    def as_dict(self) -> dict[str, object]:
        return {
            "name": self.name,
            "source_locator": self.source_locator,
            "term_exponents": {
                key: _fraction_text(value) for key, value in self.term_exponents.items()
            },
            "invariant_exponents": {
                key: _fraction_text(value) for key, value in self.invariant_exponents.items()
            },
            "momentum_terms_match": self.momentum_terms_match,
            "evidence_class": self.evidence_class,
            "claim_status": self.claim_status,
        }


@dataclass(frozen=True)
class ScalingLaw:
    """Powers for ``u=a U(bx,ct)``, ``p=d P(bx,ct)``, and ``f=e F(bx,ct)``."""

    velocity: Fraction
    space_argument: Fraction
    time_argument: Fraction
    pressure: Fraction
    force: Fraction
    viscosity_coefficient: Fraction

    def certify(self, name: str, source_locator: str) -> ScalingCertificate:
        velocity = self.velocity
        space = self.space_argument
        time = self.time_argument
        vorticity = velocity + space
        return ScalingCertificate(
            name=name,
            source_locator=source_locator,
            term_exponents={
                "time_derivative": velocity + time,
                "convection": 2 * velocity + space,
                "viscous_laplacian": self.viscosity_coefficient + velocity + 2 * space,
                "pressure_gradient": self.pressure + space,
                "force": self.force,
            },
            invariant_exponents={
                "divergence_amplitude": velocity + space,
                "vorticity_linf": vorticity,
                "bkm_time_integral": vorticity - time,
                "energy_squared": 2 * velocity - 3 * space,
                "viscous_dissipation": (
                    self.viscosity_coefficient + 2 * vorticity - 3 * space - time
                ),
            },
        )


def viscosity_scaling_certificate() -> ScalingCertificate:
    """Certify the powers in paper equations (10.22)--(10.23)."""
    half = Fraction(1, 2)
    law = ScalingLaw(
        velocity=half,
        space_argument=-half,
        time_argument=Fraction(0),
        pressure=Fraction(1),
        force=half,
        viscosity_coefficient=Fraction(1),
    )
    return law.certify(
        name="viscosity_rescaling",
        source_locator="navier-stokes.pdf:p124:eq10.22-eq10.23",
    )


def periodic_scaling_certificate() -> ScalingCertificate:
    """Certify the parabolic powers used before periodization on paper page 125."""
    law = ScalingLaw(
        velocity=Fraction(1),
        space_argument=Fraction(1),
        time_argument=Fraction(2),
        pressure=Fraction(2),
        force=Fraction(3),
        viscosity_coefficient=Fraction(0),
    )
    return law.certify(
        name="parabolic_periodic_embedding",
        source_locator="navier-stokes.pdf:p125:periodic-scaling",
    )


def viscosity_rescale_velocity(velocity: VelocityField, viscosity: float) -> VelocityField:
    root = _positive_root(viscosity)

    def transformed(point: Point3, time: float) -> tuple[float, float, float]:
        source_point = point[0] / root, point[1] / root, point[2] / root
        return scale(root, velocity(source_point, time))

    return transformed


def viscosity_rescale_pressure(pressure: ScalarField, viscosity: float) -> ScalarField:
    root = _positive_root(viscosity)

    def transformed(point: Point3, time: float) -> float:
        source_point = point[0] / root, point[1] / root, point[2] / root
        return viscosity * pressure(source_point, time)

    return transformed


def viscosity_rescale_force(force: ForceField, viscosity: float) -> ForceField:
    root = _positive_root(viscosity)

    def transformed(point: Point3, time: float) -> tuple[float, float, float]:
        source_point = point[0] / root, point[1] / root, point[2] / root
        return scale(root, force(source_point, time))

    return transformed


def _positive_root(value: float) -> float:
    if not isfinite(value) or value <= 0:
        raise ValueError("viscosity must be finite and positive")
    return sqrt(value)
