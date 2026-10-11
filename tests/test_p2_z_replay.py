"""Synthetic replay negative controls; passing these tests is not Lean evidence."""

import hashlib
import importlib.util
import json
import subprocess
from pathlib import Path
from types import SimpleNamespace

import pytest

SPEC = importlib.util.spec_from_file_location(
    "z_replay", Path(__file__).parents[1] / "scripts/run-p2-z-replay.py")
runner = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(runner)


def synthetic(root, monkeypatch, failure=None):
    source, nsrw, base, output = ((root / n).resolve() for n in ("source", "nsrw", "base", "run"))
    for path in (source, nsrw, base):
        path.mkdir()
    binding = {"commit": "a" * 40, "tracked_clean": True, "inputs": {}}
    for relative in runner.INPUTS:
        path = nsrw / relative
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_bytes(relative.encode())
        binding["inputs"][relative] = {"raw_sha256": runner.digest(path), "git_blob_sha1": "b" * 40}
    target = source / "target.olean"
    target.write_bytes(b"pinned source target")
    names = [*runner.COMMITTED, *runner.Z_BLOBS]
    original_run = subprocess.run

    def execute(s, b, dependencies, proof, destination, sha):
        assert (s, b, dependencies, proof) == (source, base, nsrw / "formal/p2", nsrw / runner.PROOF)
        assert sha == runner.digest(proof) and subprocess.run is original_run
        destination.mkdir()
        (destination / "inputs").mkdir()
        (destination / "artifacts").mkdir()
        report = {"check_status": "PASS[LOCAL_PROOF_COMPILE:P2_ZPLUS_J_COMPOSITION]",
                  "claim_authority": "NONE", "claim_status": "UNVERIFIED",
                  "stages": {}, "inputs": {}, "fresh_artifacts": {},
                  "pre_source_identity": {"pin": "same"}, "post_source_identity": {"pin": "same"},
                  "target_olean_before_sha256": runner.digest(target),
                  "target_olean_after_sha256": runner.digest(target)}
        for relative in runner.INPUTS:
            if relative == runner.RUNNER:
                continue
            path = destination / "inputs" / Path(relative).name
            path.write_bytes((nsrw / relative).read_bytes())
            report["inputs"][path.name] = runner.digest(path)
        for name in ["source", *names]:
            text = "\n".join(f"'NSRW.P2.{n}' depends on axioms: [propext, Classical.choice, Quot.sound]"
                             for n in runner.SURFACES.get(name, ()))
            out, err = destination / (name + ".stdout.log"), destination / (name + ".stderr.log")
            out.write_text(text, encoding="utf-8")
            err.write_bytes(b"warning" if failure == "stderr" and name == runner.MODULE else b"")
            report["stages"][name] = {"exit": 1 if failure == name else 0,
                "stdout_bytes": out.stat().st_size, "stderr_bytes": err.stat().st_size,
                "stdout_sha256": runner.digest(out), "stderr_sha256": runner.digest(err)}
        for name in names:
            artifact = destination / "artifacts" / (name + ".olean")
            artifact.write_bytes(b"fresh " + name.encode())
            report["fresh_artifacts"][artifact.name] = runner.digest(artifact)
        report["axiom_surfaces"] = runner.inspect_axioms(
            (destination / (runner.MODULE + ".stdout.log")).read_text(encoding="utf-8"), runner.THEOREMS)
        if failure == "claim":
            report["claim_status"] = "CONFIRMED"
        if failure == "execution":
            report["check_status"] = "ERROR[LEAN_COMPILE]"
        if failure == "stage_set":
            report["stages"].pop("source")
        if failure == "artifact_set":
            report["fresh_artifacts"].pop(names[0] + ".olean")
        if failure == "input_set":
            report["inputs"].pop(Path(runner.ENGINE).name)
        if failure == "axiom_metadata":
            report["axiom_surfaces"] = {}
        (destination / "run-metadata.json").write_text(json.dumps(report), encoding="utf-8")
        if failure == "metadata":
            (destination / "run-metadata.json").write_text("{}", encoding="utf-8")
        if failure in {"log", "axioms"}:
            (destination / (runner.MODULE + ".stdout.log")).write_bytes(b"changed")
        if failure == "artifact":
            (destination / "artifacts" / (names[0] + ".olean")).write_bytes(b"changed")
        if failure in {"input", "engine"}:
            name = names[0] + ".lean" if failure == "input" else Path(runner.ENGINE).name
            (destination / "inputs" / name).write_bytes(b"changed")
        if failure == "extra_input":
            (destination / "inputs" / "shadow.lean").write_bytes(b"extra")
        if failure == "extra_artifact":
            (destination / "artifacts" / "shadow.olean").write_bytes(b"extra")
        if failure == "target":
            target.write_bytes(b"changed")
        if failure == "invocation":
            raise FileNotFoundError("missing executable")
        return report

    engine = SimpleNamespace(run=execute, COMMITTED=runner.COMMITTED,
                             DEVELOPMENT=runner.DEVELOPMENT, BASE=runner.BASE,
                             HELPER_BLOB=runner.PINS[runner.HELPER], MODULE=runner.MODULE,
                             THEOREMS=runner.THEOREMS)
    if failure == "dependency_surface":
        engine.COMMITTED = {}
    if failure == "theorem_surface":
        engine.THEOREMS = ("other",)
    if failure == "engine_base":
        engine.BASE = "c" * 40
    helper = SimpleNamespace(reject_shadow_inputs=lambda *_: None,
        source_identity=lambda *_: {"pin": "changed" if failure == "source_identity" else "same"},
        TARGET_ARTIFACT="target.olean")
    monkeypatch.setattr(runner, "__file__", str(nsrw / runner.RUNNER))
    identities = iter([binding, {**binding, "commit": "c" * 40} if failure == "head" else binding])
    monkeypatch.setattr(runner, "identity", lambda *_: next(identities))

    def base_binding(*_):
        if failure == "base_dirty":
            raise RuntimeError("DEPENDENCY_BASE_DIRTY")
        return {"commit": runner.BASE, "tracked_clean": True}

    monkeypatch.setattr(runner, "base_identity", base_binding)
    monkeypatch.setattr(runner, "load_module", lambda path, _: engine if path.name == Path(runner.ENGINE).name else helper)
    report = runner.replay(source, nsrw, base, output, "a" * 40)
    assert subprocess.run is original_run
    return report, output


