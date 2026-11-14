import hashlib
import io
import json
import zipfile
from dataclasses import dataclass, replace
from pathlib import Path
from types import ModuleType

import pytest

from nsrw import research_verification_cli
from nsrw.lean_archive_verification import check_lean_archive, inspect_declarations
from nsrw.research_verification import Finding, Status, Verification, run_verification

ROOT = Path(__file__).resolve().parents[1]


def check(evaluate):
    return Verification(
        "extension-example", "1", "sum of two integers", "exact addition",
        "two fixed input operands", "EXACT_ARITHMETIC_DIAGNOSTIC",
        ("operands", "result"), evaluate,
    )


def test_new_evaluator_can_use_common_runner_with_multiple_inputs():
    def evaluate(evidence):
        operands = json.loads(evidence["operands"])
        matches = sum(operands) == int(evidence["result"])
        return Finding(Status.PASS if matches else Status.FAIL, {"matches": matches})

    evidence = {"operands": b"[2,3]", "result": b"5"}
    report = run_verification(check(evaluate), evidence)
    assert report["status"] == "PASS"
    assert report["inputs"]["result"] == {"sha256": hashlib.sha256(b"5").hexdigest(), "bytes": 1}
    assert report["claim_authority"] == "NONE"
    assert report["claim_status"] == "UNVERIFIED"
    assert run_verification(check(evaluate), {**evidence, "result": b"6"})["status"] == "FAIL"


@pytest.mark.parametrize(
    ("evidence", "expected"),
    [({"operands": b"[]"}, "NOT_RUN"), ({"other": b""}, "FAIL")],
)
def test_incomplete_or_unexpected_input_stops_before_evaluation(evidence, expected):
    def should_not_run(_evidence):
        pytest.fail("evaluated input outside the checker contract")

    assert run_verification(check(should_not_run), evidence)["status"] == expected


@pytest.mark.parametrize(
    ("result", "expected"),
    [
        (ImportError("missing backend"), "ENV_BLOCKED"),
        (FileNotFoundError("backend file missing"), "ENV_BLOCKED"),
        (RuntimeError("unexpected checker failure"), "ERROR"),
        ({"status": "PASS"}, "ERROR"),
        (Finding(Status.PASS, {"nonfinite": float("nan")}), "ERROR"),
        (Finding(Status.UNRESOLVED, {"reason": "interval overlaps zero"}), "UNRESOLVED"),
    ],
)
def test_checker_error_or_unresolved_does_not_pass(result, expected):
    def evaluate(_evidence):
        if isinstance(result, Exception):
            raise result
        return result

    evidence = {"operands": b"[]", "result": b"0"}
    assert run_verification(check(evaluate), evidence)["status"] == expected


@pytest.fixture
def runner():
    return research_verification_cli


def test_pde_cli_checks_manufactured_oracle_and_force_mutation(runner, capsys):
    fixture = ROOT / "examples" / "research-verification" / "forced-shear.json"
    assert runner.main(["forced-shear", "--input", f"fixture={fixture}"]) == 0
    report = json.loads(capsys.readouterr().out)
    assert report["evidence_class"] == "SAMPLED_PDE_DIAGNOSTIC"
    assert report["details"]["checks"] == {
        "momentum_and_divergence": True, "force_removal_detected": True,
    }
    assert report["details"]["removed_force_sample"]["residual"][0] == pytest.approx(0.75)


def test_mutated_fixture_fails(runner, capsys, tmp_path):
    fixture = tmp_path / "mutated.json"
    fixture.write_text('{"tolerance": 1.0}', encoding="utf-8")
    assert runner.main(["forced-shear", "--input", f"fixture={fixture}"]) == 1
    assert json.loads(capsys.readouterr().out)["status"] == "FAIL"


def test_cli_missing_file_is_not_run(runner, capsys, tmp_path):
    fixture = tmp_path / "missing.json"
    assert runner.main(["forced-shear", "--input", f"fixture={fixture}"]) == 1
    report = json.loads(capsys.readouterr().out)
    assert report["status"] == "NOT_RUN"
    assert report["details"]["missing_inputs"] == ["fixture"]


