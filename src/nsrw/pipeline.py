"""Deterministic end-to-end research pipeline."""

from __future__ import annotations

import hashlib
import json
import shutil
from pathlib import Path
from typing import Any

from nsrw.contracts import load_contract
from nsrw.falsification import run_research_gate
from nsrw.graph import build_research_graph


def load_json(path: Path) -> dict[str, Any]:
    value = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise ValueError(f"JSON root must be an object: {path}")
    return value


def lean_toolchain_status() -> dict[str, Any]:
    tools = {name: shutil.which(name) for name in ("lake", "lean", "elan")}
    available = bool(tools["lake"] and tools["lean"])
    return {
        "status": "AVAILABLE" if available else "UNAVAILABLE",
        "tools": tools,
        "scope": "availability_only_not_build_execution",
    }


def _source_identity(contract: dict[str, Any]) -> list[dict[str, str]]:
    fields = ("source_id", "representation", "authority", "locator", "sha256", "git_commit")
    return [
        {field: str(source[field]) for field in fields if field in source}
        for source in contract.get("sources", [])
    ]


def _fingerprint(payload: dict[str, Any]) -> str:
    encoded = json.dumps(payload, sort_keys=True, separators=(",", ":"), ensure_ascii=False)
    return hashlib.sha256(encoded.encode("utf-8")).hexdigest().upper()


def _graph_summary(graph: Any, claim_id: str, graph_errors: list[str]) -> dict[str, Any]:
    return {
        "node_count": len(graph.nodes),
        "edge_count": len(graph.edges),
        "critical_path": [] if graph_errors else graph.critical_path(claim_id),
        "high_fan_in": [
            {"node_id": node_id, "incoming": count} for node_id, count in graph.high_fan_in()
        ],
    }


def _pipeline_checks(
    gate: dict[str, Any], graph_errors: list[str], toolchain: dict[str, Any]
) -> dict[str, str]:
    return {
        "contract_and_falsification_gate": (
            "PASS" if gate.get("stage_status") == "GREEN" else "FAIL"
        ),
        "proof_graph_integrity": "PASS" if not graph_errors else "FAIL",
        "lean_toolchain_availability": str(toolchain["status"]),
        "lean_build": "UNAVAILABLE",
        "semantic_alignment": "UNVERIFIED",
    }


def run_pipeline(
    contract_path: Path,
    graph_seed_path: Path,
    *,
    verify_sources: bool = True,
    full_output: bool = False,
) -> dict[str, Any]:
    contract = load_contract(contract_path)
    seed = load_json(graph_seed_path)
    gate_receipt = run_research_gate(contract, verify_sources=verify_sources).to_dict()
    graph, claim_id = build_research_graph(contract, gate_receipt, seed)
    graph_errors = graph.validate()
    claim_status = graph.effective_claim_status(claim_id)
    toolchain = lean_toolchain_status()
    checks = _pipeline_checks(gate_receipt, graph_errors, toolchain)
    pipeline_green = checks["contract_and_falsification_gate"] == "PASS" and not graph_errors
    core = {
        "schema_id": "flamehaven.navier-stokes-research-pipeline-receipt.v1",
        "pipeline_status": "GREEN" if pipeline_green else "HELD",
        "claim_status": claim_status,
        "research_id": contract["research_id"],
        "checks": checks,
        "source_identity": _source_identity(contract),
        "mutation_summary": gate_receipt["mutation_summary"],
        "graph_summary": _graph_summary(graph, claim_id, graph_errors),
        "unavailable_checks": ["lean_build", "paper_lean_semantic_equivalence"],
        "non_claims": list(contract["theorem"]["non_claims"]),
        "errors": [*gate_receipt["errors"], *graph_errors],
    }
    core["replay_fingerprint"] = _fingerprint(core)
    if full_output:
        core["gate_receipt"] = gate_receipt
        core["proof_graph"] = graph.to_dict()
        core["toolchain"] = toolchain
    return core


def render_receipt(receipt: dict[str, Any]) -> str:
    return json.dumps(receipt, indent=2, sort_keys=True, ensure_ascii=False) + "\n"
