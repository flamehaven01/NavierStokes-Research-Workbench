"""Synthetic runner controls only; these tests do not compile C02 Lean."""

import importlib.util
import json
import subprocess
from pathlib import Path
from types import SimpleNamespace
from unittest.mock import patch

import pytest

RUNNER = Path(__file__).resolve().parents[1] / "colab/run-c02-development.py"
SPEC = importlib.util.spec_from_file_location("c02_development", RUNNER)
runner = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(runner)


def synthetic_run(root, *, fail=None, stderr=b"", mutate=None, axioms=None,
                  invocation_error=None, head_change=False):
    source, nsrw = (root / "source").resolve(), (root / "nsrw").resolve()
    source.mkdir()
    nsrw.mkdir()
    proof = nsrw / runner.PROOF
    proof.parent.mkdir(parents=True)
    proof.write_bytes(b"uncommitted development input\n")
    output = root / "evidence" / "run"
    target = source / runner.TARGET_ARTIFACT
    target.parent.mkdir(parents=True)
    calls = []
    text = "\n".join(
        f"'NSRW.P2.{name}' depends on axioms: [propext, Classical.choice, Quot.sound]"
        for name in runner.THEOREMS
    ).encode()

    def command(args, *, cwd, env, stdout, stderr, check):
        assert cwd == source
        assert "LEAN_PATH" not in env and "LEAN_SRC_PATH" not in env
        assert subprocess.run is original_run
        name = "source" if "build" in args else "c02"
        calls.append(name)
        if name == invocation_error:
            raise FileNotFoundError("missing executable")
        if name == "source":
            assert args == ["lake", "build", "+NavierStokes.OutgoingProfile"]
            target.write_bytes(b"source compiled artifact")
        else:
            assert Path(args[args.index("-R") + 1]) == output.resolve() / "inputs"
            fresh = Path(args[args.index("-o") + 1])
            assert fresh.parent.name == "artifacts" and not fresh.exists()
            assert Path(args[-1]).parent.name == "inputs"
            stdout.write(text if axioms is None else axioms)
            fresh.write_bytes(b"fresh c02 artifact")
            if mutate == "target":
                target.write_bytes(b"changed source target")
            if mutate == "proof":
                proof.write_bytes(b"changed proof during execution")
        if name == fail:
            stderr.write(b"Core.olean.private read error\xff\xfe")
            return SimpleNamespace(returncode=1)
        if name == "c02":
            stderr.write(raw_stderr)
        return SimpleNamespace(returncode=0)

    raw_stderr, original_run = stderr, subprocess.run
    proof_identities = [
        {"head": "initial-head", "head_git_blob": runner.PROOF_BLOB},
        {"head": "other-head" if head_change else "initial-head", "head_git_blob": runner.PROOF_BLOB},
    ]
    with patch.object(runner, "source_identity", return_value={"commit": runner.SOURCE_COMMIT}), \
         patch.object(runner, "proof_identity", side_effect=proof_identities), \
         patch.object(runner, "nsrw_observation", return_value={
             "head": "development-head", "tracked_dirty": True, "untracked_count": 7,
         }), patch.object(runner, "run_command", side_effect=command):
        result = runner.run(source, nsrw, output, runner.digest(proof))
    assert subprocess.run is original_run
    return result, output, calls


def test_success_permits_dirty_repo_with_bound_proof_without_promotion(tmp_path):
    result, output, calls = synthetic_run(tmp_path)
    assert calls == ["source", "c02"]
    assert result["check_status"] == "PASS[LOCAL_PROOF_COMPILE:P2_C02]"
    assert result["claim_status"] == "UNVERIFIED"
    assert result["claim_authority"] == "NONE"
    assert result["nsrw_pre_observation"]["tracked_dirty"]
    assert result["pre_proof_identity"]["head_git_blob"] == runner.PROOF_BLOB
    assert result["target_olean_before_c02_sha256"] == result["target_olean_after_c02_sha256"]
    assert (output / "inputs" / (runner.MODULE + ".lean")).exists()
    assert not list((output / "inputs").glob("*.olean"))
    assert json.loads((output / "run-metadata.json").read_text())["claim_authority"] == "NONE"