def test_cli_cannot_overwrite_report(runner, tmp_path):
    fixture = ROOT / "examples" / "research-verification" / "forced-shear.json"
    output = tmp_path / "report.json"
    args = ["forced-shear", "--input", f"fixture={fixture}", "--output", str(output)]
    assert runner.main(args) == 0
    original = output.read_bytes()
    with pytest.raises(SystemExit) as raised:
        runner.main(args)
    assert raised.value.code == 2
    assert output.read_bytes() == original


def test_manifest_binds_report_inputs_and_implementation(runner, tmp_path):
    fixture = ROOT / "examples" / "research-verification" / "forced-shear.json"
    output, manifest = (tmp_path / name for name in ("report.json", "manifest.json"))
    assert runner.main([
        "forced-shear", "--input", f"fixture={fixture}",
        "--output", str(output), "--manifest", str(manifest),
    ]) == 0
    record = json.loads(manifest.read_bytes())
    assert record["report_sha256"] == hashlib.sha256(output.read_bytes()).hexdigest()
    assert record["inputs"] == json.loads(output.read_bytes())["inputs"]
    implementation = ROOT / "src/nsrw/research_verification.py"
    assert record["implementation_files"]["nsrw.research_verification"]["sha256"] == (
        hashlib.sha256(implementation.read_bytes()).hexdigest()
    )
    assert record["runtime"]["python"]


@pytest.mark.parametrize(
    ("check_id", "input_spec", "component"),
    [
        ("forced-shear", "fixture=examples/research-verification/forced-shear.json", "module"),
        ("mb06-ratio", "record=examples/research-verification/mb06-ratio-20261113.json", "package"),
    ],
)
def test_manifest_rejects_incomplete_identity(runner, tmp_path, monkeypatch, capsys, check_id,
                                             input_spec, component):
    from nsrw import verification_manifest

    identity = verification_manifest.implementation_identity(check_id)
    if component == "module":
        identity["implementation_files"].pop("nsrw.math_kernel.operators")
        identity["unavailable_implementation_files"] = ["nsrw.math_kernel.operators"]
    else:
        identity["dependencies"]["mpmath"]["version"] = None
    monkeypatch.setattr(verification_manifest, "implementation_identity", lambda _name: identity)
    output, manifest = (tmp_path / name for name in ("report.json", "manifest.json"))
    with pytest.raises(SystemExit) as raised:
        runner.main([check_id, "--input", input_spec, "--output", str(output),
                     "--manifest", str(manifest)])
    assert raised.value.code == 2
    assert "execution manifest blocked" in capsys.readouterr().err
    assert not output.exists()
    assert not manifest.exists()


def test_inverse_adapter_dispatch_and_source_pin(runner, monkeypatch, capsys):
    import sys

    # A test double checks dispatch. The real FHVAL backend is exercised separately.
    backend = ModuleType("fhval.exact_inverse")
    calls = []

    @dataclass
    class Result:
        status: str
        determinant: object

    def evaluate(reference, rhs, candidate, determinant, inverse, solution):
        calls.append((reference, rhs, candidate, determinant, inverse, solution))
        status = "SINGULAR" if reference[0] == reference[1] else "REJECT"
        return Result(status, determinant)

    backend.check_inverse = evaluate
    monkeypatch.setitem(sys.modules, backend.__name__, backend)
    from nsrw import mb08_inverse_diagnostic as inverse

    source = b"synthetic source fixture"
    check = runner.CHECKS["mb08-inverse"]
    assert run_verification(check, {"source": source})["status"] == "FAIL"
    assert not calls
    monkeypatch.setattr(inverse, "SOURCE_SHA256", hashlib.sha256(source).hexdigest())
    report = run_verification(check, {"source": source})
    assert report["status"] == "FAIL"
    assert len(report["details"]["cases"]) == 9
    assert len(calls) == 9


