"""Verify the fixed MomentBound arithmetic record, without invoking its producer.

This checks a static source-bound derivation's rational calculation, not the
derivation in Lean or a source Profile instance. The exponential primitive and
operator are shared with the producer; this is not independent reproduction.
"""

from __future__ import annotations

import argparse
import json
import re
from fractions import Fraction
from pathlib import Path

from nsrw.math_kernel.p2_core_scalars import exp_bounds

MAX_BYTES = 65536
PROOF_HASHES = {
    "P2_F1_MainMomentPositivity.lean": "df9f605fa7ad9fa2842f54ae2d67b6a9b1773849d72c695192ae1bebe2f01206",
    "P2_L2_NormalizedMainMomentComparison.lean": "624f1aa042377db7e2bbe50ba70d08a35035cddc51697bd5a69a1ce0bd9bbcdd",
    "P2_L3_TemplateMomentComparison.lean": "9ad9b6ea625e2c39f126a8d3a770cb365f48db9f67c734964d972e382b5fa1d4",
    "P2_C_MainOnlyCoefficient.lean": "6be4e26255568f5b45c297b548ecadceb35f807519e01bf21e372eb9fbd22fcf",
    "P2_C02_ActualCoefficientDecomposition.lean": "a2ad4f0e47428c869873de96ba681d17f0d9299ae80094f9c40462b1a8cfd5f7",
}


def record_context() -> dict:
    """Closed v1 metadata contract shared with producer; no computed results."""
    return {
        "format": "nsrw-p2-scaled-coefficient-bound-v1",
        "scope": "SCALED_COEFFICIENT_BOUND_ONLY",
        "method": "coarse-rational-source-bounds-v1",
        "inputs": {
            "P": "1", "m": "1", "lambda": "1/1000000000000", "eta": "1/1048576",
            "h": "1/4000000000000", "wait": "60*log(1000000000000)", "K": None,
        },
        "source_binding": {
            "upstream_commit": "8937a8f4cbc7abaab5e9e97d1cc7f5d2319d9538",
            "nsrw_dependency_commit": "7f29ebf0e2b894bf598144628230ae09df436c3d",
            "hash_convention": "SHA256_OF_GIT_BLOB_BYTES",
            "proof_sha256": dict(PROOF_HASHES),
        },
        "positive_scale": {
            "representation": "SYMBOLIC_POSITIVE_FACTOR",
            "definition": "exp(-beta1*center0)/(A1*D)",
            "numerator_exponent": "-3249999999986250000000003/500000000000",
            "denominator": "A1*D",
            "A1": "rowMoment(c.exponents(1))",
            "D": "exp(2*beta0)-exp(2*beta1)",
            "numerically_evaluated": False,
            "positivity_basis": ["rowMoment_pos", "mainOnly_separation_gap_pos", "Real.exp_pos"],
        },
        "mathematical_bridge": "STATIC_DERIVATION_NOT_ADMITTED",
        "assumptions": [
            "SOURCE_CORE_AT_FIXED_TUPLE_NOT_CONSTRUCTED",
            "NEW_COEFFICIENT_BRIDGE_NOT_COMPILED",
            "ACTUAL_C1_REQUIRES_SAME_PROFILE_AMP_GT_9_OVER_10",
            "RESET_WITNESS_AND_POSITIVE_K_UNASSIGNED",
            "COMBINED_SCALE_LE_1_OVER_1000_NOT_CERTIFIED",
            "AMPLITUDE_SPEC_FULL_HYPOTHESES_REQUIRE_SOURCE_REVIEW",
            "NUMERICAL_Q_AND_J_NOT_EVALUATED",
        ],
        "check_status": "PASS[EXACT_RATIONAL_SCALED_BOUND]",
        "claim_authority": "NONE",
        "claim_status": "UNVERIFIED",
    }


def _bounded_tree(value: object, depth: int = 0, budget: list | None = None) -> None:
    if budget is None:
        budget = [512]
    budget[0] -= 1
    if depth > 8 or budget[0] < 0:
        raise ValueError("record nesting/node limit exceeded")
    if type(value) is dict:
        if len(value) > 64:
            raise ValueError("too many keys")
        for k, v in value.items():
            if type(k) is not str or len(k) > 128:
                raise ValueError("invalid key")
            _bounded_tree(v, depth + 1, budget)
    elif type(value) is list:
        if len(value) > 64:
            raise ValueError("too many entries")
        for v in value:
            _bounded_tree(v, depth + 1, budget)
    elif type(value) is str:
        if len(value) > 1024:
            raise ValueError("string limit exceeded")
    elif value is not None and type(value) not in (bool, int):
        raise ValueError("unsupported value type")
    elif type(value) is int and value.bit_length() > 32:
        raise ValueError("integer limit exceeded")


