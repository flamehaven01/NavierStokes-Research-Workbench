"""Synthetic runner controls only; these tests are NOT Lean compile evidence."""

import ast
import base64
import hashlib
import importlib.util
import json
from pathlib import Path
from types import SimpleNamespace

import pytest

SPEC = importlib.util.spec_from_file_location(
    "zplus_development", Path(__file__).parents[1] / "colab/run-zplus-j-development.py"
)
runner = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(runner)


def axiom_output():
    return "\n".join(
        f"'NSRW.P2.{name}' depends on axioms: [Classical.choice, Quot.sound, propext]"
        for name in runner.THEOREMS
    )


def test_exact_minimal_dependency_and_conditional_scope():
    root = Path(__file__).parents[1]
    assert list(runner.DEPENDENCIES) == [
        "P2_Z01_LocalMassIdentities", "P2_Z02_BoundaryMassSigns"
    ]
    for module, digest in runner.DEPENDENCIES.items():
        assert runner.sha(root / "formal/p2" / (module + ".lean")) == digest
    proof = (root / "formal/p2" / (runner.MODULE + ".lean")).read_text(encoding="utf-8")
    assert proof.splitlines()[0] == "import P2_Z02_BoundaryMassSigns"
    target = proof.split("theorem angularMoment_pos_of_firstRepair_mass_zero", 1)[1].split(":= by", 1)[0]
    assert "(hM : localMass F eta r = 0)" in target
    assert "(hc1 : 0 < localSecondRepairCoefficient F eta)" in target
    assert "0 < localAngularMoment F eta r" in target
    assert "0 < eta" not in target and "epsilon" not in target
    assert "sorry" not in proof and "admit" not in proof and "axiom " not in proof
    for name in runner.THEOREMS:
        assert "#print axioms NSRW.P2." + name in proof


def test_frozen_notebook_contains_exact_current_execution_inputs():
    root = Path(__file__).parents[1]
    notebook = json.loads((root / "colab/ZPLUS_J_DEVELOPMENT_2026-10-11.ipynb").read_text(
        encoding="utf-8"
    ))
    cells = [c for c in notebook["cells"] if c["cell_type"] == "code"]
    assert len(cells) == 1 and cells[0]["outputs"] == []
    code = "".join(cells[0]["source"])
    tree = ast.parse(code)
    assignment = next(n for n in tree.body if isinstance(n, ast.Assign)
                      and any(isinstance(t, ast.Name) and t.id == "PAYLOAD" for t in n.targets))
    payload = json.loads(ast.literal_eval(assignment.value.args[0]))
    expected = {module + ".lean": root / "formal/p2" / (module + ".lean")
                for module in [*runner.DEPENDENCIES, runner.MODULE]}
    expected["run-zplus-j-development.py"] = root / "colab/run-zplus-j-development.py"
    assert {item["name"] for item in payload} == set(expected)
    for item in payload:
        data = base64.b64decode(item["base64"], validate=True)
        assert data == expected[item["name"]].read_bytes()
        assert hashlib.sha256(data).hexdigest() == item["sha256"]
    compile(code, "frozen-zplus-notebook", "exec")


@pytest.mark.parametrize("surface", ["full", "reduced", "empty_list", "no_axioms"])
def test_auxiliary_axiom_observation_is_not_fabricated(surface):
    text = axiom_output()
    first = text.splitlines()[0]
    if surface == "reduced":
        text = text.replace(first, first.replace("Classical.choice, Quot.sound, propext", "propext"))
    elif surface == "empty_list":
        text = text.replace(first, first.split("[")[0] + "[]")
    elif surface == "no_axioms":
        text = text.replace(first, f"'NSRW.P2.{runner.THEOREMS[0]}' does not depend on any axioms")
    observed = runner.inspect_axioms(text)
    assert len(observed) == 12
    assert set(observed["NSRW.P2." + runner.THEOREMS[-1]]) == runner.STANDARD_AXIOMS


@pytest.mark.parametrize("change", ["missing", "duplicate", "sorry", "extra", "target_empty"])
def test_bad_axiom_surface_rejected(change):
    text = axiom_output()
    if change == "missing":
        text = "\n".join(text.splitlines()[1:])
    elif change == "duplicate":
        text += "\n" + text.splitlines()[0]
    elif change == "sorry":
        text += "\nsorryAx"
    elif change == "extra":
        text = text.replace("propext]", "propext, extraAx]", 1)
    else:
        last = text.splitlines()[-1]
        text = text.replace(last, last.split("[")[0] + "[]")
    with pytest.raises(ValueError):
        runner.inspect_axioms(text)