def test_ratio_adapter_runs_tracked_record(runner):
    path = ROOT / "examples/research-verification/mb06-ratio-20261113.json"
    check = runner.CHECKS["mb06-ratio"]
    assert run_verification(check, {"record": path.read_bytes()})["status"] == "PASS"
    assert run_verification(check, {"record": b"{}"})["status"] == "FAIL"


@pytest.mark.parametrize(
    "arguments",
    [
        ["forced-shear", "--manifest", "manifest.json"],
        ["forced-shear", "--input", "broken"],
        ["forced-shear", "--input", "other=broken"],
    ],
)
def test_cli_rejects_invalid_arguments(runner, arguments):
    with pytest.raises(SystemExit) as raised:
        runner.main(arguments)
    assert raised.value.code == 2


@pytest.mark.parametrize(
    "text",
    [
        "'Test.example' depends on axioms: [propext]",
        "Test.example : True\n'Test.example' depends on axioms: [sorryAx]",
        "Test.example : True\n'Test.example' depends on axioms: [propext, propext]",
    ],
)
def test_lean_record_rejects_missing_signature_or_bad_axioms(text):
    with pytest.raises(ValueError):
        inspect_declarations(text, ("Test.example",), {"Test.example": ["propext"]})


def test_lean_report_rejects_archive_drift(runner):
    report = run_verification(runner.CHECKS["p1-lean-margin"], {"archive": b"replaced evidence"})
    assert report["status"] == "FAIL"
    assert "SHA-256" in report["details"]["reason"]


def test_lean_signature_digest_captures_hypothesis_changes():
    name = "Test.example"
    suffix = "\n  True\n'Test.example' depends on axioms: [propext]"
    args = ((name,), {name: ["propext"]})
    typed = inspect_declarations(name + " (hM : True) :" + suffix, *args)
    dropped = inspect_declarations(name + " :" + suffix, *args)
    assert typed[name]["signature_sha256"] != dropped[name]["signature_sha256"]


def test_consistent_repacked_archive_cannot_drop_a_pinned_hypothesis(runner):
    folder = ROOT / "colab/evidence/2026-10-22/p1-margin-final-admission-review"
    archive = folder / "nsrw-p1-margin-replay-20261021T181509633115Z-replay-evidence.zip"
    if not archive.is_file():
        pytest.skip("private P1 evidence archive is absent")
    pin = runner.P1_MARGIN
    assert len(check_lean_archive(archive.read_bytes(), pin)["declarations"]) == 10
    with zipfile.ZipFile(archive) as original:
        records = {name: original.read(name) for name in original.namelist()}
    stage = "P2_ZPLUS_J_QuantitativeMargin"
    log = f"{stage}.stdout.log"
    original_log = records[log]
    records[log] = original_log.replace(b" (hM : localMass F eta r = 0)", b"", 1)
    assert records[log] != original_log
    metadata = json.loads(records["replay-metadata.json"])
    metadata["stages"][stage]["stdout_sha256"] = hashlib.sha256(records[log]).hexdigest()
    metadata["stages"][stage]["stdout_bytes"] = len(records[log])
    records["replay-metadata.json"] = json.dumps(metadata).encode()
    repacked = io.BytesIO()
    with zipfile.ZipFile(repacked, "w") as bundle:
        for name, data in records.items():
            bundle.writestr(name, data)
    changed = repacked.getvalue()
    repinned = replace(pin, archive_sha256=hashlib.sha256(changed).hexdigest())
    with pytest.raises(ValueError, match="critical declaration signature differs"):
        check_lean_archive(changed, repinned)


