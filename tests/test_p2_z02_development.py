"""Focused driver controls only; not Lean compilation or claim admission."""

import importlib.util
import json
from pathlib import Path

import pytest

SPEC = importlib.util.spec_from_file_location(
    "z02_development", Path(__file__).parents[1] / "colab/run-z02-development.py"
)
runner = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(runner)


def axiom_output():
    return "\n".join(
        f"'NSRW.P2.{name}' depends on axioms: [Classical.choice, Quot.sound, propext]"
        for name in runner.THEOREMS
    )


def test_exact_named_surface_only():
    assert len(runner.inspect_axioms(axiom_output())) == 8
    assert runner.DEPENDENCY == "P2_Z01_LocalMassIdentities"
    assert runner.Z01_SHA == "ff7101067a98fbaa8974c1aa409b83740cd17eb4f1778f20cdc23b44e2a5c267"


@pytest.mark.parametrize("alteration", ["missing", "duplicate", "sorry", "extra-axiom"])
def test_bad_axiom_surface_rejected(alteration):
    text = axiom_output()
    if alteration == "missing":
        text = "\n".join(text.splitlines()[1:])
    elif alteration == "duplicate":
        text += "\n" + text.splitlines()[0]
    elif alteration == "sorry":
        text += "\nsorryAx"
    else:
        text = text.replace("propext]", "propext, newAxiom]", 1)
    with pytest.raises(ValueError):
        runner.inspect_axioms(text)


@pytest.mark.parametrize("digest", ["invalid", "0" * 64])
def test_input_failure_preserved_without_admission(tmp_path, digest):
    proof = tmp_path / "proof.lean"
    proof.write_bytes(b"example : True := True.intro\n")
    output = tmp_path / "run"
    meta = runner.run(tmp_path / "source", tmp_path / "base", tmp_path / "z01",
                      proof, output, digest)
    assert meta["failure_boundary"] == "PROOF_SHA_MISMATCH"
    assert meta["claim_authority"] == "NONE"
    assert meta["claim_status"] == "UNVERIFIED"
    assert meta["stages"] == {}
    assert meta["mathematical_interpretation"] == "NONE"
    assert json.loads((output / "run-metadata.json").read_text())["check_status"].startswith("ERROR[")
    assert Path(str(output) + "-evidence.zip").is_file()


def test_wrong_z01_bytes_rejected_before_tools(tmp_path):
    proof = tmp_path / "proof.lean"
    proof.write_bytes(b"proof bytes")
    dependency = tmp_path / "dependency.lean"
    dependency.write_bytes(b"not the compiled Z01 bytes")
    meta = runner.run(tmp_path / "source", tmp_path / "base", dependency,
                      proof, tmp_path / "run", runner.sha(proof))
    assert meta["failure_boundary"] == "Z01_DEPENDENCY_SHA_MISMATCH"
    assert meta["stages"] == {}
    assert meta["claim_status"] == "UNVERIFIED"


@pytest.mark.parametrize("protected", ["source", "base", "archive", "existing"])
def test_protected_or_existing_output_not_modified(tmp_path, protected):
    source, base, output = tmp_path / "source", tmp_path / "base", tmp_path / "run"
    if protected in ("source", "base"):
        root = source if protected == "source" else base
        root.mkdir()
        output = root / ".." / root.name / "run"
    elif protected == "archive":
        Path(str(output) + "-evidence.zip").write_bytes(b"preserve")
    else:
        output.mkdir()
        (output / "keep").write_bytes(b"preserve")
    with pytest.raises(ValueError, match="OUTPUT_MUST_BE_NEW"):
        runner.run(source, base, tmp_path / "z01", tmp_path / "proof", output, "0" * 64)
    if protected == "archive":
        assert Path(str(output) + "-evidence.zip").read_bytes() == b"preserve"
    elif protected == "existing":
        assert (output / "keep").read_bytes() == b"preserve"
    else:
        assert not output.exists()
