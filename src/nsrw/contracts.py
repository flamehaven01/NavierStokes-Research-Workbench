"""Fail-closed Research Proof Contract v1 validation."""

from __future__ import annotations

import hashlib
import json
import re
import subprocess
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

SCHEMA_ID = "flamehaven.research-proof-contract.v1"
CONTRACT_VERSION = "1.0.0"
CLAIM_STATUSES = frozenset(
    {"CONFIRMED", "SUPPORTED", "HYPOTHESIS", "UNVERIFIED", "CONTESTED", "FALSIFIED"}
)
CHECK_STATUSES = frozenset({"PASS", "FAIL", "SKIPPED", "ERROR", "UNAVAILABLE", "UNVERIFIED"})
MAPPING_STATUSES = frozenset({"MAPPED", "PARTIAL", "UNVERIFIED"})
NAVIER_REQUIRED_HYPOTHESES = frozenset(
    {
        "smooth_divergence_free_initial_data",
        "smooth_compactly_supported_forcing",
        "forced_navier_stokes",
        "domain_R3_or_periodic",
    }
)
CONFIRMATION_CHECKS = frozenset({"source_hashes", "lean_build", "semantic_alignment"})


@dataclass
class ValidationReceipt:
    contract_id: str
    valid: bool = False
    claim_status: str = "UNVERIFIED"
    checks: dict[str, str] = field(default_factory=dict)
    errors: list[str] = field(default_factory=list)
    warnings: list[str] = field(default_factory=list)

    def to_dict(self) -> dict[str, Any]:
        return {
            "schema_id": "flamehaven.research-proof-validation-receipt.v1",
            "contract_id": self.contract_id,
            "valid": self.valid,
            "claim_status": self.claim_status,
            "checks": dict(sorted(self.checks.items())),
            "errors": self.errors,
            "warnings": self.warnings,
        }


def load_contract(path: Path) -> dict[str, Any]:
    data = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(data, dict):
        raise ValueError("contract root must be a JSON object")
    return data


def file_sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest().upper()


def _validate_source_pins(
    source_id: str, source: dict[str, Any], receipt: ValidationReceipt
) -> None:
    if not source.get("locator"):
        receipt.errors.append(f"source {source_id}: locator is required")
    sha256 = source.get("sha256")
    if sha256 is not None and not re.fullmatch(r"[0-9A-Fa-f]{64}", str(sha256)):
        receipt.errors.append(f"source {source_id}: invalid sha256")
    commit = source.get("git_commit")
    if commit is not None and not re.fullmatch(r"[0-9A-Fa-f]{40}", str(commit)):
        receipt.errors.append(f"source {source_id}: invalid git_commit")


def _validate_source_record(
    source: object,
    index: int,
    source_map: dict[str, dict[str, Any]],
    authorities: set[str],
    receipt: ValidationReceipt,
) -> None:
    if not isinstance(source, dict):
        receipt.errors.append(f"sources[{index}] must be an object")
        return
    source_id = source.get("source_id")
    if not isinstance(source_id, str) or not source_id:
        receipt.errors.append(f"sources[{index}].source_id is required")
        return
    if source_id in source_map:
        receipt.errors.append(f"duplicate source_id: {source_id}")
        return
    source_map[source_id] = source
    authority = source.get("authority")
    authorities.add(str(authority))
    authority_for = {
        "primary_pdf": "PRIMARY",
        "searchable_transport": "TRANSPORT",
        "formal_source": "FORMAL",
        "derived_summary": "DERIVED",
    }
    if authority_for.get(str(source.get("representation"))) != authority:
        receipt.errors.append(f"source {source_id}: representation/authority mismatch")
    _validate_source_pins(source_id, source, receipt)


def _validate_sources(sources: object, receipt: ValidationReceipt) -> dict[str, dict[str, Any]]:
    if not isinstance(sources, list) or not sources:
        receipt.errors.append("sources must be a non-empty list")
        return {}
    source_map: dict[str, dict[str, Any]] = {}
    authorities: set[str] = set()
    for index, source in enumerate(sources):
        _validate_source_record(source, index, source_map, authorities, receipt)
    for required in ("PRIMARY", "FORMAL"):
        if required not in authorities:
            receipt.errors.append(f"at least one {required} source is required")
    return source_map


