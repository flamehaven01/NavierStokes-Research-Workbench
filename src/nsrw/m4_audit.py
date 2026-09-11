"""M4 parametric obligation audit with fail-closed claim custody.

The numerical evaluators below test declared fixtures.  They do not construct the
noncomputable source witness and do not prove the quantified Lean statements.
"""

from __future__ import annotations

import copy
import hashlib
import importlib.metadata
import json
import subprocess
from dataclasses import asdict, dataclass
from fractions import Fraction
from math import isfinite
from pathlib import Path
from typing import Any, Callable, cast

SCHEMA_ID = "flamehaven.nsrw-m4-obligation-manifest.v2"
COMPILED_EVIDENCE_SCHEMA_ID = "flamehaven.nsrw-lean-compiled-evidence.v1"
FAMILIES = frozenset({"SUPPORT", "CONE", "MOMENT", "FALSIFICATION"})
EVIDENCE_CLASSES = frozenset(
    {"FINITE_GRID", "EXACT_SYMBOLIC", "COMPILED_TARGET", "MANUFACTURED_FALSIFIER"}
)
CLAIM_SCOPES = frozenset(
    {"SAMPLED_PARAMETRIC_DIAGNOSTIC", "SYMBOLIC_PARAMETRIC_IDENTITY", "SOURCE_INSTANCE"}
)
CONSTRUCTIBILITY = frozenset(
    {
        "EXPLICIT",
        "DERIVED_COMPUTABLE",
        "EXISTENTIAL__NO_PINNED_NUMERICAL_EVALUATOR",
        "EXISTENTIAL_NONCOMPUTABLE_IN_CURRENT_SOURCE_INTERFACE",
    }
)
REQUIRED_MUTATIONS = (
    "swap_quantifier_order",
    "drop_required_assumption",
    "finite_grid_to_symbolic",
    "parametric_to_source_instance",
    "malformed_source_hash",
    "compiled_target_drift",
)
EXPECTED_MUTATION_DETECTORS = {
    "swap_quantifier_order": "M4P-CONE-001:quantifier_custody",
    "drop_required_assumption": "manifest_contract",
    "finite_grid_to_symbolic": "M4P-SUPPORT-001:quantifier_custody",
    "parametric_to_source_instance": "M4P-SUPPORT-001:quantifier_custody",
    "malformed_source_hash": "manifest_contract",
    "compiled_target_drift": "manifest_contract",
}
SOURCE_QUANTIFIER_PROJECTION = "NAMED_BINDERS_AND_DATA_EXISTENTIALS"


class Serializable:
    def as_dict(self) -> dict[str, object]:
        return asdict(self)


@dataclass(frozen=True)
class Check(Serializable):
    check_id: str
    check_status: str
    detail: str
    critical: bool = True

@dataclass(frozen=True)
class MutationResult(Serializable):
    mutation_id: str
    killed: bool
    reasons: tuple[str, ...]

def _is_sha256(value: object) -> bool:
    return isinstance(value, str) and len(value) == 64 and all(
        character in "0123456789abcdefABCDEF" for character in value
    )


def _canonical_source_sha256(path: Path) -> str:
    """Hash source bytes after the sole portable transform CRLF -> LF."""

    canonical_bytes = path.read_bytes().replace(b"\r\n", b"\n")
    return hashlib.sha256(canonical_bytes).hexdigest().upper()


def _quantifier_signature(items: object) -> tuple[tuple[str, str], ...] | None:
    if not isinstance(items, list) or not items:
        return None
    signature: list[tuple[str, str]] = []
    for item in items:
        if not isinstance(item, dict):
            return None
        quantifier = item.get("quantifier")
        binder = item.get("binder")
        if quantifier not in {"FORALL", "EXISTS", "ONE_FIXTURE", "FINITE_GRID", "DECLARED"}:
            return None
        if not isinstance(binder, str) or not binder:
            return None
        signature.append((quantifier, binder))
    return tuple(signature)


def _valid_relative_path(value: object) -> bool:
    if not isinstance(value, str) or not value:
        return False
    path = Path(value)
    return not path.is_absolute() and ".." not in path.parts


