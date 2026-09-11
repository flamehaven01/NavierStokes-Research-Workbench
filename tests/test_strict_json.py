from __future__ import annotations

from pathlib import Path

import pytest
from jsonschema import Draft202012Validator

import nsrw.strict_json as strict_json
from nsrw.strict_json import (
    MAX_DEPTH,
    StrictJSONError,
    canonical_json_bytes,
    evidence_digests,
    parse_strict_json_bytes,
)

ROOT = Path(__file__).resolve().parents[1]


def test_strict_json_rejects_duplicate_keys_and_nonfinite_values() -> None:
    with pytest.raises(StrictJSONError, match="duplicate"):
        parse_strict_json_bytes(b'{"a": 1, "a": 2}')
    with pytest.raises(StrictJSONError, match="non-finite"):
        parse_strict_json_bytes(b'{"a": NaN}')


def test_strict_json_rejects_bom_and_excessive_depth() -> None:
    with pytest.raises(StrictJSONError, match="BOM"):
        parse_strict_json_bytes(b"\xef\xbb\xbf{}")
    nested = b"[" * (MAX_DEPTH + 2) + b"0" + b"]" * (MAX_DEPTH + 2)
    with pytest.raises(StrictJSONError, match="depth|malformed"):
        parse_strict_json_bytes(nested)


def test_depth_scan_is_string_aware_and_total_nodes_are_bounded(monkeypatch) -> None:
    value = parse_strict_json_bytes(b'{"text": "[{\\\"still-a-string\\\"}]"}')
    assert value["text"].startswith("[")
    monkeypatch.setattr(strict_json, "MAX_TOTAL_NODES", 3)
    with pytest.raises(StrictJSONError, match="total node"):
        parse_strict_json_bytes(b'{"a": 1, "b": 2}')


def test_canonical_json_and_digests_are_deterministic() -> None:
    value = parse_strict_json_bytes(b'{"b": 2, "a": "x"}')
    assert canonical_json_bytes(value) == b'{"a":"x","b":2}'
    digests = evidence_digests(b'{"b": 2, "a": "x"}', value)
    assert digests["canonicalization_profile"] == "NSRW-CANONICAL-JSON-1"
    assert len(digests["input_bytes_sha256"]) == 64
    assert len(digests["canonical_manifest_sha256"]) == 64


def test_v3_receipt_and_provenance_schemas_are_valid_documents() -> None:
    import json

    for path in (
        ROOT / "contracts" / "m4-obligation-manifest-v3.schema.json",
        ROOT / "contracts" / "lean-compiled-evidence-v1.schema.json",
        ROOT / "contracts" / "lean-execution-provenance-v1.schema.json",
        ROOT / "contracts" / "m4-mutation-corpus-v1.schema.json",
        ROOT / "contracts" / "lean-receipt-migration-v1.schema.json",
        ROOT / "contracts" / "lean-build-request-v1.schema.json",
    ):
        Draft202012Validator.check_schema(json.loads(path.read_text(encoding="utf-8")))


def test_v3_pilot_and_mutation_corpus_match_their_schemas() -> None:
    import json

    pairs = (
        (
            ROOT / "contracts" / "m4-obligation-manifest-v3.schema.json",
            ROOT / "fixtures" / "m4-parametric-pilot-v3.json",
        ),
        (
            ROOT / "contracts" / "m4-mutation-corpus-v1.schema.json",
            ROOT / "fixtures" / "mutations" / "m4p-v3" / "corpus.json",
        ),
        (
            ROOT / "contracts" / "lean-receipt-migration-v1.schema.json",
            ROOT / "fixtures" / "evidence" / "lean-scoped-targets-v3-migration.json",
        ),
        (
            ROOT / "contracts" / "lean-build-request-v1.schema.json",
            ROOT / "fixtures" / "evidence" / "lean-scoped-build-request-v1.json",
        ),
        (
            ROOT / "contracts" / "lean-compiled-evidence-v1.schema.json",
            ROOT / "fixtures" / "evidence" / "lean-scoped-targets-v3-replay.json",
        ),
    )
    for schema_path, document_path in pairs:
        schema = json.loads(schema_path.read_text(encoding="utf-8"))
        document = json.loads(document_path.read_text(encoding="utf-8"))
        Draft202012Validator(schema).validate(document)
