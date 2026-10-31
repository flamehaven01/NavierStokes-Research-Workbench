from __future__ import annotations

import copy
import json
import subprocess
import sys
from fractions import Fraction as F
from pathlib import Path

import pytest

from nsrw.math_kernel.p2_core_scalars import (
    ETA,
    LAM,
    UNRESOLVED,
    _positive_product,
    _round,
    _small_exp,
    exp_bounds,
    expm1_bounds,
    main,
    positive_main_ratio_lower,
    produce_core_scalar_certificate,
    verify_core_scalar_certificate,
)


def direct_series_reference(x: F) -> tuple[F, F]:
    """A separate direct-series path: no range reduction or dyadic rounding.

    At N=256 and |x|<=16 the remaining term ratios are below 1/2,
    so twice the next positive term bounds the entire remainder.
    """
    positive = abs(x)
    term, total = F(1), F(1)
    for n in range(1, 257):
        term *= positive / n
        total += term
    tail = 2 * term * positive / 257
    return (total, total + tail) if x >= 0 else (1 / (total + tail), 1 / total)


@pytest.mark.parametrize("x", [F(-16), F(-13), F(-23, 20), F(0), F(1, 2), F(1), F(16)])
def test_exp_encloses_tighter_direct_series(x: F) -> None:
    lo, hi = exp_bounds(x)
    a, b = direct_series_reference(x)
    assert 0 < lo <= a <= b <= hi


@pytest.mark.parametrize("bits", [128, 256, 512])
def test_fixed_certificate_positive_at_each_declared_precision(bits: int) -> None:
    record = produce_core_scalar_certificate(bits)
    assert verify_core_scalar_certificate(record)["verdict"] == "ACCEPT"
    for key in ("ell", "v", "plateau_width", "weight_gap", "main_denominator"):
        assert 0 < F(record[key]["lower"]) < F(record[key]["upper"])
    assert record["scope"] == "CORE_SCALAR_ENCLOSURES_ONLY"
    assert record["unresolved"] == list(UNRESOLVED)
    assert record["inputs"]["K"] is None
    assert record["i01_lower_bound"]["exponent"] == "6499999999987"
    assert "upper" not in record["i01_lower_bound"]


@pytest.mark.parametrize("t", [F(0), 2 * LAM, 17 * LAM / 10, F(1, 2)])
def test_expm1_direct_series_and_zero(t: F) -> None:
    lo, hi = expm1_bounds(t)
    a, b = direct_series_reference(t)
    assert lo <= a - 1 <= b - 1 <= hi
    if t == 0:
        assert (lo, hi) == (0, 0)


def test_outward_rounding_and_product() -> None:
    lo, hi = _round((F(-1, 3), F(1, 3)), 128)
    assert lo <= F(-1, 3) < F(1, 3) <= hi
    assert (hi - F(1, 3)) < F(1, 2**128)
    assert _positive_product((F(2), F(3)), (F(4), F(5)), 128) == (8, 15)


def test_main_ratio_uses_upper_denominator_not_lower() -> None:
    value = positive_main_ratio_lower((F(2), F(3)), (F(4), F(8)))
    assert value == F(1, 4)
    assert value != F(2, 4)
    for n in (F(2), F(3)):
        for d in (F(4), F(8)):
            assert value <= n / d
    assert positive_main_ratio_lower((F(1), F(1)), (F(3), F(3))) <= F(1, 3)


@pytest.mark.parametrize("denominator", [(F(0), F(1)), (F(-1), F(1)), (F(2), F(1))])
def test_zero_crossing_or_inverted_denominator_rejected(denominator) -> None:
    with pytest.raises(ValueError):
        positive_main_ratio_lower((F(1), F(2)), denominator)


@pytest.mark.parametrize("bits", [0, 64, 513, 128.0, True, None])
def test_unapproved_precision_rejected(bits) -> None:
    with pytest.raises(ValueError):
        produce_core_scalar_certificate(bits)


@pytest.mark.parametrize("x", [0.1, float("inf"), F(17)])
def test_float_or_out_of_range_exp_argument_rejected(x) -> None:
    with pytest.raises(ValueError):
        exp_bounds(x)


@pytest.mark.parametrize("t", [F(-1), F(1), 0.1])
def test_expm1_domain_rejected(t) -> None:
    with pytest.raises(ValueError):
        expm1_bounds(t)


def test_bad_private_arithmetic_inputs_rejected() -> None:
    with pytest.raises(ValueError):
        _small_exp(F(1), 128)
    with pytest.raises(ValueError):
        _round((F(2), F(1)), 128)
    with pytest.raises(ValueError):
        _positive_product((F(-1), F(1)), (F(1), F(2)), 128)
    with pytest.raises(ValueError):
        positive_main_ratio_lower((0.1, F(1)), (F(1), F(2)))
    with pytest.raises(ValueError):
        positive_main_ratio_lower((F(0), F(1)), (F(1), F(2)))


