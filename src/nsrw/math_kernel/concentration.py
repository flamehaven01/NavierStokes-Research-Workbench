"""Exact exponent ledger for the paper's concentrating leading field."""

from __future__ import annotations

from dataclasses import dataclass
from fractions import Fraction


def _fraction_text(value: Fraction) -> str:
    if value.denominator == 1:
        return str(value.numerator)
    return f"{value.numerator}/{value.denominator}"


@dataclass(frozen=True)
class AffineHExponent:
    """An exact exponent of the form ``constant + h_coefficient*h``."""

    constant: Fraction = Fraction(0)
    h_coefficient: int = 0

    def evaluate(self, h: Fraction) -> Fraction:
        return self.constant + self.h_coefficient * h

    def as_text(self) -> str:
        constant = _fraction_text(self.constant)
        if self.h_coefficient == 0:
            return constant
        sign = "+" if self.h_coefficient > 0 else "-"
        coefficient = abs(self.h_coefficient)
        h_term = "h" if coefficient == 1 else f"{coefficient}h"
        if self.constant == 0:
            return h_term if sign == "+" else f"-{h_term}"
        return f"{constant} {sign} {h_term}"


@dataclass(frozen=True)
class ConcentrationParameters:
    h: Fraction

    def __post_init__(self) -> None:
        if not isinstance(self.h, Fraction):
            raise TypeError("h must be a Fraction for exact exponent algebra")
        if not 0 < self.h < Fraction(1, 100):
            raise ValueError("h must satisfy 0 < h < 1/100")

    @property
    def amplitude_exponent(self) -> Fraction:
        return Fraction(1, 2) + self.h

    @property
    def axial_exponent(self) -> Fraction:
        return Fraction(1, 2) - self.h


def concentration_exponent_ledger() -> dict[str, AffineHExponent]:
    """Derive the page-8 powers from ``A=1/2+h`` and ``D=1/2-h``."""
    return {
        "radial_length": AffineHExponent(Fraction(1, 2)),
        "axial_length": AffineHExponent(Fraction(1, 2), -1),
        "axial_to_radial_aspect": AffineHExponent(Fraction(0), -1),
        "azimuthal_velocity": AffineHExponent(Fraction(-1, 2), -1),
        "axial_velocity": AffineHExponent(Fraction(-1, 2), -1),
        "radial_velocity": AffineHExponent(Fraction(-1, 2)),
        "radial_to_azimuthal_velocity": AffineHExponent(Fraction(0), 1),
        "pressure": AffineHExponent(Fraction(-1), -2),
        "azimuthal_reynolds": AffineHExponent(Fraction(0), -1),
        "leading_transport_rate": AffineHExponent(Fraction(-1)),
        "radial_diffusion_rate": AffineHExponent(Fraction(-1)),
        "axial_to_radial_diffusion": AffineHExponent(Fraction(0), 2),
    }


def correction_exponent(order: int) -> AffineHExponent:
    """Return the exponent ``2*order*h`` used by the background expansion."""
    if order < 1:
        raise ValueError("correction order must be positive")
    return AffineHExponent(Fraction(0), 2 * order)


def render_exponent_ledger(h: Fraction) -> dict[str, dict[str, str]]:
    return {
        name: {"symbolic": exponent.as_text(), "at_h": _fraction_text(exponent.evaluate(h))}
        for name, exponent in concentration_exponent_ledger().items()
    }
