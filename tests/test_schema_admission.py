from __future__ import annotations

import copy
import json
from pathlib import Path
from typing import Any, Callable

import pytest

from nsrw.lean_receipt import build_compiled_receipt
from nsrw.m4_audit import run_m4_audit
from nsrw.schema_admission import admit_declared_json, validate_document

ROOT = Path(__file__).resolve().parents[1]


def _json(path: str) -> dict[str, Any]:
    return json.loads((ROOT / path).read_text(encoding="utf-8"))


def _compiled_v2() -> dict[str, Any]:
    return build_compiled_receipt(
        "a" * 40,
        "leanprover/lean4:v4.34.0-rc2",
        {
            "+Example.Target": {
                "target": "+Example.Target",
                "exit_code": 0,
                "olean_path": ".lake/build/lib/lean/Example/Target.olean",
                "olean_sha256": "b" * 64,
                "dependency_surface_path": "outputs/deps/target.txt",
                "dependency_surface_sha256": "c" * 64,
            }
        },
        "d" * 64,
        "e" * 64,
    )


def _provenance() -> dict[str, Any]:
    return {
        "schema_id": "flamehaven.nsrw-lean-execution-provenance.v1",
        "provider": "LOCAL",
        "workflow": "LOCAL_UNHOSTED",
        "run_id": "UNHOSTED",
        "attempt": 1,
        "platform": "nt",
        "canonical_receipt_sha256": "a" * 64,
    }


DOCUMENTS: tuple[tuple[str, Callable[[], dict[str, Any]], str], ...] = (
    (
        "flamehaven.nsrw-m4-obligation-manifest.v3",
        lambda: _json("fixtures/m4-parametric-pilot-v3.json"),
        "stage",
    ),
    (
        "flamehaven.nsrw-lean-build-request.v1",
        lambda: _json("fixtures/evidence/lean-scoped-build-request-v1.json"),
        "targets",
    ),
    ("flamehaven.nsrw-lean-compiled-evidence.v2", _compiled_v2, "targets"),
    ("flamehaven.nsrw-lean-execution-provenance.v1", _provenance, "provider"),
    (
        "flamehaven.nsrw-lean-receipt-migration.v1",
        lambda: _json("fixtures/evidence/lean-scoped-targets-v3-migration.json"),
        "migration_ruleset",
    ),
    (
        "flamehaven.nsrw-m4p-mutation-corpus.v1",
        lambda: _json("fixtures/mutations/m4p-v3/corpus.json"),
        "cases",
    ),
)


@pytest.mark.parametrize(("schema_id", "factory", "required_field"), DOCUMENTS)
def test_all_custody_documents_share_schema_first_admission(
    schema_id: str,
    factory: Callable[[], dict[str, Any]],
    required_field: str,
) -> None:
    document = factory()
    validate_document(document, schema_id)

    unexpected = copy.deepcopy(document)
    unexpected["undeclared"] = True
    with pytest.raises(ValueError, match="schema admission"):
        validate_document(unexpected, schema_id)

    missing = copy.deepcopy(document)
    missing.pop(required_field)
    with pytest.raises(ValueError, match="schema admission"):
        validate_document(missing, schema_id)

    wrong_id = copy.deepcopy(document)
    wrong_id["schema_id"] = "unknown.schema"
    with pytest.raises(ValueError, match="expected schema id"):
        validate_document(wrong_id, schema_id)


def test_nested_fields_paths_hashes_and_enums_fail_schema_admission() -> None:
    manifest = _json("fixtures/m4-parametric-pilot-v3.json")
    manifest["obligations"][0]["evaluator"]["undeclared"] = True
    with pytest.raises(ValueError, match="schema admission"):
        validate_document(manifest, manifest["schema_id"])

    build_request = _json("fixtures/evidence/lean-scoped-build-request-v1.json")
    build_request["targets"][0]["module_source"] = "../escape.lean"
    with pytest.raises(ValueError, match="schema admission"):
        validate_document(build_request, build_request["schema_id"])

    compiled = _compiled_v2()
    compiled["targets"]["+Example.Target"]["olean_sha256"] = "bad"
    with pytest.raises(ValueError, match="schema admission"):
        validate_document(compiled, compiled["schema_id"])

    provenance = _provenance()
    provenance["attempt"] = 0
    with pytest.raises(ValueError, match="schema admission"):
        validate_document(provenance, provenance["schema_id"])

    migration = _json("fixtures/evidence/lean-scoped-targets-v3-migration.json")
    migration["migration_class"] = "UNDECLARED_CLASS"
    with pytest.raises(ValueError, match="schema admission"):
        validate_document(migration, migration["schema_id"])

    corpus = _json("fixtures/mutations/m4p-v3/corpus.json")
    corpus["cases"][0]["applicable_evidence_modes"] = ["UNKNOWN"]
    with pytest.raises(ValueError, match="schema admission"):
        validate_document(corpus, corpus["schema_id"])


def test_unknown_declared_schema_fails_closed(tmp_path: Path) -> None:
    path = tmp_path / "unknown.json"
    path.write_text('{"schema_id":"unknown.schema"}\n', encoding="utf-8")
    with pytest.raises(ValueError, match="unsupported schema id"):
        admit_declared_json(path)


def test_schema_admission_does_not_bypass_stricter_runtime_semantics() -> None:
    manifest = _json("fixtures/m4-parametric-pilot-v3.json")
    cone = next(item for item in manifest["obligations"] if item["family"] == "CONE")
    cone["evaluator"]["threshold_dependencies"] = {"A": ["B"], "B": ["A"]}
    cone["evaluator"]["threshold_values"] = {"A": "3", "B": "2"}
    validate_document(manifest, manifest["schema_id"])
    receipt = run_m4_audit(manifest, evidence_root=ROOT)
    assert any(
        check["check_id"] == "M4P-CONE-001:cone" and check["check_status"] == "FAIL"
        for check in receipt["checks"]
    )
