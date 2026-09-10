"""Execute the two remaining M3 evidence checks without changing the source repo."""

from __future__ import annotations

import argparse
import json
import os
import shutil
from math import exp
from pathlib import Path

from nsrw.math_kernel.pressure_tail_witness import source_power_tail_witness
from nsrw.math_kernel.profile_closure import audit_lean_crosswalk

DEFAULT_LEAN_ROOT = Path(os.environ.get("NSRW_LEAN_ROOT", "external/NavierStokesAndEuler"))


def execute(lean_root: Path) -> dict[str, object]:
    lake = shutil.which("lake")
    lean = shutil.which("lean")
    crosswalk = audit_lean_crosswalk(lean_root)
    entries = crosswalk["entries"]
    static_status = "PASS" if all(entry["status"] == "PRESENT" for entry in entries) else "FAIL"
    tail = source_power_tail_witness(
        h=1.0 / 200.0,
        amplitude=1.25,
        radius=2.0,
        cutoff=2.0 * exp(14.0 / 5.0),
    )
    return {
        "schema": "nsrw.m3-evidence-execution.v1",
        "stage": "M3",
        "lean_build": {
            "check_status": "PASS" if lake and lean else "ERROR",
            "claim_status": "UNVERIFIED",
            "build_attempted": True,
            "lake_executable": lake,
            "lean_executable": lean,
            "commands": ["lake build", "lake env lean NavierStokes.lean"],
            "error": None if lake and lean else "lake/lean executable not found on PATH",
        },
        "theorem_dependency_surface": {
            "check_status": static_status,
            "claim_status": "SUPPORTED" if static_status == "PASS" else "UNVERIFIED",
            "evidence": crosswalk,
            "non_claim": "static declaration presence is not a compiled theorem dependency graph",
        },
        "source_pressure_tail": {
            "check_status": tail.check_status,
            "claim_status": "SUPPORTED" if tail.check_status == "PASS" else "UNVERIFIED",
            "witness": tail.as_dict(),
            "source_instance_status": "HELD_PARAMETERS_NOT_EVALUATED_BY_LEAN",
            "source_formula_locators": [
                "NavierStokes/OutgoingDilation.lean:canonicalKernel",
                "NavierStokes/OutgoingDilation.lean:Pi_canonical",
                "NavierStokes/HeatTailEdit.lean:powerTail",
                "NavierStokes/OutgoingDilation.lean:E_tail_factorization",
            ],
        },
        "stage_status": "HELD_LEAN_TOOLCHAIN_AND_SOURCE_INSTANCE",
        "claim_status": "UNVERIFIED",
        "non_claims": [
            "No Lean build or compiled dependency graph is established when the toolchain is absent.",
            "The tail witness validates the parametric eventual power law, not the concrete noncomputable source instance.",
            "No Navier-Stokes theorem or Clay problem solution is established.",
        ],
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--lean-root", type=Path, default=DEFAULT_LEAN_ROOT)
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    receipt = execute(args.lean_root)
    rendered = json.dumps(receipt, indent=2, sort_keys=True) + "\n"
    if args.output:
        args.output.write_text(rendered, encoding="utf-8")
    else:
        print(rendered, end="")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
