"""Numerical closure of the source-shaped profile identities from Section 4.

This module is deliberately a bounded diagnostic.  It derives ``V0`` and the
canonical pressure from ``U`` and ``E`` instead of accepting four unrelated
profiles.  The resulting samples are evidence for the identities only; they
are not a proof of Theorem 4.6 or of the Navier--Stokes millennium claim.
"""

from __future__ import annotations

import hashlib
import json
import re
from collections.abc import Callable
from dataclasses import asdict, dataclass
from fractions import Fraction
from math import exp, isfinite, sqrt
from pathlib import Path

from nsrw.math_kernel.concentration import ConcentrationParameters
from nsrw.math_kernel.leading_field import LeadingProfiles

Profile = Callable[[float, float], float]
TailIntegral = Callable[[float], float]


@dataclass(frozen=True)
class QuadratureSpec:
    """Deterministic composite-Simpson settings."""

    panels: int = 256

    def __post_init__(self) -> None:
        if self.panels <= 0 or self.panels % 2:
            raise ValueError("Simpson panels must be a positive even integer")


DEFAULT_QUADRATURE = QuadratureSpec()


@dataclass(frozen=True)
class ClosureSample:
    name: str
    value: float
    expected: float
    absolute_error: float
    tolerance: float
    check_status: str
    evidence_class: str = "BOUNDED_NUMERICAL_CLOSURE_DIAGNOSTIC"

    def as_dict(self) -> dict[str, object]:
        return asdict(self)


@dataclass(frozen=True)
class ClosedLeadingProfiles:
    """A profile bundle with source identities derived, not independently supplied."""

    azimuthal: Profile
    axial: Profile
    h: Fraction
    pressure_cutoff: float
    pressure_tail: TailIntegral
    axis_integrand_limit: Callable[[float], float] | None = None
    quadrature: QuadratureSpec = QuadratureSpec()
    profile_id: str = "closed-leading-profile-v1"
    authority: str = "MANUFACTURED_CLOSURE_DIAGNOSTIC_NOT_SOURCE_WITNESS"

    def __post_init__(self) -> None:
        ConcentrationParameters(self.h)
        if not (isfinite(self.pressure_cutoff) and self.pressure_cutoff > 0):
            raise ValueError("pressure cutoff must be finite and positive")

    def radial_flux(self, capital_x: float, eta: float) -> float:
        return derived_radial_flux(self.axial, self.h, capital_x, eta, self.quadrature)

    def pressure(self, capital_x: float, eta: float) -> float:
        return canonical_pressure(
            self.azimuthal,
            capital_x,
            eta,
            self.pressure_cutoff,
            self.pressure_tail,
            self.quadrature,
            axis_integrand_limit=self.axis_integrand_limit,
        )

    def as_leading_profiles(self) -> LeadingProfiles:
        return LeadingProfiles(
            azimuthal=self.azimuthal,
            axial=self.axial,
            radial_flux=self.radial_flux,
            pressure=self.pressure,
            profile_id=self.profile_id,
            authority=self.authority,
        )


def _validate_point(capital_x: float, eta: float) -> None:
    if not (isfinite(capital_x) and capital_x >= 0):
        raise ValueError("X must be finite and non-negative")
    if not (isfinite(eta) and -1 <= eta <= 1):
        raise ValueError("eta must lie in [-1, 1]")


def _simpson(function: Callable[[float], float], lower: float, upper: float, spec: QuadratureSpec) -> float:
    if lower == upper:
        return 0.0
    if not (isfinite(lower) and isfinite(upper) and lower < upper):
        raise ValueError("Simpson interval must be finite with lower < upper")
    step = (upper - lower) / spec.panels
    total = function(lower) + function(upper)
    total += 4.0 * sum(function(lower + index * step) for index in range(1, spec.panels, 2))
    total += 2.0 * sum(function(lower + index * step) for index in range(2, spec.panels, 2))
    value = total * step / 3.0
    if not isfinite(value):
        raise ArithmeticError("quadrature produced a non-finite value")
    return value


def radial_average(
    field: Profile, capital_x: float, eta: float, spec: QuadratureSpec = DEFAULT_QUADRATURE
) -> float:
    """Equation (4.6), including its continuous axis extension."""

    _validate_point(capital_x, eta)
    if capital_x == 0:
        return field(0.0, eta)
    return _simpson(lambda radial_x: field(radial_x, eta), 0.0, capital_x, spec) / capital_x


