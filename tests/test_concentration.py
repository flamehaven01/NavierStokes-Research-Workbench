from __future__ import annotations

from fractions import Fraction

import pytest

from nsrw.math_kernel.concentration import (
    AffineHExponent,
    ConcentrationParameters,
    concentration_exponent_ledger,
    correction_exponent,
    render_exponent_ledger,
)


def test_concentration_parameters_are_exact() -> None:
    parameters = ConcentrationParameters(Fraction(1, 200))
    assert parameters.amplitude_exponent == Fraction(101, 200)
    assert parameters.axial_exponent == Fraction(99, 200)


@pytest.mark.parametrize("bad", [Fraction(0), Fraction(1, 100), Fraction(-1, 200)])
def test_concentration_parameters_reject_out_of_range_h(bad: Fraction) -> None:
    with pytest.raises(ValueError, match="0 < h"):
        ConcentrationParameters(bad)


def test_concentration_parameters_require_fraction() -> None:
    with pytest.raises(TypeError, match="Fraction"):
        ConcentrationParameters(0.005)  # type: ignore[arg-type]


def test_affine_exponent_rendering_and_evaluation() -> None:
    h = Fraction(1, 200)
    assert AffineHExponent(Fraction(1, 2)).as_text() == "1/2"
    assert AffineHExponent(Fraction(1, 2), -1).as_text() == "1/2 - h"
    assert AffineHExponent(Fraction(0), 2).as_text() == "2h"
    assert AffineHExponent(Fraction(0), -1).as_text() == "-h"
    assert AffineHExponent(Fraction(-1), 2).as_text() == "-1 + 2h"
    assert AffineHExponent(Fraction(1, 2), -1).evaluate(h) == Fraction(99, 200)


def test_concentration_ledger_matches_page_eight_powers() -> None:
    ledger = concentration_exponent_ledger()
    assert ledger["radial_length"] == AffineHExponent(Fraction(1, 2))
    assert ledger["axial_length"] == AffineHExponent(Fraction(1, 2), -1)
    assert ledger["azimuthal_velocity"] == AffineHExponent(Fraction(-1, 2), -1)
    assert ledger["radial_velocity"] == AffineHExponent(Fraction(-1, 2))
    assert ledger["axial_to_radial_diffusion"] == AffineHExponent(Fraction(0), 2)
    rendered = render_exponent_ledger(Fraction(1, 200))
    assert rendered["pressure"] == {"symbolic": "-1 - 2h", "at_h": "-101/100"}


def test_correction_orders_are_generated_and_validated() -> None:
    assert correction_exponent(3) == AffineHExponent(Fraction(0), 6)
    with pytest.raises(ValueError, match="positive"):
        correction_exponent(0)
