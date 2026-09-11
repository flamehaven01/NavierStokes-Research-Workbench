"""Execute the two remaining M3 evidence checks without changing the source repo."""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import shutil
import subprocess
from math import exp
from pathlib import Path

from nsrw.math_kernel.pressure_tail_witness import source_power_tail_witness
from nsrw.math_kernel.profile_closure import audit_lean_crosswalk

DEFAULT_LEAN_ROOT = Path(os.environ.get("NSRW_LEAN_ROOT", "external/NavierStokesAndEuler"))


def _unfinished_build(
    lake: str | None,
    lean: str | None,
    command: list[str],
    *,
    attempted: bool,
    error: str,
) -> dict[str, object]:
    return {
        "check_status": "ERROR",
        "claim_status": "UNVERIFIED",
        "build_attempted": attempted,
        "lake_executable": lake,
        "lean_executable": lean,
        "command": command,
        "exit_code": None,
        "stdout_sha256": None,
        "stderr_sha256": None,
        "error": error,
    }


def _execute_lean_build(lean_root: Path, timeout_seconds: int) -> dict[str, object]:
    lake = shutil.which("lake")
    lean = shutil.which("lean")
    command = ["lake", "build", "+NavierStokes.OutgoingDilation"]
    if not lake or not lean:
        return _unfinished_build(
            lake,
            lean,
            command,
            attempted=False,
            error="lake/lean executable not found on PATH",
        )
    try:
        process = subprocess.run(
            command,
            cwd=lean_root,
            capture_output=True,
            text=True,
            check=False,
            timeout=timeout_seconds,
        )
    except (OSError, subprocess.TimeoutExpired) as exc:
        return _unfinished_build(
            lake,
            lean,
            command,
            attempted=True,
            error=f"{type(exc).__name__}: build did not complete",
        )
    passed = process.returncode == 0
    return {
        "check_status": "PASS" if passed else "FAIL",
        "claim_status": "SUPPORTED" if passed else "UNVERIFIED",
        "build_attempted": True,
        "lake_executable": lake,
        "lean_executable": lean,
        "command": command,
        "exit_code": process.returncode,
        "stdout_sha256": hashlib.sha256(process.stdout.encode("utf-8")).hexdigest().upper(),
        "stderr_sha256": hashlib.sha256(process.stderr.encode("utf-8")).hexdigest().upper(),
        "error": None if passed else "scoped Lean target build returned non-zero",
    }


def execute(lean_root: Path, timeout_seconds: int = 900) -> dict[str, object]:
    lean_build = _execute_lean_build(lean_root, timeout_seconds)
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
        "schema": "nsrw.m3-evidence-execution.v2",
        "stage": "M3",
        "lean_build": lean_build,
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
        "stage_status": (
            "CLOSED_WITH_NONCOMPUTABLE_SOURCE_BOUNDARY"
            if lean_build["check_status"] == "PASS"
            else "HELD_LEAN_BUILD_AND_SOURCE_INSTANCE"
        ),
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
    return {"PASS": 0, "FAIL": 1, "ERROR": 2}.get(
        str(receipt["lean_build"]["check_status"]),
        2,
    )


if __name__ == "__main__":
    raise SystemExit(main())
