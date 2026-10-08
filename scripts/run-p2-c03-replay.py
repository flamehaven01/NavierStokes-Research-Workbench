#!/usr/bin/env python3
"""Fresh commit-bound C03 replay; no installation or automatic claim admission."""

import argparse
import hashlib
import importlib.util
import json
import os
import re
import shutil
import subprocess
from datetime import datetime, timezone
from pathlib import Path

RUNNER = "scripts/run-p2-c03-replay.py"
ENGINE = "colab/run-c03-development.py"
HELPER = "colab/run-c02-development.py"
PROOF = "formal/p2/P2_C03_ActualCoefficientAtZero.lean"
PROOF_BLOB = "a28d007dd1f84cd8a6e2fc4d03b540eea3ee9ad0"
DEPENDENCIES = (
    ("P2_F1_MainMomentPositivity", "2cc10212d7383a015072e03cbcf7d065117a7be4"),
    ("P2_L2_NormalizedMainMomentComparison", "cd2a549f4648088e4f5aea04228847b7603caf45"),
    ("P2_L3_TemplateMomentComparison", "c359075d585f5b66934ad81ae8b29ecba16c9eae"),
    ("P2_D_DeltaMComposition", "6e2bbf2e33efa8a7e36f5d0d4269b96aed5afd56"),
    ("P2_C_MainOnlyCoefficient", "9a73a3e3483dda1a606fde64f792ed457e0fa446"),
    ("P2_C02_ActualCoefficientDecomposition", "fe4c2d1e18c7fbe9db5b9ce36196a9c22184827c"),
)
MODULE = "P2_C03_ActualCoefficientAtZero"
PINS = {"formal/p2/" + name + ".lean": blob for name, blob in DEPENDENCIES}
PINS.update({PROOF: PROOF_BLOB, HELPER: "518de06530c4c7c56edafdf571e5fb2ef0f808b3"})
INPUTS = (*PINS, ENGINE, RUNNER)
PASS = "PASS[COMMIT_BOUND_EXTERNAL_P2_C03_REPLAY]"


def require(condition, message):
    if not condition:
        raise RuntimeError(message)


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def run_command(args, **kwargs):
    """Bounded test seam; never patch the shared stdlib subprocess module."""
    return subprocess.run(args, **kwargs)


def git(root, args, env):
    return run_command(["git", *args], cwd=root, env=env,
                       capture_output=True, check=True).stdout


def identity(root, expected_commit, env):
    head = git(root, ["rev-parse", "HEAD"], env).decode().strip()
    require(head == expected_commit, "NSRW_COMMIT_MISMATCH")
    require(not git(root, ["status", "--porcelain", "--untracked-files=no"], env).strip(),
            "NSRW_TRACKED_TREE_DIRTY")
    inputs = {}
    for relative in INPUTS:
        path = root / relative
        require(path.is_file() and not path.is_symlink(), "INPUT_UNAVAILABLE: " + relative)
        data = git(root, ["show", "HEAD:" + relative], env)
        require(path.read_bytes() == data, "INPUT_NOT_EXACT_COMMITTED_BYTES: " + relative)
        blob = hashlib.sha1(b"blob " + str(len(data)).encode() + b"\0" + data).hexdigest()
        if relative in PINS:
            require(blob == PINS[relative], "INPUT_BLOB_MISMATCH: " + relative)
        inputs[relative] = {"raw_sha256": digest(path), "git_blob_sha1": blob}
    return {"commit": head, "tracked_clean": True, "inputs": inputs}


