"""Run a registered NSRW research verification and write a scoped JSON report."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

from nsrw.lean_archive_verification import ReplayPin, check_lean_archive
from nsrw.math_kernel.manufactured import forced_linear_shear, zero_force
from nsrw.math_kernel.operators import sample_residual
from nsrw.research_verification import Finding, Status, Verification, run_verification
from nsrw.strict_json import canonical_json_bytes, parse_strict_json_bytes

P1_MARGIN = ReplayPin(
    archive_sha256="9163d2ee67a4cab03c152151d1df7c3e4990306c6d2fa184b52d63e556aa52a5",
    members=25,
    execution_commit="7f29ebf0e2b894bf598144628230ae09df436c3d",
    source_commit="8937a8f4cbc7abaab5e9e97d1cc7f5d2319d9538",
    toolchain="leanprover/lean4:v4.34.0-rc2",
    run_status="PASS[COMMIT_BOUND_EXTERNAL_P1_MARGIN_REPLAY]",
    declarations={
        "P2_ZPLUS_J_QuantitativeMargin": (
            "NSRW.P2.secondBump_massTail_eq_full",
            "NSRW.P2.firstRepair_weightGap_pos",
            "NSRW.P2.angularMoment_ge_firstRepair_margin",
            "NSRW.P2.firstRepair_margin_pos",
        ),
        "P2_ZPLUS_J_MarginNormalization": (
            "NSRW.P2.firstRepair_weightGap_exp_eq",
            "NSRW.P2.normalizedSecondBumpMoment_eq_interval",
            "NSRW.P2.secondBumpWeightedMoment_eq_normalized",
            "NSRW.P2.normalizedSecondBumpMoment_eq_rowMoment",
            "NSRW.P2.normalizedSecondBumpMoment_ge_plateau",
            "NSRW.P2.angularMoment_ge_plateau_margin",
        ),
    },
    critical_signature_sha256={
        "NSRW.P2.angularMoment_ge_firstRepair_margin":
            "407b11e0498bb5d30957818545573634af712c1c4d42083d1d26c233bb953ad4",
        "NSRW.P2.angularMoment_ge_plateau_margin":
            "588a6b70f945e276650a0ed9c846bec1e67e88490170419e365be2fa9c19277e",
    },
)


def _inverse(evidence) -> Finding:
    from nsrw import mb08_inverse_diagnostic

    try:
        result = mb08_inverse_diagnostic.run(evidence["source"])
    except ValueError as exc:
        return Finding(Status.FAIL, {"reason": str(exc)})
    return Finding(Status(result["status"]), result)


def _ratio(evidence) -> Finding:
    from nsrw import mb06_ratio_crosscheck as checker
    if checker.mpmath.__version__ != "1.3.0":
        return Finding(Status.ENV_BLOCKED, {"reason": "mpmath 1.3.0 required"})
    try:
        result = checker.check(evidence["record"])
    except (ValueError, KeyError, TypeError) as exc:
        status = Status.UNRESOLVED if str(exc).startswith("UNRESOLVED[") else Status.FAIL
        return Finding(status, {"reason": str(exc)})
    return Finding(Status.PASS, result)


def _shear(evidence) -> Finding:
    # Fixed probe, with analytic momentum residual (0,0,0) and divergence 0.
    # Removing the force gives the independently known residual (3/4,0,0).
    expected = {"point": [0, 0.75, 0], "time": 0.5, "viscosity": 1, "tolerance": 2e-6}
    try:
        fixture = parse_strict_json_bytes(evidence["fixture"])
    except ValueError as exc:
        return Finding(Status.FAIL, {"reason": str(exc)})
    if canonical_json_bytes(fixture) != canonical_json_bytes(expected):
        return Finding(Status.FAIL, {"reason": "manufactured-shear fixture differs from reference"})
    velocity, pressure, force = forced_linear_shear()
    point = (0.0, 0.75, 0.0)
    tolerance = expected["tolerance"]
    sample = sample_residual(velocity, pressure, force, 1.0, point, 0.5)
    no_force = sample_residual(velocity, pressure, zero_force, 1.0, point, 0.5)
    checks = {
        "momentum_and_divergence": sample.residual_infinity_norm <= tolerance
        and abs(sample.divergence) <= tolerance,
        "force_removal_detected": abs(no_force.residual[0] - 0.75) <= tolerance
        and max(abs(no_force.residual[1]), abs(no_force.residual[2])) <= tolerance,
    }
    return Finding(Status.PASS if all(checks.values()) else Status.FAIL, {
        "checks": checks,
        "tolerance": tolerance,
        "sample": sample.as_dict(),
        "removed_force_sample": no_force.as_dict(),
    })


def _lean_margin(evidence) -> Finding:
    try:
        result = check_lean_archive(evidence["archive"], P1_MARGIN)
    except ValueError as exc:
        return Finding(Status.FAIL, {"reason": str(exc)})
    return Finding(Status.PASS, result)


CHECKS = {
    check.check_id: check for check in (
        Verification(
            "mb08-inverse", "1", "Original reset matrix convention and synthetic inverses",
            "Exact rational residuals and analytic envelope arithmetic",
            "Pinned source plus nine synthetic two-by-two cases", "EXACT_ARITHMETIC_DIAGNOSTIC",
            ("source",), _inverse,
        ),
        Verification(
            "mb06-ratio", "1", "Recorded normalized angular-moment factor",
            "Outward mpmath interval exponentials and containment",
            "Fixed parameter tuple and the submitted fractional precision", "INTERVAL_CROSSCHECK",
            ("record",), _ratio,
        ),
        Verification(
            "forced-shear", "1", "Navier–Stokes momentum and divergence residual implementation",
            "Finite differences against analytic manufactured field and force removal",
            "One interior sample of u=(ty,0,0) with f=(y,0,0)", "SAMPLED_PDE_DIAGNOSTIC",
            ("fixture",), _shear,
        ),
        Verification(
            "p1-lean-margin", "1", "Recorded Lean quantitative and normalized margin declarations",
            "Archive pin, member hashes, declaration signatures and axiom consistency",
            "Ten named declarations in the original P1 commit-bound archive", "LEAN_RECORD_CROSSCHECK",
            ("archive",), _lean_margin,
        ),
    )
}


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("check", choices=CHECKS)
    parser.add_argument("--input", metavar="NAME=FILE", action="append", default=[])
    parser.add_argument("--output", type=Path)
    parser.add_argument("--manifest", type=Path, help="write implementation and environment identity")
    args = parser.parse_args(argv)
    if args.manifest is not None and args.output is None:
        parser.error("--manifest requires --output")
    files = {}
    for entry in args.input:
        name, sep, path = entry.partition("=")
        if not sep or not name or not path or name in files:
            parser.error("--input must be unique NAME=FILE")
        files[name] = Path(path)
    if set(files) - set(CHECKS[args.check].inputs):
        parser.error("unknown input name for this check")
    evidence = {}
    unavailable = {}
    blocked = {}
    for name, path in files.items():
        try:
            evidence[name] = path.read_bytes()
        except (FileNotFoundError, NotADirectoryError) as exc:
            unavailable[name] = str(exc)
        except OSError as exc:
            blocked[name] = str(exc)
    check = CHECKS[args.check]
    if args.manifest is not None:
        from nsrw.verification_manifest import implementation_identity, require_complete_identity

        before = implementation_identity(args.check)
        try:
            require_complete_identity(args.check, before)
        except ValueError as exc:
            parser.exit(2, f"execution manifest blocked: {exc}\n")
    report = run_verification(check, evidence)
    if unavailable:
        report["details"]["unavailable_files"] = unavailable
    if blocked:
        report["status"] = Status.ENV_BLOCKED.value
        report["details"]["environment_blocked_files"] = blocked
    if args.manifest is not None:
        after = implementation_identity(args.check)
        if before != after:
            parser.exit(2, "verification implementation or environment drifted during execution\n")
    rendered = json.dumps(report, indent=2, ensure_ascii=True, allow_nan=False, sort_keys=True) + "\n"
    if args.manifest is not None and args.manifest.exists():
        parser.exit(2, "manifest already exists\n")
    if args.output is not None:
        try:
            with args.output.open("x", encoding="utf-8", newline="\n") as stream:
                stream.write(rendered)
        except OSError as exc:
            parser.exit(2, f"report write failed: {exc}\n")
    if args.manifest is not None:
        from hashlib import sha256

        manifest = {
            "format": "nsrw-verification-execution-v1",
            "check_id": check.check_id,
            "revision": check.revision,
            "inputs": report["inputs"],
            "report_sha256": sha256(rendered.encode("utf-8")).hexdigest(),
            "status": report["status"],
            **before,
        }
        try:
            with args.manifest.open("x", encoding="utf-8", newline="\n") as stream:
                json.dump(manifest, stream, indent=2, sort_keys=True)
                stream.write("\n")
        except OSError as exc:
            parser.exit(2, f"manifest write failed: {exc}\n")
    print(rendered, end="")
    return 0 if report["status"] == Status.PASS else 1


if __name__ == "__main__":
    raise SystemExit(main())
