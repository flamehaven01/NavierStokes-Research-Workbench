from __future__ import annotations

import json

import pytest

from nsrw.math_cli import main
from nsrw.math_kernel.experiments import run_math_self_check
from nsrw.math_kernel.manufactured import decaying_shear


def test_math_self_check_passes_without_proof_inflation() -> None:
    receipt = run_math_self_check()
    assert receipt["check_status"] == "PASS"
    assert receipt["claim_status"] == "UNVERIFIED"
    assert receipt["authority"]["global_navier_stokes_claim"] == "NOT_ESTABLISHED"
    assert set(receipt["checks"].values()) == {"PASS"}
    assert receipt["max_residual_infinity_norm"] < receipt["tolerance"]


def test_math_self_check_fails_when_tolerance_is_too_strict() -> None:
    receipt = run_math_self_check(1e-15)
    assert receipt["check_status"] == "FAIL"
    assert receipt["checks"]["manufactured_residuals"] == "FAIL"
    assert receipt["claim_status"] == "UNVERIFIED"


def test_math_self_check_rejects_bad_tolerance() -> None:
    with pytest.raises(ValueError, match="tolerance"):
        run_math_self_check(0.0)


def test_math_cli_writes_deterministic_receipt(tmp_path, capsys) -> None:
    first = tmp_path / "first.json"
    second = tmp_path / "second.json"
    assert main(["--output", str(first)]) == 0
    capsys.readouterr()
    assert main(["--output", str(second)]) == 0
    output = capsys.readouterr().out
    assert first.read_bytes() == second.read_bytes()
    assert json.loads(output)["check_status"] == "PASS"


def test_math_cli_fails_closed(capsys) -> None:
    assert main(["--tolerance", "0"]) == 1
    receipt = json.loads(capsys.readouterr().out)
    assert receipt["check_status"] == "ERROR"
    assert receipt["claim_status"] == "UNVERIFIED"


def test_decaying_shear_rejects_nonpositive_viscosity() -> None:
    with pytest.raises(ValueError, match="viscosity"):
        decaying_shear(0.0)
