from __future__ import annotations

from fractions import Fraction
from math import exp, sqrt
from pathlib import Path

import pytest

from nsrw.math_kernel.profile_closure import (
    ClosedLeadingProfiles,
    QuadratureSpec,
    audit_lean_crosswalk,
    canonical_pressure,
    derived_radial_flux,
    parameter_derivative_of_average,
    pressure_balance_sample,
    radial_average,
    run_m3_self_check,
)


def swirl(x: float, _eta: float) -> float:
    return sqrt(2.0 * x) * exp(-x)


def constant(_x: float, _eta: float) -> float:
    return 1.0


def test_simpson_and_axis_extension() -> None:
    assert radial_average(lambda x, _eta: 2.0 * x, 0.0, 0.2) == 0.0
    assert radial_average(lambda x, _eta: 2.0 * x, 1.0, 0.2) == pytest.approx(1.0)
    assert parameter_derivative_of_average(lambda _x, eta: eta, 1.0, 0.2) == pytest.approx(1.0)


def test_derived_flux_matches_equation_4_7_for_constant_axial_profile() -> None:
    h = Fraction(1, 200)
    x, eta = 0.75, 0.2
    expected = x * (1.0 + 2.0 * h) * eta / (1.0 - 2.0 * h * eta * eta)
    assert derived_radial_flux(constant, h, x, eta) == pytest.approx(expected, abs=2e-10)
    assert derived_radial_flux(constant, h, 0.0, eta) == 0.0


def test_canonical_pressure_keeps_tail_explicit() -> None:
    cutoff = 8.0
    value = canonical_pressure(swirl, 0.75, 0.2, cutoff, lambda _eta: 0.5 * exp(-2 * cutoff))
    assert value == pytest.approx(-0.5 * exp(-1.5), abs=2e-8)
    axis_value = canonical_pressure(
        swirl,
        0.0,
        0.2,
        cutoff,
        lambda _eta: 0.5 * exp(-2 * cutoff),
        axis_integrand_limit=lambda _eta: 1.0,
    )
    assert axis_value == pytest.approx(-0.5, abs=1e-6)


def test_closed_profile_derives_both_dependent_profiles() -> None:
    closed = ClosedLeadingProfiles(
        swirl, constant, Fraction(1, 200), 8.0, lambda _eta: 0.5 * exp(-16.0),
        lambda _eta: 1.0,
    )
    profile = closed.as_leading_profiles()
    assert profile.profile_id == "closed-leading-profile-v1"
    assert profile.radial_flux(0.0, 0.0) == 0.0
    sample = pressure_balance_sample(swirl, closed.pressure, 0.75, 0.2, tolerance=2e-6)
    assert sample.check_status == "PASS"


@pytest.mark.parametrize(
    "call",
    [
        lambda: QuadratureSpec(3),
        lambda: radial_average(constant, -1.0, 0.0),
        lambda: radial_average(constant, 1.0, 2.0),
        lambda: parameter_derivative_of_average(constant, 1.0, 0.99, step=0.1),
        lambda: derived_radial_flux(constant, 0.0, 1.0, 0.0),
        lambda: derived_radial_flux(constant, Fraction(1, 100), 1.0, 0.0),
        lambda: canonical_pressure(swirl, 1.0, 0.0, 0.5, lambda _eta: 0.0),
    ],
)
def test_closure_rejects_invalid_inputs(call) -> None:
    with pytest.raises((ValueError, ArithmeticError, TypeError)):
        call()


def test_nonvanishing_axis_profile_is_not_silently_regularized() -> None:
    with pytest.raises(ValueError, match="explicit pressure integrand limit"):
        canonical_pressure(lambda _x, _eta: 1.0, 0.0, 0.0, 1.0, lambda _eta: 0.0)


def test_axis_limit_is_required_and_endpoint_derivatives_are_one_sided() -> None:
    with pytest.raises(ValueError, match="explicit pressure integrand limit"):
        canonical_pressure(swirl, 0.0, 0.0, 1.0, lambda _eta: 0.0)
    assert parameter_derivative_of_average(constant, 1.0, -1.0) == pytest.approx(0.0)
    assert parameter_derivative_of_average(lambda _x, eta: eta, 1.0, -1.0) == pytest.approx(1.0)
    assert parameter_derivative_of_average(lambda _x, eta: eta, 1.0, 1.0) == pytest.approx(1.0)


def test_m3_receipt_is_deterministic_and_scoped() -> None:
    first = run_m3_self_check()
    second = run_m3_self_check()
    assert first == second
    assert first["check_status"] == "PASS"
    assert first["claim_status"] == "UNVERIFIED"
    assert all(item["check_status"] == "PASS" for item in first["samples"])


def test_crosswalk_distinguishes_static_presence_from_build(tmp_path: Path) -> None:
    root = tmp_path
    (root / "NavierStokes").mkdir()
    (root / "NavierStokes" / "ProfileHistories.lean").write_text(
        "def average := 0\ntheorem radialPartial_pressure := by\n", encoding="utf-8"
    )
    (root / "NavierStokes" / "SlowDivergence.lean").write_text("def radialFlux := 0\n", encoding="utf-8")
    (root / "NavierStokes" / "NominalProfile.lean").write_text(
        "theorem pressure_canonical := by\n", encoding="utf-8"
    )
    (root / "NavierStokes" / "ProblemStatement.lean").write_text(
        "def candidateStatement := True\n", encoding="utf-8"
    )
    (root / "NavierStokes" / "ActualCandidateAssembly.lean").write_text(
        "theorem selected_candidate : True := by\n", encoding="utf-8"
    )
    result = audit_lean_crosswalk(root)
    assert result["build_status"] == "UNAVAILABLE_TOOLCHAIN_NOT_EXECUTED"
    assert {entry["status"] for entry in result["entries"]} == {"PRESENT"}


def test_crosswalk_reports_unavailable_files(tmp_path: Path) -> None:
    result = audit_lean_crosswalk(tmp_path)
    assert all(entry["status"] == "UNAVAILABLE" for entry in result["entries"])


def test_crosswalk_does_not_promote_comment_text_to_declaration(tmp_path: Path) -> None:
    root = tmp_path / "NavierStokes"
    root.mkdir()
    (root / "ProfileHistories.lean").write_text(
        "-- def average is discussed here\n", encoding="utf-8"
    )
    result = audit_lean_crosswalk(tmp_path)
    average = next(entry for entry in result["entries"] if entry["key"] == "average")
    assert average["status"] == "ABSENT"
