"""Streaming extraction of selected theorem types from Lean4Export NDJSON.

This module deliberately indexes only names and expression byte offsets.  It
does not construct an in-memory model of an entire Lean environment, and it
does not dereference theorem proof values.
"""

from __future__ import annotations

import json
from array import array
from dataclasses import dataclass
from hashlib import sha256
from pathlib import Path
from typing import Any

from nsrw.schema_admission import validate_document

NORMALIZED_SCHEMA_ID = "flamehaven.nsrw-lean-declaration-normalized.v1"
MAX_EXPRESSION_ID = 10_000_000
MAX_NAME_ID = 1_000_000
MAX_TYPE_SUBTREE_NODES = 100_000


class LeanExportError(ValueError):
    """Raised when an export cannot be safely normalized."""


@dataclass(frozen=True)
class SourceBinding:
    """Pinned identities supplied by the caller, never inferred from source text."""

    repository_commit: str
    module: str
    declaration: str
    source_file_sha256: str
    source_manifest_sha256: str
    lean_toolchain: str
    exporter_commit: str
    exporter_binary_sha256: str

    def as_dict(self) -> dict[str, str]:
        return {
            "repository_commit": self.repository_commit,
            "module": self.module,
            "declaration": self.declaration,
            "source_file_sha256": self.source_file_sha256,
            "source_manifest_sha256": self.source_manifest_sha256,
            "lean_toolchain": self.lean_toolchain,
        }


@dataclass(frozen=True)
class _TargetDeclaration:
    kind: str
    name_id: int
    type_expression_id: int
    value_expression_id: int | None


