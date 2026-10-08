"""Synthetic commit/replay controls only; not evidence of Lean compilation."""

import importlib.util
import json
import subprocess
from pathlib import Path
from types import SimpleNamespace

import pytest

SPEC = importlib.util.spec_from_file_location(
    "c03_replay", Path(__file__).parents[1] / "scripts/run-p2-c03-replay.py")
runner = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(runner)


def synthetic(root, monkeypatch, failure=None):
    source, nsrw, output = ((root / name).resolve() for name in ("source", "nsrw", "run"))
    source.mkdir()
    nsrw.mkdir()
    binding = {"commit": "a" * 40, "tracked_clean": True, "inputs": {}}
    for relative in runner.INPUTS:
        path = nsrw / relative
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_bytes(relative.encode())
        binding["inputs"][relative] = {"raw_sha256": runner.digest(path), "git_blob_sha1": "b" * 40}
    target = source / "target.olean"
    target.write_bytes(b"source target")
    names = [name for name, _ in runner.DEPENDENCIES] + [runner.MODULE]
    original = subprocess.run

    def execute(s, n, proof, destination, sha, *, expected_dependency_commit):
        assert (s, n, proof) == (source, nsrw, nsrw / runner.PROOF)
        assert expected_dependency_commit == "a" * 40
        assert sha == runner.digest(proof) and subprocess.run is original
        destination.mkdir()
        (destination / "inputs").mkdir()
        (destination / "artifacts").mkdir()
        report = {"check_status": "PASS[LOCAL_PROOF_COMPILE:P2_C03]", "stages": {},
                  "fresh_artifacts": {}, "axiom_surface": {"exact": ["expected"]},
                  "pre_source_identity": {"pin": "same"}, "post_source_identity": {"pin": "same"},
                  "target_olean_before_sha256": runner.digest(target),
                  "target_olean_after_sha256": runner.digest(target)}
        for stage in ["source", *names]:
            out, err = destination / (stage + ".stdout.log"), destination / (stage + ".stderr.log")
            out.write_bytes(b"expected output")
            err.write_bytes(b"warning" if failure == "stderr" and stage == runner.MODULE else b"")
            report["stages"][stage] = {"exit": 1 if failure == stage else 0,
                "stdout_bytes": out.stat().st_size, "stderr_bytes": err.stat().st_size,
                "stdout_sha256": runner.digest(out), "stderr_sha256": runner.digest(err)}
        for name in names:
            artifact = destination / "artifacts" / (name + ".olean")
            artifact.write_bytes(b"fresh")
            report["fresh_artifacts"][name] = runner.digest(artifact)
            (destination / "inputs" / (name + ".lean")).write_bytes(
                (nsrw / ("formal/p2/" + name + ".lean")).read_bytes())
        for relative in (runner.ENGINE, runner.HELPER):
            (destination / Path(relative).name).write_bytes((nsrw / relative).read_bytes())
        (destination / "run-metadata.json").write_text(json.dumps(report), encoding="utf-8")
        if failure == "log":
            (destination / (runner.MODULE + ".stdout.log")).write_bytes(b"changed")
        if failure == "artifact":
            (destination / "artifacts" / (names[0] + ".olean")).write_bytes(b"changed")
        if failure == "input":
            (destination / "inputs" / (names[0] + ".lean")).write_bytes(b"changed")
        if failure == "engine":
            (destination / Path(runner.ENGINE).name).write_bytes(b"changed")
        if failure == "target":
            target.write_bytes(b"changed")
        return 1 if failure == "execution" else 0

    engine = SimpleNamespace(run=execute, DEPENDENCIES=runner.DEPENDENCIES,
                             MODULE=runner.MODULE, THEOREMS=("named",))
    helper = SimpleNamespace(reject_shadow_inputs=lambda *_: None,
        axiom_surface=lambda _: {"exact": ["unexpected" if failure == "axioms" else "expected"]},
        source_identity=lambda *_: {"pin": "changed" if failure == "source_identity" else "same"},
        TARGET_ARTIFACT="target.olean")
    monkeypatch.setattr(runner, "__file__", str(nsrw / runner.RUNNER))
    observed = iter([binding, {**binding, "commit": "c" * 40} if failure == "head" else binding])
    monkeypatch.setattr(runner, "identity", lambda *_: next(observed))
    monkeypatch.setattr(runner, "load_module", lambda path, _: engine if path.name == Path(runner.ENGINE).name else helper)
    report = runner.replay(source, nsrw, output, "a" * 40)
    assert subprocess.run is original
    return report, output