def _has_bound_compiled_fields(record: dict[str, Any]) -> bool:
    return all(
        (
            _valid_relative_path(record.get("receipt_path")),
            _is_sha256(record.get("receipt_sha256")),
            _is_sha256(record.get("olean_sha256")),
        )
    )


def _valid_compiled_record_header(target: object, record: object) -> bool:
    return all((isinstance(target, str), bool(target), isinstance(record, dict)))


def _validate_optional_hash(
    target: str,
    label: str,
    value: object,
    errors: list[str],
) -> None:
    if value is not None and not _is_sha256(value):
        errors.append(f"compiled target {target} {label} sha256 is invalid")


def _validate_compiled_target(target: object, record: object, errors: list[str]) -> None:
    if not _valid_compiled_record_header(target, record):
        errors.append("compiled target record is invalid")
        return
    assert isinstance(target, str) and isinstance(record, dict)
    status = record.get("check_status")
    if status not in {"PASS", "HELD"}:
        errors.append(f"compiled target {target} has an invalid status")
    _validate_optional_hash(target, "receipt", record.get("receipt_sha256"), errors)
    _validate_optional_hash(target, "olean", record.get("olean_sha256"), errors)
    receipt_path = record.get("receipt_path")
    if receipt_path is not None and not _valid_relative_path(receipt_path):
        errors.append(f"compiled target {target} receipt path is invalid")
    if status == "PASS" and not _has_bound_compiled_fields(record):
        errors.append(f"compiled target {target} PASS lacks bound receipt evidence")


def _validate_source_binding(binding: object, errors: list[str]) -> dict[str, Any]:
    if not isinstance(binding, dict):
        errors.append("source_binding must be an object")
        binding = {}
    commit = binding.get("formal_source_commit")
    if (
        not isinstance(commit, str)
        or len(commit) != 40
        or any(character not in "0123456789abcdefABCDEF" for character in commit)
    ):
        errors.append("formal source commit is invalid")
    toolchain = binding.get("formal_source_toolchain")
    if not isinstance(toolchain, str) or not toolchain:
        errors.append("formal source toolchain is invalid")
    targets = binding.get("compiled_targets")
    if not isinstance(targets, dict) or not targets:
        errors.append("source_binding.compiled_targets must be a non-empty object")
        targets = {}
    for target, record in targets.items():
        _validate_compiled_target(target, record, errors)
    return targets


def _validate_assumptions(prefix: str, obligation: dict[str, Any], errors: list[str]) -> None:
    assumptions = obligation.get("assumptions")
    evaluator = obligation.get("evaluator")
    if not isinstance(assumptions, list) or not all(
        isinstance(item, str) and item for item in assumptions
    ):
        errors.append(f"{prefix}.assumptions is invalid")
        assumptions = []
    if not isinstance(evaluator, dict):
        errors.append(f"{prefix}.evaluator must be an object")
        evaluator = {}
    required = evaluator.get("required_assumptions", [])
    if not isinstance(required, list) or not set(required).issubset(set(assumptions)):
        errors.append(f"{prefix} is missing an evaluator-required assumption")


def _validate_locator(prefix: str, locator: object, errors: list[str]) -> None:
    if not isinstance(locator, dict):
        errors.append(f"{prefix}.source_locator must be an object")
        return
    relative_path = locator.get("relative_path")
    if not relative_path or not locator.get("declaration"):
        errors.append(f"{prefix}.source_locator is incomplete")
    elif not _valid_relative_path(relative_path):
        errors.append(f"{prefix}.source_locator.relative_path is invalid")
    if not _is_sha256(locator.get("sha256")):
        errors.append(f"{prefix}.source_locator.sha256 is invalid")
    if not _is_sha256(locator.get("signature_sha256")):
        errors.append(f"{prefix}.source_locator.signature_sha256 is invalid")
    if locator.get("quantifier_projection") != SOURCE_QUANTIFIER_PROJECTION:
        errors.append(f"{prefix}.source_locator.quantifier_projection is invalid")


def _validate_source_quantifiers(prefix: str, items: object, errors: list[str]) -> None:
    if not isinstance(items, list):
        return
    for item in items:
        if (
            not isinstance(item, dict)
            or item.get("quantifier") not in {"FORALL", "EXISTS"}
            or not isinstance(item.get("source_fragment"), str)
            or not item["source_fragment"]
        ):
            errors.append(f"{prefix}.source_quantifiers require ordered source_fragment bindings")
            return


