"""Executable falsification gate for Research Proof Contract v1."""

from __future__ import annotations

import copy
import re
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Callable

from nsrw.contracts import ValidationReceipt, validate_contract

Mutation = Callable[[dict[str, Any]], None]


@dataclass(frozen=True)
class MutationResult:
    mutation_id: str
    killed: bool
    errors: tuple[str, ...]

    def to_dict(self) -> dict[str, Any]:
        return {"mutation_id": self.mutation_id, "killed": self.killed, "errors": list(self.errors)}


@dataclass
class ResearchGateReceipt:
    research_id: str
    stage_status: str
    claim_status: str
    checks: dict[str, str] = field(default_factory=dict)
    mutation_results: list[MutationResult] = field(default_factory=list)
    errors: list[str] = field(default_factory=list)
    non_claims: list[str] = field(default_factory=list)

    def to_dict(self) -> dict[str, Any]:
        return {
            "schema_id": "flamehaven.research-falsification-receipt.v1",
            "research_id": self.research_id,
            "stage_status": self.stage_status,
            "claim_status": self.claim_status,
            "checks": dict(sorted(self.checks.items())),
            "mutation_summary": {
                "total": len(self.mutation_results),
                "killed": sum(result.killed for result in self.mutation_results),
            },
            "mutation_results": [result.to_dict() for result in self.mutation_results],
            "errors": self.errors,
            "non_claims": self.non_claims,
        }


def _weaken_hypothesis(contract: dict[str, Any]) -> None:
    hypotheses = contract["theorem"]["hypotheses"]
    hypotheses.remove("smooth_compactly_supported_forcing")


def _remove_locator(contract: dict[str, Any]) -> None:
    contract["crosswalk"][0]["paper_locator"] = ""


def _fake_confirmation(contract: dict[str, Any]) -> None:
    contract["theorem"]["claim_status"] = "CONFIRMED"


def _wrong_bkm(contract: dict[str, Any]) -> None:
    contract["theorem"]["bkm_quantity"] = "terminal_vorticity_Linf"


def _inflate_scope(contract: dict[str, Any]) -> None:
    contract["theorem"]["formulation"] = "unforced_generic_blowup"


MUTATIONS: tuple[tuple[str, Mutation], ...] = (
    ("weakened_hypothesis", _weaken_hypothesis),
    ("missing_locator", _remove_locator),
    ("fake_confirmed", _fake_confirmation),
    ("wrong_bkm_quantity", _wrong_bkm),
    ("forced_to_unforced_scope", _inflate_scope),
)


def run_mutation_suite(contract: dict[str, Any]) -> list[MutationResult]:
    results: list[MutationResult] = []
    for mutation_id, mutate in MUTATIONS:
        candidate = copy.deepcopy(contract)
        mutate(candidate)
        receipt = validate_contract(candidate)
        results.append(MutationResult(mutation_id, not receipt.valid, tuple(receipt.errors)))
    return results


def _transport_source(contract: dict[str, Any]) -> dict[str, Any] | None:
    for source in contract.get("sources", []):
        if source.get("representation") == "searchable_transport":
            return source
    return None


def _paper_locator_ok(locator: str, transport: dict[str, Any]) -> bool:
    match = re.fullmatch(r"(.+):(\d+)", locator)
    if not match:
        return False
    expected_name, line_text = match.groups()
    path = Path(transport["locator"])
    if path.name != expected_name or not path.is_file():
        return False
    line_number = int(line_text)
    if line_number < 1:
        return False
    lines = path.read_text(encoding="utf-8").splitlines()
    return line_number <= len(lines) and bool(lines[line_number - 1].strip())


def verify_paper_locators(contract: dict[str, Any]) -> tuple[bool, list[str]]:
    transport = _transport_source(contract)
    crosswalk = contract.get("crosswalk", [])
    if not crosswalk:
        return True, []
    if transport is None:
        return False, ["searchable transport source is required for paper locators"]
    errors = [
        f"invalid paper locator: {item.get('paper_locator', '')}"
        for item in crosswalk
        if not _paper_locator_ok(str(item.get("paper_locator", "")), transport)
    ]
    return not errors, errors


def _base_checks(validation: ValidationReceipt, locator_status: str) -> dict[str, str]:
    return {
        "contract_semantics": validation.checks.get("contract_semantics", "ERROR"),
        "source_bindings": validation.checks.get("source_bindings", "SKIPPED"),
        "lean_declaration_static_presence": validation.checks.get(
            "lean_declaration_static_presence", "SKIPPED"
        ),
        "paper_locator_static_presence": locator_status,
    }


def run_research_gate(
    contract: dict[str, Any], *, verify_sources: bool = True, run_mutations: bool = True
) -> ResearchGateReceipt:
    validation = validate_contract(contract, verify_sources=verify_sources)
    if verify_sources:
        locators_ok, locator_errors = verify_paper_locators(contract)
        locator_status = "PASS" if locators_ok else "FAIL"
    else:
        locators_ok, locator_errors = True, []
        locator_status = "SKIPPED"
    should_mutate = run_mutations and contract.get("control_type") == "PRIMARY_CASE"
    mutation_results = run_mutation_suite(contract) if should_mutate else []
    mutations_ok = all(result.killed for result in mutation_results)
    checks = _base_checks(validation, locator_status)
    checks["required_mutations_killed"] = "PASS" if mutations_ok else "FAIL"
    errors = [*validation.errors, *locator_errors]
    if not mutations_ok:
        errors.append("one or more required mutations survived")
    stage_green = validation.valid and locators_ok and mutations_ok
    theorem = contract.get("theorem", {})
    return ResearchGateReceipt(
        research_id=str(contract.get("research_id", "UNKNOWN")),
        stage_status="GREEN" if stage_green else "HELD",
        claim_status=str(theorem.get("claim_status", "UNVERIFIED")),
        checks=checks,
        mutation_results=mutation_results,
        errors=errors,
        non_claims=list(theorem.get("non_claims", [])),
    )
