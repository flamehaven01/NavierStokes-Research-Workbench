"""MB-06 bounded positive ratio R(lambda), not an actual Profile/J evaluation.

The underlying exact-real source cancellation is a separate Lean obligation.
All returned endpoints are exact Fractions computed from rigorously bounded
positive expm1 factors. No float64, source Profile, or root is evaluated.
"""
from __future__ import annotations

import argparse
import json
from fractions import Fraction
from pathlib import Path

from nsrw.math_kernel.p2_core_scalars import expm1_bounds
from nsrw.math_kernel.p2_normalized_j_verify import record_context

LAM = Fraction(1, 10**12)
COARSE_B = Fraction(207522463005781740692370179, 2305843009213693952)
BITS = (128, 256, 512)


def bound_normalized_ratio(*, bits: int = 128) -> dict:
    """Compute enclosures for R=expm1(17*lam/10)/expm1(2*lam)."""
    if type(bits) is not int or bits not in BITS:
        raise ValueError("unsupported fractional precision")
    a, b = 17 * LAM / 10, 2 * LAM
    numerator = expm1_bounds(a, bits)
    denominator = expm1_bounds(b, bits)
    if not (0 < numerator[0] <= numerator[1] and 0 < denominator[0] <= denominator[1]):
        raise ArithmeticError("UNRESOLVED[POSITIVE_DENOMINATOR_ENCLOSURE]")
    ratio_lo, ratio_hi = numerator[0] / denominator[1], numerator[1] / denominator[0]
    # Independent analytic inequalities:
    # x <= exp(x)-1 <= x*exp(x), and 1-x <= exp(-x), for x >= 0.
    # For a<1, R lies between (17/20)*(1-2*lam) and (17/20)/(1-17*lam/10).
    analytic_lo = Fraction(17, 20) * (1 - b)
    analytic_hi = Fraction(17, 20) / (1 - a)
    if not (0 < analytic_lo <= ratio_lo <= ratio_hi <= analytic_hi):
        raise ArithmeticError("UNRESOLVED[RATIO_ENCLOSURE_INCONSISTENT]")
    payload = record_context()
    payload["precision_fractional_bits"] = bits
    payload["expm1_factors"] = {
        "numerator_lower": str(numerator[0]), "numerator_upper": str(numerator[1]),
        "denominator_lower": str(denominator[0]), "denominator_upper": str(denominator[1]),
    }
    payload["analytic_rational_bracket"] = {"lower": str(analytic_lo), "upper": str(analytic_hi)}
    payload["rigorous_R_bracket"] = {"lower": str(ratio_lo), "upper": str(ratio_hi)}
    payload["rigorous_B_times_R_bracket"] = {
        "lower": str(COARSE_B * ratio_lo), "upper": str(COARSE_B * ratio_hi),
    }
    return payload


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", required=True, type=Path)
    parser.add_argument("--precision", type=int, choices=BITS, default=128)
    args = parser.parse_args(argv)
    try:
        payload = bound_normalized_ratio(bits=args.precision)
        args.output.write_text(json.dumps(payload, sort_keys=True, indent=2) + "\n", encoding="utf-8")
    except (ValueError, ArithmeticError, OSError) as exc:
        print(json.dumps({"status": "UNRESOLVED", "reason": str(exc)}))
        return 1
    print(json.dumps({"status": "PASS[FACTOR_ENCLOSURE_ONLY]", "output": str(args.output)}))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