def _validate_obligation(
    index: int,
    obligation: object,
    targets: dict[str, Any],
    seen: set[str],
    errors: list[str],
) -> None:
    prefix = f"obligations[{index}]"
    if not isinstance(obligation, dict):
        errors.append(f"{prefix} must be an object")
        return
    obligation_id = obligation.get("obligation_id")
    if not isinstance(obligation_id, str) or not obligation_id:
        errors.append(f"{prefix}.obligation_id is required")
    elif obligation_id in seen:
        errors.append(f"duplicate obligation_id: {obligation_id}")
    else:
        seen.add(obligation_id)
    value_sets = (
        ("family", FAMILIES),
        ("evidence_class", EVIDENCE_CLASSES),
        ("claimed_scope", CLAIM_SCOPES),
        ("constructibility", CONSTRUCTIBILITY),
    )
    for field, allowed in value_sets:
        if obligation.get(field) not in allowed:
            errors.append(f"{prefix}.{field} is invalid")
    for field in ("source_quantifiers", "artifact_quantifiers"):
        if _quantifier_signature(obligation.get(field)) is None:
            errors.append(f"{prefix}.{field} is invalid")
    _validate_source_quantifiers(prefix, obligation.get("source_quantifiers"), errors)
    _validate_assumptions(prefix, obligation, errors)
    _validate_locator(prefix, obligation.get("source_locator"), errors)
    if obligation.get("compiled_target") not in targets:
        errors.append(f"{prefix}.compiled_target has no source-binding record")


def validate_manifest(manifest: dict[str, Any]) -> list[str]:
    """Validate the portable P0 contract without claiming source freshness."""

    errors: list[str] = []
    if manifest.get("schema_id") != SCHEMA_ID:
        errors.append(f"schema_id must be {SCHEMA_ID}")
    if manifest.get("stage") != "M4-P":
        errors.append("stage must be M4-P")
    targets = _validate_source_binding(manifest.get("source_binding"), errors)

    obligations = manifest.get("obligations")
    if not isinstance(obligations, list) or not obligations:
        errors.append("obligations must be a non-empty list")
        return errors
    seen: set[str] = set()
    for index, obligation in enumerate(obligations):
        _validate_obligation(index, obligation, targets, seen, errors)
    configured = manifest.get("required_mutations")
    if configured != list(REQUIRED_MUTATIONS):
        errors.append("required_mutations must exactly match the M4-P mutation bank")
    return errors


def _quantifier_scope_error(
    obligation: dict[str, Any],
    source: tuple[tuple[str, str], ...],
    artifact: tuple[tuple[str, str], ...],
) -> str | None:
    evidence = obligation.get("evidence_class")
    scope = obligation.get("claimed_scope")
    constructibility = obligation.get("constructibility")
    if evidence == "FINITE_GRID" and scope != "SAMPLED_PARAMETRIC_DIAGNOSTIC":
        return "finite-grid evidence was promoted beyond sampled scope"
    if scope == "SOURCE_INSTANCE" and constructibility.startswith("EXISTENTIAL"):
        return "source-instance claim has no pinned numerical evaluator"
    if scope == "SYMBOLIC_PARAMETRIC_IDENTITY" and source != artifact:
        return "symbolic claim changed the source quantifier prefix"
    if scope == "SAMPLED_PARAMETRIC_DIAGNOSTIC":
        allowed = {"ONE_FIXTURE", "FINITE_GRID", "DECLARED"}
        if any(quantifier not in allowed for quantifier, _ in artifact):
            return "sampled artifact contains a universal/existential claim"
    return None


def check_quantifier_custody(obligation: dict[str, Any]) -> Check:
    source = _quantifier_signature(obligation.get("source_quantifiers"))
    artifact = _quantifier_signature(obligation.get("artifact_quantifiers"))
    if source is None or artifact is None:
        return Check("quantifier_custody", "FAIL", "quantifier signature is invalid")
    error = _quantifier_scope_error(obligation, source, artifact)
    if error:
        return Check("quantifier_custody", "FAIL", error)
    return Check("quantifier_custody", "PASS", "executable scope does not exceed the declared claim scope")


