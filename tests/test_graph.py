from __future__ import annotations

import json
from pathlib import Path

import pytest

from nsrw.graph import Edge, Node, ProofGraph, build_research_graph

ROOT = Path(__file__).resolve().parents[1]


def load(name: str) -> dict:
    return json.loads((ROOT / "fixtures" / name).read_text(encoding="utf-8"))


def built_graph() -> tuple[ProofGraph, str]:
    contract = load("navier-stokes-research-contract-v1.json")
    seed = load("navier-stokes-proof-graph-v1.json")
    gate = {
        "checks": {
            "source_hashes": "PASS",
            "lean_declaration_static_presence": "PASS",
            "lean_build": "UNAVAILABLE",
            "semantic_alignment": "UNVERIFIED",
        }
    }
    return build_research_graph(contract, gate, seed)


def test_missing_edge_endpoint_fails_closed():
    graph = ProofGraph()
    graph.add_node(Node("a", "CLAIM", "DERIVED", "UNVERIFIED"))
    with pytest.raises(ValueError, match="missing nodes"):
        graph.add_edge(Edge("a", "missing", "depends_on"))


def test_authority_cycle_is_rejected():
    graph = ProofGraph()
    graph.add_node(Node("a", "CLAIM", "DERIVED", "UNVERIFIED"))
    graph.add_node(Node("b", "PAPER_STATEMENT", "TRANSPORT", "MAPPED"))
    graph.add_edge(Edge("a", "b", "depends_on"))
    graph.add_edge(Edge("b", "a", "depends_on"))
    assert graph.validate() == ["authority/dependency cycle detected"]


def test_graph_is_valid_and_has_a_source_bound_critical_path():
    graph, claim_id = built_graph()
    assert graph.validate() == []
    path = graph.critical_path(claim_id)
    assert path[0] == "theorem:theorem_1_1"
    assert "paper:proposition_10_1" in path
    assert path[-1] == "paper:corollary_10_6"


def test_high_fan_in_finds_convergent_paper_node():
    graph, _ = built_graph()
    assert ("paper:proposition_8_3", 2) in graph.high_fan_in()


def test_static_presence_cannot_confirm_top_claim():
    graph, claim_id = built_graph()
    assert graph.effective_claim_status(claim_id) == "UNVERIFIED"


def test_all_required_authority_checks_can_confirm_only_the_graph_status():
    graph, claim_id = built_graph()
    for check_id in ("source_hashes", "lean_build", "semantic_alignment"):
        old = graph.nodes[f"check:{check_id}"]
        graph.nodes[old.node_id] = Node(
            old.node_id, old.kind, old.authority, "PASS", old.locator, old.metadata
        )
    assert graph.effective_claim_status(claim_id) == "CONFIRMED"


def test_failed_semantic_check_makes_claim_contested():
    graph, claim_id = built_graph()
    old = graph.nodes["check:semantic_alignment"]
    graph.nodes[old.node_id] = Node(
        old.node_id, old.kind, old.authority, "FAIL", old.locator, old.metadata
    )
    assert graph.effective_claim_status(claim_id) == "CONTESTED"


def test_taylor_green_negative_control_remains_falsified():
    contract = load("taylor-green-negative-control-v1.json")
    seed = {"nodes": [], "edges": []}
    graph, claim_id = build_research_graph(contract, {"checks": {}}, seed)
    assert graph.effective_claim_status(claim_id) == "FALSIFIED"


def test_graph_serialization_is_deterministic():
    graph, _ = built_graph()
    first = json.dumps(graph.to_dict(), sort_keys=True)
    second = json.dumps(graph.to_dict(), sort_keys=True)
    assert first == second
