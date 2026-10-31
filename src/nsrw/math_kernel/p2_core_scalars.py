"""Exact rational enclosures for one fixed P2 core-scalar experiment.

This is not a Profile evaluator, quadrature engine or interval library. For
0 <= y <= 1/2, the exponential tail after term N is at most
a_(N+1)/(1-y/(N+2)): subsequent positive-term ratios are bounded by y/(N+2).
Negative arguments use reciprocal bounds. Range reduction, squaring and all
outward rounding use Fraction/integer arithmetic, never floating arithmetic.
"""

from __future__ import annotations

import argparse
import json
from fractions import Fraction
from pathlib import Path

PRECISIONS = (128, 256, 512)
LAM = Fraction(1, 10**12)
ETA = Fraction(1, 2**20)
UNRESOLVED = (
    "CORE_AFFINE_COEFFICIENTS_NOT_ENCLOSED",
    "Q_LOWER_NOT_ESTABLISHED",
    "UNRESOLVED_COMBINED_SCALE_STEPBOUND",
    "UNASSIGNED_RESET_K",
    "UNCONSTRUCTED_SOURCE_PROFILE",
    "LOCAL_TO_PROFILE_J_QUANTITATIVE_WRAPPER_NOT_COMPILED",
)


def _precision(bits: int) -> None:
    if type(bits) is not int or bits not in PRECISIONS:
        raise ValueError("precision must be 128, 256 or 512 fractional bits")


