#!/usr/bin/env python3
"""One C02 development compile; no installation or commit-bound claim admission."""

import argparse
import hashlib
import json
import os
import platform
import re
import shutil
import subprocess
import time
from datetime import datetime, timezone
from pathlib import Path

SOURCE_COMMIT = "8937a8f4cbc7abaab5e9e97d1cc7f5d2319d9538"
MANIFEST_BLOB = "f07a8454cb6200d90bcc4371bc9965e9f8f46c7d"
TOOLCHAIN = "leanprover/lean4:v4.34.0-rc2"
LEAN_COMMIT = "6a10ac8c22beadecabdbb0919c2b50214762f91d"
TARGET = "+NavierStokes.OutgoingProfile"
MODULE = "P2_C02_ActualCoefficientDecomposition"
PROOF = f"formal/p2/{MODULE}.lean"
PROOF_BLOB = "fe4c2d1e18c7fbe9db5b9ce36196a9c22184827c"
TARGET_ARTIFACT = ".lake/build/lib/lean/NavierStokes/OutgoingProfile.olean"
THEOREMS = (
    "actualRepairCoefficient_decomposition",
    "profile_secondRepairCoefficient_decomposition",
)
AXIOMS = {"propext", "Classical.choice", "Quot.sound"}


class RunFailure(RuntimeError):
    def __init__(self, boundary, message):
        super().__init__(message)
        self.boundary = boundary


def require(condition, boundary, message):
    if not condition:
        raise RunFailure(boundary, message)


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def run_command(args, **kwargs):
    """Bounded mock boundary: tests must not patch stdlib subprocess.run."""
    return subprocess.run(args, **kwargs)


def query(root, args, env):
    result = run_command(args, cwd=root, env=env, capture_output=True, check=False)
    if result.returncode != 0:
        failure = RunFailure("ENVIRONMENT_IDENTITY", "QUERY_FAILED: " + args[0])
        failure.command = args
        failure.exit_code = result.returncode
        failure.stdout = result.stdout
        failure.stderr = result.stderr
        raise failure
    return result.stdout.decode("utf-8", errors="replace").strip()


def reject_shadow_inputs(root, env):
    tracked = set(query(root, ["git", "ls-files", "-z"], env).split("\0"))
    for directory, folders, files in os.walk(root):
        folders[:] = [name for name in folders if name not in {".git", ".lake"}]
        for name in files:
            path = Path(directory) / name
            if path.suffix in {".lean", ".olean", ".ilean"}:
                relative = path.relative_to(root).as_posix()
                require(relative in tracked, "SOURCE_IDENTITY", "UNTRACKED_LEAN_SHADOW_INPUT: " + relative)


def proof_identity(root, env):
    identity = {
        "head": query(root, ["git", "rev-parse", "HEAD"], env),
        "head_git_blob": query(root, ["git", "rev-parse", "HEAD:" + PROOF], env),
        "tracked_diff_status": query(root, ["git", "status", "--porcelain",
                                           "--untracked-files=no", "--", PROOF], env),
        "worktree_git_blob": query(root, ["git", "hash-object", PROOF], env),
        "executor_raw_sha256": digest(root / PROOF),
    }
    require(identity["head_git_blob"] == PROOF_BLOB, "INPUT_IDENTITY", "PROOF_HEAD_BLOB_MISMATCH")
    require(not identity["tracked_diff_status"], "INPUT_IDENTITY", "PROOF_TRACKED_DIFF")
    require(identity["worktree_git_blob"] == PROOF_BLOB,
            "INPUT_IDENTITY", "PROOF_WORKTREE_BLOB_MISMATCH")
    return identity


def source_identity(source, env):
    manifest = source / "lake-manifest.json"
    identity = {
        "commit": query(source, ["git", "rev-parse", "HEAD"], env),
        "manifest_blob": query(source, ["git", "rev-parse", "HEAD:lake-manifest.json"], env),
        "manifest_raw_sha256": digest(manifest),
        "tracked_status": query(source, ["git", "status", "--porcelain", "--untracked-files=no"], env),
        "toolchain_file": (source / "lean-toolchain").read_text(encoding="utf-8").strip(),
        "dependencies": {},
    }
    require(identity["commit"] == SOURCE_COMMIT, "SOURCE_IDENTITY", "SOURCE_COMMIT_MISMATCH")
    require(identity["manifest_blob"] == MANIFEST_BLOB, "SOURCE_IDENTITY", "MANIFEST_MISMATCH")
    require(not identity["tracked_status"], "SOURCE_IDENTITY", "SOURCE_TRACKED_DIRTY")
    require(identity["toolchain_file"] == TOOLCHAIN, "SOURCE_IDENTITY", "TOOLCHAIN_FILE_MISMATCH")
    for package in json.loads(manifest.read_text(encoding="utf-8"))["packages"]:
        root = source / ".lake/packages" / package["name"]
        require(root.is_dir(), "ENVIRONMENT_IDENTITY", "DEPENDENCY_MISSING: " + package["name"])
        revision = query(root, ["git", "rev-parse", "HEAD"], env)
        require(revision == package["rev"], "SOURCE_IDENTITY", "DEPENDENCY_REVISION_MISMATCH")
        dirty = query(root, ["git", "status", "--porcelain", "--untracked-files=no"], env)
        require(not dirty, "SOURCE_IDENTITY", "DEPENDENCY_TRACKED_DIRTY")
        identity["dependencies"][package["name"]] = revision
    reject_shadow_inputs(source, env)
    installed = query(source, ["elan", "toolchain", "list"], env)
    require(any(line.split() and line.split()[0] == TOOLCHAIN for line in installed.splitlines()),
            "ENVIRONMENT_IDENTITY", "PINNED_TOOLCHAIN_NOT_INSTALLED")
    # Refuse absent toolchains before invoking elan-managed Lean/Lake binaries.
    identity["lean_version"] = query(source, ["lake", "env", "lean", "--version"], env)
    identity["lake_version"] = query(source, ["lake", "--version"], env)
    require("4.34.0-rc2" in identity["lean_version"] and LEAN_COMMIT in identity["lean_version"],
            "SOURCE_IDENTITY", "LEAN_VERSION_MISMATCH")
    return identity


