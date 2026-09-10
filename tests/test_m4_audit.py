from __future__ import annotations

import copy
import hashlib
import json
from pathlib import Path

import pytest

from nsrw.m4_audit import (
    REQUIRED_MUTATIONS,
    check_quantifier_custody,
    evaluate_obligation,
    inspect_spar_identity,
    load_manifest,
    run_m4_audit,
    run_mutations,
    run_spar_diagnostic,
    validate_manifest,
    verify_source_bindings,
)
from nsrw.m4_cli import main

ROOT = Path(__file__).resolve().parents[1]
MANIFEST = ROOT / "fixtures" / "m4-parametric-pilot-v1.json"


def fixture() -> dict:
    return json.loads(MANIFEST.read_text(encoding="utf-8"))


def obligation(family: str) -> dict:
    return next(item for item in fixture()["obligations"] if item["family"] == family)


def test_p0_manifest_and_quantifier_custody_pass():
    data = fixture()
    assert validate_manifest(data) == []
    assert all(check_quantifier_custody(item).check_status == "PASS" for item in data["obligations"])


@pytest.mark.parametrize(
    ("mutation", "fragment"),
    [
        (lambda data: data.update(schema_id="wrong"), "schema_id"),
        (lambda data: data.update(stage="M4-S"), "stage"),
        (lambda data: data.update(source_binding=[]), "source_binding"),
        (lambda data: data["source_binding"].update(formal_source_commit="bad"), "commit"),
        (lambda data: data["source_binding"].update(compiled_targets=[]), "compiled_targets"),
        (lambda data: data.update(obligations=[]), "non-empty"),
        (lambda data: data.update(required_mutations=[]), "mutation bank"),
    ],
)
def test_p0_invalid_top_level_contracts_fail(mutation, fragment):
    data = fixture()
    mutation(data)
    assert any(fragment in error for error in validate_manifest(data))


def test_p0_rejects_duplicate_and_malformed_obligations():
    data = fixture()
    data["obligations"].append(copy.deepcopy(data["obligations"][0]))
    broken = data["obligations"][0]
    broken["family"] = "UNKNOWN"
    broken["evidence_class"] = "UNKNOWN"
    broken["claimed_scope"] = "UNKNOWN"
    broken["constructibility"] = "UNKNOWN"
    broken["source_quantifiers"] = []
    broken["artifact_quantifiers"] = [{}]
    broken["assumptions"] = "not-a-list"
    broken["evaluator"] = None
    broken["source_locator"] = None
    errors = validate_manifest(data)
    assert len(errors) >= 9
    assert any("duplicate obligation_id" in error for error in errors)


def test_p0_rejects_missing_id_locator_fields_and_target_drift():
    data = fixture()
    item = data["obligations"][0]
    item["obligation_id"] = ""
    item["source_locator"] = {"sha256": "x" * 64}
    item["compiled_target"] = "wrong"
    errors = validate_manifest(data)
    assert any("obligation_id" in error for error in errors)
    assert any("incomplete" in error for error in errors)
    assert any("compiled_target" in error for error in errors)


def test_p0_rejects_invalid_compiled_target_records():
    data = fixture()
    targets = data["source_binding"]["compiled_targets"]
    targets["+NavierStokes.OutgoingDilation"]["receipt_sha256"] = "bad"
    targets["+NavierStokes.OutgoingCone"]["check_status"] = "UNKNOWN"
    targets["+NavierStokes.NominalConeAssembly"]["olean_sha256"] = "bad"
    targets[""] = []
    errors = validate_manifest(data)
    assert sum("compiled target" in error for error in errors) >= 3


def test_quantifier_promotion_rules_fail_closed():
    item = obligation("SUPPORT")
    item["claimed_scope"] = "SYMBOLIC_PARAMETRIC_IDENTITY"
    assert check_quantifier_custody(item).check_status == "FAIL"
    item["claimed_scope"] = "SOURCE_INSTANCE"
    assert check_quantifier_custody(item).check_status == "FAIL"
    item["claimed_scope"] = "SAMPLED_PARAMETRIC_DIAGNOSTIC"
    item["artifact_quantifiers"][0]["quantifier"] = "FORALL"
    assert check_quantifier_custody(item).check_status == "FAIL"
    item["artifact_quantifiers"] = []
    assert check_quantifier_custody(item).check_status == "FAIL"


