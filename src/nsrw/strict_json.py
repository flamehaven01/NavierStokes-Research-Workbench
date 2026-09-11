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
MAX_TOTAL_NODES = 100_000
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


def _string_state(character: str, in_string: bool, escaped: bool) -> tuple[bool, bool]:
    if not in_string:
        return character == '"', False
    if escaped:
        return True, False
    if character == "\\":
        return True, True
    return character != '"', False


def _nesting_delta(character: str) -> int:
    if character in "[{":
        return 1
    if character in "]}":
        return -1
    return 0


def _scan_nesting_depth(text: str) -> None:
    depth = 0
    in_string = False
    escaped = False
    for character in text:
        if in_string:
            in_string, escaped = _string_state(character, in_string, escaped)
            continue
        if character == '"':
            in_string = True
            continue
        depth += _nesting_delta(character)
        if depth > MAX_DEPTH:
            raise StrictJSONError("JSON nesting depth limit exceeded")
        if depth < 0:
            raise StrictJSONError("JSON nesting is unbalanced")


def _check_sequence(items: list[Any], depth: int, nodes: list[int]) -> None:
    if len(items) > MAX_ARRAY_ITEMS:
        raise StrictJSONError("JSON array item limit exceeded")
    for item in items:
        _check_limits(item, depth + 1, nodes)


def _check_mapping(value: dict[Any, Any], depth: int, nodes: list[int]) -> None:
    if len(value) > MAX_OBJECT_MEMBERS:
        raise StrictJSONError("JSON object member limit exceeded")
    for key, item in value.items():
        _check_limits(key, depth + 1, nodes)
        _check_limits(item, depth + 1, nodes)


def _check_limits(value: Any, depth: int = 0, nodes: list[int] | None = None) -> None:
    if nodes is None:
        nodes = [0]
    nodes[0] += 1
    if nodes[0] > MAX_TOTAL_NODES:
        raise StrictJSONError("JSON total node limit exceeded")
    if depth > MAX_DEPTH:
        raise StrictJSONError("JSON nesting depth limit exceeded")
    if isinstance(value, str):
        if len(value.encode("utf-8")) > MAX_STRING_BYTES:
            raise StrictJSONError("JSON string byte limit exceeded")
    elif isinstance(value, list):
        _check_sequence(value, depth, nodes)
    elif isinstance(value, dict):
        _check_mapping(value, depth, nodes)


def parse_strict_json_bytes(raw: bytes) -> Any:
    if len(raw) > MAX_INPUT_BYTES:
        raise StrictJSONError("JSON input byte limit exceeded")
    if raw.startswith(b"\xef\xbb\xbf"):
        raise StrictJSONError("UTF-8 BOM is forbidden")
    try:
        text = raw.decode("utf-8")
    except UnicodeDecodeError as exc:
        raise StrictJSONError("JSON input must be UTF-8") from exc
    _scan_nesting_depth(text)
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