def test_unrelated_head_change_is_observation_only_when_proof_binding_is_stable(tmp_path):
    result, _, _ = synthetic_run(tmp_path, head_change=True)
    assert result["check_status"] == "PASS[LOCAL_PROOF_COMPILE:P2_C02]"
    assert result["pre_proof_identity"]["head"] != result["post_proof_identity"]["head"]


@pytest.mark.parametrize("stage", ["source", "c02"])
def test_nonzero_exit_preserves_original_binary_error(tmp_path, stage):
    result, output, calls = synthetic_run(tmp_path, fail=stage)
    assert result["check_status"] == "ERROR[DEVELOPMENT_COMPILE]"
    assert result["failure_boundary"] == stage.upper() + "_EXECUTION"
    assert result["stages"][stage]["exit_code"] == 1
    assert (output / f"{stage}.stderr.log").read_bytes().endswith(b"\xff\xfe")
    assert result["mathematical_interpretation"].startswith("NONE")
    if stage == "source":
        assert calls == ["source"]


def test_zero_exit_with_stderr_requires_review(tmp_path):
    result, output, _ = synthetic_run(tmp_path, stderr=b"warning requiring review\xff")
    assert result["failure_boundary"] == "STDERR_REVIEW"
    assert result["stages"]["c02"]["exit_code"] == 0
    assert (output / "c02.stderr.log").read_bytes() == b"warning requiring review\xff"


@pytest.mark.parametrize("mutation,boundary", [("target", "ARTIFACT_IDENTITY"), ("proof", "INPUT_IDENTITY")])
def test_mutation_never_passes(tmp_path, mutation, boundary):
    result, _, _ = synthetic_run(tmp_path, mutate=mutation)
    assert result["check_status"] == "ERROR[DEVELOPMENT_COMPILE]"
    assert result["failure_boundary"] == boundary


@pytest.mark.parametrize("text", [b"", b"sorryAx", b"unexpected axiom output"])
def test_missing_or_bad_axiom_surface_never_passes(tmp_path, text):
    result, _, _ = synthetic_run(tmp_path, axioms=text)
    assert result["failure_boundary"] == "AXIOM_SURFACE"


def test_existing_directory_is_not_overwritten(tmp_path):
    marker = tmp_path / "preserved.log"
    marker.write_bytes(b"old run")
    with pytest.raises(runner.RunFailure, match="OUTPUT_ALREADY_EXISTS"):
        runner.run(tmp_path / "source", tmp_path / "nsrw", tmp_path, "a" * 64)
    assert marker.read_bytes() == b"old run"
    assert not (tmp_path / "run-metadata.json").exists()


def test_proof_hash_mismatch_persists_failed_metadata(tmp_path):
    nsrw = tmp_path / "nsrw"
    proof = nsrw / runner.PROOF
    proof.parent.mkdir(parents=True)
    proof.write_bytes(b"actual input")
    output = tmp_path / "run"
    result = runner.run(tmp_path / "source", nsrw, output, "a" * 64)
    assert result["failure_boundary"] == "INPUT_IDENTITY"
    assert result["error"] == "PROOF_SHA_MISMATCH"
    assert (output / "run-metadata.json").is_file()


def test_source_pin_mismatch_rejected_before_build(tmp_path):
    (tmp_path / "lake-manifest.json").write_text('{"packages": []}', encoding="utf-8")
    (tmp_path / "lean-toolchain").write_text(runner.TOOLCHAIN, encoding="utf-8")
    with patch.object(runner, "query", return_value="wrong-commit"):
        with pytest.raises(runner.RunFailure, match="SOURCE_COMMIT_MISMATCH"):
            runner.source_identity(tmp_path, {})


def test_dirty_nsrw_observation_is_not_a_gate(tmp_path):
    with patch.object(runner, "query", side_effect=[" M README.md", "draft.lean\nnotes.md", "head"]):
        result = runner.nsrw_observation(tmp_path, {})
    assert result == {"head": "head", "tracked_dirty": True, "untracked_count": 2}


