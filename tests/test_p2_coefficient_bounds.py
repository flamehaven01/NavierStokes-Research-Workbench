"""MomentBound arithmetic, adverse records and CLI checks; not source instances."""

import copy
import hashlib
import inspect
import json
import subprocess
import sys
from fractions import Fraction as F
from pathlib import Path

import pytest

from nsrw.math_kernel import p2_coefficient_bounds as producer
from nsrw.math_kernel import p2_coefficient_verify as verifier

B = F(207522463005781740692370179, 2305843009213693952)
ROOT = Path(__file__).resolve().parents[1]


@pytest.fixture
def record():
    return producer.produce_coefficient_bound_record()


@pytest.mark.parametrize("bits", [128, 256, 512])
def test_exact_result(bits):
    data = producer.produce_coefficient_bound_record(supporting_bits=bits)
    assert F(data["scaled_bounds"]["q_over_scale_lower"]) == B
    assert producer.compute_coarse_scaled_bound() == B
    assert B.numerator > 89998522 * B.denominator
    assert B.numerator < 89998523 * B.denominator
    assert F(data["constants"]["prefix_bound_upper_1"]) == (F(5, 2) + 12 * 3**9) * 3**8
    assert verifier.verify_coefficient_bound_record(data)["scaled_B"] == str(B)
    lam = F(data["inputs"]["lambda"])
    assert F(data["positive_scale"]["numerator_exponent"]) == -(F(1, 2) - 2 * lam) * (13 / lam - 3)
    assert -2 + F(63, 20) * lam < -1
    assert -13 + F(63, 20) * lam < 0


@pytest.mark.parametrize("u0,u1", [(F(1), F(0)), (F(0), F(1)), (F(2), F(3))])
def test_normalized_system_sign_and_triangle(u0, u1):
    # Synthetic exact rows, not a claimed numerical source Profile.
    e0, e1, a0, a1, t0, t1 = F(2), F(3), F(4), F(5), F(7), F(2)
    debt0, debt1 = -e0 * u0 / a0, -e1 * u1 / a1
    x1 = (debt0 - debt1) / (t0 - t1)
    x0 = debt0 - t0 * x1
    assert x0 + t1 * x1 == debt1
    scale = e1 / (a1 * (t0 - t1))
    rho_actual = e0 * a1 / (e1 * a0)
    assert x1 == scale * (u1 - rho_actual * u0)
    assert abs(x1) <= scale * (u1 + rho_actual * u0)
    if x1:
        assert -x1 != scale * (u1 - rho_actual * u0)


def test_bound_assumptions_matter():
    s, rho, h0, h1 = F(2), F(1), F(3), F(4)
    for u0, u1 in [(F(0), F(4)), (F(3), F(0)), (F(3), F(4))]:
        assert abs(s * (u1 - rho * u0)) <= s * (h1 + rho * h0)
    assert abs(s * (100 - rho * 0)) > s * (h1 + rho * h0)


@pytest.mark.parametrize("path,value", [
    (("p",), "0"),
    (("constants", "kappa_lower"), "3/4"),
    (("constants", "rho_upper"), "1/2"),
    (("constants", "prefix_bound_upper_0"), "327"),
    (("constants", "prefix_bound_upper_1"), "1"),
    (("scaled_bounds", "q_over_scale_lower"), str(B + 1)),
    (("scaled_bounds", "abs_prefix_over_scale_upper"), "0"),
    (("scaled_bounds", "main_over_scale_lower"), "100000001"),
    (("inputs", "eta"), "1/1048575"),
    (("inputs", "lambda"), "1/1000000000001"),
    (("inputs", "K"), "1"),
    (("positive_scale", "definition"), "exp(-beta1*center1)"),
    (("positive_scale", "denominator"), "D"),
    (("positive_scale", "numerator_exponent"), "-1"),
    (("positive_scale", "numerically_evaluated"), 0),
    (("positive_scale", "numerically_evaluated"), True),
    (("positive_scale", "positivity_basis"), []),
    (("source_binding", "upstream_commit"), "wrong"),
    (("source_binding", "proof_sha256", "P2_F1_MainMomentPositivity.lean"), "0" * 64),
    (("scope",), "NUMERICAL_J_CERTIFICATE"),
    (("mathematical_bridge",), "ADMITTED"),
    (("claim_status",), "CONFIRMED"),
    (("assumptions",), []),
    (("check_status",), "CONFIRMED"),
    (("supporting_arithmetic", "fractional_bits"), True),
    (("supporting_arithmetic", "fractional_bits"), 128.0),
    (("supporting_arithmetic", "fractional_bits"), 64),
    (("supporting_arithmetic", "exp_one", "lower"), "3"),
    (("supporting_arithmetic", "exp_one", "upper"), "2"),
])
def test_mutations_rejected(record, path, value):
    target = record
    for key in path[:-1]:
        target = target[key]
    target[path[-1]] = value
    with pytest.raises(ValueError):
        verifier.verify_coefficient_bound_record(record)


