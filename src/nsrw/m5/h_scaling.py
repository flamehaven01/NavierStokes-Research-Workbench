"""Independent bounded reconstruction of OutgoingDilation.H_scaling."""

from __future__ import annotations

from dataclasses import dataclass
from decimal import Decimal, localcontext
from hashlib import sha256
from typing import Callable

from nsrw.m5.lean_export import NORMALIZED_SCHEMA_ID
from nsrw.schema_admission import validate_document
from nsrw.strict_json import canonical_json_bytes

TARGET_DECLARATION = "NavierStokes.OutgoingDilation.H_scaling"
EXPECTED_NORMALIZED_SEMANTIC_SHA256 = "5f7773b0de7a5776b40a44ac9065be9f80b19929a94cf0930345383ed262e677"
EXPECTED_SOURCE = {
    "repository_commit": "8937a8f4cbc7abaab5e9e97d1cc7f5d2319d9538",
    "module": "NavierStokes.OutgoingDilation",
    "declaration": TARGET_DECLARATION,
    "source_file_sha256": "be46401810940d1021c2f2ccf0ce00bdffef82d413f2146742564d15c5516438",
    "source_manifest_sha256": "d8d5387db4bfe8dcdd867d1c4979d2911f194dfe8dae3012463c620e19c6001f",
    "lean_toolchain": "leanprover/lean4:v4.34.0-rc2",
}
EXPECTED_EXPORT = {
    "lean_version": "4.34.0-rc2",
    "lean_githash": "6a10ac8c22beadecabdbb0919c2b50214762f91d",
    "exporter_name": "lean4export",
    "exporter_version": "3.1.0",
    "exporter_commit": "cacf989bd75f608700820f6afc595f32e7a99a4d",
    "exporter_binary_sha256": "a638952892fede28e6b530243dc4f15a5d0fddd988f3f2494ded812249315234",
    "format_version": "3.1.0",
    "raw_sha256": "129f7dee6cf93f3588c4cceb13d55cb88345f39b525bfbbd58031eb0f7cd0148",
    "raw_bytes": 237875864,
    "record_count": 4408528,
}
EXPECTED_BINDERS = (
    ("F", "default", 4126865),
    ("XR", "default", 249100),
    ("hXR", "default", 379760),
    ("p", "default", 717340),
)
EXPECTED_TYPE_EXPRESSION_ID = 4127204
EXPECTED_VALUE_EXPRESSION_ID = 4127601
EXPECTED_TYPE_NODE_COUNT = 78
PRECISION_DIGITS = 80
COMPARISON_TOLERANCE = Decimal("1e-60")
XR_VALUES = (Decimal("0.25"), Decimal("2"), Decimal("9"))
P1_VALUES = (
    Decimal("-4"),
    Decimal("-0.25"),
    Decimal("0"),
    Decimal("0.125"),
    Decimal("3"),
    Decimal("25"),
)
P2_VALUES = (Decimal("-2"), Decimal("0"), Decimal("0.75"), Decimal("3"))

ProfileField = Callable[[Decimal, Decimal], Decimal]


@dataclass(frozen=True)
class ProfileFixture:
    name: str
    field: ProfileField


def lean_real_sqrt(value: Decimal) -> Decimal:
    """Model Mathlib's real square root at the negative boundary."""

    return Decimal(0) if value < 0 else value.sqrt()


def dilated_e(field: ProfileField, xr: Decimal, p1: Decimal, p2: Decimal) -> Decimal:
    if xr <= 0:
        raise ValueError("XR must be positive")
    return field(p1 / xr, p2)


def lhs_h(field: ProfileField, xr: Decimal, p1: Decimal, p2: Decimal) -> Decimal:
    """Left side, built from dilated E and not from the right side."""

    return lean_real_sqrt(Decimal(2) * p1) * dilated_e(field, xr, p1, p2)


def base_h(field: ProfileField, p1: Decimal, p2: Decimal) -> Decimal:
    """Base profile H, independently defined from the dilated left side."""

    return lean_real_sqrt(Decimal(2) * p1) * field(p1, p2)


def rhs_h(field: ProfileField, xr: Decimal, p1: Decimal, p2: Decimal) -> Decimal:
    if xr <= 0:
        raise ValueError("XR must be positive")
    return lean_real_sqrt(xr) * base_h(field, p1 / xr, p2)


def _mutated_rhs_scale(field: ProfileField, xr: Decimal, p1: Decimal, p2: Decimal) -> Decimal:
    return xr * base_h(field, p1 / xr, p2)


def _mutated_lhs_argument(field: ProfileField, xr: Decimal, p1: Decimal, p2: Decimal) -> Decimal:
    return lean_real_sqrt(Decimal(2) * p1) * field(p1 * xr, p2)


def _profile_one(p1: Decimal, p2: Decimal) -> Decimal:
    return Decimal(1) + p1**2 + p2**2


def _profile_two(p1: Decimal, p2: Decimal) -> Decimal:
    return Decimal(2) + p1 * p2 + p1**4 + p2**2


PROFILE_FIXTURES = (
    ProfileFixture("polynomial_even", _profile_one),
    ProfileFixture("polynomial_mixed", _profile_two),
)


