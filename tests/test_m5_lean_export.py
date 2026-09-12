from __future__ import annotations

import json
import os
from pathlib import Path

import pytest

from nsrw.m5.h_scaling import run_h_scaling_reconstruction
from nsrw.m5.lean_export import (
    LeanExportError,
    SourceBinding,
    normalize_declaration,
    normalize_declarations,
    write_normalized_declaration,
)
from nsrw.schema_admission import validate_document


def _binding(declaration: str = "NavierStokes.OutgoingDilation.H_scaling") -> SourceBinding:
    return SourceBinding(
        repository_commit="a" * 40,
        module="NavierStokes.OutgoingDilation",
        declaration=declaration,
        source_file_sha256="b" * 64,
        source_manifest_sha256="c" * 64,
        lean_toolchain="leanprover/lean4:v4.34.0-rc2",
        exporter_commit="d" * 40,
        exporter_binary_sha256="e" * 64,
    )


def _record(identifier: int, parent: int, token: str) -> dict[str, object]:
    return {"in": identifier, "str": {"pre": parent, "str": token}}


def _export_records(
    *,
    opaque_root: bool = False,
    duplicate_expression: bool = False,
    extra_declaration: str | None = None,
) -> list[dict[str, object]]:
    records: list[dict[str, object]] = [
        {
            "meta": {
                "exporter": {"name": "lean4export", "version": "3.1.0"},
                "lean": {"githash": "f" * 40, "version": "4.34.0-rc2"},
                "format": {"version": "3.1.0"},
            }
        },
        _record(1, 0, "NavierStokes"),
        _record(2, 1, "OutgoingDilation"),
        _record(3, 2, "H_scaling"),
        _record(4, 0, "F"),
        _record(5, 0, "XR"),
        _record(6, 0, "hXR"),
        _record(7, 0, "p"),
        _record(8, 0, "Profile"),
        _record(9, 0, "Real"),
        _record(10, 0, "Proof"),
        {"const": {"name": 8, "us": []}, "ie": 11},
        {"const": {"name": 9, "us": []}, "ie": 12},
        {"const": {"name": 10, "us": []}, "ie": 13},
        {"forallE": {"name": 7, "type": 12, "body": 13, "binderInfo": "default"}, "ie": 14},
        {"forallE": {"name": 6, "type": 13, "body": 14, "binderInfo": "default"}, "ie": 15},
        {"forallE": {"name": 5, "type": 12, "body": 15, "binderInfo": "default"}, "ie": 16},
        {"forallE": {"name": 4, "type": 11, "body": 16, "binderInfo": "default"}, "ie": 17},
    ]
    if extra_declaration is not None:
        records.insert(9, _record(18, 2, extra_declaration))
    if opaque_root:
        records.append({"mdata": {"expr": 17, "data": {}}, "ie": 18})
        type_expression = 18
    else:
        type_expression = 17
    if duplicate_expression:
        records.append({"const": {"name": 9, "us": []}, "ie": 17})
    records.append(
        {
            "thm": {
                "name": 3,
                "levelParams": [],
                "type": type_expression,
                "value": 999,
                "all": [3],
            }
        }
    )
    if extra_declaration is not None:
        records.append(
            {
                "thm": {
                    "name": 18,
                    "levelParams": [],
                    "type": type_expression,
                    "value": 998,
                    "all": [18],
                }
            }
        )
    return records


def _write_export(path: Path, records: list[dict[str, object]]) -> None:
    path.write_bytes(
        b"".join(json.dumps(record, separators=(",", ":")).encode("utf-8") + b"\n" for record in records)
    )


def test_normalizer_reads_only_theorem_type_subtree(tmp_path: Path) -> None:
    raw = tmp_path / "export.ndjson"
    _write_export(raw, _export_records())

    normalized = normalize_declaration(raw, _binding())

    validate_document(normalized, "flamehaven.nsrw-lean-declaration-normalized.v1")
    assert normalized["normalization_status"] == "PASS"
    assert normalized["declaration"]["value_expression_id"] == 999
    assert [binder["name"] for binder in normalized["declaration"]["binders"]] == [
        "F",
        "XR",
        "hXR",
        "p",
    ]
    assert normalized["type_projection"]["referenced_constants"] == ["Profile", "Proof", "Real"]
    assert all(node["expression_id"] != 999 for node in normalized["type_projection"]["nodes"])