def nsrw_observation(root, env):
    """Observation only: dirty/untracked development inputs are permitted."""
    tracked = query(root, ["git", "status", "--porcelain", "--untracked-files=no"], env)
    untracked = query(root, ["git", "ls-files", "--others", "--exclude-standard"], env)
    return {
        "head": query(root, ["git", "rev-parse", "HEAD"], env),
        "tracked_dirty": bool(tracked),
        "untracked_count": len(untracked.splitlines()),
    }


def axiom_surface(text):
    require("sorryAx" not in text, "AXIOM_SURFACE", "SORRY_AXIOM_OBSERVED")
    result = {}
    for short in THEOREMS:
        name = "NSRW.P2." + short
        matches = re.findall(r"'" + re.escape(name) + r"' depends on axioms: \[([^\]]*)\]", text)
        require(len(matches) == 1, "AXIOM_SURFACE", "AXIOM_OUTPUT_MISSING_OR_DUPLICATED: " + name)
        values = [item.strip() for item in matches[0].split(",") if item.strip()]
        require(len(values) == len(AXIOMS) and set(values) == AXIOMS,
                "AXIOM_SURFACE", "UNEXPECTED_AXIOM_SURFACE: " + name)
        result[name] = sorted(values)
    return result


def run(source, nsrw, output, expected_proof_sha256):
    source, nsrw, output = source.resolve(), nsrw.resolve(), output.resolve()
    require(re.fullmatch(r"[0-9a-f]{64}", expected_proof_sha256) is not None,
            "INPUT_IDENTITY", "EXPECTED_SHA_MUST_BE_LOWERCASE_64_HEX")
    require(not output.exists(), "OUTPUT_LOCATION", "OUTPUT_ALREADY_EXISTS")
    require(not output.is_relative_to(source), "OUTPUT_LOCATION", "OUTPUT_INSIDE_SOURCE")
    require(not output.is_relative_to(nsrw / "formal"), "OUTPUT_LOCATION", "OUTPUT_INSIDE_PROOFS")
    output.mkdir(parents=True, exist_ok=False)
    metadata = {
        "kind": "DEVELOPMENT_COMPILE", "claim_authority": "NONE", "claim_status": "UNVERIFIED",
        "check_status": "UNVERIFIED", "started_utc": datetime.now(timezone.utc).isoformat(),
        "scope": "Two C02 equalities only; no actual coefficient sign or mass zero claim",
        "stages": {},
    }
    env = os.environ.copy()
    env.pop("LEAN_PATH", None)
    env.pop("LEAN_SRC_PATH", None)
    proof, driver = nsrw / PROOF, Path(__file__).resolve()

    def save():
        (output / "run-metadata.json").write_text(json.dumps(metadata, indent=2), encoding="utf-8")

    def stage(name, args):
        out, err = output / f"{name}.stdout.log", output / f"{name}.stderr.log"
        started = time.monotonic()
        info = {"command": args, "exit_code": None}
        metadata["stages"][name] = info
        save()
        try:
            with out.open("wb") as stdout, err.open("wb") as stderr:
                result = run_command(args, cwd=source, env=env, stdout=stdout, stderr=stderr, check=False)
            info["exit_code"] = result.returncode
        except OSError as exc:
            info["exception_type"] = type(exc).__name__
            info["exception"] = str(exc)
            raise RunFailure(name.upper() + "_INVOCATION", "INVOCATION_FAILED: " + name) from exc
        finally:
            info["elapsed_seconds"] = time.monotonic() - started
            for label, path in (("stdout", out), ("stderr", err)):
                if path.exists():
                    info[label + "_sha256"] = digest(path)
                    info[label + "_bytes"] = path.stat().st_size
            save()
        require(result.returncode == 0, name.upper() + "_EXECUTION", "NONZERO_EXIT: " + name)
        require(err.stat().st_size == 0, "STDERR_REVIEW", "STDERR_REQUIRES_REVIEW: " + name)

    save()
    try:
        metadata["runtime"] = {"os": platform.system(), "release": platform.release()}
        require(proof.is_file() and not proof.is_symlink(), "INPUT_IDENTITY", "PROOF_UNAVAILABLE")
        require(digest(proof) == expected_proof_sha256, "INPUT_IDENTITY", "PROOF_SHA_MISMATCH")
        inputs, artifacts = output / "inputs", output / "artifacts"
        inputs.mkdir()
        artifacts.mkdir()
        copied = inputs / proof.name
        runner_copy = inputs / "run-c02-development.py"
        shutil.copyfile(proof, copied)
        shutil.copyfile(driver, runner_copy)
        metadata["proof_sha256"] = expected_proof_sha256
        metadata["runner_sha256"] = digest(driver)
        require(digest(copied) == expected_proof_sha256, "INPUT_IDENTITY", "COPIED_PROOF_CHANGED")
        metadata["nsrw_pre_observation"] = nsrw_observation(nsrw, env)
        metadata["pre_proof_identity"] = proof_identity(nsrw, env)
        metadata["pre_source_identity"] = source_identity(source, env)
        save()
        stage("source", ["lake", "build", TARGET])
        target, fresh = source / TARGET_ARTIFACT, artifacts / f"{MODULE}.olean"
        metadata["target_olean_before_c02_sha256"] = digest(target)
        require(not fresh.exists(), "ARTIFACT_IDENTITY", "FRESH_ARTIFACT_ALREADY_EXISTS")
        stage("c02", ["lake", "env", "lean", "-R", str(inputs), "-o", str(fresh), str(copied)])
        metadata["axiom_surface"] = axiom_surface(
            (output / "c02.stdout.log").read_bytes().decode("utf-8", errors="replace")
        )
        require(fresh.is_file() and not fresh.is_symlink(), "ARTIFACT_IDENTITY", "FRESH_ARTIFACT_MISSING")
        metadata["fresh_olean_sha256"] = digest(fresh)
        metadata["target_olean_after_c02_sha256"] = digest(target)
        require(metadata["target_olean_before_c02_sha256"] == metadata["target_olean_after_c02_sha256"],
                "ARTIFACT_IDENTITY", "SOURCE_TARGET_ARTIFACT_CHANGED")
        metadata["post_source_identity"] = source_identity(source, env)
        require(metadata["pre_source_identity"] == metadata["post_source_identity"],
                "SOURCE_IDENTITY", "SOURCE_IDENTITY_CHANGED")
        metadata["nsrw_post_observation"] = nsrw_observation(nsrw, env)
        metadata["post_proof_identity"] = proof_identity(nsrw, env)
        pre_binding = {k: v for k, v in metadata["pre_proof_identity"].items() if k != "head"}
        post_binding = {k: v for k, v in metadata["post_proof_identity"].items() if k != "head"}
        require(pre_binding == post_binding,
                "INPUT_IDENTITY", "PROOF_GIT_IDENTITY_CHANGED")
        require(digest(proof) == digest(copied) == expected_proof_sha256,
                "INPUT_IDENTITY", "PROOF_CHANGED_DURING_RUN")
        require(digest(driver) == digest(runner_copy) == metadata["runner_sha256"],
                "INPUT_IDENTITY", "RUNNER_CHANGED_DURING_RUN")
        require(digest(fresh) == metadata["fresh_olean_sha256"],
                "ARTIFACT_IDENTITY", "FRESH_ARTIFACT_CHANGED")
        metadata["check_status"] = "PASS[LOCAL_PROOF_COMPILE:P2_C02]"
    except Exception as exc:
        metadata["check_status"] = "ERROR[DEVELOPMENT_COMPILE]"
        metadata["failure_boundary"] = getattr(exc, "boundary", "ENVIRONMENT_OR_INVOCATION_REVIEW")
        metadata["error"] = str(exc)
        metadata["mathematical_interpretation"] = "NONE; inspect raw logs before classifying cause"
        if hasattr(exc, "command"):
            metadata["failed_identity_query"] = {"command": exc.command, "exit_code": exc.exit_code}
            for label in ("stdout", "stderr"):
                path = output / f"identity-query.{label}.log"
                path.write_bytes(getattr(exc, label))
                metadata["failed_identity_query"][label + "_sha256"] = digest(path)
    finally:
        metadata["finished_utc"] = datetime.now(timezone.utc).isoformat()
        save()
    return metadata


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--source-root", type=Path, required=True)
    parser.add_argument("--nsrw-root", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--proof-sha256", required=True, help="Reviewed executor raw SHA, not a Git blob")
    args = parser.parse_args()
    try:
        metadata = run(args.source_root, args.nsrw_root, args.output, args.proof_sha256)
    except RunFailure as exc:
        print(f"ERROR[{exc.boundary}]: {exc}")
        return 1
    # Never dump raw logs through a Windows console; their original bytes are saved.
    print(metadata["check_status"])
    print("claim_authority=NONE")
    return 0 if metadata["check_status"].startswith("PASS[") else 1


if __name__ == "__main__":
    raise SystemExit(main())
