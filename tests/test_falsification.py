from __future__ import annotations

import copy
import hashlib
import json
from pathlib import Path

import pytest

from nsrw.falsification import run_mutation_suite, run_research_gate, verify_paper_locators

ROOT = Path(__file__).resolve().parents[1]


def fixture() -> dict:
    return json.loads(
        (ROOT / "fixtures" / "navier-stokes-research-contract-v1.json").read_text(
            encoding="utf-8"
        )
    )


def portable_contract(tmp_path: Path) -> dict:
    data = fixture()
    paper = tmp_path / "paper.pdf"
    paper.write_bytes(b"paper")
    transport = tmp_path / "paper.md"
    transport.write_text("title\ntheorem statement\n", encoding="utf-8")
    formal = tmp_path / "formal"
    lean = formal / "NavierStokes" / "ComparatorSolution.lean"
    lean.parent.mkdir(parents=True)
    lean.write_text("theorem navier_stokes_breakdown_R3 : True := by trivial\n", encoding="utf-8")
    data["sources"] = [
        {
            "source_id": "paper_pdf",
            "representation": "primary_pdf",
            "authority": "PRIMARY",
            "locator": str(paper),
            "sha256": hashlib.sha256(paper.read_bytes()).hexdigest(),
        },
        {
            "source_id": "paper_markdown",
            "representation": "searchable_transport",
            "authority": "TRANSPORT",
            "locator": str(transport),
            "sha256": hashlib.sha256(transport.read_bytes()).hexdigest(),
        },
        {
            "source_id": "openai_lean",
            "representation": "formal_source",
            "authority": "FORMAL",
            "locator": str(formal),
            "git_commit": "2" * 40,
        },
    ]
    data["crosswalk"] = [
        {
            "paper_locator": "paper.md:2",
            "formal_source_id": "openai_lean",
            "lean_file": "NavierStokes/ComparatorSolution.lean",
            "declaration": "navier_stokes_breakdown_R3",
            "mapping_status": "PARTIAL",
        }
    ]
    return data


def mock_git(monkeypatch: pytest.MonkeyPatch) -> None:
    result = type("Process", (), {"returncode": 0, "stdout": "2" * 40})()
    monkeypatch.setattr("nsrw.contracts.subprocess.run", lambda *args, **kwargs: result)


def test_all_five_required_mutations_are_killed():
    results = run_mutation_suite(fixture())
    assert [result.mutation_id for result in results] == [
        "weakened_hypothesis",
        "missing_locator",
        "fake_confirmed",
        "wrong_bkm_quantity",
        "forced_to_unforced_scope",
    ]
    assert all(result.killed for result in results)


def test_positive_gate_is_green_but_claim_remains_unverified(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
):
    data = portable_contract(tmp_path)
    mock_git(monkeypatch)
    receipt = run_research_gate(data)
    assert receipt.stage_status == "GREEN"
    assert receipt.claim_status == "UNVERIFIED"
    assert receipt.checks["required_mutations_killed"] == "PASS"


def test_missing_or_blank_paper_locator_fails_closed(tmp_path: Path):
    data = portable_contract(tmp_path)
    data["crosswalk"][0]["paper_locator"] = "paper.md:3"
    ok, errors = verify_paper_locators(data)
    assert not ok
    assert errors


def test_gate_is_held_when_locator_does_not_resolve(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
):
    data = portable_contract(tmp_path)
    data["crosswalk"][0]["paper_locator"] = "paper.md:999"
    mock_git(monkeypatch)
    receipt = run_research_gate(data)
    assert receipt.stage_status == "HELD"
    assert receipt.checks["paper_locator_static_presence"] == "FAIL"


def test_surviving_mutation_holds_gate(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
):
    data = portable_contract(tmp_path)
    mock_git(monkeypatch)
    monkeypatch.setattr(
        "nsrw.falsification.run_mutation_suite",
        lambda contract: [
            type("Mutation", (), {"killed": False, "to_dict": lambda self: {}})()
        ],
    )
    receipt = run_research_gate(data)
    assert receipt.stage_status == "HELD"
    assert receipt.checks["required_mutations_killed"] == "FAIL"


def test_fake_green_base_contract_is_rejected(tmp_path: Path):
    data = portable_contract(tmp_path)
    data["theorem"]["claim_status"] = "CONFIRMED"
    receipt = run_research_gate(data, verify_sources=False, run_mutations=False)
    assert receipt.stage_status == "HELD"
    assert any("CONFIRMED requires PASS" in error for error in receipt.errors)


def test_scope_inflation_cannot_be_hidden_by_open_falsifier(tmp_path: Path):
    data = copy.deepcopy(portable_contract(tmp_path))
    data["theorem"]["formulation"] = "unforced_generic_blowup"
    receipt = run_research_gate(data, verify_sources=False, run_mutations=False)
    assert receipt.stage_status == "HELD"


def test_no_verify_mode_marks_source_and_locator_checks_skipped():
    receipt = run_research_gate(fixture(), verify_sources=False)
    assert receipt.stage_status == "GREEN"
    assert receipt.checks["source_bindings"] == "SKIPPED"
    assert receipt.checks["paper_locator_static_presence"] == "SKIPPED"
