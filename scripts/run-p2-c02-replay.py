#!/usr/bin/env python3
"""Clean commit-bound C02 replay; no installation or automatic claim admission."""

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

RUNNER = "scripts/run-p2-c02-replay.py"
ENGINE = "colab/run-c02-development.py"
PROOF = "formal/p2/P2_C02_ActualCoefficientDecomposition.lean"
PROOF_BLOB = "fe4c2d1e18c7fbe9db5b9ce36196a9c22184827c"
INPUTS = (PROOF, ENGINE, RUNNER)
PASS = "PASS[COMMIT_BOUND_EXTERNAL_P2_C02_REPLAY]"


def require(condition, message):
    if not condition:
        raise RuntimeError(message)


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def run_command(args, **kwargs):
    """Tests mock this boundary, never the shared stdlib subprocess module."""
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
        blob = git(root, ["show", "HEAD:" + relative], env)
        require(path.read_bytes() == blob, "INPUT_NOT_EXACT_COMMITTED_BYTES: " + relative)
        inputs[relative] = {
            "raw_sha256": digest(path),
            "git_blob_sha1": git(root, ["rev-parse", "HEAD:" + relative], env).decode().strip(),
        }
    require(inputs[PROOF]["git_blob_sha1"] == PROOF_BLOB, "PROOF_BLOB_MISMATCH")
    return {"commit": head, "tracked_clean": True, "inputs": inputs}


def load_engine(path):
    spec = importlib.util.spec_from_file_location("c02_committed_engine", path)
    engine = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(engine)
    return engine


def replay(source, nsrw, output, expected_commit):
    source, nsrw, output = source.resolve(), nsrw.resolve(), output.resolve()
    require(not output.exists(), "OUTPUT_ALREADY_EXISTS")
    require(not output.is_relative_to(source) and not output.is_relative_to(nsrw),
            "OUTPUT_MUST_BE_OUTSIDE_CHECKOUTS")
    require(re.fullmatch(r"[0-9a-f]{40}", expected_commit) is not None,
            "EXPECTED_COMMIT_MUST_BE_FULL_LOWERCASE_SHA1")
    env = os.environ.copy()
    env.pop("LEAN_PATH", None)
    env.pop("LEAN_SRC_PATH", None)
    metadata = {
        "kind": "COMMIT_BOUND_REPLAY", "claim_authority": "NONE", "claim_status": "UNVERIFIED",
        "check_status": "ERROR[REPLAY_NOT_ADMITTED]",
        "started_utc": datetime.now(timezone.utc).isoformat(),
        "expected_nsrw_commit": expected_commit,
        "cache_policy": "REUSED_PINNED_SOURCE_CACHE; FRESH_EXTERNAL_C02; SHARED_TRUST_DOMAIN",
        "scope": "Two C02 decomposition equalities only; not coefficient positivity or mass zeros",
    }
    try:
        require(Path(__file__).resolve() == nsrw / RUNNER, "RUNNER_OUTSIDE_CANONICAL_PATH")
        metadata["pre_identity"] = identity(nsrw, expected_commit, env)
        engine = load_engine(nsrw / ENGINE)
        engine.reject_shadow_inputs(nsrw, env)
        # Execute anew. The inner report remains DEVELOPMENT_COMPILE; it is not relabeled.
        result = engine.run(source, nsrw, output,
                            metadata["pre_identity"]["inputs"][PROOF]["raw_sha256"])
        metadata["execution_check_status"] = result["check_status"]
        metadata["execution_metadata_sha256"] = digest(output / "run-metadata.json")
        require(result["check_status"] == "PASS[LOCAL_PROOF_COMPILE:P2_C02]",
                "EXECUTION_NOT_ADMITTED: " + result.get("failure_boundary", "UNKNOWN"))
        for stage in ("source", "c02"):
            info = result["stages"][stage]
            require(info["exit_code"] == 0 and info["stderr_bytes"] == 0,
                    "STAGE_NOT_ADMITTED: " + stage)
            for stream in ("stdout", "stderr"):
                require(digest(output / f"{stage}.{stream}.log") == info[stream + "_sha256"],
                        "LOG_CHANGED: " + stage + "." + stream)
        require(engine.axiom_surface((output / "c02.stdout.log").read_text(encoding="utf-8"))
                == result["axiom_surface"], "AXIOM_SURFACE_CHANGED")
        require(digest(output / "artifacts" / (engine.MODULE + ".olean"))
                == result["fresh_olean_sha256"], "FRESH_ARTIFACT_CHANGED")
        metadata["post_identity"] = identity(nsrw, expected_commit, env)
        require(metadata["pre_identity"] == metadata["post_identity"], "NSRW_IDENTITY_CHANGED")
        engine.reject_shadow_inputs(nsrw, env)
        for relative, archived in ((PROOF, Path(PROOF).name), (ENGINE, Path(ENGINE).name)):
            require(digest(output / "inputs" / archived)
                    == metadata["pre_identity"]["inputs"][relative]["raw_sha256"],
                    "ARCHIVED_INPUT_CHANGED: " + relative)
        shutil.copyfile(nsrw / RUNNER, output / "inputs" / Path(RUNNER).name)
        require(digest(output / "inputs" / Path(RUNNER).name)
                == metadata["pre_identity"]["inputs"][RUNNER]["raw_sha256"],
                "ARCHIVED_WRAPPER_CHANGED")
        metadata["check_status"] = PASS
    except Exception as exc:
        metadata["error"] = str(exc)
        metadata["failure_boundary"] = getattr(exc, "boundary", "COMMIT_OR_EXECUTION_REVIEW")
        metadata["mathematical_interpretation"] = "NONE; preserve and review original execution logs"
    finally:
        output.mkdir(parents=True, exist_ok=True)
        metadata["finished_utc"] = datetime.now(timezone.utc).isoformat()
        temporary = output / "replay-metadata.json.tmp"
        temporary.write_text(json.dumps(metadata, indent=2) + "\n", encoding="utf-8")
        temporary.replace(output / "replay-metadata.json")
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