def _fraction(value: object) -> Fraction:
    if not isinstance(value, (str, int)):
        raise ValueError("exact moment values must be integer or rational strings")
    return Fraction(value)


def _support_interval_error(interval: object, cutoff: float, previous: float) -> tuple[str | None, float]:
    if not isinstance(interval, dict):
        return "support interval is not an object", previous
    lower, upper = interval.get("lower"), interval.get("upper")
    if not isinstance(lower, (int, float)) or not isinstance(upper, (int, float)):
        return "support bounds must be numeric", previous
    if not all(isfinite(float(item)) for item in (lower, upper, cutoff)):
        return "support bounds must be finite", previous
    if lower < previous or lower > upper or upper > cutoff:
        return "support ordering, inclusion, or cutoff failed", previous
    return None, float(upper)


def _evaluate_support(evaluator: dict[str, Any]) -> Check:
    intervals = evaluator.get("intervals")
    cutoff = evaluator.get("cutoff")
    if not isinstance(intervals, list) or not intervals or not isinstance(cutoff, (int, float)):
        return Check("support", "FAIL", "support evaluator requires intervals and cutoff")
    previous = float("-inf")
    for interval in intervals:
        error, previous = _support_interval_error(interval, float(cutoff), previous)
        if error:
            return Check("support", "FAIL", error)
    return Check("support", "PASS", "declared support intervals are ordered and lie below the cutoff")


def _dependency_shape_error(graph: dict[str, object]) -> str | None:
    nodes = set(graph)
    for node, dependencies in graph.items():
        if not isinstance(node, str) or not node:
            return "threshold dependency graph has an invalid node"
        if not isinstance(dependencies, list) or any(
            not isinstance(item, str) or not item for item in dependencies
        ):
            return "threshold dependency graph is malformed"
        if any(item not in nodes for item in dependencies):
            return "threshold dependency graph has a dangling dependency"
    return None


def _has_dependency_cycle(graph: dict[str, list[str]]) -> bool:

    visiting: set[str] = set()
    visited: set[str] = set()

    def visit(node: str) -> bool:
        if node in visiting:
            return True
        if node in visited:
            return False
        visiting.add(node)
        if any(visit(item) for item in graph[node]):
            return True
        visiting.remove(node)
        visited.add(node)
        return False

    return any(visit(node) for node in graph)


def _dependency_graph_error(graph: dict[str, object]) -> str | None:
    if shape_error := _dependency_shape_error(graph):
        return shape_error
    valid_graph = cast(dict[str, list[str]], graph)
    if _has_dependency_cycle(valid_graph):
        return "threshold dependency graph is cyclic"
    return None


def _cone_margin(item: object) -> tuple[float | None, str | None]:
    if not isinstance(item, dict):
        return None, "cone inequality is malformed"
    lhs, rhs, minimum = item.get("lhs"), item.get("rhs"), item.get("minimum_margin", 0)
    relation = item.get("relation")
    if relation not in {"LE", "GE"}:
        return None, "cone relation must be LE or GE"
    if not all(isinstance(value, (int, float)) for value in (lhs, rhs, minimum)):
        return None, "cone values must be numeric"
    if not all(isfinite(float(value)) for value in (lhs, rhs, minimum)):
        return None, "cone values must be finite"
    margin = float(rhs - lhs) if relation == "LE" else float(lhs - rhs)
    if margin < float(minimum):
        return None, "a cone inequality lacks its declared margin"
    return margin, None


def _evaluate_cone(evaluator: dict[str, Any]) -> Check:
    inequalities = evaluator.get("inequalities")
    graph = evaluator.get("threshold_dependencies", {})
    if not isinstance(inequalities, list) or not inequalities or not isinstance(graph, dict):
        return Check("cone", "FAIL", "cone evaluator requires inequalities and a dependency graph")
    if graph_error := _dependency_graph_error(graph):
        return Check("cone", "FAIL", graph_error)
    margins: list[float] = []
    for item in inequalities:
        margin, error = _cone_margin(item)
        if error:
            return Check("cone", "FAIL", error)
        assert margin is not None
        margins.append(margin)
    return Check("cone", "PASS", f"cone inequalities pass; minimum observed margin={min(margins):.12g}")


