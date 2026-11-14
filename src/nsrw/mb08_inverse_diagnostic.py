"""Run the internal MB-08 exact inverse diagnostic with a local FHVAL install."""

from __future__ import annotations

import argparse
import hashlib
import json
from dataclasses import asdict
from fractions import Fraction as Q
from pathlib import Path
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from fhval.exact_inverse import Matrix, Vector

SOURCE_COMMIT = "8937a8f4cbc7abaab5e9e97d1cc7f5d2319d9538"
SOURCE_SHA256 = "54e4ee32a9b432e589dafddf73b6a2a2cffeac75627ebcbcf5e0e2b93e9892cc"


def _source_envelope() -> dict[str, str]:
    moment_lower, moment_upper = Q(3, 40), Q(3, 5)
    gap_lower, e_upper, f_upper = Q(9, 5), 9, 1
    determinant_lower = 2 * moment_lower**2 * gap_lower
    adjugate_upper = max(
        (2 * f_upper + e_upper) * moment_upper, 3 * moment_upper
    )
    inverse_upper = adjugate_upper / determinant_lower
    if not 0 < inverse_upper < 1000:
        raise ValueError("source envelope exceeds the requested norm bound")
    return {
        "abs_determinant_lower": str(determinant_lower),
        "adjugate_inf_norm_upper": str(adjugate_upper),
        "inverse_inf_norm_upper": str(inverse_upper),
    }


def run(source_bytes: bytes) -> dict:
    source_sha256 = hashlib.sha256(source_bytes).hexdigest()
    if source_sha256 != SOURCE_SHA256:
        raise ValueError("source bytes do not match the pinned reset file")
    from fhval.exact_inverse import check_inverse

    a, b, e, f = Q(1, 10), Q(1, 10), Q(4), Q(1, 4)
    reference: Matrix = ((a, e * a), (2 * b, 2 * f * b))
    rhs: Vector = (Q(1, 2), Q(1, 4))
    det = Q(-3, 40)
    inverse: Matrix = ((Q(-2, 3), Q(16, 3)), (Q(8, 3), Q(-4, 3)))
    solution: Vector = (1, 1)
    eps = Q(1, 2**200)
    near: Matrix = ((1, 1), (1, 1 + eps))
    near_inverse: Matrix = ((1 + 1 / eps, -1 / eps), (-1 / eps, 1 / eps))
    singular: Matrix = ((1, 1), (1, 1))
    cases = (
        ("exact_control", "PASS",
         check_inverse(reference, rhs, reference, det, inverse, solution)),
        ("coherent_row_swap", "REJECT",
         check_inverse(reference, rhs, reference[::-1], -det,
                       (inverse[0][::-1], inverse[1][::-1]), (Q(5, 2), 0))),
        ("coherent_pressure_factor_removed", "REJECT",
         check_inverse(reference, rhs, (reference[0], (b, f * b)), det / 2,
                       ((inverse[0][0], 2 * inverse[0][1]),
                        (inverse[1][0], 2 * inverse[1][1])), (Q(7, 3), Q(2, 3)))),
        ("determinant_sign_flip", "REJECT",
         check_inverse(reference, rhs, reference, -det, inverse, solution)),
        ("inverse_error", "REJECT",
         check_inverse(reference, rhs, reference, det, ((1, 0), (0, 1)), solution)),
        ("solution_error", "REJECT",
         check_inverse(reference, rhs, reference, det, inverse, (1, 2))),
        ("near_singular_exact", "PASS",
         check_inverse(near, (2, 2 + eps), near, eps, near_inverse, solution)),
        ("near_singular_rounded_det", "REJECT",
         check_inverse(near, (2, 2 + eps), near, 0, near_inverse, solution)),
        ("singular", "SINGULAR",
         check_inverse(singular, (2, 2), singular, 0, inverse, solution)),
    )
    return {
        "status": "PASS" if all(r.status == expected for _, expected, r in cases) else "FAIL",
        "scope": "synthetic_exact_residuals_and_source_inequality_arithmetic",
        "source_commit": SOURCE_COMMIT,
        "source_sha256": source_sha256,
        "source_envelope": _source_envelope(),
        "cases": [
            dict(asdict(result), case=name, expected=expected, determinant=str(result.determinant))
            for name, expected, result in cases
        ],
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("source", type=Path, help="pinned AngularMomentReset.lean")
    parser.add_argument("--output", type=Path, help="write a new diagnostic JSON file")
    args = parser.parse_args()
    try:
        report = run(args.source.read_bytes())
        content = json.dumps(report, indent=2, sort_keys=True) + "\n"
        if args.output is not None:
            with args.output.open("x", encoding="utf-8", newline="\n") as output:
                output.write(content)
        print(content, end="")
        return 0 if report["status"] == "PASS" else 1
    except (OSError, ValueError) as exc:
        print(json.dumps({"status": "ERROR", "detail": str(exc)}))
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
