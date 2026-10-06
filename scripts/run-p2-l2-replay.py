#!/usr/bin/env python3
"""Bounded clean-checkout replay of F1 and strict L2; no dependency bootstrap."""

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
MODULES = ("P2_F1_MainMomentPositivity", "P2_L2_NormalizedMainMomentComparison")
AXIOMS = {"propext", "Classical.choice", "Quot.sound"}


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def query(root, args, env):
    return subprocess.check_output(args, cwd=root, env=env, text=True).strip()


def ensure(condition, message):
    if not condition:
        raise RuntimeError(message)


def reject_shadow_inputs(root):
    """Reject non-tracked Lean inputs outside the explicitly admitted Lake cache."""
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


def axiom_surface(text, names):
    for name in names:
        match = re.search(r"'" + re.escape(name) + r"' depends on axioms: \[([^\]]*)\]", text)
        ensure(match is not None, "AXIOM_OUTPUT_MISSING: " + name)
        ensure({item.strip() for item in match[1].split(",")} == AXIOMS,
               "UNEXPECTED_AXIOM_SURFACE: " + name)
    ensure("sorryAx" not in text, "SORRY_AXIOM_OBSERVED")


def replay(source, nsrw, output, expected_commit):
    source, nsrw, output = source.resolve(), nsrw.resolve(), output.resolve()
    ensure(not output.exists(), "OUTPUT_ALREADY_EXISTS")
    ensure(not output.is_relative_to(source) and not output.is_relative_to(nsrw),
           "OUTPUT_MUST_BE_OUTSIDE_CHECKOUTS")
    env = os.environ.copy()
    env.pop("LEAN_PATH", None)
    env.pop("LEAN_SRC_PATH", None)
    runner = Path(__file__).resolve()
    proof_paths = [nsrw / "formal/p2" / (name + ".lean") for name in MODULES]
    inputs = proof_paths + [runner]
    ensure(runner.is_relative_to(nsrw), "RUNNER_OUTSIDE_NSRW")
    initial_hashes = {path.relative_to(nsrw).as_posix(): digest(path) for path in inputs}
    manifest_raw = digest(source / "lake-manifest.json")

    def identity():
        for root, commit in ((source, SOURCE_COMMIT), (nsrw, expected_commit)):
            ensure(query(root, ["git", "rev-parse", "HEAD"], env) == commit,
                   "COMMIT_MISMATCH")
            ensure(not query(root, ["git", "status", "--porcelain", "--untracked-files=no"], env),
                   "TRACKED_TREE_DIRTY")
            reject_shadow_inputs(root)
        ensure(query(source, ["git", "hash-object", "lake-manifest.json"], env) == MANIFEST_BLOB,
               "MANIFEST_BLOB_MISMATCH")
        ensure(digest(source / "lake-manifest.json") == manifest_raw, "MANIFEST_BYTES_CHANGED")
        ensure((source / "lean-toolchain").read_text().strip() == TOOLCHAIN, "TOOLCHAIN_MISMATCH")
        for path in inputs:
            relative = path.relative_to(nsrw).as_posix()
            query(nsrw, ["git", "ls-files", "--error-unmatch", "--", relative], env)
            ensure(digest(path) == initial_hashes[relative], "INPUT_BYTES_CHANGED")
        manifest = json.loads(query(source, ["git", "show", "HEAD:lake-manifest.json"], env))
        packages = {}
        for package in manifest["packages"]:
            root = source / manifest["packagesDir"] / package["name"]
            revision = query(root, ["git", "rev-parse", "HEAD"], env)
            ensure(revision == package["rev"], "DEPENDENCY_REVISION_MISMATCH")
            ensure(not query(root, ["git", "status", "--porcelain", "--untracked-files=no"], env),
                   "DEPENDENCY_TRACKED_TREE_DIRTY")
            reject_shadow_inputs(root)
            packages[package["name"]] = revision
        return packages

    packages = identity()
    lean_version = query(source, ["lean", "--version"], env)
    ensure("version 4.34.0-rc2," in lean_version, "OBSERVED_LEAN_VERSION_MISMATCH")
    output.mkdir(parents=True)
    deps = output / "deps"
    deps.mkdir()
    metadata = {
        "scope": "COMMIT_BOUND_EXTERNAL_F1_STRICT_L2_REPLAY",
        "started_utc": datetime.now(timezone.utc).isoformat(),
        "source_commit": SOURCE_COMMIT, "nsrw_commit": expected_commit,
        "manifest_blob_sha1": MANIFEST_BLOB, "manifest_raw_sha256": manifest_raw,
        "toolchain": TOOLCHAIN, "lean_version": lean_version,
        "lake_version": query(source, ["lake", "--version"], env),
        "input_raw_sha256": initial_hashes,
        "input_git_blobs": {p.relative_to(nsrw).as_posix(): query(nsrw,
            ["git", "rev-parse", "HEAD:" + p.relative_to(nsrw).as_posix()], env) for p in inputs},
        "dependency_revisions": packages, "pre_identity": "OBSERVED_PASS",
        "source_cache": "REUSED; external F1 artifact is fresh", "stages": {},
        "runtime": {"os": platform.system(), "kernel": platform.release(),
                    "cpu_count": os.cpu_count(),
                    "ram_bytes": os.sysconf("SC_PHYS_PAGES") * os.sysconf("SC_PAGE_SIZE"),
                    "disk_free_bytes": shutil.disk_usage(source).free},
        "boundary": "Named Lean propositions only; not paper equivalence, DeltaM, or repair zero.",
    }

    def save():
        (output / "metadata.json").write_text(json.dumps(metadata, indent=2) + "\n")

    def stage(name, args, stage_env):
        print("START " + name, flush=True)
        start = time.monotonic()
        stdout, stderr = output / (name + ".stdout.log"), output / (name + ".stderr.log")
        with stdout.open("wb") as out, stderr.open("wb") as err:
            result = subprocess.run(args, cwd=source, env=stage_env, stdout=out, stderr=err)
        metadata["stages"][name] = {
            "command": args, "exit": result.returncode,
            "elapsed_seconds": time.monotonic() - start,
            "stdout_sha256": digest(stdout), "stderr_sha256": digest(stderr),
        }
        save()
        print(name + "_exit=" + str(result.returncode), flush=True)
        print(stdout.read_text(errors="replace")[-16000:], flush=True)
        print(stderr.read_text(errors="replace")[-8000:], flush=True)
        ensure(result.returncode == 0, "EXECUTION_FAILED: " + name)
        identity()

    try:
        stage("source", ["lake", "build", "+NavierStokes.PulseAmplitude"], env)
        metadata["source_target_olean_sha256"] = digest(
            source / ".lake/build/lib/lean/NavierStokes/PulseAmplitude.olean")
        f1_artifact = deps / (MODULES[0] + ".olean")
        module_root = nsrw / "formal/p2"
        stage("f1", ["lake", "env", "lean", "-R", str(module_root), "-o",
                     str(f1_artifact), str(proof_paths[0])], env)
        ensure(f1_artifact.is_file(), "FRESH_F1_ARTIFACT_MISSING")
        metadata["fresh_f1_olean_sha256"] = digest(f1_artifact)
        l2_env = env.copy()
        l2_env["LEAN_PATH"] = str(deps)
        stage("l2", ["lake", "env", "lean", "-R", str(module_root), str(proof_paths[1])], l2_env)
        axiom_surface((output / "f1.stdout.log").read_text(),
                      ["NSRW.P2.mainMoment_one_lower", "NSRW.P2.mainMoment_one_pos"])
        axiom_surface((output / "l2.stdout.log").read_text(),
                      ["NSRW.P2.normalizedMainMoment_log_short",
                       "NSRW.P2.normalizedMainMoment_one_pos",
                       "NSRW.P2.normalizedMainMoment_zero_lt_target_one"])
        for name in ("source", "f1", "l2"):
            ensure((output / (name + ".stderr.log")).stat().st_size == 0,
                   "STDERR_REQUIRES_REVIEW: " + name)
        ensure(digest(f1_artifact) == metadata["fresh_f1_olean_sha256"], "F1_ARTIFACT_CHANGED")
        identity()
        metadata["post_identity"] = "OBSERVED_PASS"
        metadata["check_status"] = "PASS[COMMIT_BOUND_EXTERNAL_F1_STRICT_L2_REPLAY]"
    except Exception as error:
        metadata["check_status"] = "ERROR[REPLAY_NOT_ADMITTED]"
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