def test_portable_lean_record_check_without_private_archive(runner):
    stage = "TestModule"
    declaration = "Test.result"
    axioms = ["propext"]
    signature = f"{declaration} (h : True) : True"
    stdout = f"{signature}\n'{declaration}' depends on axioms: [propext]\n".encode()
    identity = {"commit": runner.P1_MARGIN.execution_commit, "tracked_clean": True}
    source = {"commit": runner.P1_MARGIN.source_commit, "toolchain_file": runner.P1_MARGIN.toolchain}
    proof, artifact = b"example", b"synthetic artifact"
    def digest(raw):
        return hashlib.sha256(raw).hexdigest()

    metadata = {
        "pre_identity": identity, "post_identity": identity,
        "expected_nsrw_commit": identity["commit"],
        "pre_source_identity": source, "post_source_identity": source,
        "check_status": runner.P1_MARGIN.run_status,
        "claim_authority": "NONE", "claim_status": "UNVERIFIED",
        "inputs": {"TestModule.lean": digest(proof)},
        "fresh_artifacts": {"TestModule.olean": digest(artifact)},
        "axiom_surfaces": {declaration: axioms},
        "stages": {stage: {
            "exit": 0, "stdout_bytes": len(stdout), "stdout_sha256": digest(stdout),
            "stderr_bytes": 0, "stderr_sha256": digest(b""),
        }},
    }
    stream = io.BytesIO()
    with zipfile.ZipFile(stream, "w") as archive:
        archive.writestr("replay-metadata.json", json.dumps(metadata))
        archive.writestr("inputs/TestModule.lean", proof)
        archive.writestr("artifacts/TestModule.olean", artifact)
        archive.writestr(f"{stage}.stdout.log", stdout)
        archive.writestr(f"{stage}.stderr.log", b"")
    raw = stream.getvalue()
    pin = replace(
        runner.P1_MARGIN, archive_sha256=digest(raw), members=5,
        declarations={stage: (declaration,)},
        critical_signature_sha256={declaration: digest(signature.encode())},
    )
    result = check_lean_archive(raw, pin)
    assert result["declarations"][declaration]["axioms"] == axioms
    assert result["kernel_reexecuted"] is False


def test_checker_cannot_mutate_input_custody():
    original = {"operands": b"[2,3]", "result": b"5"}
    pristine = {key: value for key, value in original.items()}
    before = hashlib.sha256(original["result"]).hexdigest()

    def malicious(evidence):
        evidence["result"] = b"999"
        return Finding(Status.PASS, {"forged": True})

    report = run_verification(check(malicious), original)
    assert report["status"] == "ERROR"
    assert report["inputs"]["result"]["sha256"] == before
    assert original == pristine
    assert "TypeError" in report["details"]["reason"]


def test_checker_receives_only_pinned_immutable_bytes():
    def inspect(evidence):
        assert isinstance(evidence["result"], bytes)
        assert evidence["result"] == b"5"
        return Finding(Status.PASS, {"observed": True})

    before = {"operands": b"[2,3]", "result": b"5"}
    report = run_verification(check(inspect), before)
    assert report["status"] == "PASS"
    assert report["inputs"]["result"]["sha256"] == hashlib.sha256(b"5").hexdigest()


@pytest.mark.parametrize("value", ["5", bytearray(b"5"), None])
def test_non_bytes_evidence_fails_closed(value):
    def forbidden(_evidence):
        pytest.fail("non-byte evidence must not be checked")

    report = run_verification(check(forbidden), {"operands": b"[]", "result": value})
    assert report["status"] == "ERROR"
    assert report["claim_authority"] == "NONE"


def test_cli_unreadable_input_is_environment_blocked(runner, capsys, tmp_path, monkeypatch):
    fixture = tmp_path / "unreadable.json"
    fixture.write_text("{}", encoding="utf-8")
    original = Path.read_bytes

    def permission_denied(path):
        if path == fixture:
            raise PermissionError("SYNTHETIC_ACCESS_DENIED")
        return original(path)

    monkeypatch.setattr(Path, "read_bytes", permission_denied)
    assert runner.main(["forced-shear", "--input", f"fixture={fixture}"]) == 1
    report = json.loads(capsys.readouterr().out)
    assert report["status"] == "ENV_BLOCKED"
    assert "SYNTHETIC_ACCESS_DENIED" in report["details"]["environment_blocked_files"]["fixture"]
    assert report["claim_authority"] == "NONE"
