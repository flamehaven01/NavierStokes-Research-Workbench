"""Strict JSON and JSON Schema admission for public custody documents."""

from __future__ import annotations

from pathlib import Path
from typing import Any

from jsonschema import Draft202012Validator

from .strict_json import load_strict_json

SCHEMA_FILES = {
    "flamehaven.nsrw-m4-obligation-manifest.v1": "m4-obligation-manifest-v1.schema.json",
    "flamehaven.nsrw-m4-obligation-manifest.v2": "m4-obligation-manifest-v2.schema.json",
    "flamehaven.nsrw-m4-obligation-manifest.v3": "m4-obligation-manifest-v3.schema.json",
    "flamehaven.nsrw-m4p-mutation-corpus.v1": "m4-mutation-corpus-v1.schema.json",
    "flamehaven.nsrw-lean-build-request.v1": "lean-build-request-v1.schema.json",
    "flamehaven.nsrw-lean-compiled-evidence.v1": "lean-compiled-evidence-v1.schema.json",
    "flamehaven.nsrw-lean-compiled-evidence.v2": "lean-compiled-evidence-v2.schema.json",
    "flamehaven.nsrw-lean-execution-provenance.v1": "lean-execution-provenance-v1.schema.json",
    "flamehaven.nsrw-lean-receipt-migration.v1": "lean-receipt-migration-v1.schema.json",
    "flamehaven.nsrw-lean-declaration-normalized.v1": "lean-declaration-normalized-v1.schema.json",
}


def _contracts_root() -> Path:
    return Path(__file__).resolve().parents[2] / "contracts"


def validate_document(document: Any, expected_schema_id: str) -> None:
    if expected_schema_id not in SCHEMA_FILES:
        raise ValueError(f"unsupported schema id: {expected_schema_id}")
    if not isinstance(document, dict) or document.get("schema_id") != expected_schema_id:
        raise ValueError(f"document does not declare expected schema id: {expected_schema_id}")
    schema, _ = load_strict_json(_contracts_root() / SCHEMA_FILES[expected_schema_id])
    errors = sorted(
        Draft202012Validator(schema).iter_errors(document),
        key=lambda item: tuple(str(part) for part in item.absolute_path),
    )
    if errors:
        first = errors[0]
        location = ".".join(str(part) for part in first.absolute_path) or "<root>"
        raise ValueError(f"schema admission failed at {location}: {first.message}")


def admit_strict_json(path: Path, expected_schema_id: str) -> tuple[dict[str, Any], bytes]:
    document, raw = load_strict_json(path)
    validate_document(document, expected_schema_id)
    return document, raw


def admit_declared_json(path: Path) -> tuple[dict[str, Any], bytes]:
    """Admit strict JSON against the schema declared by the document itself."""

    document, raw = load_strict_json(path)
    if not isinstance(document, dict):
        raise ValueError("schema-bound JSON document must be an object")
    schema_id = document.get("schema_id")
    if not isinstance(schema_id, str):
        raise ValueError("schema-bound JSON document must declare schema_id")
    validate_document(document, schema_id)
    return document, raw
