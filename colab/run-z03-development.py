#!/usr/bin/env python3
"""Development only: pinned source -> fresh Z01 -> Z02 -> conditional Z03."""

import argparse
import hashlib
import importlib.util
import json
import os
import re
import shutil
import subprocess
import time
import zipfile
from datetime import datetime, timezone
from pathlib import Path

BASE = "10d5a1f517b8665137f2354746d70752f8ef67fd"
DEPENDENCIES = {
    "P2_Z01_LocalMassIdentities": "ff7101067a98fbaa8974c1aa409b83740cd17eb4f1778f20cdc23b44e2a5c267",
    "P2_Z02_BoundaryMassSigns": "7b5764911790054cbba982acfde8ed673705a2d68e85bcd341507d7e0b5f8c2c",
}
MODULE = "P2_Z03_ConditionalInteriorZero"
SURFACES = {
    "z01": ("localMass_partial_identity", "localMass_tail_identity"),
    "z02": ("prefixM_pos", "radialPulse_before_first_lower", "localMass_lower_pos",
            "secondBumpWeightedMoment_pos", "upperTail_radialPulse_eq",
            "secondBumpWeightedMoment_tail_eq", "localMass_upper_eq_second_tail",
            "localMass_upper_neg_of_secondCoeff_pos"),
    "z03": ("massMoment_continuous", "localMass_continuousOn_firstRepair",
            "exists_firstRepair_zero_of_secondCoeff_pos"),
}


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def inspect_axioms(text, names):
    if "sorryAx" in text:
        raise ValueError("SORRY_AXIOM_OBSERVED")
    result = {}
    for short in names:
        name = "NSRW.P2." + short
        matches = re.findall(r"'" + re.escape(name) + r"' depends on axioms: \[([^\]]*)\]", text)
        if len(matches) != 1:
            raise ValueError("AXIOM_SURFACE_MISSING_OR_DUPLICATED: " + name)
        values = [part.strip() for part in matches[0].split(",")]
        if len(values) != 3 or set(values) != {"propext", "Classical.choice", "Quot.sound"}:
            raise ValueError("AXIOM_SURFACE_UNEXPECTED: " + name)
        result[name] = sorted(values)
    return result


