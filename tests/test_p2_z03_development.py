"""Z03 runner controls only; these tests are not Lean or claim evidence."""

import importlib.util
import json
from pathlib import Path

import pytest

SPEC = importlib.util.spec_from_file_location(
    "z03_development", Path(__file__).parents[1] / "colab/run-z03-development.py"
)
runner = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(runner)


def output():
    return "\n".join(
        f"'NSRW.P2.{name}' depends on axioms: [Classical.choice, Quot.sound, propext]"
        for name in runner.SURFACES["z03"]
    )


def test_scope_and_exact_axiom_surface():
    assert list(runner.SURFACES) == ["z01", "z02", "z03"]
    assert len(runner.inspect_axioms(output(), runner.SURFACES["z03"])) == 3
    assert len(runner.DEPENDENCIES) == 2
    root = Path(__file__).parents[1]
    for module, digest in runner.DEPENDENCIES.items():
        assert runner.sha(root / "formal/p2" / (module + ".lean")) == digest
    proof = (root / "formal/p2" / (runner.MODULE + ".lean")).read_text(encoding="utf-8")
    assert proof.splitlines()[0] == "import P2_Z02_BoundaryMassSigns"
    assert "import P2_C04" not in proof


@pytest.mark.parametrize("change", ["missing", "duplicate", "sorry", "extra"])
def test_bad_axiom_surface(change):
    text = output()
    if change == "missing":
        text = "\n".join(text.splitlines()[1:])
    elif change == "duplicate":
        text += "\n" + text.splitlines()[0]
    elif change == "sorry":
        text += "\nsorryAx"
    else:
        text = text.replace("propext]", "propext, customAxiom]", 1)
    with pytest.raises(ValueError):
        runner.inspect_axioms(text, runner.SURFACES["z03"])


@pytest.mark.parametrize("failure", ["proof", "z01", "z02"])
def test_input_failure_is_archived_without_admission(tmp_path, failure, monkeypatch):
    proof = tmp_path / "proof.lean"
    proof.write_bytes(b"proof")
    deps = tmp_path / "dependencies"
    deps.mkdir()
    for module in runner.DEPENDENCIES:
        (deps / (module + ".lean")).write_bytes(module.encode())
    pins = {module: runner.sha(deps / (module + ".lean"))
            for module in runner.DEPENDENCIES}
    if failure != "proof":
        pins[list(pins)[0 if failure == "z01" else 1]] = "0" * 64
    monkeypatch.setattr(runner, "DEPENDENCIES", pins)
    run_dir = tmp_path / "run"
    meta = runner.run(tmp_path / "source", tmp_path / "base", deps, proof, run_dir,
                      "0" * 64 if failure == "proof" else runner.sha(proof))
    assert meta["failure_boundary"].startswith(
        "PROOF_SHA_MISMATCH" if failure == "proof" else "DEPENDENCY_SHA_MISMATCH"
    )
    assert meta["stages"] == {}
    assert meta["claim_authority"] == "NONE"
    assert meta["claim_status"] == "UNVERIFIED"
    assert meta["mathematical_interpretation"] == "NONE"
    assert Path(str(run_dir) + "-evidence.zip").is_file()
    assert json.loads((run_dir / "run-metadata.json").read_text())["check_status"].startswith("ERROR[")


@pytest.mark.parametrize("protected", ["source", "base", "dependencies", "archive", "existing"])
def test_existing_and_protected_outputs_preserved(tmp_path, protected):
    roots = {name: tmp_path / name for name in ("source", "base", "dependencies")}
    output_path = tmp_path / "run"
    if protected in roots:
        output_path = roots[protected] / ".." / protected / "run"
    elif protected == "archive":
        Path(str(output_path) + "-evidence.zip").write_bytes(b"keep")
    else:
        output_path.mkdir()
        (output_path / "keep").write_bytes(b"keep")
    with pytest.raises(ValueError, match="OUTPUT_MUST_BE_NEW"):
        runner.run(roots["source"], roots["base"], roots["dependencies"],
                   tmp_path / "proof", output_path, "0" * 64)
    if protected == "archive":
        assert Path(str(output_path) + "-evidence.zip").read_bytes() == b"keep"
    elif protected == "existing":
        assert (output_path / "keep").read_bytes() == b"keep"
    else:
        assert not output_path.exists()
