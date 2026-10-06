#!/usr/bin/env python3
"""Commit-bound fresh F1/L2/L3/D replay; no bootstrap or automatic claim promotion."""

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
RUNNER = "scripts/run-p2-d-replay.py"
TARGET = "+NavierStokes.OutgoingPulseBounds"
AXIOMS = {"propext", "Classical.choice", "Quot.sound"}
MODULES = (
    ("f1", "P2_F1_MainMomentPositivity",
     "df9f605fa7ad9fa2842f54ae2d67b6a9b1773849d72c695192ae1bebe2f01206",
     ("mainMoment_one_lower", "mainMoment_one_pos")),
    ("l2", "P2_L2_NormalizedMainMomentComparison",
     "624f1aa042377db7e2bbe50ba70d08a35035cddc51697bd5a69a1ce0bd9bbcdd",
     ("normalizedMainMoment_log_short", "normalizedMainMoment_one_pos",
      "normalizedMainMoment_zero_lt_target_one")),
    ("l3", "P2_L3_TemplateMomentComparison",
     "9ad9b6ea625e2c39f126a8d3a770cb365f48db9f67c734964d972e382b5fa1d4",
     ("rowMoment_one_scaled_le_rowMoment_zero",)),
    ("d", "P2_D_DeltaMComposition",
     "8f5df8d9f5df6ea29b8138cf087a271bb7606131667b5b25adf3179a286d39b2",
     ("normalizedDebt_affineDebt_zero_one_eq_neg_normalizedMainMoment",
      "normalizedAffineMainDifference_eq_neg_deltaM", "deltaM_neg")),
)


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
    return {"raw_sha256": digest(path),
            "git_blob_sha1": query(root, ["git", "rev-parse", "HEAD:" + relative], env)}


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


def axiom_surface(text, names):
    ensure("sorryAx" not in text, "SORRY_AXIOM_OBSERVED")
    result = {}
    for short in names:
        name = "NSRW.P2." + short
        matches = re.findall(
            r"'" + re.escape(name) + r"' depends on axioms: \[([^\]]*)\]", text
        )
        ensure(len(matches) == 1, "AXIOM_OUTPUT_MISSING_OR_DUPLICATED: " + name)
        values = [item.strip() for item in matches[0].split(",") if item.strip()]
        ensure(len(values) == len(AXIOMS) and set(values) == AXIOMS,
               "UNEXPECTED_AXIOM_SURFACE: " + name)
        result[name] = sorted(values)
    return result


def proof_environment(env, artifacts):
    result = env.copy()
    result.pop("LEAN_PATH", None)
    result.pop("LEAN_SRC_PATH", None)
    result["LEAN_PATH"] = str(artifacts)
    return result


def unchanged_artifacts(artifacts, expected):
    for name, sha256 in expected.items():
        path = artifacts / name
        ensure(path.is_file() and not path.is_symlink(), "FRESH_ARTIFACT_MISSING: " + name)
        ensure(digest(path) == sha256, "FRESH_ARTIFACT_CHANGED: " + name)


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
        inputs = ["formal/p2/" + module + ".lean" for _, module, _, _ in MODULES] + [RUNNER]
        result["inputs"] = {name: committed_input(nsrw, name, env) for name in inputs}
        for _, module, expected_sha, _ in MODULES:
            ensure(result["inputs"]["formal/p2/" + module + ".lean"]["raw_sha256"] == expected_sha,
                   "PROOF_SHA_MISMATCH: " + module)
        result["manifest"] = committed_input(source, "lake-manifest.json", env)
        ensure(result["manifest"]["git_blob_sha1"] == MANIFEST_BLOB, "MANIFEST_BLOB_MISMATCH")
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
        "scope": "COMMIT_BOUND_EXTERNAL_P2_D_REPLAY",
        "started_utc": datetime.now(timezone.utc).isoformat(),
        "expected_nsrw_commit": expected_commit, "toolchain": TOOLCHAIN,
        "check_status": "ERROR[REPLAY_NOT_ADMITTED]", "claim_status": "UNVERIFIED",
        "cache_policy": "REUSED_SOURCE_CACHE; FRESH_EXTERNAL_F1_L2_L3_D; NOT_INDEPENDENTLY_ATTESTED",
        "boundary": "NSRW source-linked deltaM_neg and two debt identities only; not coefficient sign, repair zero, or paper equivalence.",
        "stages": {}, "fresh_artifacts": {}, "axiom_surface": {},
        "runtime": {"os": platform.system(), "kernel": platform.release(),
                    "cpu_count": os.cpu_count(), "disk_free_bytes": shutil.disk_usage(source).free,
                    "ram_bytes": os.sysconf("SC_PHYS_PAGES") * os.sysconf("SC_PAGE_SIZE")},
    }

    def save():
        temporary = output / "metadata.json.tmp"
        temporary.write_text(json.dumps(metadata, indent=2) + "\n")
        temporary.replace(output / "metadata.json")

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
        modules, artifacts = output / "modules", output / "artifacts"
        modules.mkdir()
        artifacts.mkdir()
        shutil.copyfile(nsrw / RUNNER, output / Path(RUNNER).name)
        for _, module, expected_sha, _ in MODULES:
            proof = "formal/p2/" + module + ".lean"
            shutil.copyfile(nsrw / proof, modules / (module + ".lean"))
            ensure(digest(modules / (module + ".lean")) == expected_sha, "COPIED_PROOF_CHANGED")
        stage("source", ["lake", "build", TARGET], env)
        target = source / ".lake/build/lib/lean/NavierStokes/OutgoingPulseBounds.olean"
        metadata["target_olean_before_proof_sha256"] = digest(target)
        lean_env = proof_environment(env, artifacts)
        for name, module, expected_sha, names in MODULES:
            unchanged_artifacts(artifacts, metadata["fresh_artifacts"])
            proof, fresh = modules / (module + ".lean"), artifacts / (module + ".olean")
            ensure(digest(proof) == expected_sha, "COPIED_PROOF_CHANGED: " + name)
            ensure(not fresh.exists(), "ARTIFACT_NOT_FRESH: " + name)
            stage(name, ["lake", "env", "lean", "-R", str(modules),
                         "-o", str(fresh), str(proof)], lean_env)
            metadata["axiom_surface"].update(axiom_surface(
                (output / (name + ".stdout.log")).read_text(), names
            ))
            ensure(fresh.is_file() and not fresh.is_symlink(), "FRESH_ARTIFACT_MISSING: " + name)
            metadata["fresh_artifacts"][fresh.name] = digest(fresh)
            unchanged_artifacts(artifacts, metadata["fresh_artifacts"])
            ensure(digest(target) == metadata["target_olean_before_proof_sha256"],
                   "TARGET_OLEAN_CHANGED_DURING_PROOF: " + name)
            save()
        metadata["target_olean_after_proof_sha256"] = digest(target)
        metadata["post_identity"] = identity()
        ensure(metadata["pre_identity"] == metadata["post_identity"], "POST_IDENTITY_CHANGED")
        for _, module, expected_sha, _ in MODULES:
            ensure(digest(modules / (module + ".lean")) == expected_sha, "ARCHIVED_PROOF_CHANGED")
        ensure(digest(output / Path(RUNNER).name)
               == metadata["pre_identity"]["inputs"][RUNNER]["raw_sha256"], "ARCHIVED_RUNNER_CHANGED")
        metadata["check_status"] = "PASS[COMMIT_BOUND_EXTERNAL_P2_D_REPLAY]"
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
