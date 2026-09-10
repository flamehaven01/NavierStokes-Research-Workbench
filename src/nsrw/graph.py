"""Typed, authority-aware paper-to-formal-proof graph."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Iterable

NODE_KINDS = frozenset({"SOURCE", "CLAIM", "PAPER_STATEMENT", "LEAN_DECLARATION", "CHECK", "FALSIFIER"})
RELATIONS = frozenset({"depends_on", "formalizes", "checked_by", "contradicted_by", "supersedes"})
ACYCLIC_RELATIONS = frozenset({"depends_on", "formalizes", "checked_by", "supersedes"})
REQUIRED_CONFIRMATION_CHECKS = frozenset({"source_hashes", "lean_build", "semantic_alignment"})


@dataclass(frozen=True)
class Node:
    node_id: str
    kind: str
    authority: str
    status: str
    locator: str = ""
    metadata: dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        return {
            "node_id": self.node_id,
            "kind": self.kind,
            "authority": self.authority,
            "status": self.status,
            "locator": self.locator,
            "metadata": self.metadata,
        }


@dataclass(frozen=True)
class Edge:
    source: str
    target: str
    relation: str

    def to_dict(self) -> dict[str, str]:
        return {"source": self.source, "target": self.target, "relation": self.relation}


class ProofGraph:
    def __init__(self) -> None:
        self.nodes: dict[str, Node] = {}
        self.edges: list[Edge] = []

    def add_node(self, node: Node) -> None:
        if node.kind not in NODE_KINDS:
            raise ValueError(f"unsupported node kind: {node.kind}")
        if node.node_id in self.nodes:
            raise ValueError(f"duplicate node: {node.node_id}")
        self.nodes[node.node_id] = node

    def add_edge(self, edge: Edge) -> None:
        if edge.relation not in RELATIONS:
            raise ValueError(f"unsupported relation: {edge.relation}")
        missing = [node_id for node_id in (edge.source, edge.target) if node_id not in self.nodes]
        if missing:
            raise ValueError("edge references missing nodes: " + ", ".join(missing))
        self.edges.append(edge)

    def outgoing(self, node_id: str, relations: Iterable[str] | None = None) -> list[Edge]:
        allowed = set(relations) if relations is not None else RELATIONS
        return [edge for edge in self.edges if edge.source == node_id and edge.relation in allowed]

    def incoming(self, node_id: str, relations: Iterable[str] | None = None) -> list[Edge]:
        allowed = set(relations) if relations is not None else RELATIONS
        return [edge for edge in self.edges if edge.target == node_id and edge.relation in allowed]

    def validate(self) -> list[str]:
        errors: list[str] = []
        for edge in self.edges:
            if edge.source not in self.nodes or edge.target not in self.nodes:
                errors.append(f"missing endpoint for {edge.source}->{edge.target}")
        if self._has_authority_cycle():
            errors.append("authority/dependency cycle detected")
        return errors

    def _has_authority_cycle(self) -> bool:
        visiting: set[str] = set()
        visited: set[str] = set()

        def visit(node_id: str) -> bool:
            if node_id in visiting:
                return True
            if node_id in visited:
                return False
            visiting.add(node_id)
            for edge in self.outgoing(node_id, ACYCLIC_RELATIONS):
                if visit(edge.target):
                    return True
            visiting.remove(node_id)
            visited.add(node_id)
            return False

        return any(visit(node_id) for node_id in self.nodes if node_id not in visited)

    def critical_path(self, root: str) -> list[str]:
        if root not in self.nodes:
            raise KeyError(root)

        def longest(node_id: str, trail: frozenset[str]) -> list[str]:
            if node_id in trail:
                raise ValueError("cycle encountered while finding critical path")
            children = self.outgoing(node_id, {"depends_on", "formalizes"})
            if not children:
                return [node_id]
            options = [longest(edge.target, trail | {node_id}) for edge in children]
            return [node_id, *max(options, key=len)]

        return longest(root, frozenset())

    def high_fan_in(self, minimum: int = 2) -> list[tuple[str, int]]:
        counts = [
            (node_id, len(self.incoming(node_id, {"depends_on", "formalizes"})))
            for node_id in self.nodes
        ]
        return sorted(
            [(node_id, count) for node_id, count in counts if count >= minimum],
            key=lambda item: (-item[1], item[0]),
        )

    def effective_claim_status(self, claim_id: str) -> str:
        claim = self.nodes[claim_id]
        if claim.kind != "CLAIM":
            raise ValueError(f"not a claim node: {claim_id}")
        if claim.status == "FALSIFIED":
            return "FALSIFIED"
        check_nodes = [self.nodes[edge.target] for edge in self.outgoing(claim_id, {"checked_by"})]
        statuses = {str(node.metadata.get("check_id")): node.status for node in check_nodes}
        if any(status == "FAIL" for status in statuses.values()):
            return "CONTESTED"
        confirmed = all(statuses.get(check_id) == "PASS" for check_id in REQUIRED_CONFIRMATION_CHECKS)
        return "CONFIRMED" if confirmed else "UNVERIFIED"

    def to_dict(self) -> dict[str, Any]:
        return {
            "schema_id": "flamehaven.research-proof-graph.v1",
            "nodes": [self.nodes[node_id].to_dict() for node_id in sorted(self.nodes)],
            "edges": [edge.to_dict() for edge in sorted(self.edges, key=lambda e: (e.source, e.target, e.relation))],
        }


def _add_contract_nodes(graph: ProofGraph, contract: dict[str, Any]) -> str:
    for source in contract.get("sources", []):
        graph.add_node(
            Node(
                node_id=f"source:{source['source_id']}",
                kind="SOURCE",
                authority=str(source["authority"]),
                status="PINNED",
                locator=str(source["locator"]),
            )
        )
    theorem = contract["theorem"]
    claim_id = f"theorem:{theorem['theorem_id']}"
    graph.add_node(
        Node(
            node_id=claim_id,
            kind="CLAIM",
            authority="DERIVED",
            status=str(theorem["claim_status"]),
            metadata={"formulation": theorem["formulation"]},
        )
    )
    for source in contract.get("sources", []):
        graph.add_edge(Edge(claim_id, f"source:{source['source_id']}", "depends_on"))
    return claim_id


def _add_seed(graph: ProofGraph, seed: dict[str, Any]) -> None:
    for item in seed.get("nodes", []):
        graph.add_node(Node(**item))
    for item in seed.get("edges", []):
        graph.add_edge(Edge(**item))


def _add_crosswalk(graph: ProofGraph, contract: dict[str, Any]) -> None:
    for item in contract.get("crosswalk", []):
        paper_id = f"paper:{item['paper_locator'].split(':')[-1]}"
        if paper_id not in graph.nodes:
            paper_id = next(
                (
                    node_id
                    for node_id, node in graph.nodes.items()
                    if node.kind == "PAPER_STATEMENT" and node.locator == item["paper_locator"]
                ),
                paper_id,
            )
        lean_id = f"lean:{item['declaration']}"
        graph.add_node(
            Node(
                lean_id,
                "LEAN_DECLARATION",
                "FORMAL",
                str(item["mapping_status"]),
                f"{item['lean_file']}::{item['declaration']}",
            )
        )
        if paper_id not in graph.nodes:
            graph.add_node(Node(paper_id, "PAPER_STATEMENT", "TRANSPORT", "UNVERIFIED", item["paper_locator"]))
        graph.add_edge(Edge(lean_id, paper_id, "formalizes"))


def _add_checks(graph: ProofGraph, claim_id: str, checks: dict[str, str]) -> None:
    for check_id, status in checks.items():
        node_id = f"check:{check_id}"
        graph.add_node(Node(node_id, "CHECK", "EXECUTABLE", status, metadata={"check_id": check_id}))
        graph.add_edge(Edge(claim_id, node_id, "checked_by"))


def _add_falsifiers(graph: ProofGraph, claim_id: str, contract: dict[str, Any]) -> None:
    for item in contract.get("falsifiers", []):
        node_id = f"falsifier:{item['falsifier_id']}"
        graph.add_node(
            Node(
                node_id,
                "FALSIFIER",
                "DERIVED",
                str(item["status"]),
                metadata={"blocking": bool(item["blocking"]), "condition": item["condition"]},
            )
        )
        graph.add_edge(Edge(claim_id, node_id, "contradicted_by"))


def build_research_graph(
    contract: dict[str, Any], gate_receipt: dict[str, Any], seed: dict[str, Any]
) -> tuple[ProofGraph, str]:
    graph = ProofGraph()
    claim_id = _add_contract_nodes(graph, contract)
    _add_seed(graph, seed)
    _add_crosswalk(graph, contract)
    executable_checks = dict(gate_receipt.get("checks", {}))
    if "source_bindings" in executable_checks:
        executable_checks["source_hashes"] = executable_checks["source_bindings"]
    executable_checks.setdefault("lean_build", "UNAVAILABLE")
    executable_checks.setdefault("semantic_alignment", "UNVERIFIED")
    _add_checks(graph, claim_id, executable_checks)
    _add_falsifiers(graph, claim_id, contract)
    return graph, claim_id
