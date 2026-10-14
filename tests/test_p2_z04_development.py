"""Z04 driver negative controls only; synthetic execution is not Lean evidence."""

import importlib.util
import json
from pathlib import Path
from types import SimpleNamespace

import pytest

SPEC = importlib.util.spec_from_file_location(
    "z04_development", Path(__file__).parents[1] / "colab/run-z04-development.py"
)
runner = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(runner)


def axiom_output():
    return "\n".join(
        f"'NSRW.P2.{name}' depends on axioms: [Classical.choice, Quot.sound, propext]"
        for name in runner.THEOREMS
    )


def test_exact_source_scope_and_dependency_bytes():
    root = Path(__file__).parents[1]
    assert len(runner.COMMITTED) == 8
    assert len(runner.DEVELOPMENT) == 3
    for module, digest in runner.DEVELOPMENT.items():
        assert runner.sha(root / "formal/p2" / (module + ".lean")) == digest
    proof = (root / "formal/p2" / (runner.MODULE + ".lean")).read_text(encoding="utf-8")
    assert proof.splitlines()[:2] == [
        "import P2_C04_SmallPositiveEta", "import P2_Z03_ConditionalInteriorZero"
    ]
    assert "(hr : 1 ≤ r)" in proof
    assert "F.M eta (Real.exp F.data.core.pulseStart * r) = 0" in proof
    assert "F.J" not in proof
    for name in runner.THEOREMS:
        assert "#print axioms NSRW.P2." + name in proof


@pytest.mark.parametrize("alias", ["source_axioms", "empty_list", "no_axioms_message"])
def test_observed_alias_axioms_not_fabricated(alias):
    text = axiom_output()
    first = text.splitlines()[0]
    if alias == "empty_list":
        text = text.replace(first, first.split("[")[0] + "[]")
    elif alias == "no_axioms_message":
        text = text.replace(first, f"'NSRW.P2.{runner.THEOREMS[0]}' does not depend on any axioms")
    observed = runner.inspect_axioms(text)
    assert len(observed) == 4
    assert observed["NSRW.P2." + runner.THEOREMS[0]] == (
        ["Classical.choice", "Quot.sound", "propext"] if alias == "source_axioms" else []
    )


@pytest.mark.parametrize("change", ["missing", "duplicate", "sorry", "extra", "alias_extra"])
def test_bad_axiom_surfaces_rejected(change):
    text = axiom_output()
    if change == "missing":
        text = "\n".join(text.splitlines()[1:])
    elif change == "duplicate":
        text += "\n" + text.splitlines()[0]
    elif change == "sorry":
        text += "\nsorryAx"
    elif change == "alias_extra":
        text = text.replace("propext]", "propext, extraAx]", 1)
    else:
        text = text.replace("propext]", "propext, extraAx]")
    with pytest.raises(ValueError):
        runner.inspect_axioms(text)


@pytest.mark.parametrize("failure", ["proof", *runner.DEVELOPMENT])
def test_input_failure_preserved_without_admission(tmp_path, failure, monkeypatch):
    proof = tmp_path / "proof.lean"
    proof.write_bytes(b"proof")
    deps = tmp_path / "dependencies"
    deps.mkdir()
    for module in runner.DEVELOPMENT:
        (deps / (module + ".lean")).write_bytes(module.encode())
    pins = {module: runner.sha(deps / (module + ".lean")) for module in runner.DEVELOPMENT}
    if failure != "proof":
        pins[failure] = "0" * 64
    monkeypatch.setattr(runner, "DEVELOPMENT", pins)
    output = tmp_path / "run"
    meta = runner.run(tmp_path / "source", tmp_path / "base", deps, proof, output,
                      "0" * 64 if failure == "proof" else runner.sha(proof))
    assert meta["stages"] == {}
    assert meta["claim_authority"] == "NONE"
    assert meta["claim_status"] == "UNVERIFIED"
    assert meta["check_status"].startswith("ERROR[")
    assert Path(str(output) + "-evidence.zip").is_file()
    assert json.loads((output / "run-metadata.json").read_text())["mathematical_interpretation"] == "NONE"