def _round(bounds: tuple[Fraction, Fraction], bits: int) -> tuple[Fraction, Fraction]:
    lo, hi = bounds
    if lo > hi:
        raise ValueError("inverted interval")
    scale = 1 << bits
    a, b = lo * scale, hi * scale
    return Fraction(a.numerator // a.denominator, scale), Fraction(
        -((-b.numerator) // b.denominator), scale
    )


def _positive_product(
    a: tuple[Fraction, Fraction], b: tuple[Fraction, Fraction], bits: int
) -> tuple[Fraction, Fraction]:
    if not (0 <= a[0] <= a[1] and 0 <= b[0] <= b[1]):
        raise ValueError("ordered nonnegative intervals required")
    return _round((a[0] * b[0], a[1] * b[1]), bits)


def _small_exp(y: Fraction, bits: int, *, minus_one: bool = False) -> tuple[Fraction, Fraction]:
    if not isinstance(y, Fraction) or not 0 <= y <= Fraction(1, 2):
        raise ValueError("small exponential argument outside [0, 1/2]")
    term = Fraction(1)
    total = Fraction(0 if minus_one else 1)
    tolerance = Fraction(1, 1 << (bits + 4))
    for n in range(1, 1025):
        term *= y / n
        total += term
        next_term = term * y / (n + 1)
        remainder = next_term / (1 - y / (n + 2))
        if remainder <= tolerance:
            return _round((total, total + remainder), bits)
    raise ValueError("UNRESOLVED[BACKEND_ENCLOSURE_BUDGET_EXCEEDED]")


def exp_bounds(x: Fraction, bits: int = 128) -> tuple[Fraction, Fraction]:
    """Enclose exp(x), |x|<=16. Precision is fractional bits, not integer size."""
    _precision(bits)
    if not isinstance(x, Fraction) or abs(x) > 16:
        raise ValueError("exact rational argument within [-16, 16] required")
    work_bits = bits + 64
    y, squarings = abs(x), 0
    while y > Fraction(1, 2):
        y /= 2
        squarings += 1
    bounds = _small_exp(y, work_bits)
    for _ in range(squarings):
        bounds = _positive_product(bounds, bounds, work_bits)
    if x < 0:
        if bounds[0] <= 0:
            raise ValueError("nonpositive reciprocal denominator")
        bounds = 1 / bounds[1], 1 / bounds[0]
    return _round(bounds, bits)


def expm1_bounds(t: Fraction, bits: int = 128) -> tuple[Fraction, Fraction]:
    """Positive small expm1 via its own series, without subtracting near ones."""
    _precision(bits)
    if not isinstance(t, Fraction) or not 0 <= t <= Fraction(1, 2):
        raise ValueError("exact rational t in [0, 1/2] required")
    return _small_exp(t, bits, minus_one=True)


def positive_main_ratio_lower(
    numerator: tuple[Fraction, Fraction], denominator: tuple[Fraction, Fraction],
    bits: int = 128,
) -> Fraction:
    """If supplied positive intervals are valid, lower(N/D)=lower(N)/upper(D).

    This arithmetic operation does not supply the missing source moment bounds.
    """
    _precision(bits)
    values = (*numerator, *denominator)
    if not all(isinstance(x, Fraction) for x in values):
        raise ValueError("exact rational interval endpoints required")
    if not (0 < numerator[0] <= numerator[1] and 0 < denominator[0] <= denominator[1]):
        raise ValueError("ordered strictly positive intervals required")
    value = numerator[0] / denominator[1]
    return _round((value, value), bits)[0]


def _encoded(bounds: tuple[Fraction, Fraction]) -> dict[str, str]:
    return {"lower": str(bounds[0]), "upper": str(bounds[1])}


def produce_core_scalar_certificate(bits: int = 128) -> dict:
    """A deterministic record of core factors only: no c1, q or J certificate."""
    _precision(bits)
    # Each exponential performs its range reduction with 64 guard bits.
    ell = exp_bounds(Fraction(-23, 20), bits)
    v = exp_bounds(Fraction(-17, 20), bits)
    width = _round(((v[0] - ell[1]) / 4, (v[1] - ell[0]) / 4), bits)
    gap = _positive_product(
        exp_bounds(-13 + 23 * LAM / 20, bits),
        expm1_bounds(17 * LAM / 10, bits), bits,
    )
    beta0, beta1 = Fraction(1, 2) - LAM, Fraction(1, 2) - 2 * LAM
    assert 2 * beta1 == 1 - 4 * LAM
    assert 2 * beta0 - 2 * beta1 == 2 * LAM
    denominator = _positive_product(
        exp_bounds(2 * beta1, bits), expm1_bounds(2 * LAM, bits), bits
    )
    if not all(0 < b[0] < b[1] for b in (ell, v, width, gap, denominator)):
        raise ValueError("UNRESOLVED[INSUFFICIENT_POSITIVE_SEPARATION]")
    scale_exponent = 13 / LAM * beta0
    return {
        "format": "nsrw-p2-core-scalars-v1",
        "scope": "CORE_SCALAR_ENCLOSURES_ONLY",
        "precision_fractional_bits": bits,
        "outward_quantum": str(Fraction(1, 1 << bits)),
        "arithmetic": "exact Fraction series/remainder and dyadic outward rounding",
        "inputs": {"P": "1", "m": "1", "lambda": str(LAM), "eta": str(ETA),
                   "h": str(LAM / 4), "wait": "60*log(1000000000000)", "K": None},
        "formal_basis": {
            "source_commit": "8937a8f4cbc7abaab5e9e97d1cc7f5d2319d9538",
            "p1_execution_commit": "7f29ebf0e2b894bf598144628230ae09df436c3d",
            "gap": "NSRW.P2.firstRepair_weightGap_exp_eq",
            "plateau": "NSRW.P2.normalizedSecondBumpMoment_ge_plateau",
            "normalization": "NSRW.P2.secondBumpWeightedMoment_eq_normalized",
        },
        "ell": _encoded(ell), "v": _encoded(v), "plateau_width": _encoded(width),
        "weight_gap": _encoded(gap), "main_denominator": _encoded(denominator),
        "main_denominator_identity": {
            "two_beta1": str(2 * beta1), "two_beta0_minus_two_beta1": str(2 * LAM),
            "basis": "exp(a)-exp(b)=exp(b)*(exp(a-b)-1); not an added Lean admission",
        },
        "i01_lower_bound": {
            "representation": "exp(exponent)*mantissa_lower",
            "exponent": str(scale_exponent), "mantissa_lower": str(width[0]),
            "meaning": "lower bound only; no upper enclosure for I01 and no evaluated logarithm",
        },
        "unresolved": list(UNRESOLVED),
    }


def verify_core_scalar_certificate(payload: object) -> dict[str, str]:
    """Recompute all bounds. This shares the producer algorithm/trust domain."""
    try:
        if type(payload) is not dict:
            raise ValueError("record must be an object")
        expected = produce_core_scalar_certificate(payload.get("precision_fractional_bits"))
        if payload != expected:
            raise ValueError("scope, input, hypothesis or recomputed enclosure mismatch")
    except (ValueError, TypeError) as error:
        return {"verdict": "REJECT", "reason": str(error)}
    return {"verdict": "ACCEPT", "scope": "CORE_SCALAR_ENCLOSURES_ONLY"}


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("operation", choices=("produce", "verify"))
    parser.add_argument("--precision", type=int, default=128)
    parser.add_argument("--input", type=Path)
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    try:
        if args.operation == "produce":
            result = produce_core_scalar_certificate(args.precision)
        else:
            if args.input is None:
                raise ValueError("verify requires --input")
            result = verify_core_scalar_certificate(json.loads(
                args.input.read_text(encoding="utf-8"), object_pairs_hook=_unique_object
            ))
    except (ValueError, OSError) as error:
        result = {"verdict": "REJECT", "reason": str(error)}
    encoded = json.dumps(result, indent=2, sort_keys=True) + "\n"
    if args.output:
        args.output.write_text(encoded, encoding="utf-8")
    else:
        print(encoded, end="")
    return 1 if result.get("verdict") == "REJECT" else 0


def _unique_object(pairs: list[tuple[str, object]]) -> dict:
    result = {}
    for key, value in pairs:
        if key in result:
            raise ValueError("duplicate JSON key")
        result[key] = value
    return result


if __name__ == "__main__":
    raise SystemExit(main())
