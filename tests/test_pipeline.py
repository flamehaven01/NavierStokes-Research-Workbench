from __future__ import annotations

import json
from pathlib import Path

from nsrw import cli
from nsrw.pipeline import render_receipt, run_pipeline

ROOT = Path(__file__).resolve().parents[1]
CONTRACT = ROOT / "fixtures" / "navier-stokes-research-contract-v1.json"
GRAPH = ROOT / "fixtures" / "navier-stokes-proof-graph-v1.json"


def test_end_to_end_positive_fixture_is_green_but_not_a_proof(monkeypatch):
    monkeypatch.setattr("nsrw.pipeline.shutil.which", lambda name: None)
    receipt = run_pipeline(CONTRACT, GRAPH, verify_sources=False)
    assert receipt["pipeline_status"] == "GREEN"
    assert receipt["claim_status"] == "UNVERIFIED"
    assert receipt["checks"]["lean_toolchain_availability"] == "UNAVAILABLE"
    assert "unforced_global_regular_or_blowup" in receipt["non_claims"]


def test_replay_is_byte_deterministic(monkeypatch):
    monkeypatch.setattr("nsrw.pipeline.shutil.which", lambda name: None)
    first = render_receipt(run_pipeline(CONTRACT, GRAPH, verify_sources=False, full_output=True))
    second = render_receipt(run_pipeline(CONTRACT, GRAPH, verify_sources=False, full_output=True))
    assert first == second


def test_compact_and_full_output_boundaries(monkeypatch):
    monkeypatch.setattr("nsrw.pipeline.shutil.which", lambda name: None)
    compact = run_pipeline(CONTRACT, GRAPH, verify_sources=False)
    full = run_pipeline(CONTRACT, GRAPH, verify_sources=False, full_output=True)
    assert "proof_graph" not in compact
    assert "gate_receipt" not in compact
    assert full["proof_graph"]["nodes"]
    assert full["gate_receipt"]["mutation_summary"] == {"total": 5, "killed": 5}


def test_wrong_source_hash_holds_pipeline(tmp_path: Path, monkeypatch):
    data = json.loads(CONTRACT.read_text(encoding="utf-8"))
    data["sources"][0]["sha256"] = "0" * 64
    mutated = tmp_path / "wrong-hash.json"
    mutated.write_text(json.dumps(data), encoding="utf-8")
    monkeypatch.setattr("nsrw.pipeline.shutil.which", lambda name: None)
    receipt = run_pipeline(mutated, GRAPH)
    assert receipt["pipeline_status"] == "HELD"
    assert receipt["checks"]["contract_and_falsification_gate"] == "FAIL"


def test_cycle_holds_pipeline(tmp_path: Path, monkeypatch):
    seed = json.loads(GRAPH.read_text(encoding="utf-8"))
    seed["edges"].append(
        {
            "source": "paper:corollary_10_6",
            "target": "theorem:theorem_1_1",
            "relation": "depends_on",
        }
    )
    mutated = tmp_path / "cycle.json"
    mutated.write_text(json.dumps(seed), encoding="utf-8")
    monkeypatch.setattr("nsrw.pipeline.shutil.which", lambda name: None)
    receipt = run_pipeline(CONTRACT, mutated, verify_sources=False)
    assert receipt["pipeline_status"] == "HELD"
    assert "authority/dependency cycle detected" in receipt["errors"]


def test_cli_writes_same_receipt_it_prints(tmp_path: Path, capsys, monkeypatch):
    output = tmp_path / "receipt.json"
    monkeypatch.setattr("nsrw.pipeline.shutil.which", lambda name: None)
    exit_code = cli.main(["--no-verify-sources", "--output", str(output)])
    assert exit_code == 0
    assert output.read_text(encoding="utf-8") == capsys.readouterr().out


def test_cli_malformed_input_fails_closed(tmp_path: Path, capsys):
    malformed = tmp_path / "bad.json"
    malformed.write_text("not-json", encoding="utf-8")
    exit_code = cli.main(["--contract", str(malformed)])
    payload = json.loads(capsys.readouterr().out)
    assert exit_code == 1
    assert payload["pipeline_status"] == "HELD"
    assert payload["checks"] == {"pipeline_execution": "ERROR"}


def test_negative_control_does_not_run_primary_mutations():
    negative = json.loads(
        (ROOT / "fixtures" / "taylor-green-negative-control-v1.json").read_text(
            encoding="utf-8"
        )
    )
    from nsrw.falsification import run_research_gate

    receipt = run_research_gate(negative, verify_sources=False)
    assert receipt.claim_status == "FALSIFIED"
    assert receipt.mutation_results == []


def test_forged_all_pass_contract_cannot_confirm_pipeline(tmp_path: Path, monkeypatch):
    data = json.loads(CONTRACT.read_text(encoding="utf-8"))
    data["theorem"]["claim_status"] = "CONFIRMED"
    data["checks"].update({"lean_build": "PASS", "semantic_alignment": "PASS"})
    forged = tmp_path / "forged.json"
    forged.write_text(json.dumps(data), encoding="utf-8")
    monkeypatch.setattr("nsrw.pipeline.shutil.which", lambda name: None)
    receipt = run_pipeline(forged, GRAPH, verify_sources=False)
    assert receipt["pipeline_status"] == "HELD"
    assert receipt["claim_status"] == "CONTESTED"
