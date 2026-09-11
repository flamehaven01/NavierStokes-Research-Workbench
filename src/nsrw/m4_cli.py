"""Command-line entry point for the bounded M4-P audit."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

from nsrw.m4_audit import load_manifest, run_m4_audit


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("manifest", type=Path)
    parser.add_argument("--lean-root", type=Path)
    parser.add_argument(
        "--evidence-root",
        type=Path,
        help="root used to resolve compiled receipt paths (defaults to repository root)",
    )
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    evidence_root = args.evidence_root or args.manifest.resolve().parents[1]
    receipt = run_m4_audit(load_manifest(args.manifest), args.lean_root, evidence_root)
    rendered = json.dumps(receipt, indent=2, sort_keys=True) + "\n"
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(rendered, encoding="utf-8")
    else:
        print(rendered, end="")
    return 0 if receipt["check_status"] == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