@pytest.mark.parametrize("value", ["1/0", "1/-2", "00", "-0", "1/1", "2/4", "1e9", " 1", "١", "9" * 1025, 1, True, None, float("nan")])
def test_bad_rationals(record, value):
    record["p"] = value
    with pytest.raises(ValueError):
        verifier.verify_coefficient_bound_record(record)


@pytest.mark.parametrize("section", [None, "constants", "scaled_bounds", "supporting_arithmetic", "positive_scale"])
@pytest.mark.parametrize("mode", ["missing", "extra", "wrong_type"])
def test_closed_schema(record, section, mode):
    target = record if section is None else record[section]
    if mode == "missing":
        del target[next(iter(target))]
    elif mode == "extra":
        target["numeric_q"] = "1"
    elif section is None:
        record = []
    else:
        record[section] = []
    with pytest.raises(ValueError):
        verifier.verify_coefficient_bound_record(record)


def test_no_producer_dependency(record, monkeypatch):
    def forbidden(*args, **kwargs):
        raise AssertionError("producer must not be called")
    monkeypatch.setattr(producer, "produce_coefficient_bound_record", forbidden)
    monkeypatch.setattr(producer, "compute_coarse_scaled_bound", forbidden)
    assert verifier.verify_coefficient_bound_record(record)["claim_status"] == "UNVERIFIED"
    assert "import p2_coefficient_bounds" not in inspect.getsource(verifier)


def test_pinned_dependency_files():
    for name, digest in verifier.PROOF_HASHES.items():
        data = (ROOT / "formal" / "p2" / name).read_bytes().replace(b"\r\n", b"\n")
        assert hashlib.sha256(data).hexdigest() == digest


@pytest.mark.parametrize("bits", [True, 128.0, 64, "128"])
def test_bad_producer_precision(bits):
    with pytest.raises(ValueError):
        producer.produce_coefficient_bound_record(supporting_bits=bits)


@pytest.mark.parametrize("raw", [b'{"x":1,"x":2}', b'{"x":{"a":1,"a":2}}', b'x', b'\xff', b' ' * 65537, b'[' * 2000 + b']' * 2000], ids=["duplicate", "nested-duplicate", "syntax", "encoding", "oversize", "depth"])
def test_malformed_json(tmp_path, raw):
    path = tmp_path / "bad.json"
    path.write_bytes(raw)
    assert verifier.main(["--input", str(path)]) == 1


@pytest.mark.parametrize("value", [float("inf"), {"x": 1 << 33}, {"x" * 129: 1}, {str(i): 0 for i in range(65)}, [0] * 65])
def test_resource_and_type_limits(value):
    with pytest.raises(ValueError):
        verifier.verify_coefficient_bound_record(value)


def test_deep_and_cyclic_objects():
    cycle = []
    cycle.append(cycle)
    with pytest.raises(ValueError):
        verifier.verify_coefficient_bound_record(cycle)
    with pytest.raises(ValueError):
        verifier.verify_coefficient_bound_record([[0] * 64 for _ in range(64)])


def test_cli_roundtrip_and_failure(tmp_path, monkeypatch):
    path = tmp_path / "record.json"
    args = ["produce", "--output", str(path)]
    assert producer.main(args) == 0
    original = path.read_bytes()
    assert producer.main(args) == 0
    assert path.read_bytes() == original
    assert verifier.main(["--input", str(path)]) == 0
    bad = json.loads(original)
    bad["p"] = "0"
    path.write_text(json.dumps(bad))
    assert verifier.main(["--input", str(path)]) == 1
    assert verifier.main(["--input", str(tmp_path / "absent")]) == 3
    assert producer.main(["produce", "--output", str(tmp_path / "absent" / "record")]) == 1
    monkeypatch.setattr(producer, "compute_coarse_scaled_bound", lambda: F(-1))
    assert producer.main(args) == 3


def test_bad_exp_support(record, monkeypatch):
    monkeypatch.setattr(producer, "exp_bounds", lambda *args: (F(1), F(4)))
    with pytest.raises(ArithmeticError):
        producer.produce_coefficient_bound_record()
    record["supporting_arithmetic"]["exp_one"] = {"lower": "1", "upper": "4"}
    monkeypatch.setattr(verifier, "exp_bounds", lambda *args: (F(1), F(4)))
    with pytest.raises(ValueError, match="support not established"):
        verifier.verify_coefficient_bound_record(record)


def test_module_entrypoints(tmp_path):
    path = tmp_path / "subprocess.json"
    for module, args in [
        ("p2_coefficient_bounds", ["produce", "--output", str(path)]),
        ("p2_coefficient_verify", ["--input", str(path)]),
    ]:
        result = subprocess.run([sys.executable, "-m", "nsrw.math_kernel." + module, *args], capture_output=True, text=True, timeout=30)
        assert result.returncode == 0, result.stderr
    bad = subprocess.run([sys.executable, "-m", "nsrw.math_kernel.p2_coefficient_bounds", "produce", "--supporting-precision", "64", "--output", str(path)], capture_output=True, timeout=30)
    assert bad.returncode == 2


def test_context_is_fresh(record):
    original = copy.deepcopy(record)
    record["source_binding"]["proof_sha256"].clear()
    assert producer.produce_coefficient_bound_record() == original