def test_success_does_not_self_promote_and_archives_wrapper_report(tmp_path, monkeypatch):
    report, output = synthetic(tmp_path, monkeypatch)
    assert report["check_status"] == runner.PASS
    assert report["claim_authority"] == "NONE" and report["claim_status"] == "UNVERIFIED"
    assert report["pre_identity"] == report["post_identity"]
    assert json.loads((output / "replay-metadata.json").read_text())["claim_status"] == "UNVERIFIED"
    assert Path(str(output) + "-replay-evidence.zip").is_file()
    assert (output / Path(runner.RUNNER).name).is_file()


@pytest.mark.parametrize("failure", ["source", runner.MODULE, "stderr", "execution", "log",
    "artifact", "input", "engine", "target", "axioms", "source_identity", "head"])
def test_negative_controls_never_admit(tmp_path, monkeypatch, failure):
    report, output = synthetic(tmp_path, monkeypatch, failure)
    assert report["check_status"] == "ERROR[REPLAY_NOT_ADMITTED]"
    assert report["claim_authority"] == "NONE" and report["claim_status"] == "UNVERIFIED"
    assert report["error"]
    assert (output / "replay-metadata.json").is_file()
    assert Path(str(output) + "-replay-evidence.zip").is_file()


def test_existing_run_is_not_overwritten(tmp_path):
    sentinel = tmp_path / "old.log"
    sentinel.write_bytes(b"preserve")
    with pytest.raises(RuntimeError, match="OUTPUT_ALREADY_EXISTS"):
        runner.replay(tmp_path / "source", tmp_path / "nsrw", tmp_path, "a" * 40)
    assert sentinel.read_bytes() == b"preserve"


def test_resolved_alias_inside_checkout_rejected(tmp_path):
    source = tmp_path / "source"
    source.mkdir()
    with pytest.raises(RuntimeError, match="OUTPUT_MUST_BE_OUTSIDE_CHECKOUTS"):
        runner.replay(source, tmp_path / "nsrw", source / ".." / "source" / "run", "a" * 40)


@pytest.mark.parametrize("suffix", ["-evidence.zip", "-replay-evidence.zip"])
def test_existing_archive_is_not_overwritten(tmp_path, suffix):
    output = tmp_path / "run"
    archive = Path(str(output) + suffix)
    archive.write_bytes(b"preserve original evidence")
    with pytest.raises(RuntimeError, match="EVIDENCE_ARCHIVE_ALREADY_EXISTS"):
        runner.replay(tmp_path / "source", tmp_path / "nsrw", output, "a" * 40)
    assert archive.read_bytes() == b"preserve original evidence"
    assert not output.exists()


@pytest.mark.parametrize("failure", ["head", "dirty", "bytes", "pin"])
def test_identity_rejects_wrong_commit_dirty_or_self_consistent_wrong_proof(tmp_path, monkeypatch, failure):
    first = runner.INPUTS[0]
    path = tmp_path / first
    path.parent.mkdir(parents=True)
    path.write_bytes(b"candidate")

    def git(root, args, env):
        if args == ["rev-parse", "HEAD"]:
            return ("c" * 40 if failure == "head" else "a" * 40).encode()
        if args[0] == "status":
            return b" M input" if failure == "dirty" else b""
        if args[0] == "show":
            return b"other" if failure == "bytes" else b"candidate"
        pytest.fail("Unexpected identity command")

    monkeypatch.setattr(runner, "git", git)
    with pytest.raises(RuntimeError, match={"head": "COMMIT_MISMATCH", "dirty": "TRACKED_TREE_DIRTY",
            "bytes": "NOT_EXACT_COMMITTED_BYTES", "pin": "INPUT_BLOB_MISMATCH"}[failure]):
        runner.identity(tmp_path, "a" * 40, {})