def _validate_theorem(contract: dict[str, Any], receipt: ValidationReceipt) -> None:
    theorem = contract.get("theorem")
    required = {
        "theorem_id",
        "problem_id",
        "formulation",
        "claim_status",
        "hypotheses",
        "conclusion",
        "bkm_quantity",
        "non_claims",
    }
    if not isinstance(theorem, dict):
        receipt.errors.append("theorem must be an object")
        return
    missing = sorted(required - set(theorem))
    if missing:
        receipt.errors.append(f"theorem missing fields: {', '.join(missing)}")
    status = theorem.get("claim_status")
    if status not in CLAIM_STATUSES:
        receipt.errors.append(f"invalid theorem.claim_status: {status}")
    hypotheses = theorem.get("hypotheses")
    if not isinstance(hypotheses, list):
        receipt.errors.append("theorem.hypotheses must be a list")
        hypotheses = []
    if theorem.get("problem_id") == "navier_stokes_clay":
        missing_hypotheses = sorted(NAVIER_REQUIRED_HYPOTHESES - set(hypotheses))
        if missing_hypotheses:
            receipt.errors.append(
                "Navier-Stokes contract missing hypotheses: " + ", ".join(missing_hypotheses)
            )
        if theorem.get("formulation") != "forced_clay_C_or_D":
            receipt.errors.append("Navier-Stokes formulation must remain forced_clay_C_or_D")
        if "unforced_global_regular_or_blowup" not in theorem.get("non_claims", []):
            receipt.errors.append("unforced Navier-Stokes must be an explicit non-claim")
        if theorem.get("bkm_quantity") != "time_integral_vorticity_Linf":
            receipt.errors.append("BKM quantity must be time_integral_vorticity_Linf")


def _validate_crosswalk(crosswalk: object, source_map: dict[str, dict[str, Any]], receipt: ValidationReceipt) -> None:
    if not isinstance(crosswalk, list):
        receipt.errors.append("crosswalk must be a list")
        return
    for index, item in enumerate(crosswalk):
        if not isinstance(item, dict):
            receipt.errors.append(f"crosswalk[{index}] must be an object")
            continue
        for name in ("paper_locator", "formal_source_id", "lean_file", "declaration"):
            if not item.get(name):
                receipt.errors.append(f"crosswalk[{index}].{name} is required")
        if item.get("formal_source_id") not in source_map:
            receipt.errors.append(f"crosswalk[{index}] references an unknown formal source")
        if item.get("mapping_status") not in MAPPING_STATUSES:
            receipt.errors.append(f"crosswalk[{index}].mapping_status is invalid")


def _validate_check_statuses(contract: dict[str, Any], receipt: ValidationReceipt) -> dict[str, str]:
    checks = contract.get("checks")
    if not isinstance(checks, dict):
        receipt.errors.append("checks must be an object")
        return {}
    for check_id, status in checks.items():
        if status not in CHECK_STATUSES:
            receipt.errors.append(f"invalid check status {check_id}={status}")
    return checks


def _blocking_falsifiers(contract: dict[str, Any], receipt: ValidationReceipt) -> list[dict[str, Any]]:
    falsifiers = contract.get("falsifiers")
    if not isinstance(falsifiers, list):
        receipt.errors.append("falsifiers must be a list")
        return []
    return [
        item
        for item in falsifiers
        if isinstance(item, dict) and item.get("blocking") is True and item.get("status") == "TRIGGERED"
    ]


def _validate_claim_gate(
    claim_status: str,
    checks: dict[str, str],
    triggered: list[dict[str, Any]],
    receipt: ValidationReceipt,
) -> None:
    if claim_status != "CONFIRMED":
        return
    receipt.errors.append(
        "CONFIRMED cannot be self-attested by contract checks; independent executable receipts are required"
    )
    absent = sorted(name for name in CONFIRMATION_CHECKS if checks.get(name) != "PASS")
    if absent:
        receipt.errors.append("CONFIRMED requires PASS checks: " + ", ".join(absent))
    if triggered:
        receipt.errors.append("CONFIRMED is impossible with a triggered blocking falsifier")


def _validate_negative_control(
    contract: dict[str, Any], triggered: list[dict[str, Any]], receipt: ValidationReceipt
) -> None:
    if contract.get("control_type") != "NEGATIVE_CONTROL":
        return
    if receipt.claim_status != "FALSIFIED":
        receipt.errors.append("NEGATIVE_CONTROL claim_status must be FALSIFIED")
    if not triggered:
        receipt.errors.append("NEGATIVE_CONTROL requires a triggered blocking falsifier")


def _validate_checks_and_falsifiers(contract: dict[str, Any], receipt: ValidationReceipt) -> None:
    checks = _validate_check_statuses(contract, receipt)
    triggered = _blocking_falsifiers(contract, receipt)
    _validate_claim_gate(receipt.claim_status, checks, triggered, receipt)
    _validate_negative_control(contract, triggered, receipt)