@pytest.mark.parametrize("protected", ["source", "base", "dependencies", "archive", "existing"])
def test_protected_output_cannot_be_overwritten(tmp_path, protected):
    roots = {name: tmp_path / name for name in ("source", "base", "dependencies")}
    output = tmp_path / "run"
    if protected in roots:
        output = roots[protected] / ".." / protected / "run"
    elif protected == "archive":
        Path(str(output) + "-evidence.zip").write_bytes(b"keep")
    else:
        output.mkdir()
        (output / "keep").write_bytes(b"keep")
    with pytest.raises(ValueError, match="OUTPUT_MUST_BE_NEW"):
        runner.run(roots["source"], roots["base"], roots["dependencies"],
                   tmp_path / "proof", output, "0" * 64)
    if protected == "archive":
        assert Path(str(output) + "-evidence.zip").read_bytes() == b"keep"
    elif protected == "existing":
        assert (output / "keep").read_bytes() == b"keep"


@pytest.mark.parametrize("failure", ["none", "source_exit", "source_invocation", "proof_exit",
                                    "proof_stderr", "proof_axioms", "artifact_drift", "source_drift"])
def test_synthetic_fresh_chain_fail_closed(tmp_path, monkeypatch, failure):
    source, base, deps = [tmp_path / name for name in ("source", "base", "deps")]
    for path in (source, base, deps):
        path.mkdir()
    proof = tmp_path / "proof.lean"
    proof.write_bytes(b"target")
    development = {"dev": b"development"}
    committed = {"dep": b"committed"}
    for module, data in development.items():
        (deps / (module + ".lean")).write_bytes(data)
    monkeypatch.setattr(runner, "DEVELOPMENT", {m: runner.sha(deps / (m + ".lean"))
                                              for m in development})
    monkeypatch.setattr(runner, "COMMITTED", {m: runner.blob(data) for m, data in committed.items()})
    helper = (b"TARGET_ARTIFACT = 'target.olean'\n"
              b"calls = 0\n"
              b"def source_identity(root, env):\n"
              b" global calls\n calls += 1\n return {'id': calls if "
              + (b"True" if failure == "source_drift" else b"False")
              + b" else 1}\n"
              b"def nsrw_observation(root, env):\n return {'dirty': True}\n")
    monkeypatch.setattr(runner, "HELPER_BLOB", runner.blob(helper))

    def command(args, **kwargs):
        if args[0] == "git":
            if args[1] == "rev-parse":
                data = runner.BASE.encode()
            elif args[-1].endswith("run-c02-development.py"):
                data = helper
            else:
                data = committed["dep"]
            return SimpleNamespace(returncode=0, stdout=data)
        is_source = args[1] == "build"
        is_target = not is_source and Path(args[-1]).stem == runner.MODULE
        if is_source and failure == "source_invocation":
            raise FileNotFoundError("synthetic executable absent")
        if is_source:
            (source / "target.olean").write_bytes(b"source-target")
        else:
            Path(args[args.index("-o") + 1]).write_bytes(b"artifact:" + args[-1].encode())
        if is_target:
            text = axiom_output() + ("\nsorryAx" if failure == "proof_axioms" else "")
            kwargs["stdout"].write(text.encode())
            if failure == "proof_stderr":
                kwargs["stderr"].write(b"must review")
            if failure == "artifact_drift":
                (Path(args[args.index("-o") + 1]).parent / "dep.olean").write_bytes(b"changed")
        nonzero = (is_source and failure == "source_exit") or (is_target and failure == "proof_exit")
        return SimpleNamespace(returncode=1 if nonzero else 0)

    monkeypatch.setattr(runner, "run_command", command)
    output = tmp_path / "run"
    meta = runner.run(source, base, deps, proof, output, runner.sha(proof))
    assert meta["claim_authority"] == "NONE" and meta["claim_status"] == "UNVERIFIED"
    assert Path(str(output) + "-evidence.zip").is_file()
    assert meta["check_status"].startswith("PASS[" if failure == "none" else "ERROR[")
    if failure == "none":
        assert len(meta["stages"]) == 4 and len(meta["fresh_artifacts"]) == 3
        assert meta["nsrw_pre_observation"]["dirty"] is True
    elif failure == "source_invocation":
        assert meta["failure_boundary"] == "SOURCE_INVOCATION"
