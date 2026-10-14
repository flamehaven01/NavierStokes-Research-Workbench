#!/usr/bin/env python3
"""Develop only Z01's two mass identities; no bootstrap or claim admission."""

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

MODULE = "P2_Z01_LocalMassIdentities"
THEOREMS = ("localMass_partial_identity", "localMass_tail_identity")
BASE = "10d5a1f517b8665137f2354746d70752f8ef67fd"


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def inspect_axioms(text):
    if "sorryAx" in text:
        raise ValueError("SORRY_AXIOM_OBSERVED")
    result = {}
    for short in THEOREMS:
        name = "NSRW.P2." + short
        matches = re.findall(r"'" + re.escape(name) + r"' depends on axioms: \[([^\]]*)\]", text)
        if len(matches) != 1:
            raise ValueError("AXIOM_SURFACE_MISSING_OR_DUPLICATED: " + name)
        values = [part.strip() for part in matches[0].split(",")]
        if len(values) != 3 or set(values) != {"propext", "Classical.choice", "Quot.sound"}:
            raise ValueError("AXIOM_SURFACE_UNEXPECTED: " + name)
        result[name] = sorted(values)
    return result


def run(source, base, proof, output, expected_sha):
    source, base, proof, output = (p.resolve() for p in (source, base, proof, output))
    if output.exists() or output.is_relative_to(source) or output.is_relative_to(base):
        raise ValueError("OUTPUT_MUST_BE_NEW_AND_OUTSIDE_CHECKOUTS")
    output.mkdir(parents=True, exist_ok=False)
    metadata = {"kind": "DEVELOPMENT_COMPILE", "claim_authority": "NONE",
                "claim_status": "UNVERIFIED", "check_status": "UNVERIFIED",
                "scope": "Two Z01 mass identities only; no boundary signs or IVT",
                "started_utc": datetime.now(timezone.utc).isoformat(), "stages": {}}
    env = os.environ.copy()
    env.pop("LEAN_PATH", None)
    env.pop("LEAN_SRC_PATH", None)

    def save():
        (output / "run-metadata.json").write_text(json.dumps(metadata, indent=2), encoding="utf-8")

    def query(args):
        return subprocess.check_output(args, cwd=base, env=env).decode().strip()

    def stage(name, command):
        info = {"command": command, "exit": None}
        metadata["stages"][name] = info
        save()
        started = time.monotonic()
        try:
            with (output / (name + ".stdout.log")).open("xb") as out, \
                    (output / (name + ".stderr.log")).open("xb") as err:
                info["exit"] = subprocess.run(command, cwd=source, env=env,
                                               stdout=out, stderr=err).returncode
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
        helper_path = base / "colab/run-c02-development.py"
        committed = subprocess.check_output(["git", "show", BASE + ":colab/run-c02-development.py"],
                                            cwd=base, env=env)
        if query(["git", "rev-parse", "HEAD"]) != BASE or helper_path.read_bytes() != committed:
            raise ValueError("PINNED_IDENTITY_HELPER_MISMATCH")
        spec = importlib.util.spec_from_file_location("source_checks", helper_path)
        helper = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(helper)
        inputs, artifacts = output / "inputs", output / "artifacts"
        inputs.mkdir()
        artifacts.mkdir()
        copied = inputs / (MODULE + ".lean")
        driver = Path(__file__).resolve()
        for original, name in ((proof, copied.name), (driver, driver.name),
                               (helper_path, "run-c02-development.py")):
            shutil.copyfile(original, inputs / name)
        metadata["inputs"] = {p.name: sha(p) for p in inputs.iterdir()}
        metadata["proof_state"] = "UNCOMMITTED_DEVELOPMENT_BYTES"
        metadata["helper_base_commit"] = BASE
        metadata["pre_source_identity"] = helper.source_identity(source, env)
        stage("source", ["lake", "build", "+NavierStokes.OutgoingProfile"])
        target = source / ".lake/build/lib/lean/NavierStokes/OutgoingProfile.olean"
        metadata["target_olean_before_sha256"] = sha(target)
        fresh = artifacts / (MODULE + ".olean")
        if fresh.exists():
            raise ValueError("ARTIFACT_NOT_FRESH")
        stage("z01", ["lake", "env", "lean", "-R", str(inputs), "-o", str(fresh), str(copied)])
        metadata["axiom_surface"] = inspect_axioms((output / "z01.stdout.log").read_text())
        metadata["fresh_olean_sha256"] = sha(fresh)
        metadata["target_olean_after_sha256"] = sha(target)
        metadata["post_source_identity"] = helper.source_identity(source, env)
        if metadata["pre_source_identity"] != metadata["post_source_identity"]:
            raise ValueError("SOURCE_IDENTITY_DRIFT")
        if metadata["target_olean_before_sha256"] != metadata["target_olean_after_sha256"]:
            raise ValueError("SOURCE_TARGET_DRIFT")
        if metadata["inputs"] != {p.name: sha(p) for p in inputs.iterdir()}:
            raise ValueError("ARCHIVED_INPUT_DRIFT")
        if sha(proof) != expected_sha or sha(driver) != metadata["inputs"][driver.name]:
            raise ValueError("EXECUTION_INPUT_DRIFT")
        metadata["check_status"] = "PASS[LOCAL_PROOF_COMPILE:P2_Z01]"
    except Exception as exc:
        metadata["check_status"] = "ERROR[Z01_DEVELOPMENT_COMPILE]"
        metadata["failure_boundary"] = getattr(exc, "boundary", str(exc))
        metadata["error_type"] = type(exc).__name__
        metadata["mathematical_interpretation"] = "NONE"
    finally:
        metadata["finished_utc"] = datetime.now(timezone.utc).isoformat()
        save()
        archive = Path(str(output) + "-evidence.zip")
        with zipfile.ZipFile(archive, "x", zipfile.ZIP_DEFLATED) as bundle:
            for path in output.rglob("*"):
                if path.is_file():
                    bundle.write(path, path.relative_to(output).as_posix())
        print(metadata["check_status"], "claim_authority=NONE", flush=True)
        print("ARCHIVE", archive, sha(archive), archive.stat().st_size, flush=True)
    return metadata


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    for name in ("source", "base", "proof", "output"):
        parser.add_argument("--" + name, type=Path, required=True)
    parser.add_argument("--proof-sha256", required=True)
    args = parser.parse_args()
    outcome = run(args.source, args.base, args.proof, args.output, args.proof_sha256)
    raise SystemExit(0 if outcome["check_status"].startswith("PASS[") else 1)