def _evaluate_moment(evaluator: dict[str, Any]) -> Check:
    identities = evaluator.get("identities")
    if not isinstance(identities, list) or not identities:
        return Check("moment", "FAIL", "moment evaluator requires exact identities")
    try:
        for identity in identities:
            terms = identity["terms"]
            expected = _fraction(identity["expected"])
            if not isinstance(terms, list) or sum((_fraction(term) for term in terms), Fraction()) != expected:
                return Check("moment", "FAIL", "an exact moment or cancellation identity failed")
    except (KeyError, TypeError, ValueError, ZeroDivisionError):
        return Check("moment", "FAIL", "moment identity is malformed")
    return Check("moment", "PASS", "all declared moment identities hold in exact rational arithmetic")


def evaluate_obligation(obligation: dict[str, Any]) -> Check:
    evaluator = obligation.get("evaluator")
    if not isinstance(evaluator, dict):
        return Check("evaluator", "FAIL", "evaluator is missing")
    family = obligation.get("family")
    dispatch: dict[str, Callable[[dict[str, Any]], Check]] = {
        "SUPPORT": _evaluate_support,
        "CONE": _evaluate_cone,
        "MOMENT": _evaluate_moment,
    }
    if family == "FALSIFICATION":
        return Check("falsification_fixture", "PASS", "mutation execution is evaluated by the manifest gate")
    function = dispatch.get(str(family))
    return function(evaluator) if function else Check("evaluator", "FAIL", "unsupported family")


def _normalized_declaration_signature(text: str, declaration: str) -> str | None:
    start = text.find(declaration)
    if start < 0:
        return None
    tail = text[start:]
    endings = [
        position
        for marker in (":= by", " where")
        if (position := tail.find(marker)) >= 0
    ]
    if not endings:
        return None
    return " ".join(tail[: min(endings)].split())


def _source_fragments_are_ordered(signature: str, obligation: dict[str, Any]) -> bool:
    cursor = 0
    for item in obligation.get("source_quantifiers", []):
        fragment = " ".join(str(item.get("source_fragment", "")).split())
        position = signature.find(fragment, cursor)
        if not fragment or position < 0:
            return False
        cursor = position + len(fragment)
    return True


def _verify_source_obligation(obligation: dict[str, Any], lean_root: Path) -> list[Check]:
    locator = obligation.get("source_locator", {})
    path = lean_root / str(locator.get("relative_path", ""))
    actual = _canonical_source_sha256(path) if path.is_file() else ""
    expected = str(locator.get("sha256", "")).upper()
    declaration = str(locator.get("declaration", ""))
    text = path.read_text(encoding="utf-8") if path.is_file() else ""
    locator_ok = actual == expected and declaration in text
    obligation_id = obligation.get("obligation_id", "UNKNOWN")
    locator_check = Check(
        f"source_locator:{obligation_id}",
        "PASS" if locator_ok else "FAIL",
        (
            "LF-canonicalized source bytes and declaration match"
            if locator_ok
            else "source locator, hash, or declaration mismatch"
        ),
    )
    signature = _normalized_declaration_signature(text, declaration)
    actual_signature_hash = (
        hashlib.sha256(signature.encode("utf-8")).hexdigest().upper()
        if signature is not None
        else ""
    )
    signature_ok = all(
        (
            locator_ok,
            actual_signature_hash == str(locator.get("signature_sha256", "")).upper(),
            signature is not None,
            signature is not None and _source_fragments_are_ordered(signature, obligation),
        )
    )
    signature_check = Check(
        f"source_quantifier_binding:{obligation_id}",
        "PASS" if signature_ok else "FAIL",
        (
            "normalized declaration signature and ordered quantifier fragments match"
            if signature_ok
            else "declaration signature hash or ordered quantifier fragments mismatch"
        ),
    )
    return [locator_check, signature_check]


