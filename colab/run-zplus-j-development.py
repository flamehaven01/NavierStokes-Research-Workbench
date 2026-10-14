"""Development only: source -> fresh Z01 -> Z02 -> conditional Z+J; no admission."""

import argparse
import hashlib
import importlib.util
import json
import os
import re
import shutil
import subprocess
import sys
import time
import zipfile
from datetime import datetime, timezone
from pathlib import Path

BASE = "10d5a1f517b8665137f2354746d70752f8ef67fd"
HELPER_BLOB = "518de06530c4c7c56edafdf571e5fb2ef0f808b3"
DEPENDENCIES = {
    "P2_Z01_LocalMassIdentities": "ff7101067a98fbaa8974c1aa409b83740cd17eb4f1778f20cdc23b44e2a5c267",
    "P2_Z02_BoundaryMassSigns": "7b5764911790054cbba982acfde8ed673705a2d68e85bcd341507d7e0b5f8c2c",
}
MODULE = "P2_ZPLUS_J_FirstRepairAngularMoment"
THEOREMS = (
    "localAngularMoment_partial_identity", "localAngularMoment_tail_identity",
    "first_upper_lt_second_lower", "secondExponent_eq_first_sub_lam",
    "future_radialPulse_eq_two_bumps", "weighted_future_integral_eq_two_tails",
    "secondBump_massTail_pos", "firstRepair_mass_zero_tail_balance",
    "firstBumpTail_pos_and_firstCoeff_neg", "firstBump_angularTail_lower",
    "secondBump_angularTail_upper", "angularMoment_pos_of_firstRepair_mass_zero",
)
STANDARD_AXIOMS = {"propext", "Classical.choice", "Quot.sound"}


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def blob(data):
    return hashlib.sha1(b"blob " + str(len(data)).encode() + b"\0" + data).hexdigest()


def run_command(command, **kwargs):
    """Bounded test boundary: do not monkeypatch stdlib subprocess globally."""
    return subprocess.run(command, **kwargs)


def query(root, command, env):
    result = run_command(command, cwd=root, env=env, capture_output=True, check=False)
    if result.returncode:
        raise RuntimeError("IDENTITY_QUERY_FAILED: " + repr(command))
    return result.stdout


def inspect_axioms(text):
    if "sorryAx" in text:
        raise ValueError("SORRY_AXIOM_OBSERVED")
    result = {}
    for short in THEOREMS:
        name = "NSRW.P2." + short
        matches = re.findall(r"'" + re.escape(name) + r"' depends on axioms: \[([^\]]*)\]", text)
        empty = text.count("'" + name + "' does not depend on any axioms")
        if len(matches) + empty != 1:
            raise ValueError("AXIOM_SURFACE_MISSING_OR_DUPLICATED: " + name)
        values = [p.strip() for p in matches[0].split(",") if p.strip()] if matches else []
        if len(values) != len(set(values)) or not set(values) <= STANDARD_AXIOMS:
            raise ValueError("AXIOM_SURFACE_UNEXPECTED: " + name)
        # Arithmetic helpers may have a smaller surface; the structural target
        # must match the already reviewed source-proof surface exactly.
        if short == THEOREMS[-1] and set(values) != STANDARD_AXIOMS:
            raise ValueError("TARGET_AXIOM_SURFACE_UNEXPECTED")
        result[name] = sorted(values)
    return result


