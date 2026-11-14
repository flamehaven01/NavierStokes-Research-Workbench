"""MB-06 exact factor enclosures; never a numerical source Profile/J test."""
import inspect
from fractions import Fraction as F

import pytest

from nsrw.math_kernel import p2_normalized_j_factors as producer
from nsrw.math_kernel import p2_normalized_j_verify as verifier


@pytest.mark.parametrize("bits", [128, 256, 512])
def test_roundtrip_and_analytic_bracket(bits):
    obj = producer.bound_normalized_ratio(bits=bits)
    result = verifier.verify_normalized_ratio(obj)
    r = obj["rigorous_R_bracket"]
    assert result["claim_status"] == "UNVERIFIED"
    assert F(r["lower"]) > 0
    assert F(r["lower"]) <= F(r["upper"])
    assert F(obj["analytic_rational_bracket"]["lower"]) <= F(r["lower"])
    assert F(r["upper"]) <= F(obj["analytic_rational_bracket"]["upper"])
    assert F(obj["rigorous_B_times_R_bracket"]["lower"]) > 0
    assert obj["formal_bridge"] == "NOT_COMPILED_OR_ADMITTED"


@pytest.mark.parametrize("path,value", [
    (("input", "eta"), "0"),
    (("source_binding", "momentbound_execution_commit"), "tampered"),
    (("scope",), "NUMERICAL_J_CERTIFICATE"),
    (("formal_bridge",), "ADMITTED"),
    (("claim_status",), "CONFIRMED"),
    (("required_for_J",), []),
    (("precision_fractional_bits",), True),
    (("expm1_factors", "denominator_lower"), "0"),
    (("rigorous_R_bracket", "lower"), "1"),
    (("rigorous_B_times_R_bracket", "lower"), "90000000"),
    (("analytic_rational_bracket", "upper"), "1"),
])
def test_mutated_record_rejected(path, value):
    record = producer.bound_normalized_ratio()
    cur = record
    for key in path[:-1]:
        cur = cur[key]
    cur[path[-1]] = value
    with pytest.raises(ValueError):
        verifier.verify_normalized_ratio(record)


def test_closed_fields_and_verifier_independence(monkeypatch):
    r = producer.bound_normalized_ratio()
    r["numeric_J"] = "1"
    with pytest.raises(ValueError):
        verifier.verify_normalized_ratio(r)
    r.pop("numeric_J")

    def forbidden(*_args, **_kwargs):
        raise AssertionError("producer cannot be consulted")
    monkeypatch.setattr(producer, "bound_normalized_ratio", forbidden)
    assert verifier.verify_normalized_ratio(r)["verification_status"].startswith("PASS")
    assert "p2_normalized_j_factors" not in inspect.getsource(verifier)


@pytest.mark.parametrize("bits", [0, 64, True, 128.0, "128"])
def test_reject_invalid_precision(bits):
    with pytest.raises(ValueError):
        producer.bound_normalized_ratio(bits=bits)
