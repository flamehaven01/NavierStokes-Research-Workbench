#!/usr/bin/env python3
"""One clean Z-core/Z+J replay; no installation or automatic claim admission."""

import argparse
import hashlib
import importlib.util
import json
import os
import re
import shutil
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path

RUNNER = "scripts/run-p2-z-replay.py"
ENGINE = "colab/run-zplus-j-composition-development.py"
HELPER = "colab/run-c02-development.py"
BASE = "10d5a1f517b8665137f2354746d70752f8ef67fd"
COMMITTED = {
    "P2_F1_MainMomentPositivity": "2cc10212d7383a015072e03cbcf7d065117a7be4",
    "P2_L2_NormalizedMainMomentComparison": "cd2a549f4648088e4f5aea04228847b7603caf45",
    "P2_L3_TemplateMomentComparison": "c359075d585f5b66934ad81ae8b29ecba16c9eae",
    "P2_D_DeltaMComposition": "6e2bbf2e33efa8a7e36f5d0d4269b96aed5afd56",
    "P2_C_MainOnlyCoefficient": "9a73a3e3483dda1a606fde64f792ed457e0fa446",
    "P2_C02_ActualCoefficientDecomposition": "fe4c2d1e18c7fbe9db5b9ce36196a9c22184827c",
    "P2_C03_ActualCoefficientAtZero": "a28d007dd1f84cd8a6e2fc4d03b540eea3ee9ad0",
    "P2_C04_SmallPositiveEta": "63a1f00db5a38bdb0c9c93e15d2b3f9bc71f2b02",
}
Z_BLOBS = {
    "P2_Z01_LocalMassIdentities": "9d6a9a2196b8383fc17b38585e39a80188e3bfcd",
    "P2_Z02_BoundaryMassSigns": "a4681a313cbebcbacbf49962484725cbafe896a2",
    "P2_Z03_ConditionalInteriorZero": "3759d1eb22a00bb9651536fdfb4f83611b1d1812",
    "P2_Z04_FirstRepairInteriorZero": "054eb77f015dd425b574b19b945d9f7e2aa9192f",
    "P2_ZPLUS_J_FirstRepairAngularMoment": "11ccd687f7157c7a1bb5529843344ce04373d7af",
    "P2_ZPLUS_J_SourceComposition": "759b0ad12ed646d56388bf9c1bd92485d702bf07",
}
DEVELOPMENT = {
    "P2_Z01_LocalMassIdentities": "ff7101067a98fbaa8974c1aa409b83740cd17eb4f1778f20cdc23b44e2a5c267",
    "P2_Z02_BoundaryMassSigns": "7b5764911790054cbba982acfde8ed673705a2d68e85bcd341507d7e0b5f8c2c",
    "P2_Z03_ConditionalInteriorZero": "5e174ab2281ad0b20b8bc684977bcd0bfa5ecc4f79351ac60cb56ed99d043d40",
    "P2_Z04_FirstRepairInteriorZero": "f3bce7c0a6d28922bd592d6dbfb5b0735a058ffc84c2100bc4328be1df5b2d5d",
    "P2_ZPLUS_J_FirstRepairAngularMoment": "2af3c68a73530a97421b3bd971bae5e63bbfb60c1abb7f40361d6d347e875d4a",
}
MODULE = "P2_ZPLUS_J_SourceComposition"
PROOF = "formal/p2/" + MODULE + ".lean"
THEOREMS = ("localAngularMoment_eq_profileJ", "profileJ_pos_of_firstRepair_mass_zero",
            "profileMJ_firstRepair_zero_small_positive")