def _reject_duplicate_keys(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
    result: dict[str, Any] = {}
    for key, value in pairs:
        if key in result:
            raise LeanExportError(f"duplicate NDJSON key: {key}")
        result[key] = value
    return result


def _parse_record(raw: bytes, line_number: int) -> dict[str, Any]:
    try:
        value = json.loads(raw.decode("utf-8"), object_pairs_hook=_reject_duplicate_keys)
    except (UnicodeDecodeError, json.JSONDecodeError) as exc:
        raise LeanExportError(f"invalid NDJSON record at line {line_number}") from exc
    if not isinstance(value, dict):
        raise LeanExportError(f"NDJSON record at line {line_number} must be an object")
    return value


def _require_int(value: Any, label: str) -> int:
    if isinstance(value, bool) or not isinstance(value, int):
        raise LeanExportError(f"{label} must be an integer")
    return value


def _ensure_offset_capacity(offsets: array, expression_id: int) -> None:
    if expression_id < 0 or expression_id > MAX_EXPRESSION_ID:
        raise LeanExportError(f"expression id outside supported bound: {expression_id}")
    if expression_id >= len(offsets):
        offsets.extend(array("Q", [0]) * (expression_id + 1 - len(offsets)))


def _name_node(record: dict[str, Any]) -> tuple[int, int, str] | None:
    if "in" not in record:
        return None
    name_id = _require_int(record["in"], "name id")
    if name_id <= 0 or name_id > MAX_NAME_ID:
        raise LeanExportError(f"name id outside supported bound: {name_id}")
    if "str" in record:
        payload = record["str"]
        if not isinstance(payload, dict):
            raise LeanExportError("name str payload must be an object")
        parent = _require_int(payload.get("pre"), "name parent")
        token = payload.get("str")
        if not isinstance(token, str) or not token:
            raise LeanExportError("name string token must be non-empty")
        return name_id, parent, token
    if "num" in record:
        payload = record["num"]
        if not isinstance(payload, dict):
            raise LeanExportError("name num payload must be an object")
        parent = _require_int(payload.get("pre"), "name parent")
        token = str(_require_int(payload.get("i"), "name numeric token"))
        return name_id, parent, token
    return None


def _is_level_record(record: dict[str, Any]) -> bool:
    """Levels are outside the type slice unless a future decoder needs them."""

    return "il" in record and any(key in record for key in ("succ", "max", "imax", "param"))


def _resolve_name(name_id: int, names: dict[int, tuple[int, str]], cache: dict[int, str]) -> str:
    if name_id == 0:
        return ""
    if name_id in cache:
        return cache[name_id]
    chain: list[tuple[int, str]] = []
    seen: set[int] = set()
    cursor = name_id
    while cursor:
        if cursor in cache:
            prefix = cache[cursor]
            break
        if cursor in seen:
            raise LeanExportError(f"cyclic Lean name reference: {name_id}")
        seen.add(cursor)
        try:
            parent, token = names[cursor]
        except KeyError as exc:
            raise LeanExportError(f"unresolved Lean name id: {cursor}") from exc
        chain.append((cursor, token))
        cursor = parent
    else:
        prefix = ""
    for current_id, token in reversed(chain):
        prefix = token if not prefix else f"{prefix}.{token}"
        cache[current_id] = prefix
    return cache[name_id]


def _declaration_record(record: dict[str, Any]) -> tuple[str, dict[str, Any]] | None:
    for kind in ("axiom", "def", "opaque", "thm", "quot", "inductive", "ctor", "recursor"):
        if kind in record:
            payload = record[kind]
            if not isinstance(payload, dict):
                raise LeanExportError(f"{kind} declaration payload must be an object")
            return kind, payload
    return None


def _child_expression_ids(kind: str, payload: Any) -> list[int]:
    if kind in {"bvar", "sort", "const", "natVal", "strVal"}:
        return []
    if not isinstance(payload, dict):
        raise LeanExportError(f"expression payload {kind} must be an object")
    fields = {
        "app": ("fn", "arg"),
        "lam": ("type", "body"),
        "forallE": ("type", "body"),
        "letE": ("type", "value", "body"),
        "proj": ("struct",),
    }
    if kind not in fields:
        return []
    return [_require_int(payload.get(field), f"{kind}.{field}") for field in fields[kind]]


def _project_expression(
    expression_id: int,
    raw_path: Path,
    offsets: array,
    names: dict[int, tuple[int, str]],
    name_cache: dict[int, str],
) -> tuple[dict[str, Any], list[int], set[str], list[dict[str, Any]]]:
    if expression_id < 0 or expression_id >= len(offsets) or not offsets[expression_id]:
        raise LeanExportError(f"missing expression record: {expression_id}")
    with raw_path.open("rb") as handle:
        handle.seek(offsets[expression_id])
        record = _parse_record(handle.readline(), 0)
    if _require_int(record.get("ie"), "expression id") != expression_id:
        raise LeanExportError(f"expression offset mismatch: {expression_id}")
    keys = [key for key in record if key != "ie"]
    if len(keys) != 1:
        raise LeanExportError(f"expression {expression_id} has ambiguous constructor")
    kind = keys[0]
    payload = record[kind]
    supported = {"bvar", "sort", "const", "app", "lam", "forallE", "letE", "proj", "natVal", "strVal"}
    if kind not in supported:
        return (
            {"expression_id": expression_id, "kind": "OPAQUE_EXPR", "children": []},
            [],
            set(),
            [{"expression_id": expression_id, "constructor": kind}],
        )

    children = _child_expression_ids(kind, payload)
    node: dict[str, Any] = {
        "expression_id": expression_id,
        "kind": kind,
        "children": children,
    }
    constants: set[str] = set()
    if kind == "bvar":
        node["debruijn_index"] = _require_int(payload, "bvar index")
    elif kind == "sort":
        node["level_id"] = _require_int(payload, "sort level")
    elif kind == "const":
        if not isinstance(payload, dict):
            raise LeanExportError("const payload must be an object")
        node["name"] = _resolve_name(_require_int(payload.get("name"), "const name"), names, name_cache)
        universe_levels = payload.get("us")
        if not isinstance(universe_levels, list):
            raise LeanExportError("const.us must be an array")
        node["universe_level_ids"] = [_require_int(item, "const universe level") for item in universe_levels]
        constants.add(node["name"])
    elif kind in {"lam", "forallE"}:
        node["name"] = _resolve_name(_require_int(payload.get("name"), f"{kind} name"), names, name_cache)
        binder_info = payload.get("binderInfo")
        if binder_info not in {"default", "implicit", "strictImplicit", "instImplicit"}:
            raise LeanExportError(f"unsupported binderInfo: {binder_info}")
        node["binder_info"] = binder_info
    elif kind == "letE":
        node["name"] = _resolve_name(_require_int(payload.get("name"), "letE name"), names, name_cache)
        nondependent = payload.get("nondep")
        if not isinstance(nondependent, bool):
            raise LeanExportError("letE.nondep must be boolean")
        node["nondependent"] = nondependent
    elif kind == "proj":
        node["type_name"] = _resolve_name(_require_int(payload.get("typeName"), "proj typeName"), names, name_cache)
        node["projection_index"] = _require_int(payload.get("idx"), "proj idx")
    elif kind in {"natVal", "strVal"}:
        if not isinstance(payload, str):
            raise LeanExportError(f"{kind} literal must be a string")
        node["literal"] = payload
    return node, children, constants, []


def normalize_declarations(
    raw_path: Path, bindings: tuple[SourceBinding, ...] | list[SourceBinding]
) -> dict[str, dict[str, Any]]:
    """Normalize selected theorem types through one two-pass streaming read.

    This is deliberately a selected-declaration interface, not a general Lean
    environment parser. Every requested declaration must be a theorem present
    in the same raw export, and each result retains its own source binding.
    """

    if not bindings:
        raise LeanExportError("at least one declaration binding is required")
    binding_by_declaration = {binding.declaration: binding for binding in bindings}
    if len(binding_by_declaration) != len(bindings):
        raise LeanExportError("duplicate requested declaration binding")

    raw_path = raw_path.resolve()
    if not raw_path.is_file():
        raise LeanExportError(f"raw export is unavailable: {raw_path}")
    names: dict[int, tuple[int, str]] = {}
    name_cache: dict[int, str] = {}
    offsets = array("Q", [0])
    metadata: dict[str, Any] | None = None
    targets: dict[str, _TargetDeclaration] = {}
    record_count = 0
    raw_hash = sha256()

    with raw_path.open("rb") as handle:
        line_number = 0
        while raw := handle.readline():
            line_number += 1
            offset = handle.tell() - len(raw)
            raw_hash.update(raw)
            record_count += 1
            record = _parse_record(raw, line_number)
            if "meta" in record:
                if metadata is not None or line_number != 1 or not isinstance(record["meta"], dict):
                    raise LeanExportError("export metadata must be the first unique record")
                metadata = record["meta"]
                continue
            name_node = _name_node(record)
            if name_node is not None:
                name_id, parent, token = name_node
                if name_id in names:
                    raise LeanExportError(f"duplicate Lean name id: {name_id}")
                names[name_id] = parent, token
                continue
            if _is_level_record(record):
                continue
            if "ie" in record:
                expression_id = _require_int(record["ie"], "expression id")
                _ensure_offset_capacity(offsets, expression_id)
                if offsets[expression_id]:
                    raise LeanExportError(f"duplicate expression id: {expression_id}")
                offsets[expression_id] = offset
                continue
            declaration_record = _declaration_record(record)
            if declaration_record is None:
                raise LeanExportError(f"unrecognized export record at line {line_number}")
            kind, payload = declaration_record
            # M5-2 only selects a theorem. Other declaration encodings,
            # including grouped inductive records, are deliberately outside
            # this narrow type-only slice.
            if kind != "thm":
                continue
            name_id = _require_int(payload.get("name"), f"{kind} declaration name")
            declaration_name = _resolve_name(name_id, names, name_cache)
            if declaration_name not in binding_by_declaration:
                continue
            if declaration_name in targets:
                raise LeanExportError(f"duplicate target declaration: {declaration_name}")
            targets[declaration_name] = _TargetDeclaration(
                kind=kind,
                name_id=name_id,
                type_expression_id=_require_int(payload.get("type"), "theorem type expression"),
                value_expression_id=_require_int(payload.get("value"), "theorem value expression"),
            )

    if metadata is None:
        raise LeanExportError("export metadata is missing")
    missing = sorted(set(binding_by_declaration).difference(targets))
    if missing:
        raise LeanExportError(f"target declaration not found: {missing[0]}")
    lean_metadata = metadata.get("lean")
    exporter_metadata = metadata.get("exporter")
    format_metadata = metadata.get("format")
    if not all(isinstance(item, dict) for item in (lean_metadata, exporter_metadata, format_metadata)):
        raise LeanExportError("export metadata is incomplete")

    normalized_by_declaration: dict[str, dict[str, Any]] = {}
    for declaration_name in (binding.declaration for binding in bindings):
        binding = binding_by_declaration[declaration_name]
        target = targets[declaration_name]
        nodes: dict[int, dict[str, Any]] = {}
        referenced_constants: set[str] = set()
        losses: list[dict[str, Any]] = []
        pending = [target.type_expression_id]
        while pending:
            expression_id = pending.pop()
            if expression_id in nodes:
                continue
            if len(nodes) >= MAX_TYPE_SUBTREE_NODES:
                raise LeanExportError("type subtree node limit exceeded")
            node, children, constants, node_losses = _project_expression(
                expression_id, raw_path, offsets, names, name_cache
            )
            nodes[expression_id] = node
            referenced_constants.update(constants)
            losses.extend(node_losses)
            pending.extend(children)

        binders: list[dict[str, Any]] = []
        cursor = target.type_expression_id
        while nodes[cursor]["kind"] == "forallE":
            node = nodes[cursor]
            binders.append(
                {
                    "name": node["name"],
                    "binder_info": node["binder_info"],
                    "type_expression_id": node["children"][0],
                }
            )
            cursor = node["children"][1]

        normalized = {
            "schema_id": NORMALIZED_SCHEMA_ID,
            "normalizer": "nsrw.m5.lean_export.v1",
            "source": binding.as_dict(),
            "export": {
                "lean_version": lean_metadata.get("version"),
                "lean_githash": lean_metadata.get("githash"),
                "exporter_name": exporter_metadata.get("name"),
                "exporter_version": exporter_metadata.get("version"),
                "exporter_commit": binding.exporter_commit,
                "exporter_binary_sha256": binding.exporter_binary_sha256,
                "format_version": format_metadata.get("version"),
                "raw_sha256": raw_hash.hexdigest(),
                "raw_bytes": raw_path.stat().st_size,
                "record_count": record_count,
            },
            "declaration": {
                "kind": target.kind,
                "name": _resolve_name(target.name_id, names, name_cache),
                "type_expression_id": target.type_expression_id,
                "value_expression_id": target.value_expression_id,
                "binders": binders,
            },
            "type_projection": {
                "root_expression_id": target.type_expression_id,
                "nodes": [nodes[key] for key in sorted(nodes)],
                "referenced_constants": sorted(referenced_constants),
            },
            "losses": losses,
            "normalization_status": "PASS" if not losses else "HELD[OPAQUE_CRITICAL_EXPR]",
        }
        validate_document(normalized, NORMALIZED_SCHEMA_ID)
        normalized_by_declaration[declaration_name] = normalized
    return normalized_by_declaration


def normalize_declaration(raw_path: Path, binding: SourceBinding) -> dict[str, Any]:
    """Normalize one theorem type through the selected-declaration reader."""

    return normalize_declarations(raw_path, [binding])[binding.declaration]


def write_normalized_declaration(path: Path, normalized: dict[str, Any]) -> None:
    """Write a deterministic normalized artifact after schema admission."""

    validate_document(normalized, NORMALIZED_SCHEMA_ID)
    payload = (json.dumps(normalized, ensure_ascii=False, indent=2, sort_keys=True) + "\n").encode("utf-8")
    path.write_bytes(payload)