def load_module(path, name):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def replay(source, nsrw, output, expected_commit):
    source, nsrw, output = (path.resolve() for path in (source, nsrw, output))
    require(not output.exists(), "OUTPUT_ALREADY_EXISTS")
    require(not Path(str(output) + "-evidence.zip").exists()
            and not Path(str(output) + "-replay-evidence.zip").exists(),
            "EVIDENCE_ARCHIVE_ALREADY_EXISTS")
    require(not output.is_relative_to(source) and not output.is_relative_to(nsrw),
            "OUTPUT_MUST_BE_OUTSIDE_CHECKOUTS")
    require(re.fullmatch(r"[0-9a-f]{40}", expected_commit) is not None,
            "EXPECTED_COMMIT_MUST_BE_FULL_LOWERCASE_SHA1")
    env = os.environ.copy()
    env["PATH"] = "/root/.elan/bin:" + env["PATH"]
    env.pop("LEAN_PATH", None)
    env.pop("LEAN_SRC_PATH", None)
    metadata = {
        "kind": "COMMIT_BOUND_REPLAY", "claim_authority": "NONE", "claim_status": "UNVERIFIED",
        "check_status": "ERROR[REPLAY_NOT_ADMITTED]",
        "started_utc": datetime.now(timezone.utc).isoformat(),
        "expected_nsrw_commit": expected_commit,
        "cache_policy": "REUSED_PINNED_SOURCE_CACHE; FRESH_EXTERNAL_F1_L2_L3_D_C01_C02_C03; SHARED_TRUST_DOMAIN",
        "scope": "Actual second axial coefficient at zero identity, positivity, and continuity only; no C04 epsilon or mass zero",
    }
    try:
        require(Path(__file__).resolve() == nsrw / RUNNER, "RUNNER_OUTSIDE_CANONICAL_PATH")
        metadata["pre_identity"] = identity(nsrw, expected_commit, env)
        engine = load_module(nsrw / ENGINE, "c03_committed_engine")
        helper = load_module(nsrw / HELPER, "c03_identity_helpers")
        helper.reject_shadow_inputs(nsrw, env)
        require(engine.DEPENDENCIES == DEPENDENCIES and engine.MODULE == MODULE,
                "ENGINE_DEPENDENCY_SURFACE_MISMATCH")
        # New execution, not a promotion/relabeling of the earlier development archive.
        code = engine.run(source, nsrw, nsrw / PROOF, output,
                          metadata["pre_identity"]["inputs"][PROOF]["raw_sha256"],
                          expected_dependency_commit=expected_commit)
        report = json.loads((output / "run-metadata.json").read_text(encoding="utf-8"))
        metadata["execution_metadata_sha256"] = digest(output / "run-metadata.json")
        require(code == 0 and report["check_status"] == "PASS[LOCAL_PROOF_COMPILE:P2_C03]",
                "EXECUTION_NOT_ADMITTED")
        names = [name for name, _ in DEPENDENCIES] + [MODULE]
        require(set(report["stages"]) == {"source", *names}, "STAGE_SET_MISMATCH")
        require(set(report["fresh_artifacts"]) == set(names), "ARTIFACT_SET_MISMATCH")
        for stage, info in report["stages"].items():
            require(info["exit"] == 0 and info["stderr_bytes"] == 0,
                    "STAGE_NOT_ADMITTED: " + stage)
            for stream in ("stdout", "stderr"):
                path = output / f"{stage}.{stream}.log"
                require(digest(path) == info[stream + "_sha256"]
                        and path.stat().st_size == info[stream + "_bytes"],
                        "LOG_CHANGED: " + stage + "." + stream)
        helper.THEOREMS = engine.THEOREMS
        require(helper.axiom_surface((output / (MODULE + ".stdout.log")).read_text(encoding="utf-8"))
                == report["axiom_surface"], "AXIOM_SURFACE_CHANGED")
        for name in names:
            artifact = output / "artifacts" / (name + ".olean")
            require(artifact.is_file() and not artifact.is_symlink()
                    and digest(artifact) == report["fresh_artifacts"][name],
                    "FRESH_ARTIFACT_CHANGED: " + name)
            require(digest(output / "inputs" / (name + ".lean"))
                    == metadata["pre_identity"]["inputs"]["formal/p2/" + name + ".lean"]["raw_sha256"],
                    "ARCHIVED_PROOF_CHANGED: " + name)
        for relative in (ENGINE, HELPER):
            require(digest(output / Path(relative).name)
                    == metadata["pre_identity"]["inputs"][relative]["raw_sha256"],
                    "ARCHIVED_RUNNER_CHANGED: " + relative)
        require(helper.source_identity(source, env) == report["post_source_identity"]
                == report["pre_source_identity"], "SOURCE_IDENTITY_CHANGED")
        require(digest(source / helper.TARGET_ARTIFACT) == report["target_olean_after_sha256"]
                == report["target_olean_before_sha256"], "SOURCE_TARGET_ARTIFACT_CHANGED")
        metadata["post_identity"] = identity(nsrw, expected_commit, env)
        require(metadata["pre_identity"] == metadata["post_identity"], "NSRW_IDENTITY_CHANGED")
        helper.reject_shadow_inputs(nsrw, env)
        shutil.copyfile(nsrw / RUNNER, output / Path(RUNNER).name)
        require(digest(output / Path(RUNNER).name)
                == metadata["pre_identity"]["inputs"][RUNNER]["raw_sha256"],
                "ARCHIVED_WRAPPER_CHANGED")
        metadata["check_status"] = PASS
    except Exception as exc:
        metadata["error"] = str(exc)
        metadata["failure_boundary"] = getattr(exc, "boundary", "COMMIT_OR_EXECUTION_REVIEW")
        metadata["mathematical_interpretation"] = "NONE; review original logs"
    finally:
        output.mkdir(parents=True, exist_ok=True)
        metadata["finished_utc"] = datetime.now(timezone.utc).isoformat()
        temporary = output / "replay-metadata.json.tmp"
        temporary.write_text(json.dumps(metadata, indent=2) + "\n", encoding="utf-8")
        temporary.replace(output / "replay-metadata.json")
        # Distinct archive includes the wrapper report; the inner development ZIP is preserved.
        archive = Path(shutil.make_archive(str(output) + "-replay-evidence", "zip", root_dir=output))
        print("ARCHIVE", archive, "BYTES", archive.stat().st_size, "SHA256", digest(archive), flush=True)
    return metadata


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--source-root", type=Path, required=True)
    parser.add_argument("--nsrw-root", type=Path, required=True)
    parser.add_argument("--output-dir", type=Path, required=True)
    parser.add_argument("--expected-nsrw-commit", required=True)
    args = parser.parse_args()
    report = replay(args.source_root, args.nsrw_root, args.output_dir, args.expected_nsrw_commit)
    print(report["check_status"])
    print("claim_authority=NONE")
    raise SystemExit(0 if report["check_status"] == PASS else 1)