@pytest.mark.parametrize("protected", ["source", "base", "dependencies", "archive", "existing"])
def test_protected_output_is_not_modified(tmp_path, protected):
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


@pytest.mark.parametrize("failure", [
    "none", "proof_identity", "dependency_identity", "base_identity", "helper_identity",
    "source_exit", "source_invocation", "zplus_invocation", "zplus_exit", "zplus_stderr",
    "zplus_axioms", "missing_artifact", "artifact_drift", "input_drift", "log_drift",
    "source_target_drift", "source_identity_drift", "original_proof_drift",
])
def test_synthetic_chain_preserves_failure_without_admission(tmp_path, monkeypatch, failure):
    source, base, deps = [tmp_path / name for name in ("source", "base", "deps")]
    for path in (source, base, deps):
        path.mkdir()
    proof = tmp_path / "proof.lean"
    proof.write_bytes(b"target")
    dependency = deps / "dependency.lean"
    dependency.write_bytes(b"dependency")
    monkeypatch.setattr(runner, "DEPENDENCIES", {
        "dependency": "0" * 64 if failure == "dependency_identity" else runner.sha(dependency)
    })
    helper = (b"TARGET_ARTIFACT = 'target.olean'\ncalls = 0\n"
              b"def source_identity(root, env):\n"
              b" global calls\n calls += 1\n return {'id': calls if "
              + (b"True" if failure == "source_identity_drift" else b"False")
              + b" else 1}\n"
              b"def nsrw_observation(root, env):\n return {'dirty': True}\n")
    monkeypatch.setattr(runner, "HELPER_BLOB",
                        "0" * 40 if failure == "helper_identity" else runner.blob(helper))

    def command(args, **kwargs):
        if args[0] == "git":
            data = ((b"wrong" if failure == "base_identity" else runner.BASE.encode())
                    if args[1] == "rev-parse" else helper)
            return SimpleNamespace(returncode=0, stdout=data)
        is_source = args[1] == "build"
        is_target = not is_source and Path(args[-1]).stem == runner.MODULE
        if (is_source and failure == "source_invocation") or (
                is_target and failure == "zplus_invocation"):
            raise FileNotFoundError("synthetic executable absent")
        if is_source:
            (source / "target.olean").write_bytes(b"source-target")
        elif not (is_target and failure == "missing_artifact"):
            Path(args[args.index("-o") + 1]).write_bytes(b"artifact:" + args[-1].encode())
        if is_target:
            kwargs["stdout"].write((axiom_output() + (
                "\nsorryAx" if failure == "zplus_axioms" else ""
            )).encode())
            if failure == "zplus_stderr":
                kwargs["stderr"].write(b"raw invalid UTF8: \xff must be preserved")
            if failure == "artifact_drift":
                (Path(args[args.index("-o") + 1]).parent / "dependency.olean").write_bytes(b"changed")
            if failure == "input_drift":
                (Path(args[-1]).parent / "dependency.lean").write_bytes(b"changed")
            if failure == "log_drift":
                (Path(kwargs["stdout"].name).parent / "source.stdout.log").write_bytes(b"changed")
            if failure == "source_target_drift":
                (source / "target.olean").write_bytes(b"changed")
            if failure == "original_proof_drift":
                proof.write_bytes(b"changed")
        failed = (is_source and failure == "source_exit") or (is_target and failure == "zplus_exit")
        return SimpleNamespace(returncode=1 if failed else 0)

    monkeypatch.setattr(runner, "run_command", command)
    output = tmp_path / "run"
    digest = "0" * 64 if failure == "proof_identity" else runner.sha(proof)
    meta = runner.run(source, base, deps, proof, output, digest)
    assert meta["claim_authority"] == "NONE" and meta["claim_status"] == "UNVERIFIED"
    assert Path(str(output) + "-evidence.zip").is_file()
    assert meta["check_status"].startswith("PASS[" if failure == "none" else "ERROR[")
    recorded = json.loads((output / "run-metadata.json").read_text())
    assert recorded == meta
    if failure == "none":
        assert len(meta["stages"]) == 3 and len(meta["fresh_artifacts"]) == 2
        assert meta["nsrw_pre_observation"]["dirty"] is True
    else:
        assert meta["mathematical_interpretation"] == "NONE"
    if failure.endswith("invocation"):
        assert meta["failure_boundary"].endswith("_INVOCATION")
    if failure == "zplus_stderr":
        assert (output / (runner.MODULE + ".stderr.log")).read_bytes().startswith(
            b"raw invalid UTF8: \xff"
        )
