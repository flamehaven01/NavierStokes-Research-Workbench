"""Fixed-input MomentBound producer: exact B, with positive scale left symbolic.

The source-to-bound bridge is a static derivation pending its own Lean proof.
No numerical q, actual coefficient, source Profile or J is returned.
"""

from __future__ import annotations

import argparse
import json
from fractions import Fraction
from pathlib import Path

from nsrw.math_kernel.p2_coefficient_verify import record_context
from nsrw.math_kernel.p2_core_scalars import exp_bounds


def _terms() -> tuple[Fraction, Fraction, Fraction, Fraction]:
    lam, eta = Fraction(1, 10**12), Fraction(1, 2**20)
    p = eta * (1 + eta**2)
    h0 = Fraction(4 + 12 * 3**3)
    h1 = (Fraction(5, 2) + 12 * 3**9) * 3**8
    main = Fraction(1, 10000) / lam
    return p, h0, h1, main


def compute_coarse_scaled_bound() -> Fraction:
    """B <= q_star/s under the proposed source bridge; B is not q_star."""
    p, h0, h1, main = _terms()
    return Fraction(9, 10) * main - abs(p) * (h0 + h1)


def produce_coefficient_bound_record(*, supporting_bits: int = 128) -> dict:
    if type(supporting_bits) is not int or supporting_bits not in (128, 256, 512):
        raise ValueError("supporting precision must be 128, 256 or 512")
    lo, hi = exp_bounds(Fraction(1), supporting_bits)
    bound = compute_coarse_scaled_bound()
    if not 2 < lo <= hi < 3 or bound <= 0:
        raise ArithmeticError("UNRESOLVED[COARSE_BOUND_OR_EXP_SUPPORT]")
    p, h0, h1, main = _terms()
    result = record_context()
    result.update({
        "p": str(p),
        "constants": {
            "kappa_lower": "1/2", "rho_upper": "1",
            "prefix_bound_upper_0": str(h0), "prefix_bound_upper_1": str(h1),
        },
        "scaled_bounds": {
            "main_over_scale_lower": str(main),
            "abs_prefix_over_scale_upper": str(h0 + h1),
            "q_over_scale_lower": str(bound),
        },
        "supporting_arithmetic": {
            "fractional_bits": supporting_bits,
            "exp_one": {"lower": str(lo), "upper": str(hi)},
        },
    })
    return result


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("command", choices=["produce"])
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--supporting-precision", type=int, choices=[128, 256, 512], default=128)
    args = parser.parse_args(argv)
    try:
        result = produce_coefficient_bound_record(supporting_bits=args.supporting_precision)
        args.output.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    except ArithmeticError as exc:
        print(json.dumps({"status": "UNRESOLVED", "reason": str(exc)}))
        return 3
    except (OSError, ValueError) as exc:
        print(json.dumps({"status": "ERROR", "reason": str(exc)}))
        return 1
    print(json.dumps({"status": result["check_status"], "output": str(args.output)}))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
