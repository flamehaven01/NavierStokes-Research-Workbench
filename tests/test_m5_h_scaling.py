from __future__ import annotations

import copy
import json
from decimal import Decimal, localcontext
from pathlib import Path

import pytest

from nsrw.m5.h_scaling import (
    COMPARISON_TOLERANCE,
    TARGET_DECLARATION,
    dilated_e,
    lean_real_sqrt,
    lhs_h,
    rhs_h,
    run_h_scaling_reconstruction,
)

ROOT = Path(__file__).resolve().parents[1]


def _normalized_h_scaling() -> dict[str, object]:
    return json.loads(
        (ROOT / "fixtures/m5/h_scaling.normalized.json").read_text(encoding="utf-8")
    )


def test_lean_real_sqrt_preserves_negative_real_boundary() -> None:
    assert lean_real_sqrt(Decimal("-4")) == 0
    assert lean_real_sqrt(Decimal("0")) == 0
    assert lean_real_sqrt(Decimal("9")) == 3


def test_independent_h_scaling_reconstruction_and_mutations() -> None:
    receipt = run_h_scaling_reconstruction(_normalized_h_scaling())

    assert receipt["check_status"] == "PASS"
    assert receipt["evidence_class"] == "BOUNDED_SOURCE_DERIVED_IDENTITY_RECONSTRUCTION"
    assert Decimal(receipt["maximum_absolute_error"]) <= COMPARISON_TOLERANCE
    assert receipt["sample_count"] == 144
    assert all(mutation["detected"] for mutation in receipt["mutations"])


def test_committed_normalized_fixture_drives_the_bounded_reconstruction() -> None:
    normalized = _normalized_h_scaling()

    receipt = run_h_scaling_reconstruction(normalized)

    assert normalized["normalization_status"] == "PASS"
    assert normalized["declaration"]["name"] == TARGET_DECLARATION
    assert len(normalized["type_projection"]["nodes"]) == 78
    assert receipt["check_status"] == "PASS"


def test_changed_theorem_body_cannot_run_the_calculator() -> None:
    normalized = copy.deepcopy(_normalized_h_scaling())
    app_node = next(
        node for node in normalized["type_projection"]["nodes"] if node["kind"] == "app"
    )
    app_node["children"] = list(reversed(app_node["children"]))

    with pytest.raises(ValueError, match="canonical semantic digest binding mismatch"):
        run_h_scaling_reconstruction(normalized)


def test_changed_raw_export_binding_cannot_run_the_calculator() -> None:
    normalized = copy.deepcopy(_normalized_h_scaling())
    normalized["export"]["raw_sha256"] = "0" * 64

    with pytest.raises(ValueError, match="raw_sha256"):
        run_h_scaling_reconstruction(normalized)


def test_left_and_right_are_separate_implementations() -> None:
    def profile(p1: Decimal, p2: Decimal) -> Decimal:
        return Decimal(1) + p1**2 + p2

    with localcontext() as context:
        context.prec = 80
        left = lhs_h(profile, Decimal("9"), Decimal("3"), Decimal("0.75"))
        right = rhs_h(profile, Decimal("9"), Decimal("3"), Decimal("0.75"))
    assert abs(left - right) <= COMPARISON_TOLERANCE


@pytest.mark.parametrize("invalid_xr", [Decimal("-1"), Decimal("0")])
def test_dilated_and_right_hand_fields_reject_out_of_scope_xr(invalid_xr: Decimal) -> None:
    def profile(p1: Decimal, p2: Decimal) -> Decimal:
        return p1 + p2

    with pytest.raises(ValueError, match="XR"):
        dilated_e(profile, invalid_xr, Decimal("1"), Decimal("0"))
    with pytest.raises(ValueError, match="XR"):
        rhs_h(profile, invalid_xr, Decimal("1"), Decimal("0"))
