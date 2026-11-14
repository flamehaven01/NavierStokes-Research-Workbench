"""Fail-closed recomputation of MB-06 R factor bounds, no producer import.

This shares the pinned Fraction/expm1_bounds backend with the producer.
It is same-operator verification, not external independent reproduction.
"""
from __future__ import annotations

import argparse
import json
from fractions import Fraction
from pathlib import Path

from nsrw.math_kernel.p2_coefficient_verify import _bounded_tree, _rational, _same, read_record
from nsrw.math_kernel.p2_core_scalars import expm1_bounds

LAM = Fraction(1, 10**12)
B = Fraction(207522463005781740692370179, 2305843009213693952)
EXPECTED_KEYS = frozenset({
    "precision_fractional_bits", "expm1_factors", "analytic_rational_bracket",
    "rigorous_R_bracket", "rigorous_B_times_R_bracket",
})


def record_context() -> dict:
    return {
        "format": "nsrw-mb06-normalized-j-factor-v1",
        "scope": "NORMALIZED_J_FACTOR_ENCLOSURES_ONLY",
        "input": {"P": "1", "m": "1", "lambda": "1/1000000000000",
                  "eta": "1/1048576", "B_coarse": str(B)},
        "ratio": "expm1(17*lambda/10)/expm1(2*lambda)",
        "method": "positive-expm1-fraction-enclosures-v1",
        "formal_bridge": "NOT_COMPILED_OR_ADMITTED",
        "required_for_J": [
            "SAME_SOURCE_PROFILE_F", "F_AMP_ETA_GT_9_OVER_10",
            "EXACT_FIRST_WINDOW_LOCAL_MASS_ZERO",
            "LOCAL_J_NORMALIZATION_BRIDGE_NOT_COMPILED",
            "SOURCE_PROFILE_FIXED_TUPLE_NOT_CONSTRUCTED",
            "COMBINED_SCALE_AND_RESET_K_UNRESOLVED",
        ],
        "source_binding": {
            "upstream_commit": "8937a8f4cbc7abaab5e9e97d1cc7f5d2319d9538",
            "momentbound_execution_commit": "fb5ad6001f1637417efda6ef34f3b75c8266c059",
            "p1_execution_commit": "7f29ebf0e2b894bf598144628230ae09df436c3d",
        },
        "claim_authority": "NONE",
        "claim_status": "UNVERIFIED",
    }


def _exact_map(observed: object, expected: dict[str, Fraction]) -> None:
    if type(observed) is not dict or observed.keys() != expected.keys():
        raise ValueError("interval fields mismatch")
    for key, val in expected.items():
        if _rational(observed[key]) != val:
            raise ValueError("altered bound: " + key)


def verify_normalized_ratio(payload: object) -> dict:
    _bounded_tree(payload)
    context = record_context()
    if type(payload) is not dict or payload.keys() != (context.keys() | EXPECTED_KEYS):
        raise ValueError("record field set mismatch")
    for key, value in context.items():
        if not _same(payload[key], value):
            raise ValueError("context/scope mismatch: " + key)
    bits = payload["precision_fractional_bits"]
    if type(bits) is not int or bits not in (128, 256, 512):
        raise ValueError("unsupported precision")
    a, b = 17 * LAM / 10, 2 * LAM
    n_lo, n_hi = expm1_bounds(a, bits)
    d_lo, d_hi = expm1_bounds(b, bits)
    if not (0 < n_lo <= n_hi and 0 < d_lo <= d_hi):
        raise ValueError("unresolved denominator or numerator")
    lo, hi = n_lo / d_hi, n_hi / d_lo
    analytic_lo = Fraction(17, 20) * (1 - b)
    analytic_hi = Fraction(17, 20) / (1 - a)
    if not (0 < analytic_lo <= lo <= hi <= analytic_hi):
        raise ValueError("inconsistent analytic and series enclosures")
    _exact_map(payload["expm1_factors"], {
        "numerator_lower": n_lo, "numerator_upper": n_hi,
        "denominator_lower": d_lo, "denominator_upper": d_hi,
    })
    _exact_map(payload["analytic_rational_bracket"], {"lower": analytic_lo, "upper": analytic_hi})
    _exact_map(payload["rigorous_R_bracket"], {"lower": lo, "upper": hi})
    _exact_map(payload["rigorous_B_times_R_bracket"], {"lower": B * lo, "upper": B * hi})
    return {
        "verification_status": "PASS[RECOMPUTED_MB06_FACTOR_ONLY]",
        "R_lower": str(lo), "R_upper": str(hi),
        "claim_authority": "NONE", "claim_status": "UNVERIFIED",
    }


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--input", type=Path, required=True)
    args = parser.parse_args(argv)
    try:
        verdict = verify_normalized_ratio(read_record(args.input))
    except (ValueError, OSError, UnicodeError, ArithmeticError) as exc:
        print(json.dumps({"verification_status": "REJECT", "reason": str(exc)}))
        return 1
    print(json.dumps(verdict, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
