"""Strict, bounded JSON parsing for evidence custody.

The parser is intentionally separate from mathematical evaluation.  It rejects
ambiguous JSON before schema or evaluator dispatch and exposes two digests:
the exact admitted bytes and a deterministic semantic-object encoding.
"""

from __future__ import annotations

import hashlib
import json
from pathlib import Path
from typing import Any

MAX_INPUT_BYTES = 1_048_576
MAX_DEPTH = 32
MAX_OBJECT_MEMBERS = 1_024
MAX_ARRAY_ITEMS = 4_096
MAX_STRING_BYTES = 262_144
CANONICALIZATION_PROFILE = "NSRW-CANONICAL-JSON-1"


class StrictJSONError(ValueError):
    """Raised when evidence JSON violates the parser contract."""


def _reject_constant(value: str) -> None:
    raise StrictJSONError(f"non-finite JSON constant is forbidden: {value}")


def _reject_duplicate_keys(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
    result: dict[str, Any] = {}
    for key, value in pairs:
        if key in result:
            raise StrictJSONError(f"duplicate JSON object key: {key}")
        result[key] = value
    if len(result) > MAX_OBJECT_MEMBERS:
        raise StrictJSONError("JSON object member limit exceeded")
    return result


def _check_limits(value: Any, depth: int = 0) -> None:
    if depth > MAX_DEPTH:
        raise StrictJSONError("JSON nesting depth limit exceeded")
    if isinstance(value, str):
        if len(value.encode("utf-8")) > MAX_STRING_BYTES:
            raise StrictJSONError("JSON string byte limit exceeded")
    elif isinstance(value, list):
        if len(value) > MAX_ARRAY_ITEMS:
            raise StrictJSONError("JSON array item limit exceeded")
        for item in value:
            _check_limits(item, depth + 1)
    elif isinstance(value, dict):
        if len(value) > MAX_OBJECT_MEMBERS:
            raise StrictJSONError("JSON object member limit exceeded")
        for key, item in value.items():
            _check_limits(key, depth + 1)
            _check_limits(item, depth + 1)


def parse_strict_json_bytes(raw: bytes) -> Any:
    if len(raw) > MAX_INPUT_BYTES:
        raise StrictJSONError("JSON input byte limit exceeded")
    if raw.startswith(b"\xef\xbb\xbf"):
        raise StrictJSONError("UTF-8 BOM is forbidden")
    try:
        text = raw.decode("utf-8")
    except UnicodeDecodeError as exc:
        raise StrictJSONError("JSON input must be UTF-8") from exc
    try:
        value = json.loads(
            text,
            object_pairs_hook=_reject_duplicate_keys,
            parse_constant=_reject_constant,
        )
    except StrictJSONError:
        raise
    except (json.JSONDecodeError, RecursionError) as exc:
        raise StrictJSONError("JSON input is malformed or too deeply nested") from exc
    _check_limits(value)
    return value


def load_strict_json(path: Path) -> tuple[Any, bytes]:
    raw = path.read_bytes()
    return parse_strict_json_bytes(raw), raw


def canonical_json_bytes(value: Any) -> bytes:
    """Return the project canonical semantic encoding.

    Custody-facing exact values are strings, so the standard encoder is
    deterministic for the admitted contract.  Non-finite values are rejected
    instead of being serialized as JavaScript extensions.
    """

    try:
        rendered = json.dumps(
            value,
            ensure_ascii=False,
            allow_nan=False,
            sort_keys=True,
            separators=(",", ":"),
        )
    except (TypeError, ValueError) as exc:
        raise StrictJSONError("value cannot be canonically encoded") from exc
    return rendered.encode("utf-8")


def evidence_digests(raw: bytes, value: Any) -> dict[str, str]:
    return {
        "input_bytes_sha256": hashlib.sha256(raw).hexdigest().upper(),
        "canonical_manifest_sha256": hashlib.sha256(canonical_json_bytes(value)).hexdigest().upper(),
        "canonicalization_profile": CANONICALIZATION_PROFILE,
    }
