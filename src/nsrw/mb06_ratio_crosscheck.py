"""MB-06 R(lambda) cross-check using independent mpmath.iv interval exponentials.

Does not import the Fraction expm1 producer/verifier. It checks recorded
factor enclosure containment, not a source Profile, numerical J, or a Lean proof.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import sys
from fractions import Fraction
from pathlib import Path

import mpmath
from mpmath.ctx_iv import MPIntervalContext

LAMBDA = Fraction(1, 10**12)
B = Fraction(207522463005781740692370179, 2305843009213693952)
SOURCE_COMMIT = "8937a8f4cbc7abaab5e9e97d1cc7f5d2319d9538"
MB05_COMMIT = "fb5ad6001f1637417efda6ef34f3b75c8266c059"


def unique_object(pairs):
    result = {}
    for key, value in pairs:
        if key in result:
            raise ValueError("duplicate JSON key: " + key)
        result[key] = value
    return result


def read_fraction(value):
    if not isinstance(value, str) or len(value) > 500:
        raise ValueError("invalid rational field")
    try:
        return Fraction(value)
    except (ValueError, ZeroDivisionError) as exc:
        raise ValueError("malformed rational field") from exc


def check(raw: bytes) -> dict:
    if mpmath.__version__ != "1.3.0":
        raise ValueError("mpmath 1.3.0 required")
    if not isinstance(raw, bytes) or len(raw) > 16_384:
        raise ValueError("invalid record size")
    record = json.loads(raw, object_pairs_hook=unique_object)
    if not isinstance(record, dict):
        raise ValueError("record not an object")
    if record.get("format") != "nsrw-mb06-normalized-j-factor-v1":
        raise ValueError("incorrect record format")
    if record.get("scope") != "NORMALIZED_J_FACTOR_ENCLOSURES_ONLY":
        raise ValueError("scope mismatch")
    if record.get("claim_authority") != "NONE" or record.get("claim_status") != "UNVERIFIED":
        raise ValueError("illegal claim promotion")
    if record.get("formal_bridge") != "NOT_COMPILED_OR_ADMITTED":
        raise ValueError("historical input record changed")
    if record.get("input") != {"P": "1", "m": "1", "lambda": str(LAMBDA),
                               "eta": "1/1048576", "B_coarse": str(B)}:
        raise ValueError("fixed rational inputs mismatch")
    source = record.get("source_binding")
    if not isinstance(source, dict) or source.get("upstream_commit") != SOURCE_COMMIT or source.get("momentbound_execution_commit") != MB05_COMMIT:
        raise ValueError("unbound source commit")
    if record.get("ratio") != "expm1(17*lambda/10)/expm1(2*lambda)":
        raise ValueError("ratio identity mismatch")
    bits = record.get("precision_fractional_bits")
    if type(bits) is not int or bits not in (128, 256, 512):
        raise ValueError("unsupported precision")
    lo, hi = read_fraction(record["rigorous_R_bracket"]["lower"]), read_fraction(record["rigorous_R_bracket"]["upper"])
    blo, bhi = read_fraction(record["rigorous_B_times_R_bracket"]["lower"]), read_fraction(record["rigorous_B_times_R_bracket"]["upper"])
    if not (0 < lo < hi and blo == B * lo and bhi == B * hi):
        raise ValueError("inconsistent or nonpositive factor intervals")

    iv = MPIntervalContext()
    iv.prec = bits + 192

    def exact(frac: Fraction):
        return iv.mpf(frac.numerator) / iv.mpf(frac.denominator)

    lam = exact(LAMBDA)
    # Different algorithm from expm1_bounds: raw interval exponential
    # subtraction, with precision raised to avoid catastrophic cancellation.
    numer = iv.exp(exact(Fraction(17, 10)) * lam) - iv.mpf(1)
    denom = iv.exp(iv.mpf(2) * lam) - iv.mpf(1)
    if (iv.mpf(0).b < numer.a) is not True or (iv.mpf(0).b < denom.a) is not True:
        raise ValueError("UNRESOLVED[DENOMINATOR_OR_NUMERATOR_NOT_SEPARATED]")
    value = numer / denom
    if (exact(lo).b <= value.a) is not True or (value.b <= exact(hi).a) is not True:
        raise ValueError("independent ratio outside recorded interval")
    scaled = exact(B) * value
    if (exact(blo).b <= scaled.a) is not True or (scaled.b <= exact(bhi).a) is not True:
        raise ValueError("independent scaled factor outside recorded interval")
    return {
        "status": "PASS[INDEPENDENT_ALGORITHM_FACTOR_CONTAINMENT]",
        "backend": "mpmath.iv 1.3.0",
        "algorithm": "direct outward interval exp(x)-1 then divide",
        "input_sha256": hashlib.sha256(raw).hexdigest(),
        "precision_bits": iv.prec,
        "source_profile_constructed": False,
        "numeric_J_certified": False,
        "claim_authority": "NONE",
        "claim_status": "UNVERIFIED",
        "independent_operator": False,
    }


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("record", type=Path)
    args = parser.parse_args(argv)
    try:
        result = check(args.record.read_bytes())
    except (ValueError, KeyError, TypeError, OSError, ZeroDivisionError) as exc:
        print(json.dumps({"status": "REJECT", "reason": str(exc)}), file=sys.stderr)
        return 1
    print(json.dumps(result, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