def _verify_formal_source(source_id: str, source: dict[str, Any], receipt: ValidationReceipt) -> bool:
    locator = Path(source["locator"])
    expected = source.get("git_commit")
    if not locator.is_dir() or not expected:
        receipt.errors.append(f"formal source unavailable or unpinned: {source_id}")
        return False
    proc = subprocess.run(
        ["git", "-C", str(locator), "rev-parse", "HEAD"],
        capture_output=True,
        text=True,
        check=False,
    )
    actual = proc.stdout.strip()
    if proc.returncode == 0 and actual.lower() == str(expected).lower():
        return True
    receipt.errors.append(
        f"formal source commit mismatch for {source_id}: expected {expected}, got {actual or 'UNAVAILABLE'}"
    )
    return False


def _verify_file_source(source_id: str, source: dict[str, Any], receipt: ValidationReceipt) -> bool:
    locator = Path(source["locator"])
    expected = source.get("sha256")
    if not locator.is_file() or not expected:
        receipt.errors.append(f"source file unavailable or unpinned: {source_id}")
        return False
    actual = file_sha256(locator)
    if actual == str(expected).upper():
        return True
    receipt.errors.append(f"source hash mismatch for {source_id}: expected {expected}, got {actual}")
    return False


def _verify_source(source_id: str, source: dict[str, Any], receipt: ValidationReceipt) -> bool:
    if source.get("representation") == "formal_source":
        return _verify_formal_source(source_id, source, receipt)
    return _verify_file_source(source_id, source, receipt)


def _verify_lean_item(
    item: dict[str, Any], source_map: dict[str, dict[str, Any]], receipt: ValidationReceipt
) -> bool:
    formal = source_map.get(item.get("formal_source_id", ""))
    if not formal:
        return False
    lean_path = Path(formal["locator"]) / item["lean_file"]
    if not lean_path.is_file():
        receipt.errors.append(f"Lean locator missing: {lean_path}")
        return False
    text = lean_path.read_text(encoding="utf-8")
    declaration = re.escape(str(item["declaration"]))
    if re.search(rf"\b(?:theorem|def|structure|lemma)\s+{declaration}\b", text):
        return True
    receipt.errors.append(f"Lean declaration not found: {item['declaration']} in {item['lean_file']}")
    return False


def _verify_bound_sources(
    contract: dict[str, Any], source_map: dict[str, dict[str, Any]], receipt: ValidationReceipt
) -> None:
    source_results = [_verify_source(source_id, source, receipt) for source_id, source in source_map.items()]
    receipt.checks["source_bindings"] = "PASS" if all(source_results) else "FAIL"
    lean_results = [_verify_lean_item(item, source_map, receipt) for item in contract.get("crosswalk", [])]
    receipt.checks["lean_declaration_static_presence"] = "PASS" if all(lean_results) else "FAIL"
    receipt.warnings.append(
        "Static Lean declaration presence does not establish Lean build success or semantic equivalence."
    )


def validate_contract(contract: dict[str, Any], *, verify_sources: bool = False) -> ValidationReceipt:
    theorem = contract.get("theorem") if isinstance(contract, dict) else None
    claim_status = theorem.get("claim_status", "UNVERIFIED") if isinstance(theorem, dict) else "UNVERIFIED"
    receipt = ValidationReceipt(str(contract.get("research_id", "UNKNOWN")), claim_status=str(claim_status))
    required = {
        "schema_id",
        "contract_version",
        "research_id",
        "control_type",
        "sources",
        "theorem",
        "crosswalk",
        "checks",
        "falsifiers",
    }
    missing = sorted(required - set(contract))
    if missing:
        receipt.errors.append(f"missing top-level fields: {', '.join(missing)}")
    if contract.get("schema_id") != SCHEMA_ID:
        receipt.errors.append(f"schema_id must be {SCHEMA_ID}")
    if contract.get("contract_version") != CONTRACT_VERSION:
        receipt.errors.append(f"contract_version must be {CONTRACT_VERSION}")
    if contract.get("control_type") not in {"PRIMARY_CASE", "NEGATIVE_CONTROL"}:
        receipt.errors.append("control_type must be PRIMARY_CASE or NEGATIVE_CONTROL")
    source_map = _validate_sources(contract.get("sources"), receipt)
    _validate_theorem(contract, receipt)
    _validate_crosswalk(contract.get("crosswalk"), source_map, receipt)
    _validate_checks_and_falsifiers(contract, receipt)
    receipt.checks["contract_semantics"] = "PASS" if not receipt.errors else "FAIL"
    if verify_sources and not receipt.errors:
        _verify_bound_sources(contract, source_map, receipt)
    else:
        receipt.checks["source_bindings"] = "SKIPPED"
        receipt.checks["lean_declaration_static_presence"] = "SKIPPED"
    receipt.valid = not receipt.errors and all(status != "FAIL" for status in receipt.checks.values())
    return receipt