def test_p1_support_positive_and_boundaries():
    assert evaluate_obligation(obligation("SUPPORT")).check_status == "PASS"
    for change in (
        lambda e: e.update(intervals=[]),
        lambda e: e["intervals"][1].update(lower=0.5),
        lambda e: e["intervals"][1].update(upper=9),
        lambda e: e["intervals"][0].update(lower=float("inf")),
        lambda e: e["intervals"].__setitem__(0, "bad"),
        lambda e: e["intervals"][0].update(lower="bad"),
    ):
        item = obligation("SUPPORT")
        change(item["evaluator"])
        assert evaluate_obligation(item).check_status == "FAIL"


def test_p2_cone_positive_margin_and_cycle_failures():
    assert evaluate_obligation(obligation("CONE")).check_status == "PASS"
    variants = []
    malformed = obligation("CONE")
    malformed["evaluator"]["inequalities"] = []
    variants.append(malformed)
    cyclic = obligation("CONE")
    cyclic["evaluator"]["threshold_dependencies"] = {"A": ["B"], "B": ["A"]}
    variants.append(cyclic)
    weak = obligation("CONE")
    weak["evaluator"]["inequalities"][0]["minimum_margin"] = 10
    variants.append(weak)
    relation = obligation("CONE")
    relation["evaluator"]["inequalities"][0]["relation"] = "EQ"
    variants.append(relation)
    nonfinite = obligation("CONE")
    nonfinite["evaluator"]["inequalities"][0]["lhs"] = float("nan")
    variants.append(nonfinite)
    bad_graph = obligation("CONE")
    bad_graph["evaluator"]["threshold_dependencies"] = {"A": "B"}
    variants.append(bad_graph)
    for item in variants:
        assert evaluate_obligation(item).check_status == "FAIL"


def test_p3_exact_moment_positive_and_failures():
    assert evaluate_obligation(obligation("MOMENT")).check_status == "PASS"
    bad = obligation("MOMENT")
    bad["evaluator"]["identities"][0]["terms"] = ["1/3", "-1/4"]
    assert evaluate_obligation(bad).check_status == "FAIL"
    malformed = obligation("MOMENT")
    malformed["evaluator"]["identities"][0]["terms"] = [0.5]
    assert evaluate_obligation(malformed).check_status == "FAIL"
    missing = obligation("MOMENT")
    missing["evaluator"]["identities"] = []
    assert evaluate_obligation(missing).check_status == "FAIL"


def test_dispatch_handles_falsification_missing_and_unknown():
    assert evaluate_obligation(obligation("FALSIFICATION")).check_status == "PASS"
    assert evaluate_obligation({"family": "SUPPORT"}).check_status == "FAIL"
    assert evaluate_obligation({"family": "UNKNOWN", "evaluator": {}}).check_status == "FAIL"


def _make_lean_root(tmp_path: Path, data: dict) -> Path:
    lean_root = tmp_path / "lean"
    for item in data["obligations"]:
        locator = item["source_locator"]
        path = lean_root / locator["relative_path"]
        path.parent.mkdir(parents=True, exist_ok=True)
        declaration = locator["declaration"]
        existing = path.read_text(encoding="utf-8") if path.exists() else ""
        path.write_text(existing + declaration + "\n", encoding="utf-8")
    for item in data["obligations"]:
        path = lean_root / item["source_locator"]["relative_path"]
        item["source_locator"]["sha256"] = hashlib.sha256(path.read_bytes()).hexdigest()
    return lean_root


def test_source_binding_verification(monkeypatch: pytest.MonkeyPatch, tmp_path: Path):
    data = fixture()
    lean_root = _make_lean_root(tmp_path, data)
    process = type("Process", (), {"returncode": 0, "stdout": data["source_binding"]["formal_source_commit"]})()
    monkeypatch.setattr("nsrw.m4_audit.subprocess.run", lambda *args, **kwargs: process)
    assert all(item.check_status == "PASS" for item in verify_source_bindings(data, lean_root))
    data["obligations"][0]["source_locator"]["sha256"] = "0" * 64
    assert any(item.check_status == "FAIL" for item in verify_source_bindings(data, lean_root))


