"""M4 parametric obligation audit with fail-closed claim custody.

The numerical evaluators below test declared fixtures.  They do not construct the
noncomputable source witness and do not prove the quantified Lean statements.
"""

from __future__ import annotations

import copy
import hashlib
import importlib.metadata
import re
import subprocess
from dataclasses import asdict, dataclass
from fractions import Fraction
from math import isfinite
from pathlib import Path
from typing import Any, Callable, cast

SCHEMA_ID = "flamehaven.nsrw-m4-obligation-manifest.v2"
SCHEMA_ID_V3 = "flamehaven.nsrw-m4-obligation-manifest.v3"
SUPPORTED_SCHEMA_IDS = frozenset({SCHEMA_ID, SCHEMA_ID_V3})
COMPILED_EVIDENCE_SCHEMA_ID = "flamehaven.nsrw-lean-compiled-evidence.v1"
FAMILIES = frozenset({"SUPPORT", "CONE", "MOMENT", "FALSIFICATION"})
EVIDENCE_CLASSES = frozenset(
    {
        "FINITE_GRID",
        "EXACT_SYMBOLIC",
        "COMPILED_TARGET",
        "MANUFACTURED_FALSIFIER",
        "MANUFACTURED_EXACT_CONTROL",
    }
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
HISTORICAL_V2_MUTATIONS = (
    "swap_quantifier_order",
    "drop_required_assumption",
    "finite_grid_to_symbolic",
    "parametric_to_source_instance",
    "malformed_source_hash",
    "compiled_target_drift",
)
REQUIRED_MUTATIONS = HISTORICAL_V2_MUTATIONS + (
    "negative_cutoff",
    "negative_radial_bound",
    "negative_minimum_margin",
    "boolean_as_numeric",
    "empty_moment_terms",
    "missing_live_olean",
    "dependency_value_order_drift",
    "schema_runtime_divergence",
)
EXPECTED_MUTATION_DETECTORS = {
    "swap_quantifier_order": "M4P-CONE-001:quantifier_custody",
    "drop_required_assumption": "manifest_contract",
    "finite_grid_to_symbolic": "M4P-SUPPORT-001:quantifier_custody",
    "parametric_to_source_instance": "M4P-SUPPORT-001:quantifier_custody",
    "malformed_source_hash": "manifest_contract",
    "compiled_target_drift": "manifest_contract",
    "negative_cutoff": "M4P-SUPPORT-001:support",
    "negative_radial_bound": "M4P-SUPPORT-001:support",
    "negative_minimum_margin": "M4P-CONE-001:cone",
    "boolean_as_numeric": "M4P-CONE-001:cone",
    "empty_moment_terms": "M4P-MOMENT-001:moment",
    "missing_live_olean": "live_artifact:+NavierStokes.OutgoingDilation",
    "dependency_value_order_drift": "M4P-CONE-001:cone",
    "schema_runtime_divergence": "manifest_contract",
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
    killed: bool | None
    reasons: tuple[str, ...]
    expected_detector: str
    evidence_mode: str
    full_manifest_check_status: str
    direct_evaluator_check_status: str
    allowed_secondary_detectors: tuple[str, ...]


def _obligation_by_id(candidate: dict[str, Any], obligation_id: str) -> dict[str, Any]:
    for obligation in candidate.get("obligations", []):
        if isinstance(obligation, dict) and obligation.get("obligation_id") == obligation_id:
            return obligation
    raise KeyError(f"missing obligation id: {obligation_id}")


def _mutation_corpus() -> dict[str, dict[str, Any]]:
    from .strict_json import load_strict_json

    path = Path(__file__).resolve().parents[2] / "fixtures" / "mutations" / "m4p-v3" / "corpus.json"
    value, _ = load_strict_json(path)
    if not isinstance(value, dict) or not isinstance(value.get("cases"), list):
        raise ValueError("M4-P mutation corpus is malformed")
    cases = value["cases"]
    result = {
        str(case.get("mutation_id")): case
        for case in cases
        if isinstance(case, dict) and isinstance(case.get("mutation_id"), str)
    }
    if tuple(result) != REQUIRED_MUTATIONS:
        raise ValueError("M4-P mutation corpus does not exactly match the v3 bank")
    return result

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
    if "locator_evidence_class" in locator and locator.get(
        "locator_evidence_class"
    ) != "TEXTUAL_PINNED_SOURCE_LOCATOR":
        errors.append(f"{prefix}.source_locator.locator_evidence_class is invalid")


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


def _validate_v3_closed_shapes(obligation: object, index: int, errors: list[str]) -> None:
    if not isinstance(obligation, dict):
        return
    allowed_obligation = {
        "obligation_id",
        "family",
        "source_quantifiers",
        "artifact_quantifiers",
        "assumptions",
        "evidence_class",
        "claimed_scope",
        "constructibility",
        "compiled_target",
        "source_locator",
        "evaluator",
    }
    unexpected = set(obligation) - allowed_obligation
    if unexpected:
        errors.append(f"obligations[{index}] has undocumented fields: {sorted(unexpected)}")
    evaluator = obligation.get("evaluator")
    if not isinstance(evaluator, dict):
        return
    family_fields = {
        "SUPPORT": {"required_assumptions", "cutoff", "intervals"},
        "CONE": {
            "required_assumptions",
            "threshold_dependencies",
            "threshold_values",
            "inequalities",
        },
        "MOMENT": {"required_assumptions", "identities"},
        "FALSIFICATION": {"required_assumptions"},
    }
    allowed_evaluator = family_fields.get(str(obligation.get("family")), set())
    unexpected_evaluator = set(evaluator) - allowed_evaluator
    if unexpected_evaluator:
        errors.append(
            f"obligations[{index}].evaluator has undocumented fields: "
            f"{sorted(unexpected_evaluator)}"
        )


def _validate_v3_header(manifest: dict[str, Any], errors: list[str]) -> None:
    if manifest.get("compiled_evidence_mode") not in {"RECEIPT_REPLAY", "LIVE_ARTIFACT"}:
        errors.append("v3 compiled_evidence_mode must be RECEIPT_REPLAY or LIVE_ARTIFACT")
    if manifest.get("canonicalization_profile") != "NSRW-CANONICAL-JSON-1":
        errors.append("v3 canonicalization_profile must be NSRW-CANONICAL-JSON-1")
    if manifest.get("locator_evidence_class") not in {
        None,
        "TEXTUAL_PINNED_SOURCE_LOCATOR",
    }:
        errors.append("v3 locator_evidence_class is invalid")


def _validate_v3_migration_fields(
    manifest: dict[str, Any], binding: dict[str, Any], errors: list[str]
) -> None:
    replay = manifest.get("compiled_evidence_mode") == "RECEIPT_REPLAY"
    migration_fields = (
        binding.get("migration_receipt_path"),
        binding.get("migration_receipt_sha256"),
    )
    if replay and not _valid_relative_path(migration_fields[0]):
        errors.append("v3 replay migration receipt path is invalid")
    if replay and not _is_sha256(migration_fields[1]):
        errors.append("v3 replay migration receipt sha256 is invalid")
    if not replay and any(value is not None for value in migration_fields):
        errors.append("v3 live evidence must not carry replay migration fields")


def _validate_v3_binding(
    manifest: dict[str, Any], targets: dict[str, Any], errors: list[str]
) -> None:
    binding = manifest.get("source_binding")
    if not isinstance(binding, dict):
        return
    if not _valid_relative_path(binding.get("build_request_path")):
        errors.append("v3 source_binding.build_request_path is invalid")
    digest_fields = ("input_bytes_sha256", "canonical_manifest_sha256")
    errors.extend(
        f"v3 source_binding.{field} is invalid"
        for field in digest_fields
        if not _is_sha256(binding.get(field))
    )
    _validate_v3_migration_fields(manifest, binding, errors)
    for target, record in targets.items():
        if isinstance(record, dict) and not _valid_relative_path(record.get("olean_path")):
            errors.append(f"compiled target {target} olean path is invalid")


def _validate_manifest_obligations(
    manifest: dict[str, Any], targets: dict[str, Any], schema_id: object, errors: list[str]
) -> bool:
    obligations = manifest.get("obligations")
    if not isinstance(obligations, list) or not obligations:
        errors.append("obligations must be a non-empty list")
        return False
    seen: set[str] = set()
    for index, obligation in enumerate(obligations):
        _validate_obligation(index, obligation, targets, seen, errors)
        if schema_id == SCHEMA_ID_V3:
            _validate_v3_closed_shapes(obligation, index, errors)
    if schema_id == SCHEMA_ID_V3:
        for index, obligation in enumerate(obligations):
            locator = obligation.get("source_locator") if isinstance(obligation, dict) else None
            if isinstance(locator, dict) and locator.get(
                "locator_evidence_class"
            ) != "TEXTUAL_PINNED_SOURCE_LOCATOR":
                errors.append(
                    f"obligations[{index}].source_locator.locator_evidence_class is required for v3"
                )
    return True


def validate_manifest(manifest: dict[str, Any]) -> list[str]:
    """Validate the portable P0 contract without claiming source freshness."""

    errors: list[str] = []
    schema_id = manifest.get("schema_id")
    if schema_id not in SUPPORTED_SCHEMA_IDS:
        errors.append(f"schema_id must be one of {sorted(SUPPORTED_SCHEMA_IDS)}")
    if schema_id == SCHEMA_ID_V3:
        _validate_v3_header(manifest, errors)
    if manifest.get("stage") != "M4-P":
        errors.append("stage must be M4-P")
    targets = _validate_source_binding(manifest.get("source_binding"), errors)
    if schema_id == SCHEMA_ID_V3:
        _validate_v3_binding(manifest, targets, errors)
    if not _validate_manifest_obligations(manifest, targets, schema_id, errors):
        return errors
    configured = manifest.get("required_mutations")
    expected_mutations = (
        REQUIRED_MUTATIONS if schema_id == SCHEMA_ID_V3 else HISTORICAL_V2_MUTATIONS
    )
    if configured != list(expected_mutations):
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
    if isinstance(value, bool) or not isinstance(value, (str, int)):
        raise ValueError("exact moment values must be integer or rational strings")
    text = str(value)
    if len(text) > 513 or re.fullmatch(r"-?(0|[1-9][0-9]*)(/[1-9][0-9]*)?", text) is None:
        raise ValueError("exact moment value is outside strict rational grammar")
    return Fraction(text)


def _is_real_number(value: object) -> bool:
    if isinstance(value, bool) or not isinstance(value, (int, float)):
        return False
    try:
        return isfinite(float(value))
    except (OverflowError, ValueError):
        return False


def _support_interval_error(interval: object, cutoff: float, previous: float) -> tuple[str | None, float]:
    if not isinstance(interval, dict):
        return "support interval is not an object", previous
    lower, upper = interval.get("lower"), interval.get("upper")
    if not _is_real_number(lower) or not _is_real_number(upper):
        return "support bounds must be numeric", previous
    if not all(isfinite(float(item)) for item in (lower, upper, cutoff)):
        return "support bounds must be finite", previous
    if lower < 0 or lower < previous or lower > upper or upper > cutoff:
        return "support ordering, inclusion, or cutoff failed", previous
    return None, float(upper)


def _support_name_error(interval: object, names: set[str]) -> str | None:
    if not isinstance(interval, dict):
        return "support interval is not an object"
    name = interval.get("name")
    if not isinstance(name, str) or not name:
        return "support interval names must be non-empty"
    if name in names:
        return "support interval names must be unique"
    names.add(name)
    return None


def _evaluate_support(evaluator: dict[str, Any]) -> Check:
    intervals = evaluator.get("intervals")
    cutoff = evaluator.get("cutoff")
    if not isinstance(intervals, list) or not intervals or not _is_real_number(cutoff):
        return Check("support", "FAIL", "support evaluator requires intervals and cutoff")
    if float(cutoff) <= 0:
        return Check("support", "FAIL", "support cutoff must be positive")
    previous = float("-inf")
    names: set[str] = set()
    for interval in intervals:
        if name_error := _support_name_error(interval, names):
            return Check("support", "FAIL", name_error)
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
    if not all(_is_real_number(value) for value in (lhs, rhs, minimum)):
        return None, "cone values must be numeric"
    if not all(isfinite(float(value)) for value in (lhs, rhs, minimum)):
        return None, "cone values must be finite"
    if float(minimum) < 0:
        return None, "cone minimum margin must be non-negative"
    margin = float(rhs - lhs) if relation == "LE" else float(lhs - rhs)
    if margin < float(minimum):
        return None, "a cone inequality lacks its declared margin"
    return margin, None


def _threshold_values_error(
    graph: dict[str, object], threshold_values: object
) -> str | None:
    if threshold_values is None:
        return None
    if not isinstance(threshold_values, dict) or set(threshold_values) != set(graph):
        return "threshold values must exactly match dependency nodes"
    if any(not isinstance(value, str) for value in threshold_values.values()):
        return "threshold values must use strict rational strings"
    try:
        parsed = {str(key): _fraction(value) for key, value in threshold_values.items()}
    except (TypeError, ValueError, ZeroDivisionError):
        return "threshold values must use strict rational strings"
    if any(value <= 0 for value in parsed.values()):
        return "threshold values must be positive"
    for node, dependencies in graph.items():
        if any(parsed[node] <= parsed[dependency] for dependency in dependencies):
            return "threshold dependency value ordering failed"
    return None


def _cone_margins(inequalities: list[object]) -> tuple[list[float], str | None]:
    margins: list[float] = []
    labels: set[str] = set()
    for item in inequalities:
        if not isinstance(item, dict):
            return margins, "cone inequality is malformed"
        label = item.get("label")
        if not isinstance(label, str) or not label:
            return margins, "cone inequality labels must be non-empty"
        if label in labels:
            return margins, "cone inequality labels must be unique"
        labels.add(label)
        margin, error = _cone_margin(item)
        if error:
            return margins, error
        assert margin is not None
        margins.append(margin)
    return margins, None


def _evaluate_cone(evaluator: dict[str, Any]) -> Check:
    inequalities = evaluator.get("inequalities")
    graph = evaluator.get("threshold_dependencies", {})
    if not isinstance(inequalities, list) or not inequalities or not isinstance(graph, dict):
        return Check("cone", "FAIL", "cone evaluator requires inequalities and a dependency graph")
    if graph_error := _dependency_graph_error(graph):
        return Check("cone", "FAIL", graph_error)
    if threshold_error := _threshold_values_error(graph, evaluator.get("threshold_values")):
        return Check("cone", "FAIL", threshold_error)
    margins, margin_error = _cone_margins(inequalities)
    if margin_error:
        return Check("cone", "FAIL", margin_error)
    return Check("cone", "PASS", f"cone inequalities pass; minimum observed margin={min(margins):.12g}")


def _moment_identity_error(identity: object, labels: set[str]) -> str | None:
    if not isinstance(identity, dict):
        return "moment identity is malformed"
    label = identity.get("label")
    if not isinstance(label, str) or not label or label in labels:
        return "moment labels must be non-empty and unique"
    labels.add(label)
    terms = identity["terms"]
    expected = _fraction(identity["expected"])
    if not isinstance(terms, list) or not terms:
        return "an exact moment or cancellation identity failed"
    if sum((_fraction(term) for term in terms), Fraction()) != expected:
        return "an exact moment or cancellation identity failed"
    return None


def _evaluate_moment(evaluator: dict[str, Any]) -> Check:
    identities = evaluator.get("identities")
    if not isinstance(identities, list) or not identities:
        return Check("moment", "FAIL", "moment evaluator requires exact identities")
    try:
        labels: set[str] = set()
        for identity in identities:
            if error := _moment_identity_error(identity, labels):
                return Check("moment", "FAIL", error)
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
        from .strict_json import StrictJSONError, load_strict_json

        receipt, _ = load_strict_json(path)
    except (OSError, StrictJSONError):
        return None, "compiled receipt is not valid strict JSON"
    if not isinstance(receipt, dict):
        return None, "compiled receipt root is not an object"
    return receipt, None


def _expected_compiled_fields(
    binding: dict[str, Any], target: str, record: dict[str, Any]
) -> dict[str, Any]:
    expected_olean_path = (
        record.get("olean_path")
        if binding.get("build_request_path") is not None
        else ".lake/build/lib/lean/"
        + target.removeprefix("+").replace(".", "/")
        + ".olean"
    )
    return {
        "schema_id": COMPILED_EVIDENCE_SCHEMA_ID,
        "formal_source_commit": binding.get("formal_source_commit"),
        "toolchain": binding.get("formal_source_toolchain"),
        "target": target,
        "exit_code": 0,
        "olean_path": expected_olean_path,
        "olean_sha256": str(record.get("olean_sha256", "")).upper(),
    }


def _actual_compiled_fields(
    receipt: dict[str, Any], target_evidence: dict[str, Any]
) -> dict[str, Any]:
    return {
        "schema_id": receipt.get("schema_id"),
        "formal_source_commit": receipt.get("formal_source_commit"),
        "toolchain": receipt.get("toolchain"),
        "target": target_evidence.get("target"),
        "exit_code": target_evidence.get("exit_code"),
        "olean_path": target_evidence.get("olean_path"),
        "olean_sha256": str(target_evidence.get("olean_sha256", "")).upper(),
    }


def _compiled_receipt_matches(
    receipt: dict[str, Any],
    binding: dict[str, Any],
    target: str,
    record: dict[str, Any],
    evidence_mode: str | None = None,
) -> bool:
    targets = receipt.get("targets")
    if not isinstance(targets, dict) or not isinstance(targets.get(target), dict):
        return False
    target_evidence = targets[target]
    expected = _expected_compiled_fields(binding, target, record)
    actual = _actual_compiled_fields(receipt, target_evidence)
    input_ok = True
    if binding.get("build_request_path") is not None:
        input_ok = all(
            (
                receipt.get("input_bytes_sha256") == binding.get("input_bytes_sha256"),
                receipt.get("canonical_manifest_sha256")
                == binding.get("canonical_manifest_sha256"),
            )
        )
    mode_ok = evidence_mode is None or receipt.get("compiled_evidence_mode") == evidence_mode
    return (
        mode_ok
        and input_ok
        and actual == expected
        and _is_sha256(target_evidence.get("dependency_surface_sha256"))
    )


def _compiled_target_evidence_check(
    target: str,
    record: dict[str, Any],
    binding: dict[str, Any],
    evidence_root: Path | None,
    evidence_mode: str | None = None,
) -> Check:
    check_id = f"compiled_receipt:{target}"
    if record.get("check_status") != "PASS":
        return Check(check_id, "FAIL", f"{target} is not admitted as compiled")
    if evidence_root is None:
        return Check(check_id, "SKIPPED", "compiled evidence root was not supplied")
    receipt, error = _read_compiled_receipt(record, evidence_root)
    if error or receipt is None:
        return Check(check_id, "FAIL", error or "compiled receipt is unavailable")
    matches = _compiled_receipt_matches(receipt, binding, target, record, evidence_mode)
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
    evidence_mode = manifest.get("compiled_evidence_mode")
    return [
        _compiled_target_evidence_check(target, record, binding, evidence_root, evidence_mode)
        for target, record in binding.get("compiled_targets", {}).items()
    ]


def _load_bound_migration(
    binding: dict[str, Any], evidence_root: Path
) -> tuple[dict[str, Any] | None, str | None]:
    path = _safe_evidence_path(
        evidence_root, str(binding.get("migration_receipt_path", ""))
    )
    if path is None or not path.is_file():
        return None, "replay migration receipt is unavailable"
    actual_hash = hashlib.sha256(path.read_bytes()).hexdigest().upper()
    if actual_hash != str(binding.get("migration_receipt_sha256", "")).upper():
        return None, "replay migration receipt hash mismatch"
    try:
        from .strict_json import load_strict_json

        migration, _ = load_strict_json(path)
    except (OSError, ValueError):
        return None, "replay migration receipt is invalid JSON"
    if not isinstance(migration, dict):
        return None, "replay migration receipt is not an object"
    return migration, None


def _migration_artifact_error(
    migration: dict[str, Any], evidence_root: Path
) -> str | None:
    paths_and_hashes = (
        ("source_receipt_path", "source_receipt_sha256"),
        ("migrated_receipt_path", "migrated_receipt_sha256"),
        ("replay_request_path", "replay_request_sha256"),
    )
    for path_field, hash_field in paths_and_hashes:
        artifact = _safe_evidence_path(evidence_root, str(migration.get(path_field, "")))
        if artifact is None or not artifact.is_file():
            return f"migration-bound {path_field} is unavailable"
        digest = hashlib.sha256(artifact.read_bytes()).hexdigest().upper()
        if digest != str(migration.get(hash_field, "")).upper():
            return f"migration-bound {hash_field} mismatch"
    return None


def verify_replay_migration(
    manifest: dict[str, Any], evidence_root: Path | None
) -> Check | None:
    if manifest.get("compiled_evidence_mode") != "RECEIPT_REPLAY":
        return None
    check_id = "replay_receipt_migration"
    if evidence_root is None:
        return Check(check_id, "FAIL", "replay migration evidence root was not supplied")
    binding = manifest.get("source_binding", {})
    migration, load_error = _load_bound_migration(binding, evidence_root)
    if load_error or migration is None:
        return Check(check_id, "FAIL", load_error or "replay migration unavailable")
    if artifact_error := _migration_artifact_error(migration, evidence_root):
        return Check(check_id, "FAIL", artifact_error)
    if (
        migration.get("schema_id") != "flamehaven.nsrw-lean-receipt-migration.v1"
        or migration.get("migration_ruleset") != "NSRW-LEAN-REPLAY-METADATA-1"
        or migration.get("migration_class") != "MIGRATED_METADATA_ONLY"
    ):
        return Check(check_id, "FAIL", "replay migration authority fields are invalid")
    return Check(
        check_id,
        "PASS",
        "historical and migrated receipts are hash-bound by a metadata-only migration",
    )


def verify_live_artifacts(manifest: dict[str, Any], lean_root: Path | None) -> list[Check]:
    """Verify bytes in the declared live Lean checkout; replay has no local-artifact claim."""

    if manifest.get("compiled_evidence_mode") != "LIVE_ARTIFACT":
        return []
    binding = manifest.get("source_binding", {})
    checks: list[Check] = []
    for target, record in binding.get("compiled_targets", {}).items():
        check_id = f"live_artifact:{target}"
        if lean_root is None:
            checks.append(Check(check_id, "FAIL", "live evidence requires a Lean source root"))
            continue
        path = _safe_evidence_path(lean_root, str(record.get("olean_path", "")))
        actual_hash = hashlib.sha256(path.read_bytes()).hexdigest().upper() if path and path.is_file() else ""
        expected_hash = str(record.get("olean_sha256", "")).upper()
        matches = bool(actual_hash) and actual_hash == expected_hash
        checks.append(
            Check(
                check_id,
                "PASS" if matches else "FAIL",
                "declared same-run artifact bytes match"
                if matches
                else "declared live .olean is missing or its bytes drifted",
            )
        )
    return checks


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
        replay = manifest.get("compiled_evidence_mode") == "RECEIPT_REPLAY"
        checks.append(
            Check(
                "source_bindings",
                "SKIPPED",
                "no Lean source root supplied; replay mode does not assert current-source freshness"
                if replay
                else "no Lean source root supplied",
                critical=not replay,
            )
        )
    else:
        checks.extend(verify_source_bindings(manifest, lean_root))
    migration_check = verify_replay_migration(manifest, evidence_root)
    if migration_check is not None:
        checks.append(migration_check)
    checks.extend(verify_compiled_evidence(manifest, evidence_root))
    checks.extend(verify_live_artifacts(manifest, lean_root))
    return checks


def _swap_quantifiers(candidate: dict[str, Any]) -> None:
    obligation = _obligation_by_id(candidate, "M4P-CONE-001")
    obligation["claimed_scope"] = "SYMBOLIC_PARAMETRIC_IDENTITY"
    obligation["artifact_quantifiers"] = [
        {"quantifier": item["quantifier"], "binder": item["binder"]}
        for item in reversed(obligation["source_quantifiers"])
    ]


def _drop_assumption(candidate: dict[str, Any]) -> None:
    _obligation_by_id(candidate, "M4P-SUPPORT-001")["assumptions"].remove(
        "positive_cutoff"
    )


def _inflate_finite_grid(candidate: dict[str, Any]) -> None:
    _obligation_by_id(candidate, "M4P-SUPPORT-001")[
        "claimed_scope"
    ] = "SYMBOLIC_PARAMETRIC_IDENTITY"


def _promote_source_instance(candidate: dict[str, Any]) -> None:
    _obligation_by_id(candidate, "M4P-SUPPORT-001")["claimed_scope"] = "SOURCE_INSTANCE"


def _malform_hash(candidate: dict[str, Any]) -> None:
    _obligation_by_id(candidate, "M4P-SUPPORT-001")["source_locator"]["sha256"] = "STALE"


def _drift_target(candidate: dict[str, Any]) -> None:
    _obligation_by_id(candidate, "M4P-SUPPORT-001")[
        "compiled_target"
    ] = "+NavierStokes.NotThePinnedTarget"


def _negative_cutoff(candidate: dict[str, Any]) -> None:
    _obligation_by_id(candidate, "M4P-SUPPORT-001")["evaluator"]["cutoff"] = -1


def _negative_radial_bound(candidate: dict[str, Any]) -> None:
    _obligation_by_id(candidate, "M4P-SUPPORT-001")["evaluator"]["intervals"][0][
        "lower"
    ] = -1


def _negative_minimum_margin(candidate: dict[str, Any]) -> None:
    _obligation_by_id(candidate, "M4P-CONE-001")["evaluator"]["inequalities"][0][
        "minimum_margin"
    ] = -1


def _boolean_as_numeric(candidate: dict[str, Any]) -> None:
    _obligation_by_id(candidate, "M4P-CONE-001")["evaluator"]["inequalities"][0][
        "lhs"
    ] = True


def _empty_moment_terms(candidate: dict[str, Any]) -> None:
    _obligation_by_id(candidate, "M4P-MOMENT-001")["evaluator"]["identities"][0][
        "terms"
    ] = []


def _missing_live_olean(candidate: dict[str, Any]) -> None:
    candidate["source_binding"]["compiled_targets"]["+NavierStokes.OutgoingDilation"][
        "olean_path"
    ] = ".lake/build/nsrw-missing/OutgoingDilation.olean"


def _dependency_value_order_drift(candidate: dict[str, Any]) -> None:
    _obligation_by_id(candidate, "M4P-CONE-001")["evaluator"]["threshold_values"] = {
        "R_inner": "5",
        "R_outer": "2",
    }


def _schema_runtime_divergence(candidate: dict[str, Any]) -> None:
    _obligation_by_id(candidate, "M4P-SUPPORT-001")["evaluator"][
        "undocumented_runtime_hint"
    ] = "must-fail-closed"


MUTATIONS: tuple[tuple[str, Callable[[dict[str, Any]], None]], ...] = (
    ("swap_quantifier_order", _swap_quantifiers),
    ("drop_required_assumption", _drop_assumption),
    ("finite_grid_to_symbolic", _inflate_finite_grid),
    ("parametric_to_source_instance", _promote_source_instance),
    ("malformed_source_hash", _malform_hash),
    ("compiled_target_drift", _drift_target),
    ("negative_cutoff", _negative_cutoff),
    ("negative_radial_bound", _negative_radial_bound),
    ("negative_minimum_margin", _negative_minimum_margin),
    ("boolean_as_numeric", _boolean_as_numeric),
    ("empty_moment_terms", _empty_moment_terms),
    ("missing_live_olean", _missing_live_olean),
    ("dependency_value_order_drift", _dependency_value_order_drift),
    ("schema_runtime_divergence", _schema_runtime_divergence),
)


def _direct_mutation_status(
    baseline: dict[str, Any],
    candidate: dict[str, Any],
    case: dict[str, Any],
) -> tuple[bool, str]:
    expected = str(case.get("direct_evaluator_expected_detector", "NOT_APPLICABLE"))
    obligation_id = case.get("direct_obligation_id")
    if expected == "NOT_APPLICABLE" or not isinstance(obligation_id, str):
        return True, "NOT_APPLICABLE"
    baseline_check = evaluate_obligation(_obligation_by_id(baseline, obligation_id))
    mutated_check = evaluate_obligation(_obligation_by_id(candidate, obligation_id))
    actual = f"{obligation_id}:{mutated_check.check_id}"
    passed = (
        baseline_check.check_status == "PASS"
        and mutated_check.check_status == "FAIL"
        and actual == expected
    )
    return passed, "PASS" if passed else "FAIL"


def _execute_mutation_case(
    manifest: dict[str, Any],
    mutation_id: str,
    mutate: Callable[[dict[str, Any]], None],
    case: dict[str, Any],
    baseline_failures: set[str],
    evidence_mode: str,
    lean_root: Path | None,
    evidence_root: Path | None,
) -> MutationResult:
    expected = str(
        case.get("full_manifest_expected_detector", EXPECTED_MUTATION_DETECTORS[mutation_id])
    )
    applicable_modes = tuple(case.get("applicable_evidence_modes", (evidence_mode,)))
    allowed_secondary = tuple(case.get("allowed_secondary_detectors", ()))
    if evidence_mode not in applicable_modes:
        return MutationResult(
            mutation_id,
            None,
            (),
            expected,
            evidence_mode,
            "NOT_APPLICABLE",
            "NOT_APPLICABLE",
            allowed_secondary,
        )
    candidate = copy.deepcopy(manifest)
    mutate(candidate)
    mutated_failures = {
        check.check_id
        for check in _assessment(candidate, lean_root, evidence_root)
        if check.check_status == "FAIL"
    }
    new_failures = tuple(sorted(mutated_failures - baseline_failures))
    admitted_failures = {expected, *allowed_secondary}
    full_ok = expected in new_failures and set(new_failures).issubset(admitted_failures)
    direct_ok, direct_status = _direct_mutation_status(manifest, candidate, case)
    return MutationResult(
        mutation_id,
        full_ok and direct_ok,
        new_failures,
        expected,
        evidence_mode,
        "PASS" if full_ok else "FAIL",
        direct_status,
        allowed_secondary,
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
    evidence_mode = str(manifest.get("compiled_evidence_mode", "HISTORICAL_V2"))
    required = (
        REQUIRED_MUTATIONS
        if manifest.get("schema_id") == SCHEMA_ID_V3
        else HISTORICAL_V2_MUTATIONS
    )
    corpus = _mutation_corpus() if manifest.get("schema_id") == SCHEMA_ID_V3 else {}
    results.extend(
        _execute_mutation_case(
            manifest,
            mutation_id,
            mutate,
            corpus.get(mutation_id, {}),
            baseline_failures,
            evidence_mode,
            lean_root,
            evidence_root,
        )
        for mutation_id, mutate in MUTATIONS
        if mutation_id in required
    )
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
            # Absolute import paths are machine-private and must not enter a
            # public evidence receipt.
            "module_path": "REDACTED_PUBLIC_RECEIPT",
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
    applicable_mutations = [item for item in mutations if item.killed is not None]
    mutations_ok = all(item.killed for item in applicable_mutations)
    checks.append(
        Check(
            "required_mutations_killed",
            "PASS" if mutations_ok else "FAIL",
            f"{sum(item.killed is True for item in applicable_mutations)}/"
            f"{len(applicable_mutations)} applicable required mutations killed; "
            f"{len(mutations) - len(applicable_mutations)} not applicable",
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
        "authority_status": (
            "HARDENED_V3"
            if manifest.get("schema_id") == SCHEMA_ID_V3
            else "HISTORICAL_V2_REPLAY"
        ),
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
    from .strict_json import StrictJSONError, load_strict_json

    try:
        data, _ = load_strict_json(path)
    except StrictJSONError as exc:
        raise ValueError(str(exc)) from exc
    if not isinstance(data, dict):
        raise ValueError("manifest root must be an object")
    return data
