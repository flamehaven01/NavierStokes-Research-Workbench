#!/usr/bin/env python3
"""Commit-bound L3 replay only; no bootstrap, F1/L2 imports, or claim promotion."""

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
PROOF = "formal/p2/P2_L3_TemplateMomentComparison.lean"
PROOF_SHA256 = "9ad9b6ea625e2c39f126a8d3a770cb365f48db9f67c734964d972e382b5fa1d4"
RUNNER = "scripts/run-p2-l3-replay.py"
TARGET = "+NavierStokes.OutgoingPulseBounds"
THEOREM = "NSRW.P2.rowMoment_one_scaled_le_rowMoment_zero"
AXIOMS = {"propext", "Classical.choice", "Quot.sound"}


def ensure(condition, message):
    if not condition:
        raise RuntimeError(message)


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def query(root, args, env):
    return subprocess.check_output(args, cwd=root, env=env, text=True).strip()


def committed_input(root, relative, env):
    path = root / relative
    ensure(not path.is_symlink(), "SYMLINK_INPUT: " + relative)
    blob = subprocess.check_output(["git", "show", "HEAD:" + relative], cwd=root, env=env)
    ensure(path.read_bytes() == blob, "INPUT_NOT_EXACT_COMMITTED_BYTES: " + relative)
    return {
        "raw_sha256": digest(path),
        "git_blob_sha1": query(root, ["git", "rev-parse", "HEAD:" + relative], env),
    }


def reject_shadow_inputs(root):
    tracked = set(subprocess.check_output(
        ["git", "ls-files", "-z"], cwd=root
    ).decode().split("\0"))
    for directory, folders, files in os.walk(root):
        folders[:] = [name for name in folders if name not in {".git", ".lake"}]
        for name in files:
            path = Path(directory) / name
            if path.suffix in {".lean", ".olean", ".ilean"}:
                ensure(path.relative_to(root).as_posix() in tracked,
                       "UNTRACKED_LEAN_INPUT: " + path.relative_to(root).as_posix())


def axiom_surface(text):
    ensure("sorryAx" not in text, "SORRY_AXIOM_OBSERVED")
    matches = re.findall(
        r"'" + re.escape(THEOREM) + r"' depends on axioms: \[([^\]]*)\]", text
    )
    ensure(len(matches) == 1, "AXIOM_OUTPUT_MISSING_OR_DUPLICATED")
    values = [item.strip() for item in matches[0].split(",") if item.strip()]
    ensure(len(values) == len(AXIOMS) and set(values) == AXIOMS,
           "UNEXPECTED_AXIOM_SURFACE")
    return sorted(values)


