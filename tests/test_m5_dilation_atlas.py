from __future__ import annotations

import copy
import json
import os
from dataclasses import replace
from fractions import Fraction
from hashlib import sha256
from pathlib import Path

import pytest

import nsrw.m5.dilation_atlas as dilation_atlas
from nsrw.m5.dilation_atlas import (
    EXPORTER_IDENTITY,
    PILOT_DECLARATIONS,
    SCALING_LAWS,
    SOURCE_IDENTITY,
    AtlasLedgerNotPinnedError,
    build_dilation_atlas,
    build_static_scaling_analysis,
    compute_semantic_digests,
    degree_zero_candidates,
    scale_degree,
    source_bindings,
    validate_atlas_bindings,
    validate_law_set,
)
from nsrw.m5.lean_export import normalize_declarations

ROOT = Path(__file__).resolve().parents[1]


def _atlas_records() -> dict[str, dict[str, object]]:
    h_scaling = json.loads(
        (ROOT / "fixtures/m5/h_scaling.normalized.json").read_text(encoding="utf-8")
    )
    records: dict[str, dict[str, object]] = {}
    for law in SCALING_LAWS:
        record = copy.deepcopy(h_scaling)
        record["source"] = {
            **SOURCE_IDENTITY,
            "declaration": law.declaration,
        }
        record["export"] = {
            **record["export"],
            **EXPORTER_IDENTITY,
        }
        record["declaration"]["name"] = law.declaration
        records[law.declaration] = record
    return records


def _candidate_ledger(records: dict[str, dict[str, object]]) -> dict[str, object]:
    raw_hashes = {str(record["export"]["raw_sha256"]) for record in records.values()}
    assert len(raw_hashes) == 1
    return {
        "schema_id": dilation_atlas.ATLAS_DIGEST_LEDGER_SCHEMA_ID,
        "raw_sha256": raw_hashes.pop(),
        "semantic_digests": compute_semantic_digests(records),
    }


def test_static_analysis_has_exact_ten_laws_and_generates_a_p2_question() -> None:
    analysis = build_static_scaling_analysis()

    assert analysis["check_status"] == "PASS[LOCAL]"
    assert analysis["claim_status"] == "UNVERIFIED"
    assert len(analysis["laws"]) == 10
    assert {candidate["identifier"] for candidate in analysis["degree_zero_candidates"]} >= {
        "J_over_M_times_H",
        "XR_times_canonicalKernel",
    }
    assert "support, zero-set" in analysis["p2_question"]


def test_atlas_is_held_until_independent_digest_ledger_is_pinned() -> None:
    records = _atlas_records()

    with pytest.raises(AtlasLedgerNotPinnedError, match="HELD\\[LEDGER_NOT_INDEPENDENTLY_PINNED\\]"):
        build_dilation_atlas(records)


def test_binding_validator_accepts_a_matching_test_ledger_only_at_its_internal_boundary() -> None:
    records = _atlas_records()

    validate_atlas_bindings(records, _candidate_ledger(records))


def test_source_binding_drift_is_rejected_against_a_pre_mutation_ledger() -> None:
    records = _atlas_records()
    ledger = _candidate_ledger(records)
    records[SCALING_LAWS[0].declaration]["source"]["repository_commit"] = "0" * 40

    with pytest.raises(ValueError, match="atlas source binding mismatch"):
        validate_atlas_bindings(records, ledger)


def test_attacker_recomputed_candidate_digests_cannot_bypass_unpinned_ledger() -> None:
    records = _atlas_records()
    node = next(
        item
        for item in records[SCALING_LAWS[0].declaration]["type_projection"]["nodes"]
        if item["kind"] == "app"
    )
    node["children"] = list(reversed(node["children"]))
    attacker_digests = compute_semantic_digests(records)
    assert len(attacker_digests) == len(SCALING_LAWS)

    with pytest.raises(AtlasLedgerNotPinnedError, match="HELD\\[LEDGER_NOT_INDEPENDENTLY_PINNED\\]"):
        build_dilation_atlas(records)