def test_success_never_self_promotes_and_preserves_report(tmp_path, monkeypatch):
    report, output = synthetic(tmp_path, monkeypatch)
    assert report["check_status"] == runner.PASS
    assert report["claim_authority"] == "NONE" and report["claim_status"] == "UNVERIFIED"
    assert len(report["axiom_surfaces"]) == 19
    assert report["pre_identity"] == report["post_identity"]
    assert (output / Path(runner.RUNNER).name).is_file()
    assert Path(str(output) + "-replay-evidence.zip").is_file()


@pytest.mark.parametrize("failure", ["source", runner.MODULE, "stderr", "execution", "claim",
    "log", "artifact", "input", "engine", "target", "source_identity", "head", "base_dirty",
    "dependency_surface", "theorem_surface", "engine_base", "metadata", "axiom_metadata",
    "extra_input", "extra_artifact", "stage_set", "artifact_set", "input_set", "invocation"])
def test_failure_is_preserved_without_claim_admission(tmp_path, monkeypatch, failure):
    report, output = synthetic(tmp_path, monkeypatch, failure)
    assert report["check_status"] == "ERROR[REPLAY_NOT_ADMITTED]"
    assert report["claim_authority"] == "NONE" and report["claim_status"] == "UNVERIFIED"
    assert report["error"]
    assert (output / "replay-metadata.json").is_file()
    assert Path(str(output) + "-replay-evidence.zip").is_file()


@pytest.mark.parametrize("failure", ["missing", "duplicate", "extra", "sorry"])
def test_axiom_surfaces_rejected(failure):
    text = "'NSRW.P2.test' depends on axioms: [propext, Classical.choice, Quot.sound]"
    if failure == "missing":
        text = ""
    elif failure == "duplicate":
        text += "\n" + text
    elif failure == "extra":
        text = text.replace("Quot.sound]", "Quot.sound, badAx]")
    else:
        text += "\nsorryAx"
    with pytest.raises(RuntimeError):
        runner.inspect_axioms(text, ("test",))


@pytest.mark.parametrize("failure", ["head", "dirty", "bytes", "blob"])
def test_identity_wrong_commit_dirty_and_input_rejected(tmp_path, monkeypatch, failure):
    relative = runner.INPUTS[0]
    path = tmp_path / relative
    path.parent.mkdir(parents=True)
    path.write_bytes(b"candidate")

    def git(_, args, env):
        if args[0] == "rev-parse":
            return ("b" * 40 if failure == "head" else "a" * 40).encode()
        if args[0] == "status":
            return b" M file" if failure == "dirty" else b""
        return b"different" if failure == "bytes" else b"candidate"

    monkeypatch.setattr(runner, "git", git)
    with pytest.raises(RuntimeError):
        runner.identity(tmp_path, "a" * 40, {})


@pytest.mark.parametrize("protected", ["output", "source", "nsrw", "base", "archive", "replay_archive"])
def test_output_and_archives_are_not_overwritten(tmp_path, protected):
    roots = {n: tmp_path / n for n in ("source", "nsrw", "base")}
    output = tmp_path / "run"
    if protected in roots:
        output = roots[protected] / ".." / protected / "run"
    elif protected == "output":
        output.mkdir()
    else:
        Path(str(output) + ("-evidence.zip" if protected == "archive" else "-replay-evidence.zip")).write_bytes(b"preserve")
    with pytest.raises(RuntimeError):
        runner.replay(roots["source"], roots["nsrw"], roots["base"], output, "a" * 40)


def test_pins_match_current_portable_proof_bytes_and_scope():
    root = Path(__file__).parents[1]
    assert len(runner.INPUTS) == 17
    assert len(runner.COMMITTED) == 8 and len(runner.Z_BLOBS) == 6
    for relative, pin in runner.PINS.items():
        data = (root / relative).read_bytes().replace(b"\r\n", b"\n")
        assert hashlib.sha1(b"blob " + str(len(data)).encode() + b"\0" + data).hexdigest() == pin
    assert not any("observe" in p or "preserve" in p or p.startswith("docs/") for p in runner.INPUTS)
    assert runner.THEOREMS[-1] == "profileMJ_firstRepair_zero_small_positive"