def test_absent_toolchain_rejected_without_lake_call(tmp_path):
    (tmp_path / "lake-manifest.json").write_text('{"packages": []}', encoding="utf-8")
    (tmp_path / "lean-toolchain").write_text(runner.TOOLCHAIN, encoding="utf-8")
    with patch.object(runner, "query", side_effect=[
        runner.SOURCE_COMMIT, runner.MANIFEST_BLOB, "", "", "no installed toolchains",
    ]) as query:
        with pytest.raises(runner.RunFailure, match="PINNED_TOOLCHAIN_NOT_INSTALLED"):
            runner.source_identity(tmp_path, {})
        assert not any(call.args[1][0] == "lake" for call in query.call_args_list)


def test_failed_identity_query_preserves_binary_streams(tmp_path):
    nsrw = tmp_path / "nsrw"
    proof = nsrw / runner.PROOF
    proof.parent.mkdir(parents=True)
    proof.write_bytes(b"input")
    output = tmp_path / "run"
    failed = SimpleNamespace(returncode=2, stdout=b"query output\xff", stderr=b"query error\xfe")
    with patch.object(runner, "run_command", return_value=failed):
        result = runner.run(tmp_path / "source", nsrw, output, runner.digest(proof))
    assert result["failure_boundary"] == "ENVIRONMENT_IDENTITY"
    assert (output / "identity-query.stdout.log").read_bytes() == failed.stdout
    assert (output / "identity-query.stderr.log").read_bytes() == failed.stderr


@pytest.mark.parametrize("head_blob,status,worktree_blob,message", [
    ("wrong-blob", "", runner.PROOF_BLOB, "PROOF_HEAD_BLOB_MISMATCH"),
    (runner.PROOF_BLOB, " M " + runner.PROOF, runner.PROOF_BLOB, "PROOF_TRACKED_DIFF"),
    (runner.PROOF_BLOB, "", "attacker-recomputed-blob", "PROOF_WORKTREE_BLOB_MISMATCH"),
])
def test_proof_portable_identity_cannot_be_replaced_by_caller_sha(
    tmp_path, head_blob, status, worktree_blob, message,
):
    proof = tmp_path / runner.PROOF
    proof.parent.mkdir(parents=True)
    proof.write_bytes(b"caller-selected input")
    with patch.object(runner, "query", side_effect=["head", head_blob, status, worktree_blob]):
        with pytest.raises(runner.RunFailure, match=message):
            runner.proof_identity(tmp_path, {})


@pytest.mark.parametrize("suffix", [".lean", ".olean", ".ilean"])
def test_ignored_untracked_shadow_is_detected(tmp_path, suffix):
    (tmp_path / ".gitignore").write_text("ignored/\n", encoding="utf-8")
    ignored = tmp_path / "ignored"
    ignored.mkdir()
    (ignored / ("shadow" + suffix)).write_bytes(b"untracked ignored input")
    with patch.object(runner, "query", return_value="known.lean\0"):
        with pytest.raises(runner.RunFailure, match="UNTRACKED_LEAN_SHADOW_INPUT"):
            runner.reject_shadow_inputs(tmp_path, {})


def test_tracked_files_and_admitted_cache_do_not_trigger_shadow_failure(tmp_path):
    (tmp_path / "known.lean").write_bytes(b"tracked")
    for name in (".git", ".lake"):
        directory = tmp_path / name
        directory.mkdir()
        (directory / "cache.olean").write_bytes(b"excluded")
    with patch.object(runner, "query", return_value="known.lean\0"):
        runner.reject_shadow_inputs(tmp_path, {})


@pytest.mark.parametrize("stage", ["source", "c02"])
def test_invocation_exception_has_stage_boundary_and_preserved_logs(tmp_path, stage):
    result, output, _ = synthetic_run(tmp_path, invocation_error=stage)
    assert result["check_status"] == "ERROR[DEVELOPMENT_COMPILE]"
    assert result["failure_boundary"] == stage.upper() + "_INVOCATION"
    assert result["stages"][stage]["exit_code"] is None
    assert result["stages"][stage]["exception_type"] == "FileNotFoundError"
    assert result["stages"][stage]["exception"] == "missing executable"
    assert result["stages"][stage]["command"]
    assert (output / f"{stage}.stdout.log").is_file()
    assert (output / f"{stage}.stderr.log").is_file()