def test_type_projection_mutation_is_rejected_against_a_pre_mutation_ledger() -> None:
    records = _atlas_records()
    ledger = _candidate_ledger(records)
    node = next(
        item
        for item in records[SCALING_LAWS[0].declaration]["type_projection"]["nodes"]
        if item["kind"] == "app"
    )
    node["children"] = list(reversed(node["children"]))

    with pytest.raises(ValueError, match="atlas semantic binding mismatch"):
        validate_atlas_bindings(records, ledger)


def test_raw_hash_must_match_the_pinned_ledger() -> None:
    records = _atlas_records()
    ledger = _candidate_ledger(records)
    ledger["raw_sha256"] = "0" * 64

    with pytest.raises(ValueError, match="atlas raw export does not match"):
        validate_atlas_bindings(records, ledger)


def test_build_uses_a_file_hash_pinned_test_ledger(monkeypatch: pytest.MonkeyPatch, tmp_path: Path) -> None:
    records = _atlas_records()
    payload = json.dumps(_candidate_ledger(records), sort_keys=True).encode("utf-8")
    ledger_path = tmp_path / "outgoing_dilation_atlas_digests.json"
    ledger_path.write_bytes(payload)
    monkeypatch.setattr(dilation_atlas, "ATLAS_DIGEST_LEDGER_PATH", ledger_path)
    monkeypatch.setattr(dilation_atlas, "PINNED_ATLAS_DIGEST_LEDGER_SHA256", sha256(payload).hexdigest())

    atlas = build_dilation_atlas(records)

    assert atlas["check_status"] == "PASS[PINNED_SAME_RAW]"


@pytest.mark.parametrize(
    "mutated",
    [
        replace(SCALING_LAWS[0], exponent=Fraction(7, 2)),
        replace(SCALING_LAWS[0], hypotheses=()),
        replace(SCALING_LAWS[0], coordinate_action="p.1 -> XR * p.1"),
    ],
    ids=["exponent", "hypothesis-drop", "coordinate-transform"],
)
def test_law_contract_mutations_are_rejected(mutated: object) -> None:
    laws = list(SCALING_LAWS)
    laws[0] = mutated

    with pytest.raises(ValueError, match="dilation atlas law binding mismatch"):
        validate_law_set(laws)


def test_exact_degree_algebra_is_not_float_based() -> None:
    assert scale_degree({"J": 1, "M": -1, "H": -1}) == Fraction(0)
    assert scale_degree({"canonicalKernel": 1}) == Fraction(-1)
    assert all(candidate["xr_degree"] == "0" for candidate in degree_zero_candidates())


def test_actual_atlas_export_when_explicitly_provided() -> None:
    raw_path = os.environ.get("NSRW_M5_DILATION_ATLAS_RAW_EXPORT")
    if not raw_path:
        pytest.skip("set NSRW_M5_DILATION_ATLAS_RAW_EXPORT to run the external atlas check")

    normalized = normalize_declarations(Path(raw_path), source_bindings())
    with pytest.raises(AtlasLedgerNotPinnedError, match="HELD\\[LEDGER_NOT_INDEPENDENTLY_PINNED\\]"):
        build_dilation_atlas(normalized)


def test_actual_atlas_pilot_export_when_explicitly_provided() -> None:
    raw_path = os.environ.get("NSRW_M5_DILATION_ATLAS_PILOT_RAW_EXPORT")
    if not raw_path:
        pytest.skip("set NSRW_M5_DILATION_ATLAS_PILOT_RAW_EXPORT to run the pilot atlas check")

    laws = tuple(law for law in SCALING_LAWS if law.declaration in PILOT_DECLARATIONS)
    normalized = normalize_declarations(Path(raw_path), source_bindings(laws))

    assert set(normalized) == set(PILOT_DECLARATIONS)
    assert len({record["export"]["raw_sha256"] for record in normalized.values()}) == 1
    assert all(record["normalization_status"] == "PASS" for record in normalized.values())