def verify_source_bindings(manifest: dict[str, Any], lean_root: Path) -> list[Check]:
    """Verify current source identity and locator bytes; this is not semantic equivalence."""

    binding = manifest.get("source_binding", {})
    process = subprocess.run(
        ["git", "-C", str(lean_root), "rev-parse", "HEAD"],
        capture_output=True,
        text=True,
        check=False,
    )
    expected_commit = str(binding.get("formal_source_commit", ""))
    commit_ok = process.returncode == 0 and process.stdout.strip().lower() == expected_commit.lower()
    checks = [
        Check(
            "formal_source_commit",
            "PASS" if commit_ok else "FAIL",
            "formal source commit matches the manifest" if commit_ok else "formal source commit mismatch",
        )
    ]
    for obligation in manifest.get("obligations", []):
        checks.extend(_verify_source_obligation(obligation, lean_root))
    return checks


def _safe_evidence_path(evidence_root: Path, relative_path: str) -> Path | None:
    root = evidence_root.resolve()
    candidate = (root / relative_path).resolve()
    try:
        candidate.relative_to(root)
    except ValueError:
        return None
    return candidate


def _read_compiled_receipt(
    record: dict[str, Any], evidence_root: Path
) -> tuple[dict[str, Any] | None, str | None]:
    path = _safe_evidence_path(evidence_root, str(record.get("receipt_path", "")))
    if path is None or not path.is_file():
        return None, "compiled receipt path is missing or escapes evidence root"
    actual_hash = hashlib.sha256(path.read_bytes()).hexdigest().upper()
    if actual_hash != str(record.get("receipt_sha256", "")).upper():
        return None, "compiled receipt sha256 mismatch"
    try:
        receipt = json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError:
        return None, "compiled receipt is not valid JSON"
    if not isinstance(receipt, dict):
        return None, "compiled receipt root is not an object"
    return receipt, None


def _compiled_receipt_matches(
    receipt: dict[str, Any],
    binding: dict[str, Any],
    target: str,
    record: dict[str, Any],
) -> bool:
    targets = receipt.get("targets")
    if not isinstance(targets, dict) or not isinstance(targets.get(target), dict):
        return False
    target_evidence = targets[target]
    expected = {
        "schema_id": COMPILED_EVIDENCE_SCHEMA_ID,
        "formal_source_commit": binding.get("formal_source_commit"),
        "toolchain": binding.get("formal_source_toolchain"),
        "target": target,
        "exit_code": 0,
        "olean_path": ".lake/build/lib/lean/"
        + target.removeprefix("+").replace(".", "/")
        + ".olean",
        "olean_sha256": str(record.get("olean_sha256", "")).upper(),
    }
    actual = {
        "schema_id": receipt.get("schema_id"),
        "formal_source_commit": receipt.get("formal_source_commit"),
        "toolchain": receipt.get("toolchain"),
        "target": target_evidence.get("target"),
        "exit_code": target_evidence.get("exit_code"),
        "olean_path": target_evidence.get("olean_path"),
        "olean_sha256": str(target_evidence.get("olean_sha256", "")).upper(),
    }
    return actual == expected and _is_sha256(target_evidence.get("dependency_surface_sha256"))


def _compiled_target_evidence_check(
    target: str,
    record: dict[str, Any],
    binding: dict[str, Any],
    evidence_root: Path | None,
) -> Check:
    check_id = f"compiled_receipt:{target}"
    if record.get("check_status") != "PASS":
        return Check(check_id, "FAIL", f"{target} is not admitted as compiled")
    if evidence_root is None:
        return Check(check_id, "SKIPPED", "compiled evidence root was not supplied")
    receipt, error = _read_compiled_receipt(record, evidence_root)
    if error or receipt is None:
        return Check(check_id, "FAIL", error or "compiled receipt is unavailable")
    matches = _compiled_receipt_matches(receipt, binding, target, record)
    detail = (
        "receipt hash, source commit, toolchain, target, exit code, .olean, and dependency hash match"
        if matches
        else "compiled receipt fields do not match the manifest target"
    )
    return Check(check_id, "PASS" if matches else "FAIL", detail)


def verify_compiled_evidence(
    manifest: dict[str, Any], evidence_root: Path | None
) -> list[Check]:
    """Cross-check target PASS records against a pinned structured receipt."""

    binding = manifest.get("source_binding", {})
    return [
        _compiled_target_evidence_check(target, record, binding, evidence_root)
        for target, record in binding.get("compiled_targets", {}).items()
    ]