def parameter_derivative_of_average(
    field: Profile,
    capital_x: float,
    eta: float,
    step: float = 1e-5,
    spec: QuadratureSpec = DEFAULT_QUADRATURE,
) -> float:
    """A finite-difference diagnostic for the ``eta`` derivative in (4.7)."""

    _validate_point(capital_x, eta)
    if not (isfinite(step) and step > 0):
        raise ValueError("eta derivative step must be finite and positive")
    if eta == -1.0:
        if eta + 2.0 * step > 1.0:
            raise ValueError("eta derivative step must stay inside [-1, 1]")
        left = radial_average(field, capital_x, eta, spec)
        middle = radial_average(field, capital_x, eta + step, spec)
        right = radial_average(field, capital_x, eta + 2.0 * step, spec)
        return (-3.0 * left + 4.0 * middle - right) / (2.0 * step)
    if eta == 1.0:
        if eta - 2.0 * step < -1.0:
            raise ValueError("eta derivative step must stay inside [-1, 1]")
        left = radial_average(field, capital_x, eta - 2.0 * step, spec)
        middle = radial_average(field, capital_x, eta - step, spec)
        right = radial_average(field, capital_x, eta, spec)
        return (3.0 * right - 4.0 * middle + left) / (2.0 * step)
    if eta - step < -1.0 or eta + step > 1.0:
        raise ValueError("eta derivative step must stay inside [-1, 1]")
    return (
        radial_average(field, capital_x, eta + step, spec)
        - radial_average(field, capital_x, eta - step, spec)
    ) / (2.0 * step)


def derived_radial_flux(
    axial: Profile,
    h: Fraction,
    capital_x: float,
    eta: float,
    spec: QuadratureSpec = DEFAULT_QUADRATURE,
) -> float:
    """Equation (4.7)'s incompressibility-derived ``V0``."""

    _validate_point(capital_x, eta)
    ConcentrationParameters(h)
    if capital_x == 0:
        return 0.0
    h_value = float(h)
    D = 0.5 - h_value
    d = 1.0 - eta * eta
    L = 1.0 - 2.0 * h_value * eta * eta
    average = radial_average(axial, capital_x, eta, spec)
    derivative = parameter_derivative_of_average(axial, capital_x, eta, spec=spec)
    return capital_x / L * (2.0 * eta * average - 2.0 * D * eta * average - d * derivative)


def canonical_pressure(
    azimuthal: Profile,
    capital_x: float,
    eta: float,
    cutoff: float,
    tail_integral: TailIntegral,
    spec: QuadratureSpec = DEFAULT_QUADRATURE,
    *,
    axis_integrand_limit: Callable[[float], float] | None = None,
) -> float:
    """Equation (4.25), with the omitted infinite tail supplied explicitly."""

    _validate_point(capital_x, eta)
    if not (isfinite(cutoff) and cutoff > 0 and capital_x <= cutoff):
        raise ValueError("X must satisfy 0 <= X <= the positive pressure cutoff")
    tail = tail_integral(eta)
    if not isfinite(tail):
        raise ValueError("pressure tail must be finite")

    def integrand(radial_x: float) -> float:
        value = azimuthal(radial_x, eta)
        if radial_x == 0:
            if axis_integrand_limit is None:
                raise ValueError("X=0 requires an explicit pressure integrand limit")
            limit = axis_integrand_limit(eta)
            if not isfinite(limit):
                raise ValueError("pressure integrand limit must be finite")
            return limit
        return value * value / (2.0 * radial_x)

    return -(_simpson(integrand, capital_x, cutoff, spec) + tail)


def pressure_balance_sample(
    azimuthal: Profile,
    pressure: Callable[[float, float], float],
    capital_x: float,
    eta: float,
    step: float = 1e-5,
    tolerance: float = 1e-5,
) -> ClosureSample:
    """Check ``Pi_X=E^2/(2X)`` at a positive X by centered differences."""

    _validate_point(capital_x, eta)
    if not (capital_x > step > 0 and isfinite(tolerance) and tolerance > 0):
        raise ValueError("pressure sample requires X > step > 0 and positive tolerance")
    derivative = (pressure(capital_x + step, eta) - pressure(capital_x - step, eta)) / (2.0 * step)
    expected = azimuthal(capital_x, eta) ** 2 / (2.0 * capital_x)
    return _sample("pressure_balance", derivative, expected, tolerance)


