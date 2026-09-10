from __future__ import annotations

import copy
import hashlib
import json
from pathlib import Path

import pytest

from nsrw import contracts

ROOT = Path(__file__).resolve().parents[1]


def fixture(name: str) -> dict:
    return json.loads((ROOT / "fixtures" / name).read_text(encoding="utf-8"))


def portable_contract(tmp_path: Path) -> dict:
    paper = tmp_path / "paper.pdf"
    paper.write_bytes(b"bounded source")
    formal = tmp_path / "formal"
    lean = formal / "NavierStokes" / "ComparatorSolution.lean"
    lean.parent.mkdir(parents=True)
    lean.write_text("theorem navier_stokes_breakdown_R3 : True := by trivial\n", encoding="utf-8")
    data = fixture("navier-stokes-research-contract-v1.json")
    data["sources"] = [
        {
            "source_id": "paper_pdf",
            "representation": "primary_pdf",
            "authority": "PRIMARY",
            "locator": str(paper),
            "sha256": hashlib.sha256(paper.read_bytes()).hexdigest(),
        },
        {
            "source_id": "openai_lean",
            "representation": "formal_source",
            "authority": "FORMAL",
            "locator": str(formal),
            "git_commit": "1" * 40,
        },
    ]
    data["crosswalk"] = [
        {
            "paper_locator": "paper.pdf:1",
            "formal_source_id": "openai_lean",
            "lean_file": "NavierStokes/ComparatorSolution.lean",
            "declaration": "navier_stokes_breakdown_R3",
            "mapping_status": "PARTIAL",
        }
    ]
    return data


def mock_git(monkeypatch: pytest.MonkeyPatch, commit: str = "1" * 40) -> None:
    result = type("Process", (), {"returncode": 0, "stdout": commit})()
    monkeypatch.setattr(contracts.subprocess, "run", lambda *args, **kwargs: result)


def test_primary_fixture_is_valid_without_inflating_claim():
    receipt = contracts.validate_contract(fixture("navier-stokes-research-contract-v1.json"))
    assert receipt.valid
    assert receipt.claim_status == "UNVERIFIED"
    assert receipt.checks["source_bindings"] == "SKIPPED"


def test_negative_control_is_valid_but_falsified():
    receipt = contracts.validate_contract(fixture("taylor-green-negative-control-v1.json"))
    assert receipt.valid
    assert receipt.claim_status == "FALSIFIED"


def test_missing_source_fails_closed(tmp_path: Path, monkeypatch: pytest.MonkeyPatch):
    data = portable_contract(tmp_path)
    data["sources"][0]["locator"] = str(tmp_path / "missing.pdf")
    mock_git(monkeypatch)
    receipt = contracts.validate_contract(data, verify_sources=True)
    assert not receipt.valid
    assert receipt.checks["source_bindings"] == "FAIL"


def test_hash_mismatch_fails_closed(tmp_path: Path, monkeypatch: pytest.MonkeyPatch):
    data = portable_contract(tmp_path)
    data["sources"][0]["sha256"] = "0" * 64
    mock_git(monkeypatch)
    receipt = contracts.validate_contract(data, verify_sources=True)
    assert not receipt.valid
    assert any("hash mismatch" in error for error in receipt.errors)


def test_static_declaration_presence_is_narrowly_labeled(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
):
    data = portable_contract(tmp_path)
    mock_git(monkeypatch)
    receipt = contracts.validate_contract(data, verify_sources=True)
    assert receipt.valid
    assert receipt.checks["lean_declaration_static_presence"] == "PASS"
    assert any("does not establish Lean build" in warning for warning in receipt.warnings)


def test_fake_confirmed_status_is_rejected():
    data = fixture("navier-stokes-research-contract-v1.json")
    data["theorem"]["claim_status"] = "CONFIRMED"
    receipt = contracts.validate_contract(data)
    assert not receipt.valid
    assert "lean_build" in " ".join(receipt.errors)


def test_all_pass_contract_cannot_self_attest_confirmation():
    data = fixture("navier-stokes-research-contract-v1.json")
    data["theorem"]["claim_status"] = "CONFIRMED"
    data["checks"]["lean_build"] = "PASS"
    data["checks"]["semantic_alignment"] = "PASS"
    receipt = contracts.validate_contract(data)
    assert not receipt.valid
    assert any("cannot be self-attested" in error for error in receipt.errors)


@pytest.mark.parametrize(
    ("mutation", "expected"),
    [
        ("weaken_hypothesis", "missing hypotheses"),
        ("wrong_bkm", "BKM quantity"),
        ("inflate_scope", "forced_clay_C_or_D"),
    ],
)
def test_core_mutations_are_killed(mutation: str, expected: str):
    data = copy.deepcopy(fixture("navier-stokes-research-contract-v1.json"))
    if mutation == "weaken_hypothesis":
        data["theorem"]["hypotheses"].remove("smooth_compactly_supported_forcing")
    elif mutation == "wrong_bkm":
        data["theorem"]["bkm_quantity"] = "terminal_vorticity_Linf"
    else:
        data["theorem"]["formulation"] = "unforced_generic_blowup"
    receipt = contracts.validate_contract(data)
    assert not receipt.valid
    assert expected in " ".join(receipt.errors)


def test_non_object_json_is_rejected(tmp_path: Path):
    path = tmp_path / "list.json"
    path.write_text("[]", encoding="utf-8")
    with pytest.raises(ValueError, match="root must be a JSON object"):
        contracts.load_contract(path)


def test_malformed_contract_accumulates_bounded_errors():
    data = fixture("navier-stokes-research-contract-v1.json")
    data["schema_id"] = "wrong"
    data["contract_version"] = "0"
    data["control_type"] = "UNKNOWN"
    data["sources"][0]["authority"] = "DERIVED"
    data["sources"][0]["sha256"] = "short"
    data["sources"].append(copy.deepcopy(data["sources"][0]))
    data["checks"]["invented"] = "GREEN"
    receipt = contracts.validate_contract(data)
    joined = " ".join(receipt.errors)
    assert not receipt.valid
    assert "schema_id" in joined
    assert "duplicate source_id" in joined
    assert "invalid check status" in joined


def test_formal_commit_mismatch_fails_closed(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
):
    data = portable_contract(tmp_path)
    result = type("Process", (), {"returncode": 0, "stdout": "9" * 40})()
    monkeypatch.setattr(contracts.subprocess, "run", lambda *args, **kwargs: result)
    receipt = contracts.validate_contract(data, verify_sources=True)
    assert not receipt.valid
    assert any("commit mismatch" in error for error in receipt.errors)


def test_missing_lean_declaration_fails_closed(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
):
    data = portable_contract(tmp_path)
    data["crosswalk"][0]["declaration"] = "invented_declaration"
    mock_git(monkeypatch)
    receipt = contracts.validate_contract(data, verify_sources=True)
    assert not receipt.valid
    assert receipt.checks["lean_declaration_static_presence"] == "FAIL"