def _assessment(
    manifest: dict[str, Any],
    lean_root: Path | None,
    evidence_root: Path | None,
) -> list[Check]:
    errors = validate_manifest(manifest)
    checks = [Check("manifest_contract", "PASS" if not errors else "FAIL", "; ".join(errors) or "manifest contract is valid")]
    if errors:
        return checks
    for obligation in manifest["obligations"]:
        obligation_id = obligation["obligation_id"]
        custody = check_quantifier_custody(obligation)
        evaluated = evaluate_obligation(obligation)
        checks.append(Check(f"{obligation_id}:{custody.check_id}", custody.check_status, custody.detail))
        checks.append(Check(f"{obligation_id}:{evaluated.check_id}", evaluated.check_status, evaluated.detail))
        target = obligation["compiled_target"]
        target_record = manifest["source_binding"]["compiled_targets"][target]
        target_ok = target_record.get("check_status") == "PASS"
        checks.append(
            Check(
                f"{obligation_id}:compiled_target",
                "PASS" if target_ok else "FAIL",
                f"{target} has a scoped compiled PASS" if target_ok else f"{target} remains HELD",
            )
        )
    if lean_root is None:
        checks.append(Check("source_bindings", "SKIPPED", "no Lean source root supplied"))
    else:
        checks.extend(verify_source_bindings(manifest, lean_root))
    checks.extend(verify_compiled_evidence(manifest, evidence_root))
    return checks


def _swap_quantifiers(candidate: dict[str, Any]) -> None:
    obligation = candidate["obligations"][1]
    obligation["claimed_scope"] = "SYMBOLIC_PARAMETRIC_IDENTITY"
    obligation["artifact_quantifiers"] = [
        {"quantifier": item["quantifier"], "binder": item["binder"]}
        for item in reversed(obligation["source_quantifiers"])
    ]


def _drop_assumption(candidate: dict[str, Any]) -> None:
    candidate["obligations"][0]["assumptions"].pop()


def _inflate_finite_grid(candidate: dict[str, Any]) -> None:
    candidate["obligations"][0]["claimed_scope"] = "SYMBOLIC_PARAMETRIC_IDENTITY"


def _promote_source_instance(candidate: dict[str, Any]) -> None:
    candidate["obligations"][0]["claimed_scope"] = "SOURCE_INSTANCE"


def _malform_hash(candidate: dict[str, Any]) -> None:
    candidate["obligations"][0]["source_locator"]["sha256"] = "STALE"


def _drift_target(candidate: dict[str, Any]) -> None:
    candidate["obligations"][0]["compiled_target"] = "+NavierStokes.NotThePinnedTarget"


MUTATIONS: tuple[tuple[str, Callable[[dict[str, Any]], None]], ...] = (
    ("swap_quantifier_order", _swap_quantifiers),
    ("drop_required_assumption", _drop_assumption),
    ("finite_grid_to_symbolic", _inflate_finite_grid),
    ("parametric_to_source_instance", _promote_source_instance),
    ("malformed_source_hash", _malform_hash),
    ("compiled_target_drift", _drift_target),
)


def run_mutations(
    manifest: dict[str, Any],
    lean_root: Path | None = None,
    evidence_root: Path | None = None,
) -> list[MutationResult]:
    baseline_failures = {
        check.check_id
        for check in _assessment(manifest, lean_root, evidence_root)
        if check.check_status == "FAIL"
    }
    results: list[MutationResult] = []
    for mutation_id, mutate in MUTATIONS:
        candidate = copy.deepcopy(manifest)
        mutate(candidate)
        mutated_failures = {
            check.check_id
            for check in _assessment(candidate, lean_root, evidence_root)
            if check.check_status == "FAIL"
        }
        new_failures = tuple(sorted(mutated_failures - baseline_failures))
        expected = EXPECTED_MUTATION_DETECTORS[mutation_id]
        results.append(MutationResult(mutation_id, expected in new_failures, new_failures))
    return results