def test_p4_all_required_mutations_are_killed():
    results = run_mutations(fixture())
    assert tuple(item.mutation_id for item in results) == REQUIRED_MUTATIONS
    assert all(item.killed for item in results)


def test_full_audit_passes_parametric_lane_and_holds_source_lane(
    monkeypatch: pytest.MonkeyPatch, tmp_path: Path
):
    data = fixture()
    for record in data["source_binding"]["compiled_targets"].values():
        record["check_status"] = "PASS"
    lean_root = _make_lean_root(tmp_path, data)
    process = type(
        "Process",
        (),
        {"returncode": 0, "stdout": data["source_binding"]["formal_source_commit"]},
    )()
    monkeypatch.setattr("nsrw.m4_audit.subprocess.run", lambda *args, **kwargs: process)
    monkeypatch.setattr(
        "nsrw.m4_audit.inspect_spar_identity",
        lambda expected_version="0.6.0": {"check_status": "PASS", "expected_version": expected_version},
    )
    receipt = run_m4_audit(data, lean_root)
    assert receipt["check_status"] == "PASS"
    assert receipt["lane_status"]["M4-P"] == "OPEN[PARAMETRIC_ONLY]"
    assert receipt["lane_status"]["M4-S"] == "HELD[NONCOMPUTABLE_SOURCE_INSTANCE]"
    assert receipt["spar_diagnostic"]["non_authority"]


def test_full_audit_fails_on_hard_gate():
    data = fixture()
    data["obligations"][0]["evaluator"]["intervals"][1]["lower"] = 0.5
    receipt = run_m4_audit(data)
    assert receipt["check_status"] == "FAIL"
    assert receipt["task_status"] == "HELD"


def test_target_specific_build_gate_holds_unbuilt_cone_and_moment():
    data = fixture()
    data["source_binding"]["compiled_targets"]["+NavierStokes.OutgoingCone"][
        "check_status"
    ] = "HELD"
    data["source_binding"]["compiled_targets"]["+NavierStokes.NominalConeAssembly"][
        "check_status"
    ] = "HELD"
    receipt = run_m4_audit(data)
    assert receipt["check_status"] == "FAIL"
    failed = [item["check_id"] for item in receipt["checks"] if item["check_status"] == "FAIL"]
    assert "M4P-CONE-001:compiled_target" in failed
    assert "M4P-MOMENT-001:compiled_target" in failed


def test_source_binding_cannot_be_skipped_for_an_authoritative_pass():
    data = fixture()
    for record in data["source_binding"]["compiled_targets"].values():
        record["check_status"] = "PASS"
    receipt = run_m4_audit(data)
    assert receipt["task_status"] == "HELD"
    assert any(
        item["check_id"] == "source_bindings" and item["check_status"] == "SKIPPED"
        for item in receipt["checks"]
    )


def test_spar_identity_is_explicit_and_diagnostic_cannot_override_failure():
    identity = inspect_spar_identity()
    assert identity["check_status"] in {"PASS", "FAIL", "ERROR"}
    result = run_spar_diagnostic([type("C", (), {"check_id": "x", "check_status": "FAIL", "detail": "bad", "critical": True})()])
    assert result["check_status"] == "FAIL"


def test_load_manifest_and_cli_output(monkeypatch: pytest.MonkeyPatch, tmp_path: Path):
    assert load_manifest(MANIFEST)["manifest_id"] == "nsrw-m4-parametric-pilot-v1"
    invalid = tmp_path / "invalid.json"
    invalid.write_text("[]", encoding="utf-8")
    with pytest.raises(ValueError):
        load_manifest(invalid)
    data = fixture()
    for record in data["source_binding"]["compiled_targets"].values():
        record["check_status"] = "PASS"
    runnable = tmp_path / "manifest.json"
    runnable.write_text(json.dumps(data), encoding="utf-8")
    output = tmp_path / "receipt.json"
    monkeypatch.setattr("sys.argv", ["nsrw-m4", str(runnable), "--output", str(output)])
    assert main() == 1
    assert json.loads(output.read_text(encoding="utf-8"))["stage"] == "M4-P"