def _maximum_error(
    left: Callable[[ProfileField, Decimal, Decimal, Decimal], Decimal],
    right: Callable[[ProfileField, Decimal, Decimal, Decimal], Decimal],
) -> Decimal:
    maximum = Decimal(0)
    for fixture in PROFILE_FIXTURES:
        for xr in XR_VALUES:
            for p1 in P1_VALUES:
                for p2 in P2_VALUES:
                    maximum = max(maximum, abs(left(fixture.field, xr, p1, p2) - right(fixture.field, xr, p1, p2)))
    return maximum


def validate_h_scaling_surface(normalized: dict[str, object]) -> None:
    """Bind this calculator to one complete, pinned exported theorem record."""

    try:
        validate_document(normalized, NORMALIZED_SCHEMA_ID)
    except ValueError as exc:
        raise ValueError("normalized H_scaling record fails schema admission") from exc

    source = normalized["source"]
    export = normalized["export"]
    declaration = normalized["declaration"]
    projection = normalized["type_projection"]
    if not isinstance(source, dict) or not isinstance(export, dict):
        raise ValueError("normalized H_scaling binding sections are malformed")
    if not isinstance(declaration, dict) or not isinstance(projection, dict):
        raise ValueError("normalized H_scaling declaration sections are malformed")
    for label, actual, expected in (
        ("source", source, EXPECTED_SOURCE),
        ("export", export, EXPECTED_EXPORT),
    ):
        for field, value in expected.items():
            if actual.get(field) != value:
                raise ValueError(f"H_scaling {label} binding mismatch: {field}")
    if declaration.get("kind") != "thm" or declaration.get("name") != TARGET_DECLARATION:
        raise ValueError("normalized declaration does not bind H_scaling theorem")
    if declaration.get("type_expression_id") != EXPECTED_TYPE_EXPRESSION_ID:
        raise ValueError("H_scaling type expression id binding mismatch")
    if declaration.get("value_expression_id") != EXPECTED_VALUE_EXPRESSION_ID:
        raise ValueError("H_scaling proof value id binding mismatch")
    binders = declaration.get("binders")
    observed_binders = (
        tuple((item.get("name"), item.get("binder_info"), item.get("type_expression_id"))
        for item in binders)
        if isinstance(binders, list) and all(isinstance(item, dict) for item in binders)
        else ()
    )
    if observed_binders != EXPECTED_BINDERS:
        raise ValueError("exported H_scaling binder sequence binding mismatch")
    if projection.get("root_expression_id") != EXPECTED_TYPE_EXPRESSION_ID:
        raise ValueError("H_scaling type root binding mismatch")
    nodes = projection.get("nodes")
    if not isinstance(nodes, list) or len(nodes) != EXPECTED_TYPE_NODE_COUNT:
        raise ValueError("H_scaling type node count binding mismatch")
    if normalized.get("losses") != [] or normalized.get("normalization_status") != "PASS":
        raise ValueError("H_scaling type projection contains opaque critical expressions")
    semantic_digest = sha256(canonical_json_bytes(normalized)).hexdigest()
    if semantic_digest != EXPECTED_NORMALIZED_SEMANTIC_SHA256:
        raise ValueError("H_scaling canonical semantic digest binding mismatch")


def run_h_scaling_reconstruction(normalized: dict[str, object]) -> dict[str, object]:
    """Run the bounded independent calculation and its two required mutations."""

    validate_h_scaling_surface(normalized)
    with localcontext() as context:
        context.prec = PRECISION_DIGITS
        primary_error = _maximum_error(lhs_h, rhs_h)
        wrong_scale_error = _maximum_error(lhs_h, _mutated_rhs_scale)
        wrong_argument_error = _maximum_error(_mutated_lhs_argument, rhs_h)
    primary_passes = primary_error <= COMPARISON_TOLERANCE
    mutations_detected = (
        wrong_scale_error > COMPARISON_TOLERANCE
        and wrong_argument_error > COMPARISON_TOLERANCE
    )
    return {
        "receipt_kind": "m5-h-scaling-reconstruction-v1",
        "evidence_class": "BOUNDED_SOURCE_DERIVED_IDENTITY_RECONSTRUCTION",
        "claim_status": "SUPPORTED" if primary_passes and mutations_detected else "UNVERIFIED",
        "check_status": "PASS" if primary_passes and mutations_detected else "FAIL",
        "normalized_declaration_sha256": sha256(canonical_json_bytes(normalized)).hexdigest(),
        "numeric_backend": "decimal.Decimal",
        "precision_digits": PRECISION_DIGITS,
        "comparison_tolerance": str(COMPARISON_TOLERANCE),
        "profiles": [fixture.name for fixture in PROFILE_FIXTURES],
        "xr_values": [str(value) for value in XR_VALUES],
        "p1_values": [str(value) for value in P1_VALUES],
        "p2_values": [str(value) for value in P2_VALUES],
        "sample_count": len(PROFILE_FIXTURES) * len(XR_VALUES) * len(P1_VALUES) * len(P2_VALUES),
        "maximum_absolute_error": str(primary_error),
        "mutations": [
            {
                "mutation_id": "M5-H-001",
                "description": "sqrt(XR) replaced by XR on the right side",
                "maximum_absolute_error": str(wrong_scale_error),
                "detected": wrong_scale_error > COMPARISON_TOLERANCE,
            },
            {
                "mutation_id": "M5-H-002",
                "description": "p.1 / XR replaced by p.1 * XR on the left side",
                "maximum_absolute_error": str(wrong_argument_error),
                "detected": wrong_argument_error > COMPARISON_TOLERANCE,
            },
        ],
    }
