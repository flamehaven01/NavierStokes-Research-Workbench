"""Synthetic replay controls only; no test here is evidence of Lean compilation."""

import importlib.util
import json
import subprocess
from pathlib import Path
from types import SimpleNamespace
from unittest.mock import patch

import pytest

PATH = Path(__file__).resolve().parents[1] / "scripts/run-p2-c02-replay.py"
SPEC = importlib.util.spec_from_file_location("c02_replay", PATH)
runner = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(runner)


def synthetic(root, *, failure=None, mutation=None):
    source, nsrw, output = ((root / name).resolve() for name in ("source", "nsrw", "run"))
    source.mkdir()
    nsrw.mkdir()
    identities = {"commit": "a" * 40, "tracked_clean": True, "inputs": {}}
    for relative in runner.INPUTS:
        path = nsrw / relative
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_bytes((relative + "\n").encode())
        identities["inputs"][relative] = {"raw_sha256": runner.digest(path), "git_blob_sha1": "b" * 40}
    identities["inputs"][runner.PROOF]["git_blob_sha1"] = runner.PROOF_BLOB
    original = subprocess.run

    def execute(source_root, nsrw_root, destination, sha):
        assert source_root == source and nsrw_root == nsrw and not destination.exists()
        assert sha == identities["inputs"][runner.PROOF]["raw_sha256"]
        assert subprocess.run is original
        destination.mkdir()
        (destination / "inputs").mkdir()
        (destination / "artifacts").mkdir()
        for relative in (runner.PROOF, runner.ENGINE):
            (destination / "inputs" / Path(relative).name).write_bytes((nsrw / relative).read_bytes())
        result = {"check_status": "PASS[LOCAL_PROOF_COMPILE:P2_C02]", "stages": {},
                  "axiom_surface": {"named": ["expected"]}}
        for name in ("source", "c02"):
            out, err = destination / f"{name}.stdout.log", destination / f"{name}.stderr.log"
            out.write_bytes(b"captured stdout")
            err.write_bytes(b"warning" if failure == "stderr" and name == "c02" else b"")
            result["stages"][name] = {
                "exit_code": 1 if failure == name else 0, "stderr_bytes": err.stat().st_size,
                "stdout_sha256": runner.digest(out), "stderr_sha256": runner.digest(err),
            }
        fresh = destination / "artifacts" / "C02.olean"
        fresh.write_bytes(b"fresh compiled artifact")
        result["fresh_olean_sha256"] = runner.digest(fresh)
        if failure in {"source", "c02"}:
            result.update(check_status="ERROR[DEVELOPMENT_COMPILE]", failure_boundary=failure.upper())
        (destination / "run-metadata.json").write_text(json.dumps(result), encoding="utf-8")
        if mutation == "log":
            (destination / "c02.stdout.log").write_bytes(b"changed log")
        if mutation == "artifact":
            fresh.write_bytes(b"changed artifact")
        if mutation == "archived":
            (destination / "inputs" / Path(runner.PROOF).name).write_bytes(b"changed input")
        return result

    engine = SimpleNamespace(run=execute, reject_shadow_inputs=lambda *_: None,
                             axiom_surface=lambda _: {"named": ["expected"]}, MODULE="C02")
    after = identities if mutation != "head" else {**identities, "commit": "c" * 40}
    with patch.object(runner, "__file__", str(nsrw / runner.RUNNER)), \
         patch.object(runner, "identity", side_effect=[identities, after]), \
         patch.object(runner, "load_engine", return_value=engine):
        report = runner.replay(source, nsrw, output, "a" * 40)
    assert subprocess.run is original
    return report, output


def test_success_never_self_promotes_and_preserves_inner_classification(tmp_path):
    report, output = synthetic(tmp_path)
    assert report["check_status"] == runner.PASS
    assert report["claim_authority"] == "NONE" and report["claim_status"] == "UNVERIFIED"
    assert report["pre_identity"] == report["post_identity"]
    assert (output / "inputs" / Path(runner.RUNNER).name).is_file()
    assert json.loads((output / "replay-metadata.json").read_text())["claim_status"] == "UNVERIFIED"


@pytest.mark.parametrize("failure", ["source", "c02", "stderr"])
def test_stage_failure_or_stderr_never_admitted(tmp_path, failure):
    report, output = synthetic(tmp_path, failure=failure)
    assert report["check_status"] == "ERROR[REPLAY_NOT_ADMITTED]"
    assert report["claim_status"] == "UNVERIFIED"
    assert (output / "c02.stderr.log").exists()


@pytest.mark.parametrize("mutation,message", [
    ("log", "LOG_CHANGED"), ("artifact", "FRESH_ARTIFACT_CHANGED"),
    ("head", "NSRW_IDENTITY_CHANGED"), ("archived", "ARCHIVED_INPUT_CHANGED"),
])
def test_post_execution_drift_never_admitted(tmp_path, mutation, message):
    report, _ = synthetic(tmp_path, mutation=mutation)
    assert report["check_status"] == "ERROR[REPLAY_NOT_ADMITTED]"
    assert message in report["error"]


def test_existing_evidence_is_never_overwritten(tmp_path):
    (tmp_path / "preserved.log").write_bytes(b"previous run")
    with pytest.raises(RuntimeError, match="OUTPUT_ALREADY_EXISTS"):
        runner.replay(tmp_path / "source", tmp_path / "nsrw", tmp_path, "a" * 40)
    assert (tmp_path / "preserved.log").read_bytes() == b"previous run"
    assert not (tmp_path / "replay-metadata.json").exists()


@pytest.mark.parametrize("commit", ["short", "A" * 40, "g" * 40])
def test_full_lowercase_commit_required(tmp_path, commit):
    with pytest.raises(RuntimeError, match="EXPECTED_COMMIT_MUST_BE_FULL"):
        runner.replay(tmp_path / "source", tmp_path / "nsrw", tmp_path / "run", commit)


@pytest.mark.parametrize("changed", ["commit", "dirty", *runner.INPUTS, "blob"])
def test_preflight_rejects_identity_or_committed_bytes_drift(tmp_path, changed):
    for relative in runner.INPUTS:
        path = tmp_path / relative
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_bytes(b"committed\n")

    def command(args, **kwargs):
        assert kwargs["cwd"].resolve() == tmp_path.resolve()
        if args[1:] == ["rev-parse", "HEAD"]:
            value = ("c" if changed == "commit" else "a") * 40
        elif args[1] == "status":
            value = " M README.md" if changed == "dirty" else ""
        elif args[1] == "show":
            relative = args[2].removeprefix("HEAD:")
            return SimpleNamespace(stdout=b"tampered\n" if changed == relative else b"committed\n")
        else:
            value = "b" * 40 if changed == "blob" else runner.PROOF_BLOB
        return SimpleNamespace(stdout=value.encode())

    with patch.object(runner, "run_command", side_effect=command):
        with pytest.raises(RuntimeError):
            runner.identity(tmp_path.resolve(), "a" * 40, {})


def test_canonical_path_gate_preserves_failure_without_loading_engine(tmp_path):
    with patch.object(runner, "load_engine") as load:
        report = runner.replay(tmp_path / "source", tmp_path / "nsrw", tmp_path / "run", "a" * 40)
    load.assert_not_called()
    assert report["error"] == "RUNNER_OUTSIDE_CANONICAL_PATH"
    assert (tmp_path / "run/replay-metadata.json").is_file()