def test_batch_normalizer_projects_selected_theorems_from_one_raw_export(tmp_path: Path) -> None:
    raw = tmp_path / "batch.ndjson"
    second = "J_scaling"
    _write_export(raw, _export_records(extra_declaration=second))

    normalized = normalize_declarations(
        raw,
        [
            _binding(),
            _binding(f"NavierStokes.OutgoingDilation.{second}"),
        ],
    )

    assert set(normalized) == {
        "NavierStokes.OutgoingDilation.H_scaling",
        "NavierStokes.OutgoingDilation.J_scaling",
    }
    assert normalized["NavierStokes.OutgoingDilation.H_scaling"]["export"]["raw_sha256"] == normalized[
        "NavierStokes.OutgoingDilation.J_scaling"
    ]["export"]["raw_sha256"]


def test_batch_normalizer_fails_when_one_selected_theorem_is_absent(tmp_path: Path) -> None:
    raw = tmp_path / "missing.ndjson"
    _write_export(raw, _export_records())

    with pytest.raises(LeanExportError, match="target declaration not found"):
        normalize_declarations(
            raw,
            [
                _binding(),
                _binding("NavierStokes.OutgoingDilation.J_scaling"),
            ],
        )


def test_batch_normalizer_fails_closed_on_a_truncated_ndjson_export(tmp_path: Path) -> None:
    raw = tmp_path / "truncated.ndjson"
    complete = _export_records()
    _write_export(raw, complete)
    raw.write_bytes(raw.read_bytes() + b'{"thm":{"name":3')

    with pytest.raises(LeanExportError, match="invalid NDJSON record"):
        normalize_declarations(raw, [_binding()])


def test_opaque_type_node_is_explicit_and_held(tmp_path: Path) -> None:
    raw = tmp_path / "opaque.ndjson"
    _write_export(raw, _export_records(opaque_root=True))

    normalized = normalize_declaration(raw, _binding())

    assert normalized["normalization_status"] == "HELD[OPAQUE_CRITICAL_EXPR]"
    assert normalized["losses"] == [{"expression_id": 18, "constructor": "mdata"}]


def test_normalized_writer_is_deterministic(tmp_path: Path) -> None:
    raw = tmp_path / "deterministic.ndjson"
    _write_export(raw, _export_records())
    normalized = normalize_declaration(raw, _binding())
    first = tmp_path / "first.json"
    second = tmp_path / "second.json"

    write_normalized_declaration(first, normalized)
    write_normalized_declaration(second, normalized)

    assert first.read_bytes() == second.read_bytes()
    assert b"\r\n" not in first.read_bytes()
    assert first.read_bytes().endswith(b"\n")


def test_duplicate_expression_id_fails_closed(tmp_path: Path) -> None:
    raw = tmp_path / "duplicate.ndjson"
    _write_export(raw, _export_records(duplicate_expression=True))

    with pytest.raises(LeanExportError, match="duplicate expression id"):
        normalize_declaration(raw, _binding())


def test_actual_h_scaling_export_when_explicitly_provided() -> None:
    raw_path = os.environ.get("NSRW_M5_RAW_EXPORT")
    if not raw_path:
        pytest.skip("set NSRW_M5_RAW_EXPORT to run the external raw-export integration check")

    binding = SourceBinding(
        repository_commit="8937a8f4cbc7abaab5e9e97d1cc7f5d2319d9538",
        module="NavierStokes.OutgoingDilation",
        declaration="NavierStokes.OutgoingDilation.H_scaling",
        source_file_sha256="be46401810940d1021c2f2ccf0ce00bdffef82d413f2146742564d15c5516438",
        source_manifest_sha256="d8d5387db4bfe8dcdd867d1c4979d2911f194dfe8dae3012463c620e19c6001f",
        lean_toolchain="leanprover/lean4:v4.34.0-rc2",
        exporter_commit="cacf989bd75f608700820f6afc595f32e7a99a4d",
        exporter_binary_sha256="a638952892fede28e6b530243dc4f15a5d0fddd988f3f2494ded812249315234",
    )
    normalized = normalize_declaration(Path(raw_path), binding)

    assert normalized["normalization_status"] == "PASS"
    assert normalized["export"]["raw_sha256"] == (
        "129f7dee6cf93f3588c4cceb13d55cb88345f39b525bfbbd58031eb0f7cd0148"
    )
    assert normalized["declaration"]["type_expression_id"] == 4127204
    assert normalized["declaration"]["value_expression_id"] == 4127601
    assert len(normalized["type_projection"]["nodes"]) == 78
    receipt = run_h_scaling_reconstruction(normalized)
    assert receipt["check_status"] == "PASS"
    assert all(mutation["detected"] for mutation in receipt["mutations"])
