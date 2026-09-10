"""Command line for bounded mathematical-kernel checks."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

from nsrw.math_kernel.experiments import run_math_self_check


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--tolerance", type=float, default=2e-6)
    parser.add_argument("--output", type=Path)
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    try:
        receipt = run_math_self_check(args.tolerance)
    except (ArithmeticError, ValueError) as exc:
        receipt = {
            "schema_id": "flamehaven.navier-stokes-math-kernel-receipt.v1",
            "check_status": "ERROR",
            "claim_status": "UNVERIFIED",
            "error": str(exc),
        }
    rendered = json.dumps(receipt, indent=2, sort_keys=True) + "\n"
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(rendered, encoding="utf-8")
    sys.stdout.write(rendered)
    return 0 if receipt["check_status"] == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
