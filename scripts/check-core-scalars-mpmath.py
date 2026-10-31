"""Cross-check retained scalar intervals without importing the Fraction producer.

mpmath 1.3.0 interval arithmetic; direct exponential differences, not the
producer's factored expm1 / exact-series implementation. Same operator, different
arithmetic implementation. Only the fixed core-scalar contract is checked.
"""
import argparse
import hashlib
import json
import sys
from fractions import Fraction
from pathlib import Path

import mpmath
from mpmath.ctx_iv import MPIntervalContext

INPUTS = {"P": "1", "m": "1", "lambda": "1/1000000000000", "eta": "1/1048576",
          "h": "1/4000000000000", "wait": "60*log(1000000000000)", "K": None}
UNRESOLVED = ["CORE_AFFINE_COEFFICIENTS_NOT_ENCLOSED", "Q_LOWER_NOT_ESTABLISHED",
              "UNRESOLVED_COMBINED_SCALE_STEPBOUND", "UNASSIGNED_RESET_K",
              "UNCONSTRUCTED_SOURCE_PROFILE", "LOCAL_TO_PROFILE_J_QUANTITATIVE_WRAPPER_NOT_COMPILED"]
BASIS = {"source_commit": "8937a8f4cbc7abaab5e9e97d1cc7f5d2319d9538",
         "p1_execution_commit": "7f29ebf0e2b894bf598144628230ae09df436c3d",
         "gap": "NSRW.P2.firstRepair_weightGap_exp_eq",
         "plateau": "NSRW.P2.normalizedSecondBumpMoment_ge_plateau",
         "normalization": "NSRW.P2.secondBumpWeightedMoment_eq_normalized"}
FIELDS = ("ell", "v", "plateau_width", "weight_gap", "main_denominator")


def unique_object(pairs):
    result = {}
    for key, value in pairs:
        if key in result:
            raise ValueError("Duplicate JSON key: " + key)
        result[key] = value
    return result


def check(raw: bytes) -> dict:
    """Require independent interval containment, not midpoint agreement."""
    if mpmath.__version__ != "1.3.0":
        raise ValueError("This checker is tested with mpmath==1.3.0")
    record = json.loads(raw, object_pairs_hook=unique_object)
    bits = record["precision_fractional_bits"]
    if type(bits) is not int or bits not in (128, 256, 512):
        raise ValueError("Unsupported fractional precision")
    expected = {"format": "nsrw-p2-core-scalars-v1", "scope": "CORE_SCALAR_ENCLOSURES_ONLY",
                "inputs": INPUTS, "unresolved": UNRESOLVED, "formal_basis": BASIS,
                "outward_quantum": str(Fraction(1, 1 << bits)),
                "arithmetic": "exact Fraction series/remainder and dyadic outward rounding",
                "main_denominator_identity": {
                    "two_beta1": "249999999999/250000000000",
                    "two_beta0_minus_two_beta1": "1/500000000000",
                    "basis": "exp(a)-exp(b)=exp(b)*(exp(a-b)-1); not an added Lean admission"}}
    if set(record) != {*expected, *FIELDS, "precision_fractional_bits", "i01_lower_bound"}:
        raise ValueError("Unexpected or missing record field")
    for key, value in expected.items():
        if record[key] != value:
            raise ValueError("Contract mismatch: " + key)
    iv = MPIntervalContext()
    iv.prec = bits + 192

    def rational(value):
        return iv.mpf(value.numerator) / iv.mpf(value.denominator)

    lam = rational(Fraction(1, 10**12))
    ell, v = iv.exp(rational(Fraction(-23, 20))), iv.exp(rational(Fraction(-17, 20)))
    computed = {"ell": ell, "v": v, "plateau_width": (v - ell) / 4,
                "weight_gap": iv.exp(-13 + rational(Fraction(57, 20)) * lam)
                - iv.exp(-13 + rational(Fraction(23, 20)) * lam),
                "main_denominator": iv.exp(1 - 2 * lam) - iv.exp(1 - 4 * lam)}
    checks = []
    for name, value in computed.items():
        bounds = record[name]
        if set(bounds) != {"lower", "upper"}:
            raise ValueError("Invalid interval fields: " + name)
        if any(not isinstance(s, str) or len(s) > 2000 for s in bounds.values()):
            raise ValueError("Invalid rational encoding: " + name)
        lo, hi = Fraction(bounds["lower"]), Fraction(bounds["upper"])
        if not 0 < lo < hi or any((v * (1 << bits)).denominator != 1 for v in (lo, hi)):
            raise ValueError("Invalid positive dyadic interval: " + name)
        # Endpoint operations stay intervals. None/indeterminate is rejection.
        if (rational(lo).b <= value.a) is not True or (value.b <= rational(hi).a) is not True:
            raise ValueError("Independent enclosure not contained: " + name)
        checks.append({"quantity": name, "status": "PASS", "relation": "contained"})
    if record["i01_lower_bound"] != {
        "representation": "exp(exponent)*mantissa_lower", "exponent": "6499999999987",
        "mantissa_lower": record["plateau_width"]["lower"],
        "meaning": "lower bound only; no upper enclosure for I01 and no evaluated logarithm",
    }:
        raise ValueError("Symbolic I01 binding mismatch")
    return {"format": "nsrw-core-scalar-crosscheck-v1", "status": "PASS",
            "scope": "CORE_SCALAR_ENCLOSURES_ONLY", "backend": "mpmath.iv 1.3.0",
            "working_precision_bits": iv.prec, "fractional_bits": bits,
            "input_sha256": hashlib.sha256(raw).hexdigest(), "checks": checks,
            "input_lf_sha256": hashlib.sha256(raw.replace(b"\r\n", b"\n")).hexdigest(),
            "algorithm": "direct interval exponential differences",
            "producer_imported": False, "independent_operator": False,
            "numerical_J_certificate": False}


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("inputs", nargs="+", type=Path)
    parser.add_argument("--output", type=Path)
    args = parser.parse_args(argv)
    try:
        results = [check(path.read_bytes()) for path in args.inputs]
    except (ValueError, KeyError, TypeError, OSError, ZeroDivisionError) as exc:
        print("CORE_SCALAR_CROSSCHECK_REJECTED: " + str(exc), file=sys.stderr)
        return 1
    report = json.dumps({"status": "PASS", "records": results}, indent=2) + "\n"
    if args.output:
        args.output.write_text(report, encoding="utf-8", newline="\n")
    else:
        print(report, end="")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