def replay(source, nsrw, output, expected_commit):
    source, nsrw, output = source.resolve(), nsrw.resolve(), output.resolve()
    ensure(not output.exists(), "OUTPUT_ALREADY_EXISTS")
    ensure(not output.is_relative_to(source) and not output.is_relative_to(nsrw),
           "OUTPUT_MUST_BE_OUTSIDE_CHECKOUTS")
    ensure(re.fullmatch(r"[0-9a-f]{40}", expected_commit) is not None,
           "EXPECTED_COMMIT_MUST_BE_FULL_LOWERCASE_SHA1")
    ensure(Path(__file__).resolve() == nsrw / RUNNER, "RUNNER_OUTSIDE_CANONICAL_PATH")
    env = os.environ.copy()
    env.pop("LEAN_PATH", None)
    env.pop("LEAN_SRC_PATH", None)

    def identity():
        result = {}
        for label, root, commit in (("source", source, SOURCE_COMMIT),
                                    ("nsrw", nsrw, expected_commit)):
            actual = query(root, ["git", "rev-parse", "HEAD"], env)
            ensure(actual == commit, label.upper() + "_COMMIT_MISMATCH")
            ensure(not query(root, ["git", "status", "--porcelain", "--untracked-files=no"], env),
                   label.upper() + "_TRACKED_TREE_DIRTY")
            reject_shadow_inputs(root)
            result[label + "_commit"] = actual
            result[label + "_tracked_clean"] = True
        result["inputs"] = {name: committed_input(nsrw, name, env) for name in (PROOF, RUNNER)}
        ensure(result["inputs"][PROOF]["raw_sha256"] == PROOF_SHA256, "PROOF_SHA_MISMATCH")
        ensure(query(source, ["git", "rev-parse", "HEAD:lake-manifest.json"], env) == MANIFEST_BLOB,
               "MANIFEST_BLOB_MISMATCH")
        result["manifest"] = committed_input(source, "lake-manifest.json", env)
        committed_input(source, "lean-toolchain", env)
        ensure((source / "lean-toolchain").read_text().strip() == TOOLCHAIN, "TOOLCHAIN_MISMATCH")
        result["lean_version"] = query(source, ["lean", "--version"], env)
        result["lake_version"] = query(source, ["lake", "--version"], env)
        ensure("version 4.34.0-rc2," in result["lean_version"]
               and LEAN_COMMIT in result["lean_version"], "OBSERVED_LEAN_MISMATCH")
        ensure("Lean version 4.34.0-rc2" in result["lake_version"], "OBSERVED_LAKE_MISMATCH")
        manifest = json.loads((source / "lake-manifest.json").read_text())
        result["dependency_revisions"] = {}
        for package in manifest["packages"]:
            root = source / manifest["packagesDir"] / package["name"]
            revision = query(root, ["git", "rev-parse", "HEAD"], env)
            ensure(revision == package["rev"], "DEPENDENCY_REVISION_MISMATCH: " + package["name"])
            ensure(not query(root, ["git", "status", "--porcelain", "--untracked-files=no"], env),
                   "DEPENDENCY_TRACKED_TREE_DIRTY: " + package["name"])
            reject_shadow_inputs(root)
            result["dependency_revisions"][package["name"]] = revision
        return result

    output.mkdir(parents=True)
    metadata = {
        "scope": "COMMIT_BOUND_EXTERNAL_P2_L3_REPLAY",
        "started_utc": datetime.now(timezone.utc).isoformat(),
        "expected_nsrw_commit": expected_commit, "toolchain": TOOLCHAIN,
        "check_status": "ERROR[REPLAY_NOT_ADMITTED]", "claim_status": "UNVERIFIED",
        "cache_policy": "REUSED_SOURCE_CACHE; FRESH_EXTERNAL_L3; NOT_INDEPENDENTLY_ATTESTED",
        "boundary": "Named L3 proposition only; not DeltaM, coefficient sign, repair zero, or paper equivalence.",
        "stages": {},
        "runtime": {"os": platform.system(), "kernel": platform.release(),
                    "cpu_count": os.cpu_count(), "disk_free_bytes": shutil.disk_usage(source).free,
                    "ram_bytes": os.sysconf("SC_PHYS_PAGES") * os.sysconf("SC_PAGE_SIZE")},
    }

    def save():
        temporary = output / "metadata.json.tmp"
        temporary.write_text(json.dumps(metadata, indent=2) + "\n")
        temporary.replace(output / "metadata.json")

    def stage(name, args):
        print("START " + name, flush=True)
        start = time.monotonic()
        stdout, stderr = output / (name + ".stdout.log"), output / (name + ".stderr.log")
        with stdout.open("wb") as out, stderr.open("wb") as err:
            result = subprocess.run(args, cwd=source, env=env, stdout=out, stderr=err)
        metadata["stages"][name] = {
            "command": args, "exit": result.returncode,
            "elapsed_seconds": time.monotonic() - start,
            "stdout_sha256": digest(stdout), "stderr_sha256": digest(stderr),
            "stdout_bytes": stdout.stat().st_size, "stderr_bytes": stderr.stat().st_size,
        }
        save()
        print(name + "_exit=" + str(result.returncode), flush=True)
        print(stdout.read_text(errors="replace")[-12000:], flush=True)
        print(stderr.read_text(errors="replace")[-8000:], flush=True)
        ensure(result.returncode == 0, "EXECUTION_FAILED: " + name)
        ensure(stderr.stat().st_size == 0, "STDERR_REQUIRES_REVIEW: " + name)
        ensure(identity() == metadata["pre_identity"], "IDENTITY_CHANGED: " + name)

    try:
        metadata["pre_identity"] = identity()
        shutil.copyfile(nsrw / PROOF, output / Path(PROOF).name)
        shutil.copyfile(nsrw / RUNNER, output / Path(RUNNER).name)
        stage("source", ["lake", "build", TARGET])
        target = source / ".lake/build/lib/lean/NavierStokes/OutgoingPulseBounds.olean"
        metadata["target_olean_before_proof_sha256"] = digest(target)
        artifacts = output / "artifacts"
        artifacts.mkdir()
        fresh = artifacts / "P2_L3_TemplateMomentComparison.olean"
        stage("l3", ["lake", "env", "lean", "-R", str(nsrw / "formal/p2"),
                     "-o", str(fresh), str(nsrw / PROOF)])
        metadata["axiom_surface"] = axiom_surface((output / "l3.stdout.log").read_text())
        ensure(fresh.is_file(), "FRESH_L3_ARTIFACT_MISSING")
        metadata["fresh_l3_olean_sha256"] = digest(fresh)
        metadata["target_olean_after_proof_sha256"] = digest(target)
        ensure(metadata["target_olean_before_proof_sha256"]
               == metadata["target_olean_after_proof_sha256"], "TARGET_OLEAN_CHANGED_DURING_PROOF")
        metadata["post_identity"] = identity()
        ensure(metadata["pre_identity"] == metadata["post_identity"], "POST_IDENTITY_CHANGED")
        ensure(digest(output / Path(PROOF).name) == PROOF_SHA256, "ARCHIVED_PROOF_CHANGED")
        ensure(digest(output / Path(RUNNER).name) == metadata["pre_identity"]["inputs"][RUNNER]["raw_sha256"],
               "ARCHIVED_RUNNER_CHANGED")
        metadata["check_status"] = "PASS[COMMIT_BOUND_EXTERNAL_P2_L3_REPLAY]"
    except Exception as error:
        metadata["error"] = str(error)
        raise
    finally:
        metadata["finished_utc"] = datetime.now(timezone.utc).isoformat()
        save()
        print(json.dumps(metadata, indent=2), flush=True)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--source-root", type=Path, required=True)
    parser.add_argument("--nsrw-root", type=Path, required=True)
    parser.add_argument("--output-dir", type=Path, required=True)
    parser.add_argument("--expected-nsrw-commit", required=True)
    args = parser.parse_args()
    replay(args.source_root, args.nsrw_root, args.output_dir, args.expected_nsrw_commit)