def _sample(name: str, value: float, expected: float, tolerance: float) -> ClosureSample:
    error = abs(value - expected)
    return ClosureSample(name, value, expected, error, tolerance, "PASS" if error <= tolerance else "FAIL")


def audit_lean_crosswalk(lean_root: Path) -> dict[str, object]:
    """Locate source declarations without treating text presence as a proof build."""

    required = {
        "average": ("NavierStokes/ProfileHistories.lean", "def", "average"),
        "radial_flux": ("NavierStokes/SlowDivergence.lean", "def", "radialFlux"),
        "pressure_derivative": ("NavierStokes/ProfileHistories.lean", "theorem", "radialPartial_pressure"),
        "canonical_pressure": ("NavierStokes/NominalProfile.lean", "theorem", "pressure_canonical"),
        "candidate_statement": ("NavierStokes/ProblemStatement.lean", "def", "candidateStatement"),
        "selected_candidate": ("NavierStokes/ActualCandidateAssembly.lean", "theorem", "selected_candidate"),
    }
    entries: list[dict[str, object]] = []
    for key, (relative, kind, name) in required.items():
        path = lean_root / relative
        exists = path.is_file()
        text = path.read_text(encoding="utf-8") if exists else ""
        marker = rf"^\s*(?:noncomputable\s+)?{kind}\s+{re.escape(name)}\b"
        present = re.search(marker, text, flags=re.MULTILINE) is not None
        entries.append(
            {
                "key": key,
                "relative_path": relative,
                "declaration": f"{kind} {name}",
                "status": "PRESENT" if present else ("ABSENT" if exists else "UNAVAILABLE"),
                "sha256": hashlib.sha256(path.read_bytes()).hexdigest().upper() if exists else None,
            }
        )
    return {
        "evidence_class": "STATIC_FORMAL_SOURCE_LOCATOR_NOT_BUILD_PROOF",
        "lean_root": str(lean_root),
        "entries": entries,
        "build_status": "UNAVAILABLE_TOOLCHAIN_NOT_EXECUTED",
    }


def run_m3_self_check() -> dict[str, object]:
    """Run deterministic manufactured closure samples used by the M3 receipt."""

    spec = QuadratureSpec(256)
    h = Fraction(1, 200)

    def E(capital_x: float, _eta: float) -> float:
        return sqrt(2.0 * capital_x) * exp(-capital_x)

    def U(capital_x: float, eta: float) -> float:
        # A smooth affine fixture exercises both the average and eta-derivative
        # terms in (4.7); it is not a source-paper profile.
        return 1.0 + 0.1 * capital_x + 0.03 * eta

    cutoff = 8.0
    closed = ClosedLeadingProfiles(
        E,
        U,
        h,
        cutoff,
        lambda _eta: 0.5 * exp(-2.0 * cutoff),
        lambda _eta: 1.0,
        spec,
    )
    flux = closed.radial_flux(0.75, 0.2)
    average = 1.0 + 0.1 * 0.75 / 2.0 + 0.03 * 0.2
    h_value = float(h)
    expected_flux = 0.75 / (1.0 - 2.0 * h_value * 0.2 * 0.2) * (
        (1.0 + 2.0 * h_value) * 0.2 * average - (1.0 - 0.2 * 0.2) * 0.03
    )
    samples = [
        _sample("derived_radial_flux", flux, expected_flux, 2e-8),
        pressure_balance_sample(E, closed.pressure, 0.75, 0.2, tolerance=2e-6),
    ]
    return {
        "schema_id": "flamehaven.navier-stokes-m3-closure-receipt.v1",
        "stage": "M3",
        "check_status": "PASS" if all(s.check_status == "PASS" for s in samples) else "FAIL",
        "claim_status": "UNVERIFIED",
        "evidence_class": "BOUNDED_NUMERICAL_CLOSURE_DIAGNOSTIC",
        "profile_id": closed.profile_id,
        "samples": [sample.as_dict() for sample in samples],
        "non_claims": [
            "No Theorem 4.6 existence or cone estimate is established.",
            "No Lean build or paper-Lean semantic equivalence is established.",
            "The manufactured profiles are not the source paper's witness.",
        ],
    }


def render_m3_receipt(receipt: dict[str, object]) -> str:
    return json.dumps(receipt, indent=2, sort_keys=True) + "\n"
