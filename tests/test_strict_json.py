from __future__ import annotations

from pathlib import Path

import pytest
from jsonschema import Draft202012Validator

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
    ):
        Draft202012Validator.check_schema(json.loads(path.read_text(encoding="utf-8")))