def test_one_quantum_forgery_rejected_without_hashes() -> None:
    record = produce_core_scalar_certificate()
    record["weight_gap"]["lower"] = str(F(record["weight_gap"]["lower"]) + F(1, 2**128))
    assert verify_core_scalar_certificate(record)["verdict"] == "REJECT"


@pytest.mark.parametrize("mutation", [
    "lambda", "inverted_windows", "zero_gap", "missing_hypothesis", "overclaim",
    "fake_i01_upper", "altered_scale", "extra_field", "missing_bound",
])
def test_changed_binding_hypothesis_and_scope_rejected(mutation: str) -> None:
    record = copy.deepcopy(produce_core_scalar_certificate())
    if mutation == "lambda":
        record["inputs"]["lambda"] = "0"
    elif mutation == "inverted_windows":
        record["ell"], record["v"] = record["v"], record["ell"]
    elif mutation == "zero_gap":
        record["weight_gap"]["lower"] = "0"
    elif mutation == "missing_hypothesis":
        record["unresolved"].pop()
    elif mutation == "overclaim":
        record["scope"] = "SOURCE_PROFILE_CERTIFICATE"
    elif mutation == "fake_i01_upper":
        record["i01_lower_bound"]["upper"] = "99999999"
    elif mutation == "altered_scale":
        record["i01_lower_bound"]["exponent"] = "1"
    elif mutation == "extra_field":
        record["J_positive"] = True
    else:
        record.pop("main_denominator")
    assert verify_core_scalar_certificate(record)["verdict"] == "REJECT"


@pytest.mark.parametrize("record", [None, [], "certificate", {"precision_fractional_bits": "128"}])
def test_nonrecord_or_wrong_precision_type_rejected(record) -> None:
    assert verify_core_scalar_certificate(record)["verdict"] == "REJECT"


def test_exact_scalar_constraints() -> None:
    assert 0 < LAM <= F(1, 120)
    assert 0 < ETA and ETA**2 <= 1
    assert 0 < LAM / 4 and 2 * (LAM / 4) < LAM


def test_cli_round_trip_and_duplicate_json_rejection(tmp_path, monkeypatch) -> None:
    monkeypatch.setenv("PYTHONPATH", str(Path(__file__).resolve().parents[1] / "src"))
    path = tmp_path / "core.json"
    base = [sys.executable, "-m", "nsrw.math_kernel.p2_core_scalars"]
    subprocess.run([*base, "produce", "--output", str(path)], check=True, capture_output=True)
    result = subprocess.run([*base, "verify", "--input", str(path)], check=True,
                            capture_output=True, text=True)
    assert json.loads(result.stdout)["verdict"] == "ACCEPT"
    path.write_text('{"precision_fractional_bits":128,"precision_fractional_bits":128}')
    result = subprocess.run([*base, "verify", "--input", str(path)], capture_output=True, text=True)
    assert result.returncode == 1
    assert "duplicate JSON key" in result.stdout
    result = subprocess.run([*base, "verify"], capture_output=True, text=True)
    assert result.returncode == 1
    result = subprocess.run([*base, "produce", "--precision", "64"], capture_output=True, text=True)
    assert result.returncode == 1


def test_cli_file_operations_in_process(tmp_path, monkeypatch) -> None:
    certificate, report = tmp_path / "core.json", tmp_path / "verification.json"
    monkeypatch.setattr(sys, "argv", ["core", "produce", "--output", str(certificate)])
    assert main() == 0
    payload = json.loads(certificate.read_text())
    assert payload["scope"] == "CORE_SCALAR_ENCLOSURES_ONLY"
    monkeypatch.setattr(sys, "argv", ["core", "verify", "--input", str(certificate),
                                     "--output", str(report)])
    assert main() == 0
    assert json.loads(report.read_text())["verdict"] == "ACCEPT"


@pytest.mark.parametrize("content", ["{", '{"a":1,"a":2}', '{"scope":"SOURCE_PROFILE_CERTIFICATE"}'])
def test_cli_malformed_or_promoted_record_is_a_failure(tmp_path, monkeypatch, capsys, content) -> None:
    certificate = tmp_path / "bad.json"
    certificate.write_text(content)
    monkeypatch.setattr(sys, "argv", ["core", "verify", "--input", str(certificate)])
    assert main() == 1
    assert json.loads(capsys.readouterr().out)["verdict"] == "REJECT"


@pytest.mark.parametrize("arguments", [["verify"], ["verify", "--input", "missing-core-record.json"],
                                        ["produce", "--precision", "64"]])
def test_cli_missing_input_or_invalid_precision_fails(monkeypatch, capsys, arguments) -> None:
    monkeypatch.setattr(sys, "argv", ["core", *arguments])
    assert main() == 1
    assert json.loads(capsys.readouterr().out)["verdict"] == "REJECT"