def run(source, base, dependencies, proof, output, expected_sha):
    source, base, dependencies, proof, output = (
        p.resolve() for p in (source, base, dependencies, proof, output)
    )
    archive = Path(str(output) + "-evidence.zip")
    if (output.exists() or archive.exists() or proof.is_relative_to(output)
            or any(output.is_relative_to(root) for root in (source, base, dependencies))):
        raise ValueError("OUTPUT_MUST_BE_NEW_AND_OUTSIDE_INPUT_ROOTS")
    output.mkdir(parents=True, exist_ok=False)
    meta = {
        "kind": "ZPLUS_J_DEVELOPMENT_COMPILE", "claim_authority": "NONE",
        "claim_status": "UNVERIFIED", "check_status": "ERROR[NOT_COMPLETED]",
        "scope": "First-window localMass=0 and c1>0 imply localAngularMoment>0 only",
        "non_claims": ["eta sign", "epsilon", "existence composition", "Profile.J bridge",
                       "uniqueness", "simple zero", "Q pole or limit", "claim admission"],
        "started_utc": datetime.now(timezone.utc).isoformat(), "stages": {},
        "inputs": {}, "fresh_artifacts": {},
    }
    env = os.environ.copy()
    env["PATH"] = "/root/.elan/bin:" + env.get("PATH", "")
    env.pop("LEAN_PATH", None)
    env.pop("LEAN_SRC_PATH", None)

    def save():
        (output / "run-metadata.json").write_text(json.dumps(meta, indent=2), encoding="utf-8")

    def stage(name, command, stage_env):
        info = {"command": command, "exit": None}
        meta["stages"][name] = info
        meta["active_stage"] = name
        save()
        started = time.monotonic()
        try:
            with (output / (name + ".stdout.log")).open("xb") as out, \
                    (output / (name + ".stderr.log")).open("xb") as err:
                info["exit"] = run_command(
                    command, cwd=source, env=stage_env, stdout=out, stderr=err, check=False
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
        print(name, "exit", info["exit"], flush=True)
        if info["exit"] != 0:
            raise RuntimeError(name.upper() + "_LEAN_COMPILE")
        if info["stderr_bytes"]:
            raise RuntimeError(name.upper() + "_STDERR_REVIEW")
        if "sorryAx" in (output / (name + ".stdout.log")).read_bytes().decode(
                "utf-8", errors="replace"):
            raise RuntimeError(name.upper() + "_SORRY_AXIOM_OBSERVED")

    save()
    try:
        if not re.fullmatch(r"[0-9a-f]{64}", expected_sha) or sha(proof) != expected_sha:
            raise ValueError("PROOF_SHA_MISMATCH")
        for module, digest in DEPENDENCIES.items():
            if sha(dependencies / (module + ".lean")) != digest:
                raise ValueError("DEVELOPMENT_DEPENDENCY_SHA_MISMATCH: " + module)
        if query(base, ["git", "rev-parse", "HEAD"], env).decode().strip() != BASE:
            raise ValueError("DEPENDENCY_BASE_MISMATCH")
        helper_data = query(base, ["git", "show", BASE + ":colab/run-c02-development.py"], env)
        if blob(helper_data) != HELPER_BLOB:
            raise ValueError("PINNED_IDENTITY_HELPER_MISMATCH")
        inputs, artifacts = output / "inputs", output / "artifacts"
        inputs.mkdir()
        artifacts.mkdir()
        helper_path = inputs / "run-c02-development.py"
        helper_path.write_bytes(helper_data)
        driver = Path(__file__).resolve()
        originals = {module + ".lean": dependencies / (module + ".lean")
                     for module in DEPENDENCIES}
        originals.update({MODULE + ".lean": proof, driver.name: driver})
        for name, original in originals.items():
            shutil.copyfile(original, inputs / name)
        meta["inputs"] = {p.name: sha(p) for p in inputs.iterdir()}
        meta["helper_git_blob"] = HELPER_BLOB
        meta["helper_base_commit"] = BASE
        meta["proof_state"] = "UNCOMMITTED_DEVELOPMENT_BYTES"
        spec = importlib.util.spec_from_file_location("zplus_source_checks", helper_path)
        helper = importlib.util.module_from_spec(spec)
        previous_bytecode = sys.dont_write_bytecode
        try:
            sys.dont_write_bytecode = True
            spec.loader.exec_module(helper)
        finally:
            sys.dont_write_bytecode = previous_bytecode
        meta["pre_source_identity"] = helper.source_identity(source, env)
        meta["nsrw_pre_observation"] = helper.nsrw_observation(base, env)
        stage("source", ["lake", "build", "+NavierStokes.OutgoingProfile"], env)
        target = source / helper.TARGET_ARTIFACT
        meta["target_olean_before_sha256"] = sha(target)
        proof_env = env.copy()
        proof_env["LEAN_PATH"] = str(artifacts)
        for module in [*DEPENDENCIES, MODULE]:
            fresh = artifacts / (module + ".olean")
            if fresh.exists():
                raise ValueError("ARTIFACT_NOT_FRESH: " + module)
            stage(module, ["lake", "env", "lean", "-R", str(inputs),
                           "-o", str(fresh), str(inputs / (module + ".lean"))], proof_env)
            if not fresh.is_file() or fresh.is_symlink():
                raise ValueError("FRESH_ARTIFACT_MISSING: " + module)
            meta["fresh_artifacts"][fresh.name] = sha(fresh)
        meta["axiom_surfaces"] = inspect_axioms(
            (output / (MODULE + ".stdout.log")).read_text(encoding="utf-8")
        )
        meta["target_olean_after_sha256"] = sha(target)
        meta["post_source_identity"] = helper.source_identity(source, env)
        meta["nsrw_post_observation"] = helper.nsrw_observation(base, env)
        if meta["pre_source_identity"] != meta["post_source_identity"]:
            raise ValueError("SOURCE_IDENTITY_DRIFT")
        if meta["nsrw_pre_observation"] != meta["nsrw_post_observation"]:
            raise ValueError("NSRW_OBSERVATION_DRIFT")
        if meta["target_olean_before_sha256"] != meta["target_olean_after_sha256"]:
            raise ValueError("SOURCE_TARGET_DRIFT")
        if meta["inputs"] != {p.name: sha(p) for p in inputs.iterdir()}:
            raise ValueError("ARCHIVED_INPUT_DRIFT")
        if meta["fresh_artifacts"] != {p.name: sha(p) for p in artifacts.iterdir()}:
            raise ValueError("FRESH_ARTIFACT_DRIFT")
        if any(sha(p) != meta["inputs"][name] for name, p in originals.items()):
            raise ValueError("EXECUTION_INPUT_DRIFT")
        for name, info in meta["stages"].items():
            for stream in ("stdout", "stderr"):
                if sha(output / (name + "." + stream + ".log")) != info[stream + "_sha256"]:
                    raise ValueError("LOG_DRIFT: " + name)
        meta["check_status"] = "PASS[LOCAL_PROOF_COMPILE:P2_ZPLUS_J]"
    except Exception as exc:
        meta["check_status"] = "ERROR[ZPLUS_J_DEVELOPMENT_COMPILE]"
        meta["failure_boundary"] = getattr(exc, "boundary", str(exc))
        meta["error_type"] = type(exc).__name__
        meta["mathematical_interpretation"] = "NONE"
    finally:
        meta["finished_utc"] = datetime.now(timezone.utc).isoformat()
        save()
        with zipfile.ZipFile(archive, "x", zipfile.ZIP_DEFLATED) as bundle:
            for path in output.rglob("*"):
                if path.is_file():
                    bundle.write(path, path.relative_to(output).as_posix())
        print(meta["check_status"], "claim_authority=NONE", flush=True)
        print("ARCHIVE", archive, sha(archive), archive.stat().st_size, flush=True)
    return meta


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    for name in ("source", "base", "dependencies", "proof", "output"):
        parser.add_argument("--" + name, type=Path, required=True)
    parser.add_argument("--proof-sha256", required=True)
    args = parser.parse_args()
    outcome = run(args.source, args.base, args.dependencies, args.proof,
                  args.output, args.proof_sha256)
    raise SystemExit(0 if outcome["check_status"].startswith("PASS[") else 1)
