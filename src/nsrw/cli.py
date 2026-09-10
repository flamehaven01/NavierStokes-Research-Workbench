"""Command-line interface for the Navier-Stokes Research Workbench."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

from nsrw.pipeline import render_receipt, run_pipeline

PROJECT_ROOT = Path(__file__).resolve().parents[2]
DEFAULT_CONTRACT = PROJECT_ROOT / "fixtures" / "navier-stokes-research-contract-v1.json"
DEFAULT_GRAPH = PROJECT_ROOT / "fixtures" / "navier-stokes-proof-graph-v1.json"


def _error_receipt(exc: Exception) -> dict[str, object]:
    return {
        "schema_id": "flamehaven.navier-stokes-research-pipeline-receipt.v1",
        "pipeline_status": "HELD",
        "claim_status": "UNVERIFIED",
        "checks": {"pipeline_execution": "ERROR"},
        "errors": [str(exc)],
    }


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--contract", type=Path, default=DEFAULT_CONTRACT)
    parser.add_argument("--graph-seed", type=Path, default=DEFAULT_GRAPH)
    parser.add_argument("--no-verify-sources", action="store_true")
    parser.add_argument("--full", action="store_true", help="include gate and complete graph evidence")
    parser.add_argument("--output", type=Path)
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    try:
        receipt = run_pipeline(
            args.contract,
            args.graph_seed,
            verify_sources=not args.no_verify_sources,
            full_output=args.full,
        )
    except (OSError, ValueError, KeyError, json.JSONDecodeError) as exc:
        receipt = _error_receipt(exc)
    rendered = render_receipt(receipt)
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(rendered, encoding="utf-8")
    sys.stdout.write(rendered)
    return 0 if receipt["pipeline_status"] == "GREEN" else 1


if __name__ == "__main__":
    raise SystemExit(main())