SURFACES = {
    "P2_Z04_FirstRepairInteriorZero": (
        "localSecondRepairCoefficient_eq_actual", "exists_firstRepair_zero_small_positive",
        "localMass_eq_profileM", "profileM_firstRepair_zero_small_positive"),
    "P2_ZPLUS_J_FirstRepairAngularMoment": (
        "localAngularMoment_partial_identity", "localAngularMoment_tail_identity",
        "first_upper_lt_second_lower", "secondExponent_eq_first_sub_lam",
        "future_radialPulse_eq_two_bumps", "weighted_future_integral_eq_two_tails",
        "secondBump_massTail_pos", "firstRepair_mass_zero_tail_balance",
        "firstBumpTail_pos_and_firstCoeff_neg", "firstBump_angularTail_lower",
        "secondBump_angularTail_upper", "angularMoment_pos_of_firstRepair_mass_zero"),
    MODULE: THEOREMS,
}
PINS = {"formal/p2/" + name + ".lean": pin for name, pin in {**COMMITTED, **Z_BLOBS}.items()}
PINS[HELPER] = "518de06530c4c7c56edafdf571e5fb2ef0f808b3"
INPUTS = (*PINS, ENGINE, RUNNER)
PASS = "PASS[COMMIT_BOUND_EXTERNAL_P2_Z_REPLAY]"


def require(condition, message):
    if not condition:
        raise RuntimeError(message)


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def run_command(args, **kwargs):
    return subprocess.run(args, **kwargs)


def git(root, args, env):
    return run_command(["git", *args], cwd=root, env=env,
                       capture_output=True, check=True).stdout


def identity(root, expected_commit, env):
    require(git(root, ["rev-parse", "HEAD"], env).decode().strip() == expected_commit,
            "NSRW_COMMIT_MISMATCH")
    require(not git(root, ["status", "--porcelain", "--untracked-files=no"], env).strip(),
            "NSRW_TRACKED_TREE_DIRTY")
    inputs = {}
    for relative in INPUTS:
        path = root / relative
        require(path.is_file() and not path.is_symlink(), "INPUT_UNAVAILABLE: " + relative)
        data = git(root, ["show", "HEAD:" + relative], env)
        require(path.read_bytes() == data, "INPUT_NOT_EXACT_COMMITTED_BYTES: " + relative)
        blob = hashlib.sha1(b"blob " + str(len(data)).encode() + b"\0" + data).hexdigest()
        require(relative not in PINS or blob == PINS[relative], "INPUT_BLOB_MISMATCH: " + relative)
        inputs[relative] = {"raw_sha256": digest(path), "git_blob_sha1": blob}
    return {"commit": expected_commit, "tracked_clean": True, "inputs": inputs}


def base_identity(root, env):
    require(git(root, ["rev-parse", "HEAD"], env).decode().strip() == BASE,
            "DEPENDENCY_BASE_MISMATCH")
    require(not git(root, ["status", "--porcelain", "--untracked-files=no"], env).strip(),
            "DEPENDENCY_BASE_DIRTY")
    return {"commit": BASE, "tracked_clean": True}


def load_module(path, name):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    previous = sys.dont_write_bytecode
    try:
        sys.dont_write_bytecode = True
        spec.loader.exec_module(module)
    finally:
        sys.dont_write_bytecode = previous
    return module


def inspect_axioms(text, names):
    require("sorryAx" not in text, "SORRY_AXIOM_OBSERVED")
    result = {}
    for short in names:
        name = "NSRW.P2." + short
        matches = re.findall(r"'" + re.escape(name) + r"' depends on axioms: \[([^\]]*)\]", text)
        require(len(matches) == 1, "AXIOM_OUTPUT_MISSING_OR_DUPLICATED: " + name)
        values = [s.strip() for s in matches[0].split(",") if s.strip()]
        require(len(values) == 3 and set(values) == {"propext", "Classical.choice", "Quot.sound"},
                "AXIOM_SURFACE_UNEXPECTED: " + name)
        result[name] = sorted(values)
    return result