def inspect_spar_identity(expected_version: str = "0.6.0") -> dict[str, str]:
    """Report both import-source and installed metadata identity."""

    try:
        import spar_framework

        source_version = str(getattr(spar_framework, "__version__", "UNKNOWN"))
        try:
            distribution_version = importlib.metadata.version("spar-framework")
        except importlib.metadata.PackageNotFoundError:
            distribution_version = "UNAVAILABLE"
        status = "PASS" if source_version == distribution_version == expected_version else "FAIL"
        return {
            "check_status": status,
            "expected_version": expected_version,
            "source_version": source_version,
            "distribution_version": distribution_version,
            "module_path": str(Path(spar_framework.__file__).resolve()),
        }
    except ImportError:
        return {
            "check_status": "ERROR",
            "expected_version": expected_version,
            "source_version": "UNAVAILABLE",
            "distribution_version": "UNAVAILABLE",
            "module_path": "UNAVAILABLE",
        }


def run_spar_diagnostic(checks: list[Check], report_text: str = "") -> dict[str, Any]:
    """Run SPAR as a secondary diagnostic; its score never overrides the hard gate."""

    identity = inspect_spar_identity()
    try:
        from spar_framework.engine import ReviewRuntime, run_review
        from spar_framework.result_types import CheckResult
    except ImportError:
        return {"identity": identity, "check_status": "ERROR", "review": None}

    def layer(prefix: str, selected: list[Check]) -> list[Any]:
        status_map = {"PASS": "PASS", "FAIL": "ANOMALY", "SKIPPED": "CANNOT_CHECK"}
        return [
            CheckResult(
                f"{prefix}{index}",
                item.check_id,
                status_map.get(item.check_status, "CANNOT_CHECK"),
                item.detail,
                basis="nsrw_m4_hard_gate",
                scope="M4-P",
            )
            for index, item in enumerate(selected, start=1)
        ]

    critical = [item for item in checks if item.critical]
    advisory = [item for item in checks if not item.critical]
    runtime = ReviewRuntime(
        build_layer_a=lambda **_: layer("A", critical),
        build_layer_b=lambda **_: layer("B", advisory),
        build_layer_c=lambda **_: [],
    )
    review = run_review(runtime=runtime, subject="NSRW M4-P", gate="claim_custody", report_text=report_text)
    hard_fail = any(item.check_status == "FAIL" and item.critical for item in checks)
    return {
        "identity": identity,
        "check_status": "PASS" if identity["check_status"] == "PASS" and not hard_fail else "FAIL",
        "review": review.to_dict(),
        "non_authority": "SPAR score and verdict cannot override the NSRW hard gate",
    }


def run_m4_audit(
    manifest: dict[str, Any],
    lean_root: Path | None = None,
    evidence_root: Path | None = None,
) -> dict[str, Any]:
    checks = _assessment(manifest, lean_root, evidence_root)
    mutations = run_mutations(manifest, lean_root, evidence_root)
    mutations_ok = all(item.killed for item in mutations)
    checks.append(
        Check(
            "required_mutations_killed",
            "PASS" if mutations_ok else "FAIL",
            f"{sum(item.killed for item in mutations)}/{len(mutations)} required mutations killed",
        )
    )
    hard_fail = any(item.critical and item.check_status != "PASS" for item in checks)
    spar = run_spar_diagnostic(checks, report_text="Parametric M4 obligation audit; no source-instance claim.")
    return {
        "schema_id": "flamehaven.nsrw-m4-audit-receipt.v1",
        "stage": "M4-P",
        "check_status": "FAIL" if hard_fail else "PASS",
        "task_status": "HELD" if hard_fail else "COMPLETED",
        "claim_status": "UNVERIFIED",
        "lane_status": {
            "M4-P": "OPEN[PARAMETRIC_ONLY]" if not hard_fail else "HELD",
            "M4-S": "HELD[NONCOMPUTABLE_SOURCE_INSTANCE]",
        },
        "checks": [item.as_dict() for item in checks],
        "mutations": [item.as_dict() for item in mutations],
        "spar_diagnostic": spar,
        "non_claims": [
            "No selected source witness is numerically reconstructed.",
            "Finite-grid checks are not quantified Lean proofs.",
            "A target build is not paper-Lean semantic equivalence.",
            "No Navier-Stokes millennium-problem solution is established.",
        ],
    }


def load_manifest(path: Path) -> dict[str, Any]:
    data = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(data, dict):
        raise ValueError("manifest root must be an object")
    return data