def run(source, base, dependencies, proof, output, expected_sha):
    source, base, dependencies, proof, output = (
        p.resolve() for p in (source, base, dependencies, proof, output)
    )
    archive = Path(str(output) + "-evidence.zip")
    if (output.exists() or archive.exists()
            or output.is_relative_to(source) or output.is_relative_to(base)
            or output.is_relative_to(dependencies)):
        raise ValueError("OUTPUT_MUST_BE_NEW_AND_OUTSIDE_INPUT_ROOTS")
    output.mkdir(parents=True, exist_ok=False)
    metadata = {
        "kind": "DEVELOPMENT_COMPILE", "claim_authority": "NONE",
        "claim_status": "UNVERIFIED", "check_status": "UNVERIFIED",
        "scope": "Conditional interior localMass zero; C04/epsilon/coordinates/Z04 excluded",
        "started_utc": datetime.now(timezone.utc).isoformat(), "stages": {},
    }
    env = os.environ.copy()
    env.pop("LEAN_PATH", None)
    env.pop("LEAN_SRC_PATH", None)

    def save():
        (output / "run-metadata.json").write_text(json.dumps(metadata, indent=2), encoding="utf-8")

    def stage(name, command, stage_env):
        info = {"command": command, "exit": None}
        metadata["stages"][name] = info
        save()
        started = time.monotonic()
        try:
            with (output / (name + ".stdout.log")).open("xb") as out, \
                    (output / (name + ".stderr.log")).open("xb") as err:
                info["exit"] = subprocess.run(
                    command, cwd=source, env=stage_env, stdout=out, stderr=err
                ).returncode
        except OSError as exc:
            info["invocation_exception"] = repr(exc)
            raise RuntimeError(name.upper() + "_INVOCATION") from exc
        finally:
            info["elapsed_seconds"] = time.monotonic() - started
            for stream in ("stdout", "stderr"):
                path = output / (name + "." + stream + ".log")
                if path.exists():
                    info[stream + "_sha256"] = sha(path)
                    info[stream + "_bytes"] = path.stat().st_size
            save()
        if info["exit"] != 0:
            raise RuntimeError(name.upper() + "_LEAN_COMPILE")
        if info["stderr_bytes"]:
            raise RuntimeError(name.upper() + "_STDERR_REVIEW")

    try:
        if not re.fullmatch(r"[0-9a-f]{64}", expected_sha) or sha(proof) != expected_sha:
            raise ValueError("PROOF_SHA_MISMATCH")
        for module, digest in DEPENDENCIES.items():
            if sha(dependencies / (module + ".lean")) != digest:
                raise ValueError("DEPENDENCY_SHA_MISMATCH: " + module)
        helper_path = base / "colab/run-c02-development.py"
        committed = subprocess.check_output(
            ["git", "show", BASE + ":colab/run-c02-development.py"], cwd=base, env=env
        )
        head = subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=base, env=env)
        if head.decode().strip() != BASE or helper_path.read_bytes() != committed:
            raise ValueError("PINNED_IDENTITY_HELPER_MISMATCH")
        spec = importlib.util.spec_from_file_location("source_checks", helper_path)
        helper = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(helper)
        inputs, artifacts = output / "inputs", output / "artifacts"
        inputs.mkdir()
        artifacts.mkdir()
        driver = Path(__file__).resolve()
        originals = {module + ".lean": dependencies / (module + ".lean")
                     for module in DEPENDENCIES}
        originals.update({MODULE + ".lean": proof, driver.name: driver,
                          "run-c02-development.py": helper_path})
        for name, original in originals.items():
            shutil.copyfile(original, inputs / name)
        metadata["inputs"] = {p.name: sha(p) for p in inputs.iterdir()}
        metadata["proof_state"] = "UNCOMMITTED_DEVELOPMENT_BYTES"
        metadata["helper_base_commit"] = BASE
        metadata["pre_source_identity"] = helper.source_identity(source, env)
        stage("source", ["lake", "build", "+NavierStokes.OutgoingProfile"], env)
        target = source / ".lake/build/lib/lean/NavierStokes/OutgoingProfile.olean"
        metadata["target_olean_before_sha256"] = sha(target)
        proof_env = env.copy()
        proof_env["LEAN_PATH"] = str(artifacts)
        metadata["fresh_artifacts"] = {}
        metadata["axiom_surfaces"] = {}
        for short, module in zip(SURFACES, [*DEPENDENCIES, MODULE], strict=True):
            fresh = artifacts / (module + ".olean")
            if fresh.exists():
                raise ValueError("ARTIFACT_NOT_FRESH: " + module)
            stage(short, ["lake", "env", "lean", "-R", str(inputs),
                          "-o", str(fresh), str(inputs / (module + ".lean"))], proof_env)
            metadata["fresh_artifacts"][fresh.name] = sha(fresh)
            metadata["axiom_surfaces"][short] = inspect_axioms(
                (output / (short + ".stdout.log")).read_text(encoding="utf-8"), SURFACES[short]
            )
        metadata["target_olean_after_sha256"] = sha(target)
        metadata["post_source_identity"] = helper.source_identity(source, env)
        if metadata["pre_source_identity"] != metadata["post_source_identity"]:
            raise ValueError("SOURCE_IDENTITY_DRIFT")
        if metadata["target_olean_before_sha256"] != metadata["target_olean_after_sha256"]:
            raise ValueError("SOURCE_TARGET_DRIFT")
        if metadata["inputs"] != {p.name: sha(p) for p in inputs.iterdir()}:
            raise ValueError("ARCHIVED_INPUT_DRIFT")
        if metadata["fresh_artifacts"] != {p.name: sha(p) for p in artifacts.iterdir()}:
            raise ValueError("FRESH_ARTIFACT_DRIFT")
        if any(sha(p) != metadata["inputs"][name] for name, p in originals.items()):
            raise ValueError("EXECUTION_INPUT_DRIFT")
        metadata["check_status"] = "PASS[LOCAL_PROOF_COMPILE:P2_Z03]"
    except Exception as exc:
        metadata["check_status"] = "ERROR[Z03_DEVELOPMENT_COMPILE]"
        metadata["failure_boundary"] = getattr(exc, "boundary", str(exc))
        metadata["error_type"] = type(exc).__name__
        metadata["mathematical_interpretation"] = "NONE"
    finally:
        metadata["finished_utc"] = datetime.now(timezone.utc).isoformat()
        save()
        with zipfile.ZipFile(archive, "x", zipfile.ZIP_DEFLATED) as bundle:
            for path in output.rglob("*"):
                if path.is_file():
                    bundle.write(path, path.relative_to(output).as_posix())
        print(metadata["check_status"], "claim_authority=NONE", flush=True)
        print("ARCHIVE", archive, sha(archive), archive.stat().st_size, flush=True)
    return metadata


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    for name in ("source", "base", "dependencies", "proof", "output"):
        parser.add_argument("--" + name, type=Path, required=True)
    parser.add_argument("--proof-sha256", required=True)
    args = parser.parse_args()
    outcome = run(args.source, args.base, args.dependencies, args.proof,
                  args.output, args.proof_sha256)
    raise SystemExit(0 if outcome["check_status"].startswith("PASS[") else 1)