def _same(actual: object, expected: object) -> bool:
    if type(actual) is not type(expected):
        return False
    if type(expected) is dict:
        return actual.keys() == expected.keys() and all(
            _same(actual[k], v) for k, v in expected.items()
        )
    if type(expected) is list:
        return len(actual) == len(expected) and all(
            _same(a, b) for a, b in zip(actual, expected, strict=True)
        )
    return actual == expected


def _rational(value: object) -> Fraction:
    if type(value) is not str or len(value) > 1024:
        raise ValueError("rational must be a bounded canonical string")
    if re.fullmatch(r"-?(0|[1-9][0-9]*)(/[1-9][0-9]*)?", value) is None:
        raise ValueError("invalid rational syntax")
    result = Fraction(value)
    if str(result) != value:
        raise ValueError("noncanonical rational")
    return result


def _rational_fields(actual: object, expected: dict) -> None:
    if type(actual) is not dict or actual.keys() != expected.keys():
        raise ValueError("rational field set mismatch")
    for name, value in expected.items():
        if _rational(actual[name]) != value:
            raise ValueError(f"arithmetic mismatch: {name}")


def verify_coefficient_bound_record(payload: object) -> dict:
    """Return verifier-owned status; reject malformed or altered v1 records."""
    _bounded_tree(payload)
    context = record_context()
    fields = {"p", "constants", "scaled_bounds", "supporting_arithmetic"}
    if type(payload) is not dict or payload.keys() != context.keys() | fields:
        raise ValueError("record field set mismatch")
    for name, value in context.items():
        if not _same(payload[name], value):
            raise ValueError(f"context mismatch: {name}")

    # Independent integer evaluation: eta + eta^3, not the producer's product.
    n = 2**20
    p = Fraction(n * n + 1, n**3)
    h0 = 4 + 12 * 3**3
    h1 = Fraction((5 + 24 * 3**9) * 3**8, 2)
    main = Fraction(10**12, 10000)
    prefix = h0 + h1
    bound = Fraction(9 * 10**12, 100000) - p * prefix
    if _rational(payload["p"]) != p or bound <= 0:
        raise ValueError("p or positivity mismatch")
    _rational_fields(payload["constants"], {
        "kappa_lower": Fraction(1, 2), "rho_upper": Fraction(1),
        "prefix_bound_upper_0": Fraction(h0), "prefix_bound_upper_1": h1,
    })
    _rational_fields(payload["scaled_bounds"], {
        "main_over_scale_lower": main, "abs_prefix_over_scale_upper": prefix,
        "q_over_scale_lower": bound,
    })
    supporting = payload["supporting_arithmetic"]
    if type(supporting) is not dict or supporting.keys() != {"fractional_bits", "exp_one"}:
        raise ValueError("supporting arithmetic field set mismatch")
    bits = supporting["fractional_bits"]
    if type(bits) is not int or bits not in (128, 256, 512):
        raise ValueError("unsupported precision")
    lo, hi = exp_bounds(Fraction(1), bits)
    _rational_fields(supporting["exp_one"], {"lower": lo, "upper": hi})
    if not 2 < lo <= hi < 3:
        raise ValueError("exp(1) support not established")
    return {
        "verification_status": "PASS[RECOMPUTED_SCALED_BOUND]",
        "scaled_B": str(bound), "scope": context["scope"],
        "claim_authority": "NONE", "claim_status": "UNVERIFIED",
    }


def _unique_pairs(pairs: list) -> dict:
    result = {}
    for key, value in pairs:
        if key in result:
            raise ValueError(f"duplicate key: {key}")
        result[key] = value
    return result


def read_record(path: Path) -> object:
    with path.open("rb") as stream:
        raw = stream.read(MAX_BYTES + 1)
    if len(raw) > MAX_BYTES:
        raise ValueError("record size limit exceeded")
    try:
        return json.loads(raw, object_pairs_hook=_unique_pairs)
    except RecursionError as exc:
        raise ValueError("JSON nesting limit exceeded") from exc


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--input", required=True, type=Path)
    args = parser.parse_args(argv)
    try:
        result = verify_coefficient_bound_record(read_record(args.input))
    except (ValueError, UnicodeError) as exc:
        print(json.dumps({"verification_status": "REJECT", "reason": str(exc)}))
        return 1
    except OSError as exc:
        print(json.dumps({"verification_status": "ERROR", "reason": str(exc)}))
        return 3
    print(json.dumps(result, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
