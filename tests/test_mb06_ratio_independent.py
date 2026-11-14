"""MB-06 second arithmetic engine (mpmath.iv) with strict scope boundaries."""
import json
from pathlib import Path

import pytest

from nsrw import mb06_ratio_crosscheck as m

RECORD = Path(__file__).resolve().parents[1] / "examples/research-verification/mb06-ratio-20261113.json"


def test_independent_algorithm_contains_recorded_ratio():
    result = m.check(RECORD.read_bytes())
    assert result["status"] == "PASS[INDEPENDENT_ALGORITHM_FACTOR_CONTAINMENT]"
    assert result["numeric_J_certified"] is False


def test_independent_algorithm_does_not_use_producer(monkeypatch):
    from nsrw.math_kernel import p2_core_scalars
    monkeypatch.setattr(p2_core_scalars, "expm1_bounds",
                        lambda *_: (_ for _ in ()).throw(AssertionError("shared backend called")))
    assert m.check(RECORD.read_bytes())["claim_authority"] == "NONE"


@pytest.mark.parametrize("field,value", [
    ("scope", "SOURCE_J_CERTIFICATE"),
    ("claim_status", "CONFIRMED"),
    ("formal_bridge", "ADMITTED"),
])
def test_claim_mutation_rejected(field, value):
    raw = json.loads(RECORD.read_text())
    raw[field] = value
    with pytest.raises(ValueError):
        m.check(json.dumps(raw).encode())


def test_false_narrow_ratio_rejected():
    raw = json.loads(RECORD.read_text())
    raw["rigorous_R_bracket"]["lower"] = "9/10"
    raw["rigorous_B_times_R_bracket"]["lower"] = str(m.B * m.Fraction(9, 10))
    with pytest.raises(ValueError):
        m.check(json.dumps(raw).encode())


def test_swapped_ratio_rejected():
    raw = json.loads(RECORD.read_text())
    raw["rigorous_R_bracket"]["lower"] = "1"
    raw["rigorous_R_bracket"]["upper"] = "2"
    raw["rigorous_B_times_R_bracket"]["lower"] = str(m.B)
    raw["rigorous_B_times_R_bracket"]["upper"] = str(2 * m.B)
    with pytest.raises(ValueError):
        m.check(json.dumps(raw).encode())


def test_invalid_json_duplicate_key_rejected():
    with pytest.raises(ValueError):
        m.check(b'{"scope":"a","scope":"b"}')


@pytest.mark.parametrize(
    ("field", "value"),
    [
        ("format", "unknown"),
        ("input", {}),
        ("source_binding", {}),
        ("ratio", "inverted"),
        ("precision_fractional_bits", 64),
        ("rigorous_R_bracket", {"lower": "1/0", "upper": "2"}),
        ("rigorous_R_bracket", {"lower": False, "upper": "2"}),
    ],
)
def test_invalid_ratio_inputs_are_rejected(field, value):
    raw = json.loads(RECORD.read_bytes())
    raw[field] = value
    with pytest.raises(ValueError):
        m.check(json.dumps(raw).encode())


def test_standalone_ratio_cli_exit_codes(tmp_path, capsys):
    assert m.main([str(RECORD)]) == 0
    assert json.loads(capsys.readouterr().out)["status"].startswith("PASS")
    assert m.main([str(tmp_path / "absent.json")]) == 1
    assert json.loads(capsys.readouterr().err)["status"] == "REJECT"