def replay(source, nsrw, base, output, expected_commit):
    source, nsrw, base, output = (p.resolve() for p in (source, nsrw, base, output))
    require(not output.exists(), "OUTPUT_ALREADY_EXISTS")
    require(all(not Path(str(output) + s).exists()
                for s in ("-evidence.zip", "-replay-evidence.zip")), "ARCHIVE_ALREADY_EXISTS")
    require(all(not output.is_relative_to(p) for p in (source, nsrw, base)),
            "OUTPUT_MUST_BE_OUTSIDE_CHECKOUTS")
    require(re.fullmatch(r"[0-9a-f]{40}", expected_commit) is not None, "EXPECTED_COMMIT_FORMAT")
    env = os.environ.copy()
    env["PATH"] = "/root/.elan/bin:" + env.get("PATH", "")
    env.pop("LEAN_PATH", None)
    env.pop("LEAN_SRC_PATH", None)
    meta = {
        "kind": "COMMIT_BOUND_Z_REPLAY", "claim_authority": "NONE", "claim_status": "UNVERIFIED",
        "check_status": "ERROR[REPLAY_NOT_ADMITTED]", "expected_nsrw_commit": expected_commit,
        "started_utc": datetime.now(timezone.utc).isoformat(),
        "cache_policy": "REUSED_PINNED_SOURCE_CACHE; FRESH_14_EXTERNAL_MODULES; SHARED_TRUST_DOMAIN",
        "scope": "Z-core and conditional/source-facing Z+J; separate receipt review required; no Q pole, uniqueness or numerical/uniform epsilon",
    }
    try:
        require(Path(__file__).resolve() == nsrw / RUNNER, "RUNNER_OUTSIDE_CANONICAL_PATH")
        meta["pre_identity"] = identity(nsrw, expected_commit, env)
        meta["pre_base_identity"] = base_identity(base, env)
        engine = load_module(nsrw / ENGINE, "z_committed_engine")
        helper = load_module(nsrw / HELPER, "z_identity_helpers")
        for root in (nsrw, base):
            helper.reject_shadow_inputs(root, env)
        require(engine.COMMITTED == COMMITTED and engine.DEVELOPMENT == DEVELOPMENT
                and engine.BASE == BASE and engine.HELPER_BLOB == PINS[HELPER]
                and engine.MODULE == MODULE and engine.THEOREMS == THEOREMS,
                "ENGINE_SURFACE_MISMATCH")
        report = engine.run(source, base, nsrw / "formal/p2", nsrw / PROOF, output,
                            meta["pre_identity"]["inputs"][PROOF]["raw_sha256"])
        require(report == json.loads((output / "run-metadata.json").read_text(encoding="utf-8")),
                "EXECUTION_METADATA_CHANGED")
        meta["execution_metadata_sha256"] = digest(output / "run-metadata.json")
        require(report["check_status"] == "PASS[LOCAL_PROOF_COMPILE:P2_ZPLUS_J_COMPOSITION]",
                "EXECUTION_NOT_ADMITTED")
        require(report["claim_authority"] == "NONE" and report["claim_status"] == "UNVERIFIED",
                "EXECUTION_SELF_PROMOTION")
        names = [*COMMITTED, *Z_BLOBS]
        require(set(report["stages"]) == {"source", *names}, "STAGE_SET_MISMATCH")
        require(set(report["fresh_artifacts"]) == {n + ".olean" for n in names}, "ARTIFACT_SET_MISMATCH")
        expected_inputs = {Path(p).name: v["raw_sha256"]
                           for p, v in meta["pre_identity"]["inputs"].items() if p != RUNNER}
        require(report["inputs"] == expected_inputs, "ARCHIVED_INPUT_SET_MISMATCH")
        require({p.name for p in (output / "inputs").iterdir()} == set(expected_inputs), "INPUT_SET_CHANGED")
        require({p.name for p in (output / "artifacts").iterdir()}
                == set(report["fresh_artifacts"]), "ARTIFACT_SET_CHANGED")
        for name, pin in expected_inputs.items():
            path = output / "inputs" / name
            require(path.is_file() and not path.is_symlink() and digest(path) == pin,
                    "ARCHIVED_INPUT_CHANGED: " + name)
        for name, pin in report["fresh_artifacts"].items():
            path = output / "artifacts" / name
            require(path.is_file() and not path.is_symlink() and digest(path) == pin,
                    "FRESH_ARTIFACT_CHANGED: " + name)
        for name, info in report["stages"].items():
            require(info["exit"] == 0 and info["stderr_bytes"] == 0, "STAGE_NOT_ADMITTED: " + name)
            for stream in ("stdout", "stderr"):
                path = output / (name + "." + stream + ".log")
                require(path.is_file() and not path.is_symlink()
                        and digest(path) == info[stream + "_sha256"]
                        and path.stat().st_size == info[stream + "_bytes"], "LOG_CHANGED: " + name)
            require(b"sorryAx" not in (output / (name + ".stdout.log")).read_bytes(), "SORRY_AXIOM_OBSERVED")
        meta["axiom_surfaces"] = {}
        for module, surface in SURFACES.items():
            meta["axiom_surfaces"].update(inspect_axioms(
                (output / (module + ".stdout.log")).read_text(encoding="utf-8"), surface))
        require(report["axiom_surfaces"] == inspect_axioms(
            (output / (MODULE + ".stdout.log")).read_text(encoding="utf-8"), THEOREMS),
            "AXIOM_METADATA_CHANGED")
        require(helper.source_identity(source, env) == report["pre_source_identity"]
                == report["post_source_identity"], "SOURCE_IDENTITY_CHANGED")
        require(digest(source / helper.TARGET_ARTIFACT) == report["target_olean_before_sha256"]
                == report["target_olean_after_sha256"], "SOURCE_TARGET_CHANGED")
        meta["post_identity"] = identity(nsrw, expected_commit, env)
        meta["post_base_identity"] = base_identity(base, env)
        require(meta["pre_identity"] == meta["post_identity"], "NSRW_IDENTITY_CHANGED")
        require(meta["pre_base_identity"] == meta["post_base_identity"], "BASE_IDENTITY_CHANGED")
        for root in (nsrw, base):
            helper.reject_shadow_inputs(root, env)
        shutil.copyfile(nsrw / RUNNER, output / Path(RUNNER).name)
        require(digest(output / Path(RUNNER).name)
                == meta["pre_identity"]["inputs"][RUNNER]["raw_sha256"], "ARCHIVED_WRAPPER_CHANGED")
        meta["check_status"] = PASS
    except Exception as exc:
        meta["error"] = str(exc)
        meta["failure_boundary"] = getattr(exc, "boundary", "COMMIT_OR_EXECUTION_REVIEW")
        meta["mathematical_interpretation"] = "NONE; inspect preserved raw logs"
    finally:
        output.mkdir(parents=True, exist_ok=True)
        meta["finished_utc"] = datetime.now(timezone.utc).isoformat()
        (output / "replay-metadata.json").write_text(json.dumps(meta, indent=2) + "\n", encoding="utf-8")
        archive = Path(shutil.make_archive(str(output) + "-replay-evidence", "zip", root_dir=output))
        print("ARCHIVE", archive, "BYTES", archive.stat().st_size, "SHA256", digest(archive), flush=True)
    return meta


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    for argument in ("source-root", "nsrw-root", "dependency-base", "output-dir"):
        parser.add_argument("--" + argument, type=Path, required=True)
    parser.add_argument("--expected-nsrw-commit", required=True)
    args = parser.parse_args()
    result = replay(args.source_root, args.nsrw_root, args.dependency_base,
                    args.output_dir, args.expected_nsrw_commit)
    print(result["check_status"], "claim_authority=NONE", "claim_status=UNVERIFIED")
    raise SystemExit(0 if result["check_status"] == PASS else 1)
